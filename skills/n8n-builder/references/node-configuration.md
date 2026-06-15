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

# Property Dependencies Guide

Deep dive into n8n property dependencies and displayOptions mechanism.

---

## What Are Property Dependencies?

**Definition**: Rules that control when fields are visible or required based on other field values.

**Mechanism**: `displayOptions` in node schema

**Purpose**:
- Show relevant fields only
- Hide irrelevant fields
- Simplify configuration UX
- Prevent invalid configurations

---

## displayOptions Structure

### Basic Format

```javascript
{
  "name": "fieldName",
  "type": "string",
  "displayOptions": {
    "show": {
      "otherField": ["value1", "value2"]
    }
  }
}
```

**Translation**: Show `fieldName` when `otherField` equals "value1" OR "value2"

### Show vs Hide

#### show (Most Common)

**Show field when condition matches**:
```javascript
{
  "name": "body",
  "displayOptions": {
    "show": {
      "sendBody": [true]
    }
  }
}
```

**Meaning**: Show `body` when `sendBody = true`

#### hide (Less Common)

**Hide field when condition matches**:
```javascript
{
  "name": "advanced",
  "displayOptions": {
    "hide": {
      "simpleMode": [true]
    }
  }
}
```

**Meaning**: Hide `advanced` when `simpleMode = true`

### Multiple Conditions (AND Logic)

```javascript
{
  "name": "body",
  "displayOptions": {
    "show": {
      "sendBody": [true],
      "method": ["POST", "PUT", "PATCH"]
    }
  }
}
```

**Meaning**: Show `body` when:
- `sendBody = true` AND
- `method IN (POST, PUT, PATCH)`

**All conditions must match** (AND logic)

### Multiple Values (OR Logic)

```javascript
{
  "name": "someField",
  "displayOptions": {
    "show": {
      "method": ["POST", "PUT", "PATCH"]
    }
  }
}
```

**Meaning**: Show `someField` when:
- `method = POST` OR
- `method = PUT` OR
- `method = PATCH`

**Any value matches** (OR logic)

---

## Common Dependency Patterns

### Pattern 1: Boolean Toggle

**Use case**: Optional feature flag

**Example**: HTTP Request sendBody
```javascript
// Field: sendBody (boolean)
{
  "name": "sendBody",
  "type": "boolean",
  "default": false
}

// Field: body (depends on sendBody)
{
  "name": "body",
  "displayOptions": {
    "show": {
      "sendBody": [true]
    }
  }
}
```

**Flow**:
1. User sees sendBody checkbox
2. When checked → body field appears
3. When unchecked → body field hides

### Pattern 2: Resource/Operation Cascade

**Use case**: Different operations show different fields

**Example**: Slack message operations
```javascript
// Operation: post
{
  "name": "channel",
  "displayOptions": {
    "show": {
      "resource": ["message"],
      "operation": ["post"]
    }
  }
}

// Operation: update
{
  "name": "messageId",
  "displayOptions": {
    "show": {
      "resource": ["message"],
      "operation": ["update"]
    }
  }
}
```

**Flow**:
1. User selects resource="message"
2. User selects operation="post" → sees channel
3. User changes to operation="update" → channel hides, messageId shows

### Pattern 3: Type-Specific Configuration

**Use case**: Different types need different fields

**Example**: IF node conditions
```javascript
// String operations
{
  "name": "value2",
  "displayOptions": {
    "show": {
      "conditions.string.0.operation": ["equals", "notEquals", "contains"]
    }
  }
}

// Unary operations (isEmpty) don't show value2
{
  "displayOptions": {
    "hide": {
      "conditions.string.0.operation": ["isEmpty", "isNotEmpty"]
    }
  }
}
```

### Pattern 4: Method-Specific Fields

**Use case**: HTTP methods have different options

**Example**: HTTP Request
```javascript
// Query parameters (all methods can have)
{
  "name": "queryParameters",
  "displayOptions": {
    "show": {
      "sendQuery": [true]
    }
  }
}

// Body (only certain methods)
{
  "name": "body",
  "displayOptions": {
    "show": {
      "sendBody": [true],
      "method": ["POST", "PUT", "PATCH", "DELETE"]
    }
  }
}
```

---

## Finding Property Dependencies

### Using get_node with search_properties Mode

```javascript
// Find properties related to "body"
get_node({
  nodeType: "nodes-base.httpRequest",
  mode: "search_properties",
  propertyQuery: "body"
});
```

### Using get_node with Full Detail

```javascript
// Get complete schema with displayOptions
get_node({
  nodeType: "nodes-base.httpRequest",
  detail: "full"
});
```

### When to Use

**✅ Use when**:
- Validation fails with "missing field" but you don't see that field
- A field appears/disappears unexpectedly
- You need to understand what controls field visibility
- Building dynamic configuration tools

