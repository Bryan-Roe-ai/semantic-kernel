#!/usr/bin/env python3
"""
Selective Copyright Header Tool

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This script adds copyright headers to key source files in the project.
"""

from pathlib import Path


class SelectiveCopyrightHeaders:
    """Add copyright headers to key files only."""
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.author = "Bryan Roe"
        self.year = "2025"
        self.project = "Semantic Kernel - Advanced AI Development Framework"
    
    def get_file_description(self, file_path: Path) -> str:
        """Generate appropriate description for file."""
        name = file_path.stem.replace('_', ' ').title()
        parent = file_path.parent.name
        
        if 'test' in file_path.name.lower():
            return f"Test module for {name}"
        elif 'demo' in file_path.name.lower():
            return f"Demo script for {name}"
        elif 'cli' in file_path.name.lower():
            return f"Command line interface for {name}"
        elif 'runner' in file_path.name.lower():
            return f"Runner module for {name}"
        elif 'processor' in file_path.name.lower():
            return f"Processing module for {name}"
        elif 'manager' in file_path.name.lower():
            return f"Management module for {name}"
        elif 'setup' in file_path.name.lower():
            return f"Setup and configuration module for {name}"
        else:
            return f"{name} module"
    
    def create_python_header(self, description: str) -> str:
        """Create Python copyright header."""
        return f'''#!/usr/bin/env python3
"""
{description}

Copyright (c) {self.year} {self.author}
Licensed under the MIT License

Part of the {self.project}
Author: {self.author}
"""

'''
    
    def create_js_header(self, description: str) -> str:
        """Create JavaScript/TypeScript copyright header."""
        return f'''/**
 * {description}
 * 
 * Copyright (c) {self.year} {self.author}
 * Licensed under the MIT License
 * 
 * Part of the {self.project}
 * Author: {self.author}
 */

'''
    
    def create_cs_header(self, description: str) -> str:
        """Create C# copyright header."""
        return f'''/*
 * {description}
 * 
 * Copyright (c) {self.year} {self.author}
 * Licensed under the MIT License
 * 
 * Part of the {self.project}
 * Author: {self.author}
 */

'''
    
    def has_copyright_header(self, file_path: Path) -> bool:
        """Check if file already has copyright header."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read(1000)
                return f'Copyright (c) {self.year} {self.author}' in content
        except:
            return True
    
    def add_header_to_file(self, file_path: Path, header: str) -> bool:
        """Add header to a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Skip if already has shebang and copyright
            if content.startswith('#!/') and 'Copyright' in content[:500]:
                return False
            
            # Handle shebang for Python files
            if file_path.suffix == '.py' and content.startswith('#!/'):
                lines = content.split('\n', 1)
                if len(lines) > 1:
                    # Replace shebang and add header
                    new_content = header + lines[1]
                else:
                    new_content = header + content
            else:
                new_content = header + content
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            return True
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return False
    
    def process_key_files(self):
        """Process key files in the project."""
        print(f"🔍 Adding copyright headers to key files...")
        
        # Key directories to process
        key_dirs = [
            '',  # Root directory
            '02-ai-workspace',
            '03-development-tools',
            '09-agi-development'
        ]
        
        # Key file patterns
        key_patterns = [
            '*cli*.py',
            '*runner*.py',
            '*processor*.py',
            '*manager*.py',
            '*setup*.py',
            '*demo*.py',
            '*test*.py',
            'main.py',
            'app.py',
            'server.py'
        ]
        
        processed = {
            'python': 0,
            'javascript': 0,
            'csharp': 0
        }
        
        for dir_name in key_dirs:
            if dir_name:
                base_path = self.workspace_root / dir_name
            else:
                base_path = self.workspace_root
            
            if not base_path.exists():
                continue
            
            print(f"\n📁 Processing directory: {dir_name or 'root'}")
            
            # Process key Python files
            for pattern in key_patterns:
                for file_path in base_path.glob(pattern):
                    if file_path.is_file() and not self.has_copyright_header(file_path):
                        description = self.get_file_description(file_path)
                        header = self.create_python_header(description)
                        if self.add_header_to_file(file_path, header):
                            print(f"  ✅ Added header to {file_path.name}")
                            processed['python'] += 1
            
            # Process key JavaScript/TypeScript files
            for ext in ['*.js', '*.ts']:
                for file_path in base_path.glob(ext):
                    if (file_path.is_file() and 
                        not self.has_copyright_header(file_path) and
                        'node_modules' not in str(file_path)):
                        description = self.get_file_description(file_path)
                        header = self.create_js_header(description)
                        if self.add_header_to_file(file_path, header):
                            print(f"  ✅ Added header to {file_path.name}")
                            processed['javascript'] += 1
            
            # Process key C# files
            for file_path in base_path.glob('*.cs'):
                if (file_path.is_file() and 
                    not self.has_copyright_header(file_path) and
                    'bin' not in str(file_path) and 'obj' not in str(file_path)):
                    description = self.get_file_description(file_path)
                    header = self.create_cs_header(description)
                    if self.add_header_to_file(file_path, header):
                        print(f"  ✅ Added header to {file_path.name}")
                        processed['csharp'] += 1
        
        return processed
    
    def run(self):
        """Run the selective copyright header addition."""
        print("Selective Copyright Header Tool")
        print("=" * 35)
        print(f"Author: {self.author}")
        print(f"Project: {self.project}")
        print(f"Workspace: {self.workspace_root}")
        
        processed = self.process_key_files()
        
        print(f"\n🎉 Copyright header addition complete!")
        print(f"\n📊 Summary:")
        print(f"  • Python files: {processed['python']}")
        print(f"  • JavaScript/TypeScript files: {processed['javascript']}")
        print(f"  • C# files: {processed['csharp']}")
        print(f"  • Total files processed: {sum(processed.values())}")

def main():
    """Main function."""
    workspace_root = Path(__file__).parent
    tool = SelectiveCopyrightHeaders(workspace_root)
    
    response = input("❓ Add copyright headers to key files? (y/N): ")
    if response.lower() == 'y':
        tool.run()
    else:
        print("❌ Operation cancelled.")

if __name__ == "__main__":
    main()
