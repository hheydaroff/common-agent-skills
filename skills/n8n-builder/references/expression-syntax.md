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


# n8n Expression Syntax

Expert guide for writing correct n8n expressions in workflows.

---

## Expression Format

All dynamic content in n8n uses **double curly braces**:

```
{{expression}}
```

**Examples**:
```
✅ {{$json.email}}
✅ {{$json.body.name}}
✅ {{$node["HTTP Request"].json.data}}
❌ $json.email  (no braces - treated as literal text)
❌ {$json.email}  (single braces - invalid)
```

---

## Core Variables

### $json - Current Node Output

Access data from the current node:

```javascript
{{$json.fieldName}}
{{$json['field with spaces']}}
{{$json.nested.property}}
{{$json.items[0].name}}
```

### $node - Reference Other Nodes

Access data from any previous node:

```javascript
{{$node["Node Name"].json.fieldName}}
{{$node["HTTP Request"].json.data}}
{{$node["Webhook"].json.body.email}}
```

**Important**:
- Node names **must** be in quotes
- Node names are **case-sensitive**
- Must match exact node name from workflow

### $now - Current Timestamp

Access current date/time:

```javascript
{{$now}}
{{$now.toFormat('yyyy-MM-dd')}}
{{$now.toFormat('HH:mm:ss')}}
{{$now.plus({days: 7})}}
```

### $env - Environment Variables

Access environment variables:

```javascript
{{$env.API_KEY}}
{{$env.DATABASE_URL}}
```

**Warning**: Some n8n instances have `N8N_BLOCK_ENV_ACCESS_IN_NODE` enabled, which blocks `$env` access entirely. If `$env` returns errors, use alternative approaches:
- Store values in credentials instead
- Use a Set node with manually entered values
- Pass values through webhook query parameters

---

## 🚨 CRITICAL: Webhook Data Structure

**Most Common Mistake**: Webhook data is **NOT** at the root!

### Webhook Node Output Structure

```javascript
{
  "headers": {...},
  "params": {...},
  "query": {...},
  "body": {           // ⚠️ USER DATA IS HERE!
    "name": "John",
    "email": "john@example.com",
    "message": "Hello"
  }
}
```

### Correct Webhook Data Access

```javascript
❌ WRONG: {{$json.name}}
❌ WRONG: {{$json.email}}

✅ CORRECT: {{$json.body.name}}
✅ CORRECT: {{$json.body.email}}
✅ CORRECT: {{$json.body.message}}
```

**Why**: Webhook node wraps incoming data under `.body` property to preserve headers, params, and query parameters.

---

## Common Patterns

### Access Nested Fields

```javascript
// Simple nesting
{{$json.user.email}}

// Array access
{{$json.data[0].name}}
{{$json.items[0].id}}

// Bracket notation for spaces
{{$json['field name']}}
{{$json['user data']['first name']}}
```

### Reference Other Nodes

```javascript
// Node without spaces
{{$node["Set"].json.value}}

// Node with spaces (common!)
{{$node["HTTP Request"].json.data}}
{{$node["Respond to Webhook"].json.message}}

// Webhook node
{{$node["Webhook"].json.body.email}}
```

### Combine Variables

```javascript
// Concatenation (automatic)
Hello {{$json.body.name}}!

// In URLs
https://api.example.com/users/{{$json.body.user_id}}

// In object properties
{
  "name": "={{$json.body.name}}",
  "email": "={{$json.body.email}}"
}
```

---

## When NOT to Use Expressions

### ❌ Code Nodes

Code nodes use **direct JavaScript access**, NOT expressions!

```javascript
// ❌ WRONG in Code node
const email = '={{$json.email}}';
const name = '{{$json.body.name}}';

// ✅ CORRECT in Code node
const email = $json.email;
const name = $json.body.name;

// Or using Code node API
const email = $input.item.json.email;
const allItems = $input.all();
```

### ❌ Webhook Paths

```javascript
// ❌ WRONG
path: "{{$json.user_id}}/webhook"

// ✅ CORRECT
path: "user-webhook"  // Static paths only
```

### ❌ Credential Fields

```javascript
// ❌ WRONG
apiKey: "={{$env.API_KEY}}"

// ✅ CORRECT
Use n8n credential system, not expressions
```

