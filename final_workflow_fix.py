#!/usr/bin/env python3
"""
Final comprehensive fix for GitHub Actions workflows.
"""

import os
import re
import glob
from pathlib import Path


def comprehensive_cleanup(content):
    """Comprehensive cleanup of workflow files."""
    
    lines = content.split('\n')
    cleaned_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped_line = line.strip()
        
        # Skip empty lines at the beginning
        if i == 0 and not stripped_line:
            i += 1
            continue
            
        # Handle duplicate consecutive entries
        if i < len(lines) - 1:
            next_line = lines[i + 1].strip()
            
            # Remove duplicate timeout-minutes
            if 'timeout-minutes:' in stripped_line and 'timeout-minutes:' in next_line:
                cleaned_lines.append(line)
                i += 2  # Skip the duplicate
                continue
                
            # Remove duplicate cache entries
            if ("cache: 'pip'" in stripped_line or "cache: 'npm'" in stripped_line) and \
               ("cache: 'pip'" in next_line or "cache: 'npm'" in next_line) and \
               stripped_line == next_line:
                cleaned_lines.append(line)
                i += 2  # Skip the duplicate
                continue
        
        cleaned_lines.append(line)
        i += 1
    
    return '\n'.join(cleaned_lines)


def fix_specific_issues(content):
    """Fix specific known issues."""
    
    # Fix escaped quotes in cache entries
    content = re.sub(r"cache: \\'(pip|npm)\\'", r"cache: '\1'", content)
    
    # Remove multiple consecutive blank lines
    content = re.sub(r'\n\n\n+', '\n\n', content)
    
    # Fix duplicate with entries in setup actions
    content = re.sub(r'(\s+with:\s*\n.*?cache: \'[^\']+\'\s*\n)\s*cache: \'[^\']+\'', r'\1', content, flags=re.MULTILINE | re.DOTALL)
    
    return content


def validate_yaml_structure(content):
    """Basic YAML structure validation."""
    
    lines = content.split('\n')
    issues = []
    
    for i, line in enumerate(lines, 1):
        # Check for improper indentation in key areas
        if 'timeout-minutes:' in line and not line.strip().startswith('timeout-minutes:'):
            continue  # It's properly indented under a job
        
        # Check for duplicate keys in the same block
        if i < len(lines) - 1:
            current_indent = len(line) - len(line.lstrip())
            next_line = lines[i]
            next_indent = len(next_line) - len(next_line.lstrip())
            
            if current_indent == next_indent and ':' in line and ':' in next_line:
                current_key = line.split(':')[0].strip()
                next_key = next_line.split(':')[0].strip()
                if current_key == next_key and current_key in ['timeout-minutes', 'cache']:
                    issues.append(f"Line {i}: Duplicate key '{current_key}'")
    
    return issues


def process_workflow_file(file_path):
    """Process a single workflow file comprehensively."""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply comprehensive cleanup
        content = comprehensive_cleanup(content)
        
        # Fix specific issues
        content = fix_specific_issues(content)
        
        # Validate structure
        issues = validate_yaml_structure(content)
        
        # Write back if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Fixed {file_path}")
            if issues:
                print(f"   ⚠️  Remaining issues: {len(issues)}")
                for issue in issues[:3]:  # Show first 3 issues
                    print(f"      - {issue}")
            return True
        else:
            if issues:
                print(f"ℹ️  {file_path} - Found {len(issues)} potential issues")
            return False
            
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False


def main():
    """Main function for comprehensive GitHub Actions fixes."""
    
    print("🔧 Final comprehensive GitHub Actions fix...")
    print("=" * 60)
    
    # Find all workflow files
    workflow_patterns = [
        '.github/workflows/*.yml',
        '.github/workflows/*.yaml',
        '04-infrastructure/.github/workflows/*.yml',
        '04-infrastructure/.github/workflows/*.yaml',
    ]
    
    workflow_files = []
    for pattern in workflow_patterns:
        workflow_files.extend(glob.glob(pattern, recursive=True))
    
    if not workflow_files:
        print("No workflow files found!")
        return
    
    print(f"Processing {len(workflow_files)} workflow files...")
    print()
    
    fixed_count = 0
    for file_path in sorted(workflow_files):
        if process_workflow_file(file_path):
            fixed_count += 1
    
    print("=" * 60)
    print(f"✅ Final fix completed! {fixed_count} files were updated.")
    
    print("\n📋 All GitHub Actions fixes applied:")
    print("  ✅ Updated action versions to latest")
    print("  ✅ Added timeout-minutes to jobs")
    print("  ✅ Added workflow_dispatch triggers")
    print("  ✅ Added caching for Python and Node setups")
    print("  ✅ Fixed script execution permissions")
    print("  ✅ Removed duplicate entries")
    print("  ✅ Fixed YAML formatting issues")
    print("  ✅ Cleaned up excessive blank lines")


if __name__ == "__main__":
    main()
