#!/bin/bash

# GPU Setup Script for Semantic Kernel Workspace
# This script configures GPU acceleration for the entire workspace

set -e

echo "=== Semantic Kernel GPU Setup Script ==="
echo "This script will configure GPU acceleration for your workspace"
echo ""

# Check if NVIDIA GPU is available
if command -v nvidia-smi &> /dev/null; then
    echo "✅ NVIDIA GPU detected:"
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
    echo ""
else
    echo "⚠️  No NVIDIA GPU detected or nvidia-smi not available"
    echo "This script will install CPU versions of packages"
    echo ""
fi

# Check CUDA installation
if command -v nvcc &> /dev/null; then
    echo "✅ CUDA toolkit detected:"
    nvcc --version | grep "release"
    echo ""
else
    echo "⚠️  CUDA toolkit not detected"
    echo "Please install CUDA toolkit for GPU acceleration"
    echo ""
fi

# Create virtual environment if it doesn't exist
if [ ! -d "gpu_env" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv gpu_env
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
source gpu_env/bin/activate
echo "✅ Virtual environment activated"

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install GPU requirements
echo "Installing GPU-accelerated packages..."
if [ -f "gpu_requirements.txt" ]; then
    pip install -r gpu_requirements.txt
    echo "✅ GPU requirements installed"
else
    echo "❌ gpu_requirements.txt not found"
    exit 1
fi

# Verify installations
echo ""
echo "=== Verifying GPU Setup ==="

# Check PyTorch GPU
python3 -c "
import torch
print(f'PyTorch version: {torch.__version__}')
print(f'CUDA available: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'CUDA version: {torch.version.cuda}')
    print(f'GPU device: {torch.cuda.get_device_name(0)}')
"

# Check TensorFlow GPU
python3 -c "
try:
    import tensorflow as tf
    print(f'TensorFlow version: {tf.__version__}')
    gpus = tf.config.list_physical_devices('GPU')
    print(f'TensorFlow GPU devices: {len(gpus)}')
    if gpus:
        for gpu in gpus:
            print(f'  {gpu}')
except ImportError:
    print('TensorFlow not installed')
"

echo ""
echo "=== Setup Instructions ==="
echo "1. Activate the environment: source gpu_env/bin/activate"
echo "2. Open Jupyter: jupyter notebook"
echo "3. Run the GPU setup notebook: gpu_setup_complete.ipynb"
echo "4. Test AGI notebooks: neural_symbolic_agi.ipynb, consciousness_agi.ipynb"
echo ""
echo "=== GPU Setup Complete! ==="

# Make the script executable
chmod +x setup_gpu.sh
