# GPU Helper Functions for Semantic Kernel Workspace
import torch
import json
import gc
from contextlib import contextmanager

def load_gpu_config(notebook_name="general"):
    """Load GPU configuration for a specific notebook"""
    try:
        with open("/home/broe/semantic-kernel/workspace_gpu_configs.json", "r") as f:
            configs = json.load(f)
        return configs.get(notebook_name, configs["general"])
    except FileNotFoundError:
        print("GPU config file not found. Using defaults.")
        return {"device": "cuda" if torch.cuda.is_available() else "cpu"}

def setup_gpu_environment(config_name="general"):
    """Set up GPU environment based on configuration"""
    config = load_gpu_config(config_name)

    device = torch.device(config["gpu_settings"]["device"])

    # Set memory management
    if torch.cuda.is_available():
        torch.backends.cudnn.benchmark = True
        torch.backends.cudnn.enabled = True

    return device, config

@contextmanager 
def gpu_memory_context():
    """Context manager for GPU memory management"""
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        initial_memory = torch.cuda.memory_allocated()

    try:
        yield
    finally:
        if torch.cuda.is_available():
            final_memory = torch.cuda.memory_allocated()
            print(f"Memory used: {(final_memory - initial_memory) / 1024**2:.2f} MB")
            torch.cuda.empty_cache()

def monitor_gpu_usage():
    """Print current GPU usage"""
    if torch.cuda.is_available():
        allocated = torch.cuda.memory_allocated(0) / 1024**2
        reserved = torch.cuda.memory_reserved(0) / 1024**2
        total = torch.cuda.get_device_properties(0).total_memory / 1024**2

        print(f"GPU Memory - Allocated: {allocated:.1f} MB, Reserved: {reserved:.1f} MB, Total: {total:.1f} MB")
        print(f"Usage: {(allocated/total)*100:.1f}%")
    else:
        print("No GPU available")

def cleanup_gpu_memory():
    """Clean up GPU memory"""
    if torch.cuda.is_available():
        gc.collect()
        torch.cuda.empty_cache()
        torch.cuda.synchronize()
        print("GPU memory cleaned up")

# Example usage:
# device, config = setup_gpu_environment("neural_symbolic_agi")
# with gpu_memory_context():
#     # Your GPU operations here
#     pass
