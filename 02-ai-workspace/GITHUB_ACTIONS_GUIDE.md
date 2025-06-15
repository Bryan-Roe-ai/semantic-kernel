# 🚀 GitHub Actions Deployment Guide

## Overview

The AI Workspace is configured with a complete CI/CD pipeline using GitHub Actions. This guide will help you activate and monitor the automated deployment process.

## ✅ Deployment Checklist

### Prerequisites

- [x] GitHub repository with admin access
- [x] AI Workspace code in the repository
- [x] GitHub Actions workflow file (`.github/workflows/ai-workspace-deploy.yml`)
- [x] All required files and scripts present

### Activation Steps

#### 1. Enable GitHub Pages

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Pages**
3. Under **Source**, select **GitHub Actions**
4. The workflow will automatically deploy on the next push to main

#### 2. Configure Secrets (Optional - for Docker Hub)

If you want to push Docker images to Docker Hub:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add these repository secrets:
   - `DOCKER_USERNAME`: Your Docker Hub username
   - `DOCKER_PASSWORD`: Your Docker Hub access token

#### 3. Trigger Deployment

```bash
# Make any change to the ai-workspace directory and commit
git add .
git commit -m "Deploy AI Workspace to GitHub Pages"
git push origin main
```

## 🔄 Workflow Details

The GitHub Actions workflow (`ai-workspace-deploy.yml`) performs these steps:

### 1. **Test Phase**

- Sets up Python 3.11 environment
- Installs dependencies from `requirements-minimal.txt`
- Runs integration tests (`scripts/integration_test.sh`)
- Tests API endpoints (`scripts/test_api_endpoints.sh`)

### 2. **Build Phase**

- Builds static site using `scripts/build_static.sh`
- Creates deployment artifacts
- Adds GitHub-specific deployment info

### 3. **Deploy Phase**

- **GitHub Pages**: Deploys static site to GitHub Pages
- **Docker**: Builds and pushes Docker image (optional)

### 4. **Notification Phase**

- Reports deployment status
- Provides links to deployed site

## 🌐 Access Your Deployed Site

After successful deployment, your site will be available at:

```
https://{github-username}.github.io/{repository-name}
```

### Direct Links

- **Main Interface**: `https://{username}.github.io/{repo}/index.html`
- **LLM Studio**: `https://{username}.github.io/{repo}/custom-llm-studio.html`

## 📊 Monitoring Deployment

### GitHub Actions Tab

1. Go to your repository
2. Click the **Actions** tab
3. Monitor workflow runs and deployment status

### Logs and Debugging

- Click on any workflow run to see detailed logs
- Each job (test, build, deploy) shows step-by-step execution
- Failed deployments show error details and troubleshooting info

## 🔧 Troubleshooting

### Common Issues

#### 1. **GitHub Pages Not Enabled**

**Error**: Workflow runs but site not accessible
**Solution**: Enable GitHub Pages in repository settings

#### 2. **Workflow Permissions**

**Error**: "Permission denied" in deployment step
**Solution**: Check repository permissions and GitHub Pages settings

#### 3. **Build Failures**

**Error**: Build step fails
**Solution**: Check that all required files exist and scripts are executable

#### 4. **Large File Sizes**

**Error**: GitHub Pages deployment fails due to size
**Solution**: GitHub Pages has a 1GB limit. Optimize assets or use Docker deployment

### Manual Deployment Test

```bash
# Test the build process locally
cd ai-workspace
./scripts/build_static.sh

# Validate the deployment
./scripts/validate_deployment.sh
```

## 🎯 Next Steps

### After Successful Deployment

1. **Test the Live Site**: Verify all functionality works
2. **Configure Custom Domain** (optional): Set up custom domain in GitHub Pages
3. **Monitor Performance**: Use GitHub insights to track usage
4. **Iterate**: Make improvements and push updates

### Production Considerations

- **API Backend**: The GitHub Pages deployment is static. For full API functionality, deploy the Docker container to a cloud service
- **Data Persistence**: Set up external storage for training data and models
- **Scaling**: Consider cloud deployment for high-traffic scenarios

## 📝 Files Involved

### GitHub Actions Workflow

- `.github/workflows/ai-workspace-deploy.yml` - Main workflow definition

### Build Scripts

- `ai-workspace/scripts/build_static.sh` - Static site builder
- `ai-workspace/scripts/integration_test.sh` - Integration tests
- `ai-workspace/scripts/test_api_endpoints.sh` - API tests
- `ai-workspace/scripts/validate_deployment.sh` - Deployment validation

### Configuration Files

- `ai-workspace/requirements-minimal.txt` - Python dependencies
- `ai-workspace/dist/_config.yml` - Jekyll configuration for GitHub Pages

### Deployment Artifacts

- `ai-workspace/dist/` - Built static site (created by build script)

---

## 🔄 Continuous Deployment

The workflow is configured to:

- **Trigger**: On push to main branch with changes in `ai-workspace/`
- **Test**: Run comprehensive tests before deployment
- **Deploy**: Automatically update GitHub Pages
- **Notify**: Report deployment status

This ensures your AI Workspace is always up-to-date and deployments are reliable!

---

**Need help?** Check the [Issue Resolution Guide](./ISSUE_RESOLUTION.md) for common problems and solutions.
