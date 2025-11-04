# Release Automation Principles

## Version and Tag Determination

**CRITICAL RULE: NEVER ASK THE USER FOR VERSION OR TAG INFORMATION**

All version and tag information MUST be determined automatically from the codebase:

### Version Source of Truth

**Primary Source:** `pyproject.toml`
- Field: `project.version`
- Format: `MAJOR.MINOR.PATCH` (e.g., `0.3.0`)
- **This is the single source of truth for version**

### Tag Construction

**Rule:** Tag is ALWAYS `v{version}` where `{version}` comes from `pyproject.toml`

**Example:**
- `pyproject.toml` has `version = "0.3.0"`
- Tag is ALWAYS `v0.3.0`
- **No exceptions, no questions, no variations**

### Release Notes Source

**Source:** `RELEASE_NOTES.md`
- Extract section for version: `## [VERSION] - DATE - TITLE`
- Use entire section content for GitHub release notes
- **NEVER ask user to provide release notes**

### Implementation Pattern

**For Agents:**
```bash
# Extract version from pyproject.toml
VERSION=$(uv run python -c "import tomllib; f = open('pyproject.toml', 'rb'); data = tomllib.load(f); print(data['project']['version'])")

# Construct tag
TAG="v${VERSION}"

# Use TAG for all operations
git tag -a "$TAG" -m "Release $VERSION: Description"
git push origin "$TAG"
```

**For Python Scripts:**
```python
import tomllib

with open('pyproject.toml', 'rb') as f:
    data = tomllib.load(f)
    version = data['project']['version']
    tag = f"v{version}"
```

### Release Process (Fully Automated)

1. **Version Update:** User updates version in `pyproject.toml` (and `__init__.py`, `sonar-project.properties`)
2. **Tag Creation:** Agent creates tag `v{version}` automatically
3. **Pre-Release Validation:** Workflow validates tag automatically
4. **GitHub Release:** Workflow creates GitHub release automatically (extracts notes from `RELEASE_NOTES.md`)
5. **PyPI Publishing:** Workflow publishes to PyPI automatically

**NO USER INTERVENTION REQUIRED** after version is updated in `pyproject.toml`

### What NOT to Do

**NEVER:**
- ❌ Ask user "What version should I use?"
- ❌ Ask user "What tag should I create?"
- ❌ Ask user "What should the tag name be?"
- ❌ Create tags with different format (e.g., `0.3.0` instead of `v0.3.0`)
- ❌ Guess or infer version from other sources
- ❌ Ask user to confirm version before creating tag

**ALWAYS:**
- ✅ Read version from `pyproject.toml`
- ✅ Construct tag as `v{version}`
- ✅ Extract release notes from `RELEASE_NOTES.md`
- ✅ Proceed automatically without asking

### Version Synchronization

All version fields must be synchronized:
- `pyproject.toml` - `project.version` (primary source)
- `src/beast_dream_snow_loader/__init__.py` - `__version__`
- `sonar-project.properties` - `sonar.projectVersion`

**Validation:** Pre-release workflow validates tag version matches `pyproject.toml` version

### Error Handling

**If version mismatch detected:**
- Workflow fails with clear error message
- Agent must fix version in `pyproject.toml` first
- Then recreate tag with correct version

**If release notes missing:**
- Workflow uses default: "Release {VERSION}"
- Warning logged but workflow continues

### Rationale

1. **Single Source of Truth:** `pyproject.toml` is the canonical version source
2. **Consistency:** Tag format is always `v{version}` - no variations
3. **Automation:** No user interaction required - fully automated
4. **Error Prevention:** Can't create wrong tag if reading from source of truth
5. **User Experience:** User doesn't need to remember version or tag format

### Integration with Immutability Principle

See `.kiro/steering/immutability-principle.md`:
- Tags are immutable once created
- Version must be correct before tag creation
- Pre-release validation ensures version correctness
- No tag deletion/recreation needed if version is correct from start

