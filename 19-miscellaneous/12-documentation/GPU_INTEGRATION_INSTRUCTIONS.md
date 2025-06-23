
# GPU Integration Instructions for Workspace Notebooks

## For neural_symbolic_agi.ipynb:
Add these imports at the beginning:
```python
import sys
sys.path.append('/home/broe/semantic-kernel')
from gpu_helpers import DEVICE, get_recommended_batch_size, setup_mixed_precision, cleanup_gpu_memory

# Use throughout the notebook:
device = DEVICE
batch_size = get_recommended_batch_size("neural_symbolic_agi")
scaler = setup_mixed_precision()
```

## For consciousness_agi.ipynb:
Add these imports at the beginning:
```python
import sys
sys.path.append('/home/broe/semantic-kernel')
from gpu_helpers import DEVICE, get_recommended_batch_size, monitor_gpu_memory

# Use throughout the notebook:
device = DEVICE
batch_size = get_recommended_batch_size("consciousness_agi")
```

## For finetune_gpt2_custom.py:
Add at the beginning:
```python
import sys
sys.path.append('/home/broe/semantic-kernel')
from gpu_helpers import load_gpu_config, get_optimal_device

config = load_gpu_config()
device = get_optimal_device()
```

## For any new notebooks:
```python
# Standard GPU setup for Semantic Kernel workspace
import sys
sys.path.append('/home/broe/semantic-kernel')
from gpu_helpers import *

print(f"GPU Setup: Device = {DEVICE}")
print(f"GPU Config: {GPU_CONFIG['gpu_setup']}")
```