---

## Validation Rules

### 1. Always Use {{}}

Expressions **must** be wrapped in double curly braces.

```javascript
❌ $json.field
✅ {{$json.field}}
```

### 2. Use Quotes for Spaces and Special Characters

Field or node names with spaces, diacritics, or special characters require **bracket notation**:

```javascript
❌ {{$json.field name}}
✅ {{$json['field name']}}

❌ {{$node.HTTP Request.json}}
✅ {{$node["HTTP Request"].json}}

// Bracket notation is mandatory for keys with special characters
✅ {{$json['Gross Price w/o shipment']}}
✅ {{$json['Cena brutto zł']}}
```

### 3. Match Exact Node Names

Node references are **case-sensitive**:

```javascript
❌ {{$node["http request"].json}}  // lowercase
❌ {{$node["Http Request"].json}}  // wrong case
✅ {{$node["HTTP Request"].json}}  // exact match
```

### 4. No Nested {{}}

Don't double-wrap expressions:

```javascript
❌ {{{$json.field}}}
✅ {{$json.field}}
```

---

## Common Mistakes

For complete error catalog with fixes, see COMMON_MISTAKES.md

### Quick Fixes

| Mistake | Fix |
|---------|-----|
| `$json.field` | `{{$json.field}}` |
| `{{$json.field name}}` | `{{$json['field name']}}` |
| `{{$node.HTTP Request}}` | `{{$node["HTTP Request"]}}` |
| `{{{$json.field}}}` | `{{$json.field}}` |
| `{{$json.name}}` (webhook) | `{{$json.body.name}}` |
| `'={{$json.email}}'` (Code node) | `$json.email` |

---

## Working Examples

For real workflow examples, see EXAMPLES.md

### Example 1: Webhook to Slack

**Webhook receives**:
```json
{
  "body": {
    "name": "John Doe",
    "email": "john@example.com",
    "message": "Hello!"
  }
}
```

**In Slack node text field**:
```
New form submission!

Name: {{$json.body.name}}
Email: {{$json.body.email}}
Message: {{$json.body.message}}
```

### Example 2: HTTP Request to Email

**HTTP Request returns**:
```json
{
  "data": {
    "items": [
      {"name": "Product 1", "price": 29.99}
    ]
  }
}
```

**In Email node** (reference HTTP Request):
```
Product: {{$node["HTTP Request"].json.data.items[0].name}}
Price: ${{$node["HTTP Request"].json.data.items[0].price}}
```

### Example 3: Format Timestamp

```javascript
// Current date
{{$now.toFormat('yyyy-MM-dd')}}
// Result: 2025-10-20

// Time
{{$now.toFormat('HH:mm:ss')}}
// Result: 14:30:45

// Full datetime
{{$now.toFormat('yyyy-MM-dd HH:mm')}}
// Result: 2025-10-20 14:30
```

---

## Data Type Handling

### Arrays

```javascript
// First item
{{$json.users[0].email}}

// Array length
{{$json.users.length}}

// Last item
{{$json.users[$json.users.length - 1].name}}
```

### Objects

```javascript
// Dot notation (no spaces)
{{$json.user.email}}

// Bracket notation (with spaces or dynamic)
{{$json['user data'].email}}
```

### Strings

```javascript
// Concatenation (automatic)
Hello {{$json.name}}!

// String methods
{{$json.email.toLowerCase()}}
{{$json.name.toUpperCase()}}
```

### Numbers

```javascript
// Direct use
{{$json.price}}

// Math operations
{{$json.price * 1.1}}  // Add 10%
{{$json.quantity + 5}}
```

---

## Advanced Patterns

### Conditional Content

```javascript
// Ternary operator
{{$json.status === 'active' ? 'Active User' : 'Inactive User'}}

// Default values
{{$json.email || 'no-email@example.com'}}
```

### Date Manipulation

```javascript
// Add days
{{$now.plus({days: 7}).toFormat('yyyy-MM-dd')}}

// Subtract hours
{{$now.minus({hours: 24}).toISO()}}

// Set specific date
{{DateTime.fromISO('2025-12-25').toFormat('MMMM dd, yyyy')}}
```

### String Manipulation

