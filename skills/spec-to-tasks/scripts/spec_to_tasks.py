#!/usr/bin/env python3
"""
Convert SPEC.md to tasks.json for Ralph Loop execution.

Parses SPEC.md format from prd-to-spec skill:
- Feature title from # Feature Spec: [Name]
- Acceptance Criteria from Given/When/Then table
- Atomic Tasks from ### TASK N: blocks
- Dependencies from Dependency Chain section

Usage:
    uv run spec_to_tasks.py [spec_path] [output_path]

Defaults:
    spec_path: scripts/ralph/SPEC.md
    output_path: scripts/ralph/tasks.json
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path


def extract_feature_title(content: str) -> str:
    """Extract feature name from '# Feature Spec: [Name]'."""
    match = re.search(r'^#\s+Feature Spec:\s*(.+)$', content, re.MULTILINE)
    return match.group(1).strip() if match else "unnamed-feature"


def slugify(text: str) -> str:
    """Convert text to slug format."""
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


def extract_acceptance_criteria(content: str) -> list[dict]:
    """Extract acceptance criteria from Given/When/Then table."""
    criteria = []

    # Find the AC table - look for header row then data rows
    table_pattern = r'\|\s*#\s*\|\s*Given\s*\|\s*When\s*\|\s*Then\s*\|.*?\n\|[-|\s]+\|\n((?:\|.*\|\n?)+)'
    match = re.search(table_pattern, content, re.IGNORECASE)

    if not match:
        return criteria

    rows = match.group(1).strip().split('\n')
    for row in rows:
        cells = [c.strip() for c in row.split('|')[1:-1]]
        if len(cells) >= 4 and cells[0]:
            criteria.append({
                "id": cells[0],
                "given": cells[1],
                "when": cells[2],
                "then": cells[3]
            })

    return criteria


def extract_tasks(content: str) -> list[dict]:
    """Extract tasks from ### TASK N: blocks."""
    tasks = []

    # Split by task headers
    task_pattern = r'###\s+TASK\s+(\d+):\s*(.+?)(?=###\s+TASK|\n##\s+|$)'
    matches = re.findall(task_pattern, content, re.DOTALL)

    for task_num, task_content in matches:
        task = parse_task_block(task_num, task_content)
        if task:
            tasks.append(task)

    return tasks


def parse_task_block(task_num: str, content: str) -> dict:
    """Parse a single task block into structured data."""
    lines = content.strip().split('\n')
    title = lines[0].strip() if lines else f"Task {task_num}"

    # Extract fields using bold markers
    description = extract_field(content, r'\*\*Description:\*\*\s*(.+?)(?=\*\*|$)')
    satisfies = extract_field(content, r'\*\*Satisfies:\*\*\s*(.+?)(?=\*\*|$)')
    dependencies = extract_field(content, r'\*\*Dependencies:\*\*\s*(.+?)(?=\*\*|$)')
    estimate = extract_field(content, r'\*\*Estimate:\*\*\s*(.+?)(?=\*\*|$)')
    verification = extract_field(content, r'\*\*Verification:\*\*\s*(.+?)(?=\*\*|$)')

    # Extract test cases
    test_cases = extract_test_cases(content)

    # Parse satisfies into list
    satisfies_list = []
    if satisfies and satisfies.lower() != 'none':
        satisfies_list = [s.strip() for s in re.split(r'[,\s]+', satisfies) if s.strip()]

    # Parse dependencies into list
    deps_list = []
    if dependencies and dependencies.lower() != 'none':
        dep_nums = re.findall(r'(?:TASK\s*)?#?(\d+)', dependencies, re.IGNORECASE)
        deps_list = [f"TASK-{int(n):03d}" for n in dep_nums]

    # Categorize based on title/description
    category = categorize_task(title + " " + (description or ""))

    return {
        "id": f"TASK-{int(task_num):03d}",
        "title": title,
        "description": description or title,
        "satisfies": satisfies_list,
        "testCases": test_cases,
        "dependencies": deps_list,
        "estimate": estimate or "4-8 hours",
        "category": category,
        "verification": verification,
        "status": "pending"
    }


