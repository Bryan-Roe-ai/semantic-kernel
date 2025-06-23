#!/bin/bash

echo "🔧 Installing AGI Chat VS Code Extension..."

# Check if VS Code is installed
if ! command -v code &> /dev/null; then
    echo "❌ VS Code not found. Please install VS Code first."
    exit 1
fi

# Navigate to the simple extension directory
cd "$(dirname "$0")/vscode-agi-simple"

# Check if extension files exist
if [ ! -f "package.json" ] || [ ! -f "extension.js" ]; then
    echo "❌ Extension files not found. Please ensure you're in the correct directory."
    exit 1
fi

echo "📦 Installing extension..."

# Install the extension using VS Code CLI
if code --install-extension . --force; then
    echo "✅ AGI Chat extension installed successfully!"
    echo ""
    echo "🎯 How to use:"
    echo "   1. Open VS Code"
    echo "   2. Press Ctrl+Shift+A to open AGI Chat"
    echo "   3. Or use @agi in the VS Code chat panel"
    echo "   4. Example: '@agi Hello! Can you help me with coding?'"
    echo ""
    echo "⚙️  Make sure the AGI backend is running:"
    echo "   cd ../agi-backend-server && python3 main.py"
    echo ""
    echo "🌐 Or use the web interface:"
    echo "   ./launch_agi_chat.sh"
else
    echo "❌ Failed to install extension. You can try manual installation:"
    echo "   1. Open VS Code"
    echo "   2. Press Ctrl+Shift+P"
    echo "   3. Type 'Extensions: Install from VSIX'"
    echo "   4. Navigate to this folder and select the extension"
fi
