# ServiceNow CI Class Selection Guide

## Overview

ServiceNow CIs can be queried from multiple class tables due to inheritance hierarchies. This document explains how to choose the "best" class for creating CIs.

## Class Hierarchy & Queryability

**Key Principle:** A CI created in a specific class table can be queried from all parent class tables, but NOT from child/subclass tables.

**Example:**
- A CI created in `cmdb_ci_netgear` can be queried from:
  - ✅ `cmdb_ci_netgear` (its own class)
  - ✅ `cmdb_ci_hardware` (parent class)
  - ✅ `cmdb_ci` (grandparent/base class)
  - ❌ `cmdb_ci_network_node` (child class - cannot query)

## Class Selection Strategy

**Goal:** Use the most specific appropriate class that matches the device type.

**Considerations:**
1. **Physical vs Virtual:** 
   - Physical hardware → `cmdb_ci_hardware` or subclasses
   - Virtual appliances → `cmdb_ci_vm_object` or subclasses

2. **Device Type:**
   - Network devices → `cmdb_ci_netgear` or `cmdb_ci_network_node`
   - Gateway/routers → `cmdb_ci_netgear` (physical) or gateway classes (virtual)
   - Locations → `cmdb_ci_site`

3. **Specificity:**
   - More specific = better validation and fields
   - Too specific = may not exist on all instances
   - Too generic = works everywhere but less useful

## Current Class Mappings

### Gateway (UniFi Dream Machine)

**Selected:** `cmdb_ci_netgear`

**Rationale:**
- UniFi Dream Machine is **physical network hardware**
- `cmdb_ci_netgear` is the class for physical network gear
- Alternative gateway classes (`cmdb_ci_nat_gateway`, `cmdb_ci_internet_gateway`) inherit from `cmdb_ci_vm_object` (virtual appliances)
- Hierarchy: `cmdb_ci_netgear` → `cmdb_ci_hardware` → `cmdb_ci` → `cmdb`

**Alternative Options:**
- `cmdb_ci_network_node` - Subclass of `cmdb_ci_netgear`, also valid for network devices
- `cmdb_ci_hardware` - More generic, works but less specific
- `cmdb_ci` - Base class, works everywhere but not specific

**Queryability:**
- ✅ Can query from `cmdb_ci_netgear`
- ✅ Can query from `cmdb_ci_hardware`
- ✅ Can query from `cmdb_ci`
- ❌ Cannot query from `cmdb_ci_network_node` (child class)

### Location (UniFi Site)

**Selected:** `cmdb_ci_site`

**Rationale:**
- Standard ServiceNow location class
- Hierarchy: `cmdb_ci_site` → `cmdb_ci` → `cmdb`
- `cmdb_location` doesn't exist (verified)

**Queryability:**
- ✅ Can query from `cmdb_ci_site`
- ✅ Can query from `cmdb_ci`
- ✅ Can query from `cmdb`

### Network Device (UniFi Devices)

**Selected:** `cmdb_ci_network_node`

**Rationale:**
- Subclass of `cmdb_ci_netgear`
- More specific than `cmdb_ci_netgear`
- Hierarchy: `cmdb_ci_network_node` → `cmdb_ci_netgear` → `cmdb_ci_hardware` → `cmdb_ci` → `cmdb`

**Queryability:**
- ✅ Can query from `cmdb_ci_network_node`
- ✅ Can query from `cmdb_ci_netgear`
- ✅ Can query from `cmdb_ci_hardware`
- ✅ Can query from `cmdb_ci`
- ✅ Can query from `cmdb`

### Endpoint (UniFi Clients)

**Selected:** `cmdb_ci` (base table with `sys_class_name`)

**Rationale:**
- `cmdb_endpoint` table doesn't exist
- Use base `cmdb_ci` with `sys_class_name="cmdb_endpoint"` or custom value
- Base table always available

**Queryability:**
- ✅ Can query from `cmdb_ci`
- ✅ Can query from `cmdb`

## Class Hierarchy Examples

### Gateway Classes (Virtual Appliances)
```
cmdb_ci_nat_gateway → cmdb_ci_vm_object → cmdb_ci → cmdb
cmdb_ci_internet_gateway → cmdb_ci_vm_object → cmdb_ci → cmdb
```
**Note:** These are for virtual/software appliances, not physical hardware.

### Network Device Classes (Physical Hardware)
```
cmdb_ci_network_node → cmdb_ci_netgear → cmdb_ci_hardware → cmdb_ci → cmdb
```
**Note:** This is the hierarchy for physical network devices like UniFi Dream Machine.

## Decision Matrix

| Device Type | Physical? | Recommended Class | Alternative Classes |
|------------|-----------|-------------------|---------------------|
| UniFi Dream Machine (Gateway) | ✅ Yes | `cmdb_ci_netgear` | `cmdb_ci_network_node`, `cmdb_ci_hardware` |
| UniFi Network Device | ✅ Yes | `cmdb_ci_network_node` | `cmdb_ci_netgear`, `cmdb_ci_hardware` |
| UniFi Site | N/A | `cmdb_ci_site` | `cmdb_ci` |
| UniFi Client | N/A | `cmdb_ci` (with `sys_class_name`) | Custom table |

## Verification

To check class hierarchies:
```bash
uv run python scripts/check_class_hierarchy.py
```

To check table availability:
```bash
uv run python scripts/check_table_requirements.py
```

## Future Considerations

1. **Multiple Class Support:** ServiceNow may support assigning multiple classes to a CI (needs verification)
2. **Dynamic Class Selection:** Could allow configuration of which class to use per device type
3. **Class Validation:** Could validate that selected class exists and is appropriate before creating CI

## References

- ServiceNow CMDB Class Hierarchy Documentation
- `scripts/check_class_hierarchy.py` - Tool to inspect class hierarchies
- `docs/table_requirements.md` - Table availability and plugin requirements

