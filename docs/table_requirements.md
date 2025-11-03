# ServiceNow Table Requirements & Plugin Dependencies

## Overview

This document tracks which ServiceNow tables are available and which plugins/modules are required for them.

## Table Availability Check

Run `scripts/check_table_requirements.py` to verify table availability on your ServiceNow instance.

## Target Tables

### Required Tables

1. **`cmdb_ci_network_gateway`** - Network gateway CI
   - **Status:** ❌ Not available on PDI
   - **Plugin Required:** Likely ITOM (IT Operations Management)
   - **Reference:** ServiceNow KB KB1691523

2. **`cmdb_location`** - Location records
   - **Status:** ❌ Not available on PDI
   - **Plugin Required:** Unknown (may be standard CMDB)

3. **`cmdb_ci_network_gear`** - Network device CI
   - **Status:** ❌ Not available on PDI
   - **Plugin Required:** Likely ITOM

4. **`cmdb_endpoint`** - Endpoint/client records
   - **Status:** ❌ Not available on PDI
   - **Plugin Required:** Unknown (may be custom table)

### Base Table (Fallback)

5. **`cmdb_ci`** - Base Configuration Item table
   - **Status:** ✅ Available on all instances
   - **Plugin Required:** None (core CMDB)
   - **Usage:** Can use with `sys_class_name` field to categorize CIs

## Plugin Requirements

### ITOM (IT Operations Management)

Many specific CI type tables require ITOM plugin to be installed/activated:
- `cmdb_ci_network_gateway`
- `cmdb_ci_network_gear`
- Other network device CI types

**Reference:** ServiceNow KB article KB1691523 lists CI types requiring ITOM subscription.

### Discovery Plugin

Discovery plugin may also be required for some CI types, but this needs verification.

## Verification Methods

1. **Run script:** `python scripts/check_table_requirements.py`
   - Checks table existence via API
   - Queries `sys_db_object` table for metadata (scope, plugin info)
   - Lists installed plugins (if accessible)

2. **Check ServiceNow Documentation:**
   - KB article KB1691523: CI types requiring ITOM subscription
   - ServiceNow product documentation for table requirements

3. **Query ServiceNow Instance:**
   - `sys_db_object` table: Table metadata including scope/plugin
   - `sys_plugin` table: Installed plugins (may require admin access)

## Workarounds

### Option 1: Use Base `cmdb_ci` Table

Use base `cmdb_ci` table with `sys_class_name` field:

```python
data = {
    "sys_class_name": "cmdb_ci_network_gateway",
    "name": "Gateway Name",
    # ... other fields
}
client.create_record("cmdb_ci", data)
```

**Pros:**
- Works on all instances (no plugin required)
- Standard ServiceNow pattern

**Cons:**
- Less type-specific validation
- May not have all CI type-specific fields

### Option 2: Install ITOM Plugin

Install/activate ITOM plugin on ServiceNow instance to get specific CI type tables.

**Pros:**
- Full CI type support with all fields
- Better validation and relationships

**Cons:**
- Requires ITOM license/subscription
- May not be available on all instances

### Option 3: Create Custom Tables

Create custom tables with `u_*` prefix for UniFi-specific entities.

**Pros:**
- Full control over schema
- No plugin dependencies

**Cons:**
- More setup/maintenance
- Not standard ServiceNow pattern
- May not integrate well with standard CMDB workflows

## Current Implementation

The loader currently:
1. Attempts to use specific CI type tables first
2. Falls back to base `cmdb_ci` table if specific table doesn't exist (see `examples/smoke_test.py`)

This allows the tool to work on instances without ITOM while still supporting ITOM-enabled instances.

## Next Steps

1. **Verify ITOM Requirements:**
   - Check ServiceNow KB KB1691523 for definitive list
   - Test on instance with ITOM installed

2. **Document `cmdb_location` Requirements:**
   - Verify if this is standard CMDB or requires plugin
   - Check if it exists on instances without ITOM

3. **Enhance Table Detection:**
   - Update loader to automatically detect available tables
   - Provide clear error messages when tables are missing
   - Suggest workarounds (base table vs. custom tables)

