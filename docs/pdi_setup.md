# Personal Developer Instance (PDI) Setup

**Purpose:** Guide for setting up ServiceNow PDI for REST API access.

## Enabling REST API Access

PDIs may require REST API to be enabled. To enable:

1. **Log into your PDI instance** (e.g., `https://dev212392.service-now.com`)
2. **Navigate to:** System Web Services → REST → REST API Explorer
   - Or search for "REST API Explorer" in the filter navigator
3. **Verify REST API is enabled** - you should see the REST API Explorer interface

If REST API Explorer doesn't work or shows errors, you may need to:

### Enable REST API Plugin
1. Go to **System Definition → Plugins**
2. Search for "REST API" or "API"
3. Ensure REST API plugin is **Active**

### Grant Required Roles
The user (admin) may need these roles:
- `rest_api_explorer` - Access to REST API Explorer
- `web_service_admin` - Admin access to web services
- `admin` - Should already have this on PDI

### Verify User Permissions
1. Go to **User Administration → Users**
2. Find your user (admin)
3. Verify roles include REST API access

## Testing REST API Access

Once enabled, test with:

```bash
curl -u "admin:PASSWORD" \
  -H "Accept: application/json" \
  "https://dev212392.service-now.com/api/now/table/sys_user?sysparm_limit=1"
```

Should return JSON data, not 401 error.

## Common Issues

### 401 Unauthorized - "User is not authenticated"
- **Cause:** REST API not enabled or user lacks permissions
- **Fix:** Enable REST API plugin, grant roles, verify user permissions

### 403 Forbidden
- **Cause:** User lacks required roles
- **Fix:** Grant `rest_api_explorer` and `web_service_admin` roles

### Instance URL Issues
- **PDI Instance URL:** `dev{number}.service-now.com` (e.g., `dev212392.service-now.com`)
- **Not:** `developer.service-now.com` (that's the portal, not the instance)

## References

- [ServiceNow Developer Portal](https://developer.servicenow.com)
- [PDI Guide](https://developer.servicenow.com/dev.do#!/guides/zurich/developer-program/pdi-guide/understanding-pdis)

