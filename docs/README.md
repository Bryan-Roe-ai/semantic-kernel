# AI Workspace Documentation

This directory contains the GitHub Pages site for the AI Workspace.

## Files

- `index.html` - Main AI workspace homepage
- `custom-llm-studio.html` - Custom LLM Studio interface
- `server.js` - Server-side functionality
- `express-rate.js` - Rate limiting features
- `samples/` - Code samples and demonstrations
- `.nojekyll` - Disables Jekyll processing for GitHub Pages

## Deployment

This site is automatically deployed via GitHub Actions when changes are made to:
- `docs/` folder
- `ai-workspace/` folder

The deployment workflow copies content from `ai-workspace/05-samples-demos/` to the `docs/` folder.

## Access

The site will be available at: `https://[username].github.io/semantic-kernel/`
