// Copyright (c) Microsoft. All rights reserved.
package com.microsoft.samples;

import com.microsoft.semantickernel.Kernel;
import com.microsoft.semantickernel.orchestration.PromptExecutionSettings;
import com.microsoft.semantickernel.semanticfunctions.KernelFunction;
import com.microsoft.semantickernel.semanticfunctions.KernelFunctionArguments;
import com.microsoft.semantickernel.semanticfunctions.KernelFunctionFromPrompt;
import com.microsoft.semantickernel.services.textcompletion.TextGenerationService;
import reactor.core.publisher.Flux;

/**
 * Example showing how to use a custom LLM implementation with Semantic Kernel.
 */
public class CustomLLMExample {

    public static void main(String[] args) {
        System.out.println("===== Custom LLM Integration with Semantic Kernel =====\n");
        
        // Create instance of our custom text generation service
        TextGenerationService customLLM = new MyCustomTextGenerationService("custom-service", "my-model-v1");
        
        // Create a kernel with the custom service
        Kernel kernel = Kernel.builder()
                .withAIService(TextGenerationService.class, customLLM, "my-custom-llm")
                .build();

        System.out.println("\n===== 1. Direct Text Generation =====");
        directTextGeneration(kernel);
        
        System.out.println("\n===== 2. Prompt Function with Text Generation =====");
        promptFunctionTextGeneration(kernel);
        
        System.out.println("\n===== 3. Streaming Text Generation =====");
        streamingTextGeneration(kernel);
    }
    
    /**
     * Example of direct text generation using the custom LLM.
     */
    private static void directTextGeneration(Kernel kernel) {
        String prompt = "Why is AI important for modern applications?";
        System.out.println("Prompt: " + prompt);
        
        // Get the AI service from the kernel
        TextGenerationService service = kernel.getService(TextGenerationService.class, "my-custom-llm");
        
        // Generate text directly using the service
        var response = service.getTextContentAsync(
                prompt, 
                PromptExecutionSettings.builder().build(),
                kernel).block();
        
        System.out.println("Response: " + response.getText());
    }
    
    /**
     * Example of using a prompt function with the custom LLM.
     */
    private static void promptFunctionTextGeneration(Kernel kernel) {
        // Create a semantic function from a prompt template
        String promptTemplate = "Write a paragraph about {{$input}}";
        KernelFunction<String> paragraphFunction = KernelFunctionFromPrompt
                .<String>builder()
                .withTemplate(promptTemplate)
                .withOutputVariable("result", "java.lang.String")
                .withName("WriteParagraph")
                .withDescription("Writes a paragraph about a given topic")
                .withDefaultExecutionSettings(
                        PromptExecutionSettings.builder()
                                .withServiceId("my-custom-llm")
                                .build())
                .build();

        // Create arguments
        String topic = "Artificial Intelligence in healthcare";
        KernelFunctionArguments arguments = KernelFunctionArguments.builder()
                .withInput(topic)
                .build();
        
        System.out.println("Topic: " + topic);
        
        // Execute the function
        var result = kernel.invokeAsync(paragraphFunction)
                .withArguments(arguments)
                .block();
        
        System.out.println("Result: " + result.getResult());
    }
    
    /**
     * Example of streaming text generation using the custom LLM.
     */
    private static void streamingTextGeneration(Kernel kernel) {
        String prompt = "Explain quantum computing in simple terms";
        System.out.println("Prompt: " + prompt);
        
        // Get the AI service from the kernel
        TextGenerationService service = kernel.getService(TextGenerationService.class, "my-custom-llm");
        
        // Generate streaming text
        System.out.println("Response:");
        
        Flux<com.microsoft.semantickernel.services.textcompletion.StreamingTextContent> streamingResponse = 
                service.getStreamingTextContentAsync(
                        prompt, 
                        PromptExecutionSettings.builder().build(),
                        kernel);
        
        // Process the streaming response
        streamingResponse.doOnNext(chunk -> {
            System.out.print(chunk.getText());
            System.out.flush();
        }).blockLast();
        
        System.out.println("\nStreaming completed.");
    }
}
