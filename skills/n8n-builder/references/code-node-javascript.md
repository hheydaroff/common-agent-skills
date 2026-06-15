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


# JavaScript Code Node

Expert guidance for writing JavaScript code in n8n Code nodes.

---

## Quick Start

```javascript
// Basic template for Code nodes
const items = $input.all();

// Process data
const processed = items.map(item => ({
  json: {
    ...item.json,
    processed: true,
    timestamp: new Date().toISOString()
  }
}));

return processed;
```

### Essential Rules

1. **Choose "Run Once for All Items" mode** (recommended for most use cases)
2. **Access data**: `$input.all()`, `$input.first()`, or `$input.item`
3. **CRITICAL**: Must return `[{json: {...}}]` format
4. **CRITICAL**: Webhook data is under `$json.body` (not `$json` directly)
5. **Built-ins available**: $helpers.httpRequest() (no auth), DateTime (Luxon), $jmespath(). **Not available**: $helpers.httpRequestWithAuthentication, $env (when N8N_BLOCK_ENV_ACCESS_IN_NODE=true), require() (unless allowlisted)
6. **Instance-allowlisted libraries**: Self-hosted instances can allowlist modules via `N8N_RUNNERS_ALLOWED_BUILT_IN_MODULES` and `N8N_RUNNERS_ALLOWED_EXTERNAL_MODULES` (legacy: `NODE_FUNCTION_ALLOW_BUILTIN` / `NODE_FUNCTION_ALLOW_EXTERNAL`). If the user says their instance allows specific modules (e.g. `axios`, `lodash`, `crypto`), use them via `require()` — don't refuse. If unsure, ask or default to built-ins only.
7. **Wrong skill?** If you're writing code for a **Custom Code Tool** attached to an AI Agent (`@n8n/n8n-nodes-langchain.toolCode`), stop — that node has a different contract (input via `query`, must return a string, no `$input`/`$helpers`). Use the **n8n-code-tool** skill.

---

## Mode Selection Guide

The Code node offers two execution modes. Choose based on your use case:

### Run Once for All Items (Recommended - Default)

**Use this mode for:** 95% of use cases

- **How it works**: Code executes **once** regardless of input count
- **Data access**: `$input.all()` or `items` array
- **Best for**: Aggregation, filtering, batch processing, transformations, API calls with all data
- **Performance**: Faster for multiple items (single execution)

```javascript
// Example: Calculate total from all items
const allItems = $input.all();
const total = allItems.reduce((sum, item) => sum + (item.json.amount || 0), 0);

return [{
  json: {
    total,
    count: allItems.length,
    average: total / allItems.length
  }
}];
```

**When to use:**
- ✅ Comparing items across the dataset
- ✅ Calculating totals, averages, or statistics
- ✅ Sorting or ranking items
- ✅ Deduplication
- ✅ Building aggregated reports
- ✅ Combining data from multiple items

### Run Once for Each Item

**Use this mode for:** Specialized cases only

- **How it works**: Code executes **separately** for each input item
- **Data access**: `$input.item` or `$item`
- **Best for**: Item-specific logic, independent operations, per-item validation
- **Performance**: Slower for large datasets (multiple executions)

```javascript
// Example: Add processing timestamp to each item
const item = $input.item;

return [{
  json: {
    ...item.json,
    processed: true,
    processedAt: new Date().toISOString()
  }
}];
```

**When to use:**
- ✅ Each item needs independent API call
- ✅ Per-item validation with different error handling
- ✅ Item-specific transformations based on item properties
- ✅ When items must be processed separately for business logic

**Decision Shortcut:**
- **Need to look at multiple items?** → Use "All Items" mode
- **Each item completely independent?** → Use "Each Item" mode
- **Not sure?** → Use "All Items" mode (you can always loop inside)

---

## Data Access Patterns

### Pattern 1: $input.all() - Most Common

**Use when**: Processing arrays, batch operations, aggregations

```javascript
// Get all items from previous node
const allItems = $input.all();

// Filter, map, reduce as needed
const valid = allItems.filter(item => item.json.status === 'active');
const mapped = valid.map(item => ({
  json: {
    id: item.json.id,
    name: item.json.name
  }
}));

return mapped;
```

### Pattern 2: $input.first() - Very Common

**Use when**: Working with single objects, API responses, first-in-first-out

```javascript
// Get first item only
const firstItem = $input.first();
const data = firstItem.json;

return [{
  json: {
    result: processData(data),
    processedAt: new Date().toISOString()
  }
}];
```

### Pattern 3: $input.item - Each Item Mode Only

**Use when**: In "Run Once for Each Item" mode

```javascript
// Current item in loop (Each Item mode only)
const currentItem = $input.item;

return [{
  json: {
    ...currentItem.json,
    itemProcessed: true
  }
}];
```

### Pattern 4: $node - Reference Other Nodes

**Use when**: Need data from specific nodes in workflow

```javascript
// Get output from specific node
const webhookData = $node["Webhook"].json;
const httpData = $node["HTTP Request"].json;

return [{
  json: {
    combined: {
      webhook: webhookData,
      api: httpData
    }
  }
}];
```

**See**: DATA_ACCESS.md for comprehensive guide

---

## Critical: Webhook Data Structure

**MOST COMMON MISTAKE**: Webhook data is nested under `.body`

```javascript
// ❌ WRONG - Will return undefined
const name = $json.name;
const email = $json.email;

// ✅ CORRECT - Webhook data is under .body
const name = $json.body.name;
const email = $json.body.email;

// Or with $input
const webhookData = $input.first().json.body;
const name = webhookData.name;
```

**Why**: Webhook node wraps all request data under `body` property. This includes POST data, query parameters, and JSON payloads.

**See**: DATA_ACCESS.md for full webhook structure details

---

## Return Format Requirements

**CRITICAL RULE**: Always return array of objects with `json` property

### Correct Return Formats

```javascript
// ✅ Single result
return [{
  json: {
    field1: value1,
    field2: value2
  }
}];

// ✅ Multiple results
return [
  {json: {id: 1, data: 'first'}},
  {json: {id: 2, data: 'second'}}
];

// ✅ Transformed array
const transformed = $input.all()
  .filter(item => item.json.valid)
  .map(item => ({
    json: {
      id: item.json.id,
      processed: true
    }
  }));
return transformed;

// ✅ Empty result (when no data to return)
return [];

// ✅ Conditional return
if (shouldProcess) {
  return [{json: processedData}];
} else {
  return [];
}
```

### Incorrect Return Formats

```javascript
// ❌ WRONG: Object without array wrapper
return {
  json: {field: value}
};

// ❌ WRONG: Array without json wrapper
return [{field: value}];

// ❌ WRONG: Plain string
return "processed";

// ❌ WRONG: Raw data without mapping
return $input.all();  // Missing .map()

// ❌ WRONG: Incomplete structure
return [{data: value}];  // Should be {json: value}
```

**Why it matters**: Next nodes expect array format. Incorrect format causes workflow execution to fail.

**See**: ERROR_PATTERNS.md #3 for detailed error solutions

---

## Common Patterns Overview

Based on production workflows, here are the most useful patterns:

### 1. Multi-Source Data Aggregation
Combine data from multiple APIs, webhooks, or nodes

```javascript
const allItems = $input.all();
const results = [];

for (const item of allItems) {
  const sourceName = item.json.name || 'Unknown';
  // Parse source-specific structure
  if (sourceName === 'API1' && item.json.data) {
    results.push({
      json: {
        title: item.json.data.title,
        source: 'API1'
      }
    });
  }
}

return results;
```

### 2. Filtering with Regex
Extract patterns, mentions, or keywords from text

```javascript
const pattern = /\b([A-Z]{2,5})\b/g;
const matches = {};

for (const item of $input.all()) {
  const text = item.json.text;
  const found = text.match(pattern);

  if (found) {
    found.forEach(match => {
      matches[match] = (matches[match] || 0) + 1;
    });
  }
}

return [{json: {matches}}];
```

### 3. Data Transformation & Enrichment
Map fields, normalize formats, add computed fields

```javascript
const items = $input.all();

return items.map(item => {
  const data = item.json;
  const nameParts = data.name.split(' ');

  return {
    json: {
      first_name: nameParts[0],
      last_name: nameParts.slice(1).join(' '),
      email: data.email,
      created_at: new Date().toISOString()
    }
  };
});
```

### 4. Top N Filtering & Ranking
Sort and limit results

```javascript
const items = $input.all();

const topItems = items
  .sort((a, b) => (b.json.score || 0) - (a.json.score || 0))
  .slice(0, 10);

return topItems.map(item => ({json: item.json}));
```

### 5. Aggregation & Reporting
Sum, count, group data

```javascript
const items = $input.all();
const total = items.reduce((sum, item) => sum + (item.json.amount || 0), 0);

return [{
  json: {
    total,
    count: items.length,
    average: total / items.length,
    timestamp: new Date().toISOString()
  }
}];
```

**See**: COMMON_PATTERNS.md for 10 detailed production patterns

---

## Error Prevention - Top 5 Mistakes

### #1: Empty Code or Missing Return (Most Common)

```javascript
// ❌ WRONG: No return statement
const items = $input.all();
// ... processing code ...
// Forgot to return!

// ✅ CORRECT: Always return data
const items = $input.all();
// ... processing ...
return items.map(item => ({json: item.json}));
```

### #2: Expression Syntax Confusion

```javascript
// ❌ WRONG: Using n8n expression syntax in code
const value = "{{ $json.field }}";

// ✅ CORRECT: Use JavaScript template literals
const value = `${$json.field}`;

// ✅ CORRECT: Direct access
const value = $input.first().json.field;
```

### #3: Incorrect Return Wrapper

```javascript
// ❌ WRONG: Returning object instead of array
return {json: {result: 'success'}};

// ✅ CORRECT: Array wrapper required
return [{json: {result: 'success'}}];
```

### #4: Missing Null Checks

```javascript
// ❌ WRONG: Crashes if field doesn't exist
const value = item.json.user.email;

// ✅ CORRECT: Safe access with optional chaining
const value = item.json?.user?.email || 'no-email@example.com';

// ✅ CORRECT: Guard clause
if (!item.json.user) {
  return [];
}
const value = item.json.user.email;
```

### #5: Webhook Body Nesting

```javascript
// ❌ WRONG: Direct access to webhook data
const email = $json.email;

// ✅ CORRECT: Webhook data under .body
const email = $json.body.email;
```

**See**: ERROR_PATTERNS.md for comprehensive error guide

---

## Built-in Functions & Helpers

### $helpers.httpRequest()

Make HTTP requests from within code:

```javascript
const response = await $helpers.httpRequest({
  method: 'GET',
  url: 'https://api.example.com/data',
  headers: {
    'Authorization': 'Bearer token',
    'Content-Type': 'application/json'
  }
});

return [{json: {data: response}}];
```

### DateTime (Luxon)

Date and time operations:

```javascript
// Current time
const now = DateTime.now();

// Format dates
const formatted = now.toFormat('yyyy-MM-dd');
const iso = now.toISO();

// Date arithmetic
const tomorrow = now.plus({days: 1});
const lastWeek = now.minus({weeks: 1});

return [{
  json: {
    today: formatted,
    tomorrow: tomorrow.toFormat('yyyy-MM-dd')
  }
}];
```

### $jmespath()

Query JSON structures:

```javascript
const data = $input.first().json;

// Filter array
const adults = $jmespath(data, 'users[?age >= `18`]');

// Extract fields
const names = $jmespath(data, 'users[*].name');

return [{json: {adults, names}}];
```

**See**: BUILTIN_FUNCTIONS.md for complete reference

---

## Best Practices

### 1. Always Validate Input Data

```javascript
const items = $input.all();

// Check if data exists
if (!items || items.length === 0) {
  return [];
}

// Validate structure
if (!items[0].json) {
  return [{json: {error: 'Invalid input format'}}];
}

// Continue processing...
```

### 2. Use Try-Catch for Error Handling

```javascript
try {
  const response = await $helpers.httpRequest({
    url: 'https://api.example.com/data'
  });

  return [{json: {success: true, data: response}}];
} catch (error) {
  return [{
    json: {
      success: false,
      error: error.message
    }
  }];
}
```

### 3. Prefer Array Methods Over Loops

```javascript
// ✅ GOOD: Functional approach
const processed = $input.all()
  .filter(item => item.json.valid)
  .map(item => ({json: {id: item.json.id}}));

// ❌ SLOWER: Manual loop
const processed = [];
for (const item of $input.all()) {
  if (item.json.valid) {
    processed.push({json: {id: item.json.id}});
  }
}
```

### 4. Filter Early, Process Late

```javascript
// ✅ GOOD: Filter first to reduce processing
const processed = $input.all()
  .filter(item => item.json.status === 'active')  // Reduce dataset first
  .map(item => expensiveTransformation(item));  // Then transform

// ❌ WASTEFUL: Transform everything, then filter
const processed = $input.all()
  .map(item => expensiveTransformation(item))  // Wastes CPU
  .filter(item => item.json.status === 'active');
```

### 5. Use Descriptive Variable Names

```javascript
// ✅ GOOD: Clear intent
const activeUsers = $input.all().filter(item => item.json.active);
const totalRevenue = activeUsers.reduce((sum, user) => sum + user.json.revenue, 0);

// ❌ BAD: Unclear purpose
const a = $input.all().filter(item => item.json.active);
const t = a.reduce((s, u) => s + u.json.revenue, 0);
```

### 6. Debug with console.log()

