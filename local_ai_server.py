#!/usr/bin/env python3
"""
Local AI Server with GPU Acceleration Support
Automatically detects and configures GPU acceleration for local AI models.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_gpu_availability():
    """Check for GPU availability and return configuration"""
    gpu_info = {
        'cuda_available': False,
        'metal_available': False,
        'cpu_optimized': False,
        'device': 'cpu'
    }

    try:
        # Check for CUDA (NVIDIA)
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
        if result.returncode == 0:
            gpu_info['cuda_available'] = True
            gpu_info['device'] = 'cuda'
            print("✅ NVIDIA GPU detected")
        else:
            print("❌ NVIDIA GPU not found")
    except FileNotFoundError:
        print("❌ nvidia-smi not found")

    # Check for Metal (Apple Silicon)
    if platform.system() == 'Darwin' and 'arm' in platform.machine().lower():
        gpu_info['metal_available'] = True
        gpu_info['device'] = 'mps'
        print("✅ Apple Silicon detected - Metal Performance Shaders available")

    # CPU optimization check
    try:
        import cpuinfo
        cpu_info = cpuinfo.get_cpu_info()
        if 'avx2' in cpu_info.get('flags', []) or 'avx' in cpu_info.get('flags', []):
            gpu_info['cpu_optimized'] = True
            print("✅ CPU supports AVX/AVX2 - optimized CPU acceleration available")
    except ImportError:
        # Fallback CPU check
        with open('/proc/cpuinfo', 'r') as f:
            cpu_info = f.read()
            if 'avx2' in cpu_info or 'avx' in cpu_info:
                gpu_info['cpu_optimized'] = True
                print("✅ CPU supports AVX/AVX2 - optimized CPU acceleration available")

    if not any([gpu_info['cuda_available'], gpu_info['metal_available'], gpu_info['cpu_optimized']]):
        print("⚠️  No hardware acceleration detected - using basic CPU mode")

    return gpu_info

def setup_environment_variables(gpu_info):
    """Set up environment variables for optimal performance"""
    env_vars = {}

    # CUDA settings
    if gpu_info['cuda_available']:
        env_vars.update({
            'CUDA_VISIBLE_DEVICES': '0',
            'TORCH_CUDA_ARCH_LIST': '6.0;6.1;7.0;7.5;8.0;8.6',
            'FORCE_CUDA': '1'
        })

    # CPU optimization
    if gpu_info['cpu_optimized']:
        env_vars.update({
            'OMP_NUM_THREADS': str(os.cpu_count()),
            'OPENBLAS_NUM_THREADS': str(os.cpu_count()),
            'MKL_NUM_THREADS': str(os.cpu_count()),
            'VECLIB_MAXIMUM_THREADS': str(os.cpu_count()),
            'NUMEXPR_NUM_THREADS': str(os.cpu_count())
        })

    # Set environment variables
    for key, value in env_vars.items():
        os.environ[key] = value
        print(f"🔧 Set {key}={value}")

    return env_vars

def install_optimized_packages(gpu_info):
    """Install packages optimized for available hardware"""
    packages = []

    if gpu_info['cuda_available']:
        packages.extend([
            'torch>=2.0.0+cu121',
            'torchvision+cu121',
            'torchaudio+cu121',
            '--index-url https://download.pytorch.org/whl/cu121'
        ])
    elif gpu_info['metal_available']:
        packages.extend([
            'torch>=2.0.0',
            'torchvision',
            'torchaudio'
        ])
    else:
        packages.extend([
            'torch>=2.0.0+cpu',
            'torchvision+cpu',
            'torchaudio+cpu',
            '--index-url https://download.pytorch.org/whl/cpu'
        ])

    # Common packages for local AI
    packages.extend([
        'transformers>=4.30.0',
        'accelerate>=0.20.0',
        'optimum>=1.9.0',
        'safetensors>=0.3.0',
        'tokenizers>=0.13.0'
    ])

    # GPU-specific packages
    if gpu_info['cuda_available']:
        packages.extend([
            'bitsandbytes>=0.39.0',
            'auto-gptq>=0.2.0',
            'flash-attn>=2.0.0'
        ])

    print("📦 Installing optimized packages...")
    for package in packages:
        if package.startswith('--'):
            continue
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', package],
                         check=True, capture_output=True)
            print(f"✅ Installed {package}")
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Failed to install {package}: {e}")

def create_local_ai_config():
    """Create configuration for local AI models"""
    config = {
        'model_path': str(Path.home() / '.cache' / 'huggingface' / 'transformers'),
        'device_map': 'auto',
        'torch_dtype': 'float16' if gpu_info['cuda_available'] else 'float32',
        'trust_remote_code': True,
        'use_fast_tokenizer': True
    }

    config_path = Path('.') / 'local_ai_config.json'
    with open(config_path, 'w') as f:
        import json
        json.dump(config, f, indent=2)

    print(f"📝 Created local AI config at {config_path}")
    return config

def start_local_server():
    """Start a simple local AI server"""
    print("🚀 Starting local AI server...")
    print("Server would start here - implement FastAPI/Flask server")
    print("Configure with Semantic Kernel connectors")

if __name__ == "__main__":
    print("🔍 Detecting hardware capabilities...")
    gpu_info = check_gpu_availability()

    print("\n🔧 Setting up environment...")
    env_vars = setup_environment_variables(gpu_info)

    print("\n📦 Installing optimized packages...")
    # Uncomment to actually install packages
    # install_optimized_packages(gpu_info)

    print("\n📝 Creating configuration...")
    config = create_local_ai_config()

    print("\n✅ Local AI setup complete!")
    print(f"Device: {gpu_info['device']}")
    print(f"CUDA Available: {gpu_info['cuda_available']}")
    print(f"Metal Available: {gpu_info['metal_available']}")
    print(f"CPU Optimized: {gpu_info['cpu_optimized']}")
