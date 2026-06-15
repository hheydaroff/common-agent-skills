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

# False Positives Guide

When validation warnings are acceptable and how to handle them.

---

## What Are False Positives?

**Definition**: Validation warnings that are technically "issues" but acceptable in your specific use case.

**Key insight**: Not all warnings need to be fixed!

Many warnings are context-dependent:
- ~40% of warnings are acceptable in specific use cases
- Using `ai-friendly` profile reduces false positives by 60%

---

## Philosophy

### ✅ Good Practice
```
1. Run validation with 'runtime' profile
2. Fix all ERRORS
3. Review each WARNING
4. Decide if acceptable for your use case
5. Document why you accepted it
6. Deploy with confidence
```

### ❌ Bad Practice
```
1. Ignore all warnings blindly
2. Use 'minimal' profile to avoid warnings
3. Deploy without understanding risks
```

---

## Common False Positives

### 1. Missing Error Handling

**Warning**:
```json
{
  "type": "best_practice",
  "message": "No error handling configured",
  "suggestion": "Add continueOnFail: true and retryOnFail: true"
}
```

#### When Acceptable

**✅ Development/Testing Workflows**
```javascript
// Testing workflow - failures are obvious
{
  "name": "Test Slack Integration",
  "nodes": [{
    "type": "n8n-nodes-base.slack",
    "parameters": {
      "resource": "message",
      "operation": "post",
      "channel": "#test"
      // No error handling - OK for testing
    }
  }]
}
```

**Reasoning**: You WANT to see failures during testing.

**✅ Non-Critical Notifications**
```javascript
// Nice-to-have notification
{
  "name": "Optional Slack Notification",
  "parameters": {
    "channel": "#general",
    "text": "FYI: Process completed"
    // If this fails, no big deal
  }
}
```

**Reasoning**: Notification failure doesn't affect core functionality.

**✅ Manual Trigger Workflows**
```javascript
// Manual workflow - user is watching
{
  "nodes": [{
    "type": "n8n-nodes-base.webhook",
    "parameters": {
      "path": "manual-test"
      // No error handling - user will retry manually
    }
  }]
}
```

**Reasoning**: User is present to see and handle errors.

#### When to Fix

**❌ Production Automation**
```javascript
// BAD: Critical workflow without error handling
{
  "name": "Process Customer Orders",
  "nodes": [{
    "type": "n8n-nodes-base.postgres",
    "parameters": {
      "query": "INSERT INTO orders..."
      // ❌ Should have error handling!
    }
  }]
}
```

**Fix**:
```javascript
{
  "parameters": {
    "query": "INSERT INTO orders...",
    "continueOnFail": true,
    "retryOnFail": true,
    "maxTries": 3,
    "waitBetweenTries": 1000
  }
}
```

**❌ Critical Integrations**
```javascript
// BAD: Payment processing without error handling
{
  "name": "Process Payment",
  "type": "n8n-nodes-base.stripe"
  // ❌ Payment failures MUST be handled!
}
```

---

### 2. No Retry Logic

**Warning**:
```json
{
  "type": "best_practice",
  "message": "External API calls should retry on failure",
  "suggestion": "Add retryOnFail: true with exponential backoff"
}
```

#### When Acceptable

**✅ APIs with Built-in Retry**
```javascript
// Stripe has its own retry mechanism
{
  "type": "n8n-nodes-base.stripe",
  "parameters": {
    "resource": "charge",
    "operation": "create"
    // Stripe SDK retries automatically
  }
}
```

**✅ Idempotent Operations**
```javascript
// GET request - safe to retry manually if needed
{
  "method": "GET",
  "url": "https://api.example.com/status"
  // Read-only, no side effects
}
```

**✅ Local/Internal Services**
```javascript
// Internal API with high reliability
{
  "url": "http://localhost:3000/process"
  // Local service, failures are rare and obvious
}
```

#### When to Fix

**❌ Flaky External APIs**
```javascript
// BAD: Known unreliable API without retries
{
  "url": "https://unreliable-api.com/data"
  // ❌ Should retry!
}

// GOOD:
{
  "url": "https://unreliable-api.com/data",
  "retryOnFail": true,
  "maxTries": 3,
  "waitBetweenTries": 2000
}
```

