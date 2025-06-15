#!/usr/bin/env python3
"""
Simple health check for AI Workspace CI/CD
"""

import os
import sys
from pathlib import Path

def check_workspace_health():
    """Check basic workspace health for CI/CD."""
    workspace_root = Path(".")

    print("🔍 AI Workspace Health Check")
    print("=" * 40)

    # Check required directories
    required_dirs = [
        "scripts",
        "06-backend-services",
        "05-samples-demos",
        "03-models-training",
        "04-plugins"
    ]

    missing_dirs = []
    for dir_name in required_dirs:
        dir_path = workspace_root / dir_name
        if dir_path.exists():
            print(f"✅ {dir_name}/")
        else:
            print(f"❌ {dir_name}/ (missing)")
            missing_dirs.append(dir_name)

    # Check required files
    required_files = [
        "ai_workspace_control.py",
        "README.md",
        "Dockerfile",
        "requirements-ci.txt"
    ]

    missing_files = []
    for file_name in required_files:
        file_path = workspace_root / file_name
        if file_path.exists():
            print(f"✅ {file_name}")
        else:
            print(f"❌ {file_name} (missing)")
            missing_files.append(file_name)

    # Check Python syntax of main files
    python_files = [
        "ai_workspace_control.py",
        "06-backend-services/simple_api_server.py"
    ]

    syntax_errors = []
    for py_file in python_files:
        file_path = workspace_root / py_file
        if file_path.exists():
            try:
                compile(file_path.read_text(), str(file_path), 'exec')
                print(f"✅ {py_file} (syntax OK)")
            except SyntaxError as e:
                print(f"❌ {py_file} (syntax error: {e})")
                syntax_errors.append(py_file)
        else:
            print(f"⚠️  {py_file} (not found)")

    # Summary
    print("\n📊 Health Check Summary")
    print("-" * 30)

    total_errors = len(missing_dirs) + len(missing_files) + len(syntax_errors)

    if total_errors == 0:
        print("✅ All checks passed!")
        print("🚀 Workspace is ready for deployment")
        return True
    else:
        print(f"❌ {total_errors} issues found:")
        if missing_dirs:
            print(f"  - Missing directories: {', '.join(missing_dirs)}")
        if missing_files:
            print(f"  - Missing files: {', '.join(missing_files)}")
        if syntax_errors:
            print(f"  - Syntax errors: {', '.join(syntax_errors)}")
        return False

if __name__ == "__main__":
    success = check_workspace_health()
    sys.exit(0 if success else 1)
