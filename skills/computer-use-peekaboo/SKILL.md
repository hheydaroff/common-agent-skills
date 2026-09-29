---
name: computer-use-peekaboo
description: "Give the agent computer-use on macOS via Peekaboo: screenshots, Accessibility-tree inspection, and clicking/typing into native apps, menus, dialogs, and windows. Use when the user asks to control or automate a Mac app, drive a desktop GUI, take a screenshot of an app, read or click UI that is not in a browser, test a desktop Office/Office.js add-in, or says 'computer use', 'Peekaboo', 'click this button for me', or 'automate PowerPoint/Finder/Xcode'. Not for browser pages — use Playwright/CDP there."
---

# Computer Use with Peekaboo

Peekaboo drives native macOS apps: it captures pixels, reads the Accessibility tree, and
clicks/types/presses — from `bash`, no MCP server required.

**Not for browser page content.** For DOM, forms, console, or network in a web page use
Playwright/CDP. Peekaboo's own `browser` command exists but only when that integration is
configured.

## First run on a machine

```bash
command -v peekaboo || brew install openclaw/tap/peekaboo
peekaboo permissions status        # need Screen Recording + Accessibility + Event Synthesizing
```

Grants go to the **binary** `/opt/homebrew/bin/peekaboo` (⌘⇧G in the picker), not the terminal —
one entry covers the CLI and the Bridge daemon. After granting, `pkill -f "peekaboo daemon"`;
daemons are long-lived and cache the denial. No AI provider or API key is ever needed unless
you use `peekaboo agent`. Details: [setup-and-troubleshooting.md](references/setup-and-troubleshooting.md).

## The loop: observe → target → act → verify

```bash
PB=peekaboo; APP="Microsoft PowerPoint"

$PB app list --json                                    # resolve the target
$PB window list --app "$APP" --json                    # pick an exact window id
$PB see --app "$APP" --tree --no-screenshot            # AX text + opaque elem_NN ids
$PB click --on elem_32 --app "$APP" --foreground       # act
$PB see --app "$APP" --tree --no-screenshot | grep …   # VERIFY by read-back
```

Element and snapshot IDs are **opaque and snapshot-scoped** — re-run `see` before every action.
A successful dispatch does not prove the app changed; only a fresh observation does.

## Main commands

33 root commands; `peekaboo <cmd> --help` for options, `peekaboo tools` for the MCP catalog,
`peekaboo learn` for the built-in agent guide. Full table with every subcommand:
[cli-command-reference.md](references/cli-command-reference.md).

**Observe**
```
see              pixels + element map. --tree --no-screenshot = AX only (use this on huge
                 trees); --no-elements = pixels only; --annotate = marked-up screenshot;
                 --ocr adds Vision text; --mode screen|window|frontmost|multi|area
window list      windows of an app, with is_on_screen and bounds
app list         running apps (--include-hidden --include-background)
screen list      displays, resolution, scale
verify           poll a window/element predicate → satisfied | unsatisfied | unknown
```

**Act**
```
click            --on <elemId> | "label" | --at x,y   (--foreground for real pointer)
type             text into the focused field
press            xdotool-style chords: Return, cmd+a, cmd+shift+4
set-value        write an AX value directly (native fields only — see trap 3)
action           named AX action (AXPress, AXShowMenu…)
scroll           --direction up|down|left|right --on <elemId>
drag / move      --from/--to, pointer moves (foreground only)
paste            clipboard paste, or atomic set-paste-restore
```

**System**
```
app              focus | switch | launch | quit | relaunch | hide | unhide | list
window           focus | close | minimize | restore | move | resize | set-bounds | list
menu / menubar   click | list app menus and status items
dialog           click | dismiss | file | input | list
dock             list | launch | right-click | hide | show
space            list | switch | move-window      (needs --no-remote)
clipboard        get | set | clear | save | restore
```

**Capture / other**
```
capture          action | live | video
browser          Chrome page content via the browser MCP tool
mcp              start the MCP server
permissions      status | grant | request <kind>
bridge status    which host is serving, its perms and enabled ops
config           config + credential + provider trees
clean            clear the snapshot cache (--dry-run)
```

Shared grammar: durations take `500`, `500ms`, `2s`; coordinates are `--at x,y` in **logical
points** (target-relative unless `--global`); modifiers are comma-separated `cmd,shift`.
Ordinary `see` images are logical-1x — don't divide their coordinates by the Retina scale.

## JSON envelope

`--json` on everything. Shape: `success`, `data`, `error{code,message,hint}`, `debug_logs`,
plus `effect` (`confirmed|partial|unverifiable|suspected_noop|refused`) and an `outcome`
receipt on mutating commands. Nonzero exit on failure.

## Four traps that will burn you

1. **Input commands report failure while succeeding.** `type` returns
   `Typing failed after foreground setup may have changed focus` with the text already in the
   field; `press` returns `dispatched but not verified`. **Never branch on `success` for
   `type`/`press`/`click` — re-observe and grep.** Blind retries double-type.
2. **`targetNotFound … reason=window minimized`** means no window of that app is on the active
   screen/Space — *not* broken permissions. Check
   `window list --json | jq '.data.windows[].is_on_screen'`, then
   `app focus --foreground` and retry.
3. **`set-value` silently no-ops on React/Vue controlled inputs** ("accepted, but its requested
   result could not be verified", read-back `value=""`). Use foreground `click` + `type`.
4. **`--web-focus` is a mutation, not a read flag.** It fires an AXPress focus retry, stales the
   snapshot, and makes a tree-only `see` return zero elements.

Mutating input usually needs `--foreground` (it moves the user's focus — don't do it silently in
an unattended loop). Background delivery works for `click --on` and for `type` only when the
target window holds AX focus.

## Reference files

| File | When to load |
|---|---|
| [cli-command-reference.md](references/cli-command-reference.md) | Need the full command/subcommand table, envelope semantics, or per-command doc links |
| [official-guide.md](references/official-guide.md) | Deep rules on host selection, background input, coordinates, snapshot freshness, capture engines |
| [setup-and-troubleshooting.md](references/setup-and-troubleshooting.md) | Installing, TCC grants, daemon/host issues, `window minimized`, huge AX trees, tool ranking |
| [office-addin-testing.md](references/office-addin-testing.md) | Driving desktop PowerPoint/Word/Excel or testing an Office.js task-pane add-in |

## Attribution

Adapted from the upstream [Peekaboo agent skill](https://github.com/openclaw/Peekaboo/blob/main/skills/peekaboo/SKILL.md)
(MIT, `openclaw/Peekaboo`), vendored verbatim as `references/official-guide.md`, plus
`docs/cli-command-reference.md`. The traps, the Office add-in findings, and the setup notes are
original, measured on macOS 27.0 / Peekaboo 4.6.0.
