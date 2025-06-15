// Copyright (c) Microsoft. All rights reserved.
package com.microsoft.samples;

import com.azure.ai.openai.OpenAIAsyncClient;
import com.azure.ai.openai.OpenAIClientBuilder;
import com.azure.core.credential.AzureKeyCredential;
import com.microsoft.semantickernel.Kernel;
import com.microsoft.semantickernel.services.textcompletion.TextGenerationService;
import reactor.core.publisher.Mono;

import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;

/**
 * Example showing how to integrate custom LLM training with Azure Machine Learning.
 * This demonstrates more advanced training scenarios following Azure best practices.
 */
public class AzureMLTrainingExample {
    
    // Environment variables for configuration
    private static final String AZURE_ML_ENDPOINT = System.getenv("AZURE_ML_ENDPOINT");
    private static final String AZURE_ML_API_KEY = System.getenv("AZURE_ML_API_KEY");
    private static final String AZURE_STORAGE_CONNECTION_STRING = System.getenv("AZURE_STORAGE_CONNECTION_STRING");
    
    public static void main(String[] args) {
        System.out.println("===== Azure ML Integration for LLM Training =====\n");
        
        // Create our trainable custom LLM service
        MyCustomTextGenerationService customLLM = new MyCustomTextGenerationService("azure-ml-custom", "custom-model-v1");
        
        // Create a kernel with the custom service
        Kernel kernel = Kernel.builder()
                .withAIService(TextGenerationService.class, customLLM, "custom-llm")
                .build();
                
        try {
            // Demonstrate Azure integration
            System.out.println("Checking Azure ML integration availability...");
            
            if (isAzureMLConfigured()) {
                System.out.println("Azure ML is configured. Demonstrating Azure ML integration.");
                trainWithAzureML(customLLM);
            } else {
                System.out.println("Azure ML is not configured. Running local simulation instead.");
                simulateAzureMLTraining(customLLM);
            }
            
            // Test the trained model with a few examples
            System.out.println("\n===== Testing Azure ML Trained Model =====");
            testTrainedModel(kernel, customLLM);
            
        } catch (Exception e) {
            System.err.println("Error in Azure ML training demonstration: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    /**
     * Checks if Azure ML is configured.
     */
    private static boolean isAzureMLConfigured() {
        return AZURE_ML_ENDPOINT != null && !AZURE_ML_ENDPOINT.isEmpty() &&
               AZURE_ML_API_KEY != null && !AZURE_ML_API_KEY.isEmpty();
    }
    
    /**
     * Simulates Azure ML training when actual Azure credentials are not available.
     */
    private static void simulateAzureMLTraining(TrainableLLM model) {
        System.out.println("\n===== Simulating Azure ML Training =====");
        
        // Prepare training data for Azure ML 
        List<TrainableLLM.TrainingExample> trainingExamples = createAzureSpecificTrainingData();
        
        // Create Azure-specific training configuration
        Map<String, Object> azureParams = new HashMap<>();
        azureParams.put("compute_target", "gpu-cluster");
        azureParams.put("distributed_training", true);
        azureParams.put("framework", "PyTorch");
        azureParams.put("max_runtime_hours", 2);
        
        TrainableLLM.TrainingConfig config = new TrainableLLM.TrainingConfig(
            10,      // epochs
            5e-5,    // learning rate 
            16,      // batch size
            azureParams
        );
        
        System.out.println("Submitting training job to simulated Azure ML...");
        System.out.println("Training data size: " + trainingExamples.size() + " examples");
        System.out.println("Azure ML configuration:");
        config.getAdditionalParams().forEach((key, value) -> {
            System.out.println("  " + key + ": " + value);
        });
        
        // Simulate Azure ML training
        simulateAzureMLJob(() -> {
            System.out.println("Simulating Azure ML training job...");
            
            // Just use the local training implementation with Azure parameters
            return model.trainAsync(trainingExamples, config);
        }).block();
        
        System.out.println("Azure ML training simulation completed!");
    }
    
    /**
     * Implements training with Azure Machine Learning.
     * In a real application, this would submit the training job to Azure ML.
     */
    private static void trainWithAzureML(TrainableLLM model) {
        System.out.println("\n===== Training with Azure Machine Learning =====");
        
        try {
            // Create an Azure ML client (stub for demonstration purposes)
            System.out.println("Creating Azure ML client with endpoint: " + AZURE_ML_ENDPOINT);
            var azureMlClient = createAzureMlClient();
            
            // Prepare training data
            List<TrainableLLM.TrainingExample> trainingExamples = createAzureSpecificTrainingData();
            
            // Upload training data to Azure Blob Storage
            System.out.println("Uploading training data to Azure Blob Storage...");
            Path trainingDataPath = uploadTrainingDataToBlob(trainingExamples);
            
            // Create Azure ML experiment
            System.out.println("Creating Azure ML experiment: custom-llm-training");
            
            // Configure compute target
            System.out.println("Configuring compute target: gpu-cluster");
            
            // Configure training script and parameters
            Map<String, Object> azureParams = new HashMap<>();
            azureParams.put("compute_target", "gpu-cluster");
            azureParams.put("distributed_training", true);
            azureParams.put("framework", "PyTorch");
            azureParams.put("max_runtime_hours", 4);
            azureParams.put("training_data_path", trainingDataPath.toString());
            
            TrainableLLM.TrainingConfig config = new TrainableLLM.TrainingConfig(
                20,      // epochs
                2e-5,    // learning rate
                32,      // batch size
                azureParams
            );
            
            // Submit Azure ML job
            System.out.println("Submitting training job to Azure ML...");
            
            // Simulate the Azure ML job execution
            simulateAzureMLJob(() -> {
                System.out.println("Azure ML job in progress...");
                return model.trainAsync(trainingExamples, config);
            }).block();
            
            // Download the trained model from Azure ML
            System.out.println("Training completed! Downloading trained model from Azure ML...");
            
            // Register model in Azure ML Model Registry
            System.out.println("Registering model in Azure ML Model Registry as 'custom-llm-model'");
            
            // Load the downloaded model
            System.out.println("Loading trained model...");
            model.loadModelAsync(Paths.get("azure_ml_trained_model.txt")).block();
            
            System.out.println("Azure ML training workflow completed successfully!");
            
        } catch (Exception e) {
            System.err.println("Error in Azure ML training: " + e.getMessage());
        }
    }
    
    /**
     * Creates Azure-specific training data.
     */
    private static List<TrainableLLM.TrainingExample> createAzureSpecificTrainingData() {
        List<TrainableLLM.TrainingExample> examples = new ArrayList<>();
        
        // Add Azure-specific training examples
        examples.add(new TrainableLLM.TrainingExample(
            "How do I deploy a model to Azure ML?",
            "To deploy a model to Azure ML: 1) Register your trained model, 2) Define an inference configuration " +
            "with entry script and dependencies, 3) Define a deployment configuration (ACI or AKS), " +
            "4) Deploy the model as a web service, and 5) Test the deployed endpoint with sample input data."
        ));
        
        examples.add(new TrainableLLM.TrainingExample(
            "What is Azure OpenAI Service?",
            "Azure OpenAI Service provides REST API access to OpenAI's powerful language models including GPT-4, " +
            "GPT-3.5-Turbo, and Embeddings model series. These models can be easily adapted to your specific task " +
            "including content generation, summarization, semantic search, and natural language to code translation. " +
            "Users can access the service through REST APIs, Python SDK, or web-based interface."
        ));
        
        examples.add(new TrainableLLM.TrainingExample(
            "How do I fine-tune a model with Azure OpenAI?",
            "To fine-tune a model with Azure OpenAI: 1) Prepare your training data in JSONL format with prompt-completion " +
            "pairs, 2) Upload your training data using the Azure OpenAI Studio or API, 3) Create a fine-tuning job " +
            "specifying the base model and training parameters, 4) Monitor the fine-tuning job progress, and 5) Once " +
            "complete, use the fine-tuned model by specifying its deployment name in your API calls."
        ));
        
        examples.add(new TrainableLLM.TrainingExample(
            "Compare Azure OpenAI with Azure ML for LLM deployment",
            "Azure OpenAI Service provides pre-trained LLMs with simple deployment and fine-tuning options, while Azure " +
            "Machine Learning offers a more comprehensive platform for custom ML workflows. Use Azure OpenAI for " +
            "quick access to state-of-the-art models with minimal customization, and Azure ML when you need complete " +
            "control over model training, fine-tuning pipelines, or when working with proprietary models. Azure ML " +
            "also offers better MLOps capabilities for production deployments."
        ));
        
        examples.add(new TrainableLLM.TrainingExample(
            "What are best practices for prompt engineering in Azure OpenAI?",
            "Best practices for prompt engineering in Azure OpenAI include: 1) Be clear and specific with instructions, " +
            "2) Structure prompts with clear formatting, 3) Provide high-quality examples for few-shot learning, " + 
            "4) Use system messages to set context and constraints, 5) Break complex tasks into smaller steps, " +
            "6) Implement proper error handling for API calls, 7) Use temperature settings appropriate to your task, " +
            "and 8) Apply responsible AI filters to prevent harmful content generation."
        ));
        
        return examples;
    }
    
    /**
     * Creates stub for Azure ML client.
     */
    private static Object createAzureMlClient() {
        // In a real implementation, this would create and return an actual
        // Azure ML client using the Azure SDK
        return new Object(); // Simple stub for demo
    }
    
    /**
     * Simulates uploading training data to Azure Blob Storage.
     */
    private static Path uploadTrainingDataToBlob(List<TrainableLLM.TrainingExample> trainingExamples) {
        // In a real implementation, this would upload data to Azure Blob Storage
        // and return the path/URI
        return Paths.get("azureml-data", "training-data-" + System.currentTimeMillis() + ".jsonl");
    }
    
    /**
     * Simulates an Azure ML job execution.
     */
    private static <T> Mono<T> simulateAzureMLJob(java.util.function.Supplier<Mono<T>> jobFunc) {
        return Mono.create(sink -> {
            System.out.println("Starting Azure ML job simulation...");
            
            // Simulate job preparation
            try {
                System.out.println("Preparing Azure ML environment...");
                Thread.sleep(1000);
                
                System.out.println("Allocating compute resources...");
                Thread.sleep(1000);
                
                System.out.println("Setting up Docker container...");
                Thread.sleep(1000);
                
                System.out.println("Starting training run...");
                
                // Run the actual job function
                jobFunc.get().subscribe(
                    result -> {
                        // Simulate job completion
                        try {
                            System.out.println("Training completed, finalizing results...");
                            Thread.sleep(500);
                            
                            System.out.println("Saving model artifacts...");
                            Thread.sleep(500);
                            
                            System.out.println("Generating metrics and logs...");
                            Thread.sleep(500);
                        } catch (InterruptedException e) {
                            Thread.currentThread().interrupt();
                        }
                        
                        sink.success(result);
                    },
                    error -> sink.error(error)
                );
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                sink.error(e);
            }
        });
    }
    
    /**
     * Tests the trained model with a few examples.
     */
    private static void testTrainedModel(Kernel kernel, MyCustomTextGenerationService model) {
        // Test with Azure-specific queries
        String[] testQueries = {
            "How do I deploy a model to Azure ML?",
            "What is the best way to use Azure OpenAI with Semantic Kernel?",
            "What are the cost considerations for Azure OpenAI Service?"
        };
        
        for (String query : testQueries) {
            System.out.println("\nTesting with query: " + query);
            
            // Get response directly from the model
            var response = model.getTextContentAsync(
                query, 
                com.microsoft.semantickernel.orchestration.PromptExecutionSettings.builder().build(),
                kernel).block();
            
            System.out.println("Model response: " + response.getText());
        }
    }
}
