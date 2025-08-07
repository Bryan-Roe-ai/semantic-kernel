#!/usr/bin/env python3
"""
Comprehensive File Organizer module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

import os
import shutil
import json
import logging
from pathlib import Path
from datetime import datetime
import hashlib

class SemanticKernelOrganizer:
    def __init__(self, repo_root):
        self.repo_root = Path(repo_root)
        self.cleanup_dir = self.repo_root / ".cleanup"
        self.backup_dir = self.repo_root / ".organization_backup"

        # Setup logging
        self.setup_logging()

        # Organization rules
        self.organization_rules = {
            # AGI and AI Development Files
            "09-agi-development": {
                "patterns": [
                    "agi_*.py", "agi_*.log", "agi_*.md", "agi_*.json", "agi_*.ipynb",
                    "AGI_*.md", "AI_*.md", "*agi*.html", "*agi*.sh", "*agi*.hta",
                    "consciousness_*.ipynb", "neural_symbolic_*.ipynb"
                ],
                "description": "AGI and AI development files"
            },

            # Configuration and Setup Files
            "10-configuration": {
                "patterns": [
                    "*.config", "*.json", "nuget.config", "vcpkg-configuration.jsonc",
                    "gpu_*.json", "workspace_*.json", "*config*.json", "auto-test-config.json"
                ],
                "exclude_patterns": ["package.json", "tsconfig.json"],
                "description": "Configuration files"
            },

            # Scripts and Automation
            "11-automation-scripts": {
                "patterns": [
                    "*.sh", "*.ps1", "*.py", "launch_*.sh", "setup_*.sh",
                    "check_*.sh", "run-*.sh", "simple-*.sh"
                ],
                "exclude_existing": True,
                "description": "Automation and utility scripts"
            },

            # Documentation and Guides
            "12-documentation": {
                "patterns": [
                    "*.md", "*_GUIDE.md", "*_README.md", "*_INSTRUCTIONS.md",
                    "*_COMPLETE.md", "*_SUMMARY.md"
                ],
                "exclude_existing": True,
                "description": "Documentation and guides"
            },

            # Testing and Quality Assurance
            "13-testing": {
                "patterns": [
                    "*test*.py", "*test*.cs", "*test*.sh", "AutoTest*",
                    "consumer.robot", "producer.robot", "reporter.robot",
                    "simple_agi_test.py"
                ],
                "description": "Testing and QA files"
            },

            # Build and Runtime Files
            "14-runtime": {
                "patterns": [
                    "*.exe", "*.dll", "*.app", "*.jar", "*.war",
                    "dotnet-runtime-*.exe", "RuntimeException.java"
                ],
                "description": "Runtime and executable files"
            },

            # Web and UI Components
            "15-web-ui": {
                "patterns": [
                    "*.html", "*.css", "*.js", "*.json", "*.xml", "*.xsl",
                    "server.js", "express-rate.js", "sw.js", "style.xsl"
                ],
                "exclude_patterns": ["package.json", "tsconfig.json"],
                "description": "Web and UI files"
            },

            # Project Extensions and Tools
            "16-extensions": {
                "patterns": [
                    "vscode-*", "*extension*", "DevSkim/", "Microsoft.DevSkim.*"
                ],
                "description": "VS Code extensions and development tools"
            },

            # Temporary and Cache Files
            "17-temporary": {
                "patterns": [
                    "__pycache__/", "*.pyc", "*.tmp", ".cache/", "logs/",
                    "__azurite_db_*.json", "__*storage__/", "*.log"
                ],
                "description": "Temporary and cache files"
            },

            # Data and Resources
            "18-data": {
                "patterns": [
                    "data/", "devdata/", "results/", "output.xml",
                    "references.fsx", "defaults/", "home/"
                ],
                "description": "Data files and resources"
            }
        }

    def setup_logging(self):
        """Setup logging configuration"""
        log_file = self.repo_root / "organization.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def create_directories(self):
        """Create organization directories"""
        self.logger.info("Creating organization directories...")

        for dir_name, config in self.organization_rules.items():
            target_dir = self.repo_root / dir_name
            target_dir.mkdir(exist_ok=True)

            # Create README for each directory
            readme_content = f"# {dir_name.replace('-', ' ').title()}\n\n{config['description']}\n"
            readme_file = target_dir / "README.md"
            if not readme_file.exists():
                readme_file.write_text(readme_content)

        # Create cleanup and backup directories
        self.cleanup_dir.mkdir(exist_ok=True)
        self.backup_dir.mkdir(exist_ok=True)

    def should_exclude_file(self, file_path, patterns=None):
        """Check if file should be excluded from organization"""
        exclude_patterns = patterns or []
        file_name = file_path.name

        # Always exclude certain system files and directories
        system_excludes = [
            '.git', '.vscode', '.github', 'node_modules', '.env',
            'package-lock.json', 'yarn.lock', '.gitignore', '.gitattributes'
        ]

        if any(pattern in str(file_path) for pattern in system_excludes):
            return True

        if any(file_name.endswith(pattern) or pattern in file_name for pattern in exclude_patterns):
            return True

        return False

    def matches_pattern(self, file_path, patterns):
        """Check if file matches any of the given patterns"""
        file_name = file_path.name

        for pattern in patterns:
            if pattern.endswith('/') and file_path.is_dir():
                if file_name == pattern.rstrip('/'):
                    return True
            elif '*' in pattern:
                import fnmatch
                if fnmatch.fnmatch(file_name, pattern):
                    return True
            elif pattern in file_name or file_name.startswith(pattern):
                return True

        return False

    def move_file_safely(self, source, target_dir, create_symlink=True):
        """Move file safely with backup and optional symlink creation"""
        source_path = Path(source)
        target_dir_path = Path(target_dir)
        target_path = target_dir_path / source_path.name

        # Create backup if file already exists
        if target_path.exists():
            backup_path = self.backup_dir / f"{source_path.name}.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            shutil.move(str(target_path), str(backup_path))
            self.logger.info(f"Backed up existing file: {target_path} -> {backup_path}")

        # Move the file
        try:
            shutil.move(str(source_path), str(target_path))
            self.logger.info(f"Moved: {source_path} -> {target_path}")

            # Create symlink for backward compatibility
            if create_symlink and not source_path.exists():
                try:
                    os.symlink(str(target_path), str(source_path))
                    self.logger.info(f"Created symlink: {source_path} -> {target_path}")
                except OSError as e:
                    self.logger.warning(f"Could not create symlink {source_path}: {e}")

            return True
        except Exception as e:
            self.logger.error(f"Error moving {source_path} to {target_path}: {e}")
            return False

    def organize_files(self):
        """Organize files according to the rules"""
        self.logger.info("Starting file organization...")

        # Get all files and directories in root
        items = [item for item in self.repo_root.iterdir()
                if not item.name.startswith('.') and
                not item.name.startswith('0') and  # Skip already organized dirs
                item.name not in ['docs', 'README.md', 'LICENSE']]

        organized_count = 0

        for item in items:
            organized = False

            for dir_name, config in self.organization_rules.items():
                patterns = config.get('patterns', [])
                exclude_patterns = config.get('exclude_patterns', [])
                exclude_existing = config.get('exclude_existing', False)

                # Skip if file should be excluded
                if self.should_exclude_file(item, exclude_patterns):
                    continue

                # Skip if exclude_existing and file is already in organized structure
                if exclude_existing and any(item.name in str(p) for p in self.repo_root.glob('*/') if p.name.startswith('0')):
                    continue

                # Check if item matches patterns
                if self.matches_pattern(item, patterns):
                    target_dir = self.repo_root / dir_name
                    if self.move_file_safely(item, target_dir):
                        organized = True
                        organized_count += 1
                        break

            # If not organized by rules, move to miscellaneous
            if not organized and item.exists():
                misc_dir = self.repo_root / "19-miscellaneous"
                misc_dir.mkdir(exist_ok=True)
                if self.move_file_safely(item, misc_dir):
                    organized_count += 1

        self.logger.info(f"Organization complete. {organized_count} items organized.")
        return organized_count

    def create_index(self):
        """Create comprehensive index of organized structure"""
        self.logger.info("Creating organization index...")

        index = {
            "organization_date": datetime.now().isoformat(),
            "total_directories": 0,
            "total_files": 0,
            "structure": {}
        }

        for item in sorted(self.repo_root.iterdir()):
            if item.is_dir() and not item.name.startswith('.'):
                dir_info = {
                    "type": "directory",
                    "files": [],
                    "subdirectories": []
                }

                try:
                    for subitem in sorted(item.iterdir()):
                        if subitem.is_file():
                            dir_info["files"].append(subitem.name)
                            index["total_files"] += 1
                        elif subitem.is_dir():
                            dir_info["subdirectories"].append(subitem.name)
                except PermissionError:
                    dir_info["error"] = "Permission denied"

                index["structure"][item.name] = dir_info
                index["total_directories"] += 1

        # Save index
        index_file = self.repo_root / "COMPREHENSIVE_ORGANIZATION_INDEX.json"
        with open(index_file, 'w') as f:
            json.dump(index, f, indent=2)

        # Create markdown summary
        self.create_markdown_summary(index)

        return index

    def create_markdown_summary(self, index):
        """Create markdown summary of organization"""
        summary_content = f"""# Comprehensive Repository Organization Summary

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Organizer**: Comprehensive File Organizer

