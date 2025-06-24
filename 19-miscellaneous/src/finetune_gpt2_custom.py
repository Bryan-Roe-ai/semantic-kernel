#!/usr/bin/env python3
"""
Finetune Gpt2 Custom module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Fine-tune GPT-2 on your custom data using Hugging Face Transformers and GPU
# Make sure you have 'transformers', 'torch', and 'datasets' installed
# Run: pip install transformers torch datasets

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    Trainer,
    TrainingArguments,
    TextDataset,
    DataCollatorForLanguageModeling,
)
import torch
import os

# Check for GPU
print("CUDA available:", torch.cuda.is_available())

data_path = "llm_training_data.txt"
model_name = "gpt2"
output_dir = "fine_tuned_gpt2"

# Load tokenizer and model
print("Loading model and tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Prepare dataset
print("Preparing dataset...")


def load_dataset(file_path, tokenizer, block_size=512):
    return TextDataset(tokenizer=tokenizer, file_path=file_path, block_size=block_size)


dataset = load_dataset(data_path, tokenizer)
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False,
)

# Training arguments
training_args = TrainingArguments(
    output_dir=output_dir,
    overwrite_output_dir=True,
    num_train_epochs=1,  # Increase for better results
    per_device_train_batch_size=1,  # Increase if you have more GPU memory
    save_steps=500,
    save_total_limit=2,
    prediction_loss_only=True,
    fp16=torch.cuda.is_available(),
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=dataset,
)

# Train
print("Starting training...")
trainer.train()

# Save model
print(f"Saving model to {output_dir} ...")
trainer.save_model(output_dir)
print("Done!")
