# Environment Variable Rules

**Purpose:** Guidelines for environment variable management in beast-dream-snow-loader.

## Critical Cluster-Wide Rule

**⚠️ NEVER CREATE `.env` FILES IN PROJECT DIRECTORIES**

**Cluster-wide policy:** All environment variables must be in the home directory of the executing user. No exceptions.

**For beast nodes/participants:** Environment variables can go nowhere else. This is a hard constraint.

**Enforcement:** Never create `.env` files (at least without asking). Violates cluster-wide policy.

## Location Rules

### System Environment Variables (User's Home Directory)

**Location:** User's home directory (shell environment)

**Usage:**
- Set via `export` in shell (from user's home directory)
- Available to all processes
- Only source for environment variables

**Example:**
```bash
# Set in user's home directory (e.g., ~/.bashrc, ~/.zshrc, or ~/.profile)
export SERVICENOW_INSTANCE=dev12345.service-now.com
export SERVICENOW_USERNAME=service-account-username
export SERVICENOW_API_KEY=abc123xyz...
```

**Or use system environment:**
```bash
# Set in shell session
export SERVICENOW_INSTANCE=dev12345.service-now.com
export SERVICENOW_USERNAME=service-account-username
export SERVICENOW_API_KEY=abc123xyz...
```

### Priority Order

1. **Function arguments** (highest priority)
2. **System environment variables** (`os.getenv()` - from user's home directory)
3. **1Password CLI** (if available and signed in)

**Note:** `.env` files are NOT used. Cluster-wide policy requires all env vars in user's home directory.

## When to Use Each

### Development/Testing
- Use system environment variables (from user's home directory)
- Set in shell config (`.bashrc`, `.zshrc`, etc.)
- Or export in shell session

### Production
- Use 1Password CLI (preferred)
- Or system environment variables (set by deployment system in user's home directory)
- Never use `.env` files (cluster-wide policy violation)

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

**No `.env` file template** - Use system environment variables only.

**Example shell configuration:**
```bash
# Add to ~/.bashrc, ~/.zshrc, or ~/.profile
export SERVICENOW_INSTANCE=dev12345.service-now.com
export SERVICENOW_USERNAME=service-account-username
export SERVICENOW_API_KEY=your-api-key-here
# SERVICENOW_OAUTH_TOKEN=optional-oauth-token
# SERVICENOW_PASSWORD=dev-password-only
```

## References

- [Beast Projects: Credential Management](docs/agents.md#credential-management)
- Cluster-wide policy: All env vars in user's home directory

