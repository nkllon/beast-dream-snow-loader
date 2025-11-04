# Release Automation Principles

## Version and Tag Determination

**CRITICAL RULE: NEVER ASK THE USER FOR VERSION OR TAG INFORMATION**

All version and tag information MUST be determined intelligently by analyzing changes and applying semantic versioning:

### Version Recommendation Process

**Agents MUST:**
1. Read current version from `pyproject.toml` (field: `project.version`)
2. Analyze changes since last release:
   - Review git log and commit messages
   - Identify breaking changes, new features, bug fixes
   - Assess impact and scope of changes
3. Apply semantic versioning rules to recommend next version:
   - **MAJOR** (X.0.0): Breaking changes, API incompatibilities
   - **MINOR** (0.X.0): New features, backward-compatible enhancements
   - **PATCH** (0.0.X): Bug fixes, documentation, minor improvements
4. Update `pyproject.toml` with recommended version
5. Update `__init__.py` and `sonar-project.properties` to match
6. Proceed with release using determined version

### Version Source of Truth

**Primary Source:** `pyproject.toml`
- Field: `project.version`
- Format: `MAJOR.MINOR.PATCH` (e.g., `0.3.0`)
- **Must be updated with recommended version before release**

### Tag Construction

**Rule:** Tag is ALWAYS `v{version}` where `{version}` is the recommended/updated version in `pyproject.toml`

**Example:**
- Agent analyzes changes and recommends `0.3.0`
- Agent updates `pyproject.toml` to `version = "0.3.0"`
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
# 1. Read current version
CURRENT_VERSION=$(uv run python -c "import tomllib; f = open('pyproject.toml', 'rb'); data = tomllib.load(f); print(data['project']['version'])")

# 2. Analyze changes (git log, commit messages, etc.)
# Determine version bump type: MAJOR, MINOR, or PATCH
# Based on: breaking changes, new features, bug fixes

# 3. Calculate next version
# NEXT_VERSION = bump(CURRENT_VERSION, bump_type)

# 4. Update pyproject.toml with NEXT_VERSION
# Update __init__.py
# Update sonar-project.properties

# 5. Construct tag
TAG="v${NEXT_VERSION}"

# 6. Use TAG for all operations
git tag -a "$TAG" -m "Release $NEXT_VERSION: Description"
git push origin "$TAG"
```

**Semantic Versioning Analysis:**
- Check for breaking changes (API changes, removed features) → MAJOR bump
- Check for new features (backward-compatible additions) → MINOR bump
- Check for bug fixes, docs, refactoring → PATCH bump
- Review commit messages for semantic indicators
- Consider scope and impact of changes

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
- ❌ Ask user "Should this be a patch, minor, or major release?"
- ❌ Create tags with different format (e.g., `0.3.0` instead of `v0.3.0`)
- ❌ Guess version without analyzing changes
- ❌ Ask user to confirm version before creating tag
- ❌ Use current version without considering changes

**ALWAYS:**
- ✅ Analyze changes since last release
- ✅ Apply semantic versioning rules intelligently
- ✅ Recommend next version based on change analysis
- ✅ Update `pyproject.toml` with recommended version
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

1. **Intelligent Versioning:** Agent analyzes changes and applies semantic versioning correctly
2. **Single Source of Truth:** `pyproject.toml` is the canonical version source (after update)
3. **Consistency:** Tag format is always `v{version}` - no variations
4. **Automation:** No user interaction required - fully automated
5. **Error Prevention:** Can't create wrong tag if analyzing changes and updating correctly
6. **User Experience:** User doesn't need to remember version, tag format, or semantic versioning rules
7. **Accuracy:** Agent is in best position to analyze changes and recommend correct version

### Integration with Immutability Principle

See `.kiro/steering/immutability-principle.md`:
- Tags are immutable once created
- Version must be correct before tag creation
- Pre-release validation ensures version correctness
- No tag deletion/recreation needed if version is correct from start

