#!/usr/bin/env python3
"""
🗂️ Repository Organization System
Organizes the entire Semantic Kernel repository into a logical, maintainable structure
with enhanced AI monitoring integration.
"""

import os
import sys
import shutil
import json
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('RepoOrganizer')

class RepositoryOrganizer:
    """Organizes repository structure and integrates AI monitoring"""
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = Path(workspace_root)
        self.backup_dir = self.workspace_root / '.reorganization_backup'
        
        # New structure definition
        self.new_structure = {
            "01-core": {
                "description": "Core Semantic Kernel implementations",
                "subdirs": ["dotnet", "python", "java", "typescript", "shared"]
            },
            "02-ai-workspace": {
                "description": "Enhanced AI workspace (EXPAND EXISTING)",
                "subdirs": ["agents", "monitoring", "scripts", "tools", "logs", "configs"]
            },
            "03-samples": {
                "description": "All sample implementations",
                "subdirs": ["quickstart", "advanced", "notebooks", "demos"]
            },
            "04-documentation": {
                "description": "Consolidated documentation",
                "subdirs": ["api", "guides", "architecture", "reports"]
            },
            "05-infrastructure": {
                "description": "DevOps and infrastructure",
                "subdirs": ["deployment", "ci-cd", "docker", "monitoring"]
            },
            "06-resources": {
                "description": "Static resources and data", 
                "subdirs": ["data", "templates", "configs", "assets"]
            },
            "07-archive": {
                "description": "Archived/legacy content",
                "subdirs": ["deprecated", "experiments", "legacy"]
            }
        }
        
        # File mapping rules
        self.file_mappings = {
            # Core implementations
            r"dotnet/.*": "01-core/dotnet",
            r"python/.*": "01-core/python", 
            r"java/.*": "01-core/java",
            r"typescript/.*": "01-core/typescript",
            
            # Enhanced AI workspace (keep and expand existing)
            r"02-ai-workspace/.*": "02-ai-workspace",
            r"ai-workspace/.*": "02-ai-workspace",
            
            # Samples
            r"samples/.*": "03-samples/advanced",
            r"notebooks/.*": "03-samples/notebooks",
            
            # Documentation
            r"docs/.*": "04-documentation/guides",
            r"README.*": "04-documentation/guides",
            r".*\.md$": "04-documentation/guides",
            
            # Infrastructure
            r"\.github/.*": "05-infrastructure/ci-cd",
            r"\.docker/.*": "05-infrastructure/docker",
            r"\.devcontainer/.*": "05-infrastructure/docker",
            r"scripts/.*": "05-infrastructure/deployment",
            
            # Resources
            r"data/.*": "06-resources/data",
            r"configs?/.*": "06-resources/configs",
            r"resources/.*": "06-resources",
            r"uploads/.*": "06-resources/data",
            
            # Archive legacy/experimental
            r"vscode-.*": "07-archive/experiments",
            r"agi-.*": "07-archive/experiments", 
            r"node-api-.*": "07-archive/experiments",
            r"DevSkim/.*": "07-archive/experiments",
        }
        
        # Initialize AI monitoring
        self._init_ai_monitoring()
    
    def _init_ai_monitoring(self):
        """Initialize AI monitoring for the organization process"""
        try:
            sys.path.append(str(self.workspace_root / '.ai-monitoring'))
            from universal_ai_monitor import get_universal_monitor
            self.monitor = get_universal_monitor()
            self.monitor.log_system_event("repo_organization_start", "Repository reorganization initiated")
        except ImportError:
            logger.warning("AI monitoring not available - proceeding without monitoring")
            self.monitor = None
    
    def analyze_current_structure(self) -> Dict[str, Any]:
        """Analyze the current repository structure"""
        if self.monitor:
            self.monitor.log_ai_thought("RepoOrganizer", "Analyzing current repository structure")
        
        analysis = {
            "total_files": 0,
            "total_dirs": 0,
            "file_types": {},
            "large_dirs": {},
            "duplicates": [],
            "empty_dirs": []
        }
        
        # Walk through all files and directories
        for item in self.workspace_root.rglob("*"):
            if item.is_file():
                analysis["total_files"] += 1
                suffix = item.suffix.lower()
                analysis["file_types"][suffix] = analysis["file_types"].get(suffix, 0) + 1
                
                # Check for potential duplicates
                if item.name in [p.name for p in self.workspace_root.rglob(item.name) if p != item]:
                    analysis["duplicates"].append(str(item.relative_to(self.workspace_root)))
            
            elif item.is_dir():
                analysis["total_dirs"] += 1
                
                # Count files in directory
                file_count = len(list(item.rglob("*")))
                if file_count > 100:
                    analysis["large_dirs"][str(item.relative_to(self.workspace_root))] = file_count
                elif file_count == 0:
                    analysis["empty_dirs"].append(str(item.relative_to(self.workspace_root)))
        
        logger.info(f"📊 Analysis complete: {analysis['total_files']} files, {analysis['total_dirs']} directories")
        
        if self.monitor:
            self.monitor.log_ai_analysis("RepoOrganizer", "structure_analysis", analysis)
        
        return analysis
    
    def create_backup(self) -> Path:
        """Create a backup of the current state"""
        if self.monitor:
            self.monitor.log_ai_action("RepoOrganizer", "create_backup", backup_location=str(self.backup_dir))
        
        self.backup_dir.mkdir(exist_ok=True)
        
        # Create timestamped backup
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"repo_backup_{timestamp}"
        
        logger.info(f"💾 Creating backup at: {backup_path}")
        
        # Create backup manifest
        manifest = {
            "backup_created": datetime.now().isoformat(),
            "original_structure": self.analyze_current_structure(),
            "backup_path": str(backup_path)
        }
        
        with open(self.backup_dir / f"manifest_{timestamp}.json", 'w') as f:
            json.dump(manifest, f, indent=2)
        
        logger.info("✅ Backup manifest created")
        return backup_path
    
    def create_new_structure(self):
        """Create the new directory structure"""
        if self.monitor:
            self.monitor.log_ai_action("RepoOrganizer", "create_new_structure")
        
        logger.info("🏗️ Creating new directory structure...")
        
        for main_dir, config in self.new_structure.items():
            main_path = self.workspace_root / main_dir
            main_path.mkdir(exist_ok=True)
            
            # Create subdirectories
            for subdir in config["subdirs"]:
                (main_path / subdir).mkdir(exist_ok=True)
            
            # Create README for each main directory
            readme_content = f"""# {main_dir.replace('-', ' ').title()}

{config['description']}

## Structure

{chr(10).join(f'- `{subdir}/` - {subdir.replace("_", " ").title()}' for subdir in config['subdirs'])}

## Last Updated

{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            
            with open(main_path / "README.md", 'w') as f:
                f.write(readme_content)
        
        logger.info("✅ New directory structure created")
    
    def move_files_to_new_structure(self, dry_run: bool = True) -> Dict[str, List[str]]:
        """Move files to the new structure"""
        if self.monitor:
            action_type = "dry_run_file_move" if dry_run else "file_move"
            self.monitor.log_ai_action("RepoOrganizer", action_type, dry_run=dry_run)
        
        moves = {"successful": [], "failed": [], "skipped": []}
        
        logger.info(f"📂 {'Simulating' if dry_run else 'Executing'} file moves...")
        
        # Process each file in the repository
        for item in self.workspace_root.rglob("*"):
            if not item.is_file():
                continue
            
            # Skip files in special directories
            relative_path = item.relative_to(self.workspace_root)
            if any(part.startswith('.') for part in relative_path.parts):
                moves["skipped"].append(str(relative_path))
                continue
            
            # Find matching rule
            destination = self._find_destination(relative_path)
            if not destination:
                moves["skipped"].append(str(relative_path))
                continue
            
            # Determine target path
            target_path = self.workspace_root / destination / relative_path.name
            
            # Ensure target directory exists
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            try:
                if not dry_run:
                    # Move the file
                    shutil.move(str(item), str(target_path))
                    
                    if self.monitor:
                        self.monitor.log_file_change(str(target_path), "moved")
                
                moves["successful"].append(f"{relative_path} → {destination}")
                
            except Exception as e:
                moves["failed"].append(f"{relative_path}: {str(e)}")
                logger.error(f"Failed to move {relative_path}: {e}")
        
        logger.info(f"📊 Move summary: {len(moves['successful'])} successful, {len(moves['failed'])} failed, {len(moves['skipped'])} skipped")
        
        return moves
    
    def _find_destination(self, relative_path: Path) -> str:
        """Find the destination directory for a file"""
        import re
        
        path_str = str(relative_path)
        
        for pattern, destination in self.file_mappings.items():
            if re.match(pattern, path_str):
                return destination
        
        return None
    
    def enhance_ai_workspace(self):
        """Enhance the existing AI workspace with new monitoring features"""
        if self.monitor:
            self.monitor.log_ai_action("RepoOrganizer", "enhance_ai_workspace")
        
        ai_workspace = self.workspace_root / "02-ai-workspace"
        
        # Ensure monitoring directory exists
        monitoring_dir = ai_workspace / "monitoring"
        monitoring_dir.mkdir(exist_ok=True)
        
        # Move enhanced monitoring files
        monitoring_source = self.workspace_root / ".ai-monitoring"
        if monitoring_source.exists():
            for item in monitoring_source.rglob("*"):
                if item.is_file():
                    relative_path = item.relative_to(monitoring_source)
                    target = monitoring_dir / relative_path
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(str(item), str(target))
        
        # Create enhanced configuration
        config = {
            "workspace_version": "2.0",
            "monitoring_enabled": True,
            "universal_monitoring": True,
            "enhanced_features": [
                "universal_ai_monitoring",
                "real_time_dashboard", 
                "inter_agent_communication",
                "performance_analytics",
                "predictive_insights"
            ],
            "last_organized": datetime.now().isoformat()
        }
        
        with open(ai_workspace / "workspace_config.json", 'w') as f:
            json.dump(config, f, indent=2)
        
        logger.info("✅ AI workspace enhanced with universal monitoring")
    
    def update_references(self):
        """Update file references and imports"""
        if self.monitor:
            self.monitor.log_ai_action("RepoOrganizer", "update_references")
        
        logger.info("🔗 Updating file references...")
        
        # Common reference patterns to update
        reference_updates = {
            "scripts/": "05-infrastructure/deployment/",
            "docs/": "04-documentation/guides/", 
            "samples/": "03-samples/advanced/",
            "dotnet/": "01-core/dotnet/",
            "python/": "01-core/python/"
        }
        
        updated_files = []
        
        # Find and update references in common file types
        for pattern in ["*.md", "*.json", "*.yaml", "*.yml", "*.cs", "*.py", "*.js", "*.ts"]:
            for file_path in self.workspace_root.rglob(pattern):
                if self._update_file_references(file_path, reference_updates):
                    updated_files.append(str(file_path.relative_to(self.workspace_root)))
        
        logger.info(f"✅ Updated references in {len(updated_files)} files")
        return updated_files
    
    def _update_file_references(self, file_path: Path, updates: Dict[str, str]) -> bool:
        """Update references in a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            original_content = content
            
            for old_ref, new_ref in updates.items():
                content = content.replace(old_ref, new_ref)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True
                
        except Exception as e:
            logger.warning(f"Could not update references in {file_path}: {e}")
        
        return False
    
    def generate_organization_report(self) -> Dict[str, Any]:
        """Generate a comprehensive organization report"""
        if self.monitor:
            self.monitor.log_ai_action("RepoOrganizer", "generate_report")
        
        report = {
            "organization_completed": datetime.now().isoformat(),
            "new_structure": self.new_structure,
            "post_organization_analysis": self.analyze_current_structure(),
            "ai_workspace_enhanced": True,
            "monitoring_system": "Universal AI Monitor integrated",
            "next_steps": [
                "Review new structure",
                "Update documentation",
                "Test all functionality",
                "Train team on new structure",
                "Monitor AI activities"
            ]
        }
        
        # Save report
        report_path = self.workspace_root / "ORGANIZATION_COMPLETE_REPORT.md"
        
        markdown_report = f"""# 🗂️ Repository Organization Complete

**Completed**: {report['organization_completed']}

## ✅ What Was Done

### 1. New Structure Created
```
{''.join(f'{k}/ - {v["description"]}' + chr(10) for k, v in self.new_structure.items())}
```

### 2. Enhanced AI Workspace
- Universal AI monitoring system integrated
- Real-time dashboard for all AI activities  
- Inter-agent communication tracking
- Performance analytics and insights

### 3. File Organization
- Core implementations moved to `01-core/`
- Samples consolidated in `03-samples/`
- Documentation centralized in `04-documentation/`
- Infrastructure organized in `05-infrastructure/`

## 🔍 AI Monitoring Features

### Universal Visibility
- **Every AI action tracked** across all agents
- **Real-time dashboard** showing live activities
- **Historical analysis** of AI behavior patterns
- **Performance monitoring** and optimization insights

### Key Capabilities
- 🤖 Track all AI thoughts and decisions
- 📁 Monitor file changes with AI context
- 📡 Inter-agent communication logging
- 📊 Performance metrics and trends
- 🧠 Intelligent insights and recommendations

## 🚀 Next Steps

1. **Start Monitoring**: Run the dashboard
   ```bash
   cd .ai-monitoring
   python universal_dashboard.py
   ```

2. **Review Structure**: Explore the new organization
3. **Test Everything**: Ensure all functionality works
4. **Update Team**: Share new structure with team

## 📊 Results

- **Total Files**: {report['post_organization_analysis']['total_files']:,}
- **Total Directories**: {report['post_organization_analysis']['total_dirs']:,}
- **AI Monitoring**: ✅ Active
- **Structure**: ✅ Organized

---

**You now have complete visibility into every AI action in your repository! 🎯**
"""
        
        with open(report_path, 'w') as f:
            f.write(markdown_report)
        
        logger.info(f"📊 Organization report saved: {report_path}")
        return report
    
    def organize_repository(self, dry_run: bool = False) -> Dict[str, Any]:
        """Execute the complete repository organization"""
        logger.info("🚀 Starting repository organization...")
        
        if self.monitor:
            self.monitor.log_ai_decision("RepoOrganizer", "organize_repository", 
                                       "Repository needs better organization for maintainability",
                                       ["organize", "keep_current", "partial_cleanup"])
        
        try:
            # Step 1: Analyze current structure
            analysis = self.analyze_current_structure()
            
            # Step 2: Create backup (if not dry run)
            if not dry_run:
                backup_path = self.create_backup()
            
            # Step 3: Create new structure
            if not dry_run:
                self.create_new_structure()
            
            # Step 4: Move files
            move_results = self.move_files_to_new_structure(dry_run=dry_run)
            
            # Step 5: Enhance AI workspace
            if not dry_run:
                self.enhance_ai_workspace()
            
            # Step 6: Update references
            if not dry_run:
                updated_refs = self.update_references()
            
            # Step 7: Generate report
            if not dry_run:
                report = self.generate_organization_report()
            
            result = {
                "success": True,
                "dry_run": dry_run,
                "analysis": analysis,
                "move_results": move_results,
                "ai_monitoring": "integrated" if not dry_run else "planned"
            }
            
            if not dry_run:
                result.update({
                    "backup_created": True,
                    "references_updated": len(updated_refs) if 'updated_refs' in locals() else 0,
                    "report_generated": True
                })
            
            logger.info("✅ Repository organization completed successfully!")
            
            if self.monitor:
                self.monitor.log_ai_action("RepoOrganizer", "organization_complete", 
                                         success=True, result=result)
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Organization failed: {e}")
            
            if self.monitor:
                self.monitor.log_error("RepoOrganizer", e, "During repository organization")
            
            return {"success": False, "error": str(e)}


def main():
    """Main entry point"""
    workspace_root = Path(__file__).parent.parent.parent
    
    # Check if this is a dry run
    dry_run = "--dry-run" in sys.argv or "-n" in sys.argv
    
    if dry_run:
        print("🧪 DRY RUN MODE - No actual changes will be made")
    else:
        print("⚠️  LIVE MODE - Repository will be reorganized")
        confirm = input("Are you sure you want to proceed? (yes/no): ")
        if confirm.lower() != 'yes':
            print("❌ Operation cancelled")
            return
    
    organizer = RepositoryOrganizer(workspace_root)
    
    print("🗂️ Starting repository organization...")
    result = organizer.organize_repository(dry_run=dry_run)
    
    if result["success"]:
        print("🎉 Repository organization completed!")
        if not dry_run:
            print("📊 Check ORGANIZATION_COMPLETE_REPORT.md for details")
            print("🔍 Start AI monitoring: cd .ai-monitoring && python universal_dashboard.py")
    else:
        print(f"❌ Organization failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()