**❌ Non-Idempotent Operations**
```javascript
// BAD: POST without retry - may lose data
{
  "method": "POST",
  "url": "https://api.example.com/create"
  // ❌ Could timeout and lose data
}
```

---

### 3. Missing Rate Limiting

**Warning**:
```json
{
  "type": "best_practice",
  "message": "API may have rate limits",
  "suggestion": "Add rate limiting or batch requests"
}
```

#### When Acceptable

**✅ Internal APIs**
```javascript
// Internal microservice - no rate limits
{
  "url": "http://internal-api/process"
  // Company controls both ends
}
```

**✅ Low-Volume Workflows**
```javascript
// Runs once per day
{
  "trigger": {
    "type": "n8n-nodes-base.cron",
    "parameters": {
      "mode": "everyDay",
      "hour": 9
    }
  },
  "nodes": [{
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "https://api.example.com/daily-report"
      // Once per day = no rate limit concerns
    }
  }]
}
```

**✅ APIs with Server-Side Limits**
```javascript
// API returns 429 and n8n handles it
{
  "url": "https://api.example.com/data",
  "options": {
    "response": {
      "response": {
        "neverError": false  // Will error on 429
      }
    }
  },
  "retryOnFail": true  // Retry on 429
}
```

#### When to Fix

**❌ High-Volume Public APIs**
```javascript
// BAD: Loop hitting rate-limited API
{
  "nodes": [{
    "type": "n8n-nodes-base.splitInBatches",
    "parameters": {
      "batchSize": 100
    }
  }, {
    "type": "n8n-nodes-base.httpRequest",
    "parameters": {
      "url": "https://api.github.com/..."
      // ❌ GitHub has strict rate limits!
    }
  }]
}

// GOOD: Add rate limiting
{
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "url": "https://api.github.com/...",
    "options": {
      "batching": {
        "batch": {
          "batchSize": 10,
          "batchInterval": 1000  // 1 second between batches
        }
      }
    }
  }
}
```

---

### 4. Unbounded Database Queries

**Warning**:
```json
{
  "type": "performance",
  "message": "SELECT without LIMIT can return massive datasets",
  "suggestion": "Add LIMIT clause or use pagination"
}
```

#### When Acceptable

**✅ Small Known Datasets**
```javascript
// Config table with ~10 rows
{
  "query": "SELECT * FROM app_config"
  // Known to be small, no LIMIT needed
}
```

**✅ Aggregation Queries**
```javascript
// COUNT/SUM operations
{
  "query": "SELECT COUNT(*) as total FROM users WHERE active = true"
  // Aggregation, not returning rows
}
```

**✅ Development/Testing**
```javascript
// Testing with small dataset
{
  "query": "SELECT * FROM test_users"
  // Test database has 5 rows
}
```

#### When to Fix

**❌ Production Queries on Large Tables**
```javascript
// BAD: User table could have millions of rows
{
  "query": "SELECT * FROM users"
  // ❌ Could return millions of rows!
}

// GOOD: Add LIMIT
{
  "query": "SELECT * FROM users LIMIT 1000"
}

// BETTER: Use pagination
{
  "query": "SELECT * FROM users WHERE id > {{$json.lastId}} LIMIT 1000"
}
```

---

### 5. Missing Input Validation

**Warning**:
```json
{
  "type": "best_practice",
  "message": "Webhook doesn't validate input data",
  "suggestion": "Add IF node to validate required fields"
}
```

#### When Acceptable

**✅ Internal Webhooks**
```javascript
// Webhook from your own backend
{
  "type": "n8n-nodes-base.webhook",
  "parameters": {
    "path": "internal-trigger"
    // Your backend already validates
  }
}
```

**✅ Trusted Sources**
```javascript
// Webhook from Stripe (cryptographically signed)
{
  "type": "n8n-nodes-base.webhook",
  "parameters": {
    "path": "stripe-webhook",
    "authentication": "headerAuth"
    // Stripe signature validates authenticity
  }
}
```