```javascript
// Debug statements appear in browser console
const items = $input.all();
console.log(`Processing ${items.length} items`);

for (const item of items) {
  console.log('Item data:', item.json);
  // Process...
}

return result;
```

---

## Production Gotchas

Hard-won lessons from real-world n8n workflow deployments:

### SplitInBatches Loop Semantics

The SplitInBatches node has two outputs — and the naming is counterintuitive:
- `main[0]` = **done** — fires ONCE after all batches are processed
- `main[1]` = **each batch** — fires for every batch (this is the loop body)

Always add a **Limit 1** node after the done output before downstream processing, as a safety against edge cases where done fires with extra items.

### Cross-Iteration Data Accumulation (CRITICAL)

After a SplitInBatches loop, `$('Node Inside Loop').all()` returns **ONLY the last iteration's items**, not cumulative results. This silently drops data from all but the final batch.

**Fix**: Use workflow static data to accumulate across iterations:

```javascript
// BEFORE the loop (reset accumulator):
const staticData = $getWorkflowStaticData('global');
staticData.results = [];
return $input.all();

// INSIDE the loop body (accumulate):
const staticData = $getWorkflowStaticData('global');
const results = [];
for (const item of $input.all()) {
  const processed = { /* ... */ };
  results.push({ json: processed });
  staticData.results.push(processed);
}
return results;

// AFTER the loop (read accumulated data):
const staticData = $getWorkflowStaticData('global');
const allResults = staticData.results || [];
// Now aggregate across ALL iterations
```

### pairedItem for New Output Items

When creating new items that don't map 1:1 to input items, include `pairedItem` — otherwise downstream Set nodes fail with `paired_item_no_info`:

```javascript
const results = [];
for (let i = 0; i < $input.all().length; i++) {
  const item = $input.all()[i];
  results.push({
    json: { /* new data */ },
    pairedItem: { item: i }
  });
}
return results;
```

### Correct Node Reference Syntax

```javascript
// ❌ WRONG - .json directly on node reference
const data = $('HTTP Request').json;

// ✅ CORRECT - call .first() then access .json
const data = $('HTTP Request').first().json;

// ✅ Also correct - get all items
const allData = $('HTTP Request').all();
```

### Float Precision for Price/Currency Comparison

When comparing prices or currency values, floating point noise can cause false positives. Round to cents:

```javascript
// ❌ Unreliable - float comparison
if (newPrice !== oldPrice) { /* triggers on noise */ }

// ✅ Reliable - compare at cent level
if (Math.round(newPrice * 100) !== Math.round(oldPrice * 100)) {
  // Real price change detected
}
```

---

## When to Use Code Node

Use Code node when:
- ✅ Complex transformations requiring multiple steps
- ✅ Custom calculations or business logic
- ✅ Recursive operations
- ✅ API response parsing with complex structure
- ✅ Multi-step conditionals
- ✅ Data aggregation across items

Consider other nodes when:
- ❌ Simple field mapping → Use **Set** node
- ❌ Basic filtering → Use **Filter** node
- ❌ Simple conditionals → Use **IF** or **Switch** node
- ❌ HTTP requests only → Use **HTTP Request** node

**Code node excels at**: Complex logic that would require chaining many simple nodes

---

## Integration with Other Skills

### Works With:

**n8n Expression Syntax**:
- Expressions use `{{ }}` syntax in other nodes
- Code nodes use JavaScript directly (no `{{ }}`)
- When to use expressions vs code

**n8n MCP Tools Expert**:
- How to find Code node: `search_nodes({query: "code"})`
- Get configuration help: `get_node({nodeType: "nodes-base.code"})`
- Validate code: `validate_node({nodeType: "nodes-base.code", config: {...}})`

**n8n Node Configuration**:
- Mode selection (All Items vs Each Item)
- Language selection (JavaScript vs Python)
- Understanding property dependencies

**n8n Workflow Patterns**:
- Code nodes in transformation step
- Webhook → Code → API pattern
- Error handling in workflows

**n8n Validation Expert**:
- Validate Code node configuration
- Handle validation errors
- Auto-fix common issues

---

## Quick Reference Checklist

Before deploying Code nodes, verify:

- [ ] **Code is not empty** - Must have meaningful logic
- [ ] **Return statement exists** - Must return array of objects
- [ ] **Proper return format** - Each item: `{json: {...}}`
- [ ] **Data access correct** - Using `$input.all()`, `$input.first()`, or `$input.item`
- [ ] **No n8n expressions** - Use JavaScript template literals: `` `${value}` ``
- [ ] **Error handling** - Guard clauses for null/undefined inputs
- [ ] **Webhook data** - Access via `.body` if from webhook
- [ ] **Mode selection** - "All Items" for most cases
- [ ] **Performance** - Prefer map/filter over manual loops
- [ ] **Output consistent** - All code paths return same structure

---

## Additional Resources

### Related Files
- DATA_ACCESS.md - Comprehensive data access patterns
- COMMON_PATTERNS.md - 10 production-tested patterns
- ERROR_PATTERNS.md - Top 5 errors and solutions
- BUILTIN_FUNCTIONS.md - Complete built-in reference

### n8n Documentation
- Code Node Guide: https://docs.n8n.io/code/code-node/
- Built-in Methods: https://docs.n8n.io/code-examples/methods-variables-reference/
- Luxon Documentation: https://moment.github.io/luxon/

---

**Ready to write JavaScript in n8n Code nodes!** Start with simple transformations, use the error patterns guide to avoid common mistakes, and reference the pattern library for production-ready examples.


---

# Data Access Patterns - JavaScript Code Node

Comprehensive guide to accessing data in n8n Code nodes using JavaScript.

---

## Overview

In n8n Code nodes, you access data from previous nodes using built-in variables and methods. Understanding which method to use is critical for correct workflow execution.

**Data Access Priority** (by common usage):
1. **`$input.all()`** - Most common - Batch operations, aggregations
2. **`$input.first()`** - Very common - Single item operations
3. **`$input.item`** - Common - Each Item mode only
4. **`$node["NodeName"].json`** - Specific node references
5. **`$json`** - Direct current item (legacy, use `$input` instead)

---

## Pattern 1: $input.all() - Process All Items

**Usage**: Most common pattern for batch processing

**When to use:**
- Processing multiple records
- Aggregating data (sum, count, average)
- Filtering arrays
- Transforming datasets
- Comparing items
- Sorting or ranking

### Basic Usage

```javascript
// Get all items from previous node
const allItems = $input.all();

// allItems is an array of objects like:
// [
//   {json: {id: 1, name: "Alice"}},
//   {json: {id: 2, name: "Bob"}}
// ]

console.log(`Received ${allItems.length} items`);

return allItems;
```

### Example 1: Filter Active Items

```javascript
const allItems = $input.all();

// Filter only active items
const activeItems = allItems.filter(item => item.json.status === 'active');

return activeItems;
```

### Example 2: Transform All Items

```javascript
const allItems = $input.all();

// Map to new structure
const transformed = allItems.map(item => ({
  json: {
    id: item.json.id,
    fullName: `${item.json.firstName} ${item.json.lastName}`,
    email: item.json.email,
    processedAt: new Date().toISOString()
  }
}));

return transformed;
```

### Example 3: Aggregate Data

```javascript
const allItems = $input.all();

// Calculate total
const total = allItems.reduce((sum, item) => {
  return sum + (item.json.amount || 0);
}, 0);

return [{
  json: {
    total,
    count: allItems.length,
    average: total / allItems.length
  }
}];
```

### Example 4: Sort and Limit

```javascript
const allItems = $input.all();

// Get top 5 by score
const topFive = allItems
  .sort((a, b) => (b.json.score || 0) - (a.json.score || 0))
  .slice(0, 5);

return topFive.map(item => ({json: item.json}));
```

### Example 5: Group By Category

```javascript
const allItems = $input.all();

// Group items by category
const grouped = {};

for (const item of allItems) {
  const category = item.json.category || 'Uncategorized';

  if (!grouped[category]) {
    grouped[category] = [];
  }

  grouped[category].push(item.json);
}

// Convert to array format
return Object.entries(grouped).map(([category, items]) => ({
  json: {
    category,
    items,
    count: items.length
  }
}));
```

### Example 6: Deduplicate by ID

```javascript
const allItems = $input.all();

// Remove duplicates by ID
const seen = new Set();
const unique = [];

for (const item of allItems) {
  const id = item.json.id;

  if (!seen.has(id)) {
    seen.add(id);
    unique.push(item);
  }
}

return unique;
```

---

## Pattern 2: $input.first() - Get First Item

**Usage**: Very common for single-item operations

**When to use:**
- Previous node returns single object
- Working with API responses
- Getting initial/first data point
- Configuration or metadata access

### Basic Usage

```javascript
// Get first item from previous node
const firstItem = $input.first();

// Access the JSON data
const data = firstItem.json;

console.log('First item:', data);

return [{json: data}];
```

### Example 1: Process Single API Response

```javascript
// Get API response (typically single object)
const response = $input.first().json;

// Extract what you need
return [{
  json: {
    userId: response.data.user.id,
    userName: response.data.user.name,
    status: response.status,
    fetchedAt: new Date().toISOString()
  }
}];
```

### Example 2: Transform Single Object

```javascript
const data = $input.first().json;

// Transform structure
return [{
  json: {
    id: data.id,
    contact: {
      email: data.email,
      phone: data.phone
    },
    address: {
      street: data.street,
      city: data.city,
      zip: data.zip
    }
  }
}];
```

### Example 3: Validate Single Item

```javascript
const item = $input.first().json;

// Validation logic
const isValid = item.email && item.email.includes('@');

return [{
  json: {
    ...item,
    valid: isValid,
    validatedAt: new Date().toISOString()
  }
}];
```

### Example 4: Extract Nested Data

```javascript
const response = $input.first().json;

// Navigate nested structure
const users = response.data?.users || [];

return users.map(user => ({
  json: {
    id: user.id,
    name: user.profile?.name || 'Unknown',
    email: user.contact?.email || 'no-email'
  }
}));
```

### Example 5: Combine with Other Methods

```javascript
// Get first item's data
const firstData = $input.first().json;

// Use it to filter all items
const allItems = $input.all();
const matching = allItems.filter(item =>
  item.json.category === firstData.targetCategory
);

return matching;
```

---

## Pattern 3: $input.item - Current Item (Each Item Mode)

**Usage**: Common in "Run Once for Each Item" mode

**When to use:**
- Mode is set to "Run Once for Each Item"
- Need to process items independently
- Per-item API calls or validations
- Item-specific error handling

**IMPORTANT**: Only use in "Each Item" mode. Will be undefined in "All Items" mode.

### Basic Usage

```javascript
// In "Run Once for Each Item" mode
const currentItem = $input.item;
const data = currentItem.json;

console.log('Processing item:', data.id);

return [{
  json: {
    ...data,
    processed: true
  }
}];
```

### Example 1: Add Processing Metadata

```javascript
const item = $input.item;

return [{
  json: {
    ...item.json,
    processed: true,
    processedAt: new Date().toISOString(),
    processingDuration: Math.random() * 1000  // Simulated duration
  }
}];
```

### Example 2: Per-Item Validation

```javascript
const item = $input.item;
const data = item.json;

// Validate this specific item
const errors = [];

if (!data.email) errors.push('Email required');
if (!data.name) errors.push('Name required');
if (data.age && data.age < 18) errors.push('Must be 18+');

return [{
  json: {
    ...data,
    valid: errors.length === 0,
    errors: errors.length > 0 ? errors : undefined
  }
}];
```

### Example 3: Item-Specific API Call

```javascript
const item = $input.item;
const userId = item.json.userId;

// Make API call specific to this item
const response = await $helpers.httpRequest({
  method: 'GET',
  url: `https://api.example.com/users/${userId}/details`
});

return [{
  json: {
    ...item.json,
    details: response
  }
}];
```

> ⚠️ **For authenticated APIs, don't extend this pattern.** `$helpers.httpRequestWithAuthentication` is blocked in the Code node sandbox (since n8n v2.0). Use an HTTP Request node with the credential attached, or delegate to a sub-workflow whose HTTP Request node holds the credential. See ERROR_PATTERNS.md Error #6.

### Example 4: Conditional Processing

```javascript
const item = $input.item;
const data = item.json;

// Process based on item type
if (data.type === 'premium') {
  return [{
    json: {
      ...data,
      discount: 0.20,
      tier: 'premium'
    }
  }];
} else {
  return [{
    json: {
      ...data,
      discount: 0.05,
      tier: 'standard'
    }
  }];
}
```

---

## Pattern 4: $node - Reference Other Nodes

**Usage**: Less common, but powerful for specific scenarios

**When to use:**
- Need data from specific named node
- Combining data from multiple nodes
- Accessing metadata about workflow execution

### Basic Usage

```javascript
// Get output from specific node
const webhookData = $node["Webhook"].json;
const apiData = $node["HTTP Request"].json;

return [{
  json: {
    fromWebhook: webhookData,
    fromAPI: apiData
  }
}];
```

### Example 1: Combine Multiple Sources

```javascript
// Reference multiple nodes
const webhook = $node["Webhook"].json;
const database = $node["Postgres"].json;
const api = $node["HTTP Request"].json;

return [{
  json: {
    combined: {
      webhook: webhook.body,
      dbRecords: database.length,
      apiResponse: api.status
    },
    processedAt: new Date().toISOString()
  }
}];
```

### Example 2: Compare Across Nodes

```javascript
const oldData = $node["Get Old Data"].json;
const newData = $node["Get New Data"].json;

