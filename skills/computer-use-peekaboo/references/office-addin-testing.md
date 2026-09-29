# Testing Office.js Add-ins in Desktop PowerPoint

Verified 2026-09-29 against a sideloaded task-pane add-in ("Slaide", three variants:
`Slaide`, `Slaide (Stage)`, `Slaide (Dev)`) in desktop PowerPoint on macOS.

## The boundary question: can AX see inside the WKWebView?

**Yes.** Office add-ins on Mac render in a WKWebView, and macOS exposes their DOM through the
Accessibility tree. Peekaboo reads it with no special flag. Opening the task pane took the
interactable element count from 128 → 153, and the new nodes are the add-in's own HTML:

```
elem_18 [button]    Close Slaide (Dev)
elem_15 [group]     Slaide (Dev)
elem_19 [group]     Slaide (Dev) Office Add-ins
elem_25 [other]     Slaide - smart.AI                 ← document title
elem_32 [textField] Ask anything about this deck…  value_settable=true
elem_26 [link]      Give Feedback
elem_37 [other]     Sep 23 · c01f125                  ← build stamp rendered by the add-in
elem_146[textField] Search (Cmd + Ctrl + U)
```

Role fidelity is low: web content mostly collapses to `[other]` (AXGenericContainer) — 57 of
153 nodes in one read. But `title`/`value` strings survive, which is enough to assert on
rendered text without looking at pixels.

There are no selectors, no DOM queries, no console, no network. For assertion-heavy regression
use Playwright against Office on the web instead (below).

## Sideloaded add-ins appear as ribbon buttons

Manifests live in:

```
~/Library/Containers/com.microsoft.Powerpoint/Data/Documents/wef
```

Each sideloaded variant shows up in the AX tree as a plain `[button]` with its manifest
display name, so you can enumerate and pick them:

```bash
peekaboo see --app "Microsoft PowerPoint" --tree --no-screenshot | grep -E '\[button\].*Slaide'
```

## The working loop

Every mutating call needs `--foreground` — see the focus caveat below.

```bash
PB=peekaboo; APP="Microsoft PowerPoint"

# 1. fresh observation — element IDs are snapshot-scoped
$PB see --app "$APP" --tree --no-screenshot > /tmp/ax.txt
ID=$(grep -E '\[textField\] Ask anything' /tmp/ax.txt | grep -oE 'elem_[0-9]+' | head -1)

# 2. focus, click into the field, type
$PB app focus --app "$APP" --foreground
$PB click --on "$ID" --app "$APP" --foreground
$PB type "Create a 3-slide deck about X" --app "$APP" --foreground

# 3. VERIFY by read-back — do not trust the exit status
$PB see --app "$APP" --tree --no-screenshot | grep -i "3-slide deck"

# 4. submit, then poll for the response
$PB press "Return" --app "$APP" --foreground
$PB see --app "$APP" --tree --no-screenshot | grep -iE "error|slide [0-9]+ of"

# 5. pixels (screen mode; window mode needs the window on the active Space)
$PB see --app "$APP" --window-id <id> --no-elements --path /tmp/ppt.png
```

## Four gotchas, all verified

### 1. `type` reports failure while succeeding

```
⚠️ Action outcome is indeterminate; observe the target before retrying
Error: Typing failed after foreground setup may have changed focus.
```

…and the text is in the field. Read-back showed the string in **both** the AX textField and
the rendered web node:

```
elem_32 [textField] Ask anything about this deck… value="Create a 3-slide deck about…"
elem_34 [other]     Create a 3-slide deck about… value="Create a 3-slide deck about…"
```

Same shape from `press` (`Key press dispatched but not verified`) and `click`. **Never branch
on `success` for input commands — always re-observe and grep.** Retrying blindly double-types.

Upstream documents this: `type` "can return non-success after accepted dispatch, so read the
outcome before retrying". `--accept-dispatched` opts into it explicitly but does not confirm
delivery.

### 2. Background input is impossible in PowerPoint

```
Invalid target: The exact target window reports no focused element. Background keystrokes
follow the application's own keyboard focus and cannot be aimed at a window that does not
hold it; such a window also refuses accessibility focus requests…
```

`click --on <id>` succeeds in the background, but `type`/`press` do not. Add `--foreground` to
every input command targeting Office. That is a shared-desktop action — it moves the user's
focus — so don't do it silently in a long unattended loop.

### 3. `set-value` does not stick on framework-controlled inputs

```
The accessibility value write was accepted, but its requested result could not be verified.
```

Read-back: `value=""`. React/Vue controlled inputs ignore `AXSetValue` because no input event
fires. Use foreground `click` + `type`. `set-value` is fine for native AppKit fields.

### 4. Clearing a field

```bash
peekaboo press "cmd+a" --app "$APP" --foreground
peekaboo press "delete" --app "$APP" --foreground
```

Verified: value returns to the empty placeholder.

## Dev-server prerequisite

A `(Dev)` add-in variant points at a local server. Check it is up before blaming the add-in:

```bash
lsof -nP -iTCP -sTCP:LISTEN | grep -iE "node|vite|python"
```

A Vite dev server on `[::1]:5173` is the usual shape. When the add-in's backend is unreachable
the pane renders its own error into the DOM, and AX reads it like any other text:

```
elem_35 [other] ⚠️ Error: Load failed value="⚠️ Error: Load failed"
```

That is a clean, greppable failure signal — you do not need a screenshot to detect it.

## Native debugging of the desktop WKWebView

```bash
defaults write com.microsoft.Powerpoint OfficeWebAddinDeveloperExtras -bool true
```

Restart PowerPoint, then right-click inside the add-in → **Inspect Element** opens Safari Web
Inspector with breakpoints, console, and network for the task-pane document. This is the only
way to get real DOM/console access in the desktop host.

## When to use something else

| Goal | Tool |
|---|---|
| Desktop smoke test: ribbon → pane → type → visible response | **Peekaboo** (this file) |
| Assertion-heavy regression, DOM selectors, console, network | **Playwright** on Office on the web — the task pane is an iframe named `FlexPane_AddinsPane` (`OfficeDev/office-js#6462`), reachable cross-origin via `page.frameLocator(...).locator(...)` |
| Slide geometry / palette ground truth | LibreOffice `--convert-to pdf`, then a PDF→PNG step |
| Deck content without any UI | Read the `.pptx` directly (python-pptx) |

Keyboard-only users hit a real bug in the web host: focus cannot enter `FlexPane_AddinsPane`
sequentially. That is platform-controlled, not something the add-in can fix — worth knowing
before writing a keyboard-driven web test.