**❌ Don't use when**:
- Simple configuration (use `get_node` with standard detail)
- Just starting configuration
- Field requirements are obvious

---

## Complex Dependency Examples

### Example 1: HTTP Request Complete Flow

**Scenario**: Configuring POST with JSON body

**Step 1**: Set method
```javascript
{
  "method": "POST"
  // → sendBody becomes visible
}
```

**Step 2**: Enable body
```javascript
{
  "method": "POST",
  "sendBody": true
  // → body field becomes visible AND required
}
```

**Step 3**: Configure body
```javascript
{
  "method": "POST",
  "sendBody": true,
  "body": {
    "contentType": "json"
    // → content field becomes visible AND required
  }
}
```

**Step 4**: Add content
```javascript
{
  "method": "POST",
  "sendBody": true,
  "body": {
    "contentType": "json",
    "content": {
      "name": "John",
      "email": "john@example.com"
    }
  }
}
// ✅ Valid!
```

**Dependency chain**:
```
method=POST
  → sendBody visible
    → sendBody=true
      → body visible + required
        → body.contentType=json
          → body.content visible + required
```

### Example 2: IF Node Operator Dependencies

**Scenario**: String comparison with different operators

**Binary operator** (equals):
```javascript
{
  "conditions": {
    "string": [
      {
        "operation": "equals"
        // → value1 required
        // → value2 required
        // → singleValue should NOT be set
      }
    ]
  }
}
```

**Unary operator** (isEmpty):
```javascript
{
  "conditions": {
    "string": [
      {
        "operation": "isEmpty"
        // → value1 required
        // → value2 should NOT be set
        // → singleValue should be true (auto-added)
      }
    ]
  }
}
```

**Dependency table**:

| Operator | value1 | value2 | singleValue |
|---|---|---|---|
| equals | Required | Required | false |
| notEquals | Required | Required | false |
| contains | Required | Required | false |
| isEmpty | Required | Hidden | true |
| isNotEmpty | Required | Hidden | true |

### Example 3: Slack Operation Matrix

**Scenario**: Different Slack operations show different fields

```javascript
// post message
{
  "resource": "message",
  "operation": "post"
  // Shows: channel (required), text (required), attachments, blocks
}

// update message
{
  "resource": "message",
  "operation": "update"
  // Shows: messageId (required), text (required), channel (optional)
}

// delete message
{
  "resource": "message",
  "operation": "delete"
  // Shows: messageId (required), channel (required)
  // Hides: text, attachments, blocks
}

// get message
{
  "resource": "message",
  "operation": "get"
  // Shows: messageId (required), channel (required)
  // Hides: text, attachments, blocks
}
```

**Field visibility matrix**:

| Field | post | update | delete | get |
|---|---|---|---|---|
| channel | Required | Optional | Required | Required |
| text | Required | Required | Hidden | Hidden |
| messageId | Hidden | Required | Required | Required |
| attachments | Optional | Optional | Hidden | Hidden |
| blocks | Optional | Optional | Hidden | Hidden |

---

## Nested Dependencies

### What Are They?

**Definition**: Dependencies within object properties

**Example**: HTTP Request body.contentType controls body.content structure

```javascript
{
  "body": {
    "contentType": "json",
    // → content expects JSON object
    "content": {
      "key": "value"
    }
  }
}

{
  "body": {
    "contentType": "form-data",
    // → content expects form fields array
    "content": [
      {
        "name": "field1",
        "value": "value1"
      }
    ]
  }
}
```

### How to Handle

**Strategy**: Configure parent first, then children

```javascript
// Step 1: Parent
{
  "body": {
    "contentType": "json"  // Set parent first
  }
}

// Step 2: Children (structure determined by parent)
{
  "body": {
    "contentType": "json",
    "content": {           // JSON object format
      "key": "value"
    }
  }
}
```

---

## Auto-Sanitization and Dependencies

### What Auto-Sanitization Fixes

**Operator structure issues** (IF/Switch nodes):

**Example**: singleValue property
```javascript
// You configure (missing singleValue)
{
  "type": "boolean",
  "operation": "isEmpty"
  // Missing singleValue
}

// Auto-sanitization adds it
{
  "type": "boolean",
  "operation": "isEmpty",
  "singleValue": true  // ✅ Added automatically
}
```

### What It Doesn't Fix

**Missing required fields**:
```javascript
// You configure (missing channel)
{
  "resource": "message",
  "operation": "post",
  "text": "Hello"
  // Missing required field: channel
}

// Auto-sanitization does NOT add
// You must add it yourself
{
  "resource": "message",
  "operation": "post",
  "channel": "#general",  // ← You must add
  "text": "Hello"
}
```

---

## Troubleshooting Dependencies

### Problem 1: "Field X is required but not visible"

**Error**:
```json
{
  "type": "missing_required",
  "property": "body",
  "message": "body is required"
}
```