// Compare
const changes = {
  added: newData.filter(n => !oldData.find(o => o.id === n.id)),
  removed: oldData.filter(o => !newData.find(n => n.id === o.id)),
  modified: newData.filter(n => {
    const old = oldData.find(o => o.id === n.id);
    return old && JSON.stringify(old) !== JSON.stringify(n);
  })
};

return [{
  json: {
    changes,
    summary: {
      added: changes.added.length,
      removed: changes.removed.length,
      modified: changes.modified.length
    }
  }
}];
```

### Example 3: Access Node Metadata

```javascript
// Get data from specific execution path
const ifTrueBranch = $node["IF True"].json;
const ifFalseBranch = $node["IF False"].json;

// Use whichever branch executed
const result = ifTrueBranch || ifFalseBranch || {};

return [{json: result}];
```

---

## Critical: Webhook Data Structure

**MOST COMMON MISTAKE**: Forgetting webhook data is nested under `.body`

### The Problem

Webhook node wraps all incoming data under a `body` property. This catches many developers by surprise.

### Structure

```javascript
// Webhook node output structure:
{
  "headers": {
    "content-type": "application/json",
    "user-agent": "...",
    // ... other headers
  },
  "params": {},
  "query": {},
  "body": {
    // ← YOUR DATA IS HERE
    "name": "Alice",
    "email": "alice@example.com",
    "message": "Hello!"
  }
}
```

### Wrong vs Right

```javascript
// ❌ WRONG: Trying to access directly
const name = $json.name;  // undefined
const email = $json.email;  // undefined

// ✅ CORRECT: Access via .body
const name = $json.body.name;  // "Alice"
const email = $json.body.email;  // "alice@example.com"

// ✅ CORRECT: Extract body first
const webhookData = $json.body;
const name = webhookData.name;  // "Alice"
const email = webhookData.email;  // "alice@example.com"
```

### Example: Full Webhook Processing

```javascript
// Get webhook data from previous node
const webhookOutput = $input.first().json;

// Access the actual payload
const payload = webhookOutput.body;

// Access headers if needed
const contentType = webhookOutput.headers['content-type'];

// Access query parameters if needed
const apiKey = webhookOutput.query.api_key;

// Process the actual data
return [{
  json: {
    // Data from webhook body
    userName: payload.name,
    userEmail: payload.email,
    message: payload.message,

    // Metadata
    receivedAt: new Date().toISOString(),
    contentType: contentType,
    authenticated: !!apiKey
  }
}];
```

### POST Data, Query Params, and Headers

```javascript
const webhook = $input.first().json;

return [{
  json: {
    // POST body data
    formData: webhook.body,

    // Query parameters (?key=value)
    queryParams: webhook.query,

    // HTTP headers
    userAgent: webhook.headers['user-agent'],
    contentType: webhook.headers['content-type'],

    // Request metadata
    method: webhook.method,  // POST, GET, etc.
    url: webhook.url
  }
}];
```

### Common Webhook Scenarios

```javascript
// Scenario 1: Form submission
const formData = $json.body;
const name = formData.name;
const email = formData.email;

// Scenario 2: JSON API webhook
const apiPayload = $json.body;
const eventType = apiPayload.event;
const data = apiPayload.data;

// Scenario 3: Query parameters
const apiKey = $json.query.api_key;
const userId = $json.query.user_id;

// Scenario 4: Headers
const authorization = $json.headers['authorization'];
const signature = $json.headers['x-signature'];
```

---

## Choosing the Right Pattern

### Decision Tree

```
Do you need ALL items from previous node?
├─ YES → Use $input.all()
│
└─ NO → Do you need just the FIRST item?
    ├─ YES → Use $input.first()
    │
    └─ NO → Are you in "Each Item" mode?
        ├─ YES → Use $input.item
        │
        └─ NO → Do you need specific node data?
            ├─ YES → Use $node["NodeName"]
            └─ NO → Use $input.first() (default)
```

### Quick Reference Table

| Scenario | Use This | Example |
|----------|----------|---------|
| Sum all amounts | `$input.all()` | `allItems.reduce((sum, i) => sum + i.json.amount, 0)` |
| Get API response | `$input.first()` | `$input.first().json.data` |
| Process each independently | `$input.item` | `$input.item.json` (Each Item mode) |
| Combine two nodes | `$node["Name"]` | `$node["API"].json` |
| Filter array | `$input.all()` | `allItems.filter(i => i.json.active)` |
| Transform single object | `$input.first()` | `{...input.first().json, new: true}` |
| Webhook data | `$input.first()` | `$input.first().json.body` |

---

## Common Mistakes

### Mistake 1: Using $json Without Context

```javascript
// ❌ WRONG: $json is ambiguous
const value = $json.field;

// ✅ CORRECT: Be explicit
const value = $input.first().json.field;
```

### Mistake 2: Forgetting .json Property

```javascript
// ❌ WRONG: Trying to access fields on item object
const items = $input.all();
const names = items.map(item => item.name);  // undefined

// ✅ CORRECT: Access via .json
const names = items.map(item => item.json.name);
```

### Mistake 3: Using $input.item in All Items Mode

```javascript
// ❌ WRONG: $input.item is undefined in "All Items" mode
const data = $input.item.json;  // Error!

// ✅ CORRECT: Use appropriate method
const data = $input.first().json;  // Or $input.all()
```

### Mistake 4: Not Handling Empty Arrays

```javascript
// ❌ WRONG: Crashes if no items
const first = $input.all()[0].json;

// ✅ CORRECT: Check length first
const items = $input.all();
if (items.length === 0) {
  return [];
}
const first = items[0].json;

// ✅ ALSO CORRECT: Use $input.first()
const first = $input.first().json;  // Built-in safety
```

### Mistake 5: Modifying Original Data

```javascript
// ❌ RISKY: Mutating original
const items = $input.all();
items[0].json.modified = true;  // Modifies original
return items;

// ✅ SAFE: Create new objects
const items = $input.all();
return items.map(item => ({
  json: {
    ...item.json,
    modified: true
  }
}));
```

---

## Advanced Patterns

### Pattern: Pagination Handling

```javascript
const currentPage = $input.all();
const pageNumber = $node["Set Page"].json.page || 1;

// Combine with previous pages
const allPreviousPages = $node["Accumulator"]?.json.accumulated || [];

return [{
  json: {
    accumulated: [...allPreviousPages, ...currentPage],
    currentPage: pageNumber,
    totalItems: allPreviousPages.length + currentPage.length
  }
}];
```

### Pattern: Conditional Node Reference

```javascript
// Access different nodes based on condition
const condition = $input.first().json.type;

let data;
if (condition === 'api') {
  data = $node["API Response"].json;
} else if (condition === 'database') {
  data = $node["Database"].json;
} else {
  data = $node["Default"].json;
}

return [{json: data}];
```

### Pattern: Multi-Node Aggregation

```javascript
// Collect data from multiple named nodes
const sources = ['Source1', 'Source2', 'Source3'];
const allData = [];

for (const source of sources) {
  const nodeData = $node[source]?.json;
  if (nodeData) {
    allData.push({
      source,
      data: nodeData
    });
  }
}

return allData.map(item => ({json: item}));
```

---

## Summary

**Most Common Patterns**:
1. `$input.all()` - Process multiple items, batch operations
2. `$input.first()` - Single item, API responses
3. `$input.item` - Each Item mode processing

**Critical Rule**:
- Webhook data is under `.body` property

**Best Practice**:
- Be explicit: Use `$input.first().json.field` instead of `$json.field`
- Always check for null/undefined
- Use appropriate method for your mode (All Items vs Each Item)

**See Also**:
- SKILL.md - Overview and quick start
- COMMON_PATTERNS.md - Production patterns
- ERROR_PATTERNS.md - Avoid common mistakes


---

# Built-in Functions - JavaScript Code Node

Complete reference for n8n's built-in JavaScript functions and helpers.

---

## Overview

n8n Code nodes provide powerful built-in functions beyond standard JavaScript. This guide covers:

1. **Sandbox restrictions** - What's blocked and why (READ FIRST)
2. **$helpers.httpRequest()** - Make HTTP requests
3. **DateTime (Luxon)** - Advanced date/time operations
4. **$jmespath()** - Query JSON structures
5. **$getWorkflowStaticData()** - Persistent storage
6. **Standard JavaScript Globals** - Math, JSON, console, etc.
7. **Available Node.js Modules** - crypto, Buffer, URL

---

## 0. Sandbox Restrictions (Critical)

Since n8n v2.0, Code nodes execute inside a **task runner sandbox** (`JsTaskRunnerSandbox`) which deliberately blocks several APIs. The legacy vm2 sandbox is being removed. Knowing what's blocked saves hours of "why does this throw on activation but not in the editor preview."

### Blocked helpers

```javascript
// ❌ BLOCKED — throws UnsupportedFunctionError
await $helpers.httpRequestWithAuthentication.call(this, 'credType', { ... });
await $helpers.requestWithAuthenticationPaginated.call(this, { ... }, 'credType');
```

n8n's source comment explains why: *"these rely on checking the credentials from the current node type (Code Node), and Code Node doesn't have credentials."* There is **no env var to re-enable them** in the task runner — the deny-list is compiled-in (`packages/@n8n/task-runner/src/runner-types.ts`).

**Workaround**: don't try to authenticate from inside a Code node. Instead, either:
- Replace the Code node with an HTTP Request node that has the credential attached (the canonical pattern), or
- Have the Code node prepare a payload and delegate to a sub-workflow whose HTTP Request node holds the credential.

### `$env` may be blocked

`$env` is gated by **`N8N_BLOCK_ENV_ACCESS_IN_NODE`**. When set to `true` (a common production hardening), any reference to `$env.SOMETHING` throws. Since you can't tell from inside the Code node whether it's enabled, **don't rely on `$env` for portable skills** — treat secrets as a credential concern (HTTP Request node) rather than a Code-node concern.

### `require()` is gated by allowlists

```javascript
// May throw "Cannot find module 'crypto'" — depends on env vars
const crypto = require('crypto');
```

Built-in modules need `N8N_RUNNERS_ALLOWED_BUILT_IN_MODULES` (or legacy `NODE_FUNCTION_ALLOW_BUILTIN`) set to `*` or a comma-list including `crypto`. External npm packages need `N8N_RUNNERS_ALLOWED_EXTERNAL_MODULES` plus the package being installed in the runner image. On default installs neither is set — `require()` throws.

`Buffer` and `URL` are globals (not `require`'d), so they always work.

### What's always safe

`$input.*`, `$json`, `$node[…]`, `$helpers.httpRequest()` (without auth), `$jmespath()`, `$getWorkflowStaticData()`, `DateTime` (Luxon), and all standard JavaScript globals (`Math`, `JSON`, `Object`, `Array`, `console`, `Buffer`, `URL`, `URLSearchParams`).

---

## 1. $helpers.httpRequest() - HTTP Requests

Make HTTP requests directly from Code nodes without using HTTP Request node.

### Basic Usage

```javascript
const response = await $helpers.httpRequest({
  method: 'GET',
  url: 'https://api.example.com/users'
});

return [{json: {data: response}}];
```

### Complete Options

```javascript
const response = await $helpers.httpRequest({
  method: 'POST',  // GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS
  url: 'https://api.example.com/users',
  headers: {
    'Authorization': 'Bearer token123',
    'Content-Type': 'application/json',
    'User-Agent': 'n8n-workflow'
  },
  body: {
    name: 'John Doe',
    email: 'john@example.com'
  },
  qs: {  // Query string parameters
    page: 1,
    limit: 10
  },
  timeout: 10000,  // Milliseconds (default: no timeout)
  json: true,  // Auto-parse JSON response (default: true)
  simple: false,  // Don't throw on HTTP errors (default: true)
  resolveWithFullResponse: false  // Return only body (default: false)
});
```

### GET Request

```javascript
// Simple GET
const users = await $helpers.httpRequest({
  method: 'GET',
  url: 'https://api.example.com/users'
});

return [{json: {users}}];
```

```javascript
// GET with query parameters
const results = await $helpers.httpRequest({
  method: 'GET',
  url: 'https://api.example.com/search',
  qs: {
    q: 'javascript',
    page: 1,
    per_page: 50
  }
});

return [{json: results}];
```

### POST Request

```javascript
// POST with JSON body
// NOTE: For authenticated APIs, prefer an HTTP Request node with a credential
// attached. Embedding the token in a Code node only works when (a) the token
// arrives as runtime data (e.g. from a previous node), or (b) you're sure
// $env access is enabled on this instance. See section 0.
const apiToken = $input.first().json.apiToken;  // passed in from a credential-aware upstream node

const newUser = await $helpers.httpRequest({
  method: 'POST',
  url: 'https://api.example.com/users',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${apiToken}`
  },
  body: {
    name: $json.body.name,
    email: $json.body.email,
    role: 'user'
  }
});

return [{json: newUser}];
```

### PUT/PATCH Request

```javascript
// Update resource
const updated = await $helpers.httpRequest({
  method: 'PATCH',
  url: `https://api.example.com/users/${userId}`,
  body: {
    name: 'Updated Name',
    status: 'active'
  }
});

return [{json: updated}];
```

### DELETE Request

```javascript
// Delete resource
await $helpers.httpRequest({
  method: 'DELETE',
  url: `https://api.example.com/users/${userId}`,
  headers: {
    'Authorization': `Bearer ${apiToken}`  // token passed in from upstream node, not $env
  }
});

