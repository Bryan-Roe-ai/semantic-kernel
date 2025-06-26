#!/usr/bin/env python3
"""
import re
Validate Repository module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

import os
import sys
import yaml
from pathlib import Path


def validate_github_actions():
    """Validate GitHub Actions workflows."""
    print("🔍 Validating GitHub Actions workflows...")

    # Discover all GitHub Actions workflow files recursively
    workflow_files = list(Path('.').glob('**/.github/workflows/*.yml'))
    if not workflow_files:
        print("❌ No GitHub Actions workflows found")
        return False

    valid_workflows = 0
    total_workflows = len(workflow_files)

    for workflow_file in workflow_files:
        try:
            with open(workflow_file, 'r', encoding='utf-8') as f:
                yaml.safe_load(f)
            print(f"✅ {workflow_file.relative_to(Path('.'))}")
            valid_workflows += 1
        except yaml.YAMLError as err:
            print(f"❌ {workflow_file.relative_to(Path('.'))}: {err}")
        except Exception as err:  # noqa: E722
            print(f"⚠️  {workflow_file.relative_to(Path('.'))}: {err}")

    print(f"📊 {valid_workflows}/{total_workflows} workflows valid")
    return valid_workflows == total_workflows


def validate_ai_workspace():
    """Validate AI workspace structure."""
    print("\n🤖 Validating AI Workspace...")

    ai_workspace = Path("ai-workspace")
    if not ai_workspace.exists():
        print("❌ ai-workspace directory not found")
        return False

    # Check required structure
    required_items = {
        "directories": [
            "scripts",
            "01-notebooks",
            "02-agents",
            "03-models-training",
            "04-plugins",
            "05-samples-demos",
            "06-backend-services",
            "07-data-resources",
            "08-documentation",
            "09-deployment",
            "10-config",
        ],
        "files": [
            "README.md",
            "Dockerfile",
            "docker-compose.yml",
            "ai_workspace_control.py",
            "requirements-ci.txt",
        ],
    }

    missing_items = []

    for directory in required_items["directories"]:
        dir_path = ai_workspace / directory
        if dir_path.exists():
            print(f"✅ {directory}/")
        else:
            print(f"❌ {directory}/ (missing)")
            missing_items.append(f"directory: {directory}")

    for file_name in required_items["files"]:
        file_path = ai_workspace / file_name
        if file_path.exists():
            print(f"✅ {file_name}")
        else:
            print(f"❌ {file_name} (missing)")
            missing_items.append(f"file: {file_name}")

    # Check critical scripts
    print("\n🔧 Validating critical scripts...")
    critical_scripts = [
        "scripts/health_check.py",
        "scripts/ai_workspace_optimizer.py",
        "scripts/ai_workspace_monitor.py",
        "scripts/deployment_automator.py",
        "scripts/ai_model_manager.py",
    ]

    for script in critical_scripts:
        script_path = ai_workspace / script
        if script_path.exists():
            # Check if executable
            if os.access(script_path, os.X_OK):
                print(f"✅ {script} (executable)")
            else:
                print(f"⚠️  {script} (not executable)")
        else:
            print(f"❌ {script} (missing)")
            missing_items.append(f"script: {script}")

    if missing_items:
        print(f"\n❌ {len(missing_items)} missing items:")
        for item in missing_items:
            print(f"  - {item}")
        return False

    print("✅ AI Workspace structure validated")
    return True


def validate_python_syntax():
    """Validate Python syntax in key files."""
    print("\n🐍 Validating Python syntax...")

    ai_workspace = Path("ai-workspace")
    python_files = [
        "ai_workspace_control.py",
        "06-backend-services/simple_api_server.py",
        "scripts/health_check.py",
    ]

    syntax_errors = []

    for py_file in python_files:
        file_path = ai_workspace / py_file
        if file_path.exists():
            try:
                compile(file_path.read_text(), str(file_path), 'exec')
                print(f"✅ {py_file}")
            except SyntaxError as e:
                print(f"❌ {py_file}: {e}")
                syntax_errors.append(py_file)
        else:
            print(f"⚠️  {py_file} (not found)")

    if syntax_errors:
        print(f"\n❌ {len(syntax_errors)} syntax errors found")
        return False

    print("✅ Python syntax validated")
    return True


def validate_docker_files():
    """Validate Docker configuration."""
    print("\n🐳 Validating Docker files...")

    ai_workspace = Path("ai-workspace")
    docker_files = ["Dockerfile", "docker-compose.yml"]

    valid_docker = True

    for docker_file in docker_files:
        file_path = ai_workspace / docker_file
        if file_path.exists():
            # Basic validation - check if file is not empty
            if file_path.stat().st_size > 0:
                print(f"✅ {docker_file}")
            else:
                print(f"❌ {docker_file} (empty)")
                valid_docker = False
        else:
            print(f"❌ {docker_file} (missing)")
            valid_docker = False

    if valid_docker:
        print("✅ Docker files validated")

    return valid_docker


def main():
    """Main validation function."""
    print("🔍 AI Workspace Repository Validation")
    print("=" * 50)

    validations = [
        ("GitHub Actions", validate_github_actions),
        ("AI Workspace Structure", validate_ai_workspace),
        ("Python Syntax", validate_python_syntax),
        ("Docker Files", validate_docker_files),
    ]

    passed = 0
    total = len(validations)

    for name, validator in validations:
        try:
            if validator():
                passed += 1
            else:
                print(f"❌ {name} validation failed")
        except Exception as e:  # noqa: E722
            print(f"❌ {name} validation error: {e}")

    print("\n📊 Validation Summary")
    print("=" * 30)
    print('Passed: {}/{}'.format(passed, total))

    if passed == total:
        print("✅ All validations passed!")
        print("🚀 Repository is ready for deployment")
        return True
    else:
        print(f"❌ {total - passed} validations failed")
        print("🔧 Please fix the issues above")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
