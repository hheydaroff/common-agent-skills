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


# Python Code Node (Beta)

Expert guidance for writing Python code in n8n Code nodes.

---

## ⚠️ Important: JavaScript First

**Recommendation**: Use **JavaScript for 95% of use cases**. Only use Python when:
- You need specific Python standard library functions
- You're significantly more comfortable with Python syntax
- You're doing data transformations better suited to Python

**Why JavaScript is preferred:**
- Full n8n helper functions ($helpers.httpRequest, etc.)
- Luxon DateTime library for advanced date/time operations
- No external library limitations
- Better n8n documentation and community support

---

## Quick Start

```python
# Basic template for Python Code nodes
items = _input.all()

# Process data
processed = []
for item in items:
    processed.append({
        "json": {
            **item["json"],
            "processed": True,
            "timestamp": datetime.now().isoformat()
        }
    })

return processed
```

### Essential Rules

1. **Consider JavaScript first** - Use Python only when necessary
2. **Access data**: `_input.all()`, `_input.first()`, or `_input.item`
3. **CRITICAL**: Must return `[{"json": {...}}]` format
4. **CRITICAL**: Webhook data is under `_json["body"]` (not `_json` directly)
5. **CRITICAL LIMITATION**: **No external libraries** (no requests, pandas, numpy)
6. **Standard library only**: json, datetime, re, base64, hashlib, urllib.parse, math, random, statistics

---

## Mode Selection Guide

Same as JavaScript - choose based on your use case:

### Run Once for All Items (Recommended - Default)

**Use this mode for:** 95% of use cases

- **How it works**: Code executes **once** regardless of input count
- **Data access**: `_input.all()` or `_items` array (Native mode)
- **Best for**: Aggregation, filtering, batch processing, transformations
- **Performance**: Faster for multiple items (single execution)

```python
# Example: Calculate total from all items
all_items = _input.all()
total = sum(item["json"].get("amount", 0) for item in all_items)

return [{
    "json": {
        "total": total,
        "count": len(all_items),
        "average": total / len(all_items) if all_items else 0
    }
}]
```

### Run Once for Each Item

**Use this mode for:** Specialized cases only

- **How it works**: Code executes **separately** for each input item
- **Data access**: `_input.item` or `_item` (Native mode)
- **Best for**: Item-specific logic, independent operations, per-item validation
- **Performance**: Slower for large datasets (multiple executions)

```python
# Example: Add processing timestamp to each item
item = _input.item

return [{
    "json": {
        **item["json"],
        "processed": True,
        "processed_at": datetime.now().isoformat()
    }
}]
```

---

## Python Modes: Beta vs Native

n8n offers two Python execution modes:

### Python (Beta) - Recommended
- **Use**: `_input`, `_json`, `_node` helper syntax
- **Best for**: Most Python use cases
- **Helpers available**: `_now`, `_today`, `_jmespath()`
- **Import**: `from datetime import datetime`

```python
# Python (Beta) example
items = _input.all()
now = _now  # Built-in datetime object

return [{
    "json": {
        "count": len(items),
        "timestamp": now.isoformat()
    }
}]
```

### Python (Native) (Beta)
- **Use**: `_items`, `_item` variables only
- **No helpers**: No `_input`, `_now`, etc.
- **More limited**: Standard Python only
- **Use when**: Need pure Python without n8n helpers

```python
# Python (Native) example
processed = []

for item in _items:
    processed.append({
        "json": {
            "id": item["json"].get("id"),
            "processed": True
        }
    })

return processed
```

**Recommendation**: Use **Python (Beta)** for better n8n integration.

---

## Data Access Patterns

### Pattern 1: _input.all() - Most Common

**Use when**: Processing arrays, batch operations, aggregations

```python
# Get all items from previous node
all_items = _input.all()

# Filter, transform as needed
valid = [item for item in all_items if item["json"].get("status") == "active"]

processed = []
for item in valid:
    processed.append({
        "json": {
            "id": item["json"]["id"],
            "name": item["json"]["name"]
        }
    })

return processed
```

### Pattern 2: _input.first() - Very Common

**Use when**: Working with single objects, API responses

```python
# Get first item only
first_item = _input.first()
data = first_item["json"]

return [{
    "json": {
        "result": process_data(data),
        "processed_at": datetime.now().isoformat()
    }
}]
```

### Pattern 3: _input.item - Each Item Mode Only

**Use when**: In "Run Once for Each Item" mode

```python
# Current item in loop (Each Item mode only)
current_item = _input.item

return [{
    "json": {
        **current_item["json"],
        "item_processed": True
    }
}]
```

### Pattern 4: _node - Reference Other Nodes

**Use when**: Need data from specific nodes in workflow

```python
# Get output from specific node
webhook_data = _node["Webhook"]["json"]
http_data = _node["HTTP Request"]["json"]

return [{
    "json": {
        "combined": {
            "webhook": webhook_data,
            "api": http_data
        }
    }
}]
```

**See**: DATA_ACCESS.md for comprehensive guide

---

## Critical: Webhook Data Structure

**MOST COMMON MISTAKE**: Webhook data is nested under `["body"]`

```python
# ❌ WRONG - Will raise KeyError
name = _json["name"]
email = _json["email"]

# ✅ CORRECT - Webhook data is under ["body"]
name = _json["body"]["name"]
email = _json["body"]["email"]

# ✅ SAFER - Use .get() for safe access
webhook_data = _json.get("body", {})
name = webhook_data.get("name")
```

**Why**: Webhook node wraps all request data under `body` property. This includes POST data, query parameters, and JSON payloads.

**See**: DATA_ACCESS.md for full webhook structure details

---

## Return Format Requirements

**CRITICAL RULE**: Always return list of dictionaries with `"json"` key

### Correct Return Formats

```python
# ✅ Single result
return [{
    "json": {
        "field1": value1,
        "field2": value2
    }
}]

# ✅ Multiple results
return [
    {"json": {"id": 1, "data": "first"}},
    {"json": {"id": 2, "data": "second"}}
]

# ✅ List comprehension
transformed = [
    {"json": {"id": item["json"]["id"], "processed": True}}
    for item in _input.all()
    if item["json"].get("valid")
]
return transformed

# ✅ Empty result (when no data to return)
return []

# ✅ Conditional return
if should_process:
    return [{"json": processed_data}]
else:
    return []
```

### Incorrect Return Formats

```python
# ❌ WRONG: Dictionary without list wrapper
return {
    "json": {"field": value}
}

# ❌ WRONG: List without json wrapper
return [{"field": value}]

# ❌ WRONG: Plain string
return "processed"

# ❌ WRONG: Incomplete structure
return [{"data": value}]  # Should be {"json": value}
```

**Why it matters**: Next nodes expect list format. Incorrect format causes workflow execution to fail.

**See**: ERROR_PATTERNS.md #2 for detailed error solutions

---

## Critical Limitation: No External Libraries

**MOST IMPORTANT PYTHON LIMITATION**: Cannot import external packages on default installs.

> **Self-hosted exception**: external package availability depends entirely on the instance's Python runner configuration. If the user states their self-hosted instance has specific packages available in the Python runner environment, use them — don't refuse. When unsure, ask or write standard-library-only code.

### What's NOT Available

```python
# ❌ NOT AVAILABLE - Will raise ModuleNotFoundError
import requests  # ❌ No
import pandas  # ❌ No
import numpy  # ❌ No
import scipy  # ❌ No
from bs4 import BeautifulSoup  # ❌ No
import lxml  # ❌ No
```

### What IS Available (Standard Library)

```python
# ✅ AVAILABLE - Standard library only
import json  # ✅ JSON parsing
import datetime  # ✅ Date/time operations
import re  # ✅ Regular expressions
import base64  # ✅ Base64 encoding/decoding
import hashlib  # ✅ Hashing functions
import urllib.parse  # ✅ URL parsing
import math  # ✅ Math functions
import random  # ✅ Random numbers
import statistics  # ✅ Statistical functions
```

### Workarounds

**Need HTTP requests?**
- ✅ Use **HTTP Request node** before Code node
- ✅ Or switch to **JavaScript** and use `$helpers.httpRequest()`

**Need data analysis (pandas/numpy)?**
- ✅ Use Python **statistics** module for basic stats
- ✅ Or switch to **JavaScript** for most operations
- ✅ Manual calculations with lists and dictionaries

**Need web scraping (BeautifulSoup)?**
- ✅ Use **HTTP Request node** + **HTML Extract node**
- ✅ Or switch to **JavaScript** with regex/string methods

**See**: STANDARD_LIBRARY.md for complete reference

---

## Common Patterns Overview

Based on production workflows, here are the most useful Python patterns:

### 1. Data Transformation
Transform all items with list comprehensions

```python
items = _input.all()

return [
    {
        "json": {
            "id": item["json"].get("id"),
            "name": item["json"].get("name", "Unknown").upper(),
            "processed": True
        }
    }
    for item in items
]
```

### 2. Filtering & Aggregation
Sum, filter, count with built-in functions

```python
items = _input.all()
total = sum(item["json"].get("amount", 0) for item in items)
valid_items = [item for item in items if item["json"].get("amount", 0) > 0]

return [{
    "json": {
        "total": total,
        "count": len(valid_items)
    }
}]
```

### 3. String Processing with Regex
Extract patterns from text

```python
import re

items = _input.all()
email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

all_emails = []
for item in items:
    text = item["json"].get("text", "")
    emails = re.findall(email_pattern, text)
    all_emails.extend(emails)

# Remove duplicates
unique_emails = list(set(all_emails))

return [{
    "json": {
        "emails": unique_emails,
        "count": len(unique_emails)
    }
}]
```

### 4. Data Validation
Validate and clean data

```python
items = _input.all()
validated = []

for item in items:
    data = item["json"]
    errors = []

    # Validate fields
    if not data.get("email"):
        errors.append("Email required")
    if not data.get("name"):
        errors.append("Name required")

    validated.append({
        "json": {
            **data,
            "valid": len(errors) == 0,
            "errors": errors if errors else None
        }
    })

return validated
```

### 5. Statistical Analysis
Calculate statistics with statistics module

