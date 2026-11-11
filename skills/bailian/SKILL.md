---
name: bailian
description: "Alibaba Cloud Model Studio (Bailian, DashScope) via the `bl` CLI, one skill for the whole family: image/video/speech generation and understanding, text and web search, apps and knowledge bases, personal memory, Managed Agents (agents.yaml), Sandbox, fine-tuning and model deployment, model recommendation, usage/quota/workspace/MCP/pipeline/batch, auth and config, and Bailian docs lookup. Use when the user names Bailian, 百炼, DashScope, Model Studio or `bl`, wants to generate an image or video with Qwen/Wan, asks which Bailian model to pick, or continues an existing `bl` workflow. Triggers: 百炼, 阿里云百炼, bl image, bl video, bl managed-agent, bl sandbox, bl finetune, bl usage, qwen-image, wan, TTS, 生图, 微调."
metadata:
  version: "2.8.5"
  requires:
    bins: ["bl"]
---

# Bailian (`bl`) — one skill, many references

Vendored from the 12 official `bailian-*` skills (see `ATTRIBUTION.md`). The vendor's prose still says
"the `bailian-gen` skill", "read `bailian-protocol`" and so on: read that as the matching file below
(`bailian-gen` -> `references/gen.md`). Never call `bl skill init|add|update`, they recreate the separate skills.

## Overrides to the vendor protocol

- **Pre-flight (protocol-versioning.md):** compare `metadata.version` above with `bl --version` once per session.
  On mismatch do **not** run `bl skill update`; tell the user the vendored references may be stale.
  `bl update` is fine, but it may re-link the `bailian-*` skills: tell the user to delete those symlinks again.
- **Call attribution:** `BAILIAN_SKILL_NAME=<owning-skill>` is a telemetry label. Keep the old names
  (`bailian-gen`, `bailian-cli`, ...) and use `BAILIAN_SKILL_VERSION=2.8.5`.
- **Consent first:** classify the request, confirm provider and cost, and never add `--yes` on your own
  (exit code 7 `requires_confirmation` is a stop signal). Details in protocol.md.

## Pick the job

| User wants | Read first |
|---|---|
| Any `bl` command, first run, consent, errors, language, local files | [protocol.md](references/protocol.md) |
| apps, usage/quota, auth/config, MCP, pipeline, batch, files, parsex, workspace | [cli.md](references/cli.md) |
| image, video, speech (TTS/ASR), vision, omni | [gen.md](references/gen.md) |
| which model fits a scenario | [model-recommend.md](references/model-recommend.md) |
| web search | [web-search.md](references/web-search.md) |
| knowledge base / "use my old documents" | [knowledge.md](references/knowledge.md) |
| long-term personal memory | [memory.md](references/memory.md) |
| Managed Agents, agents.yaml, Deployments | [managed-agent.md](references/managed-agent.md) |
| Sandbox instances and templates | [sandbox.md](references/sandbox.md) |
| dataset, fine-tune, export, deploy (command-level) | [finetune.md](references/finetune.md) |
| end-to-end train -> deploy loop (text/TTS/image/video) | [train-deploy.md](references/train-deploy.md) |
| model specs, prices, API params, docs lookup | [docs-wiki.md](references/docs-wiki.md) |

Rule of thumb: generation/editing and Bailian-owned resources run through `bl`; ordinary Q&A, coding and
writing stay with the host (protocol.md, "Provider selection").

## Reference files

Load the topic file first; it names the others. Every file below is flat in `references/`.

| File(s) | When to load |
|---|---|
| protocol.md, protocol-setup.md, protocol-versioning.md, protocol-issue-reporting.md | consent classes, install/auth, version pre-flight, reporting a CLI bug |
| cli.md | hub routing for the commands below |
| cmd-cli-{index,advisor,agents,alert,app,auth,batch,cmodel,config,console,decision,file,log,mcp,model,monitor,parsex,permission,pipeline,plugin,quota,search,skill,text,token-plan,update,usage,workspace}.md | flags and examples for that `bl` group (`index` = quick index and global flags) |
| gen.md, gen-video-postprocessing.md, cmd-gen-{index,image,video,speech,vision,omni}.md | media generation / understanding |
| model-recommend.md, model-recommend-{requirement-schema,samples-format,capability-codes,data-source}.md | model choice; runs `scripts/model-recommend/` |
| web-search.md | `bl search web` (model mode vs MCP mode) |
| knowledge.md, knowledge-{setup,bindings,maintenance}.md, cmd-knowledge-{index,knowledge,kscli}.md | personal knowledge base |
| memory.md, memory-{setup,profile-schema,policy}.md, memory-profile-attributes.json, cmd-memory-{index,memory}.md | personal memory |
| managed-agent.md, cmd-managed-agent-{index,managed-agent}.md | Managed Agent IaC and API |
| sandbox.md, sandbox-instance-connections.md, cmd-sandbox-{index,sandbox}.md | Sandbox |
| finetune.md, cmd-finetune-{index,dataset,finetune,deploy}.md | dataset / fine-tune / deploy commands |
| train-deploy.md, train-deploy-{text,image,video,audio,finetune,deploy}.md | the full loop; `scripts/train-deploy-wait.sh` polls jobs |
| docs-wiki.md | wiki/models/raw data in `~/.bailian/skills/bailian-docs-llm-wiki/` (not vendored) |

`<skill-dir>` in the references means the directory of this SKILL.md.

## Gotchas

- Console login (`bl auth login --console`) only knows `cn-beijing` and `ap-southeast-1`. A Frankfurt
  (`eu-central-1`) workspace needs an API key: `bl config set --key base_url` / `--key api_key`.
- The generated `cmd-*` files match `bl` 2.8.5. If `--help` disagrees, trust `--help`.
