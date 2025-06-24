#!/usr/bin/env python3
"""
Sk Integration Example module

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

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.hugging_face.services.hf_text_completion import HuggingFaceTextCompletion
from semantic_kernel.connectors.ai.hugging_face.training import (
    DatasetConfig,
    HuggingFaceModelTrainer,
    ModelTrainingConfig,
    TrainingArgumentsConfig,
)


async def train_and_use_model_in_kernel() -> None:
    """Train a language model and use it within Semantic Kernel."""
    
    # First, train or fine-tune a model
    model_output_dir = "./output/sk-model"
    
    # Sample text data for fine-tuning
    texts = [
        "Semantic Kernel is a lightweight SDK that integrates Large Language Models (LLMs) with conventional programming languages.",
        "Semantic Kernel combines the best of both worlds: the augmented intelligence of Large Language Models (LLMs) and the solid, well-understood guarantees of traditional programming languages.",
        "The Semantic Kernel is an open-source SDK that allows you to easily combine AI services like OpenAI, Azure OpenAI, and Hugging Face with conventional programming languages like C#, Python, and Java.",
        "With Semantic Kernel, developers can create AI apps that combine the best of both paradigms: the flexibility and augmented intelligence of Large Language Models (LLMs) together with the guarantees and control of traditional programming.",
        "Semantic Kernel is designed to support and encapsulate several design patterns derived from production use cases.",
        "What is Semantic Kernel? Semantic Kernel is an open source SDK that lets you easily combine AI services like OpenAI, Azure OpenAI, and Hugging Face with programming languages like C#, Python, and Java.",
    ]
    
    # Create trainer
    trainer = HuggingFaceModelTrainer.from_pretrained_model(
        model_name_or_path="distilgpt2",  # Use a smaller model for faster training
        output_dir=model_output_dir,
        num_train_epochs=3,
        learning_rate=5e-5,
    )
    
    print("Starting model fine-tuning...")
    metrics = trainer.create_fine_tuned_model(texts=texts)
    print(f"Training complete with metrics: {metrics}")
    
    # Save the model
    trainer.save_model()
    print(f"Model saved to: {model_output_dir}")
    
    # Now, use the fine-tuned model in Semantic Kernel
    kernel = Kernel()
    
    # Add the fine-tuned model as a text completion service
    text_completion = HuggingFaceTextCompletion(
        ai_model_id=model_output_dir,  # Use local path to the trained model
        task="text-generation",  # Specify task type
    )
    
    kernel.add_service(text_completion)
    
    # Create a semantic function using the trained model
    prompt_template = """
    What is Semantic Kernel?
    
    Answer:
    """
    
    # Create and invoke a semantic function
    semantic_function = kernel.create_function_from_prompt(prompt_template=prompt_template)
    result = await kernel.invoke(semantic_function)
    
    print("\nPrediction from fine-tuned model:")
    print(result)


async def train_classifier_and_use_in_kernel() -> None:
    """Train a text classifier and use it within Semantic Kernel."""
    
    # First, train a classifier
    model_output_dir = "./output/sentiment-model"
    
    # Sample text data with labels for sentiment classification
    texts = [
        "I love this product, it's amazing!",
        "The service was excellent and the staff was friendly.",
        "This was a fantastic experience overall.",
        "I'm really happy with my purchase.",
        "This exceeded all my expectations.",
        "I'm disappointed with the quality.",
        "This didn't work as advertised.",
        "The customer service was terrible.",
        "I regret buying this product.",
        "This is the worst experience I've had.",
    ]
    
    labels = [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]  # 1 for positive, 0 for negative
    
    # Create trainer
    trainer = HuggingFaceModelTrainer.from_pretrained_model(
        model_name_or_path="distilbert-base-uncased",
        output_dir=model_output_dir,
        num_train_epochs=5,
        learning_rate=2e-5,
    )
    
    print("Starting classifier training...")
    metrics = trainer.create_fine_tuned_model(texts=texts, labels=labels)
    print(f"Training complete with metrics: {metrics}")
    
    # Save the model
    trainer.save_model()
    print(f"Model saved to: {model_output_dir}")
    
    # Create an integration with the trained classifier that can be used by Semantic Kernel
    # This requires creating a custom class that integrates with Semantic Kernel
    
    class SentimentClassifier:
        """A simple sentiment classifier that can be used with Semantic Kernel."""
        
        def __init__(self, model_path: str):
            """
            Initialize the sentiment classifier.
            
            Args:
                model_path: Path to the trained classifier model.
            """
            from transformers import pipeline
            
            self.classifier = pipeline(
                "text-classification", 
                model=model_path, 
                tokenizer=model_path
            )
        
        def classify(self, text: str) -> str:
            """
            Classify the sentiment of the text.
            
            Args:
                text: The text to classify.
                
            Returns:
                The sentiment classification (positive/negative).
            """
            result = self.classifier(text)[0]
            label = result["label"]
            
            # Convert numeric labels to text
            if label == "LABEL_0":
                return "negative"
            elif label == "LABEL_1":
                return "positive"
            else:
                return label
    
    # Create the classifier
    sentiment_classifier = SentimentClassifier(model_output_dir)
    
    # Test the classifier
    test_texts = [
        "I absolutely love this product!",
        "I'm extremely disappointed with this service."
    ]
    
    print("\nTesting trained sentiment classifier:")
    for text in test_texts:
        sentiment = sentiment_classifier.classify(text)
        print(f"Text: '{text}' - Sentiment: {sentiment}")
    
    # Register the classifier as a plugin in Semantic Kernel
    # This requires creating a kernel function
    kernel = Kernel()
    
    @kernel.function()
    def get_sentiment(text: str) -> str:
        """
        Get the sentiment of the given text.
        
        Args:
            text: The text to analyze.
            
        Returns:
            The sentiment classification (positive/negative).
        """
        return sentiment_classifier.classify(text)
    
    # Use the sentiment classifier in a kernel execution
    result = await kernel.invoke(get_sentiment, "The new update is fantastic and easy to use.")
    print(f"\nSentiment analysis through kernel function: {result}")


if __name__ == "__main__":
    import asyncio
    
    # Choose one of the examples to run
    asyncio.run(train_and_use_model_in_kernel())
    # asyncio.run(train_classifier_and_use_in_kernel())