```javascript
// Substring
{{$json.email.substring(0, 5)}}

// Replace
{{$json.message.replace('old', 'new')}}

// Split and join
{{$json.tags.split(',').join(', ')}}
```

---

## Debugging Expressions

### Test in Expression Editor

1. Click field with expression
2. Open expression editor (click "fx" icon)
3. See live preview of result
4. Check for errors highlighted in red

### Common Error Messages

**"Cannot read property 'X' of undefined"**
→ Parent object doesn't exist
→ Check your data path

**"X is not a function"**
→ Trying to call method on non-function
→ Check variable type

**Expression shows as literal text**
→ Missing {{ }}
→ Add curly braces

---

## Expression Helpers

### Available Methods

**String**:
- `.toLowerCase()`, `.toUpperCase()`
- `.trim()`, `.replace()`, `.substring()`
- `.split()`, `.includes()`

**Array**:
- `.length`, `.map()`, `.filter()`
- `.find()`, `.join()`, `.slice()`

**DateTime** (Luxon):
- `.toFormat()`, `.toISO()`, `.toLocal()`
- `.plus()`, `.minus()`, `.set()`

**Number**:
- `.toFixed()`, `.toString()`
- Math operations: `+`, `-`, `*`, `/`, `%`

---

## Best Practices

### ✅ Do

- Always use {{ }} for dynamic content
- Use bracket notation for field names with spaces
- Reference webhook data from `.body`
- Use $node for data from other nodes
- Test expressions in expression editor

### ❌ Don't

- Don't use expressions in Code nodes
- Don't forget quotes around node names with spaces
- Don't double-wrap with extra {{ }}
- Don't assume webhook data is at root (it's under .body!)
- Don't use expressions in webhook paths or credentials

---

## Related Skills

- **n8n MCP Tools Expert**: Learn how to validate expressions using MCP tools
- **n8n Workflow Patterns**: See expressions in real workflow examples
- **n8n Node Configuration**: Understand when expressions are needed

---

## Summary

**Essential Rules**:
1. Wrap expressions in {{ }}
2. Webhook data is under `.body`
3. No {{ }} in Code nodes
4. Quote node names with spaces
5. Node names are case-sensitive

**Most Common Mistakes**:
- Missing {{ }} → Add braces
- `{{$json.name}}` in webhooks → Use `{{$json.body.name}}`
- `{{$json.email}}` in Code → Use `$json.email`
- `{{$node.HTTP Request}}` → Use `{{$node["HTTP Request"]}}`

For more details, see:
- COMMON_MISTAKES.md - Complete error catalog
- EXAMPLES.md - Real workflow examples

---

**Need Help?** Reference the n8n expression documentation or use n8n-mcp validation tools to check your expressions.


---

# Common n8n Expression Mistakes

Complete catalog of expression errors with explanations and fixes.

---

## 1. Missing Curly Braces

**Problem**: Expression not recognized, shows as literal text

❌ **Wrong**:
```
$json.email
```

✅ **Correct**:
```
{{$json.email}}
```

**Why it fails**: n8n treats text without {{ }} as a literal string. Expressions must be wrapped to be evaluated.

**How to identify**: Field shows exact text like "$json.email" instead of actual value.

---

## 2. Webhook Body Access

**Problem**: Undefined values when accessing webhook data

❌ **Wrong**:
```
{{$json.name}}
{{$json.email}}
{{$json.message}}
```

✅ **Correct**:
```
{{$json.body.name}}
{{$json.body.email}}
{{$json.body.message}}
```

**Why it fails**: Webhook node wraps incoming data under `.body` property. The root `$json` contains headers, params, query, and body.

**Webhook structure**:
```javascript
{
  "headers": {...},
  "params": {...},
  "query": {...},
  "body": {         // User data is HERE!
    "name": "John",
    "email": "john@example.com"
  }
}
```

**How to identify**: Webhook workflow shows "undefined" for fields that are definitely being sent.

---

## 3. Spaces in Field Names

**Problem**: Syntax error or undefined value

❌ **Wrong**:
```
{{$json.first name}}
{{$json.user data.email}}
```

✅ **Correct**:
```
{{$json['first name']}}
{{$json['user data'].email}}
```

**Why it fails**: Spaces break dot notation. JavaScript interprets space as end of property name.

