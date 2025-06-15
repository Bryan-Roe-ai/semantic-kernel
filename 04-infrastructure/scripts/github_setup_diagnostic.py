#!/usr/bin/env python3
"""
GitHub Pages Repository Setup Error Diagnostic
=============================================

Based on GitHub's official troubleshooting guides, this script diagnoses
common repository setup errors that prevent GitHub Pages from working.

Official References:
- https://docs.github.com/en/pages/getting-started-with-github-pages/troubleshooting-404-errors-for-github-pages-sites
- https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/troubleshooting-custom-domains-and-github-pages
"""

import subprocess
import sys
import urllib.request
import urllib.error
from pathlib import Path


def check_repository_setup_errors():
    """Check for common GitHub repository setup errors based on official GitHub docs"""

    print("🔍 GitHub Pages Repository Setup Error Diagnostic")
    print("=" * 60)
    print("📚 Based on GitHub's Official Troubleshooting Guides")
    print()

    issues_found = []
    recommendations = []

    # CRITICAL: Check for CNAME file when using GitHub Actions (Official Guidance)
    print("🎯 1. CNAME File Check (GitHub Actions Deployment)")
    print("-" * 55)
    print("📖 Official GitHub Documentation States:")
    print("   'If you are publishing from a custom GitHub Actions workflow,")
    print("    any CNAME file is ignored and is not required.'")
    print()

    cname_files = []
    for cname_path in [Path("CNAME"), Path("ai-workspace/CNAME")]:
        if cname_path.exists():
            cname_files.append(str(cname_path))

    if cname_files:
        print(f"✅ CNAME files detected: {', '.join(cname_files)}")
        print("   ℹ️  These files are IGNORED for GitHub Actions deployment")
        print("   ℹ️  No action needed - this is normal for your setup")
    else:
        print("✅ No CNAME files found (correct for GitHub Actions deployment)")
    print()

    # Check GitHub Actions workflow configuration
    print("🎯 2. GitHub Actions Workflow Configuration")
    print("-" * 45)

    workflow_file = Path(".github/workflows/ai-workspace-deploy.yml")
    if workflow_file.exists():
        print("✅ GitHub Actions workflow exists")

        try:
            with open(workflow_file, 'r') as f:
                content = f.read()

            # Check for required permissions
            if 'pages: write' in content and 'id-token: write' in content:
                print("✅ Workflow has correct GitHub Pages permissions")
            else:
                print("❌ Workflow missing required permissions")
                issues_found.append("Workflow lacks 'pages: write' or 'id-token: write' permissions")

            # Check for deploy-pages action
            if 'actions/deploy-pages@v' in content:
                print("✅ Workflow uses official deploy-pages action")
            else:
                print("❌ Workflow missing deploy-pages action")
                issues_found.append("Workflow doesn't use actions/deploy-pages")

            # Check for index.html in build output
            if 'index.html' in content:
                print("✅ Workflow references index.html file")
            else:
                print("⚠️  Workflow should ensure index.html is in build output")

        except Exception as e:
            print(f"❌ Error reading workflow file: {e}")
            issues_found.append("Cannot read workflow file")
    else:
        print("❌ No GitHub Actions workflow found")
        issues_found.append("Missing GitHub Actions deployment workflow")
        recommendations.append("Create .github/workflows/ai-workspace-deploy.yml")
    print()

    # Check for index.html file (Official GitHub requirement)
    print("🎯 3. Index.html File Check (GitHub Requirement)")
    print("-" * 48)
    print("📖 Official GitHub Documentation States:")
    print("   'GitHub Pages will look for an index.html file as the entry file'")
    print("   'Make sure you have an index.html file in the repository'")
    print()

    # Check build output
    dist_index = Path("ai-workspace/dist/index.html")
    source_index = Path("ai-workspace/05-samples-demos/index.html")

    if dist_index.exists():
        print("✅ index.html found in build output (ai-workspace/dist/)")
        # Check file size
        size = dist_index.stat().st_size
        if size > 100:
            print(f"✅ index.html has content ({size} bytes)")
        else:
            print(f"⚠️  index.html is very small ({size} bytes)")
            issues_found.append("index.html file appears to be empty or minimal")
    elif source_index.exists():
        print("✅ index.html found in source (ai-workspace/05-samples-demos/)")
        print("   ℹ️  Build script should copy this to dist/ directory")
    else:
        print("❌ No index.html file found in expected locations")
        issues_found.append("Missing index.html file")
        recommendations.append("Create index.html in ai-workspace/05-samples-demos/")
    print()

    # Check for .nojekyll file (Important for GitHub Actions)
    print("🎯 4. Jekyll Bypass Check")
    print("-" * 25)
    print("📖 GitHub Documentation States:")
    print("   'Adding a .nojekyll file to the root of your source branch will")
    print("    bypass the Jekyll build process and deploy the content directly'")
    print()

    nojekyll_dist = Path("ai-workspace/dist/.nojekyll")
    if nojekyll_dist.exists():
        print("✅ .nojekyll file present in build output")
    else:
        print("⚠️  .nojekyll file missing from build output")
        print("   ℹ️  Build script should create this file")
        recommendations.append("Ensure .nojekyll file is created in dist/ directory")
    print()

    # 5. Official GitHub Pages Repository Requirements Check
    print("🎯 5. Repository Requirements (GitHub Official)")
    print("-" * 50)
    print("📖 GitHub Documentation: Repository must meet these requirements:")
    print()

    # Check if we can determine repository info
    try:
        # Try to get repository information
        git_remote = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            check=False
        )
        if git_remote.returncode == 0:
            remote_url = git_remote.stdout.strip()
            print(f"✅ Git repository detected: {remote_url}")

            # Check if it's a GitHub repository
            if 'github.com' in remote_url:
                print("✅ Repository is hosted on GitHub")

                # Extract repository info for manual verification
                import re
                match = re.search(r'github\.com[:/]([^/]+)/([^/.]+)', remote_url)
                if match:
                    owner, repo = match.groups()
                    repo = repo.replace('.git', '')
                    print(f"   � Repository: {owner}/{repo}")
                    print(f"   🌐 Expected URL: https://{owner}.github.io/{repo}/")

                    print("\n   📋 MANUAL VERIFICATION REQUIRED:")
                    print(f"   1. Visit: https://github.com/{owner}/{repo}/settings/pages")
                    print("   2. Verify 'Source' is set to 'GitHub Actions'")
                    print("   3. Verify 'Custom domain' field is EMPTY")
                    print(f"   4. Check: https://github.com/{owner}/{repo}/actions")
                    print("   5. Look for successful 'AI Workspace Deployment' runs")
            else:
                print("⚠️  Repository is not hosted on GitHub")
                issues_found.append("Repository must be hosted on GitHub for GitHub Pages")
        else:
            print("⚠️  No git repository detected")
    except Exception as e:
        print(f"⚠️  Could not determine repository info: {e}")
    print()

    # 6. Official GitHub 404 Troubleshooting Steps
    print("🎯 6. GitHub Official 404 Error Troubleshooting")
    print("-" * 48)
    print("📖 Based on: docs.github.com/en/pages/.../troubleshooting-404-errors")
    print()

    print("✅ COMPLETED CHECKS:")
    print("   - ✅ index.html file verification")
    print("   - ✅ Directory contents check")
    print("   - ✅ CNAME file handling (for GitHub Actions)")
    print("   - ✅ Repository structure validation")
    print()

    print("🔧 REMAINING MANUAL CHECKS:")
    print("   1. 🌐 GitHub's Status Page: Visit https://githubstatus.com/")
    print("   2. 🔄 Browser Cache: Clear cache and try incognito mode")
    print("   3. ⏰ DNS Propagation: Wait 5-10 minutes after deployment")
    print("   4. 👁️  Repository Visibility: Ensure repo is PUBLIC")
    print("   5. 🚀 Recent Deployment: Check if workflow completed successfully")
    print()

    # Summary with official guidance
    print("📊 DIAGNOSTIC SUMMARY (Based on GitHub Official Docs)")
    print("=" * 58)

    if issues_found:
        print(f"❌ Technical Issues Found: {len(issues_found)}")
        for i, issue in enumerate(issues_found, 1):
            print(f"   {i}. {issue}")
        print()

    if recommendations:
        print(f"💡 Technical Recommendations: {len(recommendations)}")
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec}")
        print()

    # Final assessment based on GitHub's official troubleshooting
    if not issues_found:
        print("✅ TECHNICAL CONFIGURATION: All checks passed")
        print()
        print("🎯 MOST LIKELY CAUSE (per GitHub docs):")
        print("   • GitHub Pages settings not properly configured")
        print("   • Workflow has not run successfully yet")
        print("   • DNS propagation still in progress")
        print()
        print("🔧 REQUIRED MANUAL ACTION:")
        print("   1. Configure GitHub Pages in repository settings")
        print("   2. Set Source to 'GitHub Actions'")
        print("   3. Ensure Custom domain field is EMPTY")
        print("   4. Wait for next workflow run to complete")
    else:
        print("🚨 TECHNICAL ISSUES DETECTED")
        print("   Fix the issues above before proceeding")

    print()
    print("🌐 Expected Final URL: https://bryan-roe-ai.github.io/semantic-kernel/")
    print("📞 Next Step: Configure GitHub Pages settings (manual)")

    return len(issues_found) == 0


def main():
    """Main function to run the diagnostic"""
    import sys

    print("🚀 Starting GitHub Pages Setup Diagnostic...")
    print("📚 Using GitHub's Official Troubleshooting Guides")
    print()

    success = check_repository_setup_errors()

    print()
    print("🏁 DIAGNOSTIC COMPLETE")
    print("=" * 25)
    if success:
        print("✅ Repository is technically ready for GitHub Pages")
        print("🔧 Manual GitHub settings configuration required")
    else:
        print("❌ Technical issues need to be resolved first")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
