# Hugging Face Model Training with Semantic Kernel

This directory contains examples for training and fine-tuning language models using the Hugging Face training integration with Semantic Kernel.

## Overview

The Semantic Kernel Hugging Face training module allows you to:

1. Fine-tune existing Hugging Face models for specific tasks
2. Train models using custom text data
3. Create classification models
4. Integrate trained models back into the Semantic Kernel framework

## Prerequisites

```bash
pip install semantic-kernel transformers datasets torch rouge_score nltk
```

For optimal performance with GPU acceleration, install PyTorch with CUDA support.

## Examples

### Basic model fine-tuning

`fine_tune_example.py` demonstrates different ways to fine-tune language models:

- Fine-tuning using a dataset from the Hugging Face Hub
- Fine-tuning with custom text data
- Training classification models

Run the example:

```bash
python fine_tune_example.py
```

### Integration with Semantic Kernel

`sk_integration_example.py` demonstrates how to:

1. Train/fine-tune a model
2. Use the trained model as a text completion service within Semantic Kernel
3. Create a custom sentiment classifier and use it as a Semantic Kernel function

Run the example:

```bash
python sk_integration_example.py
```

## Training Configuration Options

The training module supports several configuration options:

### Model Configuration

```python
model_config = ModelTrainingConfig(
    model_name_or_path="distilbert-base-uncased",  # Model to fine-tune
    max_seq_length=128,                            # Max sequence length for tokenizer
    use_lora=True,                                # Whether to use LoRA for parameter-efficient fine-tuning
    lora_config={                                 # LoRA configuration parameters
        "r": 16,
        "lora_alpha": 32,
        "lora_dropout": 0.05,
    }
)
```

### Training Arguments

```python
training_args = TrainingArgumentsConfig(
    output_dir="./output/fine-tuned-model",      # Directory to save model
    num_train_epochs=3,                         # Number of training epochs
    per_device_train_batch_size=16,             # Batch size per device for training
    learning_rate=2e-5,                         # Learning rate
    weight_decay=0.01,                          # Weight decay for regularization
    evaluation_strategy="epoch",                # When to run evaluation
    save_strategy="epoch",                      # When to save checkpoints
    load_best_model_at_end=True,                # Whether to load best model at end
    push_to_hub=False,                          # Whether to upload model to Hub
)
```

### Dataset Configuration

```python
dataset_config = DatasetConfig(
    train_file_path="data/train.csv",           # Path to training data file
    validation_file_path="data/validation.csv", # Path to validation data file
    huggingface_dataset_name="imdb",            # Alternative: HF dataset name
    text_column="text",                         # Column name for input text
    label_column="label",                       # Column name for labels
)
```

## Training API

The simplified API allows you to create a trainer with minimal configuration:

```python
trainer = HuggingFaceModelTrainer.from_pretrained_model(
    model_name_or_path="distilroberta-base",
    output_dir="./output/custom-model",
    num_train_epochs=5,
    learning_rate=3e-5,
    use_lora=True,
)

# Train with custom texts
metrics = trainer.create_fine_tuned_model(texts=my_texts)
```

## Example Use Cases

1. **Custom chatbot training**: Fine-tune a model on your specific domain data
2. **Sentiment analysis**: Train a classifier for sentiment analysis of user reviews
3. **Document classification**: Train a model to categorize documents or support tickets
4. **Text generation**: Fine-tune a model to generate text in a specific style or domain

For more information, see the [Hugging Face Transformers documentation](https://huggingface.co/docs/transformers/index) and the [Semantic Kernel documentation](https://learn.microsoft.com/semantic-kernel/).


---

## 👨‍💻 Author & Attribution

**Created by Bryan Roe**  
Copyright (c) 2025 Bryan Roe  
Licensed under the MIT License

This is part of the Semantic Kernel - Advanced AI Development Framework.
For more information, see the main project repository.