#### When to Fix

**❌ Public Webhooks**
```javascript
// BAD: Public webhook without validation
{
  "type": "n8n-nodes-base.webhook",
  "parameters": {
    "path": "public-form-submit"
    // ❌ Anyone can send anything!
  }
}

// GOOD: Add validation
{
  "nodes": [
    {
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook"
    },
    {
      "name": "Validate Input",
      "type": "n8n-nodes-base.if",
      "parameters": {
        "conditions": {
          "boolean": [
            {
              "value1": "={{$json.body.email}}",
              "operation": "isNotEmpty"
            },
            {
              "value1": "={{$json.body.email}}",
              "operation": "regex",
              "value2": "^[^@]+@[^@]+\\.[^@]+$"
            }
          ]
        }
      }
    }
  ]
}
```

---

### 6. Hardcoded Credentials

**Warning**:
```json
{
  "type": "security",
  "message": "Credentials should not be hardcoded",
  "suggestion": "Use n8n credential system"
}
```

#### When Acceptable

**✅ Public APIs (No Auth)**
```javascript
// Truly public API with no secrets
{
  "url": "https://api.ipify.org"
  // No credentials needed
}
```

**✅ Demo/Example Workflows**
```javascript
// Example workflow in documentation
{
  "url": "https://example.com/api",
  "headers": {
    "Authorization": "Bearer DEMO_TOKEN"
  }
  // Clearly marked as example
}
```

#### When to Fix (Always!)

**❌ Real Credentials**
```javascript
// BAD: Real API key in workflow
{
  "headers": {
    "Authorization": "Bearer sk_live_abc123..."
  }
  // ❌ NEVER hardcode real credentials!
}

// GOOD: Use credentials system
{
  "authentication": "headerAuth",
  "credentials": {
    "headerAuth": {
      "id": "credential-id",
      "name": "My API Key"
    }
  }
}
```

---

## Validation Profile Strategies

### Strategy 1: Progressive Strictness

**Development**:
```javascript
validate_node({
  nodeType: "nodes-base.slack",
  config,
  profile: "ai-friendly"  // Fewer warnings during development
})
```

**Pre-Production**:
```javascript
validate_node({
  nodeType: "nodes-base.slack",
  config,
  profile: "runtime"  // Balanced validation
})
```

**Production Deployment**:
```javascript
validate_node({
  nodeType: "nodes-base.slack",
  config,
  profile: "strict"  // All warnings, review each one
})
```

### Strategy 2: Profile by Workflow Type

**Quick Automations**:
- Profile: `ai-friendly`
- Accept: Most warnings
- Fix: Only errors + security warnings

**Business-Critical Workflows**:
- Profile: `strict`
- Accept: Very few warnings
- Fix: Everything possible

**Integration Testing**:
- Profile: `minimal`
- Accept: All warnings (just testing connections)
- Fix: Only errors that prevent execution

---

## Decision Framework

### Should I Fix This Warning?

```
┌─────────────────────────────────┐
│ Is it a SECURITY warning?       │
├─────────────────────────────────┤
│ YES → Always fix                │
│ NO  → Continue                  │
└─────────────────────────────────┘
         ↓
┌─────────────────────────────────┐
│ Is this a production workflow?  │
├─────────────────────────────────┤
│ YES → Continue                  │
│ NO  → Probably acceptable       │
└─────────────────────────────────┘
         ↓
┌─────────────────────────────────┐
│ Does it handle critical data?   │
├─────────────────────────────────┤
│ YES → Fix the warning           │
│ NO  → Continue                  │
└─────────────────────────────────┘
         ↓
┌─────────────────────────────────┐
│ Is there a known workaround?    │
├─────────────────────────────────┤
│ YES → Acceptable if documented  │
│ NO  → Fix the warning           │
└─────────────────────────────────┘
```

---

## Documentation Template

When accepting a warning, document why:

