
# GPU Helper Functions for Semantic Kernel Workspace
import torch
import json
import os

def load_gpu_config():
    """Load GPU configuration for the workspace"""
    config_path = "/home/broe/semantic-kernel/workspace_gpu_config.json"
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    return {"gpu_setup": {"cuda_available": False}}

def get_optimal_device():
    """Get the optimal device for computation"""
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")

def get_recommended_batch_size(component="default"):
    """Get recommended batch size for different components"""
    config = load_gpu_config()
    component_config = config.get(component, {})
    return component_config.get("recommended_batch_size", 4 if torch.cuda.is_available() else 1)

def setup_mixed_precision():
    """Setup mixed precision training if available"""
    if torch.cuda.is_available():
        return torch.cuda.amp.GradScaler()
    return None

def monitor_gpu_memory():
    """Monitor GPU memory usage"""
    if torch.cuda.is_available():
        allocated = torch.cuda.memory_allocated(0)
        reserved = torch.cuda.memory_reserved(0)
        total = torch.cuda.get_device_properties(0).total_memory
        return {
            "allocated_mb": allocated / 1024**2,
            "reserved_mb": reserved / 1024**2,
            "total_gb": total / 1024**3,
            "free_mb": (total - allocated) / 1024**2
        }
    return {"message": "No GPU available"}

def cleanup_gpu_memory():
    """Clean up GPU memory"""
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()
        return True
    return False

# Configuration constants
DEVICE = get_optimal_device()
GPU_CONFIG = load_gpu_config()

print(f"GPU Helper functions loaded. Device: {DEVICE}")