return [{json: {deleted: true, userId}}];
```

### Authentication Patterns

> **Strong preference**: don't authenticate from inside a Code node. Use an HTTP Request node with a credential attached, or delegate to a sub-workflow whose HTTP Request node holds the credential. The patterns below only apply when the token genuinely flows through the workflow as data.

```javascript
// Bearer Token (token came from a previous node, not $env)
const response = await $helpers.httpRequest({
  url: 'https://api.example.com/data',
  headers: {
    'Authorization': `Bearer ${$input.first().json.token}`
  }
});
```

```javascript
// API Key in Header (key came from a previous node, not $env)
const response = await $helpers.httpRequest({
  url: 'https://api.example.com/data',
  headers: {
    'X-API-Key': $input.first().json.apiKey
  }
});
```

```javascript
// Basic Auth (manual)
const credentials = Buffer.from(`${username}:${password}`).toString('base64');

const response = await $helpers.httpRequest({
  url: 'https://api.example.com/data',
  headers: {
    'Authorization': `Basic ${credentials}`
  }
});
```

### Error Handling

```javascript
// Handle HTTP errors gracefully
try {
  const response = await $helpers.httpRequest({
    method: 'GET',
    url: 'https://api.example.com/users',
    simple: false  // Don't throw on 4xx/5xx
  });

  if (response.statusCode >= 200 && response.statusCode < 300) {
    return [{json: {success: true, data: response.body}}];
  } else {
    return [{
      json: {
        success: false,
        status: response.statusCode,
        error: response.body
      }
    }];
  }
} catch (error) {
  return [{
    json: {
      success: false,
      error: error.message
    }
  }];
}
```

### Full Response Access

```javascript
// Get full response including headers and status
const response = await $helpers.httpRequest({
  url: 'https://api.example.com/data',
  resolveWithFullResponse: true
});

return [{
  json: {
    statusCode: response.statusCode,
    headers: response.headers,
    body: response.body,
    rateLimit: response.headers['x-ratelimit-remaining']
  }
}];
```

---

## 2. DateTime (Luxon) - Date & Time Operations

n8n includes Luxon for powerful date/time handling. Access via `DateTime` global.

### Current Date/Time

```javascript
// Current time
const now = DateTime.now();

// Current time in specific timezone
const nowTokyo = DateTime.now().setZone('Asia/Tokyo');

// Today at midnight
const today = DateTime.now().startOf('day');

return [{
  json: {
    iso: now.toISO(),  // "2025-01-20T15:30:00.000Z"
    formatted: now.toFormat('yyyy-MM-dd HH:mm:ss'),  // "2025-01-20 15:30:00"
    unix: now.toSeconds(),  // Unix timestamp
    millis: now.toMillis()  // Milliseconds since epoch
  }
}];
```

### Formatting Dates

```javascript
const now = DateTime.now();

return [{
  json: {
    isoFormat: now.toISO(),  // ISO 8601: "2025-01-20T15:30:00.000Z"
    sqlFormat: now.toSQL(),  // SQL: "2025-01-20 15:30:00.000"
    httpFormat: now.toHTTP(),  // HTTP: "Mon, 20 Jan 2025 15:30:00 GMT"

    // Custom formats
    dateOnly: now.toFormat('yyyy-MM-dd'),  // "2025-01-20"
    timeOnly: now.toFormat('HH:mm:ss'),  // "15:30:00"
    readable: now.toFormat('MMMM dd, yyyy'),  // "January 20, 2025"
    compact: now.toFormat('yyyyMMdd'),  // "20250120"
    withDay: now.toFormat('EEEE, MMMM dd, yyyy'),  // "Monday, January 20, 2025"
    custom: now.toFormat('dd/MM/yy HH:mm')  // "20/01/25 15:30"
  }
}];
```

### Parsing Dates

```javascript
// From ISO string
const dt1 = DateTime.fromISO('2025-01-20T15:30:00');

// From specific format
const dt2 = DateTime.fromFormat('01/20/2025', 'MM/dd/yyyy');

// From SQL
const dt3 = DateTime.fromSQL('2025-01-20 15:30:00');

// From Unix timestamp
const dt4 = DateTime.fromSeconds(1737384600);

// From milliseconds
const dt5 = DateTime.fromMillis(1737384600000);

return [{json: {parsed: dt1.toISO()}}];
```

### Date Arithmetic

```javascript
const now = DateTime.now();

return [{
  json: {
    // Adding time
    tomorrow: now.plus({days: 1}).toISO(),
    nextWeek: now.plus({weeks: 1}).toISO(),
    nextMonth: now.plus({months: 1}).toISO(),
    inTwoHours: now.plus({hours: 2}).toISO(),

    // Subtracting time
    yesterday: now.minus({days: 1}).toISO(),
    lastWeek: now.minus({weeks: 1}).toISO(),
    lastMonth: now.minus({months: 1}).toISO(),
    twoHoursAgo: now.minus({hours: 2}).toISO(),

    // Complex operations
    in90Days: now.plus({days: 90}).toFormat('yyyy-MM-dd'),
    in6Months: now.plus({months: 6}).toFormat('yyyy-MM-dd')
  }
}];
```

### Time Comparisons

```javascript
const now = DateTime.now();
const targetDate = DateTime.fromISO('2025-12-31');

return [{
  json: {
    // Comparisons
    isFuture: targetDate > now,
    isPast: targetDate < now,
    isEqual: targetDate.equals(now),

    // Differences
    daysUntil: targetDate.diff(now, 'days').days,
    hoursUntil: targetDate.diff(now, 'hours').hours,
    monthsUntil: targetDate.diff(now, 'months').months,

    // Detailed difference
    detailedDiff: targetDate.diff(now, ['months', 'days', 'hours']).toObject()
  }
}];
```

### Timezone Operations

```javascript
const now = DateTime.now();

return [{
  json: {
    // Current timezone
    local: now.toISO(),

    // Convert to different timezone
    tokyo: now.setZone('Asia/Tokyo').toISO(),
    newYork: now.setZone('America/New_York').toISO(),
    london: now.setZone('Europe/London').toISO(),
    utc: now.toUTC().toISO(),

    // Get timezone info
    timezone: now.zoneName,  // "America/Los_Angeles"
    offset: now.offset,  // Offset in minutes
    offsetFormatted: now.toFormat('ZZ')  // "+08:00"
  }
}];
```

### Start/End of Period

```javascript
const now = DateTime.now();

return [{
  json: {
    startOfDay: now.startOf('day').toISO(),
    endOfDay: now.endOf('day').toISO(),
    startOfWeek: now.startOf('week').toISO(),
    endOfWeek: now.endOf('week').toISO(),
    startOfMonth: now.startOf('month').toISO(),
    endOfMonth: now.endOf('month').toISO(),
    startOfYear: now.startOf('year').toISO(),
    endOfYear: now.endOf('year').toISO()
  }
}];
```

### Weekday & Month Info

```javascript
const now = DateTime.now();

return [{
  json: {
    // Day info
    weekday: now.weekday,  // 1 = Monday, 7 = Sunday
    weekdayShort: now.weekdayShort,  // "Mon"
    weekdayLong: now.weekdayLong,  // "Monday"
    isWeekend: now.weekday > 5,  // Saturday or Sunday

    // Month info
    month: now.month,  // 1-12
    monthShort: now.monthShort,  // "Jan"
    monthLong: now.monthLong,  // "January"

    // Year info
    year: now.year,  // 2025
    quarter: now.quarter,  // 1-4
    daysInMonth: now.daysInMonth  // 28-31
  }
}];
```

---

## 3. $jmespath() - JSON Querying

Query and transform JSON structures using JMESPath syntax.

### Basic Queries

```javascript
const data = $input.first().json;

// Extract specific field
const names = $jmespath(data, 'users[*].name');

// Filter array
const adults = $jmespath(data, 'users[?age >= `18`]');

// Get specific index
const firstUser = $jmespath(data, 'users[0]');

return [{json: {names, adults, firstUser}}];
```

### Advanced Queries

```javascript
const data = $input.first().json;

// Sort and slice
const top5 = $jmespath(data, 'users | sort_by(@, &score) | reverse(@) | [0:5]');

// Extract nested fields
const emails = $jmespath(data, 'users[*].contact.email');

// Multi-field extraction
const simplified = $jmespath(data, 'users[*].{name: name, email: contact.email}');

// Conditional filtering
const premium = $jmespath(data, 'users[?subscription.tier == `premium`]');

return [{json: {top5, emails, simplified, premium}}];
```

### Common Patterns

```javascript
// Pattern 1: Filter and project
const query1 = $jmespath(data, 'products[?price > `100`].{name: name, price: price}');

// Pattern 2: Aggregate functions
const query2 = $jmespath(data, 'sum(products[*].price)');
const query3 = $jmespath(data, 'max(products[*].price)');
const query4 = $jmespath(data, 'length(products)');

// Pattern 3: Nested filtering
const query5 = $jmespath(data, 'categories[*].products[?inStock == `true`]');

return [{json: {query1, query2, query3, query4, query5}}];
```

---

## 4. $getWorkflowStaticData() - Persistent Storage

Store data that persists across workflow executions.

### Basic Usage

```javascript
// Get static data storage
const staticData = $getWorkflowStaticData();

// Initialize counter if doesn't exist
if (!staticData.counter) {
  staticData.counter = 0;
}

// Increment counter
staticData.counter++;

return [{
  json: {
    executionCount: staticData.counter
  }
}];
```

### Use Cases

```javascript
// Use Case 1: Rate limiting
const staticData = $getWorkflowStaticData();
const now = Date.now();

if (!staticData.lastRun) {
  staticData.lastRun = now;
  staticData.runCount = 1;
} else {
  const timeSinceLastRun = now - staticData.lastRun;

  if (timeSinceLastRun < 60000) {  // Less than 1 minute
    return [{json: {error: 'Rate limit: wait 1 minute between runs'}}];
  }

  staticData.lastRun = now;
  staticData.runCount++;
}

return [{json: {allowed: true, totalRuns: staticData.runCount}}];
```

```javascript
// Use Case 2: Tracking last processed ID
const staticData = $getWorkflowStaticData();
const currentItems = $input.all();

// Get last processed ID
const lastId = staticData.lastProcessedId || 0;

// Filter only new items
const newItems = currentItems.filter(item => item.json.id > lastId);

// Update last processed ID
if (newItems.length > 0) {
  staticData.lastProcessedId = Math.max(...newItems.map(item => item.json.id));
}

return newItems;
```

```javascript
// Use Case 3: Accumulating results
const staticData = $getWorkflowStaticData();

if (!staticData.accumulated) {
  staticData.accumulated = [];
}

// Add current items to accumulated list
const currentData = $input.all().map(item => item.json);
staticData.accumulated.push(...currentData);

return [{
  json: {
    currentBatch: currentData.length,
    totalAccumulated: staticData.accumulated.length,
    allData: staticData.accumulated
  }
}];
```

---

## 5. Standard JavaScript Globals

### Math Object

```javascript
return [{
  json: {
    // Rounding
    rounded: Math.round(3.7),  // 4
    floor: Math.floor(3.7),  // 3
    ceil: Math.ceil(3.2),  // 4

    // Min/Max
    max: Math.max(1, 5, 3, 9, 2),  // 9
    min: Math.min(1, 5, 3, 9, 2),  // 1

    // Random
    random: Math.random(),  // 0-1
    randomInt: Math.floor(Math.random() * 100),  // 0-99

    // Other
    abs: Math.abs(-5),  // 5
    sqrt: Math.sqrt(16),  // 4
    pow: Math.pow(2, 3)  // 8
  }
}];
```

### JSON Object

```javascript
// Parse JSON string
const jsonString = '{"name": "John", "age": 30}';
const parsed = JSON.parse(jsonString);

// Stringify object
const obj = {name: "John", age: 30};
const stringified = JSON.stringify(obj);

// Pretty print
const pretty = JSON.stringify(obj, null, 2);

return [{json: {parsed, stringified, pretty}}];
```

### console Object

```javascript
// Debug logging (appears in browser console, press F12)
console.log('Processing items:', $input.all().length);
console.log('First item:', $input.first().json);

// Other console methods
console.error('Error message');
console.warn('Warning message');
console.info('Info message');

// Continues to return data
return [{json: {processed: true}}];
```

### Object Methods

```javascript
const obj = {name: "John", age: 30, city: "NYC"};

return [{
  json: {
    keys: Object.keys(obj),  // ["name", "age", "city"]
    values: Object.values(obj),  // ["John", 30, "NYC"]
    entries: Object.entries(obj),  // [["name", "John"], ...]

    // Check property
    hasName: 'name' in obj,  // true

    // Merge objects
    merged: Object.assign({}, obj, {country: "USA"})
  }
}];
```

### Array Methods

```javascript
const arr = [1, 2, 3, 4, 5];

return [{
  json: {
    mapped: arr.map(x => x * 2),  // [2, 4, 6, 8, 10]
    filtered: arr.filter(x => x > 2),  // [3, 4, 5]
    reduced: arr.reduce((sum, x) => sum + x, 0),  // 15
    some: arr.some(x => x > 3),  // true
    every: arr.every(x => x > 0),  // true
    find: arr.find(x => x > 3),  // 4
    includes: arr.includes(3),  // true
    joined: arr.join(', ')  // "1, 2, 3, 4, 5"
  }
}];
```

---

## 6. Available Node.js Modules

### crypto Module

> **Gated**: `require('crypto')` only works if `N8N_RUNNERS_ALLOWED_BUILT_IN_MODULES` (or legacy `NODE_FUNCTION_ALLOW_BUILTIN`) includes `crypto` (or is `*`). On default installs it throws "Cannot find module 'crypto'". For hashing you control, prefer doing it before reaching the Code node, or — if you must — verify your instance's config first.

```javascript
const crypto = require('crypto');