**How to identify**: Error message about unexpected token, or undefined when field exists.

---

## 4. Spaces in Node Names

**Problem**: Cannot access other node's data

❌ **Wrong**:
```
{{$node.HTTP Request.json.data}}
{{$node.Respond to Webhook.json}}
```

✅ **Correct**:
```
{{$node["HTTP Request"].json.data}}
{{$node["Respond to Webhook"].json}}
```

**Why it fails**: Node names are treated as object property names and need quotes when they contain spaces.

**How to identify**: Error like "Cannot read property 'Request' of undefined"

---

## 5. Incorrect Node Reference Case

**Problem**: Undefined or wrong data returned

❌ **Wrong**:
```
{{$node["http request"].json.data}}  // lowercase
{{$node["Http Request"].json.data}}  // wrong capitalization
```

✅ **Correct**:
```
{{$node["HTTP Request"].json.data}}  // exact match
```

**Why it fails**: Node names are **case-sensitive**. Must match exactly as shown in workflow.

**How to identify**: Undefined value even though node exists and has data.

---

## 6. Double Wrapping

**Problem**: Literal {{ }} appears in output

❌ **Wrong**:
```
{{{$json.field}}}
```

✅ **Correct**:
```
{{$json.field}}
```

**Why it fails**: Only one set of {{ }} is needed. Extra braces are treated as literal characters.

**How to identify**: Output shows "{{value}}" instead of just "value".

---

## 7. Array Access with Dots

**Problem**: Syntax error or undefined

❌ **Wrong**:
```
{{$json.items.0.name}}
{{$json.users.1.email}}
```

✅ **Correct**:
```
{{$json.items[0].name}}
{{$json.users[1].email}}
```

**Why it fails**: Array indices require brackets, not dots. Number after dot is invalid JavaScript.

**How to identify**: Syntax error or "Cannot read property '0' of undefined"

---

## 8. Using Expressions in Code Nodes

**Problem**: Literal string instead of value, or errors

❌ **Wrong (in Code node)**:
```javascript
const email = '{{$json.email}}';
const name = '={{$json.body.name}}';
```

✅ **Correct (in Code node)**:
```javascript
const email = $json.email;
const name = $json.body.name;

// Or using Code node API
const email = $input.item.json.email;
const allItems = $input.all();
```

**Why it fails**: Code nodes have **direct access** to data. The {{ }} syntax is for expression fields in other nodes, not for JavaScript code.

**How to identify**: Literal string "{{$json.email}}" appears in Code node output instead of actual value.

---

## 9. Missing Quotes in $node Reference

**Problem**: Syntax error

❌ **Wrong**:
```
{{$node[HTTP Request].json.data}}
```

✅ **Correct**:
```
{{$node["HTTP Request"].json.data}}
```

**Why it fails**: Node names must be quoted strings inside brackets.

**How to identify**: Syntax error "Unexpected identifier"

---

## 10. Incorrect Property Path

**Problem**: Undefined value

❌ **Wrong**:
```
{{$json.data.items.name}}       // items is an array
{{$json.user.email}}            // user doesn't exist, it's userData
```

✅ **Correct**:
```
{{$json.data.items[0].name}}    // access array element
{{$json.userData.email}}        // correct property name
```

**Why it fails**: Wrong path to data. Arrays need index, property names must be exact.

**How to identify**: Check actual data structure using expression editor preview.

---

## 11. Using = Prefix Outside JSON

**Problem**: Literal "=" appears in output

❌ **Wrong (in text field)**:
```
Email: ={{$json.email}}
```

✅ **Correct (in text field)**:
```
Email: {{$json.email}}
```

**Note**: The `=` prefix is **only** needed in JSON mode or when you want to set entire field value to expression result:

```javascript
// JSON mode (set property to expression)
{
  "email": "={{$json.body.email}}"
}

// Text mode (no = needed)
Hello {{$json.body.name}}!
```

**Why it fails**: The `=` is parsed as literal text in non-JSON contexts.

**How to identify**: Output shows "=john@example.com" instead of "john@example.com"

---

## 12. Expressions in Webhook Path

**Problem**: Path doesn't update, validation error

❌ **Wrong**:
```
path: "{{$json.user_id}}/webhook"
path: "users/={{$env.TENANT_ID}}"
```

