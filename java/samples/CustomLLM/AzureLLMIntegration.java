// Copyright (c) Microsoft. All rights reserved.
package com.microsoft.samples;

import com.azure.ai.openai.OpenAIAsyncClient;
import com.azure.ai.openai.OpenAIClientBuilder;
import com.azure.core.credential.AzureKeyCredential;
import com.microsoft.semantickernel.Kernel;
import com.microsoft.semantickernel.aiservices.openai.chatcompletion.OpenAIChatCompletion;
import com.microsoft.semantickernel.orchestration.PromptExecutionSettings;
import com.microsoft.semantickernel.semanticfunctions.KernelFunction;
import com.microsoft.semantickernel.semanticfunctions.KernelFunctionArguments;
import com.microsoft.semantickernel.semanticfunctions.KernelFunctionFromPrompt;
import com.microsoft.semantickernel.services.chatcompletion.ChatCompletionService;

import java.util.HashMap;
import java.util.Map;

/**
 * Example showing how to integrate custom LLM with Azure services following best practices.
 */
public class AzureLLMIntegration {

    // Environment variables for configuration
    private static final String AZURE_OPENAI_KEY = System.getenv("AZURE_OPENAI_KEY");
    private static final String AZURE_OPENAI_ENDPOINT = System.getenv("AZURE_OPENAI_ENDPOINT"); 
    private static final String AZURE_OPENAI_DEPLOYMENT = System.getenv("AZURE_OPENAI_DEPLOYMENT");

    public static void main(String[] args) {
        System.out.println("===== Azure LLM Integration with Semantic Kernel =====\n");

        // Create a kernel with both Azure OpenAI and custom LLM services
        Kernel kernel = buildKernelWithMultipleLLMs();
        
        // Example with multiple LLMs (Azure and custom)
        System.out.println("\n===== Multi-LLM Integration Example =====");
        multiLLMExample(kernel);
    }

    /**
     * Builds a kernel with both Azure OpenAI and custom LLM services.
     * Follows Azure best practices for configuration.
     */
    private static Kernel buildKernelWithMultipleLLMs() {
        // Create our custom LLM service
        var customLLM = new MyCustomTextGenerationService("custom-service", "my-model-v1");
        
        // Create Azure OpenAI client with best practices:
        // - Using environment variables for secure configuration
        // - Using AzureKeyCredential for authentication
        // - Implementing proper error handling
        OpenAIAsyncClient azureClient = null;
        ChatCompletionService azureOpenAI = null;
        
        try {
            if (AZURE_OPENAI_KEY != null && !AZURE_OPENAI_KEY.isEmpty() && 
                AZURE_OPENAI_ENDPOINT != null && !AZURE_OPENAI_ENDPOINT.isEmpty()) {
                
                // Create Azure OpenAI client
                azureClient = new OpenAIClientBuilder()
                    .credential(new AzureKeyCredential(AZURE_OPENAI_KEY))
                    .endpoint(AZURE_OPENAI_ENDPOINT)
                    .buildAsyncClient();
                
                // Create Azure OpenAI service
                String modelId = AZURE_OPENAI_DEPLOYMENT != null ? 
                    AZURE_OPENAI_DEPLOYMENT : "gpt-35-turbo";
                
                azureOpenAI = OpenAIChatCompletion.builder()
                    .withOpenAIAsyncClient(azureClient)
                    .withModelId(modelId)
                    .build();
                
                System.out.println("Successfully configured Azure OpenAI service");
            } else {
                System.out.println("Azure OpenAI environment variables not set, using only custom LLM");
            }
        } catch (Exception e) {
            System.err.println("Failed to initialize Azure OpenAI client: " + e.getMessage());
            // In production code, consider logging this error properly
        }
        
        // Build kernel with both services when available
        var kernelBuilder = Kernel.builder()
            .withAIService(com.microsoft.semantickernel.services.textcompletion.TextGenerationService.class, 
                    customLLM, "custom-llm");
            
        if (azureOpenAI != null) {
            kernelBuilder.withAIService(ChatCompletionService.class, azureOpenAI, "azure-openai");
        }
        
        return kernelBuilder.build();
    }

    /**
     * Example demonstrating using multiple LLMs with service selection.
     */
    private static void multiLLMExample(Kernel kernel) {
        // Create a prompt template with multiple model configurations
        Map<String, PromptExecutionSettings> modelSettings = new HashMap<>();
        
        // Add settings for our custom LLM
        modelSettings.put("custom-llm", 
            PromptExecutionSettings.builder()
                .withServiceId("custom-llm")
                .build());
        
        // Add settings for Azure OpenAI if available
        if (kernel.getServices().containsKey("ChatCompletionService:azure-openai")) {
            modelSettings.put("azure-openai", 
                PromptExecutionSettings.builder()
                    .withServiceId("azure-openai")
                    .build());
        }
        
        // Create a prompt function that can use different services
        String promptTemplate = "Explain the concept of {{$input}} in simple terms.";
        KernelFunction<String> explainFunction = KernelFunctionFromPrompt
            .<String>builder()
            .withTemplate(promptTemplate)
            .withOutputVariable("result", "java.lang.String")
            .withName("ExplainConcept")
            .withDescription("Explains a concept in simple terms")
            .build();
        
        // Define the topic to explain
        String topic = "Machine Learning";
        System.out.println("Topic: " + topic);
        
        // Create arguments with execution settings for a specific service
        KernelFunctionArguments argsCustomLlm = KernelFunctionArguments.builder()
            .withInput(topic)
            .withExecutionSettings(modelSettings)
            .build();
        
        // Try to execute with custom LLM
        System.out.println("Using custom LLM:");
        try {
            var customLLMResult = kernel.invokeAsync(explainFunction)
                .withArguments(argsCustomLlm)
                .block();
            System.out.println("Result: " + customLLMResult.getResult());
        } catch (Exception e) {
            System.err.println("Error using custom LLM: " + e.getMessage());
        }
        
        // Try to execute with Azure OpenAI if available
        if (kernel.getServices().containsKey("ChatCompletionService:azure-openai")) {
            System.out.println("\nUsing Azure OpenAI:");
            try {
                // Create arguments specifying Azure service
                KernelFunctionArguments argsAzure = KernelFunctionArguments.builder()
                    .withInput(topic)
                    .withExecutionSettings("azure-openai", 
                        PromptExecutionSettings.builder().withServiceId("azure-openai").build())
                    .build();
                
                var azureResult = kernel.invokeAsync(explainFunction)
                    .withArguments(argsAzure)
                    .block();
                System.out.println("Result: " + azureResult.getResult());
            } catch (Exception e) {
                System.err.println("Error using Azure OpenAI: " + e.getMessage());
            }
        }
    }
}
