#!/usr/bin/env python3
"""Rebuild the `aws` skill's domain references from an installed AWS skill pack.

The `aws` skill is a consolidation of 24 upstream AWS skills (installed by the AWS
agent-skills installer into ~/.agents/skills/). This script re-copies them into
references/<domain>/ and rewrites every internal markdown link so it resolves from
this skill's root. It never touches SKILL.md, ATTRIBUTION.md, references/cost-projection/
or references/<domain>/references/prompt-caching-typescript-workflow.md.

Usage:
    uv run python scripts/sync-from-aws-skills.py [--source DIR] [--check]

Exit codes: 0 = synced, 1 = --check found drift, 2 = broken links after sync.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys

# (upstream skill dir, domain dir under references/)
DOMAINS = [
    ("amazon-bedrock", "bedrock"),
    ("aws-ai-ml", "ai-ml"),
    ("aws-auth", "auth"),
    ("aws-billing-and-cost-management", "billing-and-cost"),
    ("aws-blocks", "blocks"),
    ("aws-cdk", "cdk"),
    ("aws-cloudformation", "cloudformation"),
    ("aws-compute", "compute"),
    ("aws-containers", "containers"),
    ("aws-database", "database"),
    ("aws-deployment", "deployment"),
    ("aws-iam", "iam"),
    ("aws-messaging-and-streaming", "messaging-and-streaming"),
    ("aws-networking", "networking"),
    ("aws-observability", "observability"),
    ("aws-sdk-js-v3-usage", "sdk-js-v3"),
    ("aws-sdk-python-usage", "sdk-python"),
    ("aws-sdk-swift-usage", "sdk-swift"),
    ("aws-security", "security"),
    ("aws-serverless", "serverless"),
    ("aws-storage", "storage"),
    ("aws-well-architected-review", "well-architected"),
    ("launch-with-aws", "launch"),
    ("signing-in-to-aws", "signin"),
]

# Files that live inside a domain dir but come from this repo, not from AWS.
# They are preserved across a re-sync (paths relative to references/<domain>/).
LOCAL_FILES = {
    "bedrock": ["references/prompt-caching-typescript-workflow.md"],
}

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINK = re.compile(r"\]\(([^)\s]+)\)")
LOCAL_ADDITIONS = (
    "\n\n## Local additions (not from the AWS skill pack)\n\n"
    "- [references/prompt-caching-typescript-workflow.md]"
    "(references/bedrock/references/prompt-caching-typescript-workflow.md)"
    " — concrete `ConverseStreamCommand` recipe: cachePoint on system/tools, the"
    " second-to-last-message trick for agent loops, TS discriminated-union casts,"
    " stream usage logging.\n"
)
GUARDRAIL = (
    "## Where this domain's files live\n\n"
    "This is a **local install**: every path in this file is relative to the\n"
    "`aws` skill root and reads straight off the local filesystem. The AWS MCP\n"
    "`retrieve_skill` route does not apply here — never call it for these files.\n"
)


def strip_frontmatter(text: str) -> str:
    lines = text.split("\n")
    if lines and lines[0].strip() == "---":
        for i, line in enumerate(lines[1:], 1):
            if line.strip() == "---":
                return "\n".join(lines[i + 1:])
    return text


def dedupe_mcp_guardrail(body: str) -> str:
    """Swap the 'MCP retrieve_skill vs local install' section for the local-only rule."""
    if "retrieve_skill" not in body:
        return body
    lines, out, i = body.split("\n"), [], 0
    while i < len(lines):
        line = lines[i]
        is_section_head = line.startswith("## ")
        if (
            is_section_head
            and "retrieve_skill" not in line
            and i + 8 < len(lines)
            and "retrieve_skill" in "\n".join(lines[i:i + 8])
        ):
            j = i + 1
            while j < len(lines) and not lines[j].startswith("## "):
                j += 1
            out.extend(GUARDRAIL.split("\n"))
            i = j
            continue
        out.append(line)
        i += 1
    return "\n".join(out)


class LinkRewriter:
    def __init__(self, source_root: str, domain: str) -> None:
        self.source_root = source_root
        self.domain = domain
        self.broken: list[tuple[str, str]] = []

    def rewrite(self, text: str, original_rel: str) -> str:
        original_dir = os.path.dirname(original_rel)

        def resolve(target: str) -> str | None:
            path = target.split("#", 1)[0]
            if not path.strip():
                return None
            for candidate in (
                os.path.normpath(os.path.join(original_dir, path)),
                os.path.normpath(path),
            ):
                if os.path.exists(os.path.join(self.source_root, candidate)):
                    return candidate
            return None

        def repl(match: re.Match[str]) -> str:
            target = match.group(1)
            if re.match(r"^(https?:|mailto:|#)", target):
                return match.group(0)
            anchor = ""
            if "#" in target:
                target, anchor = target.split("#", 1)
                anchor = "#" + anchor
            hit = resolve(target)
            if hit is None:
                if not re.match(r"^[<\[]|^\S*[*<>]", match.group(1)):
                    self.broken.append((original_rel, match.group(1)))
                return match.group(0)
            new_path = "references/%s/%s" % (self.domain, hit)
            new_path = new_path.replace("/SKILL.md", "/INDEX.md")
            if new_path.endswith("/SKILL.md"):
                new_path = new_path[: -len("SKILL.md")] + "INDEX.md"
            if os.path.isdir(os.path.join(SKILL_ROOT, new_path)):
                new_path += "/"
            return "](%s%s)" % (new_path, anchor)

        return LINK.sub(repl, text)


def sync_domain(source_root: str, upstream: str, domain: str) -> tuple[str, int, list]:
    src_dir = os.path.join(source_root, upstream)
    dest_dir = os.path.join(SKILL_ROOT, "references", domain)
    if not os.path.isdir(src_dir):
        return "source missing — skipped", 0, []

    preserved = {}
    for rel in LOCAL_FILES.get(domain, []):
        path = os.path.join(dest_dir, rel)
        if os.path.exists(path):
            preserved[rel] = open(path).read()

    if os.path.isdir(dest_dir):
        shutil.rmtree(dest_dir)
    os.makedirs(dest_dir)

    version = "unversioned"
    meta_path = os.path.join(src_dir, ".aws-skill-metadata")
    if os.path.exists(meta_path):
        try:
            version = json.load(open(meta_path)).get("version", version)
        except json.JSONDecodeError:
            pass

    copied = 0
    for root, dirs, files in os.walk(src_dir):
        dirs[:] = [d for d in dirs if d != ".git"]
        for name in files:
            if name == ".aws-skill-metadata":
                continue
            abs_src = os.path.join(root, name)
            rel = os.path.relpath(abs_src, src_dir)
            if rel == "SKILL.md":
                continue
            out_rel = "INDEX_src.md" if rel == "INDEX.md" else rel
            abs_dest = os.path.join(dest_dir, out_rel)
            os.makedirs(os.path.dirname(abs_dest), exist_ok=True)
            shutil.copy2(abs_src, abs_dest)
            copied += 1

    body = strip_frontmatter(open(os.path.join(src_dir, "SKILL.md")).read())
    body = dedupe_mcp_guardrail(body).lstrip("\n")
    rewriter = LinkRewriter(src_dir, domain)
    body = rewriter.rewrite(body, "SKILL.md")
    header = (
        "> **Domain: %s** — from the AWS skill `%s` (%s).\n"
        "> Every path in this file is relative to the `aws` skill root"
        " (`skills/aws/`, deployed at `~/.agents/skills/aws/`).\n\n"
        % (domain, upstream, version)
    )
    index_path = os.path.join(dest_dir, "INDEX.md")
    with open(index_path, "w") as fh:
        fh.write(header + body.rstrip("\n") + "\n")

    for root, _dirs, files in os.walk(dest_dir):
        for name in files:
            if not name.endswith(".md") or (root == dest_dir and name == "INDEX.md"):
                continue
            path = os.path.join(root, name)
            original_rel = os.path.relpath(path, dest_dir)
            text = open(path).read()
            updated = rewriter.rewrite(text, original_rel)
            if updated != text:
                open(path, "w").write(updated)

    for rel, content in preserved.items():
        path = os.path.join(dest_dir, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w").write(content)

    if domain == "bedrock" and preserved:
        text = open(index_path).read().rstrip("\n")
        open(index_path, "w").write(text + LOCAL_ADDITIONS)

    return version, copied, rewriter.broken


def check_links() -> list[tuple[str, str]]:
    broken = []
    for root, _dirs, files in os.walk(SKILL_ROOT):
        for name in files:
            if not name.endswith(".md"):
                continue
            path = os.path.join(root, name)
            for match in LINK.finditer(open(path).read()):
                target = match.group(1).split("#", 1)[0]
                if not target or re.match(r"^(https?:|mailto:)", match.group(1)):
                    continue
                # ignore prose that only looks like a link (regex fragments, <url>)
                if "." not in target and "/" not in target:
                    continue
                if not os.path.exists(os.path.join(SKILL_ROOT, target)):
                    broken.append((os.path.relpath(path, SKILL_ROOT), match.group(1)))
    return broken


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        default=os.path.expanduser("~/.agents/skills"),
        help="directory holding the installed upstream skills (default: ~/.agents/skills)",
    )
    args = parser.parse_args()

    if not os.path.isdir(args.source):
        print("source not found: %s" % args.source, file=sys.stderr)
        return 2

    broken: list[tuple[str, str]] = []
    print("%-26s %-32s %-5s %s" % ("domain", "upstream", "ver", "files"))
    for upstream, domain in DOMAINS:
        version, copied, bad = sync_domain(args.source, upstream, domain)
        broken.extend([(domain, *b) for b in bad])
        print("%-26s %-32s %-5s %s" % (domain, upstream, version, copied))

    broken.extend(check_links())
    if broken:
        print("\n%d unresolved links:" % len(broken), file=sys.stderr)
        for entry in broken[:25]:
            print("  %s" % (entry,), file=sys.stderr)
        return 2
    print("\nall local links resolve from the skill root")
    return 0


if __name__ == "__main__":
    sys.exit(main())