```python
from statistics import mean, median, stdev

items = _input.all()
values = [item["json"].get("value", 0) for item in items if "value" in item["json"]]

if values:
    return [{
        "json": {
            "mean": mean(values),
            "median": median(values),
            "stdev": stdev(values) if len(values) > 1 else 0,
            "min": min(values),
            "max": max(values),
            "count": len(values)
        }
    }]
else:
    return [{"json": {"error": "No values found"}}]
```

**See**: COMMON_PATTERNS.md for 10 detailed Python patterns

---

## Error Prevention - Top 5 Mistakes

### #1: Importing External Libraries (Python-Specific!)

```python
# ❌ WRONG: Trying to import external library
import requests  # ModuleNotFoundError!

# ✅ CORRECT: Use HTTP Request node or JavaScript
# Add HTTP Request node before Code node
# OR switch to JavaScript and use $helpers.httpRequest()
```

### #2: Empty Code or Missing Return

```python
# ❌ WRONG: No return statement
items = _input.all()
# Processing...
# Forgot to return!

# ✅ CORRECT: Always return data
items = _input.all()
# Processing...
return [{"json": item["json"]} for item in items]
```

### #3: Incorrect Return Format

```python
# ❌ WRONG: Returning dict instead of list
return {"json": {"result": "success"}}

# ✅ CORRECT: List wrapper required
return [{"json": {"result": "success"}}]
```

### #4: KeyError on Dictionary Access

```python
# ❌ WRONG: Direct access crashes if missing
name = _json["user"]["name"]  # KeyError!

# ✅ CORRECT: Use .get() for safe access
name = _json.get("user", {}).get("name", "Unknown")
```

### #5: Webhook Body Nesting

```python
# ❌ WRONG: Direct access to webhook data
email = _json["email"]  # KeyError!

# ✅ CORRECT: Webhook data under ["body"]
email = _json["body"]["email"]

# ✅ BETTER: Safe access with .get()
email = _json.get("body", {}).get("email", "no-email")
```

**See**: ERROR_PATTERNS.md for comprehensive error guide

---

## Standard Library Reference

### Most Useful Modules

```python
# JSON operations
import json
data = json.loads(json_string)
json_output = json.dumps({"key": "value"})

# Date/time
from datetime import datetime, timedelta
now = datetime.now()
tomorrow = now + timedelta(days=1)
formatted = now.strftime("%Y-%m-%d")

# Regular expressions
import re
matches = re.findall(r'\d+', text)
cleaned = re.sub(r'[^\w\s]', '', text)

# Base64 encoding
import base64
encoded = base64.b64encode(data).decode()
decoded = base64.b64decode(encoded)

# Hashing
import hashlib
hash_value = hashlib.sha256(text.encode()).hexdigest()

# URL parsing
import urllib.parse
params = urllib.parse.urlencode({"key": "value"})
parsed = urllib.parse.urlparse(url)

# Statistics
from statistics import mean, median, stdev
average = mean([1, 2, 3, 4, 5])
```

**See**: STANDARD_LIBRARY.md for complete reference

---

## Best Practices

### 1. Always Use .get() for Dictionary Access

```python
# ✅ SAFE: Won't crash if field missing
value = item["json"].get("field", "default")

# ❌ RISKY: Crashes if field doesn't exist
value = item["json"]["field"]
```

### 2. Handle None/Null Values Explicitly

```python
# ✅ GOOD: Default to 0 if None
amount = item["json"].get("amount") or 0

# ✅ GOOD: Check for None explicitly
text = item["json"].get("text")
if text is None:
    text = ""
```

### 3. Use List Comprehensions for Filtering

```python
# ✅ PYTHONIC: List comprehension
valid = [item for item in items if item["json"].get("active")]

# ❌ VERBOSE: Manual loop
valid = []
for item in items:
    if item["json"].get("active"):
        valid.append(item)
```

### 4. Return Consistent Structure

```python
# ✅ CONSISTENT: Always list with "json" key
return [{"json": result}]  # Single result
return results  # Multiple results (already formatted)
return []  # No results
```

### 5. Debug with print() Statements

```python
# Debug statements appear in browser console (F12)
items = _input.all()
print(f"Processing {len(items)} items")
print(f"First item: {items[0] if items else 'None'}")
```

---

## Production Gotchas

### SplitInBatches Loop Semantics

The SplitInBatches node has two outputs:
- `main[0]` = **done** — fires ONCE after all batches complete
- `main[1]` = **each batch** — fires for every batch (the loop body)

Always add a **Limit 1** node after the done output.

### Correct Node Reference Syntax

```python
# ❌ WRONG
data = _node['HTTP Request']['json']

# ✅ CORRECT - call .first() then access json
data = _node['HTTP Request'].first()['json']
```

### Cross-Iteration Data Not Available in Python

`$getWorkflowStaticData('global')` may not be available in Python Beta mode. If you need to accumulate data across SplitInBatches iterations, use a JavaScript Code node for the accumulation logic instead.

---

## When to Use Python vs JavaScript

### Use Python When:
- ✅ You need `statistics` module for statistical operations
- ✅ You're significantly more comfortable with Python syntax
- ✅ Your logic maps well to list comprehensions
- ✅ You need specific standard library functions

### Use JavaScript When:
- ✅ You need HTTP requests ($helpers.httpRequest())
- ✅ You need advanced date/time (DateTime/Luxon)
- ✅ You want better n8n integration
- ✅ **For 95% of use cases** (recommended)

### Consider Other Nodes When:
- ❌ Simple field mapping → Use **Set** node
- ❌ Basic filtering → Use **Filter** node
- ❌ Simple conditionals → Use **IF** or **Switch** node
- ❌ HTTP requests only → Use **HTTP Request** node

---

## Integration with Other Skills

### Works With:

**n8n Expression Syntax**:
- Expressions use `{{ }}` syntax in other nodes
- Code nodes use Python directly (no `{{ }}`)
- When to use expressions vs code

**n8n MCP Tools Expert**:
- How to find Code node: `search_nodes({query: "code"})`
- Get configuration help: `get_node({nodeType: "nodes-base.code"})`
- Validate code: `validate_node({nodeType: "nodes-base.code", config: {...}})`

**n8n Node Configuration**:
- Mode selection (All Items vs Each Item)
- Language selection (Python vs JavaScript)
- Understanding property dependencies

**n8n Workflow Patterns**:
- Code nodes in transformation step
- When to use Python vs JavaScript in patterns

**n8n Validation Expert**:
- Validate Code node configuration
- Handle validation errors
- Auto-fix common issues

**n8n Code JavaScript**:
- When to use JavaScript instead
- Comparison of JavaScript vs Python features
- Migration from Python to JavaScript

---

## Quick Reference Checklist

Before deploying Python Code nodes, verify:

- [ ] **Considered JavaScript first** - Using Python only when necessary
- [ ] **Code is not empty** - Must have meaningful logic
- [ ] **Return statement exists** - Must return list of dictionaries
- [ ] **Proper return format** - Each item: `{"json": {...}}`
- [ ] **Data access correct** - Using `_input.all()`, `_input.first()`, or `_input.item`
- [ ] **No external imports** - Only standard library (json, datetime, re, etc.)
- [ ] **Safe dictionary access** - Using `.get()` to avoid KeyError
- [ ] **Webhook data** - Access via `["body"]` if from webhook
- [ ] **Mode selection** - "All Items" for most cases
- [ ] **Output consistent** - All code paths return same structure

---

## Additional Resources

### Related Files
- DATA_ACCESS.md - Comprehensive Python data access patterns
- COMMON_PATTERNS.md - 10 Python patterns for n8n
- ERROR_PATTERNS.md - Top 5 errors and solutions
- STANDARD_LIBRARY.md - Complete standard library reference

### n8n Documentation
- Code Node Guide: https://docs.n8n.io/code/code-node/
- Python in n8n: https://docs.n8n.io/code/builtin/python-modules/

---

**Ready to write Python in n8n Code nodes - but consider JavaScript first!** Use Python for specific needs, reference the error patterns guide to avoid common mistakes, and leverage the standard library effectively.


---

# Data Access Patterns - Python Code Node

Complete guide to accessing data in n8n Code nodes using Python.

---

## Overview

In n8n Python Code nodes, you access data using **underscore-prefixed** variables: `_input`, `_json`, `_node`.

**Data Access Priority** (by common usage):
1. **`_input.all()`** - Most common - Batch operations, aggregations
2. **`_input.first()`** - Very common - Single item operations
3. **`_input.item`** - Common - Each Item mode only
4. **`_node["NodeName"]["json"]`** - Specific node references
5. **`_json`** - Direct current item (use `_input` instead)

**Python vs JavaScript**:
| JavaScript | Python (Beta) | Python (Native) |
|------------|---------------|-----------------|
| `$input.all()` | `_input.all()` | `_items` |
| `$input.first()` | `_input.first()` | `_items[0]` |
| `$input.item` | `_input.item` | `_item` |
| `$json` | `_json` | `_item["json"]` |
| `$node["Name"]` | `_node["Name"]` | Not available |

---

## Pattern 1: _input.all() - Process All Items

**Usage**: Most common pattern for batch processing

**When to use:**
- Processing multiple records
- Aggregating data (sum, count, average)
- Filtering lists
- Transforming datasets

### Basic Usage

```python
# Get all items from previous node
all_items = _input.all()

# all_items is a list of dictionaries like:
# [
#   {"json": {"id": 1, "name": "Alice"}},
#   {"json": {"id": 2, "name": "Bob"}}
# ]

print(f"Received {len(all_items)} items")

return all_items
```

### Example 1: Filter Active Items

```python
all_items = _input.all()

# Filter only active items
active_items = [
    item for item in all_items
    if item["json"].get("status") == "active"
]

return active_items
```

### Example 2: Transform All Items

```python
all_items = _input.all()

# Transform to new structure
transformed = []
for item in all_items:
    transformed.append({
        "json": {
            "id": item["json"].get("id"),
            "full_name": f"{item['json'].get('first_name', '')} {item['json'].get('last_name', '')}",
            "email": item["json"].get("email"),
            "processed_at": datetime.now().isoformat()
        }
    })

return transformed
```

### Example 3: Aggregate Data

```python
all_items = _input.all()

# Calculate total
total = sum(item["json"].get("amount", 0) for item in all_items)

return [{
    "json": {
        "total": total,
        "count": len(all_items),
        "average": total / len(all_items) if all_items else 0
    }
}]
```