def extract_field(content: str, pattern: str) -> str | None:
    """Extract a field value using regex pattern."""
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None


def extract_test_cases(content: str) -> dict:
    """Extract test cases from ✓ Happy/Error/Edge format."""
    test_cases = {}

    # Find the Test Cases section
    test_section = re.search(r'\*\*Test Cases:\*\*(.*?)(?=\*\*Dependencies|\*\*Estimate|$)', content, re.DOTALL)
    if not test_section:
        return test_cases

    test_content = test_section.group(1)

    # Parse each line looking for Happy/Error/Edge
    for line in test_content.split('\n'):
        line = line.strip()
        if not line:
            continue

        # Match "- ✓ Happy: ..." or "✓ Happy: ..." or "- Happy: ..."
        happy_match = re.match(r'^[-✓\*\s]*Happy:\s*(.+)$', line)
        error_match = re.match(r'^[-✓\*\s]*Error:\s*(.+)$', line)
        edge_match = re.match(r'^[-✓\*\s]*Edge:\s*(.+)$', line)

        if happy_match:
            test_cases["happy"] = happy_match.group(1).strip()
        elif error_match:
            test_cases["error"] = error_match.group(1).strip()
        elif edge_match:
            test_cases["edge"] = edge_match.group(1).strip()

    return test_cases


def categorize_task(text: str) -> str:
    """Categorize task based on keywords."""
    text_lower = text.lower()

    categories = [
        ("Infrastructure", ["setup", "config", "init", "schema", "migration", "database", "db"]),
        ("Backend", ["api", "endpoint", "service", "middleware", "auth", "jwt", "server"]),
        ("Frontend", ["ui", "component", "form", "render", "display", "button", "page", "view"]),
        ("Integration", ["connect", "wire", "integrate", "e2e", "end-to-end"]),
        ("Test", ["test", "verify", "audit", "security", "validation"]),
    ]

    for category, keywords in categories:
        if any(kw in text_lower for kw in keywords):
            return category

    return "Core"


def extract_phases(content: str, tasks: list[dict]) -> dict[str, int]:
    """Extract phase assignments from Dependency Chain section."""
    phases = {}

    # Find dependency chain section
    chain_match = re.search(r'##\s+Dependency Chain.*?```(.*?)```', content, re.DOTALL | re.IGNORECASE)
    if not chain_match:
        return assign_phases_by_deps(tasks)

    chain = chain_match.group(1)

    # Parse PHASE N lines
    current_phase = 1
    for line in chain.split('\n'):
        phase_match = re.match(r'PHASE\s+(\d+)', line, re.IGNORECASE)
        if phase_match:
            current_phase = int(phase_match.group(1))
            continue

        task_refs = re.findall(r'TASK\s*(\d+)', line, re.IGNORECASE)
        for ref in task_refs:
            task_id = f"TASK-{int(ref):03d}"
            phases[task_id] = current_phase

    # Fill in any missing tasks
    for task in tasks:
        if task["id"] not in phases:
            phases[task["id"]] = assign_phases_by_deps([task]).get(task["id"], 1)

    return phases


def assign_phases_by_deps(tasks: list[dict]) -> dict[str, int]:
    """Assign phases based on dependency depth."""
    phases = {}

    # Tasks with no dependencies are phase 1
    for task in tasks:
        if not task["dependencies"]:
            phases[task["id"]] = 1

    # Iterate until all tasks assigned
    for _ in range(len(tasks)):
        for task in tasks:
            if task["id"] in phases:
                continue

            dep_phases = [phases.get(dep) for dep in task["dependencies"]]
            if all(p is not None for p in dep_phases):
                phases[task["id"]] = max(dep_phases) + 1

    # Fallback for cycles or missing deps
    for task in tasks:
        if task["id"] not in phases:
            phases[task["id"]] = 99

    return phases


