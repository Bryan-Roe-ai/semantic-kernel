#!/usr/bin/env python3
"""
Script to clean up duplicate entries in GitHub Actions workflows.
"""

import os
import re
import glob
from pathlib import Path


def remove_duplicates(content):
    """Remove duplicate lines and entries in workflow files."""
    
    lines = content.split('\n')
    cleaned_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check for duplicate timeout-minutes
        if 'timeout-minutes:' in line:
            cleaned_lines.append(line)
            # Skip any consecutive duplicate timeout-minutes lines
            j = i + 1
            while j < len(lines) and 'timeout-minutes:' in lines[j]:
                j += 1
            i = j
            continue
            
        # Check for duplicate cache entries
        if "cache: 'pip'" in line or "cache: 'npm'" in line:
            cleaned_lines.append(line)
            # Skip any consecutive duplicate cache lines
            j = i + 1
            while j < len(lines) and ('cache:' in lines[j]):
                if lines[j].strip() == line.strip():
                    j += 1
                else:
                    break
            i = j
            continue
            
        cleaned_lines.append(line)
        i += 1
    
    return '\n'.join(cleaned_lines)


def fix_yaml_formatting(content):
    """Fix common YAML formatting issues."""
    
    # Fix escaped quotes
    content = content.replace("\\'", "'")
    
    # Remove extra blank lines (more than 2 consecutive)
    content = re.sub(r'\n\n\n+', '\n\n', content)
    
    return content


def process_workflow_file(file_path):
    """Process a single workflow file to clean up issues."""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Remove duplicates
        content = remove_duplicates(content)
        
        # Fix YAML formatting
        content = fix_yaml_formatting(content)
        
        # Write back if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Cleaned up {file_path}")
            return True
        else:
            return False
            
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False


def main():
    """Main function to clean up all workflow files."""
    
    print("🧹 Cleaning up GitHub Actions workflows...")
    print("=" * 50)
    
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
    
    print(f"Found {len(workflow_files)} workflow files to clean up")
    print()
    
    cleaned_count = 0
    for file_path in sorted(workflow_files):
        if process_workflow_file(file_path):
            cleaned_count += 1
    
    print("=" * 50)
    print(f"✅ Cleanup completed! {cleaned_count} files were cleaned up.")
    
    if cleaned_count > 0:
        print("\n📋 Cleanup summary:")
        print("  - Removed duplicate timeout-minutes entries")
        print("  - Removed duplicate cache entries")
        print("  - Fixed YAML formatting issues")
        print("  - Removed excessive blank lines")


if __name__ == "__main__":
    main()