**But you don't see body field in configuration!**

**Solution**:
```javascript
// Check field dependencies using search_properties
get_node({
  nodeType: "nodes-base.httpRequest",
  mode: "search_properties",
  propertyQuery: "body"
});

// Find that body shows when sendBody=true
// Add sendBody
{
  "method": "POST",
  "sendBody": true,  // ← Now body appears!
  "body": {...}
}
```

### Problem 2: "Field disappears when I change operation"

**Scenario**:
```javascript
// Working configuration
{
  "resource": "message",
  "operation": "post",
  "channel": "#general",
  "text": "Hello"
}

// Change operation
{
  "resource": "message",
  "operation": "update",  // Changed
  "channel": "#general",  // Still here
  "text": "Updated"       // Still here
  // Missing: messageId (required for update!)
}
```

**Validation error**: "messageId is required"

**Why**: Different operation = different required fields

**Solution**:
```javascript
// Check requirements for new operation
get_node({
  nodeType: "nodes-base.slack"
});

// Configure for update operation
{
  "resource": "message",
  "operation": "update",
  "messageId": "1234567890",  // Required for update
  "text": "Updated",
  "channel": "#general"       // Optional for update
}
```

### Problem 3: "Validation passes but field doesn't save"

**Scenario**: Field hidden by dependencies after validation

**Example**:
```javascript
// Configure
{
  "method": "GET",
  "sendBody": true,  // ❌ GET doesn't support body
  "body": {...}      // This will be stripped
}

// After save
{
  "method": "GET"
  // body removed because method=GET hides it
}
```

**Solution**: Respect dependencies from the start

```javascript
// Correct approach - check property dependencies
get_node({
  nodeType: "nodes-base.httpRequest",
  mode: "search_properties",
  propertyQuery: "body"
});

// See that body only shows for POST/PUT/PATCH/DELETE
// Use correct method
{
  "method": "POST",
  "sendBody": true,
  "body": {...}
}
```

---

## Advanced Patterns

### Pattern 1: Conditional Required with Fallback

**Example**: Channel can be string OR expression

```javascript
// Option 1: String
{
  "channel": "#general"
}

// Option 2: Expression
{
  "channel": "={{$json.channelName}}"
}

// Validation accepts both
```

### Pattern 2: Mutually Exclusive Fields

**Example**: Use either ID or name, not both

```javascript
// Use messageId
{
  "messageId": "1234567890"
  // name not needed
}

// OR use messageName
{
  "messageName": "thread-name"
  // messageId not needed
}

// Dependencies ensure only one is required
```

### Pattern 3: Progressive Complexity

**Example**: Simple mode vs advanced mode

```javascript
// Simple mode
{
  "mode": "simple",
  "text": "{{$json.message}}"
  // Advanced fields hidden
}

// Advanced mode
{
  "mode": "advanced",
  "attachments": [...],
  "blocks": [...],
  "metadata": {...}
  // Simple field hidden, advanced fields shown
}
```

---

## Best Practices

### ✅ Do

1. **Check dependencies when stuck**
   ```javascript
   get_node({nodeType: "...", mode: "search_properties", propertyQuery: "..."});
   ```

2. **Configure parent properties first**
   ```javascript
   // First: method, resource, operation
   // Then: dependent fields
   ```

3. **Validate after changing operation**
   ```javascript
   // Operation changed → requirements changed
   validate_node({nodeType: "...", config: {...}, profile: "runtime"});
   ```

4. **Read validation errors for dependency hints**
   ```
   Error: "body required when sendBody=true"
   → Hint: Set sendBody=true to enable body
   ```

### ❌ Don't

1. **Don't ignore dependency errors**
   ```javascript
   // Error: "body not visible" → Check displayOptions
   ```

2. **Don't hardcode all possible fields**
   ```javascript
   // Bad: Adding fields that will be hidden
   ```

3. **Don't assume operations are identical**
   ```javascript
   // Each operation has unique requirements
   ```

---

## Summary

**Key Concepts**:
- `displayOptions` control field visibility
- `show` = field appears when conditions match
- `hide` = field disappears when conditions match
- Multiple conditions = AND logic
- Multiple values = OR logic

**Common Patterns**:
1. Boolean toggle (sendBody → body)
2. Resource/operation cascade (different operations → different fields)
3. Type-specific config (string vs boolean conditions)
4. Method-specific fields (GET vs POST)

**Troubleshooting**:
- Field required but not visible → Check dependencies
- Field disappears after change → Operation changed requirements
- Field doesn't save → Hidden by dependencies

**Tools**:
- `get_node({mode: "search_properties"})` - Find property dependencies
- `get_node({detail: "full"})` - See complete schema with displayOptions
- `get_node` - See operation requirements (standard detail)
- Validation errors - Hints about dependencies

**Related Files**:
- **SKILL.md** - Main configuration guide
- **OPERATION_PATTERNS.md** - Common patterns by node type


