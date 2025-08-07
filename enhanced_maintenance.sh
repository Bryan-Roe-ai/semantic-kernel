#!/bin/bash

# Enhanced Repository Maintenance Script
# Provides comprehensive maintenance and organization tools

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# Main functions
show_help() {
    cat << EOF
${BLUE}Enhanced Repository Maintenance Tool${NC}

${GREEN}Usage:${NC}
  ./enhanced_maintenance.sh [COMMAND] [OPTIONS]

${GREEN}Commands:${NC}
  ${CYAN}health${NC}         - Quick repository health check
  ${CYAN}organize${NC}       - Run comprehensive file organization
  ${CYAN}clean${NC}          - Clean temporary files and caches
  ${CYAN}stats${NC}          - Generate detailed repository statistics
  ${CYAN}index${NC}          - Update repository index files
  ${CYAN}symlinks${NC}       - Verify and repair symlinks
  ${CYAN}backup${NC}         - Create backup of organization structure
  ${CYAN}restore${NC}        - Restore from backup
  ${CYAN}validate${NC}       - Validate repository structure
  ${CYAN}monitor${NC}        - Start continuous monitoring
  ${CYAN}report${NC}         - Generate comprehensive report
  ${CYAN}all${NC}            - Run complete maintenance cycle

${GREEN}Options:${NC}
  -v, --verbose   Enable verbose output
  -f, --force     Force operations without prompts
  -h, --help      Show this help message

${GREEN}Examples:${NC}
  ./enhanced_maintenance.sh health
  ./enhanced_maintenance.sh organize --verbose
  ./enhanced_maintenance.sh all --force

EOF
}

check_health() {
    log "🏥 Running repository health check..."

    local issues=0

    # Check directory structure
    info "Checking directory structure..."
    local expected_dirs=(
        "01-core-implementations"
        "02-ai-workspace"
        "03-development-tools"
        "04-infrastructure"
        "05-documentation"
        "06-deployment"
        "07-resources"
        "08-archived-versions"
        "09-agi-development"
        "10-configuration"
        "11-automation-scripts"
        "12-documentation"
        "13-testing"
        "14-runtime"
        "15-web-ui"
        "16-extensions"
        "17-temporary"
        "18-data"
        "19-miscellaneous"
    )

    for dir in "${expected_dirs[@]}"; do
        if [[ ! -d "$REPO_ROOT/$dir" ]]; then
            warn "Missing directory: $dir"
            ((issues++))
        fi
    done

    # Check symlinks
    info "Checking symlinks..."
    local broken_links=0
    while IFS= read -r -d '' link; do
        if [[ ! -e "$link" ]]; then
            warn "Broken symlink: $(basename "$link")"
            ((broken_links++))
            ((issues++))
        fi
    done < <(find "$REPO_ROOT" -maxdepth 1 -type l -print0)

    # Check for large files
    info "Checking for large files..."
    local large_files
    large_files=$(find "$REPO_ROOT" -type f -size +50M 2>/dev/null || true)
    if [[ -n "$large_files" ]]; then
        warn "Large files found:"
        echo "$large_files" | sed 's/^/  /'
        ((issues++))
    fi

    # Summary
    if [[ $issues -eq 0 ]]; then
        log "✅ Repository health check passed! No issues found."
    else
        warn "⚠️  Repository health check found $issues issue(s)."
    fi

    return $issues
}

run_organization() {
    log "🗂️  Running comprehensive file organization..."

    if [[ -f "$SCRIPT_DIR/comprehensive_file_organizer.py" ]]; then
        python3 "$SCRIPT_DIR/comprehensive_file_organizer.py"
    else
        warn "Comprehensive file organizer not found. Creating basic organization..."
        # Fallback basic organization
        create_basic_structure
    fi
}

create_basic_structure() {
    log "Creating basic directory structure..."

    local dirs=(
        "09-agi-development"
        "10-configuration"
        "11-automation-scripts"
        "12-documentation"
        "13-testing"
        "14-runtime"
        "15-web-ui"
        "16-extensions"
        "17-temporary"
        "18-data"
        "19-miscellaneous"
    )

    for dir in "${dirs[@]}"; do
        mkdir -p "$REPO_ROOT/$dir"
        if [[ ! -f "$REPO_ROOT/$dir/README.md" ]]; then
            echo "# ${dir//[-_]/ }" > "$REPO_ROOT/$dir/README.md"
            echo "" >> "$REPO_ROOT/$dir/README.md"
            echo "This directory contains files related to ${dir//[-_]/ }." >> "$REPO_ROOT/$dir/README.md"
        fi
    done
}

