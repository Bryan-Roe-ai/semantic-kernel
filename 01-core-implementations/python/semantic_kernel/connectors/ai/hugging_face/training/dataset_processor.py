#!/usr/bin/env python3
"""
import re
Dataset Processor module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Copyright (c) Microsoft. All rights reserved.

import logging
import os
from typing import Any, Dict, List, Optional, Tuple, Union, cast

import datasets
import pandas as pd
from datasets import Dataset, DatasetDict

from semantic_kernel.connectors.ai.hugging_face.training.training_config import DatasetConfig

logger = logging.getLogger(__name__)


class DatasetProcessor:
    """Class for processing datasets for language model fine-tuning."""

    @staticmethod
    def load_dataset(config: DatasetConfig) -> Union[Dataset, DatasetDict]:
        """
        Load a dataset from local files or from the Hugging Face Hub.

        Args:
            config: Configuration for the dataset.

        Returns:
            The loaded dataset.

        Raises:
            ValueError: If no valid data source is provided.
        """
        # Load from Hugging Face Hub if specified
        if config.huggingface_dataset_name:
            logger.info(f"Loading dataset '{config.huggingface_dataset_name}' from the Hugging Face Hub")
            return datasets.load_dataset(
                config.huggingface_dataset_name,
                config.huggingface_dataset_config_name,
                cache_dir=config.cache_dir,
            )

        # Load from local files
        data_files = {}

        if config.train_file_path:
            if not os.path.exists(config.train_file_path):
                raise ValueError(f"Training file not found at: {config.train_file_path}")
            data_files["train"] = config.train_file_path

        if config.validation_file_path:
            if not os.path.exists(config.validation_file_path):
                raise ValueError(f"Validation file not found at: {config.validation_file_path}")
            data_files["validation"] = config.validation_file_path

        if config.test_file_path:
            if not os.path.exists(config.test_file_path):
                raise ValueError(f"Test file not found at: {config.test_file_path}")
            data_files["test"] = config.test_file_path

        if not data_files:
            raise ValueError(
                "No valid data source provided. Either specify local file paths or a Hugging Face dataset name."
            )

        # Determine file extension for loading
        file_extension = os.path.splitext(next(iter(data_files.values())))[1].lower()

        if file_extension == ".csv":
            return datasets.load_dataset("csv", data_files=data_files, cache_dir=config.cache_dir)
        elif file_extension in [".json", ".jsonl"]:
            return datasets.load_dataset("json", data_files=data_files, cache_dir=config.cache_dir)
        else:
            raise ValueError(f"Unsupported file extension: {file_extension}. Supported types are: .csv, .json, .jsonl")

    @staticmethod
    def prepare_dataset_for_training(
        dataset: Union[Dataset, DatasetDict],
        tokenizer: Any,
        config: DatasetConfig,
        max_seq_length: int = 512,
        is_mlm: bool = False,
    ) -> Union[Dataset, DatasetDict]:
        """
        Prepare a dataset for training by tokenizing the text.

        Args:
            dataset: The dataset to prepare.
            tokenizer: The tokenizer to use.
            config: Configuration for the dataset.
            max_seq_length: Maximum sequence length for tokenization.
            is_mlm: Whether the task is masked language modeling.

        Returns:
            The prepared dataset.
        """
        column_names = dataset["train"].column_names if isinstance(dataset, DatasetDict) else dataset.column_names

        if config.text_column not in column_names:
            raise ValueError(
                f"Text column '{config.text_column}' not found in dataset. Available columns: {column_names}"
            )

        # Define tokenization function
        def tokenize_function(examples):
            # For masked language modeling (MLM)
            if is_mlm:
                return tokenizer(
                    examples[config.text_column],
                    padding="max_length",
                    truncation=True,
                    max_length=max_seq_length,
                    return_special_tokens_mask=True,
                )
            # For causal language modeling (CLM) or other tasks
            else:
                return tokenizer(
                    examples[config.text_column],
                    padding="max_length",
                    truncation=True,
                    max_length=max_seq_length,
                )

        # Apply tokenization
        tokenized_dataset = dataset.map(
            tokenize_function,
            batched=True,
            num_proc=os.cpu_count(),
            remove_columns=[col for col in column_names if col != config.label_column and col != config.text_column],
            desc="Tokenizing dataset",
        )

        # For classification tasks, process labels if required
        if config.label_column and config.label_column in column_names:
            # Check if labels are numeric or text
            sample = dataset["train"][0] if isinstance(dataset, DatasetDict) else dataset[0]
            label = sample[config.label_column]

            # If labels are text, convert them to IDs
            if isinstance(label, str):
                # Get unique labels
                if isinstance(dataset, DatasetDict):
                    labels = set()
                    for split in dataset.keys():
                        labels.update(dataset[split][config.label_column])
                    labels = sorted(list(labels))
                else:
                    labels = sorted(list(set(dataset[config.label_column])))

                # Create label mapping
                label_to_id = {label: i for i, label in enumerate(labels)}

                # Function to convert labels to IDs
                def convert_labels_to_ids(examples):
                    return {"labels": [label_to_id[label] for label in examples[config.label_column]]}

                # Apply conversion
                tokenized_dataset = tokenized_dataset.map(
                    convert_labels_to_ids,
                    batched=True,
                    desc="Converting text labels to IDs",
                )
            else:
                # Rename label column to "labels" for the trainer
                def rename_label_column(examples):
                    return {"labels": examples[config.label_column]}

                tokenized_dataset = tokenized_dataset.map(
                    rename_label_column,
                    batched=True,
                    desc="Renaming label column",
                )

        return tokenized_dataset

    @staticmethod
    def create_dataset_from_text(
        texts: List[str],
        labels: Optional[List[Union[int, str]]] = None,
        split_ratio: float = 0.1
    ) -> DatasetDict:
        """
        Create a dataset from a list of texts (and optionally labels).

        Args:
            texts: List of texts to include in the dataset.
            labels: Optional list of labels for classification tasks.
            split_ratio: Ratio of validation split.

        Returns:
            A dataset dictionary with train and validation splits.
        """
        if labels and len(texts) != len(labels):
            raise ValueError(f"Number of texts ({len(texts)}) must match number of labels ({len(labels)})")

        # Create DataFrame
        data = {"text": texts}
        if labels:
            data["label"] = labels

        df = pd.DataFrame(data)

        # Create Dataset
        dataset = Dataset.from_pandas(df)

        # Split dataset
        splits = dataset.train_test_split(test_size=split_ratio)
        dataset_dict = DatasetDict({
            "train": splits["train"],
            "validation": splits["test"]
        })

        return dataset_dict
