
# GPU Integration Instructions for Semantic Kernel Workspace

## For neural_symbolic_agi.ipynb:
1. Add at the beginning of the notebook:
   ```python
   import sys
   sys.path.append('/home/broe/semantic-kernel')
   from gpu_helpers import setup_gpu_environment, gpu_memory_context

   device, config = setup_gpu_environment("neural_symbolic_agi")
   ```

2. Use the device in your models:
   ```python
   model = YourModel().to(device)
   ```

3. Wrap training loops with memory management:
   ```python
   with gpu_memory_context():
       # Your training code here
   ```

## For consciousness_agi.ipynb:
1. Similar setup but use "consciousness_agi" config
2. Enable mixed precision:
   ```python
   from torch.cuda.amp import autocast, GradScaler
   scaler = GradScaler()
   ```

## For finetune_gpt2_custom.py:
1. Load the GPT-2 specific configuration
2. Use the recommended training arguments from the config

## General Tips:
- Always monitor GPU memory with monitor_gpu_usage()
- Clean up memory between experiments with cleanup_gpu_memory()
- Use the configurations as starting points and adjust based on your specific needs