✅ **Correct**:
```
path: "my-webhook"              // Static paths only
path: "user-webhook/:userId"    // Use dynamic URL parameters instead
```

**Why it fails**: Webhook paths must be static. Use dynamic URL parameters (`:paramName`) instead of expressions.

**How to identify**: Webhook path doesn't change or validation warns about invalid path.

---

## 13. Forgetting .json in $node Reference

**Problem**: Undefined or wrong data

❌ **Wrong**:
```
{{$node["HTTP Request"].data}}          // Missing .json
{{$node["Webhook"].body.email}}         // Missing .json
```

✅ **Correct**:
```
{{$node["HTTP Request"].json.data}}
{{$node["Webhook"].json.body.email}}
```

**Why it fails**: Node data is always under `.json` property (or `.binary` for binary data).

**How to identify**: Undefined value when you know the node has data.

---

## 14. String Concatenation Confusion

**Problem**: Attempting JavaScript template literals

❌ **Wrong**:
```
`Hello ${$json.name}!`          // Template literal syntax
"Hello " + $json.name + "!"     // String concatenation
```

✅ **Correct**:
```
Hello {{$json.name}}!           // n8n expressions auto-concatenate
```

**Why it fails**: n8n expressions don't use JavaScript template literal syntax. Adjacent text and expressions are automatically concatenated.

**How to identify**: Literal backticks or + symbols appear in output.

---

## 15. Empty Expression Brackets

**Problem**: Literal {{}} in output

❌ **Wrong**:
```
{{}}
{{ }}
```

✅ **Correct**:
```
{{$json.field}}                 // Include expression content
```

**Why it fails**: Empty expression brackets have nothing to evaluate.

**How to identify**: Literal "{{ }}" text appears in output.

---

## Quick Reference Table

| Error | Symptom | Fix |
|-------|---------|-----|
| No {{ }} | Literal text | Add {{ }} |
| Webhook data | Undefined | Add `.body` |
| Space in field | Syntax error | Use `['field name']` |
| Space in node | Undefined | Use `["Node Name"]` |
| Wrong case | Undefined | Match exact case |
| Double {{ }} | Literal braces | Remove extra {{ }} |
| .0 array | Syntax error | Use [0] |
| {{ }} in Code | Literal string | Remove {{ }} |
| No quotes in $node | Syntax error | Add quotes |
| Wrong path | Undefined | Check data structure |
| = in text | Literal = | Remove = prefix |
| Dynamic path | Doesn't work | Use static path |
| Missing .json | Undefined | Add .json |
| Template literals | Literal text | Use {{ }} |
| Empty {{ }} | Literal braces | Add expression |

---

## Debugging Process

When expression doesn't work:

1. **Check braces**: Is it wrapped in {{ }}?
2. **Check data source**: Is it webhook data? Add `.body`
3. **Check spaces**: Field or node name has spaces? Use brackets
4. **Check case**: Does node name match exactly?
5. **Check path**: Is the property path correct?
6. **Use expression editor**: Preview shows actual result
7. **Check context**: Is it a Code node? Remove {{ }}

---

**Related**: See EXAMPLES.md for working examples of correct syntax.


---

# n8n Expression Examples

Real working examples from n8n workflows.

---

## Example 1: Webhook Form Submission

**Scenario**: Form submission webhook posts to Slack

**Workflow**: Webhook → Slack

**Webhook Input** (POST):
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "company": "Acme Corp",
  "message": "Interested in your product"
}
```

**Webhook Node Output**:
```json
{
  "headers": {"content-type": "application/json"},
  "params": {},
  "query": {},
  "body": {
    "name": "John Doe",
    "email": "john@example.com",
    "company": "Acme Corp",
    "message": "Interested in your product"
  }
}
```

**In Slack Node** (text field):
```
New form submission! 📝

Name: {{$json.body.name}}
Email: {{$json.body.email}}
Company: {{$json.body.company}}
Message: {{$json.body.message}}
```

**Output**:
```
New form submission! 📝

