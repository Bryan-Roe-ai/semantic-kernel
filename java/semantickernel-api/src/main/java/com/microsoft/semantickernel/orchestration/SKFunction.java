// Copyright (c) Microsoft. All rights reserved.
package com.microsoft.semantickernel.orchestration;

<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
import com.microsoft.semantickernel.memory.SemanticTextMemory;
import com.microsoft.semantickernel.skilldefinition.FunctionView;
import com.microsoft.semantickernel.skilldefinition.ReadOnlySkillCollection;
import javax.annotation.CheckReturnValue;
import javax.annotation.Nullable;
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< main
=======
import javax.annotation.CheckReturnValue;
import javax.annotation.Nullable;

import com.microsoft.semantickernel.Kernel;
>>>>>>> origin/dsgrieve/java-v1-api
import com.microsoft.semantickernel.memory.SemanticTextMemory;
import com.microsoft.semantickernel.skilldefinition.FunctionView;
import com.microsoft.semantickernel.skilldefinition.ReadOnlySkillCollection;

<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
<<<<<<< div
=======
=======
>>>>>>> Stashed changes
>>>>>>> head
<<<<<<< main
=======
import javax.annotation.CheckReturnValue;
import javax.annotation.Nullable;

import com.microsoft.semantickernel.Kernel;
>>>>>>> origin/dsgrieve/java-v1-api
import com.microsoft.semantickernel.memory.SemanticTextMemory;
import com.microsoft.semantickernel.skilldefinition.FunctionView;
import com.microsoft.semantickernel.skilldefinition.ReadOnlySkillCollection;

<<<<<<< div
>>>>>>> main
=======
<<<<<<< Updated upstream
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
import reactor.core.publisher.Mono;

/**
 * Semantic Kernel callable function interface
 *
 * @param <RequestConfiguration> The type of the configuration argument that will be provided when
 *     the function is invoked
 */
public interface SKFunction<RequestConfiguration> {
    /**
     * Returns a description of the function, including parameters.
     *
     * @return An instance of {@link FunctionView} describing the function
     */
    @Nullable
    FunctionView describe();

    /**
     * Invokes the function with the given input, context and settings
     *
     * @param input input provided to the function
     * @param context Request context
     * @param settings Configuration of the request
     * @return an updated context with the result of the request
     */
    @CheckReturnValue
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    Mono<SKContext> invokeAsync(String input, SKContext context, RequestConfiguration settings);
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
<<<<<<< Updated upstream
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
=======
>>>>>>> Stashed changes
>>>>>>> Stashed changes
<<<<<<< main
    Mono<SKContext> invokeAsync(String input, SKContext context, RequestConfiguration settings);
=======
    @Deprecated
    default Mono<SKContext> invokeAsync(String input, SKContext context, Object settings) {
        throw new UnsupportedOperationException("Deprecated");
    }
>>>>>>> origin/dsgrieve/java-v1-api
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head

    /**
     * Invokes the function
     *
     * @return an updated context with the result of the request
     */
    Mono<SKContext> invokeAsync();

    /**
     * Invokes the function with the given input
     *
     * @param input input provided to the function
     * @return an updated context with the result of the request
     */
    @CheckReturnValue
    Mono<SKContext> invokeAsync(String input);

    /**
     * The type of the configuration argument that will be provided when the function is invoked
     *
     * @return The type
     */
    @Nullable
    Class<RequestConfiguration> getType();

    /**
     * Invokes the function with the given context and settings
     *
     * @param context Request context
     * @return an updated context with the result of the request
     */
    @CheckReturnValue
<<<<<<< div
<<<<<<< div
=======
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< div
=======
<<<<<<< main
>>>>>>> main
=======
<<<<<<< Updated upstream
=======
<<<<<<< main
>>>>>>> origin/main
>>>>>>> head
=======
>>>>>>> Stashed changes
    Mono<SKContext> invokeAsync(SKContext context);