// Hash functions
const hash = crypto.createHash('sha256')
  .update('my secret text')
  .digest('hex');

// MD5 hash
const md5 = crypto.createHash('md5')
  .update('my text')
  .digest('hex');

// Random values
const randomBytes = crypto.randomBytes(16).toString('hex');

return [{json: {hash, md5, randomBytes}}];
```

### Buffer (built-in)

```javascript
// Base64 encoding
const encoded = Buffer.from('Hello World').toString('base64');

// Base64 decoding
const decoded = Buffer.from(encoded, 'base64').toString();

// Hex encoding
const hex = Buffer.from('Hello').toString('hex');

return [{json: {encoded, decoded, hex}}];
```

### URL / URLSearchParams

```javascript
// Parse URL
const url = new URL('https://example.com/path?param1=value1&param2=value2');

// Build query string
const params = new URLSearchParams({
  search: 'query',
  page: 1,
  limit: 10
});

return [{
  json: {
    host: url.host,
    pathname: url.pathname,
    search: url.search,
    queryString: params.toString()  // "search=query&page=1&limit=10"
  }
}];
```

---

## What's NOT Available

**External npm packages are NOT available** (unless explicitly allowlisted via `N8N_RUNNERS_ALLOWED_EXTERNAL_MODULES` *and* installed in the runner image — rare):
- ❌ axios
- ❌ lodash
- ❌ moment (use DateTime/Luxon instead)
- ❌ request
- ❌ Any other npm package

**Authentication helpers are blocked** in the task runner sandbox (see section 0):
- ❌ `$helpers.httpRequestWithAuthentication`
- ❌ `$helpers.requestWithAuthenticationPaginated`

**Conditionally blocked** (depends on instance config):
- ⚠️ `$env.*` — blocked when `N8N_BLOCK_ENV_ACCESS_IN_NODE=true`
- ⚠️ `require('crypto')` / `require('fs')` / etc. — blocked unless `N8N_RUNNERS_ALLOWED_BUILT_IN_MODULES` includes them

**Workarounds**:
- HTTP with auth → HTTP Request node with credential attached, or sub-workflow pattern
- Secrets → arrive as data from an upstream HTTP Request / credential-aware node
- Hashing/crypto → do it in a service the workflow calls, or get your instance config updated

---

## Summary

**Most Useful Built-ins**:
1. **$helpers.httpRequest()** - API calls without HTTP Request node
2. **DateTime** - Professional date/time handling
3. **$jmespath()** - Complex JSON queries
4. **Math, JSON, Object, Array** - Standard JavaScript utilities

**Common Patterns**:
- API calls: Use $helpers.httpRequest()
- Date operations: Use DateTime (Luxon)
- Data filtering: Use $jmespath() or JavaScript .filter()
- Persistent data: Use $getWorkflowStaticData()
- Hashing: Use crypto module

**See Also**:
- SKILL.md - Overview
- COMMON_PATTERNS.md - Real usage examples
- ERROR_PATTERNS.md - Error prevention


---

# Common Patterns - JavaScript Code Node

Production-tested patterns for n8n Code nodes. These patterns are proven in real workflows.

---

## Overview

This guide covers the 10 most useful Code node patterns for n8n workflows. Each pattern includes:
- **Use Case**: When to use this pattern
- **Key Techniques**: Important coding techniques demonstrated
- **Complete Example**: Working code you can adapt
- **Variations**: Common modifications

**Pattern Categories:**
- Data Aggregation (Patterns 1, 5, 10)
- Content Processing (Patterns 2, 3)
- Data Validation & Comparison (Patterns 4)
- Data Transformation (Patterns 5, 6, 7)
- Output Formatting (Pattern 8)
- Filtering & Ranking (Pattern 9)

---

## Pattern 1: Multi-Source Data Aggregation

**Use Case**: Combining data from multiple APIs, RSS feeds, webhooks, or databases

**When to use:**
- Collecting data from multiple services
- Normalizing different API response formats
- Merging data sources into unified structure
- Building aggregated reports

**Key Techniques**: Loop iteration, conditional parsing, data normalization

### Complete Example

```javascript
// Process and structure data collected from multiple sources
const allItems = $input.all();
let processedArticles = [];

// Handle different source formats
for (const item of allItems) {
  const sourceName = item.json.name || 'Unknown';
  const sourceData = item.json;

  // Parse source-specific structure - Hacker News format
  if (sourceName === 'Hacker News' && sourceData.hits) {
    for (const hit of sourceData.hits) {
      processedArticles.push({
        title: hit.title,
        url: hit.url,
        summary: hit.story_text || 'No summary',
        source: 'Hacker News',
        score: hit.points || 0,
        fetchedAt: new Date().toISOString()
      });
    }
  }

  // Parse source-specific structure - Reddit format
  else if (sourceName === 'Reddit' && sourceData.data?.children) {
    for (const post of sourceData.data.children) {
      processedArticles.push({
        title: post.data.title,
        url: post.data.url,
        summary: post.data.selftext || 'No summary',
        source: 'Reddit',
        score: post.data.score || 0,
        fetchedAt: new Date().toISOString()
      });
    }
  }

  // Parse source-specific structure - RSS feed format
  else if (sourceName === 'RSS' && sourceData.items) {
    for (const rssItem of sourceData.items) {
      processedArticles.push({
        title: rssItem.title,
        url: rssItem.link,
        summary: rssItem.description || 'No summary',
        source: 'RSS Feed',
        score: 0,
        fetchedAt: new Date().toISOString()
      });
    }
  }
}

// Sort by score (highest first)
processedArticles.sort((a, b) => b.score - a.score);

return processedArticles.map(article => ({json: article}));
```

### Variations

```javascript
// Variation 1: Add source weighting
for (const article of processedArticles) {
  const weights = {
    'Hacker News': 1.5,
    'Reddit': 1.0,
    'RSS Feed': 0.8
  };

  article.weightedScore = article.score * (weights[article.source] || 1.0);
}

// Variation 2: Filter by minimum score
processedArticles = processedArticles.filter(article => article.score >= 10);

// Variation 3: Deduplicate by URL
const seen = new Set();
processedArticles = processedArticles.filter(article => {
  if (seen.has(article.url)) {
    return false;
  }
  seen.add(article.url);
  return true;
});
```

---

## Pattern 2: Regex Filtering & Pattern Matching

**Use Case**: Content analysis, keyword extraction, mention tracking, text parsing

**When to use:**
- Extracting mentions or tags from text
- Finding patterns in unstructured data
- Counting keyword occurrences
- Validating formats (emails, phone numbers)

**Key Techniques**: Regex matching, object aggregation, sorting/ranking

### Complete Example

```javascript
// Extract and track mentions using regex patterns
const etfPattern = /\b([A-Z]{2,5})\b/g;
const knownETFs = ['VOO', 'VTI', 'VT', 'SCHD', 'QYLD', 'VXUS', 'SPY', 'QQQ'];

const etfMentions = {};

for (const item of $input.all()) {
  const data = item.json.data;

  // Skip if no data or children
  if (!data?.children) continue;

  for (const post of data.children) {
    // Combine title and body text
    const title = post.data.title || '';
    const body = post.data.selftext || '';
    const combinedText = (title + ' ' + body).toUpperCase();

    // Find all matches
    const matches = combinedText.match(etfPattern);

    if (matches) {
      for (const match of matches) {
        // Only count known ETFs
        if (knownETFs.includes(match)) {
          if (!etfMentions[match]) {
            etfMentions[match] = {
              count: 0,
              totalScore: 0,
              posts: []
            };
          }

          etfMentions[match].count++;
          etfMentions[match].totalScore += post.data.score || 0;
          etfMentions[match].posts.push({
            title: post.data.title,
            url: post.data.url,
            score: post.data.score
          });
        }
      }
    }
  }
}

// Convert to array and sort by mention count
return Object.entries(etfMentions)
  .map(([etf, data]) => ({
    json: {
      etf,
      mentions: data.count,
      totalScore: data.totalScore,
      averageScore: data.totalScore / data.count,
      topPosts: data.posts
        .sort((a, b) => b.score - a.score)
        .slice(0, 3)
    }
  }))
  .sort((a, b) => b.json.mentions - a.json.mentions);
```

### Variations

```javascript
// Variation 1: Email extraction
const emailPattern = /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g;
const emails = text.match(emailPattern) || [];

// Variation 2: Phone number extraction
const phonePattern = /\b\d{3}[-.]?\d{3}[-.]?\d{4}\b/g;
const phones = text.match(phonePattern) || [];

// Variation 3: Hashtag extraction
const hashtagPattern = /#(\w+)/g;
const hashtags = [];
let match;
while ((match = hashtagPattern.exec(text)) !== null) {
  hashtags.push(match[1]);
}

// Variation 4: URL extraction
const urlPattern = /https?:\/\/[^\s]+/g;
const urls = text.match(urlPattern) || [];
```

---

## Pattern 3: Markdown Parsing & Structured Data Extraction

**Use Case**: Parsing formatted text, extracting structured fields, content transformation

**When to use:**
- Parsing markdown or HTML
- Extracting data from structured text
- Converting formatted content to JSON
- Processing documentation or articles

**Key Techniques**: Regex grouping, helper functions, data normalization, while loops for iteration

### Complete Example

```javascript
// Parse markdown and extract structured information
const markdown = $input.first().json.data.markdown;
const adRegex = /##\s*(.*?)\n(.*?)(?=\n##|\n---|$)/gs;

const ads = [];
let match;

// Helper function to parse time strings to minutes
function parseTimeToMinutes(timeStr) {
  if (!timeStr) return 999999;  // Sort unparseable times last

  const hourMatch = timeStr.match(/(\d+)\s*hour/);
  const dayMatch = timeStr.match(/(\d+)\s*day/);
  const minMatch = timeStr.match(/(\d+)\s*min/);

  let totalMinutes = 0;
  if (dayMatch) totalMinutes += parseInt(dayMatch[1]) * 1440;  // 24 * 60
  if (hourMatch) totalMinutes += parseInt(hourMatch[1]) * 60;
  if (minMatch) totalMinutes += parseInt(minMatch[1]);

  return totalMinutes;
}

// Extract all job postings from markdown
while ((match = adRegex.exec(markdown)) !== null) {
  const title = match[1]?.trim() || 'No title';
  const content = match[2]?.trim() || '';

  // Extract structured fields from content
  const districtMatch = content.match(/\*\*District:\*\*\s*(.*?)(?:\n|$)/);
  const salaryMatch = content.match(/\*\*Salary:\*\*\s*(.*?)(?:\n|$)/);
  const timeMatch = content.match(/Posted:\s*(.*?)\*/);

  ads.push({
    title: title,
    district: districtMatch?.[1].trim() || 'Unknown',
    salary: salaryMatch?.[1].trim() || 'Not specified',
    postedTimeAgo: timeMatch?.[1] || 'Unknown',
    timeInMinutes: parseTimeToMinutes(timeMatch?.[1]),
    fullContent: content,
    extractedAt: new Date().toISOString()
  });
}

// Sort by recency (posted time)
ads.sort((a, b) => a.timeInMinutes - b.timeInMinutes);

return ads.map(ad => ({json: ad}));
```

### Variations

```javascript
// Variation 1: Parse HTML table to JSON
const tableRegex = /<tr>(.*?)<\/tr>/gs;
const cellRegex = /<td>(.*?)<\/td>/g;

const rows = [];
let tableMatch;

while ((tableMatch = tableRegex.exec(htmlTable)) !== null) {
  const cells = [];
  let cellMatch;

  while ((cellMatch = cellRegex.exec(tableMatch[1])) !== null) {
    cells.push(cellMatch[1].trim());
  }

  if (cells.length > 0) {
    rows.push(cells);
  }
}

// Variation 2: Extract code blocks from markdown
const codeBlockRegex = /```(\w+)?\n(.*?)```/gs;
const codeBlocks = [];

while ((match = codeBlockRegex.exec(markdown)) !== null) {
  codeBlocks.push({
    language: match[1] || 'plain',
    code: match[2].trim()
  });
}

// Variation 3: Parse YAML frontmatter
const frontmatterRegex = /^---\n(.*?)\n---/s;
const frontmatterMatch = content.match(frontmatterRegex);

if (frontmatterMatch) {
  const yamlLines = frontmatterMatch[1].split('\n');
  const metadata = {};

  for (const line of yamlLines) {
    const [key, ...valueParts] = line.split(':');
    if (key && valueParts.length > 0) {
      metadata[key.trim()] = valueParts.join(':').trim();
    }
  }
}
```

---

## Pattern 4: JSON Comparison & Validation

**Use Case**: Workflow versioning, configuration validation, change detection, data integrity

**When to use:**
- Comparing two versions of data
- Detecting changes in configurations
- Validating data consistency
- Checking for differences

**Key Techniques**: JSON ordering, base64 decoding, deep comparison, object manipulation

### Complete Example

```javascript
// Compare and validate JSON objects from different sources
const orderJsonKeys = (jsonObj) => {
  const ordered = {};
  Object.keys(jsonObj).sort().forEach(key => {
    ordered[key] = jsonObj[key];
  });
  return ordered;
};

const allItems = $input.all();

// Assume first item is base64-encoded original, second is current
const origWorkflow = JSON.parse(
  Buffer.from(allItems[0].json.content, 'base64').toString()
);
const currentWorkflow = allItems[1].json;

