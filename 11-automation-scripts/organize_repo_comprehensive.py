#!/usr/bin/env python3
"""
Comprehensive Repository Organization Script
Organizes all remaining files in the semantic-kernel repository
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime

class RepositoryOrganizer:
    def __init__(self, repo_root="/workspaces/semantic-kernel"):
        self.repo_root = Path(repo_root)
        self.moved_files = []
        self.created_symlinks = []

        # Define the organization structure
        self.organization_map = {
            # Configuration files
            "10-configuration": [
                "agent_behavior_config.json",
                "agent_config.json",
                "llm_config.json",
                "rtx4050_optimization_config.json",
                "repository_status_report.json",
                "agi_roadmap_status.json",
                ".agi_file_config.json",
                "{file}.json",
                "Untitled-1.json"
            ],

            # Automation and Scripts
            "11-automation-scripts": [
                "add_copyright_headers.py",
                "add_selective_headers.py",
                "agi_cli.py",
                "auto_codex.py",
                "automation_cli.py",
                "automation_status_dashboard.py",
                "cleanup_workflows.py",
                "collect_md_for_ai.py",
                "copyright_manager.py",
                "copyright_status_report.py",
                "decision_path_ui.py",
                "demo_local_agents.py",
                "demo_md_runner.py",
                "enhanced_ai_runner.py",
                "fake_local_llm.py",
                "final_attribution_summary.py",
                "final_workflow_fix.py",
                "fix_github_actions.py",
                "fix_github_workflows.py",
                "fix_symbolic_links.sh",
                "fix_workflows.sh",
                "fix-errors.sh",
                "local_agent_launcher.py",
                "master_launcher.py",
                "mock_environment.py",
                "ollama_probe.py",
                "run.py",
                "run_all_readmes.sh",
                "run_md_ai.py",
                "run_new.py",
                "setup_copyright_attribution.py",
                "setup_local_agents.sh",
                "simple_workflow_fixer.py",
                "simulate_user_input.py",
                "stress_test_automation.py",
                "unified_launcher.py",
                "enhanced_maintenance.sh",
                "demo_agi_agents.sh"
            ],

            # Documentation
            "12-documentation": [
                "AGI_COMMANDS.md",
                "AGI_LOCAL_SETUP_COMPLETE.md",
                "AI_AGI_DEVELOPMENT_STATUS_REPORT.md",
                "AI_MARKDOWN_GUIDE.md",
                "ATTRIBUTION.md",
                "ATTRIBUTION_REPORT.md",
                "CHANGELOG.md",
                "CONTRIBUTORS.md",
                "COPYRIGHT.md",
                "GITHUB_ACTIONS_FIX_REPORT.md",
                "HOW_TO_RUN_MD_AS_AI.md",
                "MAINTENANCE_REPORT.md",
                "README-ENHANCED.md",
                "UNIFIED_LAUNCHER_README-01JYN3X5FDA8J9MMMQMBN67RBN.md",
                "UNIFIED_LAUNCHER_README.md",
                "ai_demo.md",
                "ai_markdown_demo.md",
                "ai_types_demo.md",
                "agi_optimization_test.md",
                "demo_ai_types.md",
                "run_md_as_ai_demo.md",
                "simple_ai_demo.md",
                "all_markdown_plaintext.txt"
            ],

            # Testing
            "13-testing": [
                "test_agi_workflow.py",
                "test_agi_workflows.py",
                "test_ai_runner.py",
                "test_direct_ai.py",
                "test_local_agent.py",
                "test_multi_agent_coordination.py",
                "test_performance.py",
                "TestResults/"
            ],

            # Runtime and executables
            "14-runtime": [
                "launch",
                "launch.bat",
                "agi_memory.db",
                "agi_memory.db-shm",
                "agi_memory.db-wal",
                "local_agent_launcher.log"
            ],

            # Web UI and interfaces
            "15-web-ui": [
                "agi_status_dashboard.py",
                "ai_markdown_processor.py",
                "ai_markdown_runner.py"
            ],

            # Extensions and tools
            "16-extensions": [
                "agi-backend-server/",
                "agi-website/"
            ],

            # Temporary files
            "17-temporary": [
                "Untitled-1",
                "Untitled-1.dbcnb",
                "Untitled-1.ipynb",
                "Untitled-1.py",
                "temp/",
                "stubs/"
            ],

            # Data and resources
            "18-data": [
                "__azurite_db_blob__.json",
                "__azurite_db_blob_extent__.json",
                "__azurite_db_queue__.json",
                "__azurite_db_queue_extent__.json",
                "__azurite_db_table__.json",
                "__blobstorage__/",
                "__pycache__/",
                "Workspaces/",
                "demos/",
                "logs/"
            ],

            # Miscellaneous
            "19-miscellaneous": [
                "AzuriteConfig",
                "CITATION.cff",
                "NOTICE",
                "LICENSE",
                "semantic-kernel-fork-enhancement.ipynb",
                "COMPREHENSIVE_ORGANIZATION_INDEX.json",
                "COMPREHENSIVE_ORGANIZATION_SUMMARY.md"
            ]
        }

        # Files to keep in root
        self.keep_in_root = [
            "README.md",
            ".gitignore",
            ".gitattributes",
            ".gitmodules"
        ]

        # Directories to keep in root (already organized or system dirs)
        self.keep_dirs = [
            "01-core-implementations",
            "02-ai-workspace",
            "03-development-tools",
            "04-infrastructure",
            "05-documentation",
            "06-deployment",
            "07-resources",
            "08-archived-versions",
            "09-agi-development",
            "10-configuration",
            "11-automation-scripts",
            "12-documentation",
            "13-testing",
            "14-runtime",
            "15-web-ui",
            "16-extensions",
            "17-temporary",
            "18-data",
            "19-miscellaneous",
            "docs",
            "scripts",
            "tests",
            "tutorials",
            ".git",
            ".github",
            ".vscode",
            ".ai-monitoring",
            ".agi_backups",
            ".calva",
            ".circleci",
            ".devcontainer",
            ".docker",
            ".dvc",
            ".extended_automode",
            ".gradle",
            ".iis",
            ".mirrord",
            ".mono",
            ".reef",
            ".swm",
            ".venv"
        ]

    def create_directories(self):
        """Create all organization directories"""
        print("Creating organization directories...")
        for dir_name in self.organization_map.keys():
            dir_path = self.repo_root / dir_name
            dir_path.mkdir(exist_ok=True)
            print(f"✓ Created: {dir_name}")

    def move_file_or_dir(self, source, target_dir):
        """Move a file or directory to target directory with symlink"""
        source_path = self.repo_root / source
        target_path = self.repo_root / target_dir

        if not source_path.exists():
            return False

        # Create target directory if it doesn't exist
        target_path.mkdir(parents=True, exist_ok=True)

        # Determine destination
        dest_path = target_path / source_path.name

        try:
            # Move the file/directory
            shutil.move(str(source_path), str(dest_path))

            # Create symlink in original location
            os.symlink(str(dest_path), str(source_path))

            self.moved_files.append(f"{source} → {target_dir}/{source_path.name}")
            self.created_symlinks.append(f"{source} → {dest_path}")

            print(f"✓ Moved: {source} → {target_dir}/")
            return True

        except Exception as e:
            print(f"✗ Error moving {source}: {e}")
            return False

    def organize_files(self):
        """Organize all files according to the organization map"""
        print("\nOrganizing files...")
        total_moved = 0

        for target_dir, files in self.organization_map.items():
            for file_pattern in files:
                if self.move_file_or_dir(file_pattern, target_dir):
                    total_moved += 1

        return total_moved

    def create_summary_report(self, total_moved):
        """Create a summary report of the organization"""
        report = {
            "organization_date": datetime.now().isoformat(),
            "total_files_moved": total_moved,
            "moved_files": self.moved_files,
            "created_symlinks": self.created_symlinks,
            "organization_structure": list(self.organization_map.keys())
        }

        # Save JSON report
        with open(self.repo_root / "ORGANIZATION_REPORT.json", 'w') as f:
            json.dump(report, f, indent=2)

        # Create markdown report
        md_content = f"""# Repository Organization Report

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
- **Total files moved**: {total_moved}
- **Organization directories**: {len(self.organization_map)}
- **Symlinks created**: {len(self.created_symlinks)}

