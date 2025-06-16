#!/bin/bash

# GitHub Actions Automation Setup Script
# This script helps configure the automated workflows for your repository

set -e

echo "🚀 GitHub Actions Automation Setup"
echo "=================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}$1${NC}"
}

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    print_error "This script must be run from within a git repository"
    exit 1
fi

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    print_warning "GitHub CLI (gh) is not installed. Some features may not work."
    print_warning "Install it from: https://cli.github.com/"
fi

print_header "Step 1: Repository Information"
echo "Current repository: $(git remote get-url origin 2>/dev/null || echo 'No remote origin found')"
echo "Current branch: $(git branch --show-current)"
echo ""

# Create necessary directories
print_header "Step 2: Creating Directory Structure"
directories=(
    ".github/workflows"
    ".github/ISSUE_TEMPLATE"
    "scripts"
    "deployment"
    "helm"
    "k8s"
    "tests"
    "reports"
)

for dir in "${directories[@]}"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        print_status "Created directory: $dir"
    else
        print_status "Directory already exists: $dir"
    fi
done
echo ""

# Create basic scripts if they don't exist
print_header "Step 3: Creating Helper Scripts"

# Create cleanup script
if [ ! -f "cleanup-workspace.sh" ]; then
    cat > cleanup-workspace.sh << 'EOF'
#!/bin/bash
# Automated workspace cleanup script

echo "Running workspace cleanup..."

# Remove common temporary files
find . -name "*.tmp" -type f -delete
find . -name "*.temp" -type f -delete
find . -name ".DS_Store" -type f -delete
find . -name "Thumbs.db" -type f -delete

# Clean Python cache
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -type f -delete

# Clean Node.js cache
find . -name "node_modules/.cache" -type d -exec rm -rf {} + 2>/dev/null || true

# Clean build artifacts
find . -name "dist" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "build" -type d -exec rm -rf {} + 2>/dev/null || true

echo "Workspace cleanup completed"
EOF
    chmod +x cleanup-workspace.sh
    print_status "Created cleanup-workspace.sh"
else
    print_status "cleanup-workspace.sh already exists"
fi

# Create issue generation script
if [ ! -f "scripts/generate_issues.py" ]; then
    cat > scripts/generate_issues.py << 'EOF'
#!/usr/bin/env python3
"""
Automated issue generation script
"""

import os
import json
import subprocess
from datetime import datetime

def create_issue(title, body, labels):
    """Create a GitHub issue using gh CLI"""
    try:
        cmd = [
            "gh", "issue", "create",
            "--title", title,
            "--body", body,
            "--label", ",".join(labels)
        ]
        subprocess.run(cmd, check=True)
        print(f"Created issue: {title}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create issue: {e}")

def main():
    """Main function to generate issues based on repository analysis"""
    print("Analyzing repository for potential issues...")

    # Example: Check for TODO comments
    try:
        result = subprocess.run(
            ["grep", "-r", "TODO", "--include=*.py", "--include=*.cs", "--include=*.js", "."],
            capture_output=True, text=True
        )

        if result.stdout:
            todo_count = len(result.stdout.strip().split('\n'))
            if todo_count > 10:
                create_issue(
                    f"High number of TODO comments detected ({todo_count})",
                    f"Found {todo_count} TODO comments in the codebase. Consider addressing these for better code quality.",
                    ["maintenance", "code-quality"]
                )
    except Exception as e:
        print(f"Error checking TODO comments: {e}")

if __name__ == "__main__":
    main()
EOF
    chmod +x scripts/generate_issues.py
    print_status "Created scripts/generate_issues.py"
else
    print_status "scripts/generate_issues.py already exists"
fi

# Create repository index update script
if [ ! -f "scripts/update_repository_index.py" ]; then
    cat > scripts/update_repository_index.py << 'EOF'
#!/usr/bin/env python3
"""
Repository index update script
"""

import os
import json
from datetime import datetime

