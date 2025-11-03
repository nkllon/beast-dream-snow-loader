# ServiceNow Integration Constraints & Assumptions

**Purpose:** Document explicit assumptions and constraints for ServiceNow integration. These may be modified or violated in future revisions.

**Last Updated:** 2025-11-03

## Critical Cluster-Wide Constraints

### Environment Variables: User's Home Directory Only

**Constraint:** All environment variables must be in the home directory of the executing user. No exceptions.

**For beast nodes/participants:** Environment variables can go nowhere else. This is a hard constraint.

**Enforcement:**
- Never create `.env` files in project directories (cluster-wide policy violation)
- Never use `python-dotenv` to load `.env` files from project root
- Only use system environment variables (from user's home directory)

**Can Violate:** No - this is a cluster-wide policy constraint.

**See:** `docs/env_var_rules.md` for detailed rules.

## Assumptions

### 1. Custom Fields Available ✅

**Assumption:** ServiceNow instance allows creating custom fields with `u_*` prefix.

**Fields We Assume Available:**
- `u_unifi_source_id` (string) - Stores UniFi source identifier
- `u_unifi_raw_data` (JSON/string) - Stores raw UniFi JSON for audit/reconciliation
- `u_unifi_registration_time` (datetime) - UniFi registration timestamp
- `u_unifi_last_connection_change` (datetime) - Last connection state change

**Rationale:** Standard ServiceNow custom field pattern. If unavailable, we'll need to use standard fields or different approach.

**Impact if Violated:** Would need to use standard fields only or different identifier strategy.

---

### 2. Standard CMDB Tables Available ✅

**Assumption:** Standard ServiceNow CMDB tables are available and can be used.

**Tables We Assume:**
- `cmdb_ci_network_gateway` - Network gateway CI
- `cmdb_location` - Location records
- `cmdb_ci_network_gear` - Network device CI
- `cmdb_endpoint` - Endpoint/client records (may be custom)

**Rationale:** Standard ServiceNow CMDB structure. If custom tables needed, we'll adjust.

**Impact if Violated:** Would need to create custom tables or use different table names.

---

### 3. Required Fields Minimal ✅

**Assumption:** ServiceNow tables have minimal required fields beyond standard CMDB fields.

**Required Fields We Assume:**
- `name` - Required for all CI tables
- `class_name` - May be auto-populated or optional
- `classification` - May be auto-populated or optional
- Standard fields: `sys_id` (auto-generated), `sys_created_on`, etc.

**Rationale:** Conservative assumption - start minimal, add fields as needed.

**Impact if Violated:** Would need to add required fields to models and transformations.

---

### 4. Direct REST API (Not Import Sets) ✅

**Assumption:** We use ServiceNow REST API Table API directly for record creation/updates.

**Rationale:** Simpler for initial implementation, more control. Import Sets can be added later if needed.

**Impact if Violated:** Would need to refactor to use Import Set API instead.

---

### 5. Authentication: Service Account with API Key (Production) ✅

**Assumption:** ServiceNow instance uses a **named service account user** for API operations:
- Service account user has a name/identity (for audit logs)
- Service account user has specific role/permissions for API operations
- Service account user **cannot log into UI** (no UI access)
- Service account uses **API key** (not password) for authentication

**Authentication Methods:**
1. **API Key** (Primary for production) - `SERVICENOW_API_KEY` + `SERVICENOW_USERNAME` env vars
   - Basic Auth with API key as password
   - Service account user (no UI login)
   - Named user for audit trail
2. **OAuth Token** (Optional) - `SERVICENOW_OAUTH_TOKEN` env var
   - Bearer token authentication
   - Can be tied to service account user
3. **Username/Password** (Development/testing only) - `SERVICENOW_USERNAME` + `SERVICENOW_PASSWORD`
   - Basic Auth with actual password
   - **NOT recommended for production**
   - Only for dev/testing with regular user accounts

**Rationale:** 
- Service account pattern provides audit trail (named user) without exposing UI credentials
- API keys are simpler than OAuth for system-to-system integrations
- Never use normal user credentials in production (except dev/testing)
- Service account user should not have UI login capability

**Impact if Violated:** Would need to use regular user credentials (not recommended for production).

---

### 6. Upsert Strategy: Query by Source ID ✅

**Assumption:** For upserts (create or update), we:
1. Query by `u_unifi_source_id` to find existing record
2. If found, update by `sys_id`
3. If not found, create new record

**Rationale:** Standard upsert pattern. Alternative: use Import Sets with transform maps.

**Impact if Violated:** Would need different upsert strategy (e.g., Import Sets, external ID field).

---

### 7. Relationship Linking: Two-Phase ✅

**Assumption:** We link relationships in two phases:
1. **Phase 1:** Create all records (without relationships), capture returned `sys_id`s
2. **Phase 2:** Update records with relationship references using captured `sys_id`s

**Rationale:** ServiceNow requires `sys_id` for relationships. Cannot use source IDs.

**Impact if Violated:** Would need single-phase approach (e.g., pre-create placeholder records).

---

### 8. Field Naming Convention ✅

**Assumption:** 
- ServiceNow fields use snake_case (e.g., `ip_address`, `mac_address`)
- Custom fields use `u_*` prefix (e.g., `u_unifi_source_id`)
- Relationships use standard ServiceNow reference fields (e.g., `host_id` → sys_id reference)

**Rationale:** Standard ServiceNow conventions.

**Impact if Violated:** Would need different field naming strategy.

---

## Constraints

### 1. sys_id Handling

**Constraint:** `sys_id` is auto-generated by ServiceNow and cannot be provided on create.

**Implementation:**
- `sys_id` is optional in models (for updates only)
- Do not provide `sys_id` when creating records
- Use `sys_id` from created records for relationships

**Can Violate:** No - this is a ServiceNow platform constraint.

---

### 2. Relationship References

**Constraint:** Relationships must reference ServiceNow `sys_id` values, not source identifiers.

**Implementation:**
- Store mapping: `{unifi_source_id: servicenow_sys_id}`
- Use `sys_id` values for all relationship fields
- Two-phase approach: create records → link relationships

**Can Violate:** No - this is a ServiceNow platform constraint.

---

### 3. Field Extraction

**Constraint:** Must flatten nested UniFi fields to flat ServiceNow schema.

**Implementation:**
- Extract nested fields (e.g., `reportedState.hostname` → `hostname`)
- Store raw data in `u_unifi_raw_data` for preservation
- Map to ServiceNow-compatible field names

**Can Violate:** Yes - can preserve more nested structure if ServiceNow supports it.

---

## Revision History

| Date | Change | Reason |
|------|--------|--------|
| 2025-11-03 | Initial assumptions | First implementation |

## Future Revision Considerations

When modifying constraints/assumptions:
1. Document the change in this file
2. Update affected code (models, transformations, loaders)
3. Update tests to reflect new constraints
4. Update smoke test if needed

## Questions That May Need Answers Later

1. **Custom fields available?** → Assumed YES, may need to verify
2. **Standard tables or custom?** → Assumed STANDARD, may need custom
3. **Required fields?** → Assumed MINIMAL, may need more
4. **Import Sets vs direct API?** → Assumed DIRECT API, may switch to Import Sets
5. **OAuth vs Basic Auth?** → Assumed BASIC AUTH, may need OAuth

