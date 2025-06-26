#!/usr/bin/env python3
"""
import re
AI module for advanced llm trainer

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

import os
import json
import logging
import torch
import torch.nn as nn
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, field
from pathlib import Path
import numpy as np
from datetime import datetime

# Hugging Face imports
from transformers import (
    AutoTokenizer, AutoModelForCausalLM, AutoModelForSequenceClassification,
    Trainer, TrainingArguments, DataCollatorForLanguageModeling,
    GPT2LMHeadModel, GPT2Config, GPT2Tokenizer,
    EarlyStoppingCallback, get_linear_schedule_with_warmup
)
from datasets import Dataset, load_dataset
import wandb
from peft import LoraConfig, get_peft_model, TaskType, prepare_model_for_kbit_training
import bitsandbytes as bnb

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ModelConfig:
    """Configuration for model architecture and training."""
    model_name: str = "gpt2"
    model_type: str = "causal_lm"  # causal_lm, classification, custom
    vocab_size: int = 50257
    n_positions: int = 1024
    n_ctx: int = 1024
    n_embd: int = 768
    n_layer: int = 12
    n_head: int = 12
    use_cache: bool = True

    # Training specific
    max_length: int = 512
    learning_rate: float = 5e-5
    num_epochs: int = 3
    batch_size: int = 4
    gradient_accumulation_steps: int = 4
    warmup_steps: int = 500
    weight_decay: float = 0.01

    # LoRA configuration
    use_lora: bool = True
    lora_r: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.1

    # Quantization
    use_4bit: bool = True
    use_8bit: bool = False

@dataclass
class DataConfig:
    """Configuration for data processing and loading."""
    data_path: str = "training_data"
    train_file: str = "train.jsonl"
    eval_file: str = "eval.jsonl"
    test_file: str = "test.jsonl"
    text_column: str = "text"
    label_column: str = "label"
    max_samples: Optional[int] = None
    validation_split: float = 0.1
    preprocessing_num_workers: int = 4

class CustomDataProcessor:
    """Advanced data processing for LLM training."""

    def __init__(self, config: DataConfig, tokenizer):
        self.config = config
        self.tokenizer = tokenizer

    def load_and_process_data(self) -> Tuple[Dataset, Dataset]:
        """Load and process training data from various sources."""
        data_path = Path(self.config.data_path)

        if not data_path.exists():
            logger.warning(f"Data path {data_path} not found. Creating sample data.")
            self._create_sample_data(data_path)

        # Load datasets
        train_data = self._load_jsonl(data_path / self.config.train_file)
        eval_data = self._load_jsonl(data_path / self.config.eval_file)

        if not eval_data and train_data:
            # Split training data for validation
            split_idx = int(len(train_data) * (1 - self.config.validation_split))
            eval_data = train_data[split_idx:]
            train_data = train_data[:split_idx]

        # Convert to HuggingFace datasets
        train_dataset = Dataset.from_list(train_data)
        eval_dataset = Dataset.from_list(eval_data) if eval_data else None

        # Tokenize datasets
        train_dataset = self._tokenize_dataset(train_dataset)
        eval_dataset = self._tokenize_dataset(eval_dataset) if eval_dataset else None

        return train_dataset, eval_dataset

    def _load_jsonl(self, file_path: Path) -> List[Dict]:
        """Load data from JSONL file."""
        if not file_path.exists():
            return []

        data = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    continue

        if self.config.max_samples:
            data = data[:self.config.max_samples]

        return data

    def _create_sample_data(self, data_path: Path):
        """Create sample training data if none exists."""
        data_path.mkdir(parents=True, exist_ok=True)

        sample_data = [
            {"text": "This is a sample training text for the language model."},
            {"text": "AI and machine learning are transforming technology."},
            {"text": "Natural language processing enables computers to understand human language."},
            {"text": "Deep learning models can generate human-like text."},
            {"text": "Transformer architectures have revolutionized NLP tasks."},
        ]

        # Create training file
        with open(data_path / self.config.train_file, 'w', encoding='utf-8') as f:
            for item in sample_data:
                f.write(json.dumps(item) + '\n')

        logger.info(f"Created sample data at {data_path}")

    def _tokenize_dataset(self, dataset: Dataset) -> Dataset:
        """Tokenize the dataset."""
        def tokenize_function(examples):
            return self.tokenizer(
                examples[self.config.text_column],
                truncation=True,
                padding=True,
                max_length=self.config.max_samples or 512,
                return_tensors="pt"
            )

        return dataset.map(
            tokenize_function,
            batched=True,
            num_proc=self.config.preprocessing_num_workers,
            remove_columns=dataset.column_names
        )

class CustomLLMTrainer:
    """Advanced LLM trainer with multiple model architectures."""

    def __init__(self, model_config: ModelConfig, data_config: DataConfig):
        self.model_config = model_config
        self.data_config = data_config
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {self.device}")

        # Initialize tokenizer and model
        self.tokenizer = self._load_tokenizer()
        self.model = self._load_model()
        self.data_processor = CustomDataProcessor(data_config, self.tokenizer)

    def _load_tokenizer(self):
        """Load and configure tokenizer."""
        tokenizer = AutoTokenizer.from_pretrained(self.model_config.model_name)

        # Add special tokens if needed
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        return tokenizer

    def _load_model(self):
        """Load and configure model with optional quantization and LoRA."""
        # Configure quantization
        quantization_config = None
        if self.model_config.use_4bit:
            from transformers import BitsAndBytesConfig
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16
            )

        # Load base model
        if self.model_config.model_type == "causal_lm":
            model = AutoModelForCausalLM.from_pretrained(
                self.model_config.model_name,
                quantization_config=quantization_config,
                device_map="auto",
                trust_remote_code=True
            )
        elif self.model_config.model_type == "classification":
            model = AutoModelForSequenceClassification.from_pretrained(
                self.model_config.model_name,
                quantization_config=quantization_config,
                device_map="auto"
            )
        else:
            # Custom model
            model = self._create_custom_model()

        # Apply LoRA if specified
        if self.model_config.use_lora:
            model = self._apply_lora(model)

        return model

    def _create_custom_model(self):
        """Create a custom model architecture."""
        config = GPT2Config(
            vocab_size=self.model_config.vocab_size,
            n_positions=self.model_config.n_positions,
            n_embd=self.model_config.n_embd,
            n_layer=self.model_config.n_layer,
            n_head=self.model_config.n_head,
            use_cache=self.model_config.use_cache
        )

        model = GPT2LMHeadModel(config)
        logger.info("Created custom GPT-2 model")
        return model

    def _apply_lora(self, model):
        """Apply LoRA (Low-Rank Adaptation) to the model."""
        if self.model_config.use_4bit:
            model = prepare_model_for_kbit_training(model)

        lora_config = LoraConfig(
            task_type=TaskType.CAUSAL_LM,
            r=self.model_config.lora_r,
            lora_alpha=self.model_config.lora_alpha,
            lora_dropout=self.model_config.lora_dropout,
            target_modules=["c_attn", "c_proj", "c_fc"]  # GPT-2 specific
        )

        model = get_peft_model(model, lora_config)
        model.print_trainable_parameters()

        return model

    def train(self, output_dir: str = "custom_llm_output", use_wandb: bool = False):
        """Train the model with advanced configuration."""
        # Load and process data
        train_dataset, eval_dataset = self.data_processor.load_and_process_data()

        # Initialize wandb if specified
        if use_wandb:
            wandb.init(
                project="custom-llm-training",
                config=self.model_config.__dict__
            )

        # Data collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False,
            return_tensors="pt"
        )

        # Training arguments
        training_args = TrainingArguments(
            output_dir=output_dir,
            overwrite_output_dir=True,
            num_train_epochs=self.model_config.num_epochs,
            per_device_train_batch_size=self.model_config.batch_size,
            per_device_eval_batch_size=self.model_config.batch_size,
            gradient_accumulation_steps=self.model_config.gradient_accumulation_steps,
            learning_rate=self.model_config.learning_rate,
            weight_decay=self.model_config.weight_decay,
            warmup_steps=self.model_config.warmup_steps,
            logging_steps=100,
            eval_steps=500,
            save_steps=500,
            save_total_limit=3,
            evaluation_strategy="steps" if eval_dataset else "no",
            load_best_model_at_end=True if eval_dataset else False,
            metric_for_best_model="eval_loss",
            greater_is_better=False,
            report_to="wandb" if use_wandb else None,
            fp16=torch.cuda.is_available(),
            dataloader_pin_memory=False,
            remove_unused_columns=False,
        )

        # Callbacks
        callbacks = []
        if eval_dataset:
            callbacks.append(EarlyStoppingCallback(early_stopping_patience=3))

        # Initialize trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            data_collator=data_collator,
            callbacks=callbacks,
        )

        # Start training
        logger.info("Starting training...")
        trainer.train()

        # Save the final model
        trainer.save_model(output_dir)
        self.tokenizer.save_pretrained(output_dir)

        # Save training metrics
        if trainer.state.log_history:
            with open(f"{output_dir}/training_metrics.json", "w") as f:
                json.dump(trainer.state.log_history, f, indent=2)

        logger.info(f"Training completed. Model saved to {output_dir}")

        if use_wandb:
            wandb.finish()

        return trainer

    def generate_text(self, prompt: str, max_length: int = 100,
                     temperature: float = 0.7, top_p: float = 0.9) -> str:
        """Generate text using the trained model."""
        self.model.eval()

        inputs = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_length=max_length,
                temperature=temperature,
                top_p=top_p,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )

        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return generated_text[len(prompt):]

class ModelEvaluator:
    """Evaluate trained models with various metrics."""

    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer
        self.device = next(model.parameters()).device

    def calculate_perplexity(self, text_data: List[str]) -> float:
        """Calculate perplexity on a dataset."""
        self.model.eval()
        total_loss = 0
        total_tokens = 0

        with torch.no_grad():
            for text in text_data:
                inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
                inputs = {k: v.to(self.device) for k, v in inputs.items()}

                outputs = self.model(**inputs, labels=inputs["input_ids"])
                loss = outputs.loss

                total_loss += loss.item() * inputs["input_ids"].size(1)
                total_tokens += inputs["input_ids"].size(1)

        avg_loss = total_loss / total_tokens
        perplexity = torch.exp(torch.tensor(avg_loss))
        return perplexity.item()

    def generate_samples(self, prompts: List[str], **generation_kwargs) -> List[str]:
        """Generate samples for qualitative evaluation."""
        self.model.eval()
        generated_texts = []

        for prompt in prompts:
            inputs = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)

            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=generation_kwargs.get("max_length", 100),
                    temperature=generation_kwargs.get("temperature", 0.7),
                    top_p=generation_kwargs.get("top_p", 0.9),
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )

            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            generated_texts.append(generated_text)

        return generated_texts

def main():
    """Main training function."""
    # Configuration
    model_config = ModelConfig(
        model_name="gpt2",
        num_epochs=3,
        batch_size=2,
        learning_rate=5e-5,
        use_lora=True,
        use_4bit=True
    )

    data_config = DataConfig(
        data_path="ai-workspace/07-data-resources/training_data",
        max_samples=1000
    )

    # Initialize trainer
    trainer = CustomLLMTrainer(model_config, data_config)

    # Train the model
    output_dir = "ai-workspace/models/custom_llm"
    trained_model = trainer.train(output_dir=output_dir, use_wandb=False)

    # Evaluate the model
    evaluator = ModelEvaluator(trainer.model, trainer.tokenizer)

    # Test generation
    test_prompts = [
        "The future of AI is",
        "In machine learning, the most important concept is",
        "Natural language processing helps"
    ]

    generated_texts = evaluator.generate_samples(test_prompts)

    print("\n=== Generated Samples ===")
    for prompt, generated in zip(test_prompts, generated_texts):
        print(f"Prompt: {prompt}")
        print(f"Generated: {generated}")
        print("-" * 50)

if __name__ == "__main__":
    main()