def scan_directory(path, extensions):
    """Scan directory for files with specific extensions"""
    files = []
    for root, dirs, filenames in os.walk(path):
        # Skip hidden directories and common build directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'dist', 'build']]

        for filename in filenames:
            if any(filename.endswith(ext) for ext in extensions):
                full_path = os.path.join(root, filename)
                relative_path = os.path.relpath(full_path, path)
                files.append(relative_path)

    return files

def main():
    """Generate repository index"""
    print("Updating repository index...")

    extensions = {
        'python': ['.py'],
        'csharp': ['.cs'],
        'java': ['.java'],
        'javascript': ['.js', '.ts'],
        'documentation': ['.md', '.rst'],
        'configuration': ['.json', '.yaml', '.yml', '.toml']
    }

    index = {
        'generated_at': datetime.now().isoformat(),
        'repository': os.path.basename(os.getcwd()),
        'files_by_type': {}
    }

    for file_type, exts in extensions.items():
        files = scan_directory('.', exts)
        index['files_by_type'][file_type] = {
            'count': len(files),
            'files': files[:50]  # Limit to first 50 files
        }

    # Write to JSON file
    with open('REPOSITORY_INDEX.json', 'w') as f:
        json.dump(index, f, indent=2)

    # Create markdown summary
    with open('REPOSITORY_INDEX.md', 'w') as f:
        f.write(f"# Repository Index\n\n")
        f.write(f"Generated: {index['generated_at']}\n\n")
        f.write(f"## File Summary\n\n")

        for file_type, data in index['files_by_type'].items():
            f.write(f"- **{file_type.title()}**: {data['count']} files\n")

    print("Repository index updated successfully")

if __name__ == "__main__":
    main()
EOF
    chmod +x scripts/update_repository_index.py
    print_status "Created scripts/update_repository_index.py"
else
    print_status "scripts/update_repository_index.py already exists"
fi

echo ""

# Create basic configuration files
print_header "Step 4: Creating Configuration Files"

# Create basic requirements.txt if it doesn't exist
if [ ! -f "requirements.txt" ]; then
    cat > requirements.txt << 'EOF'
# Basic requirements for the semantic kernel project
# Add your project-specific dependencies here

# Development tools
pytest>=7.0.0
black>=22.0.0
flake8>=4.0.0
mypy>=0.900
isort>=5.10.0

# Security tools
bandit>=1.7.0
safety>=2.0.0
EOF
    print_status "Created requirements.txt"
else
    print_status "requirements.txt already exists"
fi

# Create .gitignore additions for automation
if [ ! -f ".gitignore" ]; then
    touch .gitignore
fi

gitignore_additions="
# GitHub Actions artifacts
reports/
coverage-report.md
test-coverage-summary.md
code-metrics.md
deployment-log.json
*.json.tmp
*-report.txt
*-report.json

# Environment files
.env.local
.env.*.local

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
"

if ! grep -q "# GitHub Actions artifacts" .gitignore 2>/dev/null; then
    echo "$gitignore_additions" >> .gitignore
    print_status "Updated .gitignore with automation artifacts"
else
    print_status ".gitignore already contains automation entries"
fi

echo ""

# GitHub Labels setup
print_header "Step 5: Setting up GitHub Labels"

if command -v gh &> /dev/null; then
    print_status "Setting up GitHub labels..."

    labels=(
        "automated:yellow:Issues created by automation"
        "bug:d73a4a:Something isn't working"
        "enhancement:a2eeef:New feature or request"
        "documentation:0075ca:Improvements or additions to documentation"
        "security:b60205:Security-related issues"
        "performance:1d76db:Performance improvements"
        "python:306998:Python-related issues"
        "dotnet:512bd4:C#/.NET related issues"
        "java:ed8b00:Java-related issues"
        "typescript:3178c6:TypeScript/JavaScript related issues"
        "priority:high:ee0701:High priority items"
        "stale:fef2c0:Issues with no recent activity"
        "code-quality:fbca04:Code quality improvements"
        "maintenance:0e8a16:Maintenance tasks"
        "compliance:5319e7:Compliance and licensing"
        "deployment:ff6b6b:Deployment related"
        "success:28a745:Successful operations"
        "failure:d93f0b:Failed operations"
    )

    for label in "${labels[@]}"; do
        IFS=':' read -r name color description <<< "$label"
        if gh label create "$name" --color "$color" --description "$description" 2>/dev/null; then
            print_status "Created label: $name"
        else
            print_status "Label already exists: $name"
        fi
    done