---

# Operation Patterns Guide

Common node configuration patterns organized by node type and operation.

---

## Overview

**Purpose**: Quick reference for common node configurations

**Coverage**: Top 20 most-used nodes from 525 available

**Pattern format**:
- Minimal valid configuration
- Common options
- Real-world examples
- Gotchas and tips

---

## HTTP & API Nodes

### HTTP Request (nodes-base.httpRequest)

Most versatile node for HTTP operations

#### GET Request

**Minimal**:
```javascript
{
  "method": "GET",
  "url": "https://api.example.com/users",
  "authentication": "none"
}
```

**With query parameters**:
```javascript
{
  "method": "GET",
  "url": "https://api.example.com/users",
  "authentication": "none",
  "sendQuery": true,
  "queryParameters": {
    "parameters": [
      {
        "name": "limit",
        "value": "100"
      },
      {
        "name": "offset",
        "value": "={{$json.offset}}"
      }
    ]
  }
}
```

**With authentication**:
```javascript
{
  "method": "GET",
  "url": "https://api.example.com/users",
  "authentication": "predefinedCredentialType",
  "nodeCredentialType": "httpHeaderAuth"
}
```

#### POST with JSON

**Minimal**:
```javascript
{
  "method": "POST",
  "url": "https://api.example.com/users",
  "authentication": "none",
  "sendBody": true,
  "body": {
    "contentType": "json",
    "content": {
      "name": "John Doe",
      "email": "john@example.com"
    }
  }
}
```

**With expressions**:
```javascript
{
  "method": "POST",
  "url": "https://api.example.com/users",
  "authentication": "none",
  "sendBody": true,
  "body": {
    "contentType": "json",
    "content": {
      "name": "={{$json.name}}",
      "email": "={{$json.email}}",
      "metadata": {
        "source": "n8n",
        "timestamp": "={{$now.toISO()}}"
      }
    }
  }
}
```

**Gotcha**: Remember `sendBody: true` for POST/PUT/PATCH!

#### PUT/PATCH Request

**Pattern**: Same as POST, but method changes
```javascript
{
  "method": "PUT",  // or "PATCH"
  "url": "https://api.example.com/users/123",
  "authentication": "none",
  "sendBody": true,
  "body": {
    "contentType": "json",
    "content": {
      "name": "Updated Name"
    }
  }
}
```

#### DELETE Request

**Minimal** (no body):
```javascript
{
  "method": "DELETE",
  "url": "https://api.example.com/users/123",
  "authentication": "none"
}
```

**With body** (some APIs allow):
```javascript
{
  "method": "DELETE",
  "url": "https://api.example.com/users",
  "authentication": "none",
  "sendBody": true,
  "body": {
    "contentType": "json",
    "content": {
      "ids": ["123", "456"]
    }
  }
}
```

---

### Webhook (nodes-base.webhook)

Most common trigger - 813 searches!

#### Basic Webhook

**Minimal**:
```javascript
{
  "path": "my-webhook",
  "httpMethod": "POST",
  "responseMode": "onReceived"
}
```

**Gotcha**: Webhook data is under `$json.body`, not `$json`!

```javascript
// ❌ Wrong
{
  "text": "={{$json.email}}"
}

// ✅ Correct
{
  "text": "={{$json.body.email}}"
}
```

#### Webhook with Authentication

**Header auth**:
```javascript
{
  "path": "secure-webhook",
  "httpMethod": "POST",
  "responseMode": "onReceived",
  "authentication": "headerAuth",
  "options": {
    "responseCode": 200,
    "responseData": "{\n  \"success\": true\n}"
  }
}
```

#### Webhook Returning Data

**Custom response**:
```javascript
{
  "path": "my-webhook",
  "httpMethod": "POST",
  "responseMode": "lastNode",  // Return data from last node
  "options": {
    "responseCode": 201,
    "responseHeaders": {
      "entries": [
        {
          "name": "Content-Type",
          "value": "application/json"
        }
      ]
    }
  }
}
```

---

## Communication Nodes

### Slack (nodes-base.slack)

Popular choice for AI agent workflows

#### Post Message

**Minimal**:
```javascript
{
  "resource": "message",
  "operation": "post",
  "channel": "#general",
  "text": "Hello from n8n!"
}
```

**With dynamic content**:
```javascript
{
  "resource": "message",
  "operation": "post",
  "channel": "={{$json.channel}}",
  "text": "New user: {{$json.name}} ({{$json.email}})"
}
```

**With attachments**:
```javascript
{
  "resource": "message",
  "operation": "post",
  "channel": "#alerts",
  "text": "Error Alert",
  "attachments": [
    {
      "color": "#ff0000",
      "fields": [
        {
          "title": "Error Type",
          "value": "={{$json.errorType}}"
        },
        {
          "title": "Timestamp",
          "value": "={{$now.toLocaleString()}}"
        }
      ]
    }
  ]
}
```

