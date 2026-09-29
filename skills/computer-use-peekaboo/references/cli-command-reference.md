# CLI Command Reference

This source-tree reference covers all 33 root commands in the upcoming v4 registry and is checked against the built binary's `--help` output. Use `peekaboo <command> --help` for every option and `peekaboo tools` for the separate MCP/agent tool catalog.

## Core commands

| Command | Purpose / subcommands |
| --- | --- |
| [`bridge`](https://github.com/openclaw/Peekaboo/blob/main/docs/commands/bridge.md) | Inspect Bridge connectivity; `status` is the default subcommand. |
| [`capture`](https://github.com/openclaw/Peekaboo/blob/main/docs/commands/capture.md) | `action`, `live`, and `video` capture workflows. |
| [`clean`](https://github.com/openclaw/Peekaboo/blob/main/docs/commands/clean.md) | Remove snapshot cache data, with `--dry-run` support. |
| [`completions`](https://github.com/openclaw/Peekaboo/blob/main/docs/commands/completions.md) | Generate zsh, bash, or fish completion scripts. |
| [`config`](https://github.com/openclaw/Peekaboo/blob/main/docs/commands/config.md) | Configuration plus `credential` and `provider` subcommand trees. |
| [`daemon`](https://github.com/openclaw/Peekaboo/blob/main/docs/commands/daemon.md) | `run`, `start`, `status`, and `stop` the headless daemon. |
| [`learn`](https://github.com/openclaw/Peekaboo/blob/main/docs/commands/learn.md) | Print the agent guide, tool catalog, and live command signatures. |
| [`permissions`](https://github.com/openclaw/Peekaboo/blob/main/docs/commands/permissions.md) | `status`, `grant`, or `request <kind>`. |
| [`screen`](https://github.com/openclaw/Peekaboo/blob/main/docs/commands/screen.md) | `list` connected displays. |
| [`tools`](https://github.com/openclaw/Peekaboo/blob/main/docs/commands/tools.md) | `list` MCP tools or `describe <name>` for one schema. |

## Interaction commands

| Command | Purpose |
| --- | --- |
| [`action`](https://github.com/openclaw/Peekaboo/blob/main/docs/commands/action.md) | Invoke a named accessibility action. |
| [`click`](https://github.com/openclaw/Peekaboo/blob/main/docs/commands/click.md) | Click an element/query or `--at x,y`. |
| [`drag`](https://github.com/openclaw/Peekaboo/blob/main/docs/commands/drag.md) | Drag between element IDs or coordinates using `--from` and `--to`. |
| [`move`](https://github.com/openclaw/Peekaboo/blob/main/docs/commands/move.md) | Move the physical pointer to `--on` or `--at`. |
| [`paste`](https://github.com/openclaw/Peekaboo/blob/main/docs/commands/paste.md) | Paste current clipboard content or atomically set, paste, and restore. |
| [`press`](https://github.com/openclaw/Peekaboo/blob/main/docs/commands/press.md) | Press xdotool-style chords or chord sequences. |
| [`scroll`](https://github.com/openclaw/Peekaboo/blob/main/docs/commands/scroll.md) | Scroll by direction, optionally on an element. |
| [`set-value`](https://github.com/openclaw/Peekaboo/blob/main/docs/commands/set-value.md) | Set an accessibility element value directly. |
| [`type`](https://github.com/openclaw/Peekaboo/blob/main/docs/commands/type.md) | Type text; standalone keys and chords belong to `press`. |

## System commands

| Command | Purpose / subcommands |
| --- | --- |
| [`app`](https://github.com/openclaw/Peekaboo/blob/main/docs/commands/app.md) | `focus`, `hide`, `launch`, `list`, `quit`, `relaunch`, `switch`, and `unhide`. |
| [`clipboard`](https://github.com/openclaw/Peekaboo/blob/main/docs/commands/clipboard.md) | `get`, `set`, `clear`, `save`, and `restore`. |
| [`dialog`](https://github.com/openclaw/Peekaboo/blob/main/docs/commands/dialog.md) | `click`, `dismiss`, `file`, `input`, and `list`. |
| [`dock`](https://github.com/openclaw/Peekaboo/blob/main/docs/commands/dock.md) | `hide`, `launch`, `list`, `right-click`, and `show`. |
| [`menu`](https://github.com/openclaw/Peekaboo/blob/main/docs/commands/menu.md) | `click` or `list` application menus. |
| [`menubar`](https://github.com/openclaw/Peekaboo/blob/main/docs/commands/menubar.md) | `click` or `list` menu-bar status items. |
| [`space`](https://github.com/openclaw/Peekaboo/blob/main/docs/commands/space.md) | `list`, `move-window`, and `switch` Spaces. |
| [`visualizer`](https://github.com/openclaw/Peekaboo/blob/main/docs/commands/visualizer.md) | Exercise the agent cursor, input HUD, and capture indicators. |
| [`window`](https://github.com/openclaw/Peekaboo/blob/main/docs/commands/window.md) | `close`, `focus`, `list`, `maximize`, `minimize`, `move`, `resize`, `restore`, and `set-bounds`. |

## Vision, AI, and MCP commands

| Command | Purpose / subcommands |
| --- | --- |
| [`see`](https://github.com/openclaw/Peekaboo/blob/main/docs/commands/see.md) | Capture pixels and element maps; use `--tree`, `--no-screenshot`, or `--no-elements` to select the observation shape. |
| [`verify`](https://github.com/openclaw/Peekaboo/blob/main/docs/commands/verify.md) | Poll stable window/element predicates; results are satisfied, unsatisfied, or unknown. |
| [`agent`](https://github.com/openclaw/Peekaboo/blob/main/docs/commands/agent.md) | `run`, `resume`, `sessions`, and `chat`; `run` is the default. |
| [`browser`](https://github.com/openclaw/Peekaboo/blob/main/docs/commands/browser.md) | Control Chrome page content through the browser MCP tool. |
| [`mcp`](https://github.com/openclaw/Peekaboo/blob/main/docs/commands/mcp.md) | Start the MCP server; `serve` is the default subcommand. |

## Shared grammar

Durations accept bare milliseconds, `ms`, or `s`: `500`, `500ms`, `2s`, and `1.5s` are equivalent forms. Coordinate input is `--at x,y`; with an app/window target it is target-relative unless `--global` is present. Modifier lists use comma-separated values such as `cmd,shift`.

Interaction commands share foreground/focus controls where relevant. Background delivery is the default when Peekaboo can resolve an exact process target; physical pointer gestures and intentional global input require `--foreground`.

## JSON result envelope

Pass `--json` (or the Commander-provided `--json-output` alias) for one stable result shape. Every response has `success`, `data` (null when unavailable), optional `error`, and `debug_logs`. Failed responses exit nonzero and include `error.code`, `error.message`, and an actionable `error.hint` when the command already knows the next step.

Once the command path identifies an action request, its result also includes a top-level `effect`: `confirmed` when existing AX/readback verification proves the result, `partial` for a partly completed multi-step action, `unverifiable` when input was dispatched without an application-level signal, `suspected_noop` when a post-check found no change, or `refused` when a safety gate prevented dispatch. Commander parse/bind failures for recognized action commands report `effect: refused`; read-only commands omit `effect`. MCP action tools expose the same canonical fields in result metadata.

When an interaction, window mutation, or application lifecycle command returns a native action receipt, JSON also includes a top-level `outcome` object. This includes click, type, scroll, `press`, `action`, `set-value`, background window geometry/lifecycle operations, and application launch, relaunch, quit, hide, unhide, focus, and switch. The object is the validated canonical projection: state, route, delivery, evidence, dispatch state/count, retry safety, escalation, refusal reason, and the derived `mutation_dispatched`, `retry_safe`, and `requires_fresh_observation` compatibility fields. The legacy top-level `effect` and failure safety fields derive from that same object. Read-only commands, older hosts, and actions without native receipts omit `outcome` rather than fabricating a receipt.