// Order keys for consistent comparison
const orderedOriginal = orderJsonKeys(origWorkflow);
const orderedCurrent = orderJsonKeys(currentWorkflow);

// Deep comparison
const isSame = JSON.stringify(orderedOriginal) === JSON.stringify(orderedCurrent);

// Find differences
const differences = [];
for (const key of Object.keys(orderedOriginal)) {
  if (JSON.stringify(orderedOriginal[key]) !== JSON.stringify(orderedCurrent[key])) {
    differences.push({
      field: key,
      original: orderedOriginal[key],
      current: orderedCurrent[key]
    });
  }
}

// Check for new keys
for (const key of Object.keys(orderedCurrent)) {
  if (!(key in orderedOriginal)) {
    differences.push({
      field: key,
      original: null,
      current: orderedCurrent[key],
      status: 'new'
    });
  }
}

return [{
  json: {
    identical: isSame,
    differenceCount: differences.length,
    differences: differences,
    original: orderedOriginal,
    current: orderedCurrent,
    comparedAt: new Date().toISOString()
  }
}];
```

### Variations

```javascript
// Variation 1: Simple equality check
const isEqual = JSON.stringify(obj1) === JSON.stringify(obj2);

// Variation 2: Deep diff with detailed changes
function deepDiff(obj1, obj2, path = '') {
  const changes = [];

  for (const key in obj1) {
    const currentPath = path ? `${path}.${key}` : key;

    if (!(key in obj2)) {
      changes.push({type: 'removed', path: currentPath, value: obj1[key]});
    } else if (typeof obj1[key] === 'object' && typeof obj2[key] === 'object') {
      changes.push(...deepDiff(obj1[key], obj2[key], currentPath));
    } else if (obj1[key] !== obj2[key]) {
      changes.push({
        type: 'modified',
        path: currentPath,
        from: obj1[key],
        to: obj2[key]
      });
    }
  }

  for (const key in obj2) {
    if (!(key in obj1)) {
      const currentPath = path ? `${path}.${key}` : key;
      changes.push({type: 'added', path: currentPath, value: obj2[key]});
    }
  }

  return changes;
}

// Variation 3: Schema validation
function validateSchema(data, schema) {
  const errors = [];

  for (const field of schema.required || []) {
    if (!(field in data)) {
      errors.push(`Missing required field: ${field}`);
    }
  }

  for (const [field, type] of Object.entries(schema.types || {})) {
    if (field in data && typeof data[field] !== type) {
      errors.push(`Field ${field} should be ${type}, got ${typeof data[field]}`);
    }
  }

  return {
    valid: errors.length === 0,
    errors
  };
}
```

---

## Pattern 5: CRM Data Transformation

**Use Case**: Lead enrichment, data normalization, API preparation, form data processing

**When to use:**
- Processing form submissions
- Preparing data for CRM APIs
- Normalizing contact information
- Enriching lead data

**Key Techniques**: Object destructuring, data mapping, format conversion, field splitting

### Complete Example

```javascript
// Transform form data into CRM-compatible format
const item = $input.all()[0];
const {
  name,
  email,
  phone,
  company,
  course_interest,
  message,
  timestamp
} = item.json;

// Split name into first and last
const nameParts = name.split(' ');
const firstName = nameParts[0] || '';
const lastName = nameParts.slice(1).join(' ') || 'Unknown';

// Format phone number
const cleanPhone = phone.replace(/[^\d]/g, '');  // Remove non-digits

// Build CRM data structure
const crmData = {
  data: {
    type: 'Contact',
    attributes: {
      first_name: firstName,
      last_name: lastName,
      email1: email,
      phone_work: cleanPhone,
      account_name: company,
      description: `Course Interest: ${course_interest}\n\nMessage: ${message}\n\nSubmitted: ${timestamp}`,
      lead_source: 'Website Form',
      status: 'New'
    }
  },
  metadata: {
    original_submission: timestamp,
    processed_at: new Date().toISOString()
  }
};

return [{
  json: {
    ...item.json,
    crmData,
    processed: true
  }
}];
```

### Variations

```javascript
// Variation 1: Multiple contact processing
const contacts = $input.all();

return contacts.map(item => {
  const data = item.json;
  const [firstName, ...lastNameParts] = data.name.split(' ');

  return {
    json: {
      firstName,
      lastName: lastNameParts.join(' ') || 'Unknown',
      email: data.email.toLowerCase(),
      phone: data.phone.replace(/[^\d]/g, ''),
      tags: [data.source, data.interest_level].filter(Boolean)
    }
  };
});

// Variation 2: Field validation and normalization
function normalizePContact(raw) {
  return {
    first_name: raw.firstName?.trim() || '',
    last_name: raw.lastName?.trim() || 'Unknown',
    email: raw.email?.toLowerCase().trim() || '',
    phone: raw.phone?.replace(/[^\d]/g, '') || '',
    company: raw.company?.trim() || 'Unknown',
    title: raw.title?.trim() || '',
    valid: Boolean(raw.email && raw.firstName)
  };
}

// Variation 3: Lead scoring
function calculateLeadScore(data) {
  let score = 0;

  if (data.email) score += 10;
  if (data.phone) score += 10;
  if (data.company) score += 15;
  if (data.title?.toLowerCase().includes('director')) score += 20;
  if (data.title?.toLowerCase().includes('manager')) score += 15;
  if (data.message?.length > 100) score += 10;

  return score;
}
```

---

## Pattern 6: Release Information Processing

**Use Case**: Version management, changelog parsing, release notes generation, GitHub API processing

**When to use:**
- Processing GitHub releases
- Filtering stable versions
- Generating changelog summaries
- Extracting version information

**Key Techniques**: Array filtering, conditional field extraction, date formatting, string manipulation

### Complete Example

```javascript
// Extract and filter stable releases from GitHub API
const allReleases = $input.first().json;

const stableReleases = allReleases
  .filter(release => !release.prerelease && !release.draft)
  .slice(0, 10)
  .map(release => {
    // Extract highlights section from changelog
    const body = release.body || '';
    let highlights = 'No highlights available';

    if (body.includes('## Highlights:')) {
      highlights = body.split('## Highlights:')[1]?.split('##')[0]?.trim();
    } else {
      // Fallback to first 500 chars
      highlights = body.substring(0, 500) + '...';
    }

    return {
      tag: release.tag_name,
      name: release.name,
      published: release.published_at,
      publishedDate: new Date(release.published_at).toLocaleDateString(),
      author: release.author.login,
      url: release.html_url,
      changelog: body,
      highlights: highlights,
      assetCount: release.assets.length,
      assets: release.assets.map(asset => ({
        name: asset.name,
        size: asset.size,
        downloadCount: asset.download_count,
        downloadUrl: asset.browser_download_url
      }))
    };
  });

return stableReleases.map(release => ({json: release}));
```

### Variations

```javascript
// Variation 1: Version comparison
function compareVersions(v1, v2) {
  const parts1 = v1.replace('v', '').split('.').map(Number);
  const parts2 = v2.replace('v', '').split('.').map(Number);

  for (let i = 0; i < Math.max(parts1.length, parts2.length); i++) {
    const num1 = parts1[i] || 0;
    const num2 = parts2[i] || 0;

    if (num1 > num2) return 1;
    if (num1 < num2) return -1;
  }

  return 0;
}

// Variation 2: Breaking change detection
function hasBreakingChanges(changelog) {
  const breakingKeywords = [
    'BREAKING CHANGE',
    'breaking change',
    'BC:',
    '💥'
  ];

  return breakingKeywords.some(keyword => changelog.includes(keyword));
}

// Variation 3: Extract version numbers
const versionPattern = /v?(\d+)\.(\d+)\.(\d+)/;
const match = tagName.match(versionPattern);

if (match) {
  const [_, major, minor, patch] = match;
  const version = {major: parseInt(major), minor: parseInt(minor), patch: parseInt(patch)};
}
```

---

## Pattern 7: Array Transformation with Context

**Use Case**: Quick data transformation, field mapping, adding computed fields

**When to use:**
- Transforming arrays with additional context
- Adding calculated fields
- Simplifying complex objects
- Pluralization logic

**Key Techniques**: Array methods chaining, ternary operators, computed properties

### Complete Example

```javascript
// Transform releases with contextual information
const releases = $input.first().json
  .filter(release => !release.prerelease && !release.draft)
  .slice(0, 10)
  .map(release => ({
    version: release.tag_name,
    assetCount: release.assets.length,
    assetsCountText: release.assets.length === 1 ? 'file' : 'files',
    downloadUrl: release.html_url,
    isRecent: new Date(release.published_at) > new Date(Date.now() - 30 * 24 * 60 * 60 * 1000),
    age: Math.floor((Date.now() - new Date(release.published_at)) / (24 * 60 * 60 * 1000)),
    ageText: `${Math.floor((Date.now() - new Date(release.published_at)) / (24 * 60 * 60 * 1000))} days ago`
  }));

return releases.map(release => ({json: release}));
```

### Variations

```javascript
// Variation 1: Add ranking
const items = $input.all()
  .sort((a, b) => b.json.score - a.json.score)
  .map((item, index) => ({
    json: {
      ...item.json,
      rank: index + 1,
      medal: index < 3 ? ['🥇', '🥈', '🥉'][index] : ''
    }
  }));

// Variation 2: Add percentage calculations
const total = $input.all().reduce((sum, item) => sum + item.json.value, 0);

const itemsWithPercentage = $input.all().map(item => ({
  json: {
    ...item.json,
    percentage: ((item.json.value / total) * 100).toFixed(2) + '%'
  }
}));

// Variation 3: Add category labels
const categorize = (value) => {
  if (value > 100) return 'High';
  if (value > 50) return 'Medium';
  return 'Low';
};

const categorized = $input.all().map(item => ({
  json: {
    ...item.json,
    category: categorize(item.json.value)
  }
}));
```

---

## Pattern 8: Slack Block Kit Formatting

**Use Case**: Chat notifications, rich message formatting, interactive messages

**When to use:**
- Sending formatted Slack messages
- Creating interactive notifications
- Building rich content for chat platforms
- Status reports and alerts

**Key Techniques**: Template literals, nested objects, Block Kit syntax, date formatting

### Complete Example

```javascript
// Create Slack-formatted message with structured blocks
const date = new Date().toISOString().split('T')[0];
const data = $input.first().json;

return [{
  json: {
    text: `Daily Report - ${date}`,  // Fallback text
    blocks: [
      {
        type: "header",
        text: {
          type: "plain_text",
          text: `📊 Daily Security Report - ${date}`
        }
      },
      {
        type: "section",
        text: {
          type: "mrkdwn",
          text: `*Status:* ${data.status === 'ok' ? '✅ All Clear' : '⚠️ Issues Detected'}\n*Alerts:* ${data.alertCount || 0}\n*Updated:* ${new Date().toLocaleString()}`
        }
      },
      {
        type: "divider"
      },
      {
        type: "section",
        fields: [
          {
            type: "mrkdwn",
            text: `*Failed Logins:*\n${data.failedLogins || 0}`
          },
          {
            type: "mrkdwn",
            text: `*API Errors:*\n${data.apiErrors || 0}`
          },
          {
            type: "mrkdwn",
            text: `*Uptime:*\n${data.uptime || '100%'}`
          },
          {
            type: "mrkdwn",
            text: `*Response Time:*\n${data.avgResponseTime || 'N/A'}ms`
          }
        ]
      },
      {
        type: "context",
        elements: [{
          type: "mrkdwn",
          text: `Report generated automatically by n8n workflow`
        }]
      }
    ]
  }
}];
```

### Variations

```javascript
// Variation 1: Interactive buttons
const blocksWithButtons = [
  {
    type: "section",
    text: {
      type: "mrkdwn",
      text: "Would you like to approve this request?"
    },
    accessory: {
      type: "button",
      text: {
        type: "plain_text",
        text: "Approve"
      },
      style: "primary",
      value: "approve",
      action_id: "approve_button"
    }
  }
];

// Variation 2: List formatting
const items = ['Item 1', 'Item 2', 'Item 3'];
const formattedList = items.map((item, i) => `${i + 1}. ${item}`).join('\n');

// Variation 3: Status indicators
function getStatusEmoji(status) {
  const statusMap = {
    'success': '✅',
    'warning': '⚠️',
    'error': '❌',
    'info': 'ℹ️'
  };

  return statusMap[status] || '•';
}

// Variation 4: Truncate long messages
function truncate(text, maxLength = 3000) {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength - 3) + '...';
}
```

---

## Pattern 9: Top N Filtering & Ranking

**Use Case**: RAG pipelines, ranking algorithms, result filtering, leaderboards

**When to use:**
- Getting top results by score
- Filtering best/worst performers
- Building leaderboards
- Relevance ranking

**Key Techniques**: Sorting, slicing, null coalescing, score calculations

### Complete Example

```javascript
// Filter and rank by similarity score, return top results
const ragResponse = $input.item.json;
const chunks = ragResponse.chunks || [];

// Sort by similarity (highest first)
const topChunks = chunks
  .sort((a, b) => (b.similarity || 0) - (a.similarity || 0))
  .slice(0, 6);

return [{
  json: {
    query: ragResponse.query,
    topChunks: topChunks,
    count: topChunks.length,
    maxSimilarity: topChunks[0]?.similarity || 0,
    minSimilarity: topChunks[topChunks.length - 1]?.similarity || 0,
    averageSimilarity: topChunks.reduce((sum, chunk) => sum + (chunk.similarity || 0), 0) / topChunks.length
  }
}];
```

### Variations

```javascript
// Variation 1: Top N with minimum threshold
const threshold = 0.7;
const topItems = $input.all()
  .filter(item => item.json.score >= threshold)
  .sort((a, b) => b.json.score - a.json.score)
  .slice(0, 10);