    /**
=======
<<<<<<< div
<<<<<<< div
=======
<<<<<<< head
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< main
    Mono<SKContext> invokeAsync(SKContext context);

    /**
=======
<<<<<<< div
=======
>>>>>>> main
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
    @Deprecated
    default Mono<SKContext> invokeAsync(SKContext context) {
        throw new UnsupportedOperationException("Deprecated");
    }

    /**
     * The type of the configuration argument that will be provided when the function is invoked
     *
     * @return The type @Nullable Class<RequestConfiguration> getType();
     */

    /**
     * Invokes the function with the given context and settings
     *
     * @param kernel Associated Kernel
     * @param variables Request variables
     * @param streaming Whether streaming is on or not
     * @return an updated context with the result of the request
     */
    @CheckReturnValue
    default Mono<FunctionResult> invokeAsync(Kernel kernel, ContextVariables variables, boolean streaming) {
        throw new UnsupportedOperationException("Deprecated");
    }


    /**
>>>>>>> origin/dsgrieve/java-v1-api
<<<<<<< div
<<<<<<< div
=======
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
>>>>>>> main
=======
>>>>>>> head
     * Invokes the function with the given context and settings
     *
     * @param context Request context
     * @param settings Configuration of the request
     * @return an updated context with the result of the request
     */
    @CheckReturnValue
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    Mono<SKContext> invokeAsync(SKContext context, @Nullable RequestConfiguration settings);
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< main
    Mono<SKContext> invokeAsync(SKContext context, @Nullable RequestConfiguration settings);
=======
=======
<<<<<<< main
    Mono<SKContext> invokeAsync(SKContext context, @Nullable RequestConfiguration settings);
=======
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
<<<<<<< main
    Mono<SKContext> invokeAsync(SKContext context, @Nullable RequestConfiguration settings);
=======
>>>>>>> Stashed changes
=======
<<<<<<< main
    Mono<SKContext> invokeAsync(SKContext context, @Nullable RequestConfiguration settings);
=======
>>>>>>> Stashed changes
>>>>>>> head
    @Deprecated
    default Mono<SKContext> invokeAsync(SKContext context, @Nullable Object settings) {
        throw new UnsupportedOperationException("Deprecated");
    }
>>>>>>> origin/dsgrieve/java-v1-api
<<<<<<< div
<<<<<<< div
=======
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
>>>>>>> main
=======
>>>>>>> head

    /**
     * @return The name of the skill that this function is within
     */
    String getSkillName();

    /**
     * @return The name of this function
     */
    String getName();

    /**
     * The function to create a fully qualified name for
     *
     * @return A fully qualified name for a function
     */
    String toFullyQualifiedName();

    /**
     * @return A description of the function
     */
    String getDescription();

    /**
     * Create a string for generating an embedding for a function.
     *
     * @return A string for generating an embedding for a function.
     */
    String toEmbeddingString();

    /**
     * Create a manual-friendly string for a function.
     *
<<<<<<< AI
=======
<<<<<<< HEAD
>>>>>>> main
     * @param includeOutputs Whether to include function outputs in the string.
     * @return A manual-friendly string for a function.
     */
    String toManualString(boolean includeOutputs);
<<<<<<< AI
     * @return A manual-friendly string for a function.
     */
    String toManualString();
=======
=======
     * @return A manual-friendly string for a function.
     */
    String toManualString();
>>>>>>> beeed7b7a795d8c989165740de6ddb21aeacbb6f
>>>>>>> main
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< main
=======
=======
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
<<<<<<< main
=======
>>>>>>> Stashed changes
=======
<<<<<<< main
=======
>>>>>>> Stashed changes
>>>>>>> head

    @Deprecated
    default Class<?> getType() {
        throw new UnsupportedOperationException("Deprecated");
    }
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
>>>>>>> origin/main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
<<<<<<< div
>>>>>>> main
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> origin/main
>>>>>>> head

    /**
     * Invokes the function with the given input, context and settings
     *
     * @param variables variables to be used in the function
     * @param semanticMemory semantic memory to be used in the function
     * @param skills skills to be used in the function
     * @return an updated context with the result of the request
     */
    Mono<SKContext> invokeWithCustomInputAsync(
            ContextVariables variables,
            @Nullable SemanticTextMemory semanticMemory,
            @Nullable ReadOnlySkillCollection skills);
}