else
    print_warning "GitHub CLI not available. Please create labels manually:"
    echo "  bug, enhancement, documentation, security, performance"
    echo "  python, dotnet, java, typescript, priority:high, stale"
    echo "  code-quality, maintenance, compliance, deployment"
    echo "  automated, success, failure"
fi

echo ""

# Workflow validation
print_header "Step 6: Workflow Validation"

workflow_files=(
    ".github/workflows/automated-maintenance.yml"
    ".github/workflows/intelligent-issue-management.yml"
    ".github/workflows/security-automation.yml"
    ".github/workflows/code-quality-automation.yml"
    ".github/workflows/release-automation.yml"
    ".github/workflows/deployment-automation.yml"
)

for workflow in "${workflow_files[@]}"; do
    if [ -f "$workflow" ]; then
        print_status "Workflow exists: $workflow"
    else
        print_warning "Workflow missing: $workflow"
    fi
done

echo ""

# Final setup instructions
print_header "Step 7: Final Setup Instructions"

echo "To complete the setup, please:"
echo ""
echo "1. 📋 Configure Repository Secrets (Settings → Secrets and variables → Actions):"
echo "   - AZURE_CREDENTIALS (for Azure deployments)"
echo "   - PYPI_API_TOKEN (for Python package publishing)"
echo "   - NUGET_API_KEY (for .NET package publishing)"
echo "   - NPM_TOKEN (for npm package publishing)"
echo ""
echo "2. 🔧 Configure Workflow Permissions (Settings → Actions → General):"
echo "   - Set 'Workflow permissions' to 'Read and write permissions'"
echo "   - Enable 'Allow GitHub Actions to create and approve pull requests'"
echo ""
echo "3. 🛡️ Enable Branch Protection (Settings → Branches):"
echo "   - Add rule for 'main' branch"
echo "   - Require status checks to pass"
echo "   - Require pull request reviews"
echo ""
echo "4. 📊 Enable Features:"
echo "   - Issues and Discussions (Settings → Features)"
echo "   - GitHub Pages if needed (Settings → Pages)"
echo "   - Security alerts (Settings → Security & analysis)"
echo ""
echo "5. 🎯 Customize Workflows:"
echo "   - Update team names in intelligent-issue-management.yml"
echo "   - Adjust environment URLs in deployment-automation.yml"
echo "   - Modify quality thresholds in code-quality-automation.yml"
echo ""

# Commit changes
if [ "$(git status --porcelain)" ]; then
    print_header "Step 8: Committing Changes"

    echo "The following files have been created/modified:"
    git status --short
    echo ""

    read -p "Do you want to commit these changes? (y/N): " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git add .
        git commit -m "feat: setup GitHub Actions automation workflows

- Add comprehensive workflow automation
- Configure issue management and code quality
- Setup security scanning and deployment
- Create helper scripts and documentation"
        print_status "Changes committed successfully"

        if git remote get-url origin > /dev/null 2>&1; then
            read -p "Do you want to push to remote? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                git push
                print_status "Changes pushed to remote repository"
            fi
        fi
    else
        print_status "Changes not committed. You can commit them manually later."
    fi
fi

echo ""
print_header "🎉 Setup Complete!"
echo ""
echo "Your repository is now configured with automated GitHub Actions workflows."
echo "Check the .github/workflows/README.md file for detailed documentation."
echo ""
echo "Next steps:"
echo "1. Configure the required secrets in your repository settings"
echo "2. Review and customize the workflow files as needed"
echo "3. Test the workflows by creating issues or push commits"
echo ""
echo "For support, check the workflow documentation or create an issue."
echo ""