### Example 4: Sort and Limit

```python
all_items = _input.all()

# Get top 5 by score
sorted_items = sorted(
    all_items,
    key=lambda item: item["json"].get("score", 0),
    reverse=True
)
top_five = sorted_items[:5]

return [{"json": item["json"]} for item in top_five]
```

### Example 5: Group By Category

```python
all_items = _input.all()

# Group items by category
grouped = {}
for item in all_items:
    category = item["json"].get("category", "Uncategorized")

    if category not in grouped:
        grouped[category] = []

    grouped[category].append(item["json"])

# Convert to list format
return [
    {
        "json": {
            "category": category,
            "items": items,
            "count": len(items)
        }
    }
    for category, items in grouped.items()
]
```

### Example 6: Deduplicate by ID

```python
all_items = _input.all()

# Remove duplicates by ID
seen = set()
unique = []

for item in all_items:
    item_id = item["json"].get("id")

    if item_id and item_id not in seen:
        seen.add(item_id)
        unique.append(item)

return unique
```

---

## Pattern 2: _input.first() - Get First Item

**Usage**: Very common for single-item operations

**When to use:**
- Previous node returns single object
- Working with API responses
- Getting initial/first data point

### Basic Usage

```python
# Get first item from previous node
first_item = _input.first()

# Access the JSON data
data = first_item["json"]

print(f"First item: {data}")

return [{"json": data}]
```

### Example 1: Process Single API Response

```python
# Get API response (typically single object)
response = _input.first()["json"]

# Extract what you need
return [{
    "json": {
        "user_id": response.get("data", {}).get("user", {}).get("id"),
        "user_name": response.get("data", {}).get("user", {}).get("name"),
        "status": response.get("status"),
        "fetched_at": datetime.now().isoformat()
    }
}]
```

### Example 2: Transform Single Object

```python
data = _input.first()["json"]

# Transform structure
return [{
    "json": {
        "id": data.get("id"),
        "contact": {
            "email": data.get("email"),
            "phone": data.get("phone")
        },
        "address": {
            "street": data.get("street"),
            "city": data.get("city"),
            "zip": data.get("zip")
        }
    }
}]
```

### Example 3: Validate Single Item

```python
item = _input.first()["json"]

# Validation logic
is_valid = bool(item.get("email") and "@" in item.get("email", ""))

return [{
    "json": {
        **item,
        "valid": is_valid,
        "validated_at": datetime.now().isoformat()
    }
}]
```

### Example 4: Extract Nested Data

```python
response = _input.first()["json"]

# Navigate nested structure
users = response.get("data", {}).get("users", [])

return [
    {
        "json": {
            "id": user.get("id"),
            "name": user.get("profile", {}).get("name", "Unknown"),
            "email": user.get("contact", {}).get("email", "no-email")
        }
    }
    for user in users
]
```

---

## Pattern 3: _input.item - Current Item (Each Item Mode)

**Usage**: Common in "Run Once for Each Item" mode

**When to use:**
- Mode is set to "Run Once for Each Item"
- Need to process items independently
- Per-item API calls or validations

**IMPORTANT**: Only use in "Each Item" mode. Will be undefined in "All Items" mode.

### Basic Usage

```python
# In "Run Once for Each Item" mode
current_item = _input.item
data = current_item["json"]

print(f"Processing item: {data.get('id')}")

return [{
    "json": {
        **data,
        "processed": True
    }
}]
```

### Example 1: Add Processing Metadata

```python
item = _input.item

return [{
    "json": {
        **item["json"],
        "processed": True,
        "processed_at": datetime.now().isoformat(),
        "processing_duration": random.random() * 1000  # Simulated
    }
}]
```

### Example 2: Per-Item Validation

```python
item = _input.item
data = item["json"]

# Validate this specific item
errors = []

if not data.get("email"):
    errors.append("Email required")
if not data.get("name"):
    errors.append("Name required")
if data.get("age") and data["age"] < 18:
    errors.append("Must be 18+")

return [{
    "json": {
        **data,
        "valid": len(errors) == 0,
        "errors": errors if errors else None
    }
}]
```

### Example 3: Conditional Processing

```python
item = _input.item
data = item["json"]

# Process based on item type
if data.get("type") == "premium":
    return [{
        "json": {
            **data,
            "discount": 0.20,
            "tier": "premium"
        }
    }]
else:
    return [{
        "json": {
            **data,
            "discount": 0.05,
            "tier": "standard"
        }
    }]
```

---

## Pattern 4: _node - Reference Other Nodes

**Usage**: Less common, but powerful for specific scenarios

**When to use:**
- Need data from specific named node
- Combining data from multiple nodes

### Basic Usage

```python
# Get output from specific node
webhook_data = _node["Webhook"]["json"]
api_data = _node["HTTP Request"]["json"]

return [{
    "json": {
        "from_webhook": webhook_data,
        "from_api": api_data
    }
}]
```

### Example 1: Combine Multiple Sources

```python
# Reference multiple nodes
webhook = _node["Webhook"]["json"]
database = _node["Postgres"]["json"]
api = _node["HTTP Request"]["json"]

return [{
    "json": {
        "combined": {
            "webhook": webhook.get("body", {}),
            "db_records": len(database) if isinstance(database, list) else 1,
            "api_response": api.get("status")
        },
        "processed_at": datetime.now().isoformat()
    }
}]
```

### Example 2: Compare Across Nodes

```python
old_data = _node["Get Old Data"]["json"]
new_data = _node["Get New Data"]["json"]

# Simple comparison
changes = {
    "added": [n for n in new_data if n.get("id") not in [o.get("id") for o in old_data]],
    "removed": [o for o in old_data if o.get("id") not in [n.get("id") for n in new_data]]
}

return [{
    "json": {
        "changes": changes,
        "summary": {
            "added": len(changes["added"]),
            "removed": len(changes["removed"])
        }
    }
}]
```

---

## Critical: Webhook Data Structure

**MOST COMMON MISTAKE**: Forgetting webhook data is nested under `["body"]`

### The Problem

Webhook node wraps all incoming data under a `"body"` property.

### Structure

```python
# Webhook node output structure:
{
    "headers": {
        "content-type": "application/json",
        "user-agent": "..."
    },
    "params": {},
    "query": {},
    "body": {
        # ← YOUR DATA IS HERE
        "name": "Alice",
        "email": "alice@example.com",
        "message": "Hello!"
    }
}
```

### Wrong vs Right

```python
# ❌ WRONG: Trying to access directly
name = _json["name"]  # KeyError!
email = _json["email"]  # KeyError!

# ✅ CORRECT: Access via ["body"]
name = _json["body"]["name"]  # "Alice"
email = _json["body"]["email"]  # "alice@example.com"

# ✅ SAFER: Use .get() for safe access
webhook_data = _json.get("body", {})
name = webhook_data.get("name")  # None if missing
email = webhook_data.get("email", "no-email")  # Default value
```

### Example: Full Webhook Processing

```python
# Get webhook data from previous node
webhook_output = _input.first()["json"]

# Access the actual payload
payload = webhook_output.get("body", {})

# Access headers if needed
content_type = webhook_output.get("headers", {}).get("content-type")

# Access query parameters if needed
api_key = webhook_output.get("query", {}).get("api_key")

# Process the actual data
return [{
    "json": {
        # Data from webhook body
        "user_name": payload.get("name"),
        "user_email": payload.get("email"),
        "message": payload.get("message"),

        # Metadata
        "received_at": datetime.now().isoformat(),
        "content_type": content_type,
        "authenticated": bool(api_key)
    }
}]
```

### POST Data, Query Params, and Headers

```python
webhook = _input.first()["json"]

return [{
    "json": {
        # POST body data
        "form_data": webhook.get("body", {}),

        # Query parameters (?key=value)
        "query_params": webhook.get("query", {}),

        # HTTP headers
        "user_agent": webhook.get("headers", {}).get("user-agent"),
        "content_type": webhook.get("headers", {}).get("content-type"),

        # Request metadata
        "method": webhook.get("method"),  # POST, GET, etc.
        "url": webhook.get("url")
    }
}]
```

---

## Choosing the Right Pattern

### Decision Tree

```
Do you need ALL items from previous node?
├─ YES → Use _input.all()
│
└─ NO → Do you need just the FIRST item?
    ├─ YES → Use _input.first()
    │
    └─ NO → Are you in "Each Item" mode?
        ├─ YES → Use _input.item
        │
        └─ NO → Do you need specific node data?
            ├─ YES → Use _node["NodeName"]
            └─ NO → Use _input.first() (default)
```

### Quick Reference Table

| Scenario | Use This | Example |
|----------|----------|---------|
| Sum all amounts | `_input.all()` | `sum(i["json"].get("amount", 0) for i in items)` |
| Get API response | `_input.first()` | `_input.first()["json"].get("data")` |
| Process each independently | `_input.item` | `_input.item["json"]` (Each Item mode) |
| Combine two nodes | `_node["Name"]` | `_node["API"]["json"]` |
| Filter list | `_input.all()` | `[i for i in items if i["json"].get("active")]` |
| Transform single object | `_input.first()` | `{**_input.first()["json"], "new": True}` |
| Webhook data | `_input.first()` | `_input.first()["json"]["body"]` |

---

## Common Mistakes

### Mistake 1: Using _json Without Context

```python
# ❌ RISKY: _json is ambiguous
value = _json["field"]

# ✅ CLEAR: Be explicit
value = _input.first()["json"]["field"]
```

### Mistake 2: Forgetting ["json"] Property

```python
# ❌ WRONG: Trying to access fields on item dictionary
items = _input.all()
names = [item["name"] for item in items]  # KeyError!

# ✅ CORRECT: Access via ["json"]
names = [item["json"]["name"] for item in items]
```

### Mistake 3: Using _input.item in All Items Mode

```python
# ❌ WRONG: _input.item is None in "All Items" mode
data = _input.item["json"]  # AttributeError!

# ✅ CORRECT: Use appropriate method
data = _input.first()["json"]  # Or _input.all()
```

### Mistake 4: Not Handling Empty Lists

