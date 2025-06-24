#!/usr/bin/env python3
"""
AI module for training evaluator

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
from typing import Any, Callable, Dict, List, Optional, Tuple, Union, cast

import numpy as np
import torch
from datasets import Dataset, DatasetDict
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    confusion_matrix,
    mean_squared_error,
    r2_score,
)
from transformers import EvalPrediction, PreTrainedTokenizer, TextGenerationPipeline

from semantic_kernel.connectors.ai.hugging_face.training.dataset_processor import DatasetProcessor
from semantic_kernel.connectors.ai.hugging_face.training.training_config import DatasetConfig

logger = logging.getLogger(__name__)


class TrainingEvaluator:
    """Class for evaluating models during and after training."""

    @staticmethod
    def compute_classification_metrics(eval_pred: EvalPrediction) -> Dict[str, float]:
        """
        Compute metrics for classification tasks.
        
        Args:
            eval_pred: The evaluation prediction object containing predictions and labels.
            
        Returns:
            Dict[str, float]: A dictionary containing metrics.
        """
        predictions = eval_pred.predictions
        labels = eval_pred.label_ids
        
        # Get class predictions
        if predictions.ndim > 1 and predictions.shape[-1] > 1:
            # Multi-class case: predictions has shape (batch_size, num_classes)
            predictions = np.argmax(predictions, axis=1)
        
        # Calculate metrics
        metrics = {
            "accuracy": float(accuracy_score(labels, predictions)),
            "f1": float(f1_score(labels, predictions, average="weighted")),
            "precision": float(precision_score(labels, predictions, average="weighted", zero_division=0)),
            "recall": float(recall_score(labels, predictions, average="weighted", zero_division=0)),
        }
        
        return metrics
    
    @staticmethod
    def compute_regression_metrics(eval_pred: EvalPrediction) -> Dict[str, float]:
        """
        Compute metrics for regression tasks.
        
        Args:
            eval_pred: The evaluation prediction object containing predictions and labels.
            
        Returns:
            Dict[str, float]: A dictionary containing metrics.
        """
        predictions = eval_pred.predictions
        labels = eval_pred.label_ids
        
        # Squeeze predictions if needed
        if predictions.ndim > 1 and predictions.shape[-1] == 1:
            predictions = np.squeeze(predictions)
        
        # Calculate metrics
        mse = mean_squared_error(labels, predictions)
        rmse = np.sqrt(mse)
        r2 = r2_score(labels, predictions)
        
        metrics = {
            "mse": float(mse),
            "rmse": float(rmse),
            "r2": float(r2),
        }
        
        return metrics
    
    @staticmethod
    def compute_language_modeling_perplexity(model: Any, dataset: Dataset, tokenizer: PreTrainedTokenizer) -> Dict[str, float]:
        """
        Compute perplexity for language modeling tasks.
        
        Args:
            model: The model to evaluate.
            dataset: The dataset to compute perplexity on.
            tokenizer: The tokenizer to use.
            
        Returns:
            Dict[str, float]: A dictionary containing perplexity.
        """
        try:
            # Prepare model and tokenizer
            model.eval()
            
            # Get text column
            text_column = "text"
            if text_column not in dataset.column_names:
                # Find other potential column names
                potential_text_columns = [col for col in dataset.column_names if "text" in col.lower()]
                if potential_text_columns:
                    text_column = potential_text_columns[0]
                else:
                    text_column = dataset.column_names[0]
            
            # Calculate perplexity
            total_log_likelihood = 0.0
            total_tokens = 0
            
            with torch.no_grad():
                for i in range(min(len(dataset), 100)):  # Limit to 100 examples to avoid long evaluation times
                    try:
                        sample = dataset[i]
                        if isinstance(sample[text_column], list):
                            text = " ".join(sample[text_column])
                        else:
                            text = sample[text_column]
                        
                        inputs = tokenizer(text, return_tensors="pt")
                        inputs = {k: v.to(model.device) for k, v in inputs.items()}
                        
                        outputs = model(**inputs, labels=inputs["input_ids"])
                        
                        log_likelihood = outputs.loss.item() * inputs["input_ids"].shape[1]
                        total_log_likelihood += log_likelihood
                        total_tokens += inputs["input_ids"].shape[1]
                    except Exception as e:
                        logger.warning(f"Error calculating perplexity for sample {i}: {str(e)}")
            
            perplexity = np.exp(total_log_likelihood / total_tokens) if total_tokens > 0 else float("inf")
            
            return {"perplexity": float(perplexity)}
        except Exception as e:
            logger.error(f"Failed to compute perplexity: {str(e)}")
            return {"perplexity": float("inf")}
    
    @staticmethod
    def evaluate_generation_quality(
        model: Any,
        dataset: Dataset,
        tokenizer: PreTrainedTokenizer,
        prompt_column: str = "prompt",
        reference_column: str = "completion",
        max_new_tokens: int = 128,
    ) -> Dict[str, float]:
        """
        Evaluate text generation quality using ROUGE and BLEU scores.
        
        Args:
            model: The model to evaluate.
            dataset: The dataset containing prompts and reference completions.
            tokenizer: The tokenizer to use.
            prompt_column: The column name for prompts.
            reference_column: The column name for reference completions.
            max_new_tokens: Maximum number of new tokens to generate.
            
        Returns:
            Dict[str, float]: A dictionary containing generation quality metrics.
        """
        try:
            # Validate dataset
            if prompt_column not in dataset.column_names or reference_column not in dataset.column_names:
                available_columns = dataset.column_names
                logger.error(f"Required columns not found in dataset. Available columns: {available_columns}")
                return {"error": 1.0}
            
            # Set up generation pipeline
            generation_pipeline = TextGenerationPipeline(model=model, tokenizer=tokenizer)
            
            # Sample a subset if dataset is large (max 50 samples)
            sample_size = min(len(dataset), 50)
            sample_indices = np.random.choice(len(dataset), sample_size, replace=False)
            
            all_generated_texts = []
            all_references = []
            
            # Generate text for each prompt
            for idx in sample_indices:
                sample = dataset[int(idx)]
                prompt = sample[prompt_column]
                reference = sample[reference_column]
                
                # Generate text
                try:
                    output = generation_pipeline(
                        prompt, 
                        max_new_tokens=max_new_tokens, 
                        do_sample=True, 
                        temperature=0.7
                    )
                    generated_text = output[0]["generated_text"]
                    
                    # Remove the prompt from the generated text
                    if generated_text.startswith(prompt):
                        generated_text = generated_text[len(prompt):].strip()
                    
                    all_generated_texts.append(generated_text)
                    all_references.append(reference)
                except Exception as e:
                    logger.warning(f"Error generating text for prompt {idx}: {str(e)}")
            
            # Calculate ROUGE and BLEU scores
            try:
                from rouge_score import rouge_scorer
                import nltk
                try:
                    nltk.data.find('tokenizers/punkt')
                except LookupError:
                    nltk.download('punkt')
                
                # ROUGE scores
                scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
                rouge_scores = {
                    'rouge1': 0.0,
                    'rouge2': 0.0,
                    'rougeL': 0.0
                }
                
                # BLEU score
                total_bleu = 0.0
                
                for gen, ref in zip(all_generated_texts, all_references):
                    # ROUGE
                    scores = scorer.score(ref, gen)
                    for key in rouge_scores.keys():
                        rouge_scores[key] += scores[key].fmeasure
                    
                    # BLEU
                    ref_tokens = nltk.word_tokenize(ref.lower())
                    gen_tokens = nltk.word_tokenize(gen.lower())
                    bleu = nltk.translate.bleu_score.sentence_bleu([ref_tokens], gen_tokens, weights=(0.25, 0.25, 0.25, 0.25))
                    total_bleu += bleu
                
                # Calculate averages
                sample_count = len(all_generated_texts)
                for key in rouge_scores:
                    rouge_scores[key] /= sample_count if sample_count > 0 else 1
                
                bleu_score = total_bleu / sample_count if sample_count > 0 else 0
                
                # Combine metrics
                metrics = {
                    "rouge1_f": float(rouge_scores['rouge1']),
                    "rouge2_f": float(rouge_scores['rouge2']),
                    "rougeL_f": float(rouge_scores['rougeL']),
                    "bleu": float(bleu_score)
                }
                
                return metrics
                
            except ImportError:
                logger.warning("Rouge and/or NLTK packages not found. Skipping ROUGE and BLEU evaluation.")
                return {"missing_dependencies": 1.0}
                
        except Exception as e:
            logger.error(f"Failed to evaluate generation quality: {str(e)}")
            return {"error": 1.0}
    
    @staticmethod
    def get_compute_metrics_function(task_type: str) -> Callable[[EvalPrediction], Dict[str, float]]:
        """
        Get the appropriate compute_metrics function based on the task type.
        
        Args:
            task_type: The type of task (classification, regression, etc.)
            
        Returns:
            A function that computes metrics for the given task type.
        """
        if task_type == "classification":
            return TrainingEvaluator.compute_classification_metrics
        elif task_type == "regression":
            return TrainingEvaluator.compute_regression_metrics
        else:
            # Default to classification metrics
            return TrainingEvaluator.compute_classification_metrics