**Gotcha**: Channel must start with `#` for public channels or be a channel ID!

#### Update Message

**Minimal**:
```javascript
{
  "resource": "message",
  "operation": "update",
  "messageId": "1234567890.123456",  // From previous message post
  "text": "Updated message content"
}
```

**Note**: `messageId` required, `channel` optional (can be inferred)

#### Create Channel

**Minimal**:
```javascript
{
  "resource": "channel",
  "operation": "create",
  "name": "new-project-channel",  // Lowercase, no spaces
  "isPrivate": false
}
```

**Gotcha**: Channel name must be lowercase, no spaces, 1-80 chars!

---

### Gmail (nodes-base.gmail)

Popular for email automation

#### Send Email

**Minimal**:
```javascript
{
  "resource": "message",
  "operation": "send",
  "to": "user@example.com",
  "subject": "Hello from n8n",
  "message": "This is the email body"
}
```

**With dynamic content**:
```javascript
{
  "resource": "message",
  "operation": "send",
  "to": "={{$json.email}}",
  "subject": "Order Confirmation #{{$json.orderId}}",
  "message": "Dear {{$json.name}},\n\nYour order has been confirmed.\n\nThank you!",
  "options": {
    "ccList": "admin@example.com",
    "replyTo": "support@example.com"
  }
}
```

#### Get Email

**Minimal**:
```javascript
{
  "resource": "message",
  "operation": "getAll",
  "returnAll": false,
  "limit": 10
}
```

**With filters**:
```javascript
{
  "resource": "message",
  "operation": "getAll",
  "returnAll": false,
  "limit": 50,
  "filters": {
    "q": "is:unread from:important@example.com",
    "labelIds": ["INBOX"]
  }
}
```

---

## Database Nodes

### Postgres (nodes-base.postgres)

Database operations - 456 templates

#### Execute Query

**Minimal** (SELECT):
```javascript
{
  "operation": "executeQuery",
  "query": "SELECT * FROM users WHERE active = true LIMIT 100"
}
```

**With parameters** (SQL injection prevention):
```javascript
{
  "operation": "executeQuery",
  "query": "SELECT * FROM users WHERE email = $1 AND active = $2",
  "additionalFields": {
    "mode": "list",
    "queryParameters": "user@example.com,true"
  }
}
```

**Gotcha**: ALWAYS use parameterized queries for user input!

```javascript
// ❌ BAD - SQL injection risk!
{
  "query": "SELECT * FROM users WHERE email = '{{$json.email}}'"
}

// ✅ GOOD - Parameterized
{
  "query": "SELECT * FROM users WHERE email = $1",
  "additionalFields": {
    "mode": "list",
    "queryParameters": "={{$json.email}}"
  }
}
```

#### Insert

**Minimal**:
```javascript
{
  "operation": "insert",
  "table": "users",
  "columns": "name,email,created_at",
  "additionalFields": {
    "mode": "list",
    "queryParameters": "John Doe,john@example.com,NOW()"
  }
}
```

**With expressions**:
```javascript
{
  "operation": "insert",
  "table": "users",
  "columns": "name,email,metadata",
  "additionalFields": {
    "mode": "list",
    "queryParameters": "={{$json.name}},={{$json.email}},{{JSON.stringify($json)}}"
  }
}
```

#### Update

**Minimal**:
```javascript
{
  "operation": "update",
  "table": "users",
  "updateKey": "id",
  "columns": "name,email",
  "additionalFields": {
    "mode": "list",
    "queryParameters": "={{$json.id}},Updated Name,newemail@example.com"
  }
}
```

---

## Storage Nodes

### Data Table (nodes-base.dataTable)

Persistent, structured per-project key-value storage — an in-n8n alternative to external SQL for small state like buffers, de-dup sets, counters, or lookup caches. **Do not confuse with the MCP tool `n8n_manage_datatable`** — that tool manages tables from outside n8n (create/list/delete tables and rows from Claude). The **`nodes-base.dataTable` node** below is what you drop *into a workflow* to read/write rows during execution.

> **Verified end-to-end against live n8n on 2026-04-08** with a 15-node assertion harness exercising every claim below: insert returning rows with system `id`, `like` operator, `returnAll`, `allConditions` AND-of-multiple-filters, `isTrue` unary boolean condition, `upsert` with `matchingColumns` (no duplicates), `defineBelow` resourceMapper writing values, `deleteRows` (the reserved-word workaround) returning affected rows, and `dataTableId` resourceLocator in `mode: "name"`. All 6 assertions passed.