```python
# ❌ WRONG: Crashes if no items
first = _input.all()[0]["json"]  # IndexError!

# ✅ CORRECT: Check length first
items = _input.all()
if items:
    first = items[0]["json"]
else:
    return []

# ✅ ALSO CORRECT: Use _input.first()
first = _input.first()["json"]  # Built-in safety
```

### Mistake 5: Direct Dictionary Access (KeyError)

```python
# ❌ RISKY: Crashes if key missing
value = item["json"]["field"]  # KeyError!

# ✅ SAFE: Use .get()
value = item["json"].get("field", "default")
```

---

## Advanced Patterns

### Pattern: Safe Nested Access

```python
# Deep nested access with .get()
value = (
    _input.first()["json"]
    .get("level1", {})
    .get("level2", {})
    .get("level3", "default")
)
```

### Pattern: List Comprehension with Filtering

```python
items = _input.all()

# Filter and transform in one step
result = [
    {
        "json": {
            "id": item["json"]["id"],
            "name": item["json"]["name"].upper()
        }
    }
    for item in items
    if item["json"].get("active") and item["json"].get("verified")
]

return result
```

### Pattern: Dictionary Comprehension

```python
items = _input.all()

# Create lookup dictionary
lookup = {
    item["json"]["id"]: item["json"]
    for item in items
    if "id" in item["json"]
}

return [{"json": lookup}]
```

---

## Summary

**Most Common Patterns**:
1. `_input.all()` - Process multiple items, batch operations
2. `_input.first()` - Single item, API responses
3. `_input.item` - Each Item mode processing

**Critical Rule**:
- Webhook data is under `["body"]` property

**Best Practice**:
- Use `.get()` for dictionary access to avoid KeyError
- Always check for empty lists
- Be explicit: Use `_input.first()["json"]["field"]` instead of `_json["field"]`

**See Also**:
- SKILL.md - Overview and quick start
- COMMON_PATTERNS.md - Python-specific patterns
- ERROR_PATTERNS.md - Avoid common mistakes


---

# Standard Library Reference - Python Code Node

Complete guide to available Python standard library modules in n8n Code nodes.

---

## ⚠️ Critical Limitation

**NO EXTERNAL LIBRARIES AVAILABLE**

Python Code nodes in n8n have **ONLY** the Python standard library. No pip packages.

```python
# ❌ NOT AVAILABLE - Will cause ModuleNotFoundError
import requests      # No HTTP library!
import pandas        # No data analysis!
import numpy         # No numerical computing!
import bs4          # No web scraping!
import selenium     # No browser automation!
import psycopg2     # No database drivers!
import pymongo      # No MongoDB!
import sqlalchemy   # No ORMs!

# ✅ AVAILABLE - Standard library only
import json
import datetime
import re
import base64
import hashlib
import urllib.parse
import urllib.request
import math
import random
import statistics
```

**Recommendation**: Use **JavaScript** for 95% of use cases. JavaScript has more capabilities in n8n.

---

## Available Modules

### Priority 1: Most Useful (Use These)

1. **json** - JSON parsing and generation
2. **datetime** - Date and time operations
3. **re** - Regular expressions
4. **base64** - Base64 encoding/decoding
5. **hashlib** - Hashing (MD5, SHA256, etc.)
6. **urllib.parse** - URL parsing and encoding

### Priority 2: Moderately Useful

7. **math** - Mathematical functions
8. **random** - Random number generation
9. **statistics** - Statistical functions
10. **collections** - Specialized data structures

### Priority 3: Occasionally Useful

11. **itertools** - Iterator tools
12. **functools** - Higher-order functions
13. **operator** - Standard operators as functions
14. **string** - String constants and templates
15. **textwrap** - Text wrapping utilities

---

## Module 1: json - JSON Operations

**Most common module** - Parse and generate JSON data.

### Parse JSON String

```python
import json

# Parse JSON string to Python dict
json_string = '{"name": "Alice", "age": 30}'
data = json.loads(json_string)

return [{
    "json": {
        "name": data["name"],
        "age": data["age"],
        "parsed": True
    }
}]
```

### Generate JSON String

```python
import json

# Convert Python dict to JSON string
data = {
    "users": [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"}
    ],
    "total": 2
}

json_string = json.dumps(data, indent=2)

return [{
    "json": {
        "json_output": json_string,
        "length": len(json_string)
    }
}]
```

### Handle JSON Errors

```python
import json

webhook_data = _input.first()["json"]["body"]
json_string = webhook_data.get("data", "")

try:
    parsed = json.loads(json_string)
    status = "valid"
    error = None
except json.JSONDecodeError as e:
    parsed = None
    status = "invalid"
    error = str(e)

return [{
    "json": {
        "status": status,
        "data": parsed,
        "error": error
    }
}]
```

### Pretty Print JSON

```python
import json

# Format JSON with indentation
data = _input.first()["json"]

pretty_json = json.dumps(data, indent=2, sort_keys=True)

return [{
    "json": {
        "formatted": pretty_json
    }
}]
```

---

## Module 2: datetime - Date and Time

**Very common** - Date parsing, formatting, calculations.

### Current Date and Time

```python
from datetime import datetime

now = datetime.now()

return [{
    "json": {
        "timestamp": now.isoformat(),
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "formatted": now.strftime("%B %d, %Y at %I:%M %p")
    }
}]
```

### Parse Date String

```python
from datetime import datetime

date_string = "2025-01-15T14:30:00"
dt = datetime.fromisoformat(date_string)

return [{
    "json": {
        "year": dt.year,
        "month": dt.month,
        "day": dt.day,
        "hour": dt.hour,
        "weekday": dt.strftime("%A")
    }
}]
```

### Date Calculations

```python
from datetime import datetime, timedelta

now = datetime.now()

# Calculate future/past dates
tomorrow = now + timedelta(days=1)
yesterday = now - timedelta(days=1)
next_week = now + timedelta(weeks=1)
one_hour_ago = now - timedelta(hours=1)

return [{
    "json": {
        "now": now.isoformat(),
        "tomorrow": tomorrow.isoformat(),
        "yesterday": yesterday.isoformat(),
        "next_week": next_week.isoformat(),
        "one_hour_ago": one_hour_ago.isoformat()
    }
}]
```

### Compare Dates

```python
from datetime import datetime

date1 = datetime(2025, 1, 15)
date2 = datetime(2025, 1, 20)

# Calculate difference
diff = date2 - date1

return [{
    "json": {
        "days_difference": diff.days,
        "seconds_difference": diff.total_seconds(),
        "date1_is_earlier": date1 < date2,
        "date2_is_later": date2 > date1
    }
}]
```

### Format Dates

```python
from datetime import datetime

dt = datetime.now()

return [{
    "json": {
        "iso": dt.isoformat(),
        "us_format": dt.strftime("%m/%d/%Y"),
        "eu_format": dt.strftime("%d/%m/%Y"),
        "long_format": dt.strftime("%A, %B %d, %Y"),
        "time_12h": dt.strftime("%I:%M %p"),
        "time_24h": dt.strftime("%H:%M:%S")
    }
}]
```

---

## Module 3: re - Regular Expressions

**Common** - Pattern matching, text extraction, validation.

### Pattern Matching

```python
import re

text = "Email: alice@example.com, Phone: 555-1234"

# Find email
email_match = re.search(r'\b[\w.-]+@[\w.-]+\.\w+\b', text)
email = email_match.group(0) if email_match else None

# Find phone
phone_match = re.search(r'\d{3}-\d{4}', text)
phone = phone_match.group(0) if phone_match else None

return [{
    "json": {
        "email": email,
        "phone": phone
    }
}]
```

### Extract All Matches

```python
import re

text = "Tags: #python #automation #workflow #n8n"

# Find all hashtags
hashtags = re.findall(r'#(\w+)', text)

return [{
    "json": {
        "tags": hashtags,
        "count": len(hashtags)
    }
}]
```

### Replace Patterns

```python
import re

text = "Price: $99.99, Discount: $10.00"

# Remove dollar signs
cleaned = re.sub(r'\$', '', text)

# Replace multiple spaces with single space
normalized = re.sub(r'\s+', ' ', cleaned)

return [{
    "json": {
        "original": text,
        "cleaned": cleaned,
        "normalized": normalized
    }
}]
```

### Validate Format

```python
import re

email = _input.first()["json"]["body"].get("email", "")

# Email validation pattern
email_pattern = r'^[\w.-]+@[\w.-]+\.\w+$'
is_valid = bool(re.match(email_pattern, email))

return [{
    "json": {
        "email": email,
        "valid": is_valid
    }
}]
```

### Split on Pattern

```python
import re

text = "apple,banana;orange|grape"

# Split on multiple delimiters
items = re.split(r'[,;|]', text)

# Clean up whitespace
items = [item.strip() for item in items]

return [{
    "json": {
        "items": items,
        "count": len(items)
    }
}]
```

---

## Module 4: base64 - Encoding/Decoding

**Common** - Encode binary data, API authentication.

### Encode String to Base64

```python
import base64

text = "Hello, World!"

# Encode to base64
encoded_bytes = base64.b64encode(text.encode('utf-8'))
encoded_string = encoded_bytes.decode('utf-8')

return [{
    "json": {
        "original": text,
        "encoded": encoded_string
    }
}]
```

### Decode Base64 to String

```python
import base64

encoded = "SGVsbG8sIFdvcmxkIQ=="

# Decode from base64
decoded_bytes = base64.b64decode(encoded)
decoded_string = decoded_bytes.decode('utf-8')

return [{
    "json": {
        "encoded": encoded,
        "decoded": decoded_string
    }
}]
```

### Basic Auth Header

```python
import base64

username = "admin"
password = "secret123"

# Create Basic Auth header
credentials = f"{username}:{password}"
encoded = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
auth_header = f"Basic {encoded}"

return [{
    "json": {
        "authorization": auth_header
    }
}]
```

---

## Module 5: hashlib - Hashing

**Common** - Generate checksums, hash passwords, create IDs.

### MD5 Hash

```python
import hashlib

text = "Hello, World!"

# Generate MD5 hash
md5_hash = hashlib.md5(text.encode('utf-8')).hexdigest()

return [{
    "json": {
        "original": text,
        "md5": md5_hash
    }
}]
```

### SHA256 Hash

```python
import hashlib

data = _input.first()["json"]["body"]
text = data.get("password", "")

# Generate SHA256 hash (more secure than MD5)
sha256_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()

return [{
    "json": {
        "hashed": sha256_hash
    }
}]
```