```javascript
// workflows/customer-notifications.json

{
  "nodes": [{
    "name": "Send Slack Notification",
    "type": "n8n-nodes-base.slack",
    "parameters": {
      "channel": "#notifications"
      // ACCEPTED WARNING: No error handling
      // Reason: Non-critical notification, failures are acceptable
      // Reviewed: 2025-10-20
      // Reviewer: Engineering Team
    }
  }]
}
```

---

## Known n8n Issues

### Issue #304: IF Node Metadata Warning

**Warning**:
```json
{
  "type": "metadata_incomplete",
  "message": "IF node missing conditions.options metadata",
  "node": "IF"
}
```

**Status**: False positive for IF v2.2+

**Why it occurs**: Auto-sanitization adds metadata, but validation runs before sanitization

**What to do**: Ignore - metadata is added on save

### Issue #306: Switch Branch Count

**Warning**:
```json
{
  "type": "configuration_mismatch",
  "message": "Switch has 3 rules but 4 output connections",
  "node": "Switch"
}
```

**Status**: False positive when using "fallback" mode

**Why it occurs**: Fallback creates extra output

**What to do**: Ignore if using fallback intentionally

### Issue #338: Credential Validation in Test Mode

**Warning**:
```json
{
  "type": "credentials_invalid",
  "message": "Cannot validate credentials without execution context"
}
```

**Status**: False positive during static validation

**Why it occurs**: Credentials validated at runtime, not build time

**What to do**: Ignore - credentials are validated when workflow runs

---

## Summary

### Always Fix
- ❌ Security warnings
- ❌ Hardcoded credentials
- ❌ SQL injection risks
- ❌ Production workflow errors

### Usually Fix
- ⚠️ Error handling (production)
- ⚠️ Retry logic (external APIs)
- ⚠️ Input validation (public webhooks)
- ⚠️ Rate limiting (high volume)

### Often Acceptable
- ✅ Error handling (dev/test)
- ✅ Retry logic (internal APIs)
- ✅ Rate limiting (low volume)
- ✅ Query limits (small datasets)

