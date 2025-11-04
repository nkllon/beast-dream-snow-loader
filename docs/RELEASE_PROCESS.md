# Release Process

**Version:** 1.0  
**Last Updated:** 2025-11-04

## Overview

This document describes the complete release process for `beast-dream-snow-loader`, including validation steps to prevent release failures.

## Prerequisites

Before creating a release, ensure:

1. ✅ All code changes are committed and pushed to `main`
2. ✅ CI workflow passes on `main` branch
3. ✅ Version number is updated in:
   - `pyproject.toml`
   - `src/beast_dream_snow_loader/__init__.py`
   - `sonar-project.properties`
4. ✅ Release notes are updated in `RELEASE_NOTES.md`
5. ✅ All tests pass locally
6. ✅ Quality checks pass locally:
   ```bash
   uv run ruff check .
   uv run black --check .
   uv run pytest tests/ -v
   ```

## Release Steps

### Step 1: Prepare Release

1. **Update version numbers:**
   ```bash
   # Update version in pyproject.toml
   # Update version in __init__.py
   # Update version in sonar-project.properties
   ```

2. **Update release notes:**
   - Edit `RELEASE_NOTES.md`
   - Add entry for new version
   - Move planned items from "Unreleased" to version section

3. **Commit and push:**
   ```bash
   git add -A
   git commit -m "chore: prepare release 0.X.Y - Description"
   git push origin main
   ```

4. **Wait for CI to pass:**
   - Monitor GitHub Actions: https://github.com/nkllon/beast-dream-snow-loader/actions
   - Ensure CI workflow completes successfully
   - **DO NOT proceed if CI fails**

### Step 2: Create Tag

1. **Create annotated tag:**
   ```bash
   git tag -a v0.X.Y -m "Release 0.X.Y: Description"
   ```

2. **Push tag:**
   ```bash
   git push origin v0.X.Y
   ```

3. **Wait for pre-release validation:**
   - The pre-release workflow will automatically validate the tag
   - Monitor: https://github.com/nkllon/beast-dream-snow-loader/actions
   - **DO NOT create release if validation fails**

### Step 3: Create GitHub Release

1. **Create release using GitHub CLI:**
   ```bash
   gh release create v0.X.Y \
     --title "v0.X.Y - Description" \
     --notes-file <(sed -n 'START_LINE,END_LINEp' RELEASE_NOTES.md)
   ```

2. **Or create via GitHub UI:**
   - Go to: https://github.com/nkllon/beast-dream-snow-loader/releases/new
   - Select tag: `v0.X.Y`
   - Title: `v0.X.Y - Description`
   - Description: Copy from `RELEASE_NOTES.md`

3. **Publish release:**
   - Click "Publish release"
   - This will trigger the publish workflow

### Step 4: Monitor Publication

1. **Monitor workflow:**
   ```bash
   gh run watch
   ```

2. **Verify publication:**
   - Check PyPI: https://pypi.org/project/beast-dream-snow-loader/
   - Verify version appears
   - Test installation: `pip install beast-dream-snow-loader==0.X.Y`

## Automated Validation

The following workflows automatically validate releases:

### Pre-Release Validation (`.github/workflows/pre-release.yml`)

**Triggers:** When a tag is created

**Validates:**
- ✅ Tag points to commit on main branch
- ✅ Version in tag matches version in `pyproject.toml`
- ✅ Code quality checks pass (Ruff, Black, MyPy, pytest)
- ✅ Package builds successfully

**If validation fails:**
- Workflow fails
- Tag should be deleted and recreated after fixes
- Do NOT create GitHub release until validation passes

### Publish Workflow (`.github/workflows/publish.yml`)

**Triggers:** When a GitHub release is published

**Validates:**
- ✅ Version in tag matches version in `pyproject.toml`
- ✅ Code quality checks pass
- ✅ Package builds successfully
- ✅ Publishes to PyPI

**If validation fails:**
- Workflow fails
- Release remains unpublished
- Fix issues and recreate release

## Troubleshooting

### Release Workflow Fails

**Problem:** Workflow fails at quality checks step

**Solution:**
1. Check workflow logs for specific errors
2. Fix linting/formatting issues locally
3. Commit and push fixes
4. Delete tag: `git tag -d v0.X.Y && git push origin :refs/tags/v0.X.Y`
5. Recreate tag: `git tag -a v0.X.Y -m "..." && git push origin v0.X.Y`
6. Delete and recreate GitHub release

### Pre-Release Validation Fails

**Problem:** Pre-release workflow fails

**Solution:**
1. Check workflow logs for specific errors
2. Fix issues locally
3. Commit and push fixes
4. Delete tag: `git tag -d v0.X.Y && git push origin :refs/tags/v0.X.Y`
5. Recreate tag after CI passes on main
6. Wait for pre-release validation to pass
7. Create GitHub release

### Version Mismatch

**Problem:** Tag version doesn't match project version

**Solution:**
1. Ensure version in `pyproject.toml` matches tag version
2. Commit and push version update
3. Delete and recreate tag
4. Recreate release

## Best Practices

1. **Always wait for CI to pass** before creating tags
2. **Always wait for pre-release validation** before creating GitHub release
3. **Test locally first** before pushing to main
4. **Keep release notes up to date** during development
5. **Use semantic versioning** (MAJOR.MINOR.PATCH)
6. **Document breaking changes** in release notes

## Release Checklist

- [ ] Version numbers updated in all files
- [ ] Release notes updated
- [ ] All changes committed and pushed
- [ ] CI workflow passes on main
- [ ] Local quality checks pass
- [ ] Tag created and pushed
- [ ] Pre-release validation passes
- [ ] GitHub release created
- [ ] Publish workflow completes successfully
- [ ] PyPI package verified
- [ ] Installation tested

