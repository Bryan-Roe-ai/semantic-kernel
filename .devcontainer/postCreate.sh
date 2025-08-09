#!/usr/bin/env bash
set -euo pipefail

echo "[postCreate] Starting post-create setup..."

# Ensure ownership of workspace only (avoid system directories)
if [ "${USERNAME:-vscode}" != "root" ]; then
  echo "[postCreate] Adjusting workspace ownership (if needed)..."
  sudo chown -R "${USERNAME:-vscode}:${USERNAME:-vscode}" /workspaces/semantic-kernel || true
fi

# Dotnet: verify access rather than blanket chown of /usr/share/dotnet
if command -v dotnet >/dev/null 2>&1; then
  echo "[postCreate] .NET SDK version: $(dotnet --version)"
fi

# Python: install poetry if not present (lightweight)
if ! command -v poetry >/dev/null 2>&1; then
  echo "[postCreate] Installing poetry..."
  curl -sSL https://install.python-poetry.org | python3 - --version 1.8.3
  export PATH="$HOME/.local/bin:$PATH"
fi

# Optional: pre-create a venv for python project if pyproject.toml exists
if [ -f /workspaces/semantic-kernel/python/pyproject.toml ]; then
  echo "[postCreate] Bootstrapping python dependencies (no dev) ..."
  cd /workspaces/semantic-kernel/python
  python3 -m pip install --upgrade pip
  # Use poetry export to speed up caching if lock present
  if [ -f poetry.lock ]; then
    poetry export -f requirements.txt --without-hashes -o /tmp/requirements.txt || true
    python3 -m pip install -r /tmp/requirements.txt || true
  fi
fi

echo "[postCreate] Completed."