### Always Acceptable
- ✅ Known n8n issues (#304, #306, #338)
- ✅ Auto-sanitization warnings
- ✅ Metadata completeness (auto-fixed)

**Golden Rule**: If you accept a warning, document WHY.

**Related Files**:
- **SKILL.md** - Main validation guide
- **ERROR_CATALOG.md** - Error types and fixes


---

# Error Catalog

Comprehensive catalog of n8n validation errors with real examples and fixes.

---

## Error Types Overview

Common validation errors by priority:

| Error Type | Priority | Severity | Auto-Fix |
|---|---|---|---|
| missing_required | Highest | Error | ❌ |
| invalid_value | High | Error | ❌ |
| type_mismatch | Medium | Error | ❌ |
| invalid_expression | Medium | Error | ❌ |
| invalid_reference | Low | Error | ❌ |
| operator_structure | Lowest | Warning | ✅ |

---

## Errors (Must Fix)

### 1. missing_required

**What it means**: Required field is not provided in node configuration

**When it occurs**:
- Creating new nodes without all required fields
- Copying configurations between different operations
- Switching operations that have different requirements

**Most common validation error**

#### Example 1: Slack Channel Missing

**Error**:
```json
{
  "type": "missing_required",
  "property": "channel",
  "message": "Channel name is required",
  "node": "Slack",
  "path": "parameters.channel"
}
```

**Broken Configuration**:
```javascript
{
  "resource": "message",
  "operation": "post"
  // Missing: channel
}
```

**Fix**:
```javascript
{
  "resource": "message",
  "operation": "post",
  "channel": "#general"  // ✅ Added required field
}
```

**How to identify required fields**:
```javascript
// Use get_node to see what's required
const info = get_node({
  nodeType: "nodes-base.slack"
});
// Check properties marked as "required": true
```

#### Example 2: HTTP Request Missing URL

**Error**:
```json
{
  "type": "missing_required",
  "property": "url",
  "message": "URL is required for HTTP Request",
  "node": "HTTP Request",
  "path": "parameters.url"
}
```

**Broken Configuration**:
```javascript
{
  "method": "GET",
  "authentication": "none"
  // Missing: url
}
```

**Fix**:
```javascript
{
  "method": "GET",
  "authentication": "none",
  "url": "https://api.example.com/data"  // ✅ Added
}
```

#### Example 3: Database Query Missing Connection

**Error**:
```json
{
  "type": "missing_required",
  "property": "query",
  "message": "SQL query is required",
  "node": "Postgres",
  "path": "parameters.query"
}
```

**Broken Configuration**:
```javascript
{
  "operation": "executeQuery"
  // Missing: query
}
```

**Fix**:
```javascript
{
  "operation": "executeQuery",
  "query": "SELECT * FROM users WHERE active = true"  // ✅ Added
}
```

#### Example 4: Conditional Fields

**Error**:
```json
{
  "type": "missing_required",
  "property": "body",
  "message": "Request body is required when sendBody is true",
  "node": "HTTP Request",
  "path": "parameters.body"
}
```

**Broken Configuration**:
```javascript
{
  "method": "POST",
  "url": "https://api.example.com/create",
  "sendBody": true
  // Missing: body (required when sendBody=true)
}
```

**Fix**:
```javascript
{
  "method": "POST",
  "url": "https://api.example.com/create",
  "sendBody": true,
  "body": {
    "contentType": "json",
    "content": {
      "name": "John",
      "email": "john@example.com"
    }
  }  // ✅ Added conditional required field
}
```

---

### 2. invalid_value

**What it means**: Provided value doesn't match allowed options or format

**When it occurs**:
- Using wrong enum value
- Typos in operation names
- Invalid format for specialized fields (emails, URLs, channels)

**Second most common error**

#### Example 1: Invalid Operation

**Error**:
```json
{
  "type": "invalid_value",
  "property": "operation",
  "message": "Operation must be one of: post, update, delete, get",
  "current": "send",
  "allowed": ["post", "update", "delete", "get"]
}
```

**Broken Configuration**:
```javascript
{
  "resource": "message",
  "operation": "send"  // ❌ Invalid - should be "post"
}
```

**Fix**:
```javascript
{
  "resource": "message",
  "operation": "post"  // ✅ Use valid operation
}
```

#### Example 2: Invalid HTTP Method

**Error**:
```json
{
  "type": "invalid_value",
  "property": "method",
  "message": "Method must be one of: GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS",
  "current": "FETCH",
  "allowed": ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]
}
```

**Broken Configuration**:
```javascript
{
  "method": "FETCH",  // ❌ Invalid
  "url": "https://api.example.com"
}
```

**Fix**:
```javascript
{
  "method": "GET",  // ✅ Use valid HTTP method
  "url": "https://api.example.com"
}
```

#### Example 3: Invalid Channel Format

**Error**:
```json
{
  "type": "invalid_value",
  "property": "channel",
  "message": "Channel name must start with # and be lowercase (e.g., #general)",
  "current": "General"
}
```

**Broken Configuration**:
```javascript
{
  "resource": "message",
  "operation": "post",
  "channel": "General"  // ❌ Wrong format
}
```

**Fix**:
```javascript
{
  "resource": "message",
  "operation": "post",
  "channel": "#general"  // ✅ Correct format
}
```

#### Example 4: Invalid Enum with Case Sensitivity

**Error**:
```json
{
  "type": "invalid_value",
  "property": "resource",
  "message": "Resource must be one of: channel, message, user, file",
  "current": "Message",
  "allowed": ["channel", "message", "user", "file"]
}
```

**Note**: Enums are case-sensitive!

**Broken Configuration**:
```javascript
{
  "resource": "Message",  // ❌ Capital M
  "operation": "post"
}
```

**Fix**:
```javascript
{
  "resource": "message",  // ✅ Lowercase
  "operation": "post"
}
```

---

### 3. type_mismatch

**What it means**: Value is wrong data type (string instead of number, etc.)

**When it occurs**:
- Hardcoding values that should be numbers
- Using expressions where literals are expected
- JSON serialization issues

**Common error**

#### Example 1: String Instead of Number

**Error**:
```json
{
  "type": "type_mismatch",
  "property": "limit",
  "message": "Expected number, got string",
  "expected": "number",
  "current": "100"
}
```

**Broken Configuration**:
```javascript
{
  "operation": "executeQuery",
  "query": "SELECT * FROM users",
  "limit": "100"  // ❌ String
}
```

**Fix**:
```javascript
{
  "operation": "executeQuery",
  "query": "SELECT * FROM users",
  "limit": 100  // ✅ Number
}
```

#### Example 2: Number Instead of String

**Error**:
```json
{
  "type": "type_mismatch",
  "property": "channel",
  "message": "Expected string, got number",
  "expected": "string",
  "current": 12345
}
```

**Broken Configuration**:
```javascript
{
  "resource": "message",
  "operation": "post",
  "channel": 12345  // ❌ Number (even if channel ID)
}
```

**Fix**:
```javascript
{
  "resource": "message",
  "operation": "post",
  "channel": "#general"  // ✅ String (channel name, not ID)
}
```

#### Example 3: Boolean as String

**Error**:
```json
{
  "type": "type_mismatch",
  "property": "sendHeaders",
  "message": "Expected boolean, got string",
  "expected": "boolean",
  "current": "true"
}
```

**Broken Configuration**:
```javascript
{
  "method": "GET",
  "url": "https://api.example.com",
  "sendHeaders": "true"  // ❌ String "true"
}
```

**Fix**:
```javascript
{
  "method": "GET",
  "url": "https://api.example.com",
  "sendHeaders": true  // ✅ Boolean true
}
```

#### Example 4: Object Instead of Array

**Error**:
```json
{
  "type": "type_mismatch",
  "property": "tags",
  "message": "Expected array, got object",
  "expected": "array",
  "current": {"tag": "important"}
}
```

**Broken Configuration**:
```javascript
{
  "name": "New Channel",
  "tags": {"tag": "important"}  // ❌ Object
}
```

**Fix**:
```javascript
{
  "name": "New Channel",
  "tags": ["important", "alerts"]  // ✅ Array
}
```

---

### 4. invalid_expression

**What it means**: n8n expression has syntax errors or invalid references

**When it occurs**:
- Missing `{{}}` around expressions
- Typos in variable names
- Referencing non-existent nodes or fields
- Invalid JavaScript syntax in expressions

**Moderately common**

**Related**: See **n8n Expression Syntax** skill for comprehensive expression guidance

#### Example 1: Missing Curly Braces

**Error**:
```json
{
  "type": "invalid_expression",
  "property": "text",
  "message": "Expressions must be wrapped in {{}}",
  "current": "$json.name"
}
```

**Broken Configuration**:
```javascript
{
  "resource": "message",
  "operation": "post",
  "channel": "#general",
  "text": "$json.name"  // ❌ Missing {{}}
}
```

**Fix**:
```javascript
{
  "resource": "message",
  "operation": "post",
  "channel": "#general",
  "text": "={{$json.name}}"  // ✅ Wrapped in {{}}
}
```

#### Example 2: Invalid Node Reference

**Error**:
```json
{
  "type": "invalid_expression",
  "property": "value",
  "message": "Referenced node 'HTTP Requets' does not exist",
  "current": "={{$node['HTTP Requets'].json.data}}"
}
```

**Broken Configuration**:
```javascript
{
  "field": "data",
  "value": "={{$node['HTTP Requets'].json.data}}"  // ❌ Typo in node name
}
```

**Fix**:
```javascript
{
  "field": "data",
  "value": "={{$node['HTTP Request'].json.data}}"  // ✅ Correct node name
}
```

#### Example 3: Invalid Property Access

**Error**:
```json
{
  "type": "invalid_expression",
  "property": "text",
  "message": "Cannot access property 'user' of undefined",
  "current": "={{$json.data.user.name}}"
}
```

**Broken Configuration**:
```javascript
{
  "text": "={{$json.data.user.name}}"  // ❌ Structure doesn't exist
}
```

**Fix** (with safe navigation):
```javascript
{
  "text": "={{$json.data?.user?.name || 'Unknown'}}"  // ✅ Safe navigation + fallback
}
```

#### Example 4: Webhook Data Access Error

**Error**:
```json
{
  "type": "invalid_expression",
  "property": "value",
  "message": "Property 'email' not found in $json",
  "current": "={{$json.email}}"
}
```

**Common Gotcha**: Webhook data is under `.body`!

**Broken Configuration**:
```javascript
{
  "field": "email",
  "value": "={{$json.email}}"  // ❌ Missing .body
}
```

**Fix**:
```javascript
{
  "field": "email",
  "value": "={{$json.body.email}}"  // ✅ Webhook data under .body
}
```

---

### 5. invalid_reference

**What it means**: Configuration references a node that doesn't exist in the workflow

**When it occurs**:
- Node was renamed or deleted
- Typo in node name
- Copy-pasting from another workflow

**Less common error**

#### Example 1: Deleted Node Reference

**Error**:
```json
{
  "type": "invalid_reference",
  "property": "expression",
  "message": "Node 'Transform Data' does not exist in workflow",
  "referenced_node": "Transform Data"
}
```

**Broken Configuration**:
```javascript
{
  "value": "={{$node['Transform Data'].json.result}}"  // ❌ Node deleted
}
```

**Fix**:
```javascript
// Option 1: Update to existing node
{
  "value": "={{$node['Set'].json.result}}"
}

// Option 2: Remove expression if not needed
{
  "value": "default_value"
}
```

#### Example 2: Connection to Non-Existent Node

**Error**:
```json
{
  "type": "invalid_reference",
  "message": "Connection references node 'Slack1' which does not exist",
  "source": "HTTP Request",
  "target": "Slack1"
}
```

**Fix**: Use `cleanStaleConnections` operation:
```javascript
n8n_update_partial_workflow({
  id: "workflow-id",
  operations: [{
    type: "cleanStaleConnections"
  }]
})
```

#### Example 3: Renamed Node Not Updated

**Error**:
```json
{
  "type": "invalid_reference",
  "property": "expression",
  "message": "Node 'Get Weather' does not exist (did you mean 'Weather API'?)",
  "referenced_node": "Get Weather",
  "suggestions": ["Weather API"]
}
```

**Broken Configuration**:
```javascript
{
  "value": "={{$node['Get Weather'].json.temperature}}"  // ❌ Old name
}
```

**Fix**:
```javascript
{
  "value": "={{$node['Weather API'].json.temperature}}"  // ✅ Current name
}
```

---

## Warnings (Should Fix)

### 6. best_practice

**What it means**: Configuration works but doesn't follow best practices

**Severity**: Warning (doesn't block execution)

**When acceptable**: Development, testing, simple workflows

**When to fix**: Production workflows, critical operations

#### Example 1: Missing Error Handling

**Warning**:
```json
{
  "type": "best_practice",
  "property": "onError",
  "message": "Slack API can have rate limits and connection issues",
  "suggestion": "Add error handling: onError: 'continueRegularOutput'"
}
```

**Current Configuration**:
```javascript
{
  "resource": "message",
  "operation": "post",
  "channel": "#alerts"
  // No error handling ⚠️
}
```

**Recommended Fix**:
```javascript
{
  "resource": "message",
  "operation": "post",
  "channel": "#alerts",
  "continueOnFail": true,
  "retryOnFail": true,
  "maxTries": 3
}
```

#### Example 2: No Retry Logic

**Warning**:
```json
{
  "type": "best_practice",
  "property": "retryOnFail",
  "message": "External API calls should retry on failure",
  "suggestion": "Add retryOnFail: true, maxTries: 3, waitBetweenTries: 1000"
}
```

**When to ignore**: Idempotent operations, APIs with their own retry logic

**When to fix**: Flaky external services, production automation

---

### 7. deprecated

**What it means**: Using old API version or deprecated feature

**Severity**: Warning (still works but may stop working in future)

**When to fix**: Always (eventually)

#### Example 1: Old typeVersion

**Warning**:
```json
{
  "type": "deprecated",
  "property": "typeVersion",
  "message": "typeVersion 1 is deprecated for Slack node, use version 2",
  "current": 1,
  "recommended": 2
}
```

**Fix**:
```javascript
{
  "type": "n8n-nodes-base.slack",
  "typeVersion": 2,  // ✅ Updated
  // May need to update configuration for new version
}
```

---

### 8. performance

**What it means**: Configuration may cause performance issues

**Severity**: Warning

**When to fix**: High-volume workflows, large datasets

#### Example 1: Unbounded Query

**Warning**:
```json
{
  "type": "performance",
  "property": "query",
  "message": "SELECT without LIMIT can return massive datasets",
  "suggestion": "Add LIMIT clause or use pagination"
}
```

**Current**:
```sql
SELECT * FROM users WHERE active = true
```

**Fix**:
```sql
SELECT * FROM users WHERE active = true LIMIT 1000
```

---

## Auto-Sanitization Fixes

### 9. operator_structure

**What it means**: IF/Switch operator structure issues

**Severity**: Warning

**Auto-Fix**: ✅ YES - Fixed automatically on workflow save

**Rare** (mostly auto-fixed)

#### Fixed Automatically: Binary Operators

**Before** (you create this):
```javascript
{
  "type": "boolean",
  "operation": "equals",
  "singleValue": true  // ❌ Wrong for binary operator
}
```

**After** (auto-sanitization fixes it):
```javascript
{
  "type": "boolean",
  "operation": "equals"
  // singleValue removed ✅
}
```

**You don't need to do anything** - this is fixed on save!

#### Fixed Automatically: Unary Operators

**Before**:
```javascript
{
  "type": "boolean",
  "operation": "isEmpty"
  // Missing singleValue ❌
}
```

**After**:
```javascript
{
  "type": "boolean",
  "operation": "isEmpty",
  "singleValue": true  // ✅ Added automatically
}
```

**What you should do**: Trust auto-sanitization, don't manually fix these!

---

## Recovery Patterns

### Pattern 1: Progressive Validation

**Problem**: Too many errors at once

**Solution**:
```javascript
// Step 1: Minimal valid config
let config = {
  resource: "message",
  operation: "post",
  channel: "#general",
  text: "Hello"
};

validate_node({nodeType: "nodes-base.slack", config, profile: "runtime"});
// ✅ Valid

// Step 2: Add features one by one
config.attachments = [...];
validate_node({nodeType: "nodes-base.slack", config, profile: "runtime"});

config.blocks = [...];
validate_node({nodeType: "nodes-base.slack", config, profile: "runtime"});
```

### Pattern 2: Error Triage

**Problem**: Multiple errors

**Solution**:
```javascript
const result = validate_node({...});

// 1. Fix errors (must fix)
result.errors.forEach(error => {
  console.log(`MUST FIX: ${error.property} - ${error.message}`);
});

// 2. Review warnings (should fix)
result.warnings.forEach(warning => {
  console.log(`SHOULD FIX: ${warning.property} - ${warning.message}`);
});

// 3. Consider suggestions (optional)
result.suggestions.forEach(sug => {
  console.log(`OPTIONAL: ${sug.message}`);
});
```

### Pattern 3: Use get_node

**Problem**: Don't know what's required

**Solution**:
```javascript
// Before configuring, check requirements
const info = get_node({
  nodeType: "nodes-base.slack"
});

// Look for required fields
info.properties.forEach(prop => {
  if (prop.required) {
    console.log(`Required: ${prop.name} (${prop.type})`);
  }
});
```

---

## Summary

**Most Common Errors**:
1. `missing_required` (45%) - Always check get_node
2. `invalid_value` (28%) - Check allowed values
3. `type_mismatch` (12%) - Use correct data types
4. `invalid_expression` (8%) - Use Expression Syntax skill
5. `invalid_reference` (5%) - Clean stale connections

**Auto-Fixed**:
- `operator_structure` - Trust auto-sanitization!

**Related Skills**:
- **SKILL.md** - Main validation guide
- **FALSE_POSITIVES.md** - When to ignore warnings
- **n8n Expression Syntax** - Fix expression errors
- **n8n MCP Tools Expert** - Use validation tools correctly
