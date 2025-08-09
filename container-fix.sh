#!/bin/bash
# Container fix script for Semantic Kernel development

echo "🔧 Starting container fix process..."

# Ensure we have the necessary tools
echo "📦 Installing missing tools..."
if ! command -v dotnet &> /dev/null; then
    echo "Installing .NET SDK..."
    apk add --no-cache icu-libs krb5-libs libgcc libintl libssl3 libstdc++ zlib
    cd /tmp
    wget https://dot.net/v1/dotnet-install.sh
    chmod +x dotnet-install.sh
    ./dotnet-install.sh --channel 8.0 --install-dir /usr/share/dotnet
    export PATH="/usr/share/dotnet:$PATH"
    export DOTNET_ROOT="/usr/share/dotnet"
    echo 'export PATH="/usr/share/dotnet:$PATH"' >> ~/.bashrc
    echo 'export DOTNET_ROOT="/usr/share/dotnet"' >> ~/.bashrc
fi

if ! command -v npm &> /dev/null; then
    echo "Installing npm..."
    apk add npm
fi

# Validate the development environment
echo "✅ Running validation..."
./health-check.sh

echo "🎉 Container fix complete! You can now try 'Reopen in Container'."
