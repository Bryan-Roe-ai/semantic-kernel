#!/bin/bash
# Entrypoint script for Semantic Kernel development container

set -e

echo "🚀 Starting Semantic Kernel Development Container..."

# Ensure proper ownership
sudo chown -R vscode:vscode /workspaces/semantic-kernel || true

# Set up environment
export DOTNET_CLI_TELEMETRY_OPTOUT=1
export PYTHONUNBUFFERED=1

# Initialize Python environment if needed
if [ ! -d "/workspaces/semantic-kernel/venv" ]; then
    echo "📦 Setting up Python virtual environment..."
    python3.12 -m venv /workspaces/semantic-kernel/venv
    source /workspaces/semantic-kernel/venv/bin/activate
    
    if [ -f "/workspaces/semantic-kernel/requirements.txt" ]; then
        echo "📥 Installing Python dependencies..."
        pip install --upgrade pip
        pip install -r /workspaces/semantic-kernel/requirements.txt
    fi
fi

# Restore .NET workloads
echo "🔧 Restoring .NET workloads..."
dotnet workload restore || echo "⚠️  Workload restore failed, continuing..."

# Start MongoDB if needed (for development)
if command -v mongod &> /dev/null; then
    echo "🍃 Starting MongoDB..."
    sudo mkdir -p /data/db
    sudo chown -R mongodb:mongodb /data/db
    if sudo systemctl start mongod; then
        echo "✅ MongoDB started with systemctl."
    else
        echo "⚠️  systemctl failed to start MongoDB, attempting to start with mongod --fork..."
        if sudo mongod --fork --logpath /var/log/mongod.log --dbpath /data/db; then
            echo "✅ MongoDB started with mongod --fork."
        else
            echo "⚠️  MongoDB start failed with both systemctl and mongod --fork, continuing..."
        fi
    fi
fi

echo "✅ Container initialization complete!"

# Execute the command passed to the container
exec "$@"
