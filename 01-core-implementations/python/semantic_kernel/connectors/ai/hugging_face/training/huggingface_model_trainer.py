#!/usr/bin/env python3
"""
AI module for huggingface model trainer

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union, cast

import transformers
from datasets import Dataset, DatasetDict

from semantic_kernel.connectors.ai.hugging_face.training.dataset_processor import DatasetProcessor
from semantic_kernel.connectors.ai.hugging_face.training.model_trainer import ModelTrainer
from semantic_kernel.connectors.ai.hugging_face.training.training_config import (
    DatasetConfig,
    ModelTrainingConfig,
    TrainingArgumentsConfig,
)
from semantic_kernel.connectors.ai.hugging_face.training.training_evaluator import TrainingEvaluator
from semantic_kernel.kernel_pydantic import KernelBaseModel


class HuggingFaceModelTrainer:
    """
    Semantic Kernel integration for Hugging Face model training and fine-tuning.

    This class provides a simplified interface for training and fine-tuning language models
    using the Hugging Face transformers library, integrated with Semantic Kernel.
    """

    def __init__(
        self,
        model_config: ModelTrainingConfig,
        training_args_config: TrainingArgumentsConfig,
        dataset_config: DatasetConfig,
    ):
        """
        Initialize the HuggingFaceModelTrainer.

        Args:
            model_config: Configuration for the model to be fine-tuned.
            training_args_config: Configuration for the training process.
            dataset_config: Configuration for the dataset.
        """
        self.model_trainer = ModelTrainer(
            model_config=model_config,
            training_args_config=training_args_config,
            dataset_config=dataset_config,
        )
        self.dataset_config = dataset_config
        self.model_config = model_config
        self.training_evaluator = TrainingEvaluator()

    @classmethod
    def from_pretrained_model(
        cls,
        model_name_or_path: str,
        output_dir: str = "output",
        num_train_epochs: float = 3.0,
        learning_rate: float = 5e-5,
        use_lora: bool = False,
        train_file_path: Optional[str] = None,
        validation_file_path: Optional[str] = None,
        huggingface_dataset_name: Optional[str] = None,
        push_to_hub: bool = False,
        hub_model_id: Optional[str] = None,
    ) -> "HuggingFaceModelTrainer":
        """
        Create a trainer from a pre-trained model with simplified configuration.

        Args:
            model_name_or_path: Name or path of the model to fine-tune.
            output_dir: Directory where trained model will be saved.
            num_train_epochs: Number of training epochs.
            learning_rate: Learning rate for training.
            use_lora: Whether to use LoRA for parameter-efficient fine-tuning.
            train_file_path: Path to the training data file.
            validation_file_path: Path to the validation data file.
            huggingface_dataset_name: Name of a Hugging Face dataset to use.
            push_to_hub: Whether to push the trained model to the Hub.
            hub_model_id: Model ID for the Hub if pushing to Hub.

        Returns:
            An initialized HuggingFaceModelTrainer.
        """
        # Create model configuration
        model_config = ModelTrainingConfig(
            model_name_or_path=model_name_or_path,
            use_lora=use_lora,
            lora_config={"r": 16, "lora_alpha": 32, "lora_dropout": 0.05} if use_lora else None,
        )

        # Create training arguments configuration
        training_args_config = TrainingArgumentsConfig(
            output_dir=output_dir,
            num_train_epochs=num_train_epochs,
            learning_rate=learning_rate,
            push_to_hub=push_to_hub,
            hub_model_id=hub_model_id,
            save_strategy="epoch",
            evaluation_strategy="epoch" if validation_file_path else "no",
            load_best_model_at_end=True if validation_file_path else False,
        )

        # Create dataset configuration
        dataset_config = DatasetConfig(
            train_file_path=train_file_path,
            validation_file_path=validation_file_path,
            huggingface_dataset_name=huggingface_dataset_name,
        )

        return cls(model_config, training_args_config, dataset_config)

    def train(self) -> Dict[str, float]:
        """
        Train the model using the provided configuration.

        Returns:
            Dict[str, float]: The training metrics.
        """
        # Determine if the task is classification or not
        task_type = "classification" if self.dataset_config.label_column else "language_modeling"

        # Get appropriate metrics function if classification task
        compute_metrics = None
        if task_type == "classification":
            compute_metrics = TrainingEvaluator.get_compute_metrics_function("classification")

        # Setup model and train
        self.model_trainer.setup()
        metrics = self.model_trainer.train(compute_metrics=compute_metrics)

        return metrics

    def evaluate(self, eval_dataset: Optional[Dataset] = None) -> Dict[str, float]:
        """
        Evaluate the trained model.

        Args:
            eval_dataset: Dataset to evaluate on. If not provided, will use validation set if available.

        Returns:
            Dict[str, float]: The evaluation metrics.
        """
        # Load evaluation dataset if not provided
        if eval_dataset is None and self.dataset_config.validation_file_path:
            dataset = DatasetProcessor.load_dataset(self.dataset_config)
            if isinstance(dataset, DatasetDict) and "validation" in dataset:
                eval_dataset = dataset["validation"]

        if eval_dataset is None:
            raise ValueError("No evaluation dataset provided and no validation set available in config.")

        metrics = self.model_trainer.evaluate(eval_dataset)
        return metrics

    def evaluate_generation_quality(
        self,
        prompt_column: str = "prompt",
        reference_column: str = "completion",
        dataset: Optional[Dataset] = None,
    ) -> Dict[str, float]:
        """
        Evaluate the text generation quality of the model.

        Args:
            prompt_column: Column name containing prompts in the dataset.
            reference_column: Column name containing reference completions.
            dataset: Dataset to evaluate on. If not provided, will use validation set if available.

        Returns:
            Dict[str, float]: The generation quality metrics.
        """
        # Ensure model and tokenizer are set up
        if self.model_trainer.model is None or self.model_trainer.tokenizer is None:
            self.model_trainer.setup()

        # Load evaluation dataset if not provided
        if dataset is None and self.dataset_config.validation_file_path:
            loaded_dataset = DatasetProcessor.load_dataset(self.dataset_config)
            if isinstance(loaded_dataset, DatasetDict) and "validation" in loaded_dataset:
                dataset = loaded_dataset["validation"]
            else:
                dataset = loaded_dataset

        if dataset is None:
            raise ValueError("No dataset provided and no validation set available in config.")

        metrics = TrainingEvaluator.evaluate_generation_quality(
            model=self.model_trainer.model,
            dataset=dataset,
            tokenizer=self.model_trainer.tokenizer,
            prompt_column=prompt_column,
            reference_column=reference_column,
        )

        return metrics

    def save_model(self, output_dir: Optional[str] = None) -> None:
        """
        Save the trained model.

        Args:
            output_dir: Directory to save the model to. If not provided, will use the output dir from training args.
        """
        self.model_trainer.save(output_dir)

    def create_fine_tuned_model(self, texts: List[str], labels: Optional[List[Union[str, int]]] = None) -> Dict[str, float]:
        """
        Create and train a model from a list of texts and optional labels.

        This is a convenience method that handles dataset creation and training in one step.

        Args:
            texts: List of texts to train on.
            labels: Optional list of labels for classification tasks.

        Returns:
            Dict[str, float]: The training metrics.
        """
        # Create dataset
        dataset = DatasetProcessor.create_dataset_from_text(texts, labels)

        # Setup the trainer
        self.model_trainer.setup()

        # Determine if task is classification
        task_type = "classification" if labels is not None else "language_modeling"
        compute_metrics = TrainingEvaluator.get_compute_metrics_function(task_type) if task_type == "classification" else None

        # Train the model
        metrics = self.model_trainer.train(dataset=dataset, compute_metrics=compute_metrics)

        return metrics
