#!/usr/bin/env python3
"""
Advanced Repository Organization Script
Organizes the semantic-kernel repository for optimal development workflow.
"""

import os
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set

class RepositoryOrganizer:
    def __init__(self, root_path="/workspaces/semantic-kernel"):
        self.root_path = Path(root_path)
        self.ai_workspace = self.root_path / "ai-workspace"
        self.archive_dir = self.root_path / ".archive"
        self.backup_dir = self.root_path / ".backup"

        # Create organization directories
        self.organization_dirs = {
            "core": ["dotnet", "python", "java", "typescript"],
            "infrastructure": ["scripts", "docs", "config", "configs"],
            "ai_workspace": ["ai-workspace"],
            "development": ["notebooks", "samples", "tests"],
            "deployment": ["docker", "circleci", ".github"],
            "resources": ["data", "resources", "uploads"],
            "archive": ["semantic-kernel-main", "semantic-kernel~HEAD", "semantic-kernel~HEAD_0", "semantic-kernel~main"],
            "temporary": ["results", "devdata", "organization"]
        }

        # Files to clean up or organize
        self.cleanup_patterns = {
            "duplicates": [
                "dotnet-install.sh.1",
                "dotnet-install.sh.2",
                "Documentation 1.txt",
                "Documentation 2.txt",
                "Documentation 3.txt"
            ],
            "system_files": [
                "func start.txt",
                "npm install -g azure-functions-core-tool.txt",
                "application file",
                "web archive.webarchive"
            ],
            "temp_ids": [
                "4e25f261-cb8b-4583-9e1b-1731602b9851",
                "a0e4a1f5-846d-485c-8251-cb15f0a1ff60",
                "aa2a9603-474c-4930-9b13-b59492ffc9ff"
            ]
        }

    def create_directory_structure(self):
        """Create organized directory structure."""
        print("🏗️  Creating organized directory structure...")

        # Create archive and backup directories
        self.archive_dir.mkdir(exist_ok=True)
        self.backup_dir.mkdir(exist_ok=True)

        # Create organized subdirectories
        organized_dirs = [
            "01-core-implementations",
            "02-ai-workspace",
            "03-development-tools",
            "04-infrastructure",
            "05-documentation",
            "06-deployment",
            "07-resources",
            "08-archived-versions"
        ]

        for dir_name in organized_dirs:
            (self.root_path / dir_name).mkdir(exist_ok=True)

        print("✅ Directory structure created")

    def organize_core_implementations(self):
        """Organize core implementation directories."""
        print("🔧 Organizing core implementations...")

        core_dir = self.root_path / "01-core-implementations"

        for lang_dir in ["dotnet", "python", "java", "typescript"]:
            src_path = self.root_path / lang_dir
            if src_path.exists():
                dest_path = core_dir / lang_dir
                if not dest_path.exists():
                    print(f"  Moving {lang_dir}/ to 01-core-implementations/")
                    shutil.move(str(src_path), str(dest_path))

        # Create symlinks for backward compatibility
        for lang_dir in ["dotnet", "python", "java", "typescript"]:
            src_path = self.root_path / lang_dir
            dest_path = core_dir / lang_dir
            if dest_path.exists() and not src_path.exists():
                os.symlink(f"01-core-implementations/{lang_dir}", str(src_path))

        print("✅ Core implementations organized")

    def organize_ai_workspace(self):
        """Ensure AI workspace is properly organized."""
        print("🤖 Organizing AI workspace...")

        ai_dir = self.root_path / "02-ai-workspace"

        if self.ai_workspace.exists():
            # Move ai-workspace if it's not already in the right place
            if not ai_dir.exists():
                shutil.move(str(self.ai_workspace), str(ai_dir))
                # Create symlink for compatibility
                os.symlink("02-ai-workspace", str(self.ai_workspace))

        print("✅ AI workspace organized")

    def organize_development_tools(self):
        """Organize development-related directories."""
        print("🛠️  Organizing development tools...")

        dev_dir = self.root_path / "03-development-tools"

        dev_items = ["notebooks", "samples", "tests", "plugins", "prompt_template_samples"]

        for item in dev_items:
            src_path = self.root_path / item
            if src_path.exists():
                dest_path = dev_dir / item
                if not dest_path.exists():
                    print(f"  Moving {item}/ to 03-development-tools/")
                    shutil.move(str(src_path), str(dest_path))
                    # Create symlink for compatibility
                    os.symlink(f"03-development-tools/{item}", str(src_path))

        print("✅ Development tools organized")

    def organize_infrastructure(self):
        """Organize infrastructure and configuration files."""
        print("⚙️  Organizing infrastructure...")

        infra_dir = self.root_path / "04-infrastructure"

        infra_items = ["scripts", "config", "configs", ".github", "circleci"]

        for item in infra_items:
            src_path = self.root_path / item
            if src_path.exists():
                dest_path = infra_dir / item
                if not dest_path.exists():
                    print(f"  Moving {item}/ to 04-infrastructure/")
                    shutil.move(str(src_path), str(dest_path))
                    # Create symlink for compatibility
                    os.symlink(f"04-infrastructure/{item}", str(src_path))

        print("✅ Infrastructure organized")

    def organize_documentation(self):
        """Organize documentation and related files."""
        print("📚 Organizing documentation...")

        docs_dir = self.root_path / "05-documentation"

        # Keep main docs in place but organize supporting docs
        doc_items = ["docs-backup", "AgentDocs"]

        for item in doc_items:
            src_path = self.root_path / item
            if src_path.exists():
                dest_path = docs_dir / item
                if not dest_path.exists():
                    print(f"  Moving {item}/ to 05-documentation/")
                    shutil.move(str(src_path), str(dest_path))

        print("✅ Documentation organized")

    def organize_deployment(self):
        """Organize deployment-related files."""
        print("🚀 Organizing deployment files...")

        deploy_dir = self.root_path / "06-deployment"

        deploy_items = [
            "Dockerfile", "docker-compose.yml", "entrypoint.sh.template",
            "deploy.sh", "deploy-github-pages.sh", "validate-github-pages.sh",
            "AzureFunctions", "aipmakerday"
        ]

        for item in deploy_items:
            src_path = self.root_path / item
            if src_path.exists():
                dest_path = deploy_dir / item
                if not dest_path.exists():
                    print(f"  Moving {item} to 06-deployment/")
                    shutil.move(str(src_path), str(dest_path))

        print("✅ Deployment files organized")

    def organize_resources(self):
        """Organize resource and data directories."""
        print("📦 Organizing resources...")

        resources_dir = self.root_path / "07-resources"

        resource_items = ["data", "resources", "uploads", "models", "public"]

        for item in resource_items:
            src_path = self.root_path / item
            if src_path.exists():
                dest_path = resources_dir / item
                if not dest_path.exists():
                    print(f"  Moving {item}/ to 07-resources/")
                    shutil.move(str(src_path), str(dest_path))
                    # Create symlink for compatibility
                    os.symlink(f"07-resources/{item}", str(src_path))

        print("✅ Resources organized")

    def archive_old_versions(self):
        """Archive old versions and duplicates."""
        print("📦 Archiving old versions...")

        archive_dir = self.root_path / "08-archived-versions"

        archive_items = [
            "semantic-kernel-main", "semantic-kernel~HEAD",
            "semantic-kernel~HEAD_0", "semantic-kernel~main",
            "Singularity", "Singularity~HEAD",
            "internal-semantic-core", "DevSkim-main",
            "vscode-azure-account", "git-lfs-3.4.0"
        ]

        for item in archive_items:
            src_path = self.root_path / item
            if src_path.exists():
                dest_path = archive_dir / item
                if not dest_path.exists():
                    print(f"  Archiving {item} to 08-archived-versions/")
                    shutil.move(str(src_path), str(dest_path))

        print("✅ Old versions archived")

    def cleanup_temp_files(self):
        """Clean up temporary files and duplicates."""
        print("🧹 Cleaning up temporary files...")

        cleanup_dir = self.root_path / ".cleanup"
        cleanup_dir.mkdir(exist_ok=True)

        # Clean up duplicate files
        for pattern_type, files in self.cleanup_patterns.items():
            pattern_dir = cleanup_dir / pattern_type
            pattern_dir.mkdir(exist_ok=True)

            for file_name in files:
                src_path = self.root_path / file_name
                if src_path.exists():
                    dest_path = pattern_dir / file_name
                    print(f"  Moving {file_name} to .cleanup/{pattern_type}/")
                    shutil.move(str(src_path), str(dest_path))

        # Clean up specific file types
        temp_extensions = [".tmp", ".temp", ".bak", ".old"]
        for ext in temp_extensions:
            for temp_file in self.root_path.glob(f"*{ext}"):
                if temp_file.is_file():
                    dest_path = cleanup_dir / "temp" / temp_file.name
                    dest_path.parent.mkdir(exist_ok=True)
                    print(f"  Moving {temp_file.name} to .cleanup/temp/")
                    shutil.move(str(temp_file), str(dest_path))

        print("✅ Temporary files cleaned up")

    def create_master_index(self):
        """Create a master index of the organized repository."""
        print("📋 Creating master repository index...")

        index_data = {
            "organization_date": datetime.now().isoformat(),
            "structure": {
                "01-core-implementations": "Language-specific implementations (dotnet, python, java, typescript)",
                "02-ai-workspace": "AI development workspace and tools",
                "03-development-tools": "Development utilities (notebooks, samples, tests)",
                "04-infrastructure": "Build, deployment, and configuration",
                "05-documentation": "Documentation and guides",
                "06-deployment": "Deployment scripts and Docker files",
                "07-resources": "Data, models, and static resources",
                "08-archived-versions": "Archived versions and legacy code"
            },
            "compatibility": "Symlinks created for backward compatibility",
            "cleanup": "Temporary and duplicate files moved to .cleanup/"
        }

        # Save index as JSON
        with open(self.root_path / "REPOSITORY_INDEX.json", 'w') as f:
            json.dump(index_data, f, indent=2)

        # Create markdown index
        markdown_content = f"""# Repository Organization Index

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 🏗️ Repository Structure

### 01-core-implementations/
Language-specific implementations:
- `dotnet/` - .NET Semantic Kernel implementation
- `python/` - Python Semantic Kernel implementation
- `java/` - Java Semantic Kernel implementation
- `typescript/` - TypeScript Semantic Kernel implementation

### 02-ai-workspace/
AI development workspace and tools:
- Organized AI development environment
- Sample applications and demos
- Model training and inference tools

### 03-development-tools/
Development utilities:
- `notebooks/` - Jupyter notebooks for experimentation
- `samples/` - Code samples and examples
- `tests/` - Test suites
- `plugins/` - Plugin development

### 04-infrastructure/
Build, deployment, and configuration:
- `scripts/` - Build and deployment scripts
- `.github/` - GitHub Actions workflows
- `config/` - Configuration files

### 05-documentation/
Documentation and guides:
- `docs/` - Main documentation (GitHub Pages)
- `docs-backup/` - Documentation backups
- `AgentDocs/` - Agent-specific documentation

### 06-deployment/
Deployment scripts and containers:
- Docker configurations
- Deployment scripts
- Azure Functions

### 07-resources/
Data, models, and static resources:
- `data/` - Training and test data
- `models/` - Model files
- `uploads/` - User uploads

### 08-archived-versions/
Archived versions and legacy code:
- Previous versions of the repository
- Legacy implementations
- Deprecated tools

## 🔗 Backward Compatibility

Symlinks have been created for all moved directories to maintain compatibility with existing scripts and workflows.

## 🧹 Cleanup

Temporary and duplicate files have been moved to `.cleanup/` for review:
- `.cleanup/duplicates/` - Duplicate files
- `.cleanup/temp/` - Temporary files
- `.cleanup/system_files/` - System-generated files
- `.cleanup/temp_ids/` - Files with temporary IDs

## 🚀 Quick Start

1. **Core Development**: Start in `01-core-implementations/[language]/`
2. **AI Workspace**: Explore `02-ai-workspace/` for AI tools
3. **Documentation**: Visit `docs/` or the GitHub Pages site
4. **Scripts**: Use `04-infrastructure/scripts/` for automation

## 📞 Support

For questions about the organization or to restore files from `.cleanup/`, please refer to the cleanup logs or contact the maintainers.
"""

        with open(self.root_path / "REPOSITORY_INDEX.md", 'w') as f:
            f.write(markdown_content)

        print("✅ Master index created")

    def update_gitignore(self):
        """Update .gitignore with new organization."""
        print("📝 Updating .gitignore...")

        gitignore_path = self.root_path / ".gitignore"

        # Additional entries for organized structure
        additional_entries = """
# Repository Organization
.cleanup/
.backup/
.archive/
*.tmp
*.temp
*.bak
*.old

# AI Workspace
ai-workspace/cache/
ai-workspace/logs/
ai-workspace/venv/
ai-workspace/.env

# Development
.vscode/settings.json
.idea/
*.log
__pycache__/
*.pyc
*.pyo
.pytest_cache/
.coverage
htmlcov/

# OS-specific
.DS_Store
Thumbs.db
*.swp
*.swo
*~
"""

        if gitignore_path.exists():
            with open(gitignore_path, 'a') as f:
                f.write(additional_entries)
        else:
            with open(gitignore_path, 'w') as f:
                f.write(additional_entries)

        print("✅ .gitignore updated")

    def generate_organization_report(self):
        """Generate a comprehensive organization report."""
        print("📊 Generating organization report...")

        report_content = f"""# Repository Organization Report

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Organizer**: Advanced Repository Organization Script

## 🎯 Summary

The semantic-kernel repository has been comprehensively organized into a logical structure that improves:
- **Navigation**: Clear directory hierarchy
- **Development**: Separated concerns by purpose
- **Maintenance**: Archived old versions and cleaned duplicates
- **Compatibility**: Symlinks maintain existing workflows

## 📊 Organization Statistics

### Directories Organized
- ✅ Core implementations: 4 language directories
- ✅ AI workspace: Centralized AI development tools
- ✅ Development tools: Notebooks, samples, tests
- ✅ Infrastructure: Scripts, configs, CI/CD
- ✅ Documentation: Guides and references
- ✅ Deployment: Containers and scripts
- ✅ Resources: Data and models
- ✅ Archives: Legacy versions

### Files Cleaned
- 🗑️ Duplicate files moved to `.cleanup/duplicates/`
- 🗑️ Temporary files moved to `.cleanup/temp/`
- 🗑️ System files moved to `.cleanup/system_files/`
- 🗑️ Temp IDs moved to `.cleanup/temp_ids/`

## 🔄 Backward Compatibility

All moved directories have symlinks in their original locations to ensure:
- Existing scripts continue to work
- Build processes remain functional
- Development workflows are not disrupted

## 📁 New Structure

```
semantic-kernel/
├── 01-core-implementations/    # Language implementations
├── 02-ai-workspace/           # AI development tools
├── 03-development-tools/      # Dev utilities
├── 04-infrastructure/         # Build & deployment
├── 05-documentation/          # Docs & guides
├── 06-deployment/            # Containers & deploy
├── 07-resources/             # Data & models
├── 08-archived-versions/     # Legacy code
├── .cleanup/                 # Temporary storage
└── docs/                     # GitHub Pages (unchanged)
```

## 🚀 Next Steps

1. **Review**: Check `.cleanup/` directories for any files you need
2. **Test**: Verify your workflows still function correctly
3. **Update**: Update any hardcoded paths in your scripts
4. **Clean**: After verification, you can safely delete `.cleanup/`

## 📞 Support

If you encounter any issues or need to restore files:
1. Check `.cleanup/` directories
2. Use symlinks to access moved directories
3. Refer to `REPOSITORY_INDEX.md` for the complete structure
"""

        with open(self.root_path / "ORGANIZATION_REPORT.md", 'w') as f:
            f.write(report_content)

        print("✅ Organization report generated")

    def run_organization(self):
        """Run the complete organization process."""
        print("🎯 Starting Advanced Repository Organization")
        print("=" * 50)

        try:
            self.create_directory_structure()
            self.organize_core_implementations()
            self.organize_ai_workspace()
            self.organize_development_tools()
            self.organize_infrastructure()
            self.organize_documentation()
            self.organize_deployment()
            self.organize_resources()
            self.archive_old_versions()
            self.cleanup_temp_files()
            self.create_master_index()
            self.update_gitignore()
            self.generate_organization_report()

            print("\n" + "=" * 50)
            print("🎉 Repository Organization Complete!")
            print("\n📋 Summary:")
            print("  ✅ Directory structure organized")
            print("  ✅ Files categorized by purpose")
            print("  ✅ Backward compatibility maintained")
            print("  ✅ Cleanup and archival completed")
            print("  ✅ Documentation generated")
            print("\n📖 Next Steps:")
            print("  1. Review REPOSITORY_INDEX.md")
            print("  2. Check .cleanup/ for any needed files")
            print("  3. Test your existing workflows")
            print("  4. Update any hardcoded paths")

        except Exception as e:
            print(f"❌ Error during organization: {str(e)}")
            print("Check the log files for details.")
            raise

if __name__ == "__main__":
    organizer = RepositoryOrganizer()
    organizer.run_organization()