## Organization Structure
"""

        for dir_name in self.organization_map.keys():
            md_content += f"- `{dir_name}/` - {self.get_dir_description(dir_name)}\n"

        md_content += f"""
## Files Moved
"""
        for move in self.moved_files:
            md_content += f"- {move}\n"

        with open(self.repo_root / "ORGANIZATION_REPORT.md", 'w') as f:
            f.write(md_content)

    def get_dir_description(self, dir_name):
        """Get description for directory"""
        descriptions = {
            "10-configuration": "Configuration files and settings",
            "11-automation-scripts": "Automation and utility scripts",
            "12-documentation": "Documentation and guides",
            "13-testing": "Test files and testing infrastructure",
            "14-runtime": "Runtime files and executables",
            "15-web-ui": "Web UI and interface files",
            "16-extensions": "Extensions and external tools",
            "17-temporary": "Temporary files and stubs",
            "18-data": "Data files and resources",
            "19-miscellaneous": "Miscellaneous files"
        }
        return descriptions.get(dir_name, "Organized files")

    def run(self):
        """Run the complete organization process"""
        print("🗂️  Starting comprehensive repository organization...")

        # Create directories
        self.create_directories()

        # Organize files
        total_moved = self.organize_files()

        # Create reports
        self.create_summary_report(total_moved)

        print(f"\n✅ Organization complete!")
        print(f"📁 {total_moved} files/directories organized")
        print(f"🔗 {len(self.created_symlinks)} symlinks created")
        print(f"📋 Reports saved: ORGANIZATION_REPORT.md & ORGANIZATION_REPORT.json")

        return total_moved

if __name__ == "__main__":
    organizer = RepositoryOrganizer()
    organizer.run()