// Variation 2: Bottom N (worst performers)
const bottomItems = $input.all()
  .sort((a, b) => a.json.score - b.json.score)  // Ascending
  .slice(0, 5);

// Variation 3: Top N by multiple criteria
const ranked = $input.all()
  .map(item => ({
    ...item,
    compositeScore: (item.json.relevance * 0.6) + (item.json.recency * 0.4)
  }))
  .sort((a, b) => b.compositeScore - a.compositeScore)
  .slice(0, 10);

// Variation 4: Percentile filtering
const allScores = $input.all().map(item => item.json.score).sort((a, b) => b - a);
const percentile95 = allScores[Math.floor(allScores.length * 0.05)];

const topPercentile = $input.all().filter(item => item.json.score >= percentile95);
```

---

## Pattern 10: String Aggregation & Reporting

**Use Case**: Report generation, log aggregation, content concatenation, summary creation

**When to use:**
- Combining multiple text outputs
- Generating reports from data
- Aggregating logs or messages
- Creating formatted summaries

**Key Techniques**: Array joining, string concatenation, template literals, timestamp handling

### Complete Example

```javascript
// Aggregate multiple text inputs into formatted report
const allItems = $input.all();

// Collect all messages
const messages = allItems.map(item => item.json.message);

// Build report
const header = `🎯 **Daily Summary Report**\n📅 ${new Date().toLocaleString()}\n📊 Total Items: ${messages.length}\n\n`;
const divider = '\n\n---\n\n';
const footer = `\n\n---\n\n✅ Report generated at ${new Date().toISOString()}`;

const finalReport = header + messages.join(divider) + footer;

return [{
  json: {
    report: finalReport,
    messageCount: messages.length,
    generatedAt: new Date().toISOString(),
    reportLength: finalReport.length
  }
}];
```

### Variations

```javascript
// Variation 1: Numbered list
const numberedReport = allItems
  .map((item, index) => `${index + 1}. ${item.json.title}\n   ${item.json.description}`)
  .join('\n\n');

// Variation 2: Markdown table
const headers = '| Name | Status | Score |\n|------|--------|-------|\n';
const rows = allItems
  .map(item => `| ${item.json.name} | ${item.json.status} | ${item.json.score} |`)
  .join('\n');

const table = headers + rows;

// Variation 3: HTML report
const htmlReport = `
<!DOCTYPE html>
<html>
<head><title>Report</title></head>
<body>
  <h1>Report - ${new Date().toLocaleDateString()}</h1>
  <ul>
    ${allItems.map(item => `<li>${item.json.title}: ${item.json.value}</li>`).join('\n    ')}
  </ul>
</body>
</html>
`;

// Variation 4: JSON summary
const summary = {
  generated: new Date().toISOString(),
  totalItems: allItems.length,
  items: allItems.map(item => item.json),
  statistics: {
    total: allItems.reduce((sum, item) => sum + (item.json.value || 0), 0),
    average: allItems.reduce((sum, item) => sum + (item.json.value || 0), 0) / allItems.length,
    max: Math.max(...allItems.map(item => item.json.value || 0)),
    min: Math.min(...allItems.map(item => item.json.value || 0))
  }
};
```

---

## Choosing the Right Pattern

### Pattern Selection Guide

| Your Goal | Use Pattern |
|-----------|-------------|
| Combine multiple API responses | Pattern 1 (Multi-source Aggregation) |
| Extract mentions or keywords | Pattern 2 (Regex Filtering) |
| Parse formatted text | Pattern 3 (Markdown Parsing) |
| Detect changes in data | Pattern 4 (JSON Comparison) |
| Prepare form data for CRM | Pattern 5 (CRM Transformation) |
| Process GitHub releases | Pattern 6 (Release Processing) |
| Add computed fields | Pattern 7 (Array Transformation) |
| Format Slack messages | Pattern 8 (Block Kit Formatting) |
| Get top results | Pattern 9 (Top N Filtering) |
| Create text reports | Pattern 10 (String Aggregation) |

### Combining Patterns

Many real workflows combine multiple patterns:

```javascript
// Example: Multi-source aggregation + Top N filtering
const allItems = $input.all();
const aggregated = [];

// Pattern 1: Aggregate from different sources
for (const item of allItems) {
  // ... aggregation logic
  aggregated.push(normalizedItem);
}

// Pattern 9: Get top 10 by score
const top10 = aggregated
  .sort((a, b) => b.score - a.score)
  .slice(0, 10);

// Pattern 10: Generate report
const report = `Top 10 Items:\n\n${top10.map((item, i) => `${i + 1}. ${item.title} (${item.score})`).join('\n')}`;

return [{json: {report, items: top10}}];
```

---

## Summary

**Most Useful Patterns**:
1. Multi-source Aggregation - Combining data from APIs, databases
2. Top N Filtering - Rankings, leaderboards, best results
3. Data Transformation - CRM data, field mapping, enrichment

**Key Techniques Across Patterns**:
- Array methods (map, filter, reduce, sort, slice)
- Regex for pattern matching
- Object manipulation and destructuring
- Error handling with optional chaining
- Template literals for formatting

**See Also**:
- DATA_ACCESS.md - Data access methods
- ERROR_PATTERNS.md - Avoid common mistakes
- BUILTIN_FUNCTIONS.md - Built-in helpers


---

# Error Patterns - JavaScript Code Node

Complete guide to avoiding the most common Code node errors.

---

## Overview

This guide covers the **top 5 error patterns** encountered in n8n Code nodes. Understanding and avoiding these errors will save you significant debugging time.

**Error Frequency**:
1. Empty Code / Missing Return - **38% of failures**
2. Expression Syntax Confusion - **8% of failures**
3. Incorrect Return Wrapper - **5% of failures**
4. Unmatched Expression Brackets - **6% of failures**
5. Missing Null Checks - **Common runtime error**

---

## Error #1: Empty Code or Missing Return Statement

**Frequency**: Most common error (38% of all validation failures)

**What Happens**:
- Workflow execution fails
- Next nodes receive no data
- Error: "Code cannot be empty" or "Code must return data"

### The Problem

```javascript
// ❌ ERROR: No code at all
// (Empty code field)
```

```javascript
// ❌ ERROR: Code executes but doesn't return anything
const items = $input.all();

// Process items
for (const item of items) {
  console.log(item.json.name);
}

// Forgot to return!
```

```javascript
// ❌ ERROR: Early return path exists, but not all paths return
const items = $input.all();

if (items.length === 0) {
  return [];  // ✅ This path returns
}

// Process items
const processed = items.map(item => ({json: item.json}));

// ❌ Forgot to return processed!
```

### The Solution

```javascript
// ✅ CORRECT: Always return data
const items = $input.all();

// Process items
const processed = items.map(item => ({
  json: {
    ...item.json,
    processed: true
  }
}));

return processed;  // ✅ Return statement present
```

```javascript
// ✅ CORRECT: Return empty array if no items
const items = $input.all();

if (items.length === 0) {
  return [];  // Valid: empty array when no data
}

// Process and return
return items.map(item => ({json: item.json}));
```

```javascript
// ✅ CORRECT: All code paths return
const items = $input.all();

if (items.length === 0) {
  return [];
} else if (items.length === 1) {
  return [{json: {single: true, data: items[0].json}}];
} else {
  return items.map(item => ({json: item.json}));
}

// All paths covered
```

### Checklist

- [ ] Code field is not empty
- [ ] Return statement exists
- [ ] ALL code paths return data (if/else branches)
- [ ] Return format is correct (`[{json: {...}}]`)
- [ ] Return happens even on errors (use try-catch)

---

## Error #2: Expression Syntax Confusion

**Frequency**: 8% of validation failures

**What Happens**:
- Syntax error in code execution
- Error: "Unexpected token" or "Expression syntax is not valid in Code nodes"
- Template variables not evaluated

### The Problem

n8n has TWO distinct syntaxes:
1. **Expression syntax** `{{ }}` - Used in OTHER nodes (Set, IF, HTTP Request)
2. **JavaScript** - Used in CODE nodes (no `{{ }}`)

Many developers mistakenly use expression syntax inside Code nodes.

```javascript
// ❌ WRONG: Using n8n expression syntax in Code node
const userName = "{{ $json.name }}";
const userEmail = "{{ $json.body.email }}";

return [{
  json: {
    name: userName,
    email: userEmail
  }
}];

// Result: Literal string "{{ $json.name }}", NOT the value!
```

```javascript
// ❌ WRONG: Trying to evaluate expressions
const value = "{{ $now.toFormat('yyyy-MM-dd') }}";
```

### The Solution

```javascript
// ✅ CORRECT: Use JavaScript directly (no {{ }})
const userName = $json.name;
const userEmail = $json.body.email;

return [{
  json: {
    name: userName,
    email: userEmail
  }
}];
```

```javascript
// ✅ CORRECT: JavaScript template literals (use backticks)
const message = `Hello, ${$json.name}! Your email is ${$json.email}`;

return [{
  json: {
    greeting: message
  }
}];
```

```javascript
// ✅ CORRECT: Direct variable access
const item = $input.first().json;

return [{
  json: {
    name: item.name,
    email: item.email,
    timestamp: new Date().toISOString()  // JavaScript Date, not {{ }}
  }
}];
```

### Comparison Table

| Context | Syntax | Example |
|---------|--------|---------|
| Set node | `{{ }}` expressions | `{{ $json.name }}` |
| IF node | `{{ }}` expressions | `{{ $json.age > 18 }}` |
| HTTP Request URL | `{{ }}` expressions | `{{ $json.userId }}` |
| **Code node** | **JavaScript** | `$json.name` |
| **Code node strings** | **Template literals** | `` `Hello ${$json.name}` `` |

### Quick Fix Guide

```javascript
// WRONG → RIGHT conversions

// ❌ "{{ $json.field }}"
// ✅ $json.field

// ❌ "{{ $now }}"
// ✅ new Date().toISOString()

// ❌ "{{ $node['HTTP Request'].json.data }}"
// ✅ $node["HTTP Request"].json.data

// ❌ `{{ $json.firstName }} {{ $json.lastName }}`
// ✅ `${$json.firstName} ${$json.lastName}`
```

---

## Error #3: Incorrect Return Wrapper Format

**Frequency**: 5% of validation failures

**What Happens**:
- Error: "Return value must be an array of objects"
- Error: "Each item must have a json property"
- Next nodes receive malformed data

### The Problem

Code nodes MUST return:
- **Array** of objects
- Each object MUST have a **`json` property**

```javascript
// ❌ WRONG: Returning object instead of array
return {
  json: {
    result: 'success'
  }
};
// Missing array wrapper []
```

```javascript
// ❌ WRONG: Returning array without json wrapper
return [
  {id: 1, name: 'Alice'},
  {id: 2, name: 'Bob'}
];
// Missing json property
```

```javascript
// ❌ WRONG: Returning plain value
return "processed";
```

```javascript
// ❌ WRONG: Returning items without mapping
return $input.all();
// Works if items already have json property, but not guaranteed
```

```javascript
// ❌ WRONG: Incomplete structure
return [{data: {result: 'success'}}];
// Should be {json: {...}}, not {data: {...}}
```

### The Solution

```javascript
// ✅ CORRECT: Single result
return [{
  json: {
    result: 'success',
    timestamp: new Date().toISOString()
  }
}];
```

```javascript
// ✅ CORRECT: Multiple results
return [
  {json: {id: 1, name: 'Alice'}},
  {json: {id: 2, name: 'Bob'}},
  {json: {id: 3, name: 'Carol'}}
];
```

```javascript
// ✅ CORRECT: Transforming array
const items = $input.all();

return items.map(item => ({
  json: {
    id: item.json.id,
    name: item.json.name,
    processed: true
  }
}));
```

```javascript
// ✅ CORRECT: Empty result
return [];
// Valid when no data to return
```

```javascript
// ✅ CORRECT: Conditional returns
if (shouldProcess) {
  return [{json: {result: 'processed'}}];
} else {
  return [];
}
```

### Return Format Checklist

- [ ] Return value is an **array** `[...]`
- [ ] Each array element has **`json` property**
- [ ] Structure is `[{json: {...}}]` or `[{json: {...}}, {json: {...}}]`
- [ ] NOT `{json: {...}}` (missing array wrapper)
- [ ] NOT `[{...}]` (missing json property)

### Common Scenarios

```javascript
// Scenario 1: Single object from API
const response = $input.first().json;

// ✅ CORRECT
return [{json: response}];

// ❌ WRONG
return {json: response};


// Scenario 2: Array of objects
const users = $input.all();

// ✅ CORRECT
return users.map(user => ({json: user.json}));

// ❌ WRONG
return users;  // Risky - depends on existing structure


// Scenario 3: Computed result
const total = $input.all().reduce((sum, item) => sum + item.json.amount, 0);

// ✅ CORRECT
return [{json: {total}}];

// ❌ WRONG
return {total};


// Scenario 4: No results
// ✅ CORRECT
return [];

