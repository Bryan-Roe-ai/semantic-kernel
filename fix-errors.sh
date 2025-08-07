#!/bin/bash
# Fix common errors in the repository

set -e

echo "🔧 Running repository fix script..."

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "⚠️  Not in a git repository, skipping git-related fixes"
    SKIP_GIT=true
else
    SKIP_GIT=false
fi

# Function to fix Python files
fix_python_files() {
    echo "🐍 Fixing Python files..."

    # Find Python files and fix common issues
    find . -name "*.py" -type f -not -path "./venv/*" -not -path "./.venv/*" -not -path "./env/*" -not -path "./.env/*" | while read -r file; do
        # Add main guard if missing
        if grep -q "def main" "$file" && ! grep -q "if __name__ == \"__main__\":" "$file"; then
            echo "    Adding main guard to $file"
            echo "" >> "$file"
            echo 'if __name__ == "__main__":' >> "$file"
            echo "    main()" >> "$file"
        fi

        # Remove trailing whitespace
        sed -i 's/[[:space:]]*$//' "$file" 2>/dev/null || true

        # Fix shebang if needed
        if head -1 "$file" | grep -q "^#!.*python" && ! head -1 "$file" | grep -q "#!/usr/bin/env python"; then
            sed -i '1s|^#!.*python.*|#!/usr/bin/env python3|' "$file"
        fi
    done
}

# Function to fix shell scripts
fix_shell_scripts() {
    echo "🐚 Fixing shell scripts..."

    find . -name "*.sh" -type f | while read -r file; do
        # Make executable
        chmod +x "$file"

        # Add shebang if missing
        if ! head -1 "$file" | grep -q "^#!"; then
            echo "    Adding shebang to $file"
            temp_file=$(mktemp)
            echo "#!/bin/bash" > "$temp_file"
            cat "$file" >> "$temp_file"
            mv "$temp_file" "$file"
            chmod +x "$file"
        fi

        # Remove trailing whitespace
        sed -i 's/[[:space:]]*$//' "$file" 2>/dev/null || true
    done
}

# Function to fix YAML files
fix_yaml_files() {
    echo "📄 Fixing YAML files..."

    find . -name "*.yml" -o -name "*.yaml" | while read -r file; do
        # Remove trailing whitespace
        sed -i 's/[[:space:]]*$//' "$file" 2>/dev/null || true
    done
}

# Function to fix permissions
fix_permissions() {
    echo "🔐 Fixing file permissions..."

    # Make scripts executable
    find . -name "*.sh" -type f -exec chmod +x {} \;
    find . -name "launch*" -type f -exec chmod +x {} \;

    # Fix Python script permissions
    find . -name "*.py" -type f -exec chmod 644 {} \;
}

# Function to create missing directories
create_missing_directories() {
    echo "📁 Creating missing directories..."

    local dirs=(
        "logs"
        "scripts"
        "temp"
        "TestResults"
    )

    for dir in "${dirs[@]}"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            echo "    Created directory: $dir"
        fi
    done
}

# Function to fix git issues
fix_git_issues() {
    if [ "$SKIP_GIT" = true ]; then
        return 0
    fi

    echo "🗂️ Fixing git issues..."

    # Remove files that shouldn't be tracked
    if [ -f ".DS_Store" ]; then
        rm -f .DS_Store
        echo "    Removed .DS_Store"
    fi

    # Fix line endings (convert CRLF to LF)
    if command -v dos2unix >/dev/null 2>&1; then
        find . -type f \( -name "*.py" -o -name "*.sh" -o -name "*.yml" -o -name "*.yaml" -o -name "*.md" \) -exec dos2unix {} \; 2>/dev/null || true
    fi

    # Update git config for consistent line endings
    git config core.autocrlf false 2>/dev/null || true
    git config core.eol lf 2>/dev/null || true
}

# Function to check and install missing dependencies
check_dependencies() {
    echo "📦 Checking dependencies..."

    # Check Python
    if command -v python3 >/dev/null 2>&1; then
        echo "    ✅ Python3 is available"
    else
        echo "    ❌ Python3 is not available"
    fi

    # Check Node.js
    if command -v node >/dev/null 2>&1; then
        echo "    ✅ Node.js is available"
    else
        echo "    ❌ Node.js is not available"
    fi

    # Check .NET
    if command -v dotnet >/dev/null 2>&1; then
        echo "    ✅ .NET is available"
    else
        echo "    ❌ .NET is not available"
    fi
}

# Function to create basic maintenance report
create_maintenance_report() {
    echo "📊 Creating maintenance report..."

    cat > MAINTENANCE_REPORT.md << EOF
# Repository Maintenance Report

Generated on: $(date -u)

## Repository Statistics
- Total files: $(find . -type f | wc -l)
- Python files: $(find . -name "*.py" | wc -l)
- Shell scripts: $(find . -name "*.sh" | wc -l)
- YAML files: $(find . -name "*.yml" -o -name "*.yaml" | wc -l)
- Markdown files: $(find . -name "*.md" | wc -l)

## Git Information
$(if [ "$SKIP_GIT" = false ]; then
echo "- Branch: $(git branch --show-current 2>/dev/null || echo 'unknown')"
echo "- Last commit: $(git log -1 --pretty=format:'%h - %s (%an, %ar)' 2>/dev/null || echo 'unknown')"
echo "- Total commits: $(git rev-list --count HEAD 2>/dev/null || echo 'unknown')"
else
echo "- Git repository: Not available"
fi)

## Fixes Applied
- Fixed Python file formatting and main guards
- Fixed shell script permissions and shebangs
- Fixed YAML file formatting
- Created missing directories
- Fixed file permissions
$(if [ "$SKIP_GIT" = false ]; then echo "- Fixed git configuration"; fi)

## Recommendations
- Run tests after these fixes
- Review any workflow failures
- Update dependencies if needed
- Check for any remaining linting issues

EOF

    echo "    Created MAINTENANCE_REPORT.md"
}

# Main execution
main() {
    echo "Starting repository fixes..."
    echo "=========================="

    fix_python_files
    fix_shell_scripts
    fix_yaml_files
    fix_permissions
    create_missing_directories
    fix_git_issues
    check_dependencies
    create_maintenance_report

    echo "=========================="
    echo "✅ Repository fixes completed!"
    echo "📄 Check MAINTENANCE_REPORT.md for details"
}

# Run main function
main "$@"
