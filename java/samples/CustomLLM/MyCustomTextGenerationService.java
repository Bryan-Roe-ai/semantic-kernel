// Copyright (c) Microsoft. All rights reserved.
package com.microsoft.samples;

import com.microsoft.semantickernel.Kernel;
import com.microsoft.semantickernel.services.textcompletion.TextGenerationService;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Duration;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.Collectors;

/**
 * A custom text generation service implementation with training capabilities.
 * This demonstrates how to create your own trainable LLM implementation for Semantic Kernel.
 */
public class MyCustomTextGenerationService implements TextGenerationService, TrainableLLM {

    private static String LLM_RESULT_TEXT = 
        "Output from your custom model: "
        + "AI is awesome because it can help us solve complex problems, enhance our creativity, "
        + "and improve our lives in many ways. AI can perform tasks that are too difficult, "
        + "tedious, or dangerous for humans, such as diagnosing diseases, detecting fraud, or "
        + "exploring space. AI can also augment our abilities and inspire us to create new forms "
        + "of art, music, or literature. AI can improve our well-being and happiness by "
        + "providing personalized recommendations, entertainment, and assistance.";

    private final String serviceId;
    private final String modelId;
    private final Map<String, Object> attributes;
    
    // Simple in-memory storage for training examples
    private final List<TrainingExample> trainingData = new ArrayList<>();
    
    // Model state variables
    private String modelVersion = "1.0.0";
    private boolean isModelTrained = false;
    private Map<String, String> promptCompletionMap = new ConcurrentHashMap<>();

    /**
     * Constructor for the custom text generation service.
     *
     * @param serviceId The service identifier
     * @param modelId The model identifier
     */
    public MyCustomTextGenerationService(String serviceId, String modelId) {
        this.serviceId = serviceId;
        this.modelId = modelId;
        
        // Create attributes map with service and model information
        Map<String, Object> attrs = new HashMap<>();
        attrs.put("service_id", serviceId);
        attrs.put("model_id", modelId);
        this.attributes = Collections.unmodifiableMap(attrs);
    }

    @Override
    public Map<String, Object> getAttributes() {
        return attributes;
    }

    @Override
    public Mono<com.microsoft.semantickernel.services.textcompletion.TextContent> getTextContentAsync(
            String prompt, 
            com.microsoft.semantickernel.orchestration.PromptExecutionSettings executionSettings, 
            Kernel kernel) {
        
        System.out.println("Processing prompt: " + prompt);
        
        // Simulate processing time
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        return Mono.just(new com.microsoft.semantickernel.services.textcompletion.TextContent(LLM_RESULT_TEXT));
    }

    @Override
    public Flux<com.microsoft.semantickernel.services.textcompletion.StreamingTextContent> getStreamingTextContentAsync(
            String prompt, 
            com.microsoft.semantickernel.orchestration.PromptExecutionSettings executionSettings, 
            Kernel kernel) {
        
        System.out.println("Processing streaming prompt: " + prompt);
        
        // Try to find a completion for this prompt in our trained data
        String result = promptCompletionMap.getOrDefault(prompt, LLM_RESULT_TEXT);
        
        // Split result into words for streaming simulation
        String[] words = result.split(" ");
        
        return Flux.range(0, words.length)
                .delayElements(Duration.ofMillis(100))
                .map(i -> new com.microsoft.semantickernel.services.textcompletion.StreamingTextContent(words[i] + " "));
    }
    
