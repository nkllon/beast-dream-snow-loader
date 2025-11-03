# Environment Variable Rules

**Purpose:** Guidelines for environment variable management in beast-dream-snow-loader.

## Critical Cluster-Wide Rule

**⚠️ NEVER CREATE `.env` FILES IN PROJECT DIRECTORIES**

**Cluster-wide policy:** All environment variables must be in the home directory of the executing user. No exceptions.

**For beast nodes/participants:** Environment variables can go nowhere else. This is a hard constraint.

**Enforcement:** Never create `.env` files (at least without asking). Violates cluster-wide policy.

## Principle

**The code does not manage environment variables - it only consumes them.**

The code reads from the system environment via `os.getenv()`. The user/system is responsible for making environment variables available in the system environment. The code does not care WHERE they come from - that's the user's/system's responsibility.

**Note:** The code does not care HOW the user/system makes environment variables available - whether via shell config, deployment system, CI/CD, etc. That's the user's/system's responsibility.

### Priority Order

1. **Function arguments** (highest priority)
2. **System environment variables** (`os.getenv()` - from system environment)
3. **1Password CLI** (if available and signed in)

**Note:** Code reads from system environment only. The user/system is responsible for making environment variables available in the system environment (via shell config, deployment system, etc.).

## When to Use Each

### Development/Testing
- User/system sets environment variables in system environment (via shell config, session, etc.)
- Code reads from `os.getenv()` - does not care how they were set

### Production
- Use 1Password CLI (preferred) - code integrates with 1Password CLI
- Or user/system sets environment variables in system environment (via deployment system, etc.)
- Never use project-level `.env` files (cluster-wide policy violation)

### CI/CD
- CI/CD system sets environment variables in system environment
- Or secrets management (GitHub Secrets, etc.) - CI/CD system injects into environment
- Code reads from `os.getenv()` - does not care how they were set

## Security Best Practices

1. **Never create `.env` files** - Cluster-wide policy violation
2. **Use system environment variables** (from user's home directory)
3. **Use 1Password CLI** for production credentials
4. **Rotate credentials** regularly
5. **Use service accounts** with API keys (not passwords)
6. **Separate credentials** for dev/prod environments

## Configuration

**The user/system is responsible for making environment variables available.**

The code reads from `os.getenv()` (system environment variables only). The user/system must ensure environment variables are set in the system environment before running the code.

**Example (user responsibility):**
```bash
# User sets in shell (via ~/.bashrc, ~/.zshrc, deployment system, etc.)
export SERVICENOW_INSTANCE=dev12345.service-now.com
export SERVICENOW_USERNAME=service-account-username
export SERVICENOW_API_KEY=your-api-key-here
# SERVICENOW_OAUTH_TOKEN=optional-oauth-token
# SERVICENOW_PASSWORD=dev-password-only
```

**Code responsibility:** Only reads from `os.getenv()` - does not manage or load environment variables.

## References

- [Beast Projects: Credential Management](docs/agents.md#credential-management)
- Cluster-wide policy: All env vars in user's home directory

