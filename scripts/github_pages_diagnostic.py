#!/usr/bin/env python3
"""
GitHub Pages Deployment Diagnostic Tool
=====================================

This script diagnoses common issues with GitHub Pages deployment
and provides actionable recommendations.
"""

import os
import sys
import json
import subprocess
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, List, Tuple


class GitHubPagesDiagnostic:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.ai_workspace_path = self.repo_path / "ai-workspace"
        self.workflow_path = self.repo_path / ".github" / "workflows" / "ai-workspace-deploy.yml"
        self.issues = []
        self.recommendations = []

    def log_issue(self, issue: str, severity: str = "WARNING"):
        """Log an issue with severity level"""
        self.issues.append(f"[{severity}] {issue}")
        print(f"❌ {severity}: {issue}")

    def log_success(self, message: str):
        """Log a successful check"""
        print(f"✅ {message}")

    def log_recommendation(self, rec: str):
        """Log a recommendation"""
        self.recommendations.append(rec)
        print(f"💡 RECOMMENDATION: {rec}")

    def check_repository_structure(self) -> bool:
        """Check if the repository has the correct structure"""
        print("\n🔍 Checking repository structure...")

        # Check if ai-workspace exists
        if not self.ai_workspace_path.exists():
            self.log_issue("ai-workspace directory not found", "CRITICAL")
            return False
        self.log_success("ai-workspace directory exists")

        # Check if workflow exists
        if not self.workflow_path.exists():
            self.log_issue("GitHub Actions workflow not found", "CRITICAL")
            return False
        self.log_success("GitHub Actions workflow exists")

        # Check if dist can be built
        build_script = self.ai_workspace_path / "scripts" / "build_static.sh"
        if not build_script.exists():
            self.log_issue("Build script not found", "CRITICAL")
            return False
        self.log_success("Build script exists")

        return True

    def check_build_output(self) -> bool:
        """Check if the build produces valid output"""
        print("\n🔨 Testing build process...")

        try:
            # Run the build script
            os.chdir(self.ai_workspace_path)
            result = subprocess.run(
                ["./scripts/build_static.sh"],
                capture_output=True,
                text=True,
                check=True
            )
            self.log_success("Build script executed successfully")

            # Check if dist directory exists
            dist_path = self.ai_workspace_path / "dist"
            if not dist_path.exists():
                self.log_issue("Build did not create dist directory", "CRITICAL")
                return False
            self.log_success("dist directory created")

            # Check for index.html
            index_path = dist_path / "index.html"
            if not index_path.exists():
                self.log_issue("No index.html in dist directory", "CRITICAL")
                return False
            self.log_success("index.html exists in dist")

            # Check for .nojekyll
            nojekyll_path = dist_path / ".nojekyll"
            if not nojekyll_path.exists():
                self.log_issue("No .nojekyll file - Jekyll may interfere", "WARNING")
            else:
                self.log_success(".nojekyll file present")

            # Check index.html size
            index_size = index_path.stat().st_size
            if index_size < 100:
                self.log_issue(f"index.html is very small ({index_size} bytes)", "WARNING")
            else:
                self.log_success(f"index.html has reasonable size ({index_size} bytes)")

            return True

        except subprocess.CalledProcessError as e:
            self.log_issue(f"Build script failed: {e.stderr}", "CRITICAL")
            return False
        except Exception as e:
            self.log_issue(f"Build test failed: {str(e)}", "CRITICAL")
            return False

    def check_workflow_syntax(self) -> bool:
        """Check if the workflow YAML is valid"""
        print("\n📋 Checking workflow configuration...")

        try:
            import yaml
            with open(self.workflow_path, 'r') as f:
                workflow_content = yaml.safe_load(f)

            # Check key sections
            required_sections = ['name', 'on', 'permissions', 'jobs']
            for section in required_sections:
                if section not in workflow_content:
                    self.log_issue(f"Missing required section: {section}", "CRITICAL")
                    return False

            self.log_success("Workflow YAML syntax is valid")

            # Check permissions
            permissions = workflow_content.get('permissions', {})
            if permissions.get('pages') != 'write':
                self.log_issue("Missing 'pages: write' permission", "CRITICAL")
                return False
            self.log_success("GitHub Pages permissions configured")

            # Check for deploy-pages job
            jobs = workflow_content.get('jobs', {})
            if 'deploy-pages' not in jobs:
                self.log_issue("Missing deploy-pages job", "CRITICAL")
                return False
            self.log_success("deploy-pages job configured")

            return True

        except ImportError:
            print("⚠️ PyYAML not available, skipping workflow syntax check")
            return True
        except Exception as e:
            self.log_issue(f"Workflow syntax error: {str(e)}", "CRITICAL")
            return False

    def check_git_status(self) -> bool:
        """Check git repository status"""
        print("\n📦 Checking git repository status...")

        try:
            os.chdir(self.repo_path)

            # Check if we're on main branch
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True,
                check=True
            )
            current_branch = result.stdout.strip()
            if current_branch != "main":
                self.log_issue(f"Not on main branch (current: {current_branch})", "WARNING")
            else:
                self.log_success("On main branch")

            # Check for uncommitted changes
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                check=True
            )
            if result.stdout.strip():
                self.log_issue("Uncommitted changes detected", "WARNING")
                self.log_recommendation("Commit and push all changes before deployment")
            else:
                self.log_success("No uncommitted changes")

            # Check if we're ahead of origin
            result = subprocess.run(
                ["git", "status", "-b", "--porcelain"],
                capture_output=True,
                text=True,
                check=True
            )
            if "ahead" in result.stdout:
                self.log_issue("Local branch is ahead of origin", "WARNING")
                self.log_recommendation("Push changes to trigger deployment")
            else:
                self.log_success("Repository is in sync with origin")

            return True

        except subprocess.CalledProcessError as e:
            self.log_issue(f"Git command failed: {e.stderr}", "ERROR")
            return False

    def check_github_pages_settings(self):
        """Provide instructions for checking GitHub Pages settings"""
        print("\n⚙️ GitHub Pages Settings Check (Manual Verification Required)")
        print("\nTo verify GitHub Pages settings, please check the following:")
        print("1. Go to your repository on GitHub")
        print("2. Navigate to Settings > Pages")
        print("3. Verify that:")
        print("   - Source is set to 'GitHub Actions'")
        print("   - NOT set to 'Deploy from a branch'")
        print("4. Check the Actions tab for recent workflow runs")
        print("5. Look for successful 'AI Workspace Deployment' runs")

        self.log_recommendation("Verify GitHub Pages source is set to 'GitHub Actions'")
        self.log_recommendation("Check repository Actions tab for deployment status")

    def check_common_issues(self):
        """Check for common GitHub Pages deployment issues"""
        print("\n🔧 Checking for common issues...")

        # Check if there are any large files that might cause issues
        try:
            os.chdir(self.ai_workspace_path)
            result = subprocess.run(
                ["find", ".", "-size", "+10M", "-type", "f"],
                capture_output=True,
                text=True
            )
            if result.stdout.strip():
                large_files = result.stdout.strip().split('\n')
                for file in large_files:
                    self.log_issue(f"Large file detected: {file}", "WARNING")
                self.log_recommendation("Consider using Git LFS for large files")
            else:
                self.log_success("No excessively large files detected")

        except Exception as e:
            print(f"⚠️ Could not check file sizes: {e}")

        # Check for files with problematic names
        problematic_chars = ['<', '>', ':', '"', '|', '?', '*']
        try:
            result = subprocess.run(
                ["find", ".", "-name", "*[<>:\"|?*]*"],
                capture_output=True,
                text=True
            )
            if result.stdout.strip():
                self.log_issue("Files with problematic characters detected", "WARNING")
                self.log_recommendation("Rename files to use web-safe characters")
            else:
                self.log_success("No problematic filenames detected")
        except Exception:
            pass

    def check_cname_file(self) -> bool:
        """Check CNAME file configuration for custom domains"""
        print("\n🌐 Checking CNAME file configuration...")
        
        # Check for CNAME file in repository root
        cname_root = self.repo_path / "CNAME"
        cname_workspace = self.ai_workspace_path / "CNAME"
        
        cname_found = False
        cname_path = None
        
        if cname_root.exists():
            cname_found = True
            cname_path = cname_root
            self.log_success("CNAME file found in repository root")
        elif cname_workspace.exists():
            cname_found = True
            cname_path = cname_workspace
            self.log_success("CNAME file found in ai-workspace directory")
        else:
            self.log_success("No CNAME file found - using default GitHub Pages domain")
            return True
            
        if cname_found and cname_path:
            try:
                # Read and validate CNAME file
                with open(cname_path, 'r') as f:
                    content = f.read().strip()
                    
                # Check if filename is uppercase
                if cname_path.name != "CNAME":
                    self.log_issue(f"CNAME filename should be uppercase, found: {cname_path.name}", "CRITICAL")
                    return False
                    
                # Check if content is valid
                if not content:
                    self.log_issue("CNAME file is empty", "CRITICAL")
                    return False
                    
                lines = content.split('\n')
                if len(lines) > 1:
                    self.log_issue("CNAME file should contain only one domain", "CRITICAL")
                    return False
                    
                domain = lines[0].strip()
                
                # Basic domain validation
                if not domain or ' ' in domain:
                    self.log_issue(f"Invalid domain in CNAME file: '{domain}'", "CRITICAL")
                    return False
                    
                # Check for protocol prefix (should not be there)
                if domain.startswith(('http://', 'https://')):
                    self.log_issue("CNAME file should contain domain only, not full URL", "CRITICAL")
                    return False
                    
                # Check for path (should not be there)
                if '/' in domain:
                    self.log_issue("CNAME file should contain domain only, not path", "CRITICAL")
                    return False
                    
                self.log_success(f"CNAME file properly configured for domain: {domain}")
                
                # Add recommendation about DNS configuration
                self.log_recommendation(f"Ensure DNS for {domain} points to your GitHub Pages site")
                
                return True
                
            except Exception as e:
                self.log_issue(f"Error reading CNAME file: {str(e)}", "CRITICAL")
                return False
                
        return True

    def generate_test_deployment(self):
        """Generate a minimal test deployment"""
        print("\n🧪 Generating test deployment...")

        test_dir = self.ai_workspace_path / "test-deployment"
        test_dir.mkdir(exist_ok=True)

        # Create minimal index.html
        test_index = test_dir / "index.html"
        test_index.write_text("""<!DOCTYPE html>
<html>
<head>
    <title>AI Workspace Test</title>
</head>
<body>
    <h1>AI Workspace Deployment Test</h1>
    <p>If you can see this page, the deployment is working!</p>
    <p>Timestamp: {}</p>
</body>
</html>""".format(subprocess.run(["date"], capture_output=True, text=True).stdout.strip()))

        # Create .nojekyll
        (test_dir / ".nojekyll").touch()

        self.log_success(f"Test deployment created in {test_dir}")
        self.log_recommendation("You can manually upload this test-deployment folder to verify GitHub Pages works")

    def run_full_diagnostic(self):
        """Run the complete diagnostic suite"""
        print("🚀 GitHub Pages Deployment Diagnostic")
        print("=" * 50)

        # Run all checks
        structure_ok = self.check_repository_structure()
        if not structure_ok:
            print("\n❌ Critical repository structure issues found. Fix these first.")
            return False

        build_ok = self.check_build_output()
        workflow_ok = self.check_workflow_syntax()
        git_ok = self.check_git_status()

        self.check_github_pages_settings()
        self.check_common_issues()
        self.check_cname_file()
        self.generate_test_deployment()

        # Summary
        print("\n" + "=" * 50)
        print("📊 DIAGNOSTIC SUMMARY")
        print("=" * 50)

        if self.issues:
            print(f"\n❌ Issues Found ({len(self.issues)}):")
            for issue in self.issues:
                print(f"  {issue}")
        else:
            print("\n✅ No issues detected!")

        if self.recommendations:
            print(f"\n💡 Recommendations ({len(self.recommendations)}):")
            for rec in self.recommendations:
                print(f"  • {rec}")

        # Final assessment
        critical_issues = [i for i in self.issues if "CRITICAL" in i]
        if critical_issues:
            print(f"\n🚨 CRITICAL: {len(critical_issues)} critical issues must be fixed")
            return False
        elif self.issues:
            print(f"\n⚠️ WARNING: {len(self.issues)} warnings detected")
            print("Deployment may work but could have issues")
            return True
        else:
            print("\n🎉 SUCCESS: All checks passed!")
            print("Your deployment should work correctly")
            return True


def main():
    if len(sys.argv) > 1:
        repo_path = sys.argv[1]
    else:
        repo_path = "/workspaces/semantic-kernel"

    diagnostic = GitHubPagesDiagnostic(repo_path)
    success = diagnostic.run_full_diagnostic()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
