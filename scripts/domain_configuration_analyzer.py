#!/usr/bin/env python3
"""
GitHub Pages Domain Configuration Tool
====================================

This script helps diagnose and configure the correct domain setup
for GitHub Pages deployment.
"""

import os
import sys
from pathlib import Path


def analyze_domain_configuration(repo_path: str):
    """Analyze the current domain configuration and provide recommendations"""
    
    repo_path = Path(repo_path)
    cname_root = repo_path / "CNAME"
    cname_workspace = repo_path / "ai-workspace" / "CNAME"
    
    print("🌐 GitHub Pages Domain Configuration Analysis")
    print("=" * 60)
    
    # Check for CNAME files
    cname_exists = False
    cname_location = None
    cname_content = None
    
    if cname_root.exists():
        cname_exists = True
        cname_location = "repository root"
        with open(cname_root, 'r') as f:
            cname_content = f.read().strip()
    elif cname_workspace.exists():
        cname_exists = True
        cname_location = "ai-workspace directory"
        with open(cname_workspace, 'r') as f:
            cname_content = f.read().strip()
    
    print(f"\n📋 Current Configuration:")
    print(f"Repository: Bryan-Roe-ai/semantic-kernel")
    print(f"CNAME file present: {'✅ Yes' if cname_exists else '❌ No'}")
    
    if cname_exists:
        print(f"CNAME location: {cname_location}")
        print(f"CNAME content: '{cname_content}'")
        print(f"Expected URL: https://{cname_content}/")
        
        print(f"\n🎯 CUSTOM DOMAIN CONFIGURATION DETECTED")
        print(f"With a CNAME file present, GitHub Pages expects to serve your site at:")
        print(f"  📍 https://{cname_content}/")
        print(f"\nFor this to work, you need:")
        print(f"  1. DNS configured to point {cname_content} to Bryan-Roe-ai.github.io")
        print(f"  2. GitHub Pages settings configured for custom domain")
        print(f"  3. Custom domain field in GitHub settings set to: {cname_content}")
        
    else:
        print(f"Expected URL: https://bryan-roe-ai.github.io/semantic-kernel/")
        
        print(f"\n🎯 DEFAULT DOMAIN CONFIGURATION")
        print(f"No CNAME file means you're using the default GitHub Pages domain:")
        print(f"  📍 https://bryan-roe-ai.github.io/semantic-kernel/")
        print(f"\nFor this to work, you need:")
        print(f"  1. GitHub Pages source set to 'GitHub Actions'")
        print(f"  2. Custom domain field in GitHub settings should be EMPTY")
        print(f"  3. GitHub Actions workflow should deploy successfully")
    
    print(f"\n🔧 TROUBLESHOOTING STEPS:")
    
    if cname_exists:
        print(f"\n📌 FOR CUSTOM DOMAIN ({cname_content}):")
        print(f"1. Verify DNS configuration:")
        print(f"   nslookup {cname_content}")
        print(f"   (Should point to Bryan-Roe-ai.github.io)")
        print(f"2. Check GitHub Pages settings:")
        print(f"   - Go to: https://github.com/Bryan-Roe-ai/semantic-kernel/settings/pages")
        print(f"   - Custom domain: {cname_content}")
        print(f"   - Source: GitHub Actions")
        print(f"3. Wait for DNS propagation (can take 24-48 hours)")
        print(f"4. Check for SSL certificate provisioning")
        
        print(f"\n🔄 TO SWITCH TO DEFAULT DOMAIN:")
        print(f"If you want to use the default domain instead:")
        print(f"1. Remove the CNAME file: rm {cname_root if cname_root.exists() else cname_workspace}")
        print(f"2. Clear custom domain in GitHub settings")
        print(f"3. Commit and push changes")
        
    else:
        print(f"\n📌 FOR DEFAULT DOMAIN:")
        print(f"1. Check GitHub Pages settings:")
        print(f"   - Go to: https://github.com/Bryan-Roe-ai/semantic-kernel/settings/pages")
        print(f"   - Custom domain: EMPTY (leave blank)")
        print(f"   - Source: GitHub Actions")
        print(f"2. Verify GitHub Actions workflow:")
        print(f"   - Go to: https://github.com/Bryan-Roe-ai/semantic-kernel/actions")
        print(f"   - Look for successful 'AI Workspace Deployment' runs")
        print(f"3. Test the URL: https://bryan-roe-ai.github.io/semantic-kernel/")
        
        print(f"\n🔄 TO ADD CUSTOM DOMAIN:")
        print(f"If you want to use a custom domain:")
        print(f"1. Create CNAME file: echo 'yourdomain.com' > CNAME")
        print(f"2. Configure DNS with your provider")
        print(f"3. Set custom domain in GitHub Pages settings")
        print(f"4. Commit and push changes")
    
    print(f"\n🚀 RECOMMENDED ACTIONS:")
    
    # Provide specific recommendations based on current state
    if cname_exists:
        print(f"✅ You have a custom domain configured")
        print(f"🔍 Check if DNS is properly configured for {cname_content}")
        print(f"🔍 Verify GitHub Pages settings allow custom domain")
        print(f"⏳ Custom domains can take 24-48 hours to propagate")
    else:
        print(f"✅ You're using the default GitHub Pages domain (recommended)")
        print(f"🔍 Main issue likely: GitHub Pages settings not configured")
        print(f"🎯 Go to repository Settings > Pages and set Source to 'GitHub Actions'")
        print(f"🎯 Leave custom domain field EMPTY")
    
    print(f"\n📞 NEXT STEPS:")
    print(f"1. Visit: https://github.com/Bryan-Roe-ai/semantic-kernel/settings/pages")
    print(f"2. Configure as described above")
    print(f"3. Check Actions tab for successful deployments")
    print(f"4. Test the expected URL")
    
    print(f"\n🛠️ DIAGNOSTIC COMMANDS:")
    print(f"# Run full diagnostic")
    print(f"python scripts/github_pages_diagnostic.py")
    print(f"")
    print(f"# Test website accessibility")
    print(f"python scripts/verify_github_pages.py")


def main():
    if len(sys.argv) > 1:
        repo_path = sys.argv[1]
    else:
        repo_path = "/workspaces/semantic-kernel"
    
    analyze_domain_configuration(repo_path)


if __name__ == "__main__":
    main()
