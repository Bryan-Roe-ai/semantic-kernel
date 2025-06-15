#!/usr/bin/env python3
"""
GitHub Pages Deployment Verification Tool
========================================

This script verifies that the GitHub Pages deployment is working
by checking the actual deployed website.
"""

import urllib.request
import urllib.error
import time
import sys
from typing import Optional


def check_website_accessibility(url: str, timeout: int = 10) -> tuple[bool, str]:
    """Check if a website is accessible and return status"""
    try:
        # Create request with proper headers
        request = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (compatible; GitHub-Pages-Checker/1.0)'
            }
        )

        # Try to access the website
        with urllib.request.urlopen(request, timeout=timeout) as response:
            content = response.read().decode('utf-8')
            status_code = response.getcode()

            if status_code == 200:
                # Check if it looks like our AI Workspace page
                if 'AI Workspace' in content and 'html' in content.lower():
                    return True, f"✅ Website is accessible and contains expected content (HTTP {status_code})"
                else:
                    return False, f"⚠️ Website accessible but doesn't contain expected AI Workspace content (HTTP {status_code})"
            else:
                return False, f"❌ Website returned HTTP {status_code}"

    except urllib.error.HTTPError as e:
        return False, f"❌ HTTP Error {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        return False, f"❌ URL Error: {e.reason}"
    except Exception as e:
        return False, f"❌ Unexpected error: {str(e)}"


def verify_deployment(repo_owner: str, repo_name: str, max_attempts: int = 5, delay: int = 30):
    """Verify the GitHub Pages deployment with retries"""

    # Construct the GitHub Pages URL
    github_pages_url = f"https://{repo_owner}.github.io/{repo_name}/"

    print("🚀 GitHub Pages Deployment Verification")
    print("=" * 50)
    print(f"Repository: {repo_owner}/{repo_name}")
    print(f"Expected URL: {github_pages_url}")
    print(f"Max attempts: {max_attempts}")
    print(f"Delay between attempts: {delay} seconds")
    print()

    for attempt in range(1, max_attempts + 1):
        print(f"🔍 Attempt {attempt}/{max_attempts}: Checking website accessibility...")

        # Check the website
        is_accessible, message = check_website_accessibility(github_pages_url)
        print(f"   {message}")

        if is_accessible:
            print("\n🎉 SUCCESS: GitHub Pages deployment is working!")
            print(f"✅ Your AI Workspace is accessible at: {github_pages_url}")
            return True

        if attempt < max_attempts:
            print(f"   ⏳ Waiting {delay} seconds before next attempt...")
            time.sleep(delay)
        else:
            print(f"\n❌ FAILURE: Website not accessible after {max_attempts} attempts")

    # Final troubleshooting suggestions
    print("\n🔧 TROUBLESHOOTING SUGGESTIONS:")
    print("1. Check GitHub repository Settings > Pages:")
    print("   - Ensure Source is set to 'GitHub Actions'")
    print("   - NOT 'Deploy from a branch'")
    print("\n2. Check GitHub Actions tab:")
    print(f"   - Go to https://github.com/{repo_owner}/{repo_name}/actions")
    print("   - Look for 'AI Workspace Deployment' workflow runs")
    print("   - Check if any recent runs failed")
    print("\n3. Check workflow files:")
    print("   - Ensure .github/workflows/ai-workspace-deploy.yml exists")
    print("   - Verify workflow has proper permissions")
    print("\n4. Check repository structure:")
    print("   - Ensure ai-workspace/ directory exists")
    print("   - Verify build script creates dist/ with index.html")
    print("\n5. Wait longer:")
    print("   - GitHub Pages can take 5-10 minutes to deploy")
    print("   - DNS propagation may take additional time")

    return False


def main():
    # Parse command line arguments or use defaults
    if len(sys.argv) >= 3:
        repo_owner = sys.argv[1]
        repo_name = sys.argv[2]
    else:
        # Default values for this repository
        repo_owner = "Bryan-Roe-ai"
        repo_name = "semantic-kernel"

    # Allow customizing max attempts and delay
    max_attempts = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    delay = int(sys.argv[4]) if len(sys.argv) > 4 else 30

    success = verify_deployment(repo_owner, repo_name, max_attempts, delay)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
