# Environment Variable Rules

**Purpose:** Guidelines for environment variable management in beast-dream-snow-loader.

## Critical Cluster-Wide Rule

**⚠️ NEVER CREATE `.env` FILES IN PROJECT DIRECTORIES**

**Cluster-wide policy:** All environment variables must be in the home directory of the executing user. No exceptions.

**For beast nodes/participants:** Environment variables can go nowhere else. This is a hard constraint.

**Enforcement:** Never create `.env` files (at least without asking). Violates cluster-wide policy.

## Location Rules

### System Environment Variables (User's Home Directory)

**Location:** User's home directory (shell configuration)

**Usage:**
- Set via `export` in shell configuration files (e.g., `~/.bashrc`, `~/.zshrc`, `~/.profile`)
- Or set in shell session (from user's home directory context)
- Code reads from `os.getenv()` (system environment variables only)
- If you can't see `~/.env`, you have a bigger problem (system setup issue)

**Example:**
```bash
# Set in user's home directory shell config (e.g., ~/.bashrc, ~/.zshrc)
export SERVICENOW_INSTANCE=dev12345.service-now.com
export SERVICENOW_USERNAME=service-account-username
export SERVICENOW_API_KEY=abc123xyz...
```

**Or set in shell session:**
```bash
# Set in shell session (from user's home directory)
export SERVICENOW_INSTANCE=dev12345.service-now.com
export SERVICENOW_USERNAME=service-account-username
export SERVICENOW_API_KEY=abc123xyz...
```

### Priority Order

1. **Function arguments** (highest priority)
2. **System environment variables** (`os.getenv()` - from shell environment)
3. **`~/.env` file** (user's home directory, loaded by `python-dotenv` if exists)
4. **1Password CLI** (if available and signed in)

**Note:** Only `~/.env` (user's home directory) is used. Never project-level `.env` files.

## When to Use Each

### Development/Testing
- Use system environment variables (set in shell config in user's home directory)
- Set via `export` in `~/.bashrc`, `~/.zshrc`, or `~/.profile`
- Or set in shell session

### Production
- Use 1Password CLI (preferred)
- Or system environment variables (set by deployment system in user's home directory)
- Never use project-level `.env` files (cluster-wide policy violation)

### CI/CD
- Use system environment variables (set by CI/CD system)
- Or secrets management (GitHub Secrets, etc.)
- Never use `.env` files

## Security Best Practices

1. **Never create `.env` files** - Cluster-wide policy violation
2. **Use system environment variables** (from user's home directory)
3. **Use 1Password CLI** for production credentials
4. **Rotate credentials** regularly
5. **Use service accounts** with API keys (not passwords)
6. **Separate credentials** for dev/prod environments

## Configuration

**System environment variables only** - Set via shell configuration in user's home directory.

**Example shell configuration:**
```bash
# Add to ~/.bashrc, ~/.zshrc, or ~/.profile (user's home directory)
export SERVICENOW_INSTANCE=dev12345.service-now.com
export SERVICENOW_USERNAME=service-account-username
export SERVICENOW_API_KEY=your-api-key-here
# SERVICENOW_OAUTH_TOKEN=optional-oauth-token
# SERVICENOW_PASSWORD=dev-password-only
```

**Code reads from:** `os.getenv()` (system environment variables only)

## References

- [Beast Projects: Credential Management](docs/agents.md#credential-management)
- Cluster-wide policy: All env vars in user's home directory

