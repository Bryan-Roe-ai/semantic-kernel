// Copyright (c) Microsoft. All rights reserved.
package com.microsoft.samples;

import reactor.core.publisher.Mono;
import java.util.List;
import java.util.Map;
import java.nio.file.Path;

/**
 * Interface for LLMs that support training/fine-tuning capabilities.
 * This extends the standard functionality of Semantic Kernel's text generation
 * with methods for model training.
 */
public interface TrainableLLM {
    
    /**
     * Data class representing a training example (prompt-completion pair).
     */
    class TrainingExample {
        private String prompt;
        private String completion;
        
        public TrainingExample(String prompt, String completion) {
            this.prompt = prompt;
            this.completion = completion;
        }
        
        public String getPrompt() {
            return prompt;
        }
        
        public String getCompletion() {
            return completion;
        }
    }
    
    /**
     * Data class for training configuration.
     */
    class TrainingConfig {
        private int epochs;
        private double learningRate;
        private int batchSize;
        private Map<String, Object> additionalParams;
        
        public TrainingConfig(int epochs, double learningRate, int batchSize, 
                             Map<String, Object> additionalParams) {
            this.epochs = epochs;
            this.learningRate = learningRate;
            this.batchSize = batchSize;
            this.additionalParams = additionalParams;
        }
        
        public int getEpochs() {
            return epochs;
        }
        
        public double getLearningRate() {
            return learningRate;
        }
        
        public int getBatchSize() {
            return batchSize;
        }
        
        public Map<String, Object> getAdditionalParams() {
            return additionalParams;
        }
    }
    
    /**
     * Data class for training result metrics.
     */
    class TrainingResult {
        private boolean success;
        private String modelVersion;
        private Map<String, Double> metrics;
        private String errorMessage;
        
        public TrainingResult(boolean success, String modelVersion, 
                             Map<String, Double> metrics, String errorMessage) {
            this.success = success;
            this.modelVersion = modelVersion;
            this.metrics = metrics;
            this.errorMessage = errorMessage;
        }
        
        public boolean isSuccess() {
            return success;
        }
        
        public String getModelVersion() {
            return modelVersion;
        }
        
        public Map<String, Double> getMetrics() {
            return metrics;
        }
        
        public String getErrorMessage() {
            return errorMessage;
        }
    }
    
    /**
     * Trains the LLM with provided examples.
     * 
     * @param examples List of training examples (prompt-completion pairs)
     * @param config Training configuration parameters
     * @return A Mono with training results and metrics
     */
    Mono<TrainingResult> trainAsync(List<TrainingExample> examples, TrainingConfig config);
    
    /**
     * Trains the LLM using data from a file.
     * 
     * @param trainingDataPath Path to the training data file
     * @param config Training configuration parameters
     * @return A Mono with training results and metrics
     */
    Mono<TrainingResult> trainFromFileAsync(Path trainingDataPath, TrainingConfig config);
    
    /**
     * Evaluates the LLM performance using provided examples.
     * 
     * @param testExamples List of test examples
     * @return A Mono with evaluation metrics
     */
    Mono<Map<String, Double>> evaluateAsync(List<TrainingExample> testExamples);
    
    /**
     * Saves the trained model to a specified location.
     * 
     * @param savePath Path where to save the model
     * @return A Mono completing when the save operation is done
     */
    Mono<Void> saveModelAsync(Path savePath);
    
    /**
     * Loads a previously trained model from a specified location.
     * 
     * @param modelPath Path to the saved model
     * @return A Mono completing when the load operation is done
     */
    Mono<Void> loadModelAsync(Path modelPath);
}
