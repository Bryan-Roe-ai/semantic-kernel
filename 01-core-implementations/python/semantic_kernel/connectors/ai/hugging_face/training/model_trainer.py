# Copyright (c) Microsoft. All rights reserved.

import logging
import os
from typing import Any, Callable, Dict, List, Optional, Tuple, Union, cast

import numpy as np
import torch
import transformers
from datasets import Dataset, DatasetDict
from peft import (
    LoraConfig,
    TaskType,
    get_peft_model,
    prepare_model_for_kbit_training,
)
from transformers import (
    AutoConfig,
    AutoModelForCausalLM,
    AutoModelForMaskedLM,
    AutoModelForQuestionAnswering,
    AutoModelForSequenceClassification,
    AutoTokenizer,
    DataCollatorForLanguageModeling,
    EarlyStoppingCallback,
    PreTrainedModel,
    PreTrainedTokenizer,
    Trainer,
    TrainingArguments,
)

from semantic_kernel.connectors.ai.hugging_face.training.dataset_processor import DatasetProcessor
from semantic_kernel.connectors.ai.hugging_face.training.training_config import (
    DatasetConfig,
    ModelTrainingConfig,
    TrainingArgumentsConfig,
)

logger = logging.getLogger(__name__)


class ModelTrainer:
    """Class for fine-tuning language models using the Hugging Face Transformers library."""

    def __init__(
        self,
        model_config: ModelTrainingConfig,
        training_args_config: TrainingArgumentsConfig,
        dataset_config: DatasetConfig,
    ):
        """
        Initialize the ModelTrainer.
        
        Args:
            model_config: Configuration for the model to be fine-tuned.
            training_args_config: Configuration for the training process.
            dataset_config: Configuration for the dataset.
        """
        self.model_config = model_config
        self.training_args_config = training_args_config
        self.dataset_config = dataset_config
        
        # These will be set during setup
        self.model = None
        self.tokenizer = None
        self.training_args = None
        self.trainer = None
        self.metrics = {}

    def setup(self) -> None:
        """
        Set up the model, tokenizer, and training arguments.
        
        This method prepares everything needed for training but does not start the training process.
        """
        logger.info(f"Setting up model: {self.model_config.model_name_or_path}")
        
        # Set up tokenizer
        tokenizer_name = self.model_config.tokenizer_name_or_path or self.model_config.model_name_or_path
        self.tokenizer = AutoTokenizer.from_pretrained(
            tokenizer_name,
            use_fast=True,
        )
        
        # Set up model
        model_name = self.model_config.model_name_or_path
        
        # Determine if task is classification (having a label column)
        is_classification = self.dataset_config.label_column is not None
        
        if is_classification:
            # Load labeled dataset to determine number of labels
            dataset = DatasetProcessor.load_dataset(self.dataset_config)
            
            # Get unique labels to determine num_labels
            if isinstance(dataset, DatasetDict) and "train" in dataset:
                labels = set(dataset["train"][self.dataset_config.label_column])
            else:
                labels = set(dataset[self.dataset_config.label_column])
            
            num_labels = len(labels)
            logger.info(f"Classification task detected with {num_labels} unique labels")
            
            # Initialize sequence classification model
            self.model = AutoModelForSequenceClassification.from_pretrained(
                model_name,
                num_labels=num_labels
            )
        else:
            # Initialize language model
            # Try to detect model type automatically
            try:
                config = AutoConfig.from_pretrained(model_name)
                model_type = getattr(config, "model_type", "")
                
                if model_type in ["bert", "roberta", "albert"]:
                    logger.info(f"Loading masked language model for {model_type}")
                    self.model = AutoModelForMaskedLM.from_pretrained(model_name)
                else:
                    logger.info(f"Loading causal language model for {model_type}")
                    self.model = AutoModelForCausalLM.from_pretrained(model_name)
            except Exception as e:
                logger.warning(f"Error in automatic model type detection: {str(e)}. Falling back to causal LM.")
                self.model = AutoModelForCausalLM.from_pretrained(model_name)
        
        # Apply LoRA if enabled
        if self.model_config.use_lora:
            if not self.model_config.lora_config:
                logger.info("LoRA enabled but no config provided. Using default LoRA configuration.")
                self.model_config.lora_config = {
                    "r": 16,
                    "lora_alpha": 32,
                    "lora_dropout": 0.05,
                    "bias": "none",
                    "task_type": "CAUSAL_LM",
                }
            
            # Prepare model for k-bit training if needed
            if hasattr(self.model, "is_quantized") and self.model.is_quantized:
                self.model = prepare_model_for_kbit_training(self.model)
            
            # Apply LoRA config
            lora_config = LoraConfig(
                r=self.model_config.lora_config.get("r", 16),
                lora_alpha=self.model_config.lora_config.get("lora_alpha", 32),
                lora_dropout=self.model_config.lora_config.get("lora_dropout", 0.05),
                bias=self.model_config.lora_config.get("bias", "none"),
                task_type=TaskType.CAUSAL_LM,
                target_modules=self.model_config.lora_config.get("target_modules", None),
            )
            
            logger.info(f"Applying LoRA to model with config: {lora_config}")
            self.model = get_peft_model(self.model, lora_config)
        
        # Set up training arguments
        self.training_args = TrainingArguments(**self.training_args_config.to_dict())
        
        logger.info("Model and tokenizer setup complete")

    def train(
        self, 
        dataset: Optional[Union[Dataset, DatasetDict]] = None,
        compute_metrics: Optional[Callable] = None,
        data_collator: Optional[Callable] = None,
    ) -> Dict[str, float]:
        """
        Train the model.
        
        Args:
            dataset: Optional pre-loaded dataset. If not provided, will load based on dataset_config.
            compute_metrics: Optional function to compute metrics during training.
            data_collator: Optional data collator to use for training.
            
        Returns:
            Dict[str, float]: The training metrics.
        """
        if self.model is None or self.tokenizer is None:
            self.setup()
        
        # Load dataset if not provided
        if dataset is None:
            dataset = DatasetProcessor.load_dataset(self.dataset_config)
        
        # Prepare dataset for training
        is_mlm = isinstance(self.model, transformers.PreTrainedModel) and self.model.config.model_type in ["bert", "roberta", "albert"]
        processed_dataset = DatasetProcessor.prepare_dataset_for_training(
            dataset=dataset,
            tokenizer=self.tokenizer,
            config=self.dataset_config,
            max_seq_length=self.model_config.max_seq_length,
            is_mlm=is_mlm,
        )
        
        # Setup data collator if not provided
        if data_collator is None and not self.dataset_config.label_column:
            # For language modeling tasks
            data_collator = DataCollatorForLanguageModeling(
                tokenizer=self.tokenizer,
                mlm=is_mlm,  # Use MLM loss for BERT/RoBERTa models
                mlm_probability=0.15 if is_mlm else 0.0,
            )
        
        # Initialize Trainer
        callbacks = []
        if self.training_args.load_best_model_at_end:
            callbacks.append(EarlyStoppingCallback(early_stopping_patience=3))
        
        self.trainer = Trainer(
            model=self.model,
            args=self.training_args,
            train_dataset=processed_dataset["train"] if isinstance(processed_dataset, DatasetDict) else processed_dataset,
            eval_dataset=processed_dataset.get("validation", None) if isinstance(processed_dataset, DatasetDict) else None,
            tokenizer=self.tokenizer,
            data_collator=data_collator,
            compute_metrics=compute_metrics,
            callbacks=callbacks,
        )
        
        # Start training
        logger.info("Starting training")
        train_result = self.trainer.train()
        self.metrics = train_result.metrics
        
        # Log and save metrics
        logger.info(f"Training metrics: {self.metrics}")
        self.trainer.save_metrics("train", self.metrics)
        
        # Save model and tokenizer
        self.trainer.save_model()
        self.tokenizer.save_pretrained(self.training_args.output_dir)
        
        # Run evaluation if validation set exists
        if isinstance(processed_dataset, DatasetDict) and "validation" in processed_dataset:
            eval_metrics = self.evaluate(processed_dataset["validation"])
            self.metrics.update(eval_metrics)
        
        # Push to hub if configured
        if self.training_args.push_to_hub:
            self.trainer.push_to_hub()
        
        return self.metrics
    
    def evaluate(self, eval_dataset: Optional[Dataset] = None) -> Dict[str, float]:
        """
        Evaluate the model on a dataset.
        
        Args:
            eval_dataset: Dataset to evaluate on. If not provided, will use the validation set.
            
        Returns:
            Dict[str, float]: The evaluation metrics.
        """
        if self.trainer is None:
            raise RuntimeError("Trainer not initialized. Call train() first or setup() followed by setting up trainer manually.")
        
        if eval_dataset is None and isinstance(self.trainer.eval_dataset, Dataset):
            eval_dataset = self.trainer.eval_dataset
        
        if eval_dataset is None:
            raise ValueError("No evaluation dataset provided and no validation set available in trainer.")
        
        logger.info("Starting evaluation")
        eval_metrics = self.trainer.evaluate(eval_dataset=eval_dataset)
        
        logger.info(f"Evaluation metrics: {eval_metrics}")
        self.trainer.save_metrics("eval", eval_metrics)
        
        return eval_metrics
    
    def save(self, output_dir: Optional[str] = None) -> None:
        """
        Save the model and tokenizer.
        
        Args:
            output_dir: Directory to save to. If not provided, will use the training arguments output_dir.
        """
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("Model and tokenizer not initialized. Call setup() first.")
        
        save_dir = output_dir or self.training_args.output_dir
        
        logger.info(f"Saving model and tokenizer to {save_dir}")
        self.model.save_pretrained(save_dir)
        self.tokenizer.save_pretrained(save_dir)
