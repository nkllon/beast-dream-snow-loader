# Environment Variable Rules

**Purpose:** Guidelines for environment variable management in beast-dream-snow-loader.

## Location Rules

### `.env` File (Project Root)

**Location:** `.env` file in project root (same directory as `pyproject.toml`)

**Status:** Git-ignored (never committed)

**Usage:**
- `python-dotenv` automatically loads `.env` from project root
- Use `load_dotenv()` (already in `api_client.py`)
- Loads automatically when module is imported

**Example:**
```bash
# .env file (project root)
SERVICENOW_INSTANCE=dev12345.service-now.com
SERVICENOW_USERNAME=service-account-username
SERVICENOW_API_KEY=abc123xyz...
```

### System Environment Variables

**Location:** System environment (shell environment)

**Usage:**
- Set via `export` in shell
- Available to all processes
- Higher priority than `.env` file (if both set)

**Example:**
```bash
export SERVICENOW_INSTANCE=dev12345.service-now.com
export SERVICENOW_USERNAME=service-account-username
export SERVICENOW_API_KEY=abc123xyz...
```

### Priority Order

1. **Function arguments** (highest priority)
2. **System environment variables** (`os.getenv()`)
3. **`.env` file** (loaded by `python-dotenv`)
4. **1Password CLI** (if available and signed in)

## When to Use Each

### Development/Testing
- Use `.env` file (project root, git-ignored)
- Easy to manage per-project credentials
- Can have different `.env` files for different environments

### Production
- Use 1Password CLI (preferred)
- Or system environment variables (set by deployment system)
- Never use `.env` file in production (security risk)

### CI/CD
- Use system environment variables (set by CI/CD system)
- Or secrets management (GitHub Secrets, etc.)
- Never commit `.env` file

## Security Best Practices

1. **Never commit `.env` file** - Add to `.gitignore`
2. **Use 1Password CLI** for production credentials
3. **Rotate credentials** regularly
4. **Use service accounts** with API keys (not passwords)
5. **Separate credentials** for dev/prod environments

## `.env` File Template

Create `.env.example` (committed) with placeholder values:

```bash
# ServiceNow Configuration
SERVICENOW_INSTANCE=your-instance.service-now.com
SERVICENOW_USERNAME=service-account-username
SERVICENOW_API_KEY=your-api-key-here
# SERVICENOW_OAUTH_TOKEN=optional-oauth-token
# SERVICENOW_PASSWORD=dev-password-only
```

Users copy `.env.example` to `.env` and fill in real values.

## References

- [python-dotenv Documentation](https://github.com/theskumar/python-dotenv)
- [Beast Projects: Credential Management](docs/agents.md#credential-management)