### Generate Unique ID

```python
import hashlib
from datetime import datetime

# Create unique ID from multiple values
unique_string = f"{datetime.now().isoformat()}-{_json.get('user_id', 'unknown')}"
unique_id = hashlib.sha256(unique_string.encode('utf-8')).hexdigest()[:16]

return [{
    "json": {
        "id": unique_id,
        "generated_at": datetime.now().isoformat()
    }
}]
```

---

## Module 6: urllib.parse - URL Operations

**Common** - Parse URLs, encode parameters.

### Parse URL

```python
from urllib.parse import urlparse

url = "https://example.com/path?key=value&foo=bar#section"

parsed = urlparse(url)

return [{
    "json": {
        "scheme": parsed.scheme,      # "https"
        "netloc": parsed.netloc,      # "example.com"
        "path": parsed.path,          # "/path"
        "query": parsed.query,        # "key=value&foo=bar"
        "fragment": parsed.fragment    # "section"
    }
}]
```

### URL Encode Parameters

```python
from urllib.parse import urlencode

params = {
    "name": "Alice Smith",
    "email": "alice@example.com",
    "message": "Hello, World!"
}

# Encode parameters for URL
encoded = urlencode(params)

return [{
    "json": {
        "query_string": encoded,
        "full_url": f"https://api.example.com/submit?{encoded}"
    }
}]
```

### Parse Query String

```python
from urllib.parse import parse_qs

query_string = "name=Alice&age=30&tags=python&tags=n8n"

# Parse query string
params = parse_qs(query_string)

return [{
    "json": {
        "name": params.get("name", [""])[0],
        "age": int(params.get("age", ["0"])[0]),
        "tags": params.get("tags", [])
    }
}]
```

### URL Encode/Decode Strings

```python
from urllib.parse import quote, unquote

text = "Hello, World! 你好"

# URL encode
encoded = quote(text)

# URL decode
decoded = unquote(encoded)

return [{
    "json": {
        "original": text,
        "encoded": encoded,
        "decoded": decoded
    }
}]
```

---

## Module 7: math - Mathematical Operations

**Moderately useful** - Advanced math functions.

### Basic Math Functions

```python
import math

number = 16.7

return [{
    "json": {
        "ceiling": math.ceil(number),      # 17
        "floor": math.floor(number),       # 16
        "rounded": round(number),          # 17
        "square_root": math.sqrt(16),      # 4.0
        "power": math.pow(2, 3),          # 8.0
        "absolute": math.fabs(-5.5)       # 5.5
    }
}]
```

### Trigonometry

```python
import math

angle_degrees = 45
angle_radians = math.radians(angle_degrees)

return [{
    "json": {
        "sine": math.sin(angle_radians),
        "cosine": math.cos(angle_radians),
        "tangent": math.tan(angle_radians),
        "pi": math.pi,
        "e": math.e
    }
}]
```

### Logarithms

```python
import math

number = 100

return [{
    "json": {
        "log10": math.log10(number),     # 2.0
        "natural_log": math.log(number), # 4.605...
        "log2": math.log2(number)        # 6.644...
    }
}]
```

---

## Module 8: random - Random Numbers

**Moderately useful** - Generate random data, sampling.

### Random Numbers

```python
import random

return [{
    "json": {
        "random_float": random.random(),           # 0.0 to 1.0
        "random_int": random.randint(1, 100),      # 1 to 100
        "random_range": random.randrange(0, 100, 5) # 0, 5, 10, ..., 95
    }
}]
```

### Random Choice

```python
import random

colors = ["red", "green", "blue", "yellow"]
users = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

return [{
    "json": {
        "random_color": random.choice(colors),
        "random_user": random.choice(users)
    }
}]
```

### Shuffle List

```python
import random

items = [1, 2, 3, 4, 5]
shuffled = items.copy()
random.shuffle(shuffled)

return [{
    "json": {
        "original": items,
        "shuffled": shuffled
    }
}]
```

### Random Sample

```python
import random

items = list(range(1, 101))

# Get 10 random items without replacement
sample = random.sample(items, 10)

return [{
    "json": {
        "sample": sample,
        "count": len(sample)
    }
}]
```

---

## Module 9: statistics - Statistical Functions

**Moderately useful** - Calculate stats from data.

### Basic Statistics

```python
import statistics

numbers = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

return [{
    "json": {
        "mean": statistics.mean(numbers),           # 55.0
        "median": statistics.median(numbers),       # 55.0
        "mode": statistics.mode([1, 2, 2, 3]),     # 2
        "stdev": statistics.stdev(numbers),        # 30.28...
        "variance": statistics.variance(numbers)   # 916.67...
    }
}]
```

### Aggregate from Items

```python
import statistics

all_items = _input.all()

# Extract amounts
amounts = [item["json"].get("amount", 0) for item in all_items]

if amounts:
    return [{
        "json": {
            "count": len(amounts),
            "total": sum(amounts),
            "average": statistics.mean(amounts),
            "median": statistics.median(amounts),
            "min": min(amounts),
            "max": max(amounts),
            "range": max(amounts) - min(amounts)
        }
    }]
else:
    return [{"json": {"error": "No data"}}]
```

---

## Workarounds for Missing Libraries

### HTTP Requests (No requests library)

```python
# ❌ Can't use requests library
# import requests  # ModuleNotFoundError!

# ✅ Use HTTP Request node instead
# Add HTTP Request node BEFORE Code node
# Access the response in Code node

response_data = _input.first()["json"]

return [{
    "json": {
        "status": response_data.get("status"),
        "data": response_data.get("body"),
        "processed": True
    }
}]
```

### Data Processing (No pandas)

```python
# ❌ Can't use pandas
# import pandas as pd  # ModuleNotFoundError!

# ✅ Use Python's built-in list comprehensions
all_items = _input.all()

# Filter
active_items = [
    item for item in all_items
    if item["json"].get("status") == "active"
]

# Group by
from collections import defaultdict
grouped = defaultdict(list)

for item in all_items:
    category = item["json"].get("category", "other")
    grouped[category].append(item["json"])

# Aggregate
import statistics
amounts = [item["json"].get("amount", 0) for item in all_items]
total = sum(amounts)
average = statistics.mean(amounts) if amounts else 0

return [{
    "json": {
        "active_count": len(active_items),
        "grouped": dict(grouped),
        "total": total,
        "average": average
    }
}]
```

### Database Operations (No drivers)

```python
# ❌ Can't use database drivers
# import psycopg2  # ModuleNotFoundError!
# import pymongo   # ModuleNotFoundError!

# ✅ Use n8n database nodes instead
# Add Postgres/MySQL/MongoDB node BEFORE Code node
# Process results in Code node

db_results = _input.first()["json"]

return [{
    "json": {
        "record_count": len(db_results) if isinstance(db_results, list) else 1,
        "processed": True
    }
}]
```

---

## Complete Standard Library List

**Available** (commonly useful):
- json
- datetime, time
- re
- base64
- hashlib
- urllib.parse, urllib.request, urllib.error
- math
- random
- statistics
- collections (defaultdict, Counter, namedtuple)
- itertools
- functools
- operator
- string
- textwrap

**Available** (less common):
- os.path (path operations only)
- copy
- typing
- enum
- decimal
- fractions

**NOT Available** (external libraries):
- requests (HTTP)
- pandas (data analysis)
- numpy (numerical computing)
- bs4/beautifulsoup4 (HTML parsing)
- selenium (browser automation)
- psycopg2, pymongo, sqlalchemy (databases)
- flask, fastapi (web frameworks)
- pillow (image processing)
- openpyxl, xlsxwriter (Excel)

---

## Best Practices

### 1. Use Standard Library When Possible

```python
# ✅ GOOD: Use standard library
import json
import datetime
import re

data = _input.first()["json"]
processed = json.loads(data.get("json_string", "{}"))

return [{"json": processed}]
```

### 2. Fall Back to n8n Nodes

```python
# For operations requiring external libraries,
# use n8n nodes instead:
# - HTTP Request for API calls
# - Postgres/MySQL for databases
# - Extract from File for parsing

# Then process results in Code node
result = _input.first()["json"]
return [{"json": {"processed": result}}]
```

### 3. Combine Multiple Modules

```python
import json
import base64
import hashlib
from datetime import datetime

# Combine modules for complex operations
data = _input.first()["json"]["body"]

# Hash sensitive data
user_id = hashlib.sha256(data.get("email", "").encode()).hexdigest()[:16]

# Encode for storage
encoded_data = base64.b64encode(json.dumps(data).encode()).decode()

return [{
    "json": {
        "user_id": user_id,
        "encoded_data": encoded_data,
        "timestamp": datetime.now().isoformat()
    }
}]
```

---

## Summary

**Most Useful Modules**:
1. json - Parse/generate JSON
2. datetime - Date operations
3. re - Regular expressions
4. base64 - Encoding
5. hashlib - Hashing
6. urllib.parse - URL operations

**Critical Limitation**:
- NO external libraries (requests, pandas, numpy, etc.)

**Recommended Approach**:
- Use **JavaScript** for 95% of use cases
- Use Python only when specifically needed
- Use n8n nodes for operations requiring external libraries

**See Also**:
- SKILL.md - Python Code overview
- DATA_ACCESS.md - Data access patterns
- COMMON_PATTERNS.md - Production patterns
- ERROR_PATTERNS.md - Avoid common mistakes


---

# Common Patterns - Python Code Node

Production-tested Python patterns for n8n Code nodes.

---

## ⚠️ Important: JavaScript First

**Use JavaScript for 95% of use cases.**

Python in n8n has **NO external libraries** (no requests, pandas, numpy).

Only use Python when:
- You have complex Python-specific logic
- You need Python's standard library features
- You're more comfortable with Python than JavaScript

For most workflows, **JavaScript is the better choice**.

---

## Pattern Overview

These 10 patterns cover common n8n Code node scenarios using Python:

1. **Multi-Source Data Aggregation** - Combine data from multiple nodes
2. **Regex-Based Filtering** - Filter items using pattern matching
3. **Markdown to Structured Data** - Parse markdown into structured format
4. **JSON Object Comparison** - Compare two JSON objects for changes
5. **CRM Data Transformation** - Transform CRM data to standard format
6. **Release Notes Processing** - Parse and categorize release notes
7. **Array Transformation** - Reshape arrays and extract fields
8. **Dictionary Lookup** - Create and use lookup dictionaries
9. **Top N Filtering** - Get top items by score/value
10. **String Aggregation** - Aggregate strings with formatting

---

## Pattern 1: Multi-Source Data Aggregation

**Use case**: Combine data from multiple sources (APIs, webhooks, databases).

**Scenario**: Aggregate news articles from multiple sources.

### Implementation

```python
from datetime import datetime

all_items = _input.all()
processed_articles = []

for item in all_items:
    source_name = item["json"].get("name", "Unknown")
    source_data = item["json"]

    # Process Hacker News source
    if source_name == "Hacker News" and source_data.get("hits"):
        for hit in source_data["hits"]:
            processed_articles.append({
                "title": hit.get("title", "No title"),
                "url": hit.get("url", ""),
                "summary": hit.get("story_text") or "No summary",
                "source": "Hacker News",
                "score": hit.get("points", 0),
                "fetched_at": datetime.now().isoformat()
            })

    # Process Reddit source
    elif source_name == "Reddit" and source_data.get("data"):
        for post in source_data["data"].get("children", []):
            post_data = post.get("data", {})
            processed_articles.append({
                "title": post_data.get("title", "No title"),
                "url": post_data.get("url", ""),
                "summary": post_data.get("selftext", "")[:200],
                "source": "Reddit",
                "score": post_data.get("score", 0),
                "fetched_at": datetime.now().isoformat()
            })

# Sort by score descending
processed_articles.sort(key=lambda x: x["score"], reverse=True)

# Return as n8n items
return [{"json": article} for article in processed_articles]
```

### Key Techniques

- Process multiple data sources in one loop
- Normalize different data structures
- Use datetime for timestamps
- Sort by criteria
- Return properly formatted items

---

## Pattern 2: Regex-Based Filtering

**Use case**: Filter items based on pattern matching in text fields.

**Scenario**: Filter support tickets by priority keywords.

### Implementation

```python
import re

all_items = _input.all()
priority_tickets = []

# High priority keywords pattern
high_priority_pattern = re.compile(
    r'\b(urgent|critical|emergency|asap|down|outage|broken)\b',
    re.IGNORECASE
)

for item in all_items:
    ticket = item["json"]

    # Check subject and description
    subject = ticket.get("subject", "")
    description = ticket.get("description", "")
    combined_text = f"{subject} {description}"

    # Find matches
    matches = high_priority_pattern.findall(combined_text)

    if matches:
        priority_tickets.append({
            "json": {
                **ticket,
                "priority": "high",
                "matched_keywords": list(set(matches)),
                "keyword_count": len(matches)
            }
        })
    else:
        priority_tickets.append({
            "json": {
                **ticket,
                "priority": "normal",
                "matched_keywords": [],
                "keyword_count": 0
            }
        })

# Sort by keyword count (most urgent first)
priority_tickets.sort(key=lambda x: x["json"]["keyword_count"], reverse=True)

return priority_tickets
```

### Key Techniques

- Use re.compile() for reusable patterns
- re.IGNORECASE for case-insensitive matching
- Combine multiple text fields for searching
- Extract and deduplicate matches
- Sort by priority indicators

---

## Pattern 3: Markdown to Structured Data

**Use case**: Parse markdown text into structured data.

**Scenario**: Extract tasks from markdown checklist.

### Implementation

```python
import re

markdown_text = _input.first()["json"]["body"].get("markdown", "")

# Parse markdown checklist
tasks = []
lines = markdown_text.split("\n")

for line in lines:
    # Match: - [ ] Task or - [x] Task
    match = re.match(r'^\s*-\s*\[([ x])\]\s*(.+)$', line, re.IGNORECASE)

    if match:
        checked = match.group(1).lower() == 'x'
        task_text = match.group(2).strip()

        # Extract priority if present (e.g., [P1], [HIGH])
        priority_match = re.search(r'\[(P\d|HIGH|MEDIUM|LOW)\]', task_text, re.IGNORECASE)
        priority = priority_match.group(1).upper() if priority_match else "NORMAL"

        # Remove priority tag from text
        clean_text = re.sub(r'\[(P\d|HIGH|MEDIUM|LOW)\]', '', task_text, flags=re.IGNORECASE).strip()

        tasks.append({
            "text": clean_text,
            "completed": checked,
            "priority": priority,
            "original_line": line.strip()
        })

return [{
    "json": {
        "tasks": tasks,
        "total": len(tasks),
        "completed": sum(1 for t in tasks if t["completed"]),
        "pending": sum(1 for t in tasks if not t["completed"])
    }
}]
```

### Key Techniques

- Line-by-line parsing
- Multiple regex patterns for extraction
- Extract metadata from text
- Calculate summary statistics
- Return structured data

---

## Pattern 4: JSON Object Comparison

**Use case**: Compare two JSON objects to find differences.

**Scenario**: Compare old and new user profile data.

### Implementation

```python
import json

all_items = _input.all()

# Assume first item is old data, second is new data
old_data = all_items[0]["json"] if len(all_items) > 0 else {}
new_data = all_items[1]["json"] if len(all_items) > 1 else {}

changes = {
    "added": {},
    "removed": {},
    "modified": {},
    "unchanged": {}
}

# Find all unique keys
all_keys = set(old_data.keys()) | set(new_data.keys())

for key in all_keys:
    old_value = old_data.get(key)
    new_value = new_data.get(key)

    if key not in old_data:
        # Added field
        changes["added"][key] = new_value
    elif key not in new_data:
        # Removed field
        changes["removed"][key] = old_value
    elif old_value != new_value:
        # Modified field
        changes["modified"][key] = {
            "old": old_value,
            "new": new_value
        }
    else:
        # Unchanged field
        changes["unchanged"][key] = old_value

return [{
    "json": {
        "changes": changes,
        "summary": {
            "added_count": len(changes["added"]),
            "removed_count": len(changes["removed"]),
            "modified_count": len(changes["modified"]),
            "unchanged_count": len(changes["unchanged"]),
            "has_changes": len(changes["added"]) > 0 or len(changes["removed"]) > 0 or len(changes["modified"]) > 0
        }
    }
}]
```

### Key Techniques

- Set operations for key comparison
- Dictionary .get() for safe access
- Categorize changes by type
- Create summary statistics
- Return detailed comparison

---

## Pattern 5: CRM Data Transformation

**Use case**: Transform CRM data to standard format.

**Scenario**: Normalize data from different CRM systems.

### Implementation

```python
from datetime import datetime
import re

all_items = _input.all()
normalized_contacts = []

for item in all_items:
    raw_contact = item["json"]
    source = raw_contact.get("source", "unknown")

    # Normalize email
    email = raw_contact.get("email", "").lower().strip()

    # Normalize phone (remove non-digits)
    phone_raw = raw_contact.get("phone", "")
    phone = re.sub(r'\D', '', phone_raw)

    # Parse name
    if "full_name" in raw_contact:
        name_parts = raw_contact["full_name"].split(" ", 1)
        first_name = name_parts[0] if len(name_parts) > 0 else ""
        last_name = name_parts[1] if len(name_parts) > 1 else ""
    else:
        first_name = raw_contact.get("first_name", "")
        last_name = raw_contact.get("last_name", "")

    # Normalize status
    status_raw = raw_contact.get("status", "").lower()
    status = "active" if status_raw in ["active", "enabled", "true", "1"] else "inactive"

    # Create normalized contact
    normalized_contacts.append({
        "json": {
            "id": raw_contact.get("id", ""),
            "first_name": first_name.strip(),
            "last_name": last_name.strip(),
            "full_name": f"{first_name} {last_name}".strip(),
            "email": email,
            "phone": phone,
            "status": status,
            "source": source,
            "normalized_at": datetime.now().isoformat(),
            "original_data": raw_contact
        }
    })

return normalized_contacts
```

### Key Techniques

- Multiple field name variations handling
- String cleaning and normalization
- Regex for phone number cleaning
- Name parsing logic
- Status normalization
- Preserve original data

---

## Pattern 6: Release Notes Processing

**Use case**: Parse release notes and categorize changes.

**Scenario**: Extract features, fixes, and breaking changes from release notes.

### Implementation

```python
import re

release_notes = _input.first()["json"]["body"].get("notes", "")

categories = {
    "features": [],
    "fixes": [],
    "breaking": [],
    "other": []
}

# Split into lines
lines = release_notes.split("\n")

for line in lines:
    line = line.strip()

    # Skip empty lines and headers
    if not line or line.startswith("#"):
        continue

    # Remove bullet points
    clean_line = re.sub(r'^[\*\-\+]\s*', '', line)

    # Categorize
    if re.search(r'\b(feature|add|new)\b', clean_line, re.IGNORECASE):
        categories["features"].append(clean_line)
    elif re.search(r'\b(fix|bug|patch|resolve)\b', clean_line, re.IGNORECASE):
        categories["fixes"].append(clean_line)
    elif re.search(r'\b(breaking|deprecated|remove)\b', clean_line, re.IGNORECASE):
        categories["breaking"].append(clean_line)
    else:
        categories["other"].append(clean_line)

return [{
    "json": {
        "categories": categories,
        "summary": {
            "features": len(categories["features"]),
            "fixes": len(categories["fixes"]),
            "breaking": len(categories["breaking"]),
            "other": len(categories["other"]),
            "total": sum(len(v) for v in categories.values())
        }
    }
}]
```

### Key Techniques

- Line-by-line parsing
- Pattern-based categorization
- Bullet point removal
- Skip headers and empty lines
- Summary statistics

---

## Pattern 7: Array Transformation

**Use case**: Reshape arrays and extract specific fields.

**Scenario**: Transform user data array to extract specific fields.

### Implementation

```python
all_items = _input.all()

# Extract and transform
transformed = []

for item in all_items:
    user = item["json"]

    # Extract nested fields
    profile = user.get("profile", {})
    settings = user.get("settings", {})

    transformed.append({
        "json": {
            "user_id": user.get("id"),
            "email": user.get("email"),
            "name": profile.get("name", "Unknown"),
            "avatar": profile.get("avatar_url"),
            "bio": profile.get("bio", "")[:100],  # Truncate to 100 chars
            "notifications_enabled": settings.get("notifications", True),
            "theme": settings.get("theme", "light"),
            "created_at": user.get("created_at"),
            "last_login": user.get("last_login_at")
        }
    })

return transformed
```