**Node shape**:
- `type`: `n8n-nodes-base.dataTable`
- `typeVersion`: `1.1` (also `1`)
- `resource`: `"row"` or `"table"`
- Row `operation` values — note the reserved-word workaround on delete:
  - `"insert"` — Insert row
  - `"get"` — Get row(s)
  - `"update"` — Update row(s) matching conditions
  - `"upsert"` — Update if match, else insert
  - `"deleteRows"` — Delete row(s) matching conditions (**not `"delete"`** — `delete` is a JS reserved word, the node uses `deleteRows`)
  - `"rowExists"` — Pass through input if at least one match
  - `"rowNotExists"` — Pass through input if zero matches

**Table selection** — always a resourceLocator parameter named `dataTableId`:
```javascript
"dataTableId": {
  "__rl": true,
  "mode": "list",      // or "name" or "id"
  "value": "dt_xyz123" // or the name when mode=name
}
```

**Row mapping** (insert/update/upsert) — resourceMapper parameter named `columns`:
```javascript
"columns": {
  "mappingMode": "defineBelow",    // or "autoMapInputData"
  "value": {
    "user_email": "={{ $json.email }}",
    "score": "={{ $json.score }}",
    "active": true
  },
  "matchingColumns": [],           // filled for update/upsert match keys
  "schema": [],                    // n8n re-loads at runtime; safe to leave empty
  "attemptToConvertTypes": false,
  "convertFieldsToString": false
}
```
In `autoMapInputData` mode, incoming item field names must match column names exactly and `value` is ignored.

**Filtering** (get/update/upsert/deleteRows/rowExists/rowNotExists):
```javascript
"matchType": "anyCondition",   // or "allConditions"
"filters": {
  "conditions": [
    { "keyName": "user_email", "condition": "eq",        "keyValue": "a@b.com" },
    { "keyName": "score",      "condition": "gte",       "keyValue": 10 },
    { "keyName": "archived",   "condition": "isNotEmpty"  }
  ]
}
```
Supported `condition` values: `eq, neq, like, ilike, gt, gte, lt, lte, isEmpty, isNotEmpty, isTrue, isFalse`. The last four are unary — omit `keyValue`.

**Get options**: `returnAll: true` bypasses the default 50-row limit. `options` can include ordering.

**Insert option**: `options.optimizeBulk: true` skips returning inserted rows for ~5x bulk throughput. Do not use when downstream nodes need the inserted row ids.

**Mutating ops** (update/upsert/deleteRows) accept `options.dryRun: true` — returns the rows that *would* be affected with before/after states, without writing.

#### Minimal Insert
```javascript
{
  "resource": "row",
  "operation": "insert",
  "dataTableId": { "__rl": true, "mode": "name", "value": "email_buffer" },
  "columns": {
    "mappingMode": "defineBelow",
    "value": {
      "from_name": "={{ $json.from_name }}",
      "subject":   "={{ $json.subject }}"
    },
    "matchingColumns": [],
    "schema": []
  },
  "options": {}
}
```

#### Get All Rows
`Get` requires at least one condition — a bare "return everything" isn't allowed. Trick: filter on the always-populated system `id` column with `isNotEmpty`.
```javascript
{
  "resource": "row",
  "operation": "get",
  "dataTableId": { "__rl": true, "mode": "name", "value": "email_buffer" },
  "matchType": "anyCondition",
  "filters": {
    "conditions": [ { "keyName": "id", "condition": "isNotEmpty" } ]
  },
  "returnAll": true,
  "options": {}
}
```

#### Delete All Rows
Same `id isNotEmpty` trick — a delete without conditions throws `At least one condition is required`.
```javascript
{
  "resource": "row",
  "operation": "deleteRows",
  "dataTableId": { "__rl": true, "mode": "name", "value": "email_buffer" },
  "matchType": "anyCondition",
  "filters": {
    "conditions": [ { "keyName": "id", "condition": "isNotEmpty" } ]
  },
  "options": {}
}
```

#### Upsert by Natural Key
```javascript
{
  "resource": "row",
  "operation": "upsert",
  "dataTableId": { "__rl": true, "mode": "name", "value": "user_scores" },
  "matchType": "allConditions",
  "filters": {
    "conditions": [ { "keyName": "user_email", "condition": "eq", "keyValue": "={{ $json.email }}" } ]
  },
  "columns": {
    "mappingMode": "defineBelow",
    "value": {
      "user_email": "={{ $json.email }}",
      "score":      "={{ $json.score }}"
    },
    "matchingColumns": ["user_email"],
    "schema": []
  },
  "options": {}
}
```

**System columns**: every table auto-has `id` plus created/updated timestamps — you don't declare these and can't write to them. They're usable in filters.

**When to reach for Data Table vs alternatives**:

| Need | Use |
|------|-----|
| Small per-workflow scratch state, single workflow, not durable across workflow edits | `$getWorkflowStaticData('global')` inside a Code node |
| Persistent structured state, queryable by column, survives workflow rename/edit/deactivation, shared across multiple workflows in the same project | **Data Table node** |
| Large datasets (>>10k rows), complex joins, transactions, FKs, indexes | External Postgres/MySQL |
| Unstructured key-value cache with TTL | Redis |