// ❌ WRONG
return null;
```

---

## Error #4: Unmatched Expression Brackets

**Frequency**: 6% of validation failures

**What Happens**:
- Parsing error during save
- Error: "Unmatched expression brackets"
- Code appears correct but fails validation

### The Problem

This error typically occurs when:
1. Strings contain unbalanced quotes
2. Multi-line strings with special characters
3. Template literals with nested brackets

```javascript
// ❌ WRONG: Unescaped quote in string
const message = "It's a nice day";
// Single quote breaks string
```

```javascript
// ❌ WRONG: Unbalanced brackets in regex
const pattern = /\{(\w+)\}/;  // JSON storage issue
```

```javascript
// ❌ WRONG: Multi-line string with quotes
const html = "
  <div class="container">
    <p>Hello</p>
  </div>
";
// Quote balance issues
```

### The Solution

```javascript
// ✅ CORRECT: Escape quotes
const message = "It\\'s a nice day";
// Or use different quotes
const message = "It's a nice day";  // Double quotes work
```

```javascript
// ✅ CORRECT: Escape regex properly
const pattern = /\\{(\\w+)\\}/;
```

```javascript
// ✅ CORRECT: Template literals for multi-line
const html = `
  <div class="container">
    <p>Hello</p>
  </div>
`;
// Backticks handle multi-line and quotes
```

```javascript
// ✅ CORRECT: Escape backslashes
const path = "C:\\\\Users\\\\Documents\\\\file.txt";
```

### Escaping Guide

| Character | Escape As | Example |
|-----------|-----------|---------|
| Single quote in single-quoted string | `\\'` | `'It\\'s working'` |
| Double quote in double-quoted string | `\\"` | `"She said \\"hello\\""` |
| Backslash | `\\\\` | `"C:\\\\path"` |
| Newline | `\\n` | `"Line 1\\nLine 2"` |
| Tab | `\\t` | `"Column1\\tColumn2"` |

### Best Practices

```javascript
// ✅ BEST: Use template literals for complex strings
const message = `User ${name} said: "Hello!"`;

// ✅ BEST: Use template literals for HTML
const html = `
  <div class="${className}">
    <h1>${title}</h1>
    <p>${content}</p>
  </div>
`;

// ✅ BEST: Use template literals for JSON
const jsonString = `{
  "name": "${name}",
  "email": "${email}"
}`;
```

---

## Error #5: Missing Null Checks / Undefined Access

**Frequency**: Very common runtime error

**What Happens**:
- Workflow execution stops
- Error: "Cannot read property 'X' of undefined"
- Error: "Cannot read property 'X' of null"
- Crashes on missing data

### The Problem

```javascript
// ❌ WRONG: No null check - crashes if user doesn't exist
const email = item.json.user.email;
```

```javascript
// ❌ WRONG: Assumes array has items
const firstItem = $input.all()[0].json;
```

```javascript
// ❌ WRONG: Assumes nested property exists
const city = $json.address.city;
```

```javascript
// ❌ WRONG: No validation before array operations
const names = $json.users.map(user => user.name);
```

### The Solution

```javascript
// ✅ CORRECT: Optional chaining
const email = item.json?.user?.email || 'no-email@example.com';
```

```javascript
// ✅ CORRECT: Check array length
const items = $input.all();

if (items.length === 0) {
  return [];
}

const firstItem = items[0].json;
```

```javascript
// ✅ CORRECT: Guard clauses
const data = $input.first().json;

if (!data.address) {
  return [{json: {error: 'No address provided'}}];
}

const city = data.address.city;
```

```javascript
// ✅ CORRECT: Default values
const users = $json.users || [];
const names = users.map(user => user.name || 'Unknown');
```

```javascript
// ✅ CORRECT: Try-catch for risky operations
try {
  const email = item.json.user.email.toLowerCase();
  return [{json: {email}}];
} catch (error) {
  return [{
    json: {
      error: 'Invalid user data',
      details: error.message
    }
  }];
}
```

### Safe Access Patterns

```javascript
// Pattern 1: Optional chaining (modern, recommended)
const value = data?.nested?.property?.value;

// Pattern 2: Logical OR with default
const value = data.property || 'default';

// Pattern 3: Ternary check
const value = data.property ? data.property : 'default';

// Pattern 4: Guard clause
if (!data.property) {
  return [];
}
const value = data.property;

// Pattern 5: Try-catch
try {
  const value = data.nested.property.value;
} catch (error) {
  const value = 'default';
}
```

### Webhook Data Safety

```javascript
// Webhook data requires extra safety

// ❌ RISKY: Assumes all fields exist
const name = $json.body.user.name;
const email = $json.body.user.email;

// ✅ SAFE: Check each level
const body = $json.body || {};
const user = body.user || {};
const name = user.name || 'Unknown';
const email = user.email || 'no-email';

// ✅ BETTER: Optional chaining
const name = $json.body?.user?.name || 'Unknown';
const email = $json.body?.user?.email || 'no-email';
```

### Array Safety

```javascript
// ❌ RISKY: No length check
const items = $input.all();
const firstId = items[0].json.id;

// ✅ SAFE: Check length
const items = $input.all();

if (items.length > 0) {
  const firstId = items[0].json.id;
} else {
  // Handle empty case
  return [];
}

// ✅ BETTER: Use $input.first()
const firstItem = $input.first();
const firstId = firstItem.json.id;  // Built-in safety
```

### Object Property Safety

```javascript
// ❌ RISKY: Direct access
const config = $json.settings.advanced.timeout;

// ✅ SAFE: Step by step with defaults
const settings = $json.settings || {};
const advanced = settings.advanced || {};
const timeout = advanced.timeout || 30000;

// ✅ BETTER: Optional chaining
const timeout = $json.settings?.advanced?.timeout ?? 30000;
// Note: ?? (nullish coalescing) vs || (logical OR)
```

---

## Error #6: UnsupportedFunctionError (Auth Helpers Blocked)

**Frequency**: The most common "this worked yesterday in old n8n" error after upgrading to v2.0+

**What Happens**:
- Error: `UnsupportedFunctionError: The function "helpers.httpRequestWithAuthentication" is not supported in the Code Node`
- Same for `helpers.requestWithAuthenticationPaginated`
- Throws on execution, not on save

### The Problem

Since n8n v2.0, Code nodes execute in the **task runner sandbox** which deliberately blocks the auth helpers. The legacy vm2 sandbox used to bind them, which is why old forum posts and tutorials show them working. n8n's source comment explains why: the Code node has no credential of its own, so the helper had nothing to authenticate against — it was always semantically broken, just not always loud about it.

```javascript
// ❌ BLOCKED in task runner sandbox (default since v2.0)
const data = await $helpers.httpRequestWithAuthentication.call(
  this,
  'baseLinkerApi',
  { url: '...', method: 'POST' }
);
```

### The Solution

There is **no env flag** to re-enable these in the runner — the deny-list is compiled-in. Pick one of:

**Option A — Replace the Code node with an HTTP Request node** (best):

The HTTP Request node natively supports credential attachment with full expression support for URL/body/headers. Most "Code-node-makes-an-API-call" patterns are leftovers from before HTTP Request had pagination and expression support.

**Option B — Sub-workflow with HTTP Request node** (when you need code-level logic before/after):

```javascript
// Parent Code node — prepare payloads, then delegate
return $input.all().map(i => ({ json: {
  url: 'https://api.example.com/things',
  method: 'POST',
  body: { sku: i.json.sku }
}}));
```

Then wire to **Execute Workflow** → child workflow with **Execute Workflow Trigger** → **HTTP Request** node using `={{ $json.url }}`, `={{ $json.body }}`, with the credential attached natively.

**Option C — Token as runtime data** (only when the token genuinely flows through the workflow):

```javascript
// ✅ Works — manual auth header, token came from upstream
const token = $('Get Token').first().json.access_token;

const data = await $helpers.httpRequest({
  url: 'https://api.example.com/data',
  headers: { 'Authorization': `Bearer ${token}` }
});
```

### Decision Guide

| Need | Use |
|------|-----|
| Single authenticated API call | HTTP Request node directly |
| Many API calls + pre/post processing | Sub-workflow pattern (Option B) |
| Token already in the data flow | Manual `$helpers.httpRequest()` with header |
| `httpRequestWithAuthentication` | **Doesn't work — pick A, B, or C above** |

---

## Error #7: $env is not defined / Cannot access $env

**Frequency**: Common in hardened production instances

**What Happens**:
- Error: `$env is not defined` or `ReferenceError: $env is not defined`
- Code looks correct, runs fine on dev instance, throws in production

### The Problem

`$env` access is gated by the **`N8N_BLOCK_ENV_ACCESS_IN_NODE`** environment variable. When set to `true` (a common production hardening setting), `$env` is removed from the Code node sandbox entirely. This is increasingly the default in security-conscious deployments.

```javascript
// ❌ Throws if N8N_BLOCK_ENV_ACCESS_IN_NODE=true
const apiKey = $env.API_KEY;
```

### The Solution

Treat secrets as a **credential concern**, not a Code-node concern:

```javascript
// ✅ Token arrives as data from an upstream node that used a credential
const apiKey = $('Set Secret').first().json.apiKey;

// Or: secret was attached server-side by an HTTP Request node with the credential
// — your Code node never sees the raw secret, which is the whole point
```

For values you genuinely need to inject from outside the workflow (config, not secrets), use:
- A **Set** node at the top of the workflow with hardcoded constants, or
- An **n8n credential** referenced by an HTTP Request node, or
- The **External Secrets** integration (`$secrets`) if your edition supports it.

### Why This Matters

Skills and tutorials written before 2024 routinely use `$env.API_KEY` because it was the path of least resistance. Modern n8n setups block it because letting Code nodes read arbitrary env vars is a privilege escalation surface — any user with workflow-edit access could exfiltrate `DB_PASSWORD`, `N8N_ENCRYPTION_KEY`, etc. Don't fight the restriction; route secrets through credentials.

---

## Error Prevention Checklist

Use this checklist before deploying Code nodes:

### Code Structure
- [ ] Code field is not empty
- [ ] Return statement exists
- [ ] All code paths return data

### Return Format
- [ ] Returns array: `[...]`
- [ ] Each item has `json` property: `{json: {...}}`
- [ ] Format is `[{json: {...}}]`

### Syntax
- [ ] No `{{ }}` expression syntax (use JavaScript)
- [ ] Template literals use backticks: `` `${variable}` ``
- [ ] All quotes and brackets balanced
- [ ] Strings properly escaped

### Data Safety
- [ ] Null checks for optional properties
- [ ] Array length checks before access
- [ ] Webhook data accessed via `.body`
- [ ] Try-catch for risky operations
- [ ] Default values for missing data

### Testing
- [ ] Test with empty input
- [ ] Test with missing fields
- [ ] Test with unexpected data types
- [ ] Check browser console for errors

---

## Quick Error Reference

| Error Message | Likely Cause | Fix |
|---------------|--------------|-----|
| "Code cannot be empty" | Empty code field | Add meaningful code |
| "Code must return data" | Missing return statement | Add `return [...]` |
| "Return value must be an array" | Returning object instead of array | Wrap in `[...]` |
| "Each item must have json property" | Missing `json` wrapper | Use `{json: {...}}` |
| "Unexpected token" | Expression syntax `{{ }}` in code | Remove `{{ }}`, use JavaScript |
| "Cannot read property X of undefined" | Missing null check | Use optional chaining `?.` |
| "Cannot read property X of null" | Null value access | Add guard clause or default |
| "Unmatched expression brackets" | Quote/bracket imbalance | Check string escaping |
| "UnsupportedFunctionError ... httpRequestWithAuthentication" | Auth helper blocked in task runner | Use HTTP Request node + credential, or sub-workflow pattern (Error #6) |
| "$env is not defined" | `N8N_BLOCK_ENV_ACCESS_IN_NODE=true` | Route secrets through credentials, not `$env` (Error #7) |
| "Cannot find module 'crypto'" | `require()` allowlist not set | Move logic out of Code node, or set `N8N_RUNNERS_ALLOWED_BUILT_IN_MODULES` |

---

## Debugging Tips

### 1. Use console.log()

```javascript
const items = $input.all();
console.log('Items count:', items.length);
console.log('First item:', items[0]);

// Check browser console (F12) for output
```

### 2. Return Intermediate Results

```javascript
// Debug by returning current state
const items = $input.all();
const processed = items.map(item => ({json: item.json}));

// Return to see what you have
return processed;
```

### 3. Try-Catch for Troubleshooting

```javascript
try {
  // Your code here
  const result = riskyOperation();
  return [{json: {result}}];
} catch (error) {
  // See what failed
  return [{
    json: {
      error: error.message,
      stack: error.stack
    }
  }];
}
```

### 4. Validate Input Structure

```javascript
const items = $input.all();

// Check what you received
console.log('Input structure:', JSON.stringify(items[0], null, 2));

// Then process
```

---

## Summary

**Top 7 Errors to Avoid**:
1. **Empty code / missing return** (38%) - Always return data
2. **Expression syntax `{{ }}`** (8%) - Use JavaScript, not expressions
3. **Wrong return format** (5%) - Always `[{json: {...}}]`
4. **Unmatched brackets** (6%) - Escape strings properly
5. **Missing null checks** - Use optional chaining `?.`
6. **`httpRequestWithAuthentication` blocked** - Use HTTP Request node + credential
7. **`$env` blocked** - Route secrets through credentials, not env access

**Quick Prevention**:
- Return `[{json: {...}}]` format
- Use JavaScript, NOT `{{ }}` expressions
- Check for null/undefined before accessing
- Test with empty and invalid data
- Use browser console for debugging

**See Also**:
- SKILL.md - Overview and best practices
- DATA_ACCESS.md - Safe data access patterns
- COMMON_PATTERNS.md - Working examples
