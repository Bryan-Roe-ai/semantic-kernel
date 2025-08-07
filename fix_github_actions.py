#!/usr/bin/env python3
"""
Script to fix GitHub Actions workflows by updating outdated action versions
and fixing common issues.
"""

import os
import re
import glob
from pathlib import Path


def update_action_versions(content):
    """Update outdated action versions to latest versions."""
    
    # Action version mappings (old -> new)
    version_updates = {
        'actions/checkout@v1': 'actions/checkout@v4',
        'actions/checkout@v2': 'actions/checkout@v4',
        'actions/checkout@v3': 'actions/checkout@v4',
        'actions/setup-node@v1': 'actions/setup-node@v4',
        'actions/setup-node@v2': 'actions/setup-node@v4',
        'actions/setup-node@v3': 'actions/setup-node@v4',
        'actions/setup-python@v1': 'actions/setup-python@v5',
        'actions/setup-python@v2': 'actions/setup-python@v5',
        'actions/setup-python@v3': 'actions/setup-python@v5',
        'actions/setup-python@v4': 'actions/setup-python@v5',
        'actions/setup-dotnet@v1': 'actions/setup-dotnet@v4',
        'actions/setup-dotnet@v2': 'actions/setup-dotnet@v4',
        'actions/setup-dotnet@v3': 'actions/setup-dotnet@v4',
        'actions/cache@v1': 'actions/cache@v4',
        'actions/cache@v2': 'actions/cache@v4',
        'actions/cache@v3': 'actions/cache@v4',
        'actions/upload-artifact@v1': 'actions/upload-artifact@v4',
        'actions/upload-artifact@v2': 'actions/upload-artifact@v4',
        'actions/upload-artifact@v3': 'actions/upload-artifact@v4',
        'actions/download-artifact@v1': 'actions/download-artifact@v4',
        'actions/download-artifact@v2': 'actions/download-artifact@v4',
        'actions/download-artifact@v3': 'actions/download-artifact@v4',
        'docker/login-action@v1': 'docker/login-action@v3',
        'docker/login-action@v2': 'docker/login-action@v3',
        'docker/build-push-action@v1': 'docker/build-push-action@v5',
        'docker/build-push-action@v2': 'docker/build-push-action@v5',
        'docker/build-push-action@v3': 'docker/build-push-action@v5',
        'docker/build-push-action@v4': 'docker/build-push-action@v5',
        'azure/webapps-deploy@v1': 'azure/webapps-deploy@v3',
        'azure/webapps-deploy@v2': 'azure/webapps-deploy@v3',
    }
    
    updated_content = content
    changes_made = []
    
    for old_version, new_version in version_updates.items():
        if old_version in updated_content:
            updated_content = updated_content.replace(old_version, new_version)
            changes_made.append(f"{old_version} -> {new_version}")
    
    return updated_content, changes_made


def add_timeout_to_jobs(content):
    """Add timeout-minutes to jobs that don't have it."""
    
    # Pattern to match job definitions
    job_pattern = r'(  \w+:\s*\n\s+runs-on: [^\n]+)'
    
    def add_timeout(match):
        job_def = match.group(1)
        if 'timeout-minutes:' not in job_def:
            return job_def + '\n    timeout-minutes: 30'
        return job_def
    
    updated_content = re.sub(job_pattern, add_timeout, content)
    return updated_content


def add_workflow_dispatch(content):
    """Add workflow_dispatch to workflows that don't have it."""
    
    if 'workflow_dispatch:' not in content and 'on:' in content:
        # Find the 'on:' section and add workflow_dispatch
        pattern = r'(on:\s*\n(?:  [^\n]+\n)*)'
        match = re.search(pattern, content)
        if match:
            on_section = match.group(1)
            if not on_section.strip().endswith('workflow_dispatch:'):
                new_on_section = on_section.rstrip() + '\n  workflow_dispatch:\n'
                content = content.replace(on_section, new_on_section)
                return content, True
    
    return content, False


def fix_common_issues(content):
    """Fix common issues in GitHub Actions workflows."""
    
    changes_made = []
    
    # Add error handling for script execution
    if './fix-errors.sh' in content and 'chmod +x' not in content:
        content = content.replace(
            'run: ./fix-errors.sh',
            'run: |\n          chmod +x ./fix-errors.sh\n          ./fix-errors.sh'
        )
        changes_made.append("Added chmod +x for fix-errors.sh")
    
    # Fix Python version format (strings instead of numbers)
    def fix_python_versions(match):
        versions = match.group(1)
        quoted_versions = "', '".join(versions.split(', '))
        return f"python-version: ['{quoted_versions}']"
    
    content = re.sub(r'python-version: \[([0-9.]+(?:, [0-9.]+)*)\]', 
                     fix_python_versions, 
                     content)
    
    # Add cache for Python setup
    if 'setup-python@v5' in content and "cache: 'pip'" not in content:
        content = re.sub(
            r'(uses: actions/setup-python@v5\s*\n\s*with:\s*\n\s*python-version: [^\n]+)',
            r'\1\n          cache: \'pip\'',
            content
        )
        changes_made.append("Added pip cache to Python setup")
    
    # Add cache for Node setup
    if 'setup-node@v4' in content and "cache: 'npm'" not in content:
        content = re.sub(
            r'(uses: actions/setup-node@v4\s*\n\s*with:\s*\n\s*node-version: [^\n]+)',
            r'\1\n          cache: \'npm\'',
            content
        )
        changes_made.append("Added npm cache to Node setup")
    
    return content, changes_made


def process_workflow_file(file_path):
    """Process a single workflow file."""
    
    print(f"Processing {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        all_changes = []
        
        # Update action versions
        content, version_changes = update_action_versions(content)
        all_changes.extend(version_changes)
        
        # Add timeouts
        content = add_timeout_to_jobs(content)
        
        # Add workflow_dispatch
        content, dispatch_added = add_workflow_dispatch(content)
        if dispatch_added:
            all_changes.append("Added workflow_dispatch trigger")
        
        # Fix common issues
        content, fix_changes = fix_common_issues(content)
        all_changes.extend(fix_changes)
        
        # Write back if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  ✅ Updated {file_path}")
            for change in all_changes:
                print(f"    - {change}")
        else:
            print(f"  ℹ️  No changes needed for {file_path}")
            
    except Exception as e:
        print(f"  ❌ Error processing {file_path}: {e}")


def main():
    """Main function to process all workflow files."""
    
    print("🔧 Fixing GitHub Actions workflows...")
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
    
    print(f"Found {len(workflow_files)} workflow files to process")
    print()
    
    for file_path in sorted(workflow_files):
        process_workflow_file(file_path)
        print()
    
    print("=" * 50)
    print("✅ GitHub Actions fix completed!")
    
    # Create summary
    print("\n📋 Summary of fixes applied:")
    print("  - Updated action versions to latest")
    print("  - Added timeout-minutes to jobs")
    print("  - Added workflow_dispatch triggers")
    print("  - Added caching for Python and Node setups")
    print("  - Fixed script execution permissions")
    print("  - Fixed Python version format")


if __name__ == "__main__":
    main()