def infer_verification_command(task: dict) -> str:
    """Infer verification command based on category and title."""
    # Use explicit verification if provided
    if task.get("verification"):
        return task["verification"]

    category = task["category"]
    title_slug = slugify(task["title"])[:20]

    patterns = {
        "Backend": f"npm test src/api/{title_slug}.test.ts",
        "Frontend": f"npm test src/components/{title_slug}.test.tsx",
        "Integration": "npm run test:e2e",
        "Test": "npm test",
        "Infrastructure": "npm run typecheck",
    }

    return patterns.get(category, f"echo 'Verify: {task['title'][:40]}'")


def convert_spec_to_tasks(spec_content: str) -> dict:
    """Convert SPEC.md content to tasks.json structure."""
    feature_title = extract_feature_title(spec_content)
    feature_slug = slugify(feature_title)

    acceptance_criteria = extract_acceptance_criteria(spec_content)
    tasks = extract_tasks(spec_content)
    phases = extract_phases(spec_content, tasks)

    # Add phases and verification to tasks
    for task in tasks:
        task["phase"] = phases.get(task["id"], 1)
        task["verification"] = infer_verification_command(task)

    # Sort by phase, then by ID
    tasks.sort(key=lambda t: (t["phase"], t["id"]))

    phase_count = max((t["phase"] for t in tasks), default=0)

    return {
        "meta": {
            "feature": feature_slug,
            "featureTitle": feature_title,
            "source": "SPEC.md",
            "createdAt": datetime.now().isoformat(),
            "taskCount": len(tasks),
            "phaseCount": phase_count
        },
        "config": {
            "branchName": f"feat/{feature_slug}",
            "maxRetriesPerTask": 3,
            "completionPromise": "<promise>COMPLETE</promise>"
        },
        "acceptanceCriteria": acceptance_criteria,
        "tasks": tasks
    }


def print_summary(data: dict):
    """Print formatted summary of generated tasks."""
    tasks = data["tasks"]

    print(f"\n✅ Created tasks.json: {data['meta']['taskCount']} tasks in {data['meta']['phaseCount']} phases\n")
    print("| ID       | Phase | Category       | Title                              | Deps       |")
    print("|----------|-------|----------------|-----------------------------------|------------|")

    for task in tasks:
        deps = ", ".join(d.replace("TASK-", "") for d in task["dependencies"]) if task["dependencies"] else "None"
        title = task["title"][:35] + "..." if len(task["title"]) > 35 else task["title"].ljust(35)
        print(f"| {task['id']} | {task['phase']:5} | {task['category']:14} | {title} | {deps:10} |")

    print(f"\n📁 Feature: {data['meta']['featureTitle']}")
    print(f"🌿 Branch: {data['config']['branchName']}")


def main():
    # Default paths
    spec_path = Path("scripts/ralph/SPEC.md")
    output_path = Path("scripts/ralph/tasks.json")

    if len(sys.argv) > 1:
        spec_path = Path(sys.argv[1])
    if len(sys.argv) > 2:
        output_path = Path(sys.argv[2])

    if not spec_path.exists():
        print(f"❌ Error: SPEC.md not found at {spec_path}")
        print("   Run /prd-to-spec first to generate SPEC.md")
        sys.exit(1)

    spec_content = spec_path.read_text()

    # Validate required sections
    required = ["# Feature Spec:", "## Atomic Tasks", "### TASK"]
    missing = [r for r in required if r not in spec_content]
    if missing:
        print(f"❌ Error: SPEC.md missing required sections: {missing}")
        print("   Ensure SPEC.md follows prd-to-spec format")
        sys.exit(1)

    tasks_data = convert_spec_to_tasks(spec_content)

    if not tasks_data["tasks"]:
        print("❌ Error: No tasks found in SPEC.md")
        print("   Ensure tasks use format: ### TASK N: [Title]")
        sys.exit(1)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(tasks_data, indent=2))

    print_summary(tasks_data)
    print(f"\n📄 Output: {output_path}")
    print(f"🚀 Run: ./scripts/ralph/ralph.sh 20")


if __name__ == "__main__":
    main()