clean_repository() {
    log "🧹 Cleaning temporary files and caches..."

    # Clean Python cache
    find "$REPO_ROOT" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find "$REPO_ROOT" -type f -name "*.pyc" -delete 2>/dev/null || true

    # Clean temporary files
    find "$REPO_ROOT" -type f -name "*.tmp" -delete 2>/dev/null || true
    find "$REPO_ROOT" -type f -name "*.temp" -delete 2>/dev/null || true
    find "$REPO_ROOT" -type f -name "*.bak" -delete 2>/dev/null || true
    find "$REPO_ROOT" -type f -name "*~" -delete 2>/dev/null || true

    # Clean logs older than 30 days
    find "$REPO_ROOT" -type f -name "*.log" -mtime +30 -delete 2>/dev/null || true

    # Clean empty directories
    find "$REPO_ROOT" -type d -empty -delete 2>/dev/null || true

    log "✅ Repository cleaning completed."
}

generate_stats() {
    log "📊 Generating repository statistics..."

    local stats_file="$REPO_ROOT/REPOSITORY_STATS.md"

    cat > "$stats_file" << EOF
# Repository Statistics

**Generated**: $(date)

## Overview

- **Total Files**: $(find "$REPO_ROOT" -type f | wc -l)
- **Total Directories**: $(find "$REPO_ROOT" -type d | wc -l)
- **Total Symlinks**: $(find "$REPO_ROOT" -maxdepth 1 -type l | wc -l)
- **Repository Size**: $(du -sh "$REPO_ROOT" | cut -f1)

## Directory Breakdown

EOF

    # Add directory statistics
    for dir in "$REPO_ROOT"/*/; do
        if [[ -d "$dir" ]]; then
            local dirname=$(basename "$dir")
            local file_count=$(find "$dir" -type f | wc -l)
            local size=$(du -sh "$dir" 2>/dev/null | cut -f1)
            echo "- **$dirname**: $file_count files, $size" >> "$stats_file"
        fi
    done

    cat >> "$stats_file" << EOF

## File Type Analysis

EOF

    # Add file type statistics
    find "$REPO_ROOT" -type f -name "*.*" | sed 's/.*\.//' | sort | uniq -c | sort -nr | head -20 | while read count ext; do
        echo "- **.$ext**: $count files" >> "$stats_file"
    done

    log "✅ Statistics generated: $stats_file"
}

update_index() {
    log "📋 Updating repository index..."

    # Update JSON index if organizer exists
    if [[ -f "$SCRIPT_DIR/comprehensive_file_organizer.py" ]]; then
        python3 -c "
import sys
import os
sys.path.insert(0, '$SCRIPT_DIR')
from comprehensive_file_organizer import SemanticKernelOrganizer
organizer = SemanticKernelOrganizer('$REPO_ROOT')
organizer.create_index()
"
    fi

    log "✅ Repository index updated."
}

verify_symlinks() {
    log "🔗 Verifying and repairing symlinks..."

    local fixed=0
    local broken=0

    while IFS= read -r -d '' link; do
        if [[ ! -e "$link" ]]; then
            warn "Broken symlink found: $(basename "$link")"
            ((broken++))

            # Try to repair common symlinks
            local link_name=$(basename "$link")
            local target=""

            # Define repair mappings
            case "$link_name" in
                "dotnet") target="01-core-implementations/dotnet" ;;
                "python") target="01-core-implementations/python" ;;
                "java") target="01-core-implementations/java" ;;
                "typescript") target="01-core-implementations/typescript" ;;
                "ai-workspace") target="02-ai-workspace" ;;
                "scripts") target="04-infrastructure/scripts" ;;
                *) target="19-miscellaneous/$link_name" ;;
            esac

            if [[ -n "$target" && -e "$REPO_ROOT/$target" ]]; then
                rm -f "$link"
                ln -s "$target" "$link"
                info "Repaired symlink: $link_name -> $target"
                ((fixed++))
            fi
        fi
    done < <(find "$REPO_ROOT" -maxdepth 1 -type l -print0)

    log "✅ Symlink verification complete. Fixed: $fixed, Broken: $broken"
}

create_backup() {
    log "💾 Creating backup of organization structure..."

    local backup_dir="$REPO_ROOT/.organization_backups"
    local timestamp=$(date +"%Y%m%d_%H%M%S")
    local backup_path="$backup_dir/backup_$timestamp"

    mkdir -p "$backup_path"

    # Backup directory structure
    find "$REPO_ROOT" -type d -name "[0-9]*-*" > "$backup_path/directories.txt"

    # Backup symlinks
    find "$REPO_ROOT" -maxdepth 1 -type l -exec ls -la {} \; > "$backup_path/symlinks.txt"

    # Backup organization files
    cp "$REPO_ROOT"/COMPREHENSIVE_* "$backup_path/" 2>/dev/null || true
    cp "$REPO_ROOT"/REPOSITORY_* "$backup_path/" 2>/dev/null || true
    cp "$REPO_ROOT"/ORGANIZATION_* "$backup_path/" 2>/dev/null || true

    log "✅ Backup created: $backup_path"
}

validate_structure() {
    log "✅ Validating repository structure..."

    local errors=0

    # Check for required files
    local required_files=(
        "README.md"
        "LICENSE"
        "docs"
    )

    for file in "${required_files[@]}"; do
        if [[ ! -e "$REPO_ROOT/$file" ]]; then
            error "Missing required file/directory: $file"
            ((errors++))
        fi
    done

    # Check organization directories
    for dir in "$REPO_ROOT"/[0-9]*-*/; do
        if [[ -d "$dir" && ! -f "$dir/README.md" ]]; then
            warn "Missing README.md in $(basename "$dir")"
            ((errors++))
        fi
    done

    if [[ $errors -eq 0 ]]; then
        log "✅ Repository structure validation passed."
    else
        error "Repository structure validation failed with $errors error(s)."
    fi

    return $errors
}

