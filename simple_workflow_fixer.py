#!/usr/bin/env python3
"""
Simple GitHub Actions Workflow Fixer
Fixes the most common issues in workflow files without external dependencies.
"""

import os
import re
import glob
from pathlib import Path

def fix_environment_vars(content):
    """Fix environment variable spacing issues."""
    # Fix inconsistent spacing in environment variable references
    content = re.sub(r'\$\{\{\s*env\.([^}]+?)\s*\}\}', r'${{ env.\1 }}', content)
    content = re.sub(r'\$\{\{\s*vars\.([^}]+?)\s*\}\}', r'${{ vars.\1 }}', content)
    content = re.sub(r'\$\{\{\s*secrets\.([^}]+?)\s*\}\}', r'${{ secrets.\1 }}', content)
    return content

def fix_specific_errors(content, filename):
    """Fix specific errors identified in the error list."""

    # Fix policy-validator-cfn.yml specific issues
    if 'policy-validator-cfn.yml' in filename:
        content = content.replace('${{ env.REFERENCE }}', '${{ env.REFERENCE_POLICY }}')
        content = content.replace('template-path: ${{ env.TEMPLATE_PATH}}', 'template-path: ${{ env.TEMPLATE_PATH }}')

    # Fix azure login version
    content = content.replace('azure/login@v4', 'azure/login@v2')

    # Remove duplicate action definitions
    lines = content.split('\n')
    cleaned_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Skip duplicate uses statements
        if re.match(r'\s+uses: danielpalme/ReportGenerator-GitHub-Action@\d+\.\d+\.\d+', line):
            # Check if we already have a uses for this action in recent lines
            recent_lines = cleaned_lines[-5:] if len(cleaned_lines) >= 5 else cleaned_lines
            has_recent_uses = any('danielpalme/ReportGenerator-GitHub-Action' in recent_line for recent_line in recent_lines)

            if not has_recent_uses:
                cleaned_lines.append(line)
        else:
            cleaned_lines.append(line)
        i += 1

    return '\n'.join(cleaned_lines)

def add_missing_names(content):
    """Add missing names to workflow steps."""
    lines = content.split('\n')
    fixed_lines = []

    for i, line in enumerate(lines):
        # Add name to checkout actions that don't have one
        if re.match(r'\s+- uses: actions/checkout@v\d+\s*$', line):
            indent = len(line) - len(line.lstrip())
            fixed_lines.append(' ' * indent + '- name: Checkout repository')
            fixed_lines.append(' ' * (indent + 2) + 'uses: actions/checkout@v4')
        # Add name to other actions without names
        elif re.match(r'\s+- uses: ([^@]+@[^\s]+)\s*$', line):
            indent = len(line) - len(line.lstrip())
            action_name = line.strip().split('uses:')[1].strip().split('@')[0].split('/')[-1]
            action_name = action_name.replace('-', ' ').title()
            fixed_lines.append(' ' * indent + f'- name: {action_name}')
            fixed_lines.append(line)
        else:
            fixed_lines.append(line)

    return '\n'.join(fixed_lines)

def main():
    """Main function to fix workflow files."""

    # Find workflow files in the main directories with errors
    workflow_dirs = [
        '/workspaces/semantic-kernel/.github/workflows',
        '/workspaces/semantic-kernel/04-infrastructure/.github/workflows'
    ]

    fixed_count = 0
    total_count = 0

    for workflow_dir in workflow_dirs:
        if os.path.exists(workflow_dir):
            pattern = os.path.join(workflow_dir, '*.yml')
            for file_path in glob.glob(pattern):
                total_count += 1
                print(f"Processing: {file_path}")

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        original_content = f.read()

                    # Apply fixes
                    content = fix_environment_vars(original_content)
                    content = fix_specific_errors(content, file_path)
                    content = add_missing_names(content)

                    # Only write if changes were made
                    if content != original_content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"  ✓ Fixed {file_path}")
                        fixed_count += 1
                    else:
                        print(f"  - No changes needed for {file_path}")

                except Exception as e:
                    print(f"  ❌ Error processing {file_path}: {e}")

    print(f"\n📊 Summary:")
    print(f"  • Files processed: {total_count}")
    print(f"  • Files fixed: {fixed_count}")

if __name__ == '__main__':
    main()
