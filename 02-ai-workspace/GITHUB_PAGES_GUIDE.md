# GitHub Pages Deployment Guide

This guide explains how to deploy the AI Workspace to GitHub Pages using the automated GitHub Actions workflow.

## Prerequisites

1. **GitHub Repository**: You need a GitHub repository with the AI workspace code
2. **GitHub Pages**: Must be enabled in repository settings
3. **GitHub Actions**: Must be enabled in repository settings

## Setup Steps

### 1. Enable GitHub Pages

1. Go to your GitHub repository
2. Click on **Settings** tab
3. Scroll down to **Pages** section in the left sidebar
4. Under **Source**, select **GitHub Actions**
5. Save the settings

### 2. Configure Repository Secrets (Optional - For Docker)

If you want to build and push Docker images, add these secrets:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add the following repository secrets:
   - `DOCKER_USERNAME`: Your Docker Hub username
   - `DOCKER_PASSWORD`: Your Docker Hub password or access token

### 3. Trigger Deployment

The deployment workflow triggers automatically when:

- Code is pushed to the `main` branch in the `ai-workspace/` directory
- A pull request is created targeting the `main` branch
- Manually triggered via **Actions** tab → **AI Workspace Deployment** → **Run workflow**

## Workflow Overview

The GitHub Actions workflow (`ai-workspace-deploy.yml`) performs these steps:

### 1. Test Phase

- Sets up Python environment
- Installs dependencies
- Runs integration tests
- Tests API endpoints

### 2. Build Phase

- Creates static site from source files
- Bundles documentation and backend code
- Generates deployment artifacts

### 3. Deploy Phase

- Deploys static site to GitHub Pages
- Builds and pushes Docker image (if secrets configured)
- Provides deployment status notification

## Expected Results

After successful deployment:

1. **GitHub Pages Site**: Available at `https://{username}.github.io/{repository-name}`
2. **Static Files**: All HTML, CSS, JS files served from GitHub Pages
3. **Documentation**: Available alongside the web application
4. **Docker Image**: Available at Docker Hub (if configured)

## Accessing Your Deployed Site

Once deployed, your AI workspace will be available at:

- **Main Page**: `https://{username}.github.io/{repository-name}/`
- **AI Studio**: `https://{username}.github.io/{repository-name}/custom-llm-studio.html`
- **Documentation**: `https://{username}.github.io/{repository-name}/README-workspace.md`

## Troubleshooting

### Common Issues

1. **Pages not updating**:

   - Check if GitHub Pages is enabled
   - Verify the workflow completed successfully
   - Pages deployment can take 5-10 minutes

2. **Workflow failing**:

   - Check the Actions tab for error details
   - Ensure all required files are present
   - Verify Python dependencies are correct

3. **Docker build failing**:
   - Check if Docker secrets are correctly configured
   - This doesn't affect the static site deployment

### Monitoring Deployment

1. Go to **Actions** tab in your repository
2. Find the latest **AI Workspace Deployment** workflow run
3. Check the status of each job:
   - ✅ Test: Code tests passed
   - ✅ Build: Static site built successfully
   - ✅ Deploy Pages: Site deployed to GitHub Pages
   - ✅/❌ Docker Build: Container image built (optional)

## Manual Deployment

If you need to deploy manually:

```bash
# Clone the repository
git clone https://github.com/{username}/{repository-name}.git
cd {repository-name}/ai-workspace

# Build the static site
chmod +x scripts/build_static.sh
./scripts/build_static.sh

# The built site is in ./dist/ directory
# You can serve it with any static file server
python -m http.server 8080 --directory dist
```

## Next Steps

After successful deployment:

1. **Test the deployed site**: Visit all pages and verify functionality
2. **Set up custom domain** (optional): Configure a custom domain in Pages settings
3. **Monitor usage**: Check GitHub Pages analytics
4. **Update content**: Push changes to trigger automatic redeployment

## Support

If you encounter issues:

1. Check the GitHub Actions workflow logs
2. Review this documentation
3. Test the build process locally
4. Ensure all prerequisites are met