Name: John Doe
Email: john@example.com
Company: Acme Corp
Message: Interested in your product
```

---

## Example 2: HTTP API to Database

**Scenario**: Fetch user data from API and insert into database

**Workflow**: Schedule → HTTP Request → Postgres

**HTTP Request Returns**:
```json
{
  "data": {
    "users": [
      {
        "id": 123,
        "name": "Alice Smith",
        "email": "alice@example.com",
        "role": "admin"
      }
    ]
  }
}
```

**In Postgres Node** (INSERT statement):
```sql
INSERT INTO users (user_id, name, email, role, synced_at)
VALUES (
  {{$json.data.users[0].id}},
  '{{$json.data.users[0].name}}',
  '{{$json.data.users[0].email}}',
  '{{$json.data.users[0].role}}',
  '{{$now.toFormat('yyyy-MM-dd HH:mm:ss')}}'
)
```

**Result**: User inserted with current timestamp

---

## Example 3: Multi-Node Data Flow

**Scenario**: Webhook → HTTP Request → Email

**Workflow Structure**:
1. Webhook receives order ID
2. HTTP Request fetches order details
3. Email sends confirmation

### Node 1: Webhook

**Receives**:
```json
{
  "body": {
    "order_id": "ORD-12345"
  }
}
```

### Node 2: HTTP Request

**URL field**:
```
https://api.example.com/orders/{{$json.body.order_id}}
```

**Returns**:
```json
{
  "order": {
    "id": "ORD-12345",
    "customer": "Bob Jones",
    "total": 99.99,
    "items": ["Widget", "Gadget"]
  }
}
```

### Node 3: Email

**Subject**:
```
Order {{$node["Webhook"].json.body.order_id}} Confirmed
```

**Body**:
```
Dear {{$node["HTTP Request"].json.order.customer}},

Your order {{$node["Webhook"].json.body.order_id}} has been confirmed!

Total: ${{$node["HTTP Request"].json.order.total}}
Items: {{$node["HTTP Request"].json.order.items.join(', ')}}

Thank you for your purchase!
```

**Email Result**:
```
Subject: Order ORD-12345 Confirmed

Dear Bob Jones,

Your order ORD-12345 has been confirmed!

Total: $99.99
Items: Widget, Gadget

Thank you for your purchase!
```

---

## Example 4: Date Formatting

**Scenario**: Various date format outputs

**Current Time**: 2025-10-20 14:30:45

### ISO Format
```javascript
{{$now.toISO()}}
```
**Output**: `2025-10-20T14:30:45.000Z`

### Custom Date Format
```javascript
{{$now.toFormat('yyyy-MM-dd')}}
```
**Output**: `2025-10-20`

### Time Only
```javascript
{{$now.toFormat('HH:mm:ss')}}
```
**Output**: `14:30:45`

### Full Readable Format
```javascript
{{$now.toFormat('MMMM dd, yyyy')}}
```
**Output**: `October 20, 2025`

### Date Math - Future
```javascript
{{$now.plus({days: 7}).toFormat('yyyy-MM-dd')}}
```
**Output**: `2025-10-27`

### Date Math - Past
```javascript
{{$now.minus({hours: 24}).toFormat('yyyy-MM-dd HH:mm')}}
```
**Output**: `2025-10-19 14:30`

---

## Example 5: Array Operations

**Data**:
```json
{
  "users": [
    {"name": "Alice", "email": "alice@example.com"},
    {"name": "Bob", "email": "bob@example.com"},
    {"name": "Charlie", "email": "charlie@example.com"}
  ]
}
```

### First User
```javascript
{{$json.users[0].name}}
```
**Output**: `Alice`

### Last User
```javascript
{{$json.users[$json.users.length - 1].name}}
```
**Output**: `Charlie`

### All Emails (Join)
```javascript
{{$json.users.map(u => u.email).join(', ')}}
```
**Output**: `alice@example.com, bob@example.com, charlie@example.com`

### Array Length
```javascript
{{$json.users.length}}
```
**Output**: `3`

---

## Example 6: Conditional Logic

**Data**:
```json
{
  "order": {
    "status": "completed",
    "total": 150
  }
}
```

### Ternary Operator
```javascript
{{$json.order.status === 'completed' ? 'Order Complete ✓' : 'Pending...'}}
```
**Output**: `Order Complete ✓`

### Default Values
```javascript
{{$json.order.notes || 'No notes provided'}}
```
**Output**: `No notes provided` (if notes field doesn't exist)

### Multiple Conditions
```javascript
{{$json.order.total > 100 ? 'Premium Customer' : 'Standard Customer'}}
```
**Output**: `Premium Customer`

---

## Example 7: String Manipulation

**Data**:
```json
{
  "user": {
    "email": "JOHN@EXAMPLE.COM",
    "message": "  Hello World  "
  }
}
```

### Lowercase
```javascript
{{$json.user.email.toLowerCase()}}
```
**Output**: `john@example.com`

### Uppercase
```javascript
{{$json.user.message.toUpperCase()}}
```
**Output**: `  HELLO WORLD  `

### Trim
```javascript
{{$json.user.message.trim()}}
```
**Output**: `Hello World`

### Substring
```javascript
{{$json.user.email.substring(0, 4)}}
```
**Output**: `JOHN`

### Replace
```javascript
{{$json.user.message.replace('World', 'n8n')}}
```
**Output**: `  Hello n8n  `

---

## Example 8: Fields with Spaces

**Data**:
```json
{
  "user data": {
    "first name": "Jane",
    "last name": "Doe",
    "phone number": "+1234567890"
  }
}
```

### Bracket Notation
```javascript
{{$json['user data']['first name']}}
```
**Output**: `Jane`

### Combined
```javascript
{{$json['user data']['first name']}} {{$json['user data']['last name']}}
```
**Output**: `Jane Doe`

### Nested Spaces
```javascript
Contact: {{$json['user data']['phone number']}}
```
**Output**: `Contact: +1234567890`

---

## Example 9: Code Node (Direct Access)

**Code Node**: Transform webhook data

**Input** (from Webhook node):
```json
{
  "body": {
    "items": ["apple", "banana", "cherry"]
  }
}
```

**Code** (JavaScript):
```javascript
// ✅ Direct access (no {{ }})
const items = $json.body.items;

