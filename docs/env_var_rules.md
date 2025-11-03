# Environment Variable Rules

**Purpose:** Guidelines for environment variable management in beast-dream-snow-loader.

## Critical Cluster-Wide Rule

**⚠️ NEVER CREATE `.env` FILES IN PROJECT DIRECTORIES**

**Cluster-wide policy:** All environment variables must be in the home directory of the executing user. No exceptions.

**For beast nodes/participants:** Environment variables can go nowhere else. This is a hard constraint.

**Enforcement:** Never create `.env` files (at least without asking). Violates cluster-wide policy.

## Principle: Execution Context Agnosticism

**The code does not know WHO is executing it or in WHAT context.**

The code is **execution-context-agnostic**. It reads from `os.getenv()`, which automatically reads from the **executing user's** system environment, regardless of:
- **WHO** the executing user is (beast node, local developer, CI/CD system, production deployment user, etc.)
- **WHAT** execution context it's running in (beast cluster, local dev, CI/CD pipeline, production server, etc.)
- **WHERE** the executing user's home directory is (the code doesn't need to know)
- **HOW** the environment variables got there (shell config, deployment system, CI/CD injection, etc.)

The code does not detect or know its execution context. It just reads from the system environment of whoever is executing it.

**Key insight:** "All environment variables must be in the home directory of the executing user" - but the code doesn't know or care who that executing user is. It just reads from `os.getenv()` which automatically uses the executing user's environment.

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

