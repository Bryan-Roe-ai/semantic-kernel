#!/usr/bin/env python3
"""
Comprehensive GitHub Actions Workflow Fixer
This script identifies and fixes common YAML syntax and structural issues in GitHub Actions workflows.
"""

import os
import re
import yaml
import glob
from pathlib import Path

def fix_workflow_file(file_path):
    """Fix common issues in a GitHub Actions workflow file."""
    print(f"Fixing: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Fix 1: Normalize environment variable references (consistent spacing)
    content = re.sub(r'\$\{\{\s*([^}]+?)\s*\}\}', r'${{ \1 }}', content)

    # Fix 2: Fix orphaned 'with:' clauses
    content = re.sub(r'\n\s+with:\s*\n\s+persist-credentials:', r'\n        with:\n          persist-credentials:', content)

    # Fix 3: Fix duplicated setup actions
    content = re.sub(r'(\s+- name: Setup dotnet.*?\n\s+uses: actions/setup-dotnet@v\d+.*?\n\s+with:.*?\n\s+dotnet-version:.*?\n)\s+- name: Setup dotnet\s*\n\s+uses: actions/setup-dotnet@v[\d.]+\s*\n\s+with:', r'\1', content, flags=re.DOTALL)

    # Fix 4: Ensure proper step structure
    lines = content.split('\n')
    fixed_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Fix checkout actions without names
        if re.match(r'\s+- uses: actions/checkout@v\d+\s*$', line):
            indent = len(line) - len(line.lstrip())
            fixed_lines.append(' ' * indent + '- name: Checkout repository')
            fixed_lines.append(' ' * indent + '  uses: actions/checkout@v4')

        # Fix actions without proper names
        elif re.match(r'\s+- uses: [^@]+@[^\s]+\s*$', line):
            indent = len(line) - len(line.lstrip())
            action_name = line.strip().split('uses:')[1].strip().split('@')[0].split('/')[-1]
            fixed_lines.append(' ' * indent + f'- name: {action_name.replace("-", " ").title()}')
            fixed_lines.append(line)

        else:
            fixed_lines.append(line)

        i += 1

    content = '\n'.join(fixed_lines)

    # Fix 5: Remove empty lines that break YAML structure
    content = re.sub(r'\n\s*\n\s*with:', r'\n        with:', content)

    # Fix 6: Fix environment variable references in specific files
    if 'policy-validator-cfn.yml' in file_path:
        content = content.replace('${{ env.REFERENCE }}', '${{ env.REFERENCE_POLICY }}')
        content = content.replace('${{env.REGION }}', '${{ env.REGION }}')

    # Only write if changes were made
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Fixed {file_path}")
        return True
    else:
        print(f"  - No changes needed for {file_path}")
        return False

def validate_yaml_syntax(file_path):
    """Validate YAML syntax of a workflow file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            yaml.safe_load(f.read())
        return True, None
    except yaml.YAMLError as e:
        return False, str(e)

def main():
    """Main function to fix all workflow files."""

    # Find all workflow files
    workflow_patterns = [
        '/workspaces/semantic-kernel/.github/workflows/*.yml',
        '/workspaces/semantic-kernel/.github/workflows/*.yaml',
        '/workspaces/semantic-kernel/04-infrastructure/.github/workflows/*.yml',
        '/workspaces/semantic-kernel/04-infrastructure/.github/workflows/*.yaml'
    ]

    workflow_files = []
    for pattern in workflow_patterns:
        workflow_files.extend(glob.glob(pattern))

    print(f"Found {len(workflow_files)} workflow files to process")

    fixed_count = 0
    error_count = 0

    for file_path in sorted(workflow_files):
        try:
            if fix_workflow_file(file_path):
                fixed_count += 1

            # Validate after fixing
            is_valid, error = validate_yaml_syntax(file_path)
            if not is_valid:
                print(f"  ⚠️  YAML validation failed for {file_path}: {error}")
                error_count += 1

        except Exception as e:
            print(f"  ❌ Error processing {file_path}: {e}")
            error_count += 1

    print(f"\n📊 Summary:")
    print(f"  • Files processed: {len(workflow_files)}")
    print(f"  • Files fixed: {fixed_count}")
    print(f"  • Validation errors: {error_count}")

if __name__ == '__main__':
    main()