// Transform to uppercase
const uppercased = items.map(item => item.toUpperCase());

// Return in n8n format
return [{
  json: {
    original: items,
    transformed: uppercased,
    count: items.length
  }
}];
```

**Output**:
```json
{
  "original": ["apple", "banana", "cherry"],
  "transformed": ["APPLE", "BANANA", "CHERRY"],
  "count": 3
}
```

---

## Example 10: Environment Variables

**Setup**: Environment variable `API_KEY=secret123`

### In HTTP Request (Headers)
```javascript
Authorization: Bearer {{$env.API_KEY}}
```
**Result**: `Authorization: Bearer secret123`

### In URL
```javascript
https://api.example.com/data?key={{$env.API_KEY}}
```
**Result**: `https://api.example.com/data?key=secret123`

---

## Template from Real Workflow

**Based on n8n template #2947** (Weather to Slack)

### Workflow Structure
Webhook → OpenStreetMap API → Weather API → Slack

### Webhook Slash Command
**Input**: `/weather London`

**Webhook receives**:
```json
{
  "body": {
    "text": "London"
  }
}
```

### OpenStreetMap API
**URL**:
```
https://nominatim.openstreetmap.org/search?q={{$json.body.text}}&format=json
```

### Weather API (NWS)
**URL**:
```
https://api.weather.gov/points/{{$node["OpenStreetMap"].json[0].lat}},{{$node["OpenStreetMap"].json[0].lon}}
```

### Slack Message
```
Weather for {{$json.body.text}}:

Temperature: {{$node["Weather API"].json.properties.temperature.value}}°C
Conditions: {{$node["Weather API"].json.properties.shortForecast}}
```

---

## Summary

**Key Patterns**:
1. Webhook data is under `.body`
2. Use `{{}}` for expressions (except Code nodes)
3. Reference other nodes with `$node["Node Name"].json`
4. Use brackets for field names with spaces
5. Node names are case-sensitive

**Most Common Uses**:
- `{{$json.body.field}}` - Webhook data
- `{{$node["Name"].json.field}}` - Other node data
- `{{$now.toFormat('yyyy-MM-dd')}}` - Timestamps
- `{{$json.array[0].field}}` - Array access
- `{{$json.field || 'default'}}` - Default values

---

**Related**: See COMMON_MISTAKES.md for error examples and fixes.
