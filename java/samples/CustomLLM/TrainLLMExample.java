// Copyright (c) Microsoft. All rights reserved.
package com.microsoft.samples;

import com.microsoft.semantickernel.Kernel;
import com.microsoft.semantickernel.orchestration.PromptExecutionSettings;
import com.microsoft.semantickernel.semanticfunctions.KernelFunctionArguments;
import com.microsoft.semantickernel.semanticfunctions.KernelFunctionFromPrompt;
import com.microsoft.semantickernel.services.textcompletion.TextGenerationService;

import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Example demonstrating how to train and use a custom LLM with Semantic Kernel.
 */
public class TrainLLMExample {

    public static void main(String[] args) {
        System.out.println("===== Training Custom LLM with Semantic Kernel =====\n");
        
        // Create instance of our custom text generation service with training capabilities
        MyCustomTextGenerationService customLLM = new MyCustomTextGenerationService("custom-service", "my-model-v1");
        
        // Create a kernel with the custom service
        Kernel kernel = Kernel.builder()
                .withAIService(TextGenerationService.class, customLLM, "my-custom-llm")
                .build();
        
        try {
            // Example flow: Create training data, train model, evaluate, and use
            System.out.println("\n===== 1. Prepare Training Data =====");
            List<TrainableLLM.TrainingExample> trainingExamples = createTrainingExamples();
            
            System.out.println("\n===== 2. Train the Model =====");
            TrainableLLM.TrainingConfig config = createTrainingConfig();
            trainModel(customLLM, trainingExamples, config);
            
            // Save the trained model
            Path savePath = Paths.get("trained_model.txt");
            System.out.println("\nSaving model to: " + savePath.toAbsolutePath());
            customLLM.saveModelAsync(savePath).block();
            
            System.out.println("\n===== 3. Test with Trained Model =====");
            testTrainedModel(kernel, customLLM, trainingExamples);
            
            System.out.println("\n===== 4. Create Training Data File =====");
            createTrainingDataFile();
            
            System.out.println("\n===== 5. Train from File =====");
            trainFromFile(customLLM);
            
        } catch (Exception e) {
            System.err.println("Error in training demonstration: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    /**
     * Creates a list of training examples.
     */
    private static List<TrainableLLM.TrainingExample> createTrainingExamples() {
        List<TrainableLLM.TrainingExample> examples = new ArrayList<>();
        
        // Add examples for question answering
        examples.add(new TrainableLLM.TrainingExample(
            "What is semantic kernel?",
            "Semantic Kernel is an open-source SDK that lets you easily combine AI services like " + 
            "LLMs with conventional programming languages. It supports prompt templating, function " + 
            "chaining, vectorized memory, and intelligent planning capabilities."
        ));
        
        examples.add(new TrainableLLM.TrainingExample(
            "Explain how LLMs work",
            "Large Language Models (LLMs) are deep learning models trained on vast amounts of text data. " + 
            "They use transformer architectures to process and generate human-like text by predicting " + 
            "the next word in a sequence based on context. LLMs can understand and generate language, " + 
            "translate between languages, write different kinds of creative content, and answer questions."
        ));
        
        examples.add(new TrainableLLM.TrainingExample(
            "How do I integrate a custom LLM with Semantic Kernel?",
            "To integrate a custom LLM with Semantic Kernel, you need to implement the TextGenerationService " + 
            "interface, configure the service with your model parameters, and register it with the Kernel. " + 
            "This allows Semantic Kernel to use your custom LLM for text generation tasks and prompt functions."
        ));
        
        examples.add(new TrainableLLM.TrainingExample(
            "What are the benefits of fine-tuning an LLM?",
            "Fine-tuning an LLM provides several benefits: 1) Better performance on domain-specific tasks, " + 
            "2) More consistent outputs aligned with your requirements, 3) Reduced need for complex prompting, " + 
            "4) Potentially lower latency and token usage, and 5) Ability to learn from examples that would be " + 
            "difficult to specify through prompting alone."
        ));
        
        System.out.println("Created " + examples.size() + " training examples");
        return examples;
    }
    
    /**
     * Creates training configuration.
     */
    private static TrainableLLM.TrainingConfig createTrainingConfig() {
        // Additional parameters that could be used by specific implementations
        Map<String, Object> additionalParams = new HashMap<>();
        additionalParams.put("dropout", 0.1);
        additionalParams.put("weight_decay", 0.01);
        additionalParams.put("warmup_steps", 100);
        
        TrainableLLM.TrainingConfig config = new TrainableLLM.TrainingConfig(
            5,       // epochs
            0.0002,  // learning rate
            2,       // batch size
            additionalParams
        );
        
        System.out.println("Created training configuration with " + config.getEpochs() + " epochs");
        return config;
    }
    
    /**
     * Trains the model with provided examples.
     */
    private static void trainModel(TrainableLLM model, 
                                 List<TrainableLLM.TrainingExample> trainingExamples, 
                                 TrainableLLM.TrainingConfig config) {
        System.out.println("Starting model training...");
        
        TrainableLLM.TrainingResult result = model.trainAsync(trainingExamples, config).block();
        
        if (result.isSuccess()) {
            System.out.println("Training completed successfully!");
            System.out.println("Model version: " + result.getModelVersion());
            System.out.println("Training metrics:");
            
            result.getMetrics().forEach((key, value) -> {
                System.out.println("  " + key + ": " + value);
            });
        } else {
            System.err.println("Training failed: " + result.getErrorMessage());
        }
    }
    
    /**
     * Tests the trained model by evaluating it and running inference.
     */
    private static void testTrainedModel(Kernel kernel, 
                                       TrainableLLM model, 
                                       List<TrainableLLM.TrainingExample> trainingExamples) {
        System.out.println("Evaluating model performance...");
        
        // Create test examples (using training data for simplicity)
        List<TrainableLLM.TrainingExample> testExamples = new ArrayList<>(trainingExamples);
        
        // Evaluate model
        Map<String, Double> metrics = model.evaluateAsync(testExamples).block();
        
        System.out.println("Evaluation metrics:");
        metrics.forEach((key, value) -> {
            System.out.println("  " + key + ": " + value);
        });
        
        // Test inference with a prompt function
        System.out.println("\nTesting inference with a prompt function...");
        
        // Create a semantic function using our trained model
        var promptFunction = KernelFunctionFromPrompt
            .<String>builder()
            .withTemplate("{{$input}}")
            .withOutputVariable("result", "java.lang.String")
            .withName("TrainedModelQuery")
            .withDescription("Uses the trained model to answer questions")
            .withDefaultExecutionSettings(
                PromptExecutionSettings.builder()
                    .withServiceId("my-custom-llm")
                    .build())
            .build();
            
        // Test with one of the training examples
        String testPrompt = trainingExamples.get(0).getPrompt();
        System.out.println("Test prompt: " + testPrompt);
        
        // Execute the function
        var args = KernelFunctionArguments.builder()
            .withInput(testPrompt)
            .build();
            
        var result = kernel.invokeAsync(promptFunction)
            .withArguments(args)
            .block();
        
        System.out.println("Model response: " + result.getResult());
        
        // Test with a new prompt
        String newPrompt = "How does training work in Semantic Kernel?";
        System.out.println("\nTest with new prompt: " + newPrompt);
        
        args = KernelFunctionArguments.builder()
            .withInput(newPrompt)
            .build();
            
        result = kernel.invokeAsync(promptFunction)
            .withArguments(args)
            .block();
        
        System.out.println("Model response: " + result.getResult());
    }
    
    /**
     * Creates a training data file for file-based training.
     */
    private static void createTrainingDataFile() {
        try {
            Path trainingDataPath = Paths.get("training_data.txt");
            
            StringBuilder content = new StringBuilder();
            content.append("PROMPT: What is Azure OpenAI Service?\n");
            content.append("COMPLETION: Azure OpenAI Service is a cloud-based service that provides access to OpenAI's LLMs including GPT-4, GPT-3.5-Turbo, and Embeddings models. It includes enterprise-grade security, compliance, regional availability, and provides the same capabilities as OpenAI but with the additional enterprise capabilities of Azure.\n\n");
            
            content.append("PROMPT: What are the benefits of using Semantic Kernel with Azure?\n");
            content.append("COMPLETION: Using Semantic Kernel with Azure provides several benefits: seamless integration with Azure OpenAI Service, enterprise-grade security and compliance, scalable infrastructure, and access to other Azure services like Azure Cognitive Services, Azure Machine Learning, and Azure Storage. This combination enables building advanced AI applications with proper governance and security controls.\n\n");
            
            content.append("PROMPT: How do I handle rate limiting with Azure OpenAI?\n");
            content.append("COMPLETION: To handle rate limiting with Azure OpenAI Service: 1) Implement exponential backoff and retry policies, 2) Monitor usage with Azure Metrics and set up alerts, 3) Use client-side throttling, 4) Consider using multiple deployments across regions, and 5) Cache responses when appropriate. You can also request quota increases through the Azure portal if needed.\n\n");
            
            Files.writeString(trainingDataPath, content.toString());
            System.out.println("Created training data file at: " + trainingDataPath.toAbsolutePath());
            
        } catch (Exception e) {
            System.err.println("Error creating training data file: " + e.getMessage());
        }
    }
    
    /**
     * Demonstrates training from a file.
     */
    private static void trainFromFile(TrainableLLM model) {
        try {
            Path trainingDataPath = Paths.get("training_data.txt");
            
            if (!Files.exists(trainingDataPath)) {
                System.err.println("Training data file not found: " + trainingDataPath);
                return;
            }
            
            System.out.println("Training model from file: " + trainingDataPath);
            
            // Create training config
            TrainableLLM.TrainingConfig config = new TrainableLLM.TrainingConfig(
                3,       // epochs
                0.0001,  // learning rate
                1,       // batch size
                new HashMap<>()
            );
            
            // Train from file
            TrainableLLM.TrainingResult result = model.trainFromFileAsync(trainingDataPath, config).block();
            
            if (result.isSuccess()) {
                System.out.println("File-based training completed successfully!");
                System.out.println("Model version: " + result.getModelVersion());
                System.out.println("Training metrics:");
                
                result.getMetrics().forEach((key, value) -> {
                    System.out.println("  " + key + ": " + value);
                });
            } else {
                System.err.println("File-based training failed: " + result.getErrorMessage());
            }
            
        } catch (Exception e) {
            System.err.println("Error in file-based training: " + e.getMessage());
        }
    }
}
