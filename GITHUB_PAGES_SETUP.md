# GitHub Pages Setup Guide

This guide will help you enable GitHub Pages for the Semantic Kernel repository and deploy the AI Workspace content.

## Quick Setup

### 1. Run the Setup Script

Make the setup script executable and run it:

```bash
chmod +x setup-github-pages.sh
./setup-github-pages.sh
```

### 2. Enable GitHub Pages in Repository Settings

1. Go to your GitHub repository
2. Click on **Settings** tab
3. Scroll down to **Pages** section in the left sidebar
4. Under **Source**, select **GitHub Actions**
5. Save the settings

### 3. Commit and Push Changes

```bash
git add .
git commit -m "Set up GitHub Pages deployment"
git push origin main
```

## What Gets Deployed

The GitHub Pages site will include:

- **Homepage** (`index.html`) - Main AI workspace interface
- **LLM Studio** (`custom-llm-studio.html`) - Custom LLM development interface  
- **JavaScript files** - Server functionality and rate limiting
- **Samples** - Code examples and demonstrations
- **Documentation** - All markdown files from the docs folder

## Deployment Process

### Automatic Deployment

The site automatically deploys when you:
- Push changes to the `main` branch
- Modify files in `docs/` or `ai-workspace/` folders
- Manually trigger the workflow

### Manual Deployment

You can manually trigger deployment:
1. Go to **Actions** tab in your repository
2. Select **Deploy to GitHub Pages** workflow  
3. Click **Run workflow**
4. Choose the `main` branch and click **Run workflow**

## Site URL

Once enabled, your site will be available at:
```
https://[your-username].github.io/semantic-kernel/
```

For organization repositories:
```
https://[organization-name].github.io/semantic-kernel/
```

## File Structure

```
docs/
├── index.html                 # Main homepage
├── custom-llm-studio.html     # LLM Studio interface
├── server.js                  # Server functionality
├── express-rate.js            # Rate limiting
├── samples/                   # Code samples
├── .nojekyll                  # Disables Jekyll
├── README.md                  # Documentation
└── last-deployment.txt        # Deployment timestamp
```

## Troubleshooting

### Common Issues

1. **Pages not updating**
   - Check the Actions tab for failed workflows
   - Ensure you've enabled GitHub Pages in Settings
   - Verify the workflow has proper permissions

2. **404 errors**
   - Ensure `index.html` exists in the docs folder
   - Check that GitHub Pages source is set to "GitHub Actions"
   - Wait a few minutes for deployment to complete

3. **Missing styles/scripts**
   - Check that all referenced files are in the docs folder
   - Verify file paths are relative, not absolute
   - Ensure `.nojekyll` file exists

### Checking Deployment Status

1. Go to **Actions** tab in your repository
2. Look for **Deploy to GitHub Pages** workflows
3. Click on the latest run to see deployment details
4. Check the deployment URL in the workflow output

### Updating Content

To update the site content:

1. Modify files in `ai-workspace/05-samples-demos/`
2. Run the setup script again: `./setup-github-pages.sh`
3. Commit and push changes
4. The site will automatically redeploy

## Advanced Configuration

### Custom Domain

To use a custom domain:

1. Add a `CNAME` file to the docs folder with your domain
2. Configure DNS settings with your domain provider
3. Update repository settings to use the custom domain

### Additional Pages

To add more pages:

1. Create HTML files in the `ai-workspace/05-samples-demos/` folder
2. Run the setup script to copy them to docs
3. Update navigation in `index.html` if needed

## Workflow Details

The GitHub Actions workflow:

1. **Triggers** on pushes to main branch or manual dispatch
2. **Syncs** content from `ai-workspace/05-samples-demos/` to `docs/`
3. **Validates** that required files exist and are properly formatted
4. **Deploys** the docs folder to GitHub Pages
5. **Outputs** the deployment URL

## Security Notes

- All files in the docs folder will be publicly accessible
- Ensure no sensitive information is included in the deployed files
- The `.nojekyll` file prevents Jekyll processing for faster deployment

## Support

If you encounter issues:

1. Check the [GitHub Pages documentation](https://docs.github.com/en/pages)
2. Review the workflow logs in the Actions tab
3. Ensure all file paths and permissions are correct
4. Verify that the repository has GitHub Pages enabled
