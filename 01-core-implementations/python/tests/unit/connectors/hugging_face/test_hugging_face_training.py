#!/usr/bin/env python3
"""
Test module for hugging face training

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
import tempfile
import unittest
from unittest.mock import MagicMock, patch

import pytest

from semantic_kernel.connectors.ai.hugging_face.training import (
    DatasetConfig,
    HuggingFaceModelTrainer,
    ModelTrainingConfig,
    TrainingArgumentsConfig,
)


class TestHuggingFaceTraining(unittest.TestCase):
    """Test the HuggingFace training functionality."""

    @patch("semantic_kernel.connectors.ai.hugging_face.training.model_trainer.AutoTokenizer")
    @patch("semantic_kernel.connectors.ai.hugging_face.training.model_trainer.AutoModelForCausalLM")
    @patch("semantic_kernel.connectors.ai.hugging_face.training.model_trainer.Trainer")
    def test_model_setup(self, mock_trainer, mock_auto_model, mock_tokenizer):
        """Test that the model and tokenizer are set up correctly."""
        # Arrange
        mock_tokenizer.from_pretrained.return_value = MagicMock()
        mock_auto_model.from_pretrained.return_value = MagicMock()
        mock_trainer.return_value = MagicMock()

        # Configure the mocked trainer instance
        mock_trainer_instance = mock_trainer.return_value
        mock_trainer_instance.train.return_value = MagicMock()
        mock_trainer_instance.train.return_value.metrics = {"loss": 1.0}

        with tempfile.TemporaryDirectory() as tmp_dir:
            model_config = ModelTrainingConfig(
                model_name_or_path="gpt2",
            )

            training_args = TrainingArgumentsConfig(
                output_dir=tmp_dir,
                num_train_epochs=1,
            )

            dataset_config = DatasetConfig(
                huggingface_dataset_name="imdb",
                text_column="text",
            )

            # Act
            trainer = HuggingFaceModelTrainer(
                model_config=model_config,
                training_args_config=training_args,
                dataset_config=dataset_config,
            )

            # Mock the DatasetProcessor.load_dataset method
            with patch("semantic_kernel.connectors.ai.hugging_face.training.dataset_processor.DatasetProcessor.load_dataset") as mock_load_dataset:
                mock_dataset = MagicMock()
                mock_load_dataset.return_value = mock_dataset

                # Mock the DatasetProcessor.prepare_dataset_for_training method
                with patch("semantic_kernel.connectors.ai.hugging_face.training.dataset_processor.DatasetProcessor.prepare_dataset_for_training") as mock_prepare_dataset:
                    mock_prepare_dataset.return_value = mock_dataset

                    # Call the train method
                    metrics = trainer.train()

            # Assert
            # Check that the model and tokenizer were set up correctly
            mock_tokenizer.from_pretrained.assert_called_once_with("gpt2", use_fast=True)
            mock_auto_model.from_pretrained.assert_called_once_with("gpt2")

            # Check that the trainer was created and train was called
            mock_trainer.assert_called_once()
            mock_trainer_instance.train.assert_called_once()

            # Check that we have metrics
            assert "loss" in metrics
            assert metrics["loss"] == 1.0

    @patch("semantic_kernel.connectors.ai.hugging_face.training.huggingface_model_trainer.ModelTrainer")
    def test_simplified_api(self, mock_model_trainer):
        """Test the simplified API for the HuggingFaceModelTrainer."""
        # Arrange
        mock_model_trainer_instance = MagicMock()
        mock_model_trainer.return_value = mock_model_trainer_instance
        mock_model_trainer_instance.train.return_value = {"loss": 2.0}

        # Mock the create_dataset_from_text method
        with patch("semantic_kernel.connectors.ai.hugging_face.training.dataset_processor.DatasetProcessor.create_dataset_from_text") as mock_create_dataset:
            mock_dataset = MagicMock()
            mock_create_dataset.return_value = mock_dataset

            # Act
            with tempfile.TemporaryDirectory() as tmp_dir:
                trainer = HuggingFaceModelTrainer.from_pretrained_model(
                    model_name_or_path="distilroberta-base",
                    output_dir=tmp_dir,
                    num_train_epochs=3,
                )

                texts = ["This is a test", "Another test sentence"]
                metrics = trainer.create_fine_tuned_model(texts=texts)

            # Assert
            mock_create_dataset.assert_called_once()
            mock_model_trainer_instance.train.assert_called_once()
            assert metrics["loss"] == 2.0


if __name__ == "__main__":
    unittest.main()