**Gotchas**:
- Scope is **per project** — Data Tables are not shared across n8n projects. Move a workflow to another project and its Data Table references break.
- Filter operator `eq` on a column that doesn't exist in the table returns a validation error at execution, not at import — always verify column names match the live table.
- Expression values in `columns.value` are evaluated per input item. If the upstream node emits N items, Insert runs N times unless you explicitly use `optimizeBulk`.
- `deleteRows` is the operation value, not `delete`. Using `delete` will import but fail at execution with "unknown operation".
- Race condition in buffer/flush patterns: rows added between `Get` and `deleteRows` will be wiped without being read. For at-least-once semantics, delete by specific row ids returned from `Get` instead of by a broad filter.
- **Zero-match halts the chain.** When `get`, `deleteRows`, `update`, or `upsert` matches 0 rows, the node emits 0 output items and n8n stops the downstream branch silently — no error, just nothing happens. This bites cleanup steps in idempotent test/setup workflows where the table starts empty. Fix: set node-level `"alwaysOutputData": true` (sibling of `parameters`/`type`, NOT inside `parameters`) on any DT node that may legitimately match nothing. The node will then emit a single empty item and the chain continues.
- **DT operations execute once per input item.** A `Get` node fed 3 input items will run 3 separate queries and concatenate the results — usually not what you want. Insert a "collapse" Code node (`return [{ json: {} }];`) between any multi-item-emitting node and a downstream DT op that should run exactly once.
- DT nodes do not natively offer a "run once for all items" mode like the Code node — the collapse-node pattern is currently the only clean workaround.

---

## Data Transformation Nodes

### Set (nodes-base.set)

Most used transformation - 68% of workflows!

#### Set Fixed Values

**Minimal**:
```javascript
{
  "mode": "manual",
  "duplicateItem": false,
  "assignments": {
    "assignments": [
      {
        "name": "status",
        "value": "active",
        "type": "string"
      },
      {
        "name": "count",
        "value": 100,
        "type": "number"
      }
    ]
  }
}
```

#### Set from Input Data

**Mapping data**:
```javascript
{
  "mode": "manual",
  "duplicateItem": false,
  "assignments": {
    "assignments": [
      {
        "name": "fullName",
        "value": "={{$json.firstName}} {{$json.lastName}}",
        "type": "string"
      },
      {
        "name": "email",
        "value": "={{$json.email.toLowerCase()}}",
        "type": "string"
      },
      {
        "name": "timestamp",
        "value": "={{$now.toISO()}}",
        "type": "string"
      }
    ]
  }
}
```

**Gotcha**: Use correct `type` for each field!

```javascript
// ❌ Wrong type
{
  "name": "age",
  "value": "25",      // String
  "type": "string"    // Will be string "25"
}

// ✅ Correct type
{
  "name": "age",
  "value": 25,        // Number
  "type": "number"    // Will be number 25
}
```

---

### Code (nodes-base.code)

JavaScript execution - 42% of workflows

#### Simple Transformation

**Minimal**:
```javascript
{
  "mode": "runOnceForAllItems",
  "jsCode": "return $input.all().map(item => ({\n  json: {\n    name: item.json.name.toUpperCase(),\n    email: item.json.email\n  }\n}));"
}
```

**Per-item processing**:
```javascript
{
  "mode": "runOnceForEachItem",
  "jsCode": "// Process each item\nconst data = $input.item.json;\n\nreturn {\n  json: {\n    fullName: `${data.firstName} ${data.lastName}`,\n    email: data.email.toLowerCase(),\n    timestamp: new Date().toISOString()\n  }\n};"
}
```

**Gotcha**: In Code nodes, use `$input.item.json` or `$input.all()`, NOT `{{...}}`!

```javascript
// ❌ Wrong - expressions don't work in Code nodes
{
  "jsCode": "const name = '={{$json.name}}';"
}

// ✅ Correct - direct access
{
  "jsCode": "const name = $input.item.json.name;"
}
```

---

## Conditional Nodes

### IF (nodes-base.if)

Conditional logic - 38% of workflows

#### String Comparison

**Equals** (binary):
```javascript
{
  "conditions": {
    "string": [
      {
        "value1": "={{$json.status}}",
        "operation": "equals",
        "value2": "active"
      }
    ]
  }
}
```

**Contains** (binary):
```javascript
{
  "conditions": {
    "string": [
      {
        "value1": "={{$json.email}}",
        "operation": "contains",
        "value2": "@example.com"
      }
    ]
  }
}
```

**isEmpty** (unary):
```javascript
{
  "conditions": {
    "string": [
      {
        "value1": "={{$json.email}}",
        "operation": "isEmpty"
        // No value2 - unary operator
        // singleValue: true added by auto-sanitization
      }
    ]
  }
}
```

