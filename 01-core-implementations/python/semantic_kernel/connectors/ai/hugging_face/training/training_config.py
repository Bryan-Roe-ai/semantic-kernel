# Copyright (c) Microsoft. All rights reserved.

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel

from semantic_kernel.kernel_pydantic import KernelBaseModel


class TrainingArgumentsConfig(KernelBaseModel):
    """Configuration for the training process.

    This class provides configuration options for fine-tuning models using the Hugging Face Transformers library.
    """

    output_dir: str = "output"
    """Where to save the model."""
    
    overwrite_output_dir: bool = False
    """Overwrite the content of the output directory."""
    
    num_train_epochs: float = 3.0
    """Number of training epochs."""
    
    per_device_train_batch_size: int = 8
    """Batch size per GPU/TPU/CPU for training."""
    
    per_device_eval_batch_size: int = 8
    """Batch size per GPU/TPU/CPU for evaluation."""
    
    learning_rate: float = 5e-5
    """Initial learning rate."""
    
    weight_decay: float = 0.0
    """Weight decay applied to parameters."""
    
    max_grad_norm: float = 1.0
    """Maximum gradient norm (for gradient clipping)."""
    
    gradient_accumulation_steps: int = 1
    """Number of update steps to accumulate the gradients for."""
    
    lr_scheduler_type: str = "linear"
    """Learning rate scheduler type."""
    
    warmup_ratio: float = 0.0
    """Ratio of total training steps used for warmup."""
    
    logging_steps: int = 500
    """Log every X updates steps."""
    
    evaluation_strategy: str = "epoch"
    """Evaluation strategy to adopt during training."""
    
    save_strategy: str = "epoch"
    """Save strategy to adopt during training."""
    
    save_total_limit: Optional[int] = None
    """If a value is passed, will limit the total amount of checkpoints and delete older checkpoints."""
    
    load_best_model_at_end: bool = False
    """Whether or not to load the best model found during training at the end of training."""
    
    metric_for_best_model: str = "loss"
    """The metric to use to compare two different models when `load_best_model_at_end=True`."""
    
    greater_is_better: bool = False
    """Whether the `metric_for_best_model` should be maximized or not."""
    
    push_to_hub: bool = False
    """Whether or not to upload the model to the Hub."""
    
    hub_model_id: Optional[str] = None
    """The name of the repository to keep in sync with the local `output_dir`."""
    
    fp16: bool = False
    """Whether to use mixed precision (fp16) training."""
    
    bf16: bool = False
    """Whether to use bfloat16 (bf16) training."""

    local_rank: int = -1
    """Local rank for distributed training."""
    
    deepspeed: Optional[str] = None
    """Path to deepspeed config file for optimized training."""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the config to a dictionary for the Hugging Face Trainer."""
        return {k: v for k, v in self.__dict__.items() if v is not None}


class ModelTrainingConfig(KernelBaseModel):
    """Configuration for the model training.
    
    This class provides configuration options for the model to be fine-tuned.
    """
    
    model_name_or_path: str
    """Name or path of the model to be fine-tuned."""
    
    max_seq_length: int = 512
    """Maximum sequence length for input text processing."""
    
    use_lora: bool = False
    """Whether to use LoRA (Low-Rank Adaptation) for parameter-efficient fine-tuning."""
    
    lora_config: Optional[Dict[str, Any]] = None
    """Configuration for LoRA if `use_lora` is True."""
    
    tokenizer_name_or_path: Optional[str] = None
    """Name or path of the tokenizer (if different from model)."""
    
    add_special_tokens: bool = True
    """Whether to add special tokens when tokenizing the data."""
    
    padding: str = "max_length"
    """Padding strategy for tokenization."""
    
    truncation: bool = True
    """Whether to truncate sequences that exceed `max_seq_length`."""


class DatasetConfig(KernelBaseModel):
    """Configuration for the dataset to be used for fine-tuning."""
    
    train_file_path: Optional[str] = None
    """Path to the training data file (CSV or JSON)."""
    
    validation_file_path: Optional[str] = None
    """Path to the validation data file (CSV or JSON)."""
    
    test_file_path: Optional[str] = None
    """Path to the test data file (CSV or JSON)."""
    
    huggingface_dataset_name: Optional[str] = None
    """Name of a dataset from Hugging Face Hub to use."""
    
    huggingface_dataset_config_name: Optional[str] = None
    """Configuration name of the Hugging Face dataset."""
    
    text_column: str = "text"
    """Column name for input text in the dataset."""
    
    label_column: Optional[str] = None
    """Column name for labels in the dataset (for classification/regression tasks)."""
    
    cache_dir: Optional[str] = None
    """Where to store downloaded datasets."""