## 📊 Organization Statistics

- **Total Directories**: {index['total_directories']}
- **Total Files**: {index['total_files']}
- **Organization Categories**: {len([k for k in index['structure'].keys() if k.startswith('0') or k.startswith('1')])}

## 🗂️ Directory Structure

"""

        for dir_name, info in sorted(index['structure'].items()):
            if isinstance(info, dict):
                file_count = len(info.get('files', []))
                subdir_count = len(info.get('subdirectories', []))
                summary_content += f"- **{dir_name}**: {file_count} files, {subdir_count} subdirectories\n"

        summary_content += """
## 🎯 Organization Categories

### Core Implementation (01-08)
- Language-specific implementations
- AI workspace and development tools
- Infrastructure and deployment
- Documentation and resources

### Specialized Categories (09-19)
- AGI development files
- Configuration management
- Automation scripts
- Testing and QA
- Runtime and executables
- Web and UI components
- Extensions and tools
- Temporary files and cache
- Data and resources
- Miscellaneous items

## 🔗 Backward Compatibility

All moved files maintain symlinks to their original locations for backward compatibility.

## 📞 Support

If you need to locate a file:
1. Check the comprehensive index: `COMPREHENSIVE_ORGANIZATION_INDEX.json`
2. Use the directory structure above
3. Check symlinks in the root directory
"""

        summary_file = self.repo_root / "COMPREHENSIVE_ORGANIZATION_SUMMARY.md"
        summary_file.write_text(summary_content)

    def run_organization(self):
        """Run the complete organization process"""
        self.logger.info("Starting comprehensive repository organization...")

        try:
            # Create directory structure
            self.create_directories()

            # Organize files
            organized_count = self.organize_files()

            # Create index
            index = self.create_index()

            self.logger.info(f"Organization completed successfully!")
            self.logger.info(f"- {organized_count} items organized")
            self.logger.info(f"- {index['total_directories']} directories indexed")
            self.logger.info(f"- {index['total_files']} files cataloged")

            return True

        except Exception as e:
            self.logger.error(f"Organization failed: {e}")
            return False

def main():
    """Main function"""
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    organizer = SemanticKernelOrganizer(repo_root)

    success = organizer.run_organization()

    if success:
        print("\n🎉 Repository organization completed successfully!")
        print("📁 Check COMPREHENSIVE_ORGANIZATION_SUMMARY.md for details")
        print("📋 Full index available in COMPREHENSIVE_ORGANIZATION_INDEX.json")
    else:
        print("\n❌ Organization failed. Check organization.log for details")

    return 0 if success else 1

if __name__ == "__main__":
    exit(main())