### Key Techniques

- Field extraction from nested objects
- Default values with .get()
- String truncation
- Flattening nested structures

---

## Pattern 8: Dictionary Lookup

**Use case**: Create lookup dictionary for fast data access.

**Scenario**: Look up user details by ID.

### Implementation

```python
all_items = _input.all()

# Build lookup dictionary
users_by_id = {}

for item in all_items:
    user = item["json"]
    user_id = user.get("id")

    if user_id:
        users_by_id[user_id] = {
            "name": user.get("name"),
            "email": user.get("email"),
            "status": user.get("status")
        }

# Example: Look up specific users
lookup_ids = [1, 3, 5]
looked_up = []

for user_id in lookup_ids:
    if user_id in users_by_id:
        looked_up.append({
            "json": {
                "id": user_id,
                **users_by_id[user_id],
                "found": True
            }
        })
    else:
        looked_up.append({
            "json": {
                "id": user_id,
                "found": False
            }
        })

return looked_up
```

### Key Techniques

- Dictionary comprehension alternative
- O(1) lookup time
- Handle missing keys gracefully
- Preserve lookup order

---

## Pattern 9: Top N Filtering

**Use case**: Get top items by score or value.

**Scenario**: Get top 10 products by sales.

### Implementation

```python
all_items = _input.all()

# Extract products with sales
products = []

for item in all_items:
    product = item["json"]
    products.append({
        "id": product.get("id"),
        "name": product.get("name"),
        "sales": product.get("sales", 0),
        "revenue": product.get("revenue", 0.0),
        "category": product.get("category")
    })

# Sort by sales descending
products.sort(key=lambda p: p["sales"], reverse=True)

# Get top 10
top_10 = products[:10]

return [
    {
        "json": {
            **product,
            "rank": index + 1
        }
    }
    for index, product in enumerate(top_10)
]
```

### Key Techniques

- List sorting with custom key
- Slicing for top N
- Add ranking information
- Enumerate for index

---

## Pattern 10: String Aggregation

**Use case**: Aggregate strings with formatting.

**Scenario**: Create summary text from multiple items.

### Implementation

```python
all_items = _input.all()

# Collect messages
messages = []

for item in all_items:
    data = item["json"]

    user = data.get("user", "Unknown")
    message = data.get("message", "")
    timestamp = data.get("timestamp", "")

    # Format each message
    formatted = f"[{timestamp}] {user}: {message}"
    messages.append(formatted)

# Join with newlines
summary = "\n".join(messages)

# Create statistics
total_length = sum(len(msg) for msg in messages)
average_length = total_length / len(messages) if messages else 0

return [{
    "json": {
        "summary": summary,
        "message_count": len(messages),
        "total_characters": total_length,
        "average_length": round(average_length, 2)
    }
}]
```

### Key Techniques

- String formatting with f-strings
- Join lists with separator
- Calculate string statistics
- Handle empty lists

---

## Pattern Comparison: Python vs JavaScript

### Data Access

```python
# Python
all_items = _input.all()
first_item = _input.first()
current = _input.item
webhook_data = _json["body"]

# JavaScript
const allItems = $input.all();
const firstItem = $input.first();
const current = $input.item;
const webhookData = $json.body;
```

### Dictionary/Object Access

```python
# Python - Dictionary key access
name = user["name"]           # May raise KeyError
name = user.get("name", "?")  # Safe with default

# JavaScript - Object property access
const name = user.name;              // May be undefined
const name = user.name || "?";       // Safe with default
```

### Array Operations

```python
# Python - List comprehension
filtered = [item for item in items if item["active"]]

# JavaScript - Array methods
const filtered = items.filter(item => item.active);
```

### Sorting

```python
# Python
items.sort(key=lambda x: x["score"], reverse=True)

# JavaScript
items.sort((a, b) => b.score - a.score);
```

---

## Best Practices

### 1. Use .get() for Safe Access

```python
# ✅ SAFE: Use .get() with defaults
name = user.get("name", "Unknown")
email = user.get("email", "no-email@example.com")

# ❌ RISKY: Direct key access
name = user["name"]  # KeyError if missing!
```

### 2. Handle Empty Lists

```python
# ✅ SAFE: Check before processing
items = _input.all()
if items:
    first = items[0]
else:
    return [{"json": {"error": "No items"}}]

# ❌ RISKY: Assume items exist
first = items[0]  # IndexError if empty!
```

### 3. Use List Comprehensions

```python
# ✅ PYTHONIC: List comprehension
active = [item for item in items if item["json"].get("active")]

# ❌ VERBOSE: Traditional loop
active = []
for item in items:
    if item["json"].get("active"):
        active.append(item)
```

### 4. Return Proper Format

```python
# ✅ CORRECT: Array of objects with "json" key
return [{"json": {"field": "value"}}]

# ❌ WRONG: Just the data
return {"field": "value"}

# ❌ WRONG: Array without "json" wrapper
return [{"field": "value"}]
```

### 5. Use Standard Library

```python
# ✅ GOOD: Use standard library
import statistics
average = statistics.mean(numbers)

# ✅ ALSO GOOD: Built-in functions
average = sum(numbers) / len(numbers) if numbers else 0

# ❌ CAN'T DO: External libraries
import numpy as np  # ModuleNotFoundError!
```

---

## When to Use Each Pattern

| Pattern | When to Use |
|---------|-------------|
| Multi-Source Aggregation | Combining data from different nodes/sources |
| Regex Filtering | Text pattern matching, validation, extraction |
| Markdown Parsing | Processing formatted text into structured data |
| JSON Comparison | Detecting changes between objects |
| CRM Transformation | Normalizing data from different systems |
| Release Notes | Categorizing text by keywords |
| Array Transformation | Reshaping data, extracting fields |
| Dictionary Lookup | Fast ID-based lookups |
| Top N Filtering | Getting best/worst items by criteria |
| String Aggregation | Creating formatted text summaries |

---

## Summary

**Key Takeaways**:
- Use `.get()` for safe dictionary access
- List comprehensions are pythonic and efficient
- Handle empty lists/None values
- Use standard library (json, datetime, re)
- Return proper n8n format: `[{"json": {...}}]`

**Remember**:
- JavaScript is recommended for 95% of use cases
- Python has NO external libraries
- Use n8n nodes for complex operations
- Code node is for data transformation, not API calls

**See Also**:
- SKILL.md - Python Code overview
- DATA_ACCESS.md - Data access patterns
- STANDARD_LIBRARY.md - Available modules
- ERROR_PATTERNS.md - Avoid common mistakes


---

# Error Patterns - Python Code Node

Common Python Code node errors and how to fix them.

---

## Error Overview

**Top 5 Python Code Node Errors**:

1. **ModuleNotFoundError** - Trying to import external libraries (Python-specific)
2. **Empty Code / Missing Return** - No code or return statement
3. **KeyError** - Dictionary access without .get()
4. **IndexError** - List access without bounds checking
5. **Incorrect Return Format** - Wrong data structure returned

These 5 errors cover the majority of Python Code node failures.

---

## Error #1: ModuleNotFoundError (MOST CRITICAL)

**Frequency**: Very common in Python Code nodes

**What it is**: Attempting to import external libraries that aren't available.

### The Problem

```python
# ❌ WRONG: External libraries not available
import requests  # ModuleNotFoundError: No module named 'requests'
import pandas    # ModuleNotFoundError: No module named 'pandas'
import numpy     # ModuleNotFoundError: No module named 'numpy'
import bs4       # ModuleNotFoundError: No module named 'bs4'
import pymongo   # ModuleNotFoundError: No module named 'pymongo'
import psycopg2  # ModuleNotFoundError: No module named 'psycopg2'

# This code will FAIL - these libraries are not installed!
response = requests.get("https://api.example.com/data")
```

### The Solution

**Option 1: Use JavaScript Instead** (Recommended for 95% of cases)

```javascript
// ✅ JavaScript Code node with $helpers.httpRequest()
const response = await $helpers.httpRequest({
  method: 'GET',
  url: 'https://api.example.com/data'
});

return [{json: response}];
```

**Option 2: Use n8n HTTP Request Node**

```python
# ✅ Add HTTP Request node BEFORE Python Code node
# Access the response in Python Code node

response = _input.first()["json"]

return [{
    "json": {
        "status": response.get("status"),
        "data": response.get("body"),
        "processed": True
    }
}]
```

**Option 3: Use Standard Library Only**

```python
# ✅ Use urllib from standard library (limited functionality)
from urllib.request import urlopen
from urllib.parse import urlencode
import json

# Simple GET request (no headers, no auth)
url = "https://api.example.com/data"
with urlopen(url) as response:
    data = json.loads(response.read())

return [{"json": data}]
```

### Common Library Replacements

| Need | ❌ External Library | ✅ Alternative |
|------|-------------------|----------------|
| HTTP requests | `requests` | Use HTTP Request node or JavaScript |
| Data analysis | `pandas` | Use Python list comprehensions |
| Database | `psycopg2`, `pymongo` | Use n8n database nodes |
| Web scraping | `beautifulsoup4` | Use HTML Extract node |
| Excel | `openpyxl` | Use Spreadsheet File node |
| Image processing | `pillow` | Use external API or node |

### Available Standard Library Modules

```python
# ✅ THESE WORK - Standard library only
import json          # JSON parsing
import datetime      # Date/time operations
import re            # Regular expressions
import base64        # Base64 encoding
import hashlib       # Hashing (MD5, SHA256)
import urllib.parse  # URL parsing and encoding
import math          # Math functions
import random        # Random numbers
import statistics    # Statistical functions
import collections   # defaultdict, Counter, etc.
```

---

## Error #2: Empty Code / Missing Return

**Frequency**: Common across all Code nodes

**What it is**: Code node has no code or no return statement.

### The Problem

```python
# ❌ WRONG: Empty code
# (nothing here)

# ❌ WRONG: Code but no return
items = _input.all()
processed = [item for item in items if item["json"].get("active")]
# Forgot to return!

# ❌ WRONG: Return in wrong scope
if _input.all():
    return [{"json": {"result": "success"}}]
# Return is inside if block - may not execute!
```

