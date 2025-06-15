# AI Workspace GitHub Pages Control Setup

This document explains how to control the `bryan-roe-ai.github.io` repository from the `semantic-kernel` repository, enabling automatic syncing of your AI workspace content.

## 🎯 Overview

The setup allows you to:
- **Edit content** in `semantic-kernel/ai-workspace/`
- **Automatically sync** changes to `bryan-roe-ai.github.io`
- **Deploy updates** to the live GitHub Pages site
- **Maintain single source of truth** in semantic-kernel repo

## 🔧 Setup Options

### Option 1: Manual Sync Script ✅ (Ready to Use)

A bash script for manual synchronization is already available:

```bash
# Run the sync script
cd /workspaces/semantic-kernel
./scripts/sync-ai-workspace.sh
```

**Features:**
- ✅ Syncs complete ai-workspace content
- ✅ Resolves symbolic links automatically
- ✅ Preserves important GitHub Pages files
- ✅ Interactive commit/push option
- ✅ Generates deployment information

### Option 2: Automated GitHub Actions 🚧 (Requires Setup)

GitHub Actions workflow for automatic syncing on every push.

**Setup Steps:**

1. **Create Personal Access Token (PAT)**
   ```
   GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   
   Create new token with these scopes:
   ✅ repo (Full control of private repositories)
   ✅ workflow (Update GitHub Action workflows)
   ```

2. **Add Secret to semantic-kernel Repository**
   ```
   semantic-kernel repo → Settings → Secrets and variables → Actions
   
   Add new repository secret:
   Name: PAGES_DEPLOY_TOKEN
   Value: [Your PAT from step 1]
   ```

3. **Enable Workflow**
   ```
   The workflow file is already created at:
   .github/workflows/sync-to-github-pages.yml
   
   It will automatically trigger on:
   - Push to main branch (when ai-workspace/* files change)
   - Manual workflow dispatch
   ```

## 🚀 Usage

### Manual Sync

```bash
# Navigate to semantic-kernel directory
cd /workspaces/semantic-kernel

# Run the sync script
./scripts/sync-ai-workspace.sh

# Follow the interactive prompts
```

### Automatic Sync (after setup)

1. **Edit files** in `ai-workspace/`
2. **Commit and push** to semantic-kernel main branch
3. **GitHub Actions** automatically syncs to bryan-roe-ai.github.io
4. **GitHub Pages** deploys the updated site

### Force Manual Sync via GitHub Actions

```
GitHub → semantic-kernel repo → Actions → "Sync AI Workspace to GitHub Pages"
→ Run workflow → ✅ Check "Force complete sync"
```

## 📂 What Gets Synced

### Included:
- ✅ All `ai-workspace/` content
- ✅ Directory structure (01-notebooks, 02-agents, etc.)
- ✅ Main interface files (index.html, custom-llm-studio.html)
- ✅ Documentation and guides
- ✅ Scripts and utilities
- ✅ Configuration files

### Preserved in Target:
- 🔒 `.git/` directory
- 🔒 `.github/workflows/` (GitHub Pages deployment)
- 🔒 `.nojekyll` file
- 🔒 `README.md` (if exists)
- 🔒 `.gitmodules` (if exists)

### Resolved:
- 🔗 Symbolic links → Actual file content
- 📁 Broken links → Placeholder files
- 🔄 Absolute paths → Relative or copied content

## 🔍 Verification

After sync, verify the update:

```bash
# Check deployment status
cd bryan-roe-ai.github.io
python3 deployment_summary.py

# Check git status
git status

# Check live site
curl -I https://bryan-roe-ai.github.io
```

## 📋 Workflow Details

### Manual Script Process:
1. 💾 Backup important target files
2. 🧹 Clear target content (except backups)
3. 📁 Copy complete ai-workspace content
4. 🔄 Restore backed up files
5. 🔗 Resolve all symbolic links
6. 📊 Generate deployment info
7. 💬 Interactive commit/push

### GitHub Actions Process:
1. 🔍 Check if sync needed (commit comparison)
2. 📥 Checkout both repositories
3. 🔄 Execute same sync logic as manual script
4. 🤖 Auto-commit and push changes
5. 📧 Trigger GitHub Pages deployment

## 🛠️ Troubleshooting

### Common Issues:

**Script Permission Denied:**
```bash
chmod +x scripts/sync-ai-workspace.sh
```

**PAT Authentication Failed:**
- Verify PAT has correct scopes
- Check PAT hasn't expired
- Ensure secret name is exactly: `PAGES_DEPLOY_TOKEN`

**Sync Not Triggering:**
- Check workflow file exists: `.github/workflows/sync-to-github-pages.yml`
- Verify changes are in `ai-workspace/` directory
- Check Actions tab for workflow runs

**Broken Symlinks:**
- Script automatically handles most cases
- Check `.broken` and `.missing` placeholder files
- Manually copy missing content if needed

### Manual Recovery:

```bash
# Reset target repository if needed
cd bryan-roe-ai.github.io
git reset --hard HEAD~1  # Go back one commit
git push --force origin main

# Re-run sync
cd /workspaces/semantic-kernel
./scripts/sync-ai-workspace.sh
```

## 🎉 Benefits

- **Single Source of Truth**: Edit in semantic-kernel only
- **Automatic Deployment**: Changes auto-deploy to live site
- **Link Resolution**: No broken symlinks in final site
- **Backup Safety**: Important files always preserved
- **Change Tracking**: Full git history of all syncs
- **Flexible Control**: Manual or automatic sync options

## 📞 Support

For issues:
1. Check the deployment logs
2. Run `deployment_summary.py` for diagnostics
3. Review GitHub Actions logs
4. Verify PAT permissions and expiration

---

**🚀 Your AI workspace is now ready for centralized control from the semantic-kernel repository!**
