#!/bin/bash
# Repository Maintenance Script
# Helps maintain the organized repository structure

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[$(date +'%H:%M:%S')] $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}[$(date +'%H:%M:%S')] ⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}[$(date +'%H:%M:%S')] ❌ $1${NC}"
}

# Check if we're in the right directory
if [[ ! -f "REPOSITORY_INDEX.md" ]]; then
    print_error "This script must be run from the semantic-kernel root directory"
    exit 1
fi

echo "🧹 Repository Maintenance Tool"
echo "=============================="

# Function to check for misplaced files
check_misplaced_files() {
    print_status "Checking for misplaced files..."

    misplaced=0

    # Check for language directories in root
    for lang in dotnet python java typescript; do
        if [[ -d "$lang" && ! -L "$lang" ]]; then
            print_warning "Found real directory '$lang' in root (should be symlink)"
            ((misplaced++))
        fi
    done

    # Check for dev tools in root
    for tool in notebooks samples tests plugins; do
        if [[ -d "$tool" && ! -L "$tool" ]]; then
            print_warning "Found real directory '$tool' in root (should be symlink)"
            ((misplaced++))
        fi
    done

    if [[ $misplaced -eq 0 ]]; then
        print_status "✅ No misplaced files found"
    else
        print_warning "Found $misplaced misplaced items"
    fi
}

# Function to clean up temporary files
cleanup_temp_files() {
    print_status "Cleaning up temporary files..."

    cleaned=0

    # Remove common temp files
    find . -maxdepth 1 -name "*.tmp" -type f -delete 2>/dev/null && ((cleaned++)) || true
    find . -maxdepth 1 -name "*.temp" -type f -delete 2>/dev/null && ((cleaned++)) || true
    find . -maxdepth 1 -name "*.bak" -type f -delete 2>/dev/null && ((cleaned++)) || true
    find . -maxdepth 1 -name "*.old" -type f -delete 2>/dev/null && ((cleaned++)) || true

    # Clean Python cache
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -name "*.pyc" -delete 2>/dev/null || true

    # Clean Node.js cache
    find . -type d -name "node_modules" -path "*/node_modules" -prune -o -type f -name "package-lock.json" -delete 2>/dev/null || true

    if [[ $cleaned -gt 0 ]]; then
        print_status "✅ Cleaned $cleaned temporary files"
    else
        print_status "✅ No temporary files to clean"
    fi
}

# Function to verify symlinks
verify_symlinks() {
    print_status "Verifying symlinks..."

    broken=0

    # Check all symlinks in root
    for link in dotnet python java typescript notebooks samples tests plugins prompt_template_samples ai-workspace scripts config configs .github data resources uploads public; do
        if [[ -L "$link" ]]; then
            if [[ ! -e "$link" ]]; then
                print_warning "Broken symlink: $link"
                ((broken++))
            fi
        fi
    done

    if [[ $broken -eq 0 ]]; then
        print_status "✅ All symlinks are valid"
    else
        print_warning "Found $broken broken symlinks"
    fi
}

# Function to update file counts
update_statistics() {
    print_status "Updating repository statistics..."

    cat > REPO_STATS.md << EOF
# Repository Statistics

Generated: $(date)

## Directory Structure

\`\`\`
$(tree -d -L 2 2>/dev/null || find . -type d -maxdepth 2 | sort)
\`\`\`

## File Counts

- **Core Implementations**: $(find 01-core-implementations -type f 2>/dev/null | wc -l) files
- **AI Workspace**: $(find 02-ai-workspace -type f 2>/dev/null | wc -l) files
- **Development Tools**: $(find 03-development-tools -type f 2>/dev/null | wc -l) files
- **Infrastructure**: $(find 04-infrastructure -type f 2>/dev/null | wc -l) files
- **Documentation**: $(find 05-documentation -type f 2>/dev/null | wc -l) files
- **Deployment**: $(find 06-deployment -type f 2>/dev/null | wc -l) files
- **Resources**: $(find 07-resources -type f 2>/dev/null | wc -l) files
- **Archived**: $(find 08-archived-versions -type f 2>/dev/null | wc -l) files

## Cleanup Status

- **Items in cleanup**: $(find .cleanup -type f 2>/dev/null | wc -l) files
- **Symlinks active**: $(find . -maxdepth 1 -type l | wc -l) links

## Last Maintenance

$(date)
EOF

    print_status "✅ Statistics updated in REPO_STATS.md"
}

# Function to show repository health
show_health() {
    print_status "Repository Health Check"
    echo "======================="

    echo "📁 Directory Organization:"
    for dir in 01-core-implementations 02-ai-workspace 03-development-tools 04-infrastructure 05-documentation 06-deployment 07-resources 08-archived-versions; do
        if [[ -d "$dir" ]]; then
            echo "  ✅ $dir"
        else
            echo "  ❌ $dir (missing)"
        fi
    done

    echo ""
    echo "🔗 Critical Symlinks:"
    for link in dotnet python java typescript ai-workspace scripts .github; do
        if [[ -L "$link" && -e "$link" ]]; then
            echo "  ✅ $link -> $(readlink "$link")"
        elif [[ -L "$link" ]]; then
            echo "  ❌ $link (broken)"
        elif [[ -d "$link" ]]; then
            echo "  ⚠️  $link (real directory, should be symlink)"
        else
            echo "  ❌ $link (missing)"
        fi
    done

    echo ""
    echo "🧹 Cleanup Status:"
    if [[ -d ".cleanup" ]]; then
        cleanup_files=$(find .cleanup -type f 2>/dev/null | wc -l)
        echo "  📦 $cleanup_files files in .cleanup/"
        if [[ $cleanup_files -gt 100 ]]; then
            echo "  ⚠️  Consider reviewing and purging old cleanup files"
        fi
    else
        echo "  ✅ No cleanup directory"
    fi
}

# Main menu
case "${1:-help}" in
    "check")
        check_misplaced_files
        verify_symlinks
        ;;
    "clean")
        cleanup_temp_files
        ;;
    "stats")
        update_statistics
        ;;
    "health")
        show_health
        ;;
    "all")
        check_misplaced_files
        cleanup_temp_files
        verify_symlinks
        update_statistics
        show_health
        ;;
    "help"|*)
        echo "Repository Maintenance Tool"
        echo ""
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  check   - Check for misplaced files and broken symlinks"
        echo "  clean   - Clean up temporary files"
        echo "  stats   - Update repository statistics"
        echo "  health  - Show repository health status"
        echo "  all     - Run all maintenance tasks"
        echo "  help    - Show this help message"
        echo ""
        echo "Examples:"
        echo "  $0 health     # Quick health check"
        echo "  $0 all        # Full maintenance run"
        echo "  $0 clean      # Just clean temp files"
        ;;
esac

echo ""
print_status "Maintenance complete!"