### The Solution

```python
# ✅ CORRECT: Always return
all_items = _input.all()

if not all_items:
    # Return empty array or error
    return [{"json": {"error": "No items"}}]

# Process items
processed = [item for item in all_items if item["json"].get("active")]

# Always return at the end
return processed if processed else [{"json": {"message": "No active items"}}]
```

### Best Practice

```python
# ✅ GOOD: Return at end of function (unconditional)
def process_items():
    items = _input.all()

    if not items:
        return [{"json": {"error": "Empty input"}}]

    # Process
    result = []
    for item in items:
        result.append({"json": item["json"]})

    return result

# Call function and return result
return process_items()
```

---

## Error #3: KeyError

**Frequency**: Very common in Python Code nodes

**What it is**: Accessing dictionary key that doesn't exist.

### The Problem

```python
# ❌ WRONG: Direct key access
item = _input.first()["json"]

name = item["name"]        # KeyError if "name" doesn't exist!
email = item["email"]      # KeyError if "email" doesn't exist!
age = item["age"]          # KeyError if "age" doesn't exist!

return [{
    "json": {
        "name": name,
        "email": email,
        "age": age
    }
}]
```

### Error Message

```
KeyError: 'name'
```

### The Solution

```python
# ✅ CORRECT: Use .get() with defaults
item = _input.first()["json"]

name = item.get("name", "Unknown")
email = item.get("email", "no-email@example.com")
age = item.get("age", 0)

return [{
    "json": {
        "name": name,
        "email": email,
        "age": age
    }
}]
```

### Nested Dictionary Access

```python
# ❌ WRONG: Nested key access
webhook = _input.first()["json"]
name = webhook["body"]["user"]["name"]  # Multiple KeyErrors possible!

# ✅ CORRECT: Safe nested access
webhook = _input.first()["json"]
body = webhook.get("body", {})
user = body.get("user", {})
name = user.get("name", "Unknown")

# ✅ ALSO CORRECT: Chained .get()
name = (
    webhook
    .get("body", {})
    .get("user", {})
    .get("name", "Unknown")
)

return [{"json": {"name": name}}]
```

### Webhook Body Access (Critical!)

```python
# ❌ WRONG: Forgetting webhook data is under "body"
webhook = _input.first()["json"]
name = webhook["name"]        # KeyError!
email = webhook["email"]      # KeyError!

# ✅ CORRECT: Access via ["body"]
webhook = _input.first()["json"]
body = webhook.get("body", {})
name = body.get("name", "Unknown")
email = body.get("email", "no-email")

return [{
    "json": {
        "name": name,
        "email": email
    }
}]
```

---

## Error #4: IndexError

**Frequency**: Common when processing arrays/lists

**What it is**: Accessing list index that doesn't exist.

### The Problem

```python
# ❌ WRONG: Assuming items exist
all_items = _input.all()
first_item = all_items[0]        # IndexError if list is empty!
second_item = all_items[1]       # IndexError if only 1 item!

return [{
    "json": {
        "first": first_item["json"],
        "second": second_item["json"]
    }
}]
```

### Error Message

```
IndexError: list index out of range
```

### The Solution

```python
# ✅ CORRECT: Check length first
all_items = _input.all()

if len(all_items) >= 2:
    first_item = all_items[0]["json"]
    second_item = all_items[1]["json"]

    return [{
        "json": {
            "first": first_item,
            "second": second_item
        }
    }]
else:
    return [{
        "json": {
            "error": f"Expected 2+ items, got {len(all_items)}"
        }
    }]
```

### Safe First Item Access

```python
# ✅ CORRECT: Use _input.first() instead of [0]
# This is safer than manual indexing
first_item = _input.first()["json"]

return [{"json": first_item}]

# ✅ ALSO CORRECT: Check before accessing
all_items = _input.all()
if all_items:
    first_item = all_items[0]["json"]
else:
    first_item = {}

return [{"json": first_item}]
```

### Slice Instead of Index

```python
# ✅ CORRECT: Use slicing (never raises IndexError)
all_items = _input.all()

# Get first 5 items (won't fail if fewer than 5)
first_five = all_items[:5]

# Get items after first (won't fail if empty)
rest = all_items[1:]

return [{"json": item["json"]} for item in first_five]
```

---

## Error #5: Incorrect Return Format

**Frequency**: Common for new users

**What it is**: Returning data in wrong format (n8n expects array of objects with "json" key).

### The Problem

```python
# ❌ WRONG: Returning plain dictionary
return {"name": "Alice", "age": 30}

# ❌ WRONG: Returning array without "json" wrapper
return [{"name": "Alice"}, {"name": "Bob"}]

# ❌ WRONG: Returning None
return None

# ❌ WRONG: Returning string
return "success"

# ❌ WRONG: Returning single item (not array)
return {"json": {"name": "Alice"}}
```

### The Solution

```python
# ✅ CORRECT: Array of objects with "json" key
return [{"json": {"name": "Alice", "age": 30}}]

# ✅ CORRECT: Multiple items
return [
    {"json": {"name": "Alice"}},
    {"json": {"name": "Bob"}}
]

# ✅ CORRECT: Transform items
all_items = _input.all()
return [
    {"json": item["json"]}
    for item in all_items
]

# ✅ CORRECT: Empty array (valid)
return []

# ✅ CORRECT: Single item still needs array wrapper
return [{"json": {"result": "success"}}]
```

### Common Scenarios

**Scenario 1: Aggregation (Return Single Result)**

```python
# Calculate total
all_items = _input.all()
total = sum(item["json"].get("amount", 0) for item in all_items)

# ✅ CORRECT: Wrap in array with "json"
return [{
    "json": {
        "total": total,
        "count": len(all_items)
    }
}]
```

**Scenario 2: Filtering (Return Multiple Results)**

```python
# Filter active items
all_items = _input.all()
active = [item for item in all_items if item["json"].get("active")]

# ✅ CORRECT: Already in correct format
return active

# ✅ ALSO CORRECT: If transforming
return [
    {"json": {**item["json"], "filtered": True}}
    for item in active
]
```

**Scenario 3: No Results**

```python
# ✅ CORRECT: Return empty array
return []

# ✅ ALSO CORRECT: Return error message
return [{"json": {"error": "No results found"}}]
```

---

## Bonus Error: AttributeError

**What it is**: Using _input.item in wrong mode.

### The Problem

```python
# ❌ WRONG: Using _input.item in "All Items" mode
current = _input.item        # None in "All Items" mode
data = current["json"]       # AttributeError: 'NoneType' object has no attribute '__getitem__'
```

### The Solution

```python
# ✅ CORRECT: Check mode or use appropriate method
# In "All Items" mode, use:
all_items = _input.all()

# In "Each Item" mode, use:
current_item = _input.item

# ✅ SAFE: Check if item exists
current = _input.item
if current:
    data = current["json"]
    return [{"json": data}]
else:
    # Running in "All Items" mode
    return _input.all()
```

---

## Error Prevention Checklist

Before running your Python Code node, verify:

- [ ] **No external imports**: Only standard library (json, datetime, re, etc.)
- [ ] **Code returns data**: Every code path ends with `return`
- [ ] **Correct format**: Returns `[{"json": {...}}]` (array with "json" key)
- [ ] **Safe dictionary access**: Uses `.get()` instead of `[]` for dictionaries
- [ ] **Safe list access**: Checks length before indexing or uses slicing
- [ ] **Webhook body access**: Accesses webhook data via `_json["body"]`
- [ ] **No None returns**: Returns empty array `[]` instead of `None`
- [ ] **Mode awareness**: Uses `_input.all()`, `_input.first()`, or `_input.item` appropriately

---

## Quick Fix Reference

| Error | Quick Fix |
|-------|-----------|
| `ModuleNotFoundError` | Use JavaScript or HTTP Request node instead |
| `KeyError: 'field'` | Change `data["field"]` to `data.get("field", default)` |
| `IndexError: list index out of range` | Check `if len(items) > 0:` before `items[0]` |
| Empty output | Add `return [{"json": {...}}]` at end |
| `AttributeError: 'NoneType'` | Check mode setting or verify `_input.item` exists |
| Wrong format error | Wrap result: `return [{"json": result}]` |
| Webhook KeyError | Access via `_json.get("body", {})` |

---

## Testing Your Code

### Test Pattern 1: Handle Empty Input

```python
# ✅ Always test with empty input
all_items = _input.all()

if not all_items:
    return [{"json": {"message": "No items to process"}}]

# Continue with processing
# ...
```

### Test Pattern 2: Test with Missing Fields

```python
# ✅ Use .get() with defaults
item = _input.first()["json"]

# These won't fail even if fields missing
name = item.get("name", "Unknown")
email = item.get("email", "no-email")
age = item.get("age", 0)

return [{"json": {"name": name, "email": email, "age": age}}]
```

### Test Pattern 3: Test Both Modes

```python
# ✅ Code that works in both modes
try:
    # Try "Each Item" mode first
    current = _input.item
    if current:
        return [{"json": current["json"]}]
except:
    pass

# Fall back to "All Items" mode
all_items = _input.all()
return all_items if all_items else [{"json": {"message": "No data"}}]
```

---

## Summary

**Top 5 Errors to Avoid**:
1. **ModuleNotFoundError** - Use JavaScript or n8n nodes instead
2. **Missing return** - Always end with `return [{"json": {...}}]`
3. **KeyError** - Use `.get()` for dictionary access
4. **IndexError** - Check length before indexing
5. **Wrong format** - Return `[{"json": {...}}]`, not plain objects

**Golden Rules**:
- NO external libraries (use JavaScript instead)
- ALWAYS use `.get()` for dictionaries
- ALWAYS return `[{"json": {...}}]` format
- CHECK lengths before list access
- ACCESS webhook data via `["body"]`

**Remember**:
- JavaScript is recommended for 95% of use cases
- Python has limitations (no requests, pandas, numpy)
- Use n8n nodes for complex operations

**See Also**:
- SKILL.md - Python Code overview
- DATA_ACCESS.md - Data access patterns
- STANDARD_LIBRARY.md - Available modules
- COMMON_PATTERNS.md - Production patterns
