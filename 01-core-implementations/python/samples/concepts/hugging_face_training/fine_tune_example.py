#!/usr/bin/env python3
"""
Fine Tune Example module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

import os
from typing import List, Optional

import transformers
from datasets import load_dataset

from semantic_kernel.connectors.ai.hugging_face.training import (
    DatasetConfig,
    HuggingFaceModelTrainer,
    ModelTrainingConfig,
    TrainingArgumentsConfig,
)


def fine_tune_model_from_huggingface_dataset() -> None:
    """Fine-tune a language model using a dataset from the Hugging Face Hub."""
    
    # Create configuration objects
    model_config = ModelTrainingConfig(
        model_name_or_path="distilbert-base-uncased",
        max_seq_length=128,
    )
    
    training_args = TrainingArgumentsConfig(
        output_dir="./output/fine-tuned-model",
        num_train_epochs=3,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        learning_rate=2e-5,
        weight_decay=0.01,
        logging_steps=100,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
    )
    
    dataset_config = DatasetConfig(
        huggingface_dataset_name="imdb",
        text_column="text",
        label_column="label",
    )
    
    # Create trainer and train model
    trainer = HuggingFaceModelTrainer(
        model_config=model_config,
        training_args_config=training_args,
        dataset_config=dataset_config,
    )
    
    print("Starting model fine-tuning...")
    metrics = trainer.train()
    print(f"Training complete with metrics: {metrics}")
    
    # Evaluate the model
    eval_metrics = trainer.evaluate()
    print(f"Evaluation metrics: {eval_metrics}")
    
    # Save the model
    trainer.save_model()
    print(f"Model saved to: {training_args.output_dir}")


def fine_tune_model_with_custom_text() -> None:
    """Fine-tune a language model with custom text data."""
    
    # Sample text data for fine-tuning
    texts = [
        "Semantic Kernel is a lightweight SDK that integrates Large Language Models (LLMs) with conventional programming languages.",
        "Semantic Kernel combines the best of both worlds: the augmented intelligence of Large Language Models (LLMs) and the solid, well-understood guarantees of traditional programming languages.",
        "The Semantic Kernel is an open-source SDK that allows you to easily combine AI services like OpenAI, Azure OpenAI, and Hugging Face with conventional programming languages like C#, Python, and Java.",
        "With Semantic Kernel, developers can create AI apps that combine the best of both paradigms: the flexibility and augmented intelligence of Large Language Models (LLMs) together with the guarantees and control of traditional programming.",
        "Semantic Kernel is designed to support and encapsulate several design patterns derived from production use cases.",
    ]
    
    # Create trainer with simplified interface
    trainer = HuggingFaceModelTrainer.from_pretrained_model(
        model_name_or_path="distilroberta-base",
        output_dir="./output/custom-model",
        num_train_epochs=5,
        learning_rate=3e-5,
        use_lora=True,  # Use parameter-efficient fine-tuning
    )
    
    print("Starting custom text fine-tuning...")
    metrics = trainer.create_fine_tuned_model(texts=texts)
    print(f"Training complete with metrics: {metrics}")
    
    # Save the model
    trainer.save_model()
    print("Model saved to: ./output/custom-model")


def fine_tune_classification_model(train_file_path: Optional[str] = None, validation_file_path: Optional[str] = None) -> None:
    """
    Fine-tune a classification model.
    
    Args:
        train_file_path: Path to training data CSV/JSON file with 'text' and 'label' columns
        validation_file_path: Path to validation data CSV/JSON file with 'text' and 'label' columns
    """
    # Create configuration objects
    model_config = ModelTrainingConfig(
        model_name_or_path="distilbert-base-uncased",
        max_seq_length=128,
    )
    
    training_args = TrainingArgumentsConfig(
        output_dir="./output/classifier-model",
        num_train_epochs=3,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        learning_rate=2e-5,
        weight_decay=0.01,
        logging_steps=100,
        evaluation_strategy="epoch" if validation_file_path else "no",
        save_strategy="epoch",
        load_best_model_at_end=True if validation_file_path else False,
    )
    
    dataset_config = DatasetConfig(
        # If file paths are provided, use them; otherwise use a HuggingFace dataset
        train_file_path=train_file_path,
        validation_file_path=validation_file_path,
        huggingface_dataset_name=None if train_file_path else "tweet_eval",
        huggingface_dataset_config_name=None if train_file_path else "sentiment",
        text_column="text",
        label_column="label",
    )
    
    # Create trainer and train model
    trainer = HuggingFaceModelTrainer(
        model_config=model_config,
        training_args_config=training_args,
        dataset_config=dataset_config,
    )
    
    print("Starting classification model fine-tuning...")
    metrics = trainer.train()
    print(f"Training complete with metrics: {metrics}")
    
    # Evaluate the model
    if validation_file_path or (not train_file_path and "test" in load_dataset("tweet_eval", "sentiment")):
        eval_metrics = trainer.evaluate()
        print(f"Evaluation metrics: {eval_metrics}")
    
    # Save the model
    trainer.save_model()
    print(f"Model saved to: {training_args.output_dir}")


if __name__ == "__main__":
    # Choose one of the examples to run
    fine_tune_model_from_huggingface_dataset()
    # fine_tune_model_with_custom_text()
    # fine_tune_classification_model()
