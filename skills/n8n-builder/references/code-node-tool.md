> **Adapted note (read first).** This reference is MCP-agnostic n8n knowledge adapted from
> [czlonkowski/n8n-skills](https://github.com/czlonkowski/n8n-skills) (MIT). It originally
> targeted the standalone **n8n-mcp** server, so it names tools like `search_nodes`,
> `get_node`, `validate_node`, `validate_workflow`, `n8n_create_workflow`, and
> `n8n_update_partial_workflow`. The MCP wired into this environment is n8n's **official
> Workflow-SDK MCP** with different names — see the mapping table in
> [mcp-workflow-tools.md](mcp-workflow-tools.md). Treat any such tool name below as a
> **concept** and map it to the official tool. The expression / Code-node / pattern /
> configuration knowledge itself is correct regardless of which MCP you use. Mentions of
> sibling docs (e.g. `DATA_ACCESS.md`, `ERROR_PATTERNS.md`) refer to **sections within this
> file** (these docs were consolidated).


# n8n Custom Code Tool

Expert guidance for writing code inside `@n8n/n8n-nodes-langchain.toolCode` — the tool an AI Agent can invoke, **not** the regular workflow Code node.

---

## ⚠️ This is NOT the Code node

The Custom Code Tool looks like a Code node in the editor — same JavaScript editor, similar layout — but it is a **completely different node** from a different package with a **different runtime contract**.

| | Code node | Custom Code Tool |
|---|---|---|
| **Node type** | `n8n-nodes-base.code` | `@n8n/n8n-nodes-langchain.toolCode` |
| **Package** | `n8n-nodes-base` | `@n8n/n8n-nodes-langchain` |
| **Invoked by** | Previous node (workflow flow) | AI Agent (LangChain) |
| **Input** | `$input.all()` — item stream | `query` — string or object from LLM |
| **Return** | `[{json: {...}}]` (items array) | **A string** |
| **`$fromAI()`** | N/A | **Not available** (see Errors) |
| **`$helpers`** | Full helpers incl. httpRequest | Not exposed to the tool sandbox |
| **State** | Per-run execution data | No `getContext`, no `$getWorkflowStaticData` |

**If you treat it like a Code node, it fails.** The rest of this skill covers the Code Tool's actual contract.

---

## Quick Start

### Minimal JavaScript Code Tool

```javascript
// `query` is whatever the AI sent (a string by default)
return `You asked: ${query}`;
```

### Minimal Python Code Tool

```python
# `_query` is whatever the AI sent (a string by default)
return f"You asked: {_query}"
```

### Essential Rules

1. **Return a string.** Numbers are auto-converted. Anything else throws `"The response property should be a string, but it is an object"`.
2. **Input variable is fixed**: `query` (JS), `_query` (Python). You cannot rename it.
3. **Do NOT use `$fromAI()`** inside the Code Tool sandbox — it throws `"No execution data available"`.
4. **Do NOT use `[{json: {...}}]`** return format — that's for Code nodes. Throws `"Wrong output type returned"`.
5. **Use a descriptive tool name** (letters/numbers/underscores, v1.1+). The agent calls the tool by its name.
6. **Write a precise description** — the LLM decides whether to invoke the tool based on it.

---

## The Two Input Modes

The Code Tool has two input shapes, controlled by `specifyInputSchema`:

### Mode 1: Unstructured (default, `specifyInputSchema: false`)

The AI passes **a single string** as `query`. If you need multiple fields, the AI has to stuff them into that one string and you parse them out. In practice, LLMs will happily pass a JSON string if your description tells them to.

```javascript
// Parse a JSON string the AI sent
let params;
try {
  params = typeof query === 'string' ? JSON.parse(query) : query;
} catch (e) {
  throw new Error('Expected a JSON object. Parser said: ' + e.message);
}
const price = Number(params.price);
const months = Number(params.months);
// ...
return JSON.stringify({ monthly_payment: /* ... */ });
```

**Pros**: simplest to set up, one field to describe.
**Cons**: no schema validation — if the LLM forgets a field, the tool throws at runtime.

**Best for**: quick prototypes, tools with one natural input (a question, a URL, a text blob).

### Mode 2: Structured (`specifyInputSchema: true`)

The tool becomes a LangChain `DynamicStructuredTool`. The LLM sees a typed argument schema and passes a **validated object** as `query`. You access fields directly.

```javascript
// query is now an object matching your schema
const price = query.price;
const months = query.months;
const residual_percent = query.residual_percent;

const monthly = computeAnnuity(price, months, residual_percent);
return JSON.stringify({ monthly_payment: monthly });
```

Schema is defined via either:
- `schemaType: "fromJson"` + `jsonSchemaExample` (n8n v≥1.3) — paste an example JSON, n8n infers the schema
- `schemaType: "manual"` + `inputSchema` — write a full JSON Schema yourself

**Pros**: LLM gets type hints, invalid calls rejected before your code runs, cleaner code.
**Cons**: a little more setup; requires n8n version with schema support.

**Best for**: production tools with multiple typed parameters (calculators, API wrappers, anything with numeric fields the LLM tends to stringify).

**See**: INPUT_SCHEMA.md for complete schema setup.

---

## Return Format

**The return value must be a string.** The LLM reads it as the tool's observation.

```javascript
// ✅ String
return "42";

// ✅ Number (auto-converted to string by n8n)
return 42;

// ✅ JSON-encoded structured result (recommended for rich output)
return JSON.stringify({ result: 42, currency: "SEK" });

// ❌ Raw object → "The response property should be a string, but it is an object"
return { result: 42 };

// ❌ Workflow item format → "Wrong output type returned"
return [{ json: { result: 42 } }];

// ❌ Array → "The response property should be a string, but it is an object"
return [1, 2, 3];
```

### Best practice: JSON-stringify structured results

When your tool has more than a trivial scalar output, return a JSON string:

```javascript
return JSON.stringify({
  monthly_payment_sek: 5405,
  loan_amount: 351920,
  total_cost_of_credit: 63295
});
```

The LLM parses JSON reliably and can pick the fields it needs to present to the user.

### Error handling: the agent reads your failures

Errors don't just stop the workflow — they go back to the LLM, which usually corrects its call and retries. Use that:

```javascript
// Option A: throw — n8n surfaces the message to the agent
if (!isFinite(price)) throw new Error('price must be a number, e.g. 439900');

// Option B: return an error string — agent reads it like any tool result
if (!isFinite(price)) return JSON.stringify({ error: 'price must be a number, e.g. 439900' });
```

Either way, write error messages **for the LLM**: state what was wrong and what a valid call looks like. A bare `throw new Error('invalid input')` wastes the retry; an instructive message usually fixes the next call.

---

## Tool Name and Description

These fields are NOT documentation — they are the **tool contract the LLM sees**. Treat them as prompt engineering.

### Name
- Must match `[A-Za-z0-9_]+` (v1.1+). No spaces, no hyphens, no emoji.
- Use a verb-y descriptive name: `calculate_car_loan`, `get_weather`, `search_orders`.
- The agent calls the tool by this name. `Code Tool` (the default) is useless — the agent won't know when to call it.

### Description
- Explain **when** to use it and **what** to send.
- If unstructured mode, **include an example of the JSON string** the LLM should send.
- If structured mode, the schema speaks for itself — just describe purpose.

**Unstructured example (JSON-in-string pattern):**
```
Deterministiskt beräknar månadskostnad för billån. Anropa med EN JSON-sträng:
{"price":439900,"down_payment":87980,"interest_rate":6.95,"months":36,"residual_percent":50}
Fält: price (SEK), down_payment (SEK), interest_rate (% per år), months, residual_percent (0-99).
```

**Structured example (schema-defined):**
```
Deterministically computes the monthly car-loan payment given price, down payment, 
annual interest rate, term, and residual percent. Use whenever the user asks for 
monthly cost, total credit cost, or loan breakdown.
```

---

## Top Errors and Fixes

### Error 1: `"There was an error: 'Cannot assign to read only property \"name\" of object: Error: No execution data available'"`

**Cause**: you called `$fromAI()` inside the Code Tool sandbox.

**Fix**: `$fromAI()` is a helper for **other** tool-enabled nodes (HTTP Request Tool, SendGrid Tool, `toolWorkflow`, etc.) — it's not exposed inside `toolCode`. Read the AI's input from `query` directly (or use `specifyInputSchema` for structured fields).

### Error 2: `"Wrong output type returned"`

**Cause**: you returned a workflow-style array like `[{ json: { ... } }]`. That's the Code **node** contract, not the Code **Tool** contract.

**Fix**: return a string. For structured data, `return JSON.stringify(output)`.

### Error 3: `"The response property should be a string, but it is an object"`

**Cause**: you returned a plain object or array.

**Fix**: `JSON.stringify()` the result, or coerce to a string.

### Error 4: AI never calls the tool

**Cause**: tool name is generic (`Code Tool`, `My Tool`) or description doesn't clearly state when to use it.

**Fix**: rename to a verb-y name (`calculate_car_loan`), and rewrite the description to explicitly state the trigger conditions (e.g. "Use this whenever the user asks about monthly cost").

### Error 5: AI sends garbage into `query`

**Cause**: unstructured tool with a vague description. The LLM guesses at the format.

**Fix**: either (a) include a concrete JSON example in the description, or (b) switch to `specifyInputSchema: true` so the LLM gets a typed schema.

**See**: ERROR_PATTERNS.md for full catalog with reproductions.

---

## What's NOT Available in the Sandbox

The Code Tool sandbox is **narrower** than the Code node sandbox. Don't assume helpers carry over:

| Helper | Code node | Code Tool |
|---|---|---|
| `$input.all()`, `$input.first()`, `$input.item` | ✅ | ❌ |
| `$node["NodeName"]` | ✅ | ❌ |
| `$json`, `$binary` | ✅ | ❌ |
| `$fromAI()` | ❌ | ❌ (despite sitting next to an AI agent) |
| `$helpers.httpRequest()` | ✅ | ❌ |
| `DateTime` (Luxon) | ✅ | ✅ (standard in JS sandbox) |
| `$jmespath()` | ✅ | ❌ |
| `this.getContext(...)` | ✅ | ❌ |
| `$getWorkflowStaticData(...)` | ✅ | ❌ |

**Implication**: the Code Tool is for **pure computation**. If you need an HTTP call, an API lookup, or cross-invocation state, use a different tool node:
- HTTP Request Tool for external API calls
- `toolWorkflow` (Call Sub-workflow Tool) for multi-step logic with access to the full Code node sandbox
- MCP / database tools for persistent state

---

## When to Use Code Tool vs Alternatives

Use **Code Tool** when:
- ✅ Pure deterministic computation (math, parsing, formatting, validation)
- ✅ Lightweight transformations the LLM shouldn't do itself (precision math, regex)
- ✅ You want the code inline in the workflow, not in a separate sub-workflow

Use **`toolWorkflow`** (Call Sub-workflow Tool) when:
- ✅ You need multiple parameters with clean `$fromAI()` typing
- ✅ You need access to `$helpers`, credentials, or other nodes
- ✅ Logic is reusable across agents
- ✅ You want structured typed inputs WITHOUT writing a JSON Schema

Use **HTTP Request Tool** when:
- ✅ The tool is fundamentally a single API call
- ✅ You want per-parameter `$fromAI()` bindings in URL/query/body

**Rule of thumb**: if you find yourself wanting `$fromAI()`, you probably want `toolWorkflow` instead of `toolCode`.

---

## Complete Working Example

A production calculator tool (unstructured, JSON-in-string pattern):

```json
{
  "parameters": {
    "name": "calculate_car_loan",
    "description": "Computes monthly car-loan payment using an annuity formula with residual/balloon. Call with a single JSON string. Example: {\"price\":439900,\"down_payment\":87980,\"interest_rate\":6.95,\"months\":36,\"residual_percent\":50,\"setup_fee\":695,\"monthly_admin_fee\":59}. Required: price, down_payment, interest_rate, months, residual_percent. Optional: setup_fee, monthly_admin_fee (default 0).",
    "language": "javaScript",
    "jsCode": "let params;\ntry {\n  params = typeof query === 'string' ? JSON.parse(query) : query;\n} catch (e) {\n  throw new Error('Invalid JSON: ' + e.message);\n}\n\nconst price           = Number(params.price);\nconst down_payment    = Number(params.down_payment);\nconst interest_rate   = Number(params.interest_rate);\nconst months          = Number(params.months);\nconst residual_percent= Number(params.residual_percent);\nconst setup_fee       = Number(params.setup_fee ?? 0) || 0;\nconst monthly_admin_fee = Number(params.monthly_admin_fee ?? 0) || 0;\n\nif (!isFinite(price) || price <= 0) throw new Error('price must be > 0');\nif (down_payment < 0 || down_payment >= price) throw new Error('down_payment must be in [0, price)');\n\nconst principal = price - down_payment;\nconst residual  = price * (residual_percent / 100);\nconst r = interest_rate / 100 / 12;\nconst growth = Math.pow(1 + r, months);\nconst base = r === 0\n  ? (principal - residual) / months\n  : (principal - residual / growth) * r / (1 - 1 / growth);\nconst monthly_payment = base + monthly_admin_fee;\n\nreturn JSON.stringify({\n  monthly_payment_sek: Math.round(monthly_payment),\n  loan_amount: Math.round(principal),\n  residual_value_sek: Math.round(residual),\n  total_cost_of_credit: Math.round(monthly_payment * months + residual + setup_fee - principal)\n});"
  },
  "type": "@n8n/n8n-nodes-langchain.toolCode",
  "typeVersion": 1.3,
  "name": "calculate_car_loan"
}
```

Wire it into an AI Agent via the `ai_tool` connection type.

---

## Integration with Other Skills

**n8n-code-javascript**: the Code **node** skill. Most JavaScript patterns (arrays, map/filter, DateTime) transfer — but I/O contract is different. Don't copy data-access code.

**n8n-node-configuration**: `specifyInputSchema` is a classic displayOptions-driven conditional field. Use `get_node({detail: "standard"})` on `@n8n/n8n-nodes-langchain.toolCode` to see schema-related properties.

**n8n-workflow-patterns**: Code Tool sits inside the "AI Agent with tools" pattern. An agent typically has several tools; Code Tool is the "local compute" option.

**n8n-validation-expert**: the three Code Tool errors listed above have clear signatures — if validation surfaces "Wrong output type returned", you know to switch from array-of-items to a string.

---

## Quick Reference Checklist

Before deploying a Code Tool:

- [ ] **Node type** is `@n8n/n8n-nodes-langchain.toolCode` (not `nodes-base.code`)
- [ ] **Tool name** is descriptive, verb-y, snake_case (e.g. `calculate_car_loan`)
- [ ] **Description** states when to use the tool and (if unstructured) shows a JSON example
- [ ] **Input** read from `query` (JS) or `_query` (Python)
- [ ] **No `$fromAI()`** in the code body
- [ ] **No `$input` / `$json` / `$helpers`** — those aren't in the sandbox
- [ ] **Return** is a string (use `JSON.stringify()` for structured output)
- [ ] **Wired** into an AI Agent via `ai_tool` connection
- [ ] **Tested** with the exact kind of input the LLM will send (JSON in a string, or schema-validated object)

---

## Additional Resources

- INPUT_SCHEMA.md — structured input (DynamicStructuredTool) in depth
- ERROR_PATTERNS.md — full error catalog with causes and fixes

### Official sources
- [n8n Custom Code Tool docs](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.toolcode/)
- [ToolCode source](https://github.com/n8n-io/n8n/blob/master/packages/%40n8n/nodes-langchain/nodes/tools/ToolCode/ToolCode.node.ts) — the sandbox contract
- [LangChain tool docs](https://js.langchain.com/docs/modules/agents/tools/) — DynamicTool / DynamicStructuredTool

---

**Remember**: the Code Tool is a LangChain tool wearing a Code-node UI. Contract is: **string in, string out**. Everything else follows from that.


---

# Input Schema for Code Tool (Structured Mode)

How to turn `@n8n/n8n-nodes-langchain.toolCode` into a **DynamicStructuredTool** so the LLM passes typed arguments instead of a free-form string.

---

## Why use a schema?

Without a schema, the Code Tool is a LangChain `DynamicTool`:
- LLM sees: "one string argument called query"
- You must parse whatever the LLM sends
- Typos, missing fields, wrong types are your problem at runtime

With a schema, the Code Tool becomes a `DynamicStructuredTool`:
- LLM sees: a typed object with named fields and descriptions
- Runtime rejects invalid calls before your code runs
- Numeric fields stay numeric (no more `Number(params.price)` for every field)
- Tool calls are more reliable — most modern LLMs handle structured tools better than "here's a JSON string please"

**Cost**: a little config to define the schema, and the node must be on a version that supports it.

---

## Enabling the schema

Set `specifyInputSchema: true` on the `toolCode` parameters. Two schema-definition styles:

### Style A: `fromJson` — paste a representative example (v≥1.3, recommended)

The easiest. Give n8n an example JSON, and it infers the schema for you.

```json
{
  "parameters": {
    "name": "calculate_car_loan",
    "description": "Computes monthly car-loan payment using an annuity formula with optional balloon.",
    "language": "javaScript",
    "specifyInputSchema": true,
    "schemaType": "fromJson",
    "jsonSchemaExample": "{\n  \"price\": 439900,\n  \"down_payment\": 87980,\n  \"interest_rate\": 6.95,\n  \"months\": 36,\n  \"residual_percent\": 50,\n  \"setup_fee\": 695,\n  \"monthly_admin_fee\": 59\n}",
    "jsCode": "// query is now a validated OBJECT, not a string\nconst { price, down_payment, interest_rate, months, residual_percent, setup_fee = 0, monthly_admin_fee = 0 } = query;\n\nconst principal = price - down_payment;\nconst residual  = price * (residual_percent / 100);\nconst r = interest_rate / 100 / 12;\nconst growth = Math.pow(1 + r, months);\nconst base = r === 0\n  ? (principal - residual) / months\n  : (principal - residual / growth) * r / (1 - 1 / growth);\nconst monthly_payment = base + monthly_admin_fee;\n\nreturn JSON.stringify({\n  monthly_payment_sek: Math.round(monthly_payment),\n  loan_amount: Math.round(principal)\n});"
  },
  "type": "@n8n/n8n-nodes-langchain.toolCode",
  "typeVersion": 1.3,
  "name": "calculate_car_loan"
}
```

**How it works**: n8n looks at the example, infers `{price: number, down_payment: number, ...}`, and generates a JSON Schema. The LLM sees that schema and passes a validated object.

### Style B: `manual` — write the JSON Schema yourself

Use when you need descriptions per field, enums, min/max constraints, or optional fields.

```json
{
  "parameters": {
    "name": "calculate_car_loan",
    "description": "Computes monthly car-loan payment.",
    "language": "javaScript",
    "specifyInputSchema": true,
    "schemaType": "manual",
    "inputSchema": "{\n  \"type\": \"object\",\n  \"required\": [\"price\", \"down_payment\", \"interest_rate\", \"months\", \"residual_percent\"],\n  \"properties\": {\n    \"price\": { \"type\": \"number\", \"description\": \"Car price in SEK\" },\n    \"down_payment\": { \"type\": \"number\", \"description\": \"Down payment in SEK\" },\n    \"interest_rate\": { \"type\": \"number\", \"description\": \"Annual nominal rate in percent, e.g. 6.95\" },\n    \"months\": { \"type\": \"integer\", \"minimum\": 1, \"description\": \"Loan term in months\" },\n    \"residual_percent\": { \"type\": \"number\", \"minimum\": 0, \"maximum\": 99, \"description\": \"Balloon as % of price\" },\n    \"setup_fee\": { \"type\": \"number\", \"default\": 0 },\n    \"monthly_admin_fee\": { \"type\": \"number\", \"default\": 0 }\n  }\n}",
    "jsCode": "const { price, down_payment, interest_rate, months, residual_percent, setup_fee = 0, monthly_admin_fee = 0 } = query;\n// ... same computation as above ...\nreturn JSON.stringify({ monthly_payment_sek: /*...*/ });"
  },
  "type": "@n8n/n8n-nodes-langchain.toolCode",
  "typeVersion": 1.3,
  "name": "calculate_car_loan"
}
```

**When `manual` is worth it**:
- You want per-field `description` strings (the LLM reads these)
- You need `enum` values (e.g. currency: `["SEK", "EUR", "USD"]`)
- You need numeric constraints (`minimum`, `maximum`)
- You want to mark fields as optional cleanly

---

## How `query` behaves with a schema

Source of truth from the ToolCode sandbox:

```typescript
const sandbox = new JsTaskRunnerSandbox(workflowMode, ctx, undefined, { query });
```

The sandbox always receives `{ query }`. The difference is what `query` holds:

| Mode | Type of `query` | How to use |
|---|---|---|
| No schema | `string` | `JSON.parse(query)` if you want structure |
| With schema | `object` (validated) | Destructure: `const { price, months } = query;` |

In Python, the same applies — `_query` is a string without schema, a dict with schema.

---

## Schema version compatibility

- `specifyInputSchema` and `schemaType: "manual"` with `inputSchema`: available in v1.2
- `schemaType: "fromJson"` with `jsonSchemaExample`: requires v≥1.3

Set `typeVersion: 1.3` on the node if you want `fromJson`. Older installs should use `manual`.

---

## Picking a pattern

```
Does your tool need more than one input field?
├─ No (just a URL, question, text blob)
│  └─ Unstructured — skip the schema
├─ Yes, and fields are all typed (numbers, bools, enums)
│  └─ Structured with fromJson (easiest)
├─ Yes, and you need constraints or rich descriptions
│  └─ Structured with manual
└─ Yes, and fields are complex / reusable across agents
   └─ Use toolWorkflow (sub-workflow tool) instead of toolCode
```

---

## Gotcha: schema must be valid JSON

`jsonSchemaExample` and `inputSchema` are **strings containing JSON**, not objects. Watch the escaping when you paste them into workflow JSON. If the node won't save or the LLM doesn't see the fields, validate the JSON separately first.

---

## Gotcha: schema changes don't retroactively fix old agent runs

If an agent was already started with an unstructured tool and you flip it to structured, the agent's system prompt may still reflect the old contract until it's reloaded. Force a re-run / re-open the agent node after changing schema settings.


---

# Code Tool Error Patterns

The most common failure modes for `@n8n/n8n-nodes-langchain.toolCode`, with exact error strings, root causes, and fixes.

---

## Error 1: `"Cannot assign to read only property 'name' of object: Error: No execution data available"`

**Full message (wrapped by n8n):**
> There was an error: "Cannot assign to read only property 'name' of object 'Error: No execution data available'"

**Cause**: Calling `$fromAI()` inside the Code Tool sandbox. `$fromAI()` is a helper intended for *other* tool-enabled nodes (HTTP Request Tool, SendGrid Tool, `toolWorkflow`) where AI-supplied values flow through workflow execution data. The Code Tool sandbox has no execution data — it receives input directly via `query`. The helper throws, n8n tries to annotate the error's `name` property, and that assignment fails because the error object is frozen.

**Fix**: remove `$fromAI()`. Read from `query` (or define an input schema, see INPUT_SCHEMA.md).

```javascript
// ❌ Broken
const price = $fromAI('price', 'Car price in SEK', 'number');

// ✅ Unstructured — parse a JSON string
const params = JSON.parse(query);
const price = Number(params.price);

// ✅ Structured — with specifyInputSchema: true
const { price } = query;
```

---

## Error 2: `"Wrong output type returned"`

**Cause**: You returned the workflow item format (`[{json: {...}}]`) from the Code Tool. That format is for regular Code **nodes**; tools follow the LangChain contract and must return a string.

**Fix**: return a string. For structured output, stringify:

```javascript
// ❌ Broken
return [{ json: { monthly_payment: 5405 } }];

// ✅ Fixed
return JSON.stringify({ monthly_payment: 5405 });
```

---

## Error 3: `"The response property should be a string, but it is an <type>"`

Where `<type>` is `object`, `undefined`, `function`, etc.

**Cause**: You returned a bare object, array, or nothing at all.

| Returned value | Error says | Fix |
|---|---|---|
| `{ result: 42 }` | `...is an object` | `JSON.stringify({ result: 42 })` |
| `[1, 2, 3]` | `...is an object` | `JSON.stringify([1, 2, 3])` |
| *(no `return`)* | `...is an undefined` | Add a `return` |
| `undefined` | `...is an undefined` | Return something |

**Numbers are fine** — n8n auto-converts them to strings:
```javascript
return 42;  // ✅ becomes "42"
```

**Booleans are NOT auto-converted** — stringify explicitly:
```javascript
return String(someBoolean);  // ✅
return JSON.stringify(someBoolean);  // ✅
```

---

## Error 4: AI never calls the tool

**Symptom**: the agent answers from its own reasoning and ignores the tool. No tool invocation shows up in the execution trace.

**Common causes and fixes**:

1. **Generic name**. Default names like `Code Tool` or `My Tool` give the LLM no signal.
   - Fix: rename to verb-y, domain-specific snake_case: `calculate_car_loan`, `search_orders`, `lookup_customer`.

2. **Description doesn't state the trigger**. "Calculates things" is too vague.
   - Fix: explicitly list the user intents that should invoke the tool. `"Use this whenever the user asks about monthly cost, loan breakdown, or total interest."`

3. **Tool isn't wired**. The node sits in the canvas but isn't connected to the AI Agent's `ai_tool` input.
   - Fix: connect it. Check the workflow JSON `connections` block has `"<tool_name>": { "ai_tool": [[{ "node": "AI Agent", "type": "ai_tool", "index": 0 }]] }`.

4. **Name violates `[A-Za-z0-9_]+`**. Spaces, hyphens, and emoji in the tool name cause silent skip on v1.1+.
   - Fix: rename to `snake_case_only`.

---

## Error 5: LLM sends malformed `query`

**Symptom**: your `JSON.parse(query)` throws, or fields come through as wrong types.

**Causes**:
- You're in unstructured mode and the description is ambiguous, so the LLM invents a format.
- You asked for a JSON string but the LLM sent a natural-language sentence.
- Numeric fields arrive as strings because the LLM serialized them that way.

**Fixes**, in order of preference:

1. **Switch to structured mode**. Set `specifyInputSchema: true` and define fields. The LLM now gets a typed schema and n8n validates before your code runs.

2. **Give a concrete example in the description**. LLMs imitate examples well:
   ```
   Call with a single JSON string. Example:
   {"price":439900,"down_payment":87980,"interest_rate":6.95}
   ```

3. **Coerce defensively**:
   ```javascript
   const params = JSON.parse(query);
   const price = Number(params.price);
   if (!isFinite(price)) throw new Error('price must be numeric');
   ```

---

## Error 6: `"$helpers is not defined"` / `"$input is not defined"`

**Cause**: you assumed the Code Tool sandbox exposes the same helpers as the Code node. It doesn't.

**Unavailable in Code Tool**:
- `$input`, `$json`, `$binary`
- `$node["OtherNode"]`
- `$helpers.httpRequest()`
- `$jmespath()`
- `this.getContext(...)`, `$getWorkflowStaticData(...)`
- `$fromAI()`

**Fix**:
- Pure computation? Stay in Code Tool, use plain JS.
- Need HTTP? Move to **HTTP Request Tool** (with `$fromAI()` in URL/body).
- Need other-node data or credentials? Move to **Call Sub-workflow Tool (`toolWorkflow`)** — its sub-workflow has a full Code node sandbox.
- Need state across calls? Not possible in Code Tool. Use a sub-workflow that reads/writes a Data Table, Redis, etc.

---

## Error 7: Python-specific — `"name 'query' is not defined"`

**Cause**: in Python, the input variable is `_query` (underscore prefix), not `query`.

```python
# ❌ Broken
result = process(query)

# ✅ Fixed
result = process(_query)
```

---

## Error Prevention Checklist

Before saving a Code Tool:

- [ ] Tool **name** is snake_case, descriptive, and unique
- [ ] **Description** tells the LLM when to call it, with an example if unstructured
- [ ] **No `$fromAI()`** in the code body
- [ ] **No `$input`, `$json`, `$helpers`** — not in this sandbox
- [ ] Input read from `query` (JS) or `_query` (Python)
- [ ] All code paths `return` a string (or a number that auto-converts)
- [ ] If returning structured data, wrapped in `JSON.stringify(...)`
- [ ] Wired to an AI Agent via `ai_tool` connection
- [ ] For multi-field input: either example JSON in description, or `specifyInputSchema: true`

---

## Debugging tips

- **Use the Execution view**, not just the test output. The agent's tool invocation and raw input/output are visible there — you can see exactly what `query` the LLM sent.
- **Log inside the tool** by including fields in the returned JSON:
  ```javascript
  return JSON.stringify({ received_query: query, result: /* ... */ });
  ```
  The LLM sees the echo, and you can spot malformed input.
- **Test the tool without the LLM** by temporarily turning the tool node into a standalone Code node with hard-coded `query`, running it manually, then swapping back.
