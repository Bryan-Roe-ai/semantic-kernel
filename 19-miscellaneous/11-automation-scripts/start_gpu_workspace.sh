#!/bin/bash
# GPU Setup Startup Script for Semantic Kernel Workspace

echo "🚀 Starting GPU-accelerated Semantic Kernel workspace..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install essential packages
echo "Installing GPU packages..."
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121 --quiet
pip install numpy pandas matplotlib seaborn jupyter --quiet

# Test GPU
python3 -c "
import torch
print(f'CUDA available: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'GPU: {torch.cuda.get_device_name(0)}')
    print(f'Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB')
"

echo "✅ GPU workspace ready!"
echo "📝 Run 'jupyter notebook' to start working with GPU-accelerated notebooks"
