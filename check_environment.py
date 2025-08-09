#!/usr/bin/env python3
# Quick environment check
import subprocess
import sys

def check_command(cmd):
    try:
        subprocess.run(cmd, shell=True, check=True, capture_output=True)
        return True
    except:
        return False

print("🔍 AI Environment Health Check")
print("=" * 40)

checks = [
    ("Python", "python3 --version"),
    ("Git", "git --version"),
    ("VS Code", "code --version"),
    ("Docker", "docker --version"),
    (".NET", "dotnet --version"),
]

for name, cmd in checks:
    status = "✅" if check_command(cmd) else "❌"
    print(f"{status} {name}")

print("\n📝 To fix missing components:")
print("• Install missing tools using package manager")
print("• Run: python3 setup_environment.py")
print("• Check VS Code extensions")
