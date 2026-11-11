# Bailian fine-tuning pipeline (`bl dataset` / `bl finetune` / `bl deploy`)

**CRITICAL — Before executing, MUST read the shared protocol in [`protocol.md`](protocol.md): Version & updates (pre-flight checklist), Call attribution (every Agent `bl` command), Setup & auth, and CLI errors: report an issue. Command details are authoritative in [`reference/`](cmd-finetune-index.md) (dataset / finetune / deploy) and `bl <command> --help` — do not guess flags. Examples in `reference/` stay bare; wrap with Call attribution when running. The whole pipeline requires an API key. If that protocol file is missing, stop and run `bl skill init`; do not guess auth/consent.**

**Call attribution:** Examples below and in `reference/` stay bare `bl …`. When running a command, wrap it with [`bailian-protocol` → Call attribution](protocol.md#call-attribution-mandatory-for-every-agent-bl-command) (bash or PowerShell). One sample for this skill (`BAILIAN_SKILL_NAME=bailian-finetune`; replace `codex` with this host). After deploy, `bl text chat` is owned by `bailian-cli`. **When copying commands into a reusable script / template / task definition, switch to the protocol `script` template (never keep `agent`); the sample below is for this-turn inline execution only. Strip attribution when handing a command to the user to paste.**

```bash
BAILIAN_CALLER_TYPE=agent BAILIAN_CALLER_NAME=codex BAILIAN_SKILL_NAME=bailian-finetune BAILIAN_SKILL_VERSION=<metadata.version> bl dataset validate --file train.jsonl
```

## End-to-end workflow (follow in order)

```
1. Validate data   bl dataset validate --file train.jsonl [--schema chatml|dpo|cpt|tts|image]
2. Upload data     bl dataset upload --file train.jsonl          # returns a file-id
3. Create job      bl finetune text|audio|image create --base-model <base> --datasets <file-id|path>
4. Watch progress  bl finetune watch --job-id ft-xxx             # or get / logs
5. Pick artifact   bl finetune checkpoints --job-id ft-xxx
6. Export model    bl finetune export --job-id ft-xxx --checkpoint ckpt-N --model-name my-model
7. Compress model  bl finetune compress templates --model my-model       # optional; full-parameter models only
                   bl finetune compress create --model my-model --template-id <template-id>
                   bl finetune compress watch --job-id quant-xxx --follow
8. Deploy service  bl deploy text|audio|image create --model-name <my-model|quantized-output> --display-name my-svc
```

- Unsure which training methods a base model supports → `bl finetune capability --base-model <base>` or `--training-type sft|sft-lora|dpo|cpt`.
- Text `--training-type` values: `sft` / `sft-lora` / `dpo` / `dpo-lora` / `cpt`. Audio bases include `cosyvoice-v3-flash`; image bases include `wan2.7-image-pro`.
- Deployment plans: audio defaults to `--plan mu`; text/image default to `lora`.
- For `risk: high` or `requires_confirmation`, follow `bailian-protocol`; never add `--yes` automatically.

## When to use which command

| Intent                                 | Command                                                                                                |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Validate / upload training data        | `bl dataset validate` / `upload` (`.jsonl` or `.zip`)                                                  |
| Dataset list / detail / delete         | `bl dataset list` / `get` / `delete`                                                                   |
| Create a fine-tuning job               | `bl finetune text\|audio\|image create`                                                                |
| Job list / detail / follow             | `bl finetune list` / `get` / `watch` / `logs`                                                          |
| Artifacts and export                   | `bl finetune checkpoints` / `export`                                                                   |
| Quantize / compress a full model       | `bl finetune compress templates` / `create` / `watch` / `get` / `logs` / `list`                        |
| Cancel / delete a compression job      | `bl finetune compress cancel` / `delete`                                                               |
| Cancel / delete a fine-tuning job      | `bl finetune cancel` / `delete`                                                                        |
| Import an external OSS LoRA model      | Hand-off: `bl cmodel import *` — hub-owned commands; see `bailian-cli` reference or `bl cmodel --help` |
| Trainable capability lookup            | `bl finetune capability`                                                                               |
| Deploy / lifecycle                     | `bl deploy text\|audio\|image create`, `list` / `get` / `update` / `scale` / `delete` / `models`       |
| Query throughput reservations          | `bl deploy list --plan ptu` / `bl deploy get`                                                          |
| Query capacity instances               | `bl deploy capacity list` / `get`                                                                      |
| Query / wait for a capacity operation  | `bl deploy operation get` / `wait`                                                                     |
| Buy / scale / renew / release capacity | `bl deploy capacity create` / `scale` / `renew` / `delete`                                             |
| Unsubscribe a prepaid instance         | `bl deploy capacity unsubscribe` (builds the billing console refund link)                              |
| Configure ModelCode overflow strategy  | `bl deploy overflow`                                                                                   |

The `capacity list` / `get`, `operation get` / `wait` and `deploy list` / `get` queries are read-only. Capacity values are kTPM; effective, configured and target capacities are distinct. `deploy list --status` filters only the fetched page locally, with the server total left unfiltered. `operation get` reports status as data; `operation wait` exits non-zero on failure or timeout and refreshes capacity after success. Use IDs returned by the API; waiting never retries a write.

The `capacity create` / `scale` / `renew` / `delete` and `overflow` commands are high-risk writes: preview with `--dry-run`, then confirm with the runtime-injected `--yes`. Each write is submitted once and never auto-retried; HTTP 200 is not success, so pass `--wait` or check `operation_status`. Scale values are one instance's absolute kTPM, not deltas or ModelCode totals, and zero is not release. `capacity delete` releases an instance but keeps the ModelCode; active prepaid instances cannot be DELETEd — run `capacity unsubscribe --instance-id <id>` to get the billing console refund link and finish there (no API exists for refunds). Release is confirmed by `deleted=true`. `overflow` applies to the whole ModelCode, not one instance. There is no estimator or standalone auto-renewal endpoint — renewal settings ride along purchase/scale/renew.

Flags, usage, and examples: see [`reference/`](cmd-finetune-index.md) or `bl <command> --help` — do not guess flags.

## Quick examples

```bash
bl dataset validate --file train.jsonl
bl dataset upload --file train.jsonl
bl finetune text create --base-model qwen3-8b --training-type sft-lora --datasets file-xxx
bl finetune watch --job-id ft-xxx
bl finetune export --job-id ft-xxx --checkpoint ckpt-3 --model-name my-qwen-sft
# Optional quantization (Beijing region; full-parameter fine-tuned models only)
bl finetune compress templates --model my-qwen-sft
bl finetune compress create --model my-qwen-sft --template-id quant-xxx --suffix int4
bl finetune compress watch --job-id quant-xxx --follow
bl deploy text create --model-name <my-qwen-sft-or-quantized-output> --display-name my-svc
```

## Common hand-offs

软 hand-off（按 skill **名**；已安装则 Read，否则 `--help` / 提示 `bl skill init`）：

- After deployment, try the model or generate content → skill `bailian-gen` (media) or `bl text chat` (fallback: `bl image\|video\|text --help`).
- Unsure which base model to pick → `bailian-model-recommend` / `bl advisor recommend`.
- Training quota / usage questions → skill `bailian-cli` (fallback: `bl quota` / `bl usage --help`).

## references

- [bailian-protocol](protocol.md) — shared protocol (install via `bl skill init`)
- [reference/](cmd-finetune-index.md) — command details