generate_report() {
    log "📄 Generating comprehensive repository report..."

    local report_file="$REPO_ROOT/MAINTENANCE_REPORT.md"

    cat > "$report_file" << EOF
# Repository Maintenance Report

**Generated**: $(date)
**Tool**: Enhanced Repository Maintenance Script

## Executive Summary

This report provides a comprehensive overview of the repository organization and maintenance status.

EOF

    # Add health check results
    echo "## Health Check Results" >> "$report_file"
    echo "" >> "$report_file"

    if check_health &>/dev/null; then
        echo "✅ **Status**: HEALTHY" >> "$report_file"
    else
        echo "⚠️ **Status**: ISSUES DETECTED" >> "$report_file"
    fi

    # Add statistics
    echo "" >> "$report_file"
    echo "## Repository Statistics" >> "$report_file"
    echo "" >> "$report_file"
    echo "- **Total Files**: $(find "$REPO_ROOT" -type f | wc -l)" >> "$report_file"
    echo "- **Total Directories**: $(find "$REPO_ROOT" -type d | wc -l)" >> "$report_file"
    echo "- **Repository Size**: $(du -sh "$REPO_ROOT" | cut -f1)" >> "$report_file"

    # Add recent activity
    echo "" >> "$report_file"
    echo "## Recent Activity" >> "$report_file"
    echo "" >> "$report_file"
    echo "### Recently Modified Files (Last 7 days)" >> "$report_file"
    echo "" >> "$report_file"
    find "$REPO_ROOT" -type f -mtime -7 -not -path "*/.git/*" | head -20 | while read file; do
        echo "- $(stat -c "%y %n" "$file" | cut -d' ' -f1,4-)" >> "$report_file"
    done

    log "✅ Comprehensive report generated: $report_file"
}

start_monitoring() {
    log "👁️  Starting repository monitoring..."

    # Simple monitoring loop
    while true; do
        echo -e "\n${BLUE}=== Repository Monitor - $(date) ===${NC}"

        # Quick health check
        if ! check_health &>/dev/null; then
            warn "Issues detected! Run './enhanced_maintenance.sh health' for details."
        fi

        # Check for new files in root
        local root_files
        root_files=$(find "$REPO_ROOT" -maxdepth 1 -type f -name "*" ! -name ".*" ! -name "README.md" ! -name "LICENSE" ! -name "*.md" | wc -l)
        if [[ $root_files -gt 0 ]]; then
            warn "$root_files unorganized files detected in root directory."
        fi

        sleep 300  # Check every 5 minutes
    done
}

run_complete_maintenance() {
    log "🔧 Running complete maintenance cycle..."

    check_health
    run_organization
    clean_repository
    generate_stats
    update_index
    verify_symlinks
    validate_structure
    generate_report

    log "✅ Complete maintenance cycle finished!"
}

# Main script logic
main() {
    cd "$REPO_ROOT"

    case "${1:-help}" in
        health)
            check_health
            ;;
        organize)
            run_organization
            ;;
        clean)
            clean_repository
            ;;
        stats)
            generate_stats
            ;;
        index)
            update_index
            ;;
        symlinks)
            verify_symlinks
            ;;
        backup)
            create_backup
            ;;
        validate)
            validate_structure
            ;;
        monitor)
            start_monitoring
            ;;
        report)
            generate_report
            ;;
        all)
            run_complete_maintenance
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            error "Unknown command: $1"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
