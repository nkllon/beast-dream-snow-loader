# Deployment Guide

## PyPI Deployment

### Prerequisites

1. **PyPI Account**: Create account at https://pypi.org
2. **Trusted Publishing**: Configure GitHub Actions for trusted publishing (recommended)
   - Go to PyPI → Account Settings → API tokens
   - Add new project → "beast-dream-snow-loader"
   - Copy the trust publishing configuration
3. **Or API Token**: Generate API token for manual publishing

### Automatic Deployment (GitHub Actions)

The repository includes a GitHub Actions workflow that automatically publishes to PyPI when:

1. **GitHub Release Published**: Create a GitHub release with a tag (e.g., `v0.1.0`)
2. **Manual Workflow Dispatch**: Trigger workflow manually from GitHub Actions UI

**Workflow**: `.github/workflows/publish.yml`

**Steps:**
1. Runs quality checks (Ruff, Black, MyPy, pytest)
2. Builds the package
3. Publishes to PyPI using trusted publishing

### Manual Deployment

```bash
# Install build tools
uv pip install build twine

# Build package
uv build

# Check package
twine check dist/*

# Upload to PyPI (TestPyPI first)
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*
```

### Version Management

- Update version in `pyproject.toml` and `src/beast_dream_snow_loader/__init__.py`
- Use semantic versioning (MAJOR.MINOR.PATCH)
- Create GitHub release with matching tag

## Cloudflare Configuration

### Option 1: Cloudflare Pages (Documentation Site)

If you want to host documentation on Cloudflare Pages:

1. **Connect Repository**:
   - Go to Cloudflare Dashboard → Pages
   - Connect repository `nkllon/beast-dream-snow-loader`
   - Select branch (usually `main`)

2. **Build Configuration**:
   - **Framework preset**: None (or GitBook/Docusaurus if using)
   - **Build command**: (leave empty or configure if using docs generator)
   - **Output directory**: `docs/` (if using static docs)

3. **Custom Domain** (Optional):
   - Add custom domain in Cloudflare Pages settings
   - Configure DNS records as needed

### Option 2: Cloudflare DNS (Domain Configuration)

If you have a custom domain for the project:

1. **Add DNS Records**:
   - Go to Cloudflare Dashboard → DNS
   - Add A/AAAA records for domain
   - Add CNAME records for subdomains

2. **SSL/TLS**:
   - Set SSL/TLS mode to "Full" or "Full (strict)"
   - Enable automatic HTTPS rewrites

3. **Security**:
   - Enable WAF rules
   - Configure rate limiting if needed
   - Set up security headers

### Option 3: Cloudflare Workers (API Proxy)

If you need to proxy API requests:

1. **Create Worker**:
   - Go to Cloudflare Dashboard → Workers
   - Create new worker
   - Configure routing rules

2. **Deploy**:
   - Use Wrangler CLI or Cloudflare Dashboard
   - Configure environment variables
   - Set up routes

## Post-Deployment Verification

### PyPI

1. **Verify Package**:
   ```bash
   pip install beast-dream-snow-loader
   ```

2. **Check PyPI Page**:
   - Visit https://pypi.org/project/beast-dream-snow-loader/
   - Verify version, description, and links

3. **Test Installation**:
   ```bash
   pip install beast-dream-snow-loader
   python -c "import beast_dream_snow_loader; print(beast_dream_snow_loader.__version__)"
   ```

### Cloudflare

1. **Test DNS Resolution**:
   ```bash
   dig your-domain.com
   ```

2. **Test SSL/TLS**:
   - Visit https://your-domain.com
   - Verify SSL certificate is valid

3. **Test Pages**:
   - Visit Cloudflare Pages URL
   - Verify documentation loads correctly

## Troubleshooting

### PyPI Deployment Issues

- **403 Forbidden**: Check API token permissions
- **Package already exists**: Increment version number
- **Build fails**: Check `pyproject.toml` syntax and dependencies

### Cloudflare Issues

- **DNS not resolving**: Check DNS records and propagation
- **SSL errors**: Verify SSL/TLS mode and certificate
- **Pages not building**: Check build configuration and repository access

## Security Considerations

1. **API Tokens**: Never commit PyPI API tokens to repository
2. **Trusted Publishing**: Use GitHub Actions trusted publishing when possible
3. **Environment Variables**: Store secrets in GitHub Secrets or Cloudflare Secrets
4. **DNS Security**: Enable DNSSEC in Cloudflare
5. **Rate Limiting**: Configure rate limits for API endpoints

