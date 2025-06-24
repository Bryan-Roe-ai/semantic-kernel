#!/usr/bin/env python3
"""
Copyright Header Automation Script

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This script automatically adds proper copyright headers to all Python files
in the workspace that don't already have them.

Author: Bryan Roe
Created: 2025
License: MIT
"""

import os
import re
from pathlib import Path
from typing import List, Set

# Copyright header template for Python files
PYTHON_COPYRIGHT_HEADER = '''#!/usr/bin/env python3
"""
{description}

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

'''

# Directories to skip
SKIP_DIRS = {
    '__pycache__',
    '.git',
    'node_modules',
    '.vscode',
    'venv',
    'env',
    '.env',
    'dist',
    'build',
    '08-archived-versions'  # Skip archived versions to preserve original attribution
}

# Files to skip (by name or pattern)
SKIP_FILES = {
    '__init__.py',  # Usually minimal files
    'setup.py',
    'conftest.py'
}

def has_copyright_header(file_path: Path) -> bool:
    """Check if file already has a copyright header."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read(500)  # Check first 500 chars
            return 'Copyright (c) 2025 Bryan Roe' in content or 'Copyright (c) Bryan Roe' in content
    except Exception:
        return True  # Skip files we can't read

def get_file_description(file_path: Path) -> str:
    """Generate a description based on file name and location."""
    name = file_path.stem
    parent = file_path.parent.name
    
    # Custom descriptions for specific files
    descriptions = {
        'enhanced_ai_runner': 'Enhanced AI Markdown Runner with advanced processing capabilities',
        'ai_markdown_runner': 'AI Markdown Runner for intelligent content processing',
        'ai_markdown_processor': 'AI Markdown Processor for automated content handling',
        'agi_cli': 'AGI Command Line Interface for AI development tools',
        'test_ai_runner': 'Test suite for AI Runner functionality',
        'demo_local_agents': 'Demonstration of local AI agents and capabilities',
        'local_agent_launcher': 'Local Agent Launcher for AI system management',
        'agi_status_dashboard': 'AGI Status Dashboard for system monitoring',
        'fake_local_llm': 'Local LLM Simulation for testing and development',
        'collect_md_for_ai': 'Markdown Collection Tool for AI processing',
        'run_md_ai': 'Markdown to AI Processing Pipeline',
        'run_md_as_ai_demo': 'Demonstration of Markdown AI Processing',
    }
    
    if name in descriptions:
        return descriptions[name]
    
    # Generate description based on file location and name
    if 'test' in name.lower():
        return f'Test module for {name.replace("test_", "").replace("_", " ")}'
    elif 'demo' in name.lower():
        return f'Demonstration module for {name.replace("demo_", "").replace("_", " ")}'
    elif 'ai' in name.lower():
        return f'AI module for {name.replace("_", " ")}'
    elif 'agi' in name.lower():
        return f'AGI module for {name.replace("_", " ")}'
    else:
        return f'{name.replace("_", " ").title()} module'

def find_python_files(root_dir: Path) -> List[Path]:
    """Find all Python files that need copyright headers."""
    python_files = []
    
    for file_path in root_dir.rglob('*.py'):
        # Skip if in excluded directory
        if any(skip_dir in str(file_path) for skip_dir in SKIP_DIRS):
            continue
            
        # Skip if excluded file
        if file_path.name in SKIP_FILES:
            continue
            
        # Skip if already has copyright header
        if has_copyright_header(file_path):
            continue
            
        python_files.append(file_path)
    
    return python_files

def add_copyright_header(file_path: Path) -> bool:
    """Add copyright header to a Python file."""
    try:
        # Read current content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Get description for this file
        description = get_file_description(file_path)
        
        # Generate header
        header = PYTHON_COPYRIGHT_HEADER.format(description=description)
        
        # Remove existing shebang if present
        if content.startswith('#!'):
            lines = content.split('\n')
            content = '\n'.join(lines[1:])
        
        # Remove existing docstring if it's the first thing
        if content.strip().startswith('"""') or content.strip().startswith("'''"):
            # Find end of docstring
            quote_type = '"""' if content.strip().startswith('"""') else "'''"
            start = content.find(quote_type)
            end = content.find(quote_type, start + 3)
            if end != -1:
                content = content[end + 3:].lstrip('\n')
        
        # Combine header and content
        new_content = header + content
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main function to process all Python files."""
    root_dir = Path(__file__).parent
    
    print("🔍 Scanning for Python files that need copyright headers...")
    python_files = find_python_files(root_dir)
    
    if not python_files:
        print("✅ All Python files already have proper copyright headers!")
        return
    
    print(f"📝 Found {len(python_files)} files that need copyright headers:")
    for file_path in python_files:
        rel_path = file_path.relative_to(root_dir)
        print(f"  • {rel_path}")
    
    response = input(f"\n❓ Add copyright headers to {len(python_files)} files? (y/N): ")
    if response.lower() != 'y':
        print("❌ Operation cancelled.")
        return
    
    print("\n📝 Adding copyright headers...")
    success_count = 0
    
    for file_path in python_files:
        rel_path = file_path.relative_to(root_dir)
        if add_copyright_header(file_path):
            print(f"  ✅ {rel_path}")
            success_count += 1
        else:
            print(f"  ❌ {rel_path}")
    
    print(f"\n🎉 Successfully added copyright headers to {success_count}/{len(python_files)} files!")
    print("\n📋 Summary:")
    print(f"  • Files processed: {len(python_files)}")
    print(f"  • Successfully updated: {success_count}")
    print(f"  • Errors: {len(python_files) - success_count}")

if __name__ == "__main__":
    main()