    @Override
    public Mono<com.microsoft.semantickernel.services.textcompletion.TextContent> getTextContentAsync(
            String prompt, 
            com.microsoft.semantickernel.orchestration.PromptExecutionSettings executionSettings, 
            Kernel kernel) {
        
        System.out.println("Processing prompt: " + prompt);
        
        // Simulate processing time
        try {
            Thread.sleep(500);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        // If model is trained, try to find a completion from the training data
        String result;
        if (isModelTrained && promptCompletionMap.containsKey(prompt)) {
            result = promptCompletionMap.get(prompt);
            System.out.println("Using trained response for prompt: " + prompt);
        } else {
            result = LLM_RESULT_TEXT;
            System.out.println("Using default response (no training match found)");
        }

        return Mono.just(new com.microsoft.semantickernel.services.textcompletion.TextContent(result));
    }
    
    /**
     * Updates the model's default response based on training.
     * This is a simplified representation of how training might affect the model.
     */
    private void updateModelResponse() {
        if (!trainingData.isEmpty()) {
            // In a real implementation, this would use the training data to update the model
            // For this example, we'll just concatenate some of the completions to create a new response
            String newResponse = "Output from your trained model: ";
            
            // Add a sample of completions (up to 3) to construct a representative response
            List<TrainingExample> sampleExamples = trainingData.size() > 3 ? 
                trainingData.subList(0, 3) : trainingData;
                
            for (TrainingExample example : sampleExamples) {
                newResponse += example.getCompletion().substring(0, 
                    Math.min(50, example.getCompletion().length())) + "... ";
            }
            
            // Update the model's default response
            LLM_RESULT_TEXT = newResponse;
        }
    }
    
    @Override
    public Mono<TrainingResult> trainAsync(List<TrainingExample> examples, TrainingConfig config) {
        System.out.println("Starting model training with " + examples.size() + " examples");
        System.out.println("Training configuration: " + config.getEpochs() + " epochs, " +
                        "learning rate: " + config.getLearningRate() + ", batch size: " + config.getBatchSize());
        
        return Mono.create(sink -> {
            try {
                // Clear existing training data for this example (in production, you might want to append instead)
                trainingData.clear();
                promptCompletionMap.clear();
                
                // Add all examples to our training data
                trainingData.addAll(examples);
                
                // Simulate training process
                Map<String, Double> metrics = new HashMap<>();
                double loss = 0.0;
                
                // Simulated training loop
                for (int epoch = 0; epoch < config.getEpochs(); epoch++) {
                    System.out.println("Training epoch " + (epoch + 1) + "/" + config.getEpochs());
                    
                    // Process each example in batches (simplified)
                    for (int i = 0; i < examples.size(); i += config.getBatchSize()) {
                        int endIndex = Math.min(i + config.getBatchSize(), examples.size());
                        List<TrainingExample> batch = examples.subList(i, endIndex);
                        
                        // Process batch (in a real implementation, this would update the model weights)
                        for (TrainingExample example : batch) {
                            // Add to prompt-completion map for inference
                            promptCompletionMap.put(example.getPrompt(), example.getCompletion());
                            
                            // Simulate loss calculation
                            loss += 0.1 * Math.random(); // Decreasing loss simulation
                        }
                        
                        // Simulate batch processing delay
                        Thread.sleep(200);
                    }
                    
                    // Calculate and store metrics
                    double epochLoss = loss / examples.size();
                    double accuracy = 0.5 + (0.5 * (1.0 - epochLoss)); // Simulated accuracy
                    System.out.println("Epoch " + (epoch + 1) + " - Loss: " + epochLoss + ", Accuracy: " + accuracy);
                    
                    metrics.put("loss_epoch_" + (epoch + 1), epochLoss);
                    metrics.put("accuracy_epoch_" + (epoch + 1), accuracy);
                }
                
                // Update model version
                modelVersion = "1.1." + System.currentTimeMillis() % 1000;
                isModelTrained = true;
                
                // Update the model's default response based on training
                updateModelResponse();
                
                // Add final metrics
                metrics.put("final_loss", loss / (config.getEpochs() * examples.size()));
                metrics.put("examples_count", (double) examples.size());
                metrics.put("training_time_ms", (double) (config.getEpochs() * examples.size() * 10)); // Simulated time
                
                System.out.println("Training completed successfully. New model version: " + modelVersion);
                
                TrainingResult result = new TrainingResult(true, modelVersion, metrics, null);
                sink.success(result);
                
            } catch (Exception e) {
                System.err.println("Error during training: " + e.getMessage());
                TrainingResult errorResult = new TrainingResult(false, modelVersion, 
                                                              Map.of("error", 1.0), 
                                                              e.getMessage());
                sink.success(errorResult);
            }
        });
    }
    
    @Override
    public Mono<TrainingResult> trainFromFileAsync(Path trainingDataPath, TrainingConfig config) {
        return Mono.create(sink -> {
            try {
                System.out.println("Loading training data from file: " + trainingDataPath);
                
                // Read training data from file
                List<TrainingExample> examples = new ArrayList<>();
                
                try (BufferedReader reader = Files.newBufferedReader(trainingDataPath)) {
                    String line;
                    String currentPrompt = null;
                    StringBuilder currentCompletion = new StringBuilder();
                    
                    // Simple format: lines starting with "PROMPT:" define a new example
                    // lines starting with "COMPLETION:" give the completion
                    // Empty line separates examples
                    
                    while ((line = reader.readLine()) != null) {
                        if (line.startsWith("PROMPT: ")) {
                            // If we have a previous example, save it
                            if (currentPrompt != null && currentCompletion.length() > 0) {
                                examples.add(new TrainingExample(
                                    currentPrompt, currentCompletion.toString().trim()));
                                currentCompletion = new StringBuilder();
                            }
                            currentPrompt = line.substring("PROMPT: ".length());
                        } else if (line.startsWith("COMPLETION: ")) {
                            currentCompletion.append(line.substring("COMPLETION: ".length()));
                        } else if (line.trim().isEmpty()) {
                            // Empty line means end of example
                            if (currentPrompt != null && currentCompletion.length() > 0) {
                                examples.add(new TrainingExample(
                                    currentPrompt, currentCompletion.toString().trim()));
                                currentPrompt = null;
                                currentCompletion = new StringBuilder();
                            }
                        } else if (currentPrompt != null) {
                            // Continue current completion
                            currentCompletion.append(" ").append(line);
                        }
                    }
                    
                    // Don't forget the last example
                    if (currentPrompt != null && currentCompletion.length() > 0) {
                        examples.add(new TrainingExample(
                            currentPrompt, currentCompletion.toString().trim()));
                    }
                }
                
                System.out.println("Loaded " + examples.size() + " training examples");
                
                // Forward to the regular training method
                trainAsync(examples, config).subscribe(result -> sink.success(result),
                                                      error -> sink.error(error));
                
            } catch (IOException e) {
                System.err.println("Error reading training data file: " + e.getMessage());
                TrainingResult errorResult = new TrainingResult(false, modelVersion, 
                                                              Map.of("error", 1.0), 
                                                              "Error reading file: " + e.getMessage());
                sink.success(errorResult);
            }
        });
    }
    
    @Override
    public Mono<Map<String, Double>> evaluateAsync(List<TrainingExample> testExamples) {
        return Mono.create(sink -> {
            try {
                System.out.println("Evaluating model on " + testExamples.size() + " examples");
                
                if (!isModelTrained) {
                    sink.success(Map.of(
                        "error", 1.0,
                        "message", 0.0,
                        "accuracy", 0.0
                    ));
                    return;
                }
                
                int correct = 0;
                double totalLoss = 0.0;
                
                // Evaluate each example
                for (TrainingExample example : testExamples) {
                    String expectedCompletion = example.getCompletion();
                    
                    // Get the model's completion for this prompt
                    String actualCompletion = promptCompletionMap.getOrDefault(example.getPrompt(), LLM_RESULT_TEXT);
                    
                    // Simple exact match evaluation
                    if (actualCompletion.equals(expectedCompletion)) {
                        correct++;
                    }
                    
                    // Simple loss calculation (in real implementations this would be more sophisticated)
                    totalLoss += calculateStringDistance(actualCompletion, expectedCompletion);
                }
                
                double accuracy = (double) correct / testExamples.size();
                double avgLoss = totalLoss / testExamples.size();
                
                System.out.println("Evaluation results - Accuracy: " + accuracy + ", Average Loss: " + avgLoss);
                
                Map<String, Double> metrics = new HashMap<>();
                metrics.put("accuracy", accuracy);
                metrics.put("loss", avgLoss);
                metrics.put("examples_tested", (double) testExamples.size());
                
                sink.success(metrics);
                
            } catch (Exception e) {
                System.err.println("Error during evaluation: " + e.getMessage());
                sink.success(Map.of("error", 1.0, "message", 0.0));
            }
        });
    }
    
    /**
     * Simple string distance calculation for evaluation purposes.
     * In a real implementation, you would use more sophisticated metrics.
     */
    private double calculateStringDistance(String s1, String s2) {
        // Simple implementation of normalized Levenshtein distance
        int maxLen = Math.max(s1.length(), s2.length());
        if (maxLen == 0) return 0.0;
        
        int[][] dp = new int[s1.length() + 1][s2.length() + 1];
        
        for (int i = 0; i <= s1.length(); i++) dp[i][0] = i;
        for (int j = 0; j <= s2.length(); j++) dp[0][j] = j;
        
        for (int i = 1; i <= s1.length(); i++) {
            for (int j = 1; j <= s2.length(); j++) {
                int cost = (s1.charAt(i-1) == s2.charAt(j-1)) ? 0 : 1;
                dp[i][j] = Math.min(Math.min(dp[i-1][j] + 1, dp[i][j-1] + 1), dp[i-1][j-1] + cost);
            }
        }
        
        return (double) dp[s1.length()][s2.length()] / maxLen;
    }
    
    @Override
    public Mono<Void> saveModelAsync(Path savePath) {
        return Mono.create(sink -> {
            try {
                System.out.println("Saving model to: " + savePath);
                
                // Create directory if it doesn't exist
                Files.createDirectories(savePath.getParent());
                
                // Simple serialization of the model state
                // In a real implementation, this would save actual model weights, configuration, etc.
                StringBuilder modelData = new StringBuilder();
                
                // Write metadata
                modelData.append("# Custom LLM Model Save\n");
                modelData.append("# Version: ").append(modelVersion).append("\n");
                modelData.append("# Timestamp: ").append(System.currentTimeMillis()).append("\n");
                modelData.append("# Service ID: ").append(serviceId).append("\n");
                modelData.append("# Model ID: ").append(modelId).append("\n\n");
                
                // Write training data
                modelData.append("# Training Examples: ").append(trainingData.size()).append("\n\n");
                
                for (TrainingExample example : trainingData) {
                    modelData.append("PROMPT: ").append(example.getPrompt()).append("\n");
                    modelData.append("COMPLETION: ").append(example.getCompletion()).append("\n\n");
                }
                
                // Write prompt-completion map
                modelData.append("# Prompt-Completion Mappings: ").append(promptCompletionMap.size()).append("\n\n");
                
                // Save model data to file
                Files.writeString(savePath, modelData.toString());
                
                System.out.println("Model saved successfully");
                sink.success();
                
            } catch (IOException e) {
                System.err.println("Error saving model: " + e.getMessage());
                sink.error(e);
            }
        });
    }
    
    @Override
    public Mono<Void> loadModelAsync(Path modelPath) {
        return Mono.create(sink -> {
            try {
                System.out.println("Loading model from: " + modelPath);
                
                if (!Files.exists(modelPath)) {
                    throw new IOException("Model file does not exist: " + modelPath);
                }
                
                // Clear existing state
                trainingData.clear();
                promptCompletionMap.clear();
                
                // Read model file
                List<String> lines = Files.readAllLines(modelPath);
                
                String currentPrompt = null;
                StringBuilder currentCompletion = new StringBuilder();
                String currentModelVersion = "1.0.0"; // Default if not found in file
                
                for (int i = 0; i < lines.size(); i++) {
                    String line = lines.get(i);
                    
                    // Parse metadata
                    if (line.startsWith("# Version: ")) {
                        currentModelVersion = line.substring("# Version: ".length()).trim();
                    } else if (line.startsWith("PROMPT: ")) {
                        // If we have a previous example, save it
                        if (currentPrompt != null && currentCompletion.length() > 0) {
                            TrainingExample example = new TrainingExample(
                                currentPrompt, currentCompletion.toString().trim());
                            trainingData.add(example);
                            promptCompletionMap.put(example.getPrompt(), example.getCompletion());
                            currentCompletion = new StringBuilder();
                        }
                        currentPrompt = line.substring("PROMPT: ".length());
                    } else if (line.startsWith("COMPLETION: ")) {
                        currentCompletion.append(line.substring("COMPLETION: ".length()));
                    } else if (line.trim().isEmpty()) {
                        // Empty line means end of example
                        if (currentPrompt != null && currentCompletion.length() > 0) {
                            TrainingExample example = new TrainingExample(
                                currentPrompt, currentCompletion.toString().trim());
                            trainingData.add(example);
                            promptCompletionMap.put(example.getPrompt(), example.getCompletion());
                            currentPrompt = null;
                            currentCompletion = new StringBuilder();
                        }
                    } else if (currentPrompt != null) {
                        // Continue current completion
                        currentCompletion.append(" ").append(line);
                    }
                }
                
                // Don't forget the last example
                if (currentPrompt != null && currentCompletion.length() > 0) {
                    TrainingExample example = new TrainingExample(
                        currentPrompt, currentCompletion.toString().trim());
                    trainingData.add(example);
                    promptCompletionMap.put(example.getPrompt(), example.getCompletion());
                }
                
                // Update model state
                this.modelVersion = currentModelVersion;
                isModelTrained = !trainingData.isEmpty();
                
                // Update model response if needed
                if (isModelTrained) {
                    updateModelResponse();
                }
                
                System.out.println("Model loaded successfully. Version: " + modelVersion);
                System.out.println("Loaded " + trainingData.size() + " training examples");
                
                sink.success();
                
            } catch (Exception e) {
                System.err.println("Error loading model: " + e.getMessage());
                sink.error(e);
            }
        });
    }
}
