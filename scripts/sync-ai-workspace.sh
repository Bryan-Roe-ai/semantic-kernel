#!/bin/bash

# AI Workspace Sync Script
# Syncs content from semantic-kernel/ai-workspace to bryan-roe-ai.github.io

set -e

echo "🚀 AI WORKSPACE SYNC SCRIPT"
echo "============================"

# Configuration
SOURCE_DIR="/workspaces/semantic-kernel/ai-workspace"
TARGET_DIR="/workspaces/semantic-kernel/bryan-roe-ai.github.io"

# Check if directories exist
if [ ! -d "$SOURCE_DIR" ]; then
    echo "❌ Source directory not found: $SOURCE_DIR"
    exit 1
fi

if [ ! -d "$TARGET_DIR" ]; then
    echo "❌ Target directory not found: $TARGET_DIR"
    exit 1
fi

echo "📂 Source: $SOURCE_DIR"
echo "🎯 Target: $TARGET_DIR"
echo ""

# Get current commit hash for tracking
cd /workspaces/semantic-kernel
SOURCE_COMMIT=$(git rev-parse HEAD)
echo "📝 Source commit: $SOURCE_COMMIT"

# Change to target directory
cd "$TARGET_DIR"

# Check git status
echo "🔍 Checking target repository status..."
git status --porcelain | head -5

# Backup important files
echo "💾 Backing up important files..."
mkdir -p .temp-backup
cp -r .git .temp-backup/ 2>/dev/null || true
cp -r .github .temp-backup/ 2>/dev/null || true
cp .nojekyll .temp-backup/ 2>/dev/null || true
cp .gitmodules .temp-backup/ 2>/dev/null || true
cp README.md .temp-backup/ 2>/dev/null || true

# Clear existing content (except backed up items)
echo "🧹 Clearing existing content..."
find . -maxdepth 1 -type f ! -name '.*' -delete
find . -maxdepth 1 -type d ! -name '.' ! -name '.git' ! -name '.github' ! -name '.temp-backup' -exec rm -rf {} \;

# Copy ai-workspace content
echo "📁 Copying ai-workspace content..."
cp -r "$SOURCE_DIR"/* .
cp -r "$SOURCE_DIR"/.* . 2>/dev/null || true

# Restore backed up files
echo "🔄 Restoring important files..."
cp -r .temp-backup/.git . 2>/dev/null || true
cp -r .temp-backup/.github . 2>/dev/null || true
cp .temp-backup/.nojekyll . 2>/dev/null || true
cp .temp-backup/.gitmodules . 2>/dev/null || true
cp .temp-backup/README.md . 2>/dev/null || true

# Clean up backup
rm -rf .temp-backup

# Store the source commit hash
echo "$SOURCE_COMMIT" > .sync-commit

echo "✅ Content synchronized successfully"

# Resolve symbolic links
echo "🔗 Resolving symbolic links..."

resolve_symlinks() {
    find . -type l | while read -r link; do
        target_path=$(readlink "$link")
        if [[ "$target_path" == /* ]]; then
            # Absolute path - try to find equivalent in semantic-kernel
            echo "⚠️  Absolute symlink: $link -> $target_path"
            # Try to find the file in semantic-kernel root
            source_file="/workspaces/semantic-kernel${target_path#/workspaces/semantic-kernel}"
            if [[ -e "$source_file" ]]; then
                echo "✅ Resolving absolute symlink: $link"
                rm "$link"
                cp -r "$source_file" "$link"
            else
                echo "❌ Cannot resolve absolute symlink: $link -> $target_path"
                rm "$link"
                echo "<!-- Could not resolve: $target_path -->" > "${link}.missing"
            fi
        else
            # Relative path - resolve if possible
            link_dir=$(dirname "$link")
            resolved_path="$link_dir/$target_path"
            
            if [[ -e "$resolved_path" ]]; then
                echo "✅ Resolving relative symlink: $link -> $target_path"
                rm "$link"
                cp -r "$resolved_path" "$link"
            else
                # Try to find in semantic-kernel root
                source_file="/workspaces/semantic-kernel/$target_path"
                if [[ -e "$source_file" ]]; then
                    echo "✅ Resolving symlink from root: $link -> $target_path"
                    rm "$link"
                    cp -r "$source_file" "$link"
                else
                    echo "❌ Broken symlink: $link -> $target_path"
                    rm "$link"
                    echo "<!-- Broken symlink: $target_path -->" > "${link}.broken"
                fi
            fi
        fi
    done
}

resolve_symlinks
echo "🔗 Symbolic link resolution completed"

# Update deployment info
echo "📊 Creating deployment information..."
cat > deployment-info.md << EOF
# AI Workspace Deployment Info

- **Deployed**: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
- **Source Commit**: $SOURCE_COMMIT
- **Sync Type**: Manual Script
- **Script Version**: 1.0

## Sync Status
- ✅ Content synchronized from semantic-kernel/ai-workspace
- ✅ Symbolic links resolved
- ✅ Ready for GitHub Pages deployment

## Files Synced
- Total directories: $(find . -maxdepth 1 -type d ! -name '.' ! -name '.git' | wc -l)
- Total files: $(find . -type f ! -path './.git/*' | wc -l)
- Repository size: $(du -sh . | cut -f1)

## Quick Verification
To verify the sync was successful:
1. Check https://bryan-roe-ai.github.io
2. Run: python3 deployment_summary.py
3. Verify all expected directories are present
EOF

# Show git status
echo "📋 Current git status:"
git status --short | head -10

# Commit changes if there are any
echo ""
echo "💬 Do you want to commit and push these changes? (y/N)"
read -r response

if [[ "$response" =~ ^[Yy]$ ]]; then
    echo "📝 Committing changes..."
    
    git add .
    
    if git diff --staged --quiet; then
        echo "📝 No changes to commit"
    else
        git commit -m "🔄 Manual sync from semantic-kernel ai-workspace

Source commit: $SOURCE_COMMIT
Sync timestamp: $(date -u +"%Y-%m-%d %H:%M:%S UTC")

- Synchronized complete ai-workspace content  
- Resolved symbolic links to actual files
- Updated deployment information
"
        
        echo "🚀 Pushing to remote repository..."
        git push origin main
        
        echo "✅ Changes pushed successfully!"
    fi
else
    echo "📝 Changes staged but not committed. You can review and commit manually."
fi

echo ""
echo "🎉 SYNC COMPLETED!"
echo "================="
echo "🔗 Live Site: https://bryan-roe-ai.github.io"
echo "📂 Local Target: $TARGET_DIR"
echo "📊 Deployment Info: $TARGET_DIR/deployment-info.md"
echo ""
echo "📋 Next Steps:"
echo "1. Review changes: git status"
echo "2. Check live site in 1-2 minutes"
echo "3. Run deployment summary: python3 deployment_summary.py"
echo ""
echo "✨ Happy coding!"
