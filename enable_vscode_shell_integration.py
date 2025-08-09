#!/usr/bin/env python3
import os
import shutil
import subprocess
from pathlib import Path

# Shells and their config files
SHELLS = {
    "bash": {
        "config": "~/.bashrc",
        "snippet": '[[ "$TERM_PROGRAM" == "vscode" ]] && . "$(code --locate-shell-integration-path bash)"',
    },
    "zsh": {
        "config": "~/.zshrc",
        "snippet": '[[ "$TERM_PROGRAM" == "vscode" ]] && . "$(code --locate-shell-integration-path zsh)"',
    },
    "fish": {
        "config": os.path.expandvars("$HOME/.config/fish/config.fish"),
        "snippet": 'string match -q "$TERM_PROGRAM" "vscode"\nand . (code --locate-shell-integration-path fish)',
    },
    "pwsh": {
        "config": os.path.expandvars("$HOME/.config/powershell/Microsoft.PowerShell_profile.ps1"),
        "snippet": 'if ($env:TERM_PROGRAM -eq "vscode") { . "$(code --locate-shell-integration-path pwsh)" }',
    },
}


def is_shell_installed(shell_name):
    return shutil.which(shell_name) is not None

def append_snippet(config_path, snippet):
    config_path = os.path.expanduser(config_path)
    config_file = Path(config_path)
    if not config_file.exists():
        config_file.parent.mkdir(parents=True, exist_ok=True)
        config_file.touch()
    # Backup
    backup_path = str(config_file) + ".bak"
    shutil.copy2(config_file, backup_path)
    # Check if snippet already present
    with open(config_file, "r") as f:
        content = f.read()
    if snippet in content:
        print(f"Snippet already present in {config_file}")
        return
    # Append
    with open(config_file, "a") as f:
        f.write(f"\n# VS Code shell integration\n{snippet}\n")
    print(f"Appended snippet to {config_file} (backup at {backup_path})")

def main():
    for shell, info in SHELLS.items():
        if is_shell_installed(shell):
            append_snippet(info["config"], info["snippet"])
        else:
            print(f"{shell} not found, skipping.")
    print("\nDone. Restart your terminal or source your config file to enable integration.")

if __name__ == "__main__":
    main()
