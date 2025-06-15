# GitHub Pages Custom Domain Setup Guide

## Overview

By default, GitHub Pages serves your site at `username.github.io/repository-name`. If you want to use a custom domain (like `ai-workspace.example.com`), you need to configure a CNAME file and DNS settings.

## When You Need a CNAME File

**You DON'T need a CNAME file if:**

- Using the default GitHub Pages domain (`bryan-roe-ai.github.io/semantic-kernel/`)
- You're satisfied with the default domain

**You DO need a CNAME file if:**

- You want to use a custom domain like `ai-workspace.example.com`
- You want to use a subdomain like `workspace.yourdomain.com`
- You want to use an apex domain like `yourdomain.com`

## Current Status

This repository is currently configured for the **default GitHub Pages domain**:

- **URL**: https://bryan-roe-ai.github.io/semantic-kernel/
- **CNAME file**: Not needed (and not present)
- **DNS setup**: Not required

## Setting Up a Custom Domain (Optional)

If you want to set up a custom domain in the future, follow these steps:

### 1. Create CNAME File

Create a file named `CNAME` (all uppercase) in the repository root with your domain:

```bash
# For a subdomain
echo "ai-workspace.yourdomain.com" > CNAME

# For an apex domain
echo "yourdomain.com" > CNAME
```

**CNAME File Requirements:**

- ✅ Filename must be `CNAME` (all uppercase)
- ✅ Must contain exactly one domain (no multiple domains)
- ✅ Domain only (no `http://` or `https://`)
- ✅ No paths or query parameters
- ✅ Domain must be unique across all GitHub Pages sites

**Valid CNAME content examples:**

```
ai-workspace.example.com
```

```
workspace.example.com
```

```
example.com
```

**Invalid CNAME content:**

```
https://example.com           # ❌ No protocol
example.com/workspace         # ❌ No paths
multiple.com example.com      # ❌ Only one domain
```

### 2. Configure DNS

Set up DNS records with your domain provider:

**For subdomains** (recommended):

```
Type: CNAME
Name: ai-workspace (or your subdomain)
Value: bryan-roe-ai.github.io
```

**For apex domains**:

```
Type: A
Name: @ (or leave blank)
Value: 185.199.108.153
Value: 185.199.109.153
Value: 185.199.110.153
Value: 185.199.111.153
```

### 3. Update GitHub Settings

1. Go to repository Settings → Pages
2. In the "Custom domain" field, enter your domain
3. Enable "Enforce HTTPS" (recommended)
4. Save settings

### 4. Update Build Process

Our build script automatically handles CNAME files:

- Checks for `CNAME` in repository root
- Checks for `CNAME` in `ai-workspace/` directory
- Copies it to the `dist/` folder during build
- No manual intervention required

## Troubleshooting Custom Domains

### Common Issues

1. **404 Error on custom domain**

   - Check DNS propagation (can take 24-48 hours)
   - Verify CNAME file is properly formatted
   - Ensure GitHub Pages source is set to "GitHub Actions"

2. **SSL Certificate errors**

   - Wait for GitHub to provision certificate (can take 1 hour)
   - Ensure "Enforce HTTPS" is enabled in repository settings

3. **Build overwriting CNAME file**
   - Our build script preserves CNAME files automatically
   - CNAME file is copied to dist/ during build process

### Verification Commands

```bash
# Check CNAME file format
cat CNAME

# Test DNS resolution
nslookup yourdomain.com

# Run our diagnostic tool
python scripts/github_pages_diagnostic.py
```

## Best Practices

1. **Use subdomains** instead of apex domains when possible
2. **Test thoroughly** before switching from default domain
3. **Keep CNAME simple** - just the domain name
4. **Monitor DNS propagation** - it takes time
5. **Enable HTTPS** for security and SEO

## Current Deployment

Your AI workspace is currently deployed and accessible at:
**https://bryan-roe-ai.github.io/semantic-kernel/**

This default domain works perfectly and requires no additional setup or DNS configuration. Custom domains are optional and only needed if you prefer a different URL structure.

---

_For questions about custom domain setup, refer to [GitHub Pages documentation](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)_