**Gotcha**: Unary operators (isEmpty, isNotEmpty) don't need value2!

#### Number Comparison

**Greater than**:
```javascript
{
  "conditions": {
    "number": [
      {
        "value1": "={{$json.age}}",
        "operation": "larger",
        "value2": 18
      }
    ]
  }
}
```

#### Boolean Comparison

**Is true**:
```javascript
{
  "conditions": {
    "boolean": [
      {
        "value1": "={{$json.isActive}}",
        "operation": "true"
        // Unary - no value2
      }
    ]
  }
}
```

#### Multiple Conditions (AND)

**All must match**:
```javascript
{
  "conditions": {
    "string": [
      {
        "value1": "={{$json.status}}",
        "operation": "equals",
        "value2": "active"
      }
    ],
    "number": [
      {
        "value1": "={{$json.age}}",
        "operation": "larger",
        "value2": 18
      }
    ]
  },
  "combineOperation": "all"  // AND logic
}
```

#### Multiple Conditions (OR)

**Any can match**:
```javascript
{
  "conditions": {
    "string": [
      {
        "value1": "={{$json.status}}",
        "operation": "equals",
        "value2": "active"
      },
      {
        "value1": "={{$json.status}}",
        "operation": "equals",
        "value2": "pending"
      }
    ]
  },
  "combineOperation": "any"  // OR logic
}
```

---

### Switch (nodes-base.switch)

Multi-way routing - 18% of workflows

#### Basic Switch

**Minimal**:
```javascript
{
  "mode": "rules",
  "rules": {
    "rules": [
      {
        "conditions": {
          "string": [
            {
              "value1": "={{$json.status}}",
              "operation": "equals",
              "value2": "active"
            }
          ]
        }
      },
      {
        "conditions": {
          "string": [
            {
              "value1": "={{$json.status}}",
              "operation": "equals",
              "value2": "pending"
            }
          ]
        }
      }
    ]
  },
  "fallbackOutput": "extra"  // Catch-all for non-matching
}
```

**Gotcha**: Number of rules must match number of outputs!

---

## AI Nodes

### OpenAI (nodes-langchain.openAi)

AI operations - 234 templates

#### Chat Completion

**Minimal**:
```javascript
{
  "resource": "chat",
  "operation": "complete",
  "messages": {
    "values": [
      {
        "role": "user",
        "content": "={{$json.prompt}}"
      }
    ]
  }
}
```

**With system prompt**:
```javascript
{
  "resource": "chat",
  "operation": "complete",
  "messages": {
    "values": [
      {
        "role": "system",
        "content": "You are a helpful assistant specialized in customer support."
      },
      {
        "role": "user",
        "content": "={{$json.userMessage}}"
      }
    ]
  },
  "options": {
    "temperature": 0.7,
    "maxTokens": 500
  }
}
```

---

## Schedule Nodes

### Schedule Trigger (nodes-base.scheduleTrigger)

Time-based workflows - 28% have schedule triggers

#### Daily at Specific Time

**Minimal**:
```javascript
{
  "rule": {
    "interval": [
      {
        "field": "hours",
        "hoursInterval": 24
      }
    ],
    "hour": 9,
    "minute": 0,
    "timezone": "America/New_York"
  }
}
```

**Gotcha**: Always set timezone explicitly!

```javascript
// ❌ Bad - uses server timezone
{
  "rule": {
    "interval": [...]
  }
}

// ✅ Good - explicit timezone
{
  "rule": {
    "interval": [...],
    "timezone": "America/New_York"
  }
}
```

#### Every N Minutes

**Minimal**:
```javascript
{
  "rule": {
    "interval": [
      {
        "field": "minutes",
        "minutesInterval": 15
      }
    ]
  }
}
```

#### Cron Expression

**Advanced scheduling**:
```javascript
{
  "mode": "cron",
  "cronExpression": "0 */2 * * *",  // Every 2 hours
  "timezone": "America/New_York"
}
```

---

## Summary

**Key Patterns by Category**:

| Category | Most Common | Key Gotcha |
|---|---|---|
| HTTP/API | GET, POST JSON | Remember sendBody: true |
| Webhooks | POST receiver | Data under $json.body |
| Communication | Slack post | Channel format (#name) |
| Database | SELECT with params | Use parameterized queries |
| Transform | Set assignments | Correct type per field |
| Conditional | IF string equals | Unary vs binary operators |
| AI | OpenAI chat | System + user messages |
| Schedule | Daily at time | Set timezone explicitly |

**Configuration Approach**:
1. Use patterns as starting point
2. Adapt to your use case
3. Validate configuration
4. Iterate based on errors
5. Deploy when valid

**Related Files**:
- **SKILL.md** - Configuration workflow and philosophy
- **DEPENDENCIES.md** - Property dependency rules
