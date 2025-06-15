#!/usr/bin/env python3
"""
GitHub Pages Repository Setup Error Diagnostic
=============================================

Based on GitHub's official troubleshooting guide, this script diagnoses
common repository setup errors that prevent GitHub Pages from working.

Reference: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/troubleshooting-custom-domains-and-github-pages#github-repository-setup-errors
"""

import subprocess
import sys
from pathlib import Path


def check_repository_setup_errors():
    """Check for common GitHub repository setup errors"""

    print("🔍 GitHub Pages Repository Setup Error Diagnostic")
    print("=" * 60)
    print()

    issues_found = []
    recommendations = []

    # 1. Check if we're using GitHub Actions (correct approach)
    print("📋 1. Deployment Method Check")
    print("-" * 30)

    workflow_file = Path(".github/workflows/ai-workspace-deploy.yml")
    if workflow_file.exists():
        print("✅ Using GitHub Actions deployment (CORRECT)")
        print("✅ CNAME file not required for GitHub Actions deployment")
        print()
    else:
        print("❌ No GitHub Actions workflow found")
        issues_found.append("Missing GitHub Actions deployment workflow")
        recommendations.append("Create .github/workflows/ai-workspace-deploy.yml")
        print()

    # 2. Check repository permissions and settings
    print("📋 2. Repository Configuration Requirements")
    print("-" * 40)
    print("For GitHub Actions deployment to work, verify:")
    print("   🔧 Repository Settings > Pages > Source = 'GitHub Actions'")
    print("   🔧 Repository Settings > Pages > Custom domain = EMPTY")
    print("   🔧 Repository Settings > Actions > Allow all actions")
    print("   🔧 Repository has 'pages: write' and 'id-token: write' permissions")
    print()

    # 3. Check workflow configuration
    print("📋 3. GitHub Actions Workflow Configuration")
    print("-" * 42)

    if workflow_file.exists():
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

            # Check for proper environment
            if 'environment:' in content and 'github-pages' in content:
                print("✅ Workflow has github-pages environment")
            else:
                print("⚠️  Workflow may be missing github-pages environment")

        except Exception as e:
            print(f"❌ Error reading workflow file: {e}")
            issues_found.append("Cannot read workflow file")
    print()

    # 4. Check for common file conflicts
    print("📋 4. File Conflict Check")
    print("-" * 25)

    # Check for CNAME file (should NOT exist for default domain)
    cname_files = []
    for cname_path in [Path("CNAME"), Path("ai-workspace/CNAME")]:
        if cname_path.exists():
            cname_files.append(str(cname_path))

    if cname_files:
        print(f"⚠️  CNAME files found: {', '.join(cname_files)}")
        print("   For GitHub Actions + default domain, CNAME files are ignored")
        print("   Remove them if you're not using a custom domain")
    else:
        print("✅ No CNAME files (correct for default domain)")

    # Check for Jekyll conflicts
    if Path("_config.yml").exists():
        print("⚠️  Jekyll _config.yml found - may conflict with static deployment")
        recommendations.append("Ensure .nojekyll file is in build output")

    print()

    # 5. GitHub Actions specific requirements
    print("📋 5. GitHub Actions Deployment Requirements")
    print("-" * 45)

    print("Required manual verification steps:")
    print("1. 🌐 GitHub Pages Settings:")
    print("   - Go to: https://github.com/Bryan-Roe-ai/semantic-kernel/settings/pages")
    print("   - Source: Must be 'GitHub Actions' (NOT 'Deploy from a branch')")
    print("   - Custom domain: Must be EMPTY")
    print()

    print("2. 🔐 Repository Permissions:")
    print("   - Go to: https://github.com/Bryan-Roe-ai/semantic-kernel/settings/actions")
    print("   - Workflow permissions: 'Read and write permissions'")
    print("   - OR ensure GITHUB_TOKEN has required permissions")
    print()

    print("3. 🚀 Recent Workflow Runs:")
    print("   - Go to: https://github.com/Bryan-Roe-ai/semantic-kernel/actions")
    print("   - Check 'AI Workspace Deployment' workflow runs")
    print("   - Verify 'deploy-pages' job completed successfully")
    print()

    # 6. Common solutions based on GitHub documentation
    print("📋 6. Common Solutions")
    print("-" * 22)

    print("If site still shows 404 after workflow success:")
    print("✅ Wait 5-10 minutes for DNS propagation")
    print("✅ Clear browser cache")
    print("✅ Try incognito/private browsing mode")
    print("✅ Check if repository is public (required for GitHub Pages)")
    print()

    print("If workflow is failing:")
    print("✅ Check Actions tab for specific error messages")
    print("✅ Ensure repository has GitHub Actions enabled")
    print("✅ Verify artifact upload/download steps work")
    print("✅ Check if organization has GitHub Actions restrictions")
    print()

    # Summary
    print("📊 DIAGNOSTIC SUMMARY")
    print("=" * 25)

    if issues_found:
        print(f"❌ Issues found: {len(issues_found)}")
        for i, issue in enumerate(issues_found, 1):
            print(f"   {i}. {issue}")
        print()

    if recommendations:
        print(f"💡 Recommendations: {len(recommendations)}")
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec}")
        print()

    if not issues_found:
        print("✅ No technical issues detected in repository setup")
        print("🎯 Most likely cause: GitHub Pages settings not configured")
        print("🔧 ACTION REQUIRED: Configure GitHub Pages settings manually")
        print()

    print("🌐 Expected URL: https://bryan-roe-ai.github.io/semantic-kernel/")
    print("📞 Next step: Configure GitHub Pages settings in repository")

    return len(issues_found) == 0


def main():
    success = check_repository_setup_errors()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
