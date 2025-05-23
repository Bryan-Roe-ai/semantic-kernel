<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
﻿// Copyright (c) Microsoft. All rights reserved.
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
<<<<<<< HEAD
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
﻿// Copyright (c) Microsoft. All rights reserved.
=======
// Copyright (c) Microsoft. All rights reserved.
>>>>>>> main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
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
// Copyright (c) Microsoft. All rights reserved.
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
// Copyright (c) Microsoft. All rights reserved.
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> head
using System.Collections.Generic;
=======
// Copyright (c) Microsoft. All rights reserved.
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Agents.OpenAI;
using Microsoft.SemanticKernel.Agents.OpenAI.Internal;
using Microsoft.SemanticKernel.ChatCompletion;
using OpenAI.Assistants;
using Xunit;

namespace SemanticKernel.Agents.UnitTests.OpenAI.Internal;

/// <summary>
/// Unit testing of <see cref="AssistantRunOptionsFactory"/>.
/// </summary>
public class AssistantRunOptionsFactoryTests
{
    /// <summary>
    /// Verify run options generation with null <see cref="OpenAIAssistantInvocationOptions"/>.
    /// </summary>
    [Fact]
    public void AssistantRunOptionsFactoryExecutionOptionsNullTest()
    {
        // Arrange
        RunCreationOptions defaultOptions =
            new()
            {
                ModelOverride = "gpt-anything",
                Temperature = 0.5F,
                AdditionalInstructions = "test",
            };

        // Act
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
        RunCreationOptions options = AssistantRunOptionsFactory.GenerateOptions(definition, null);

        // Assert
        Assert.NotNull(options);
        Assert.Null(options.Temperature);
        Assert.Null(options.NucleusSamplingFactor);
        Assert.Equal("test", options.AdditionalInstructions);
<<<<<<< Updated upstream
<<<<<<< Updated upstream
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
=======
>>>>>>> Stashed changes
=======
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
=======
>>>>>>> Stashed changes
=======
=======
>>>>>>> Stashed changes
>>>>>>> head
        RunCreationOptions options = AssistantRunOptionsFactory.GenerateOptions(definition, null, null);
=======
        RunCreationOptions options = AssistantRunOptionsFactory.GenerateOptions(defaultOptions, null, null);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

        // Assert
        Assert.NotNull(options);
        Assert.Empty(options.AdditionalMessages);
        Assert.Null(options.InstructionsOverride);
        Assert.Null(options.NucleusSamplingFactor);
        Assert.Equal("test", options.AdditionalInstructions);
<<<<<<< HEAD
            };

        // Act
        RunCreationOptions options = AssistantRunOptionsFactory.GenerateOptions(definition, null);

        // Assert
        Assert.NotNull(options);
        Assert.Null(options.Temperature);
        Assert.Null(options.NucleusSamplingFactor);
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
<<<<<<< HEAD
>>>>>>> main
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
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
>>>>>>> main
>>>>>>> Stashed changes
=======
>>>>>>> main
>>>>>>> Stashed changes
>>>>>>> head
=======
        Assert.Equal(0.5F, options.Temperature);
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
        Assert.Empty(options.Metadata);
    }

    /// <summary>
    /// Verify run options generation with equivalent <see cref="OpenAIAssistantInvocationOptions"/>.
    /// </summary>
    [Fact]
    public void AssistantRunOptionsFactoryExecutionOptionsEquivalentTest()
    {
        // Arrange
        RunCreationOptions defaultOptions =
            new()
            {
                ModelOverride = "gpt-anything",
                Temperature = 0.5F,
            };

        RunCreationOptions invocationOptions =
            new()
            {
                Temperature = 0.5F,
            };

        // Act
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
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
<<<<<<< HEAD
=======
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
=======
>>>>>>> Stashed changes
=======
=======
>>>>>>> Stashed changes
>>>>>>> head
        RunCreationOptions options = AssistantRunOptionsFactory.GenerateOptions(definition, "test", invocationOptions);
=======
        RunCreationOptions options = AssistantRunOptionsFactory.GenerateOptions(defaultOptions, "test", invocationOptions);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

        // Assert
        Assert.NotNull(options);
<<<<<<< HEAD
        Assert.Equal("test", options.InstructionsOverride);
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
<<<<<<< HEAD
>>>>>>> main
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
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
>>>>>>> main
>>>>>>> Stashed changes
=======
>>>>>>> main
>>>>>>> Stashed changes
>>>>>>> head
        RunCreationOptions options = AssistantRunOptionsFactory.GenerateOptions(definition, invocationOptions);

        // Assert
        Assert.NotNull(options);
<<<<<<< HEAD
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
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
<<<<<<< HEAD
=======
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
=======
>>>>>>> Stashed changes
=======
=======
>>>>>>> Stashed changes
>>>>>>> head
        RunCreationOptions options = AssistantRunOptionsFactory.GenerateOptions(definition, "test", invocationOptions);

        // Assert
        Assert.NotNull(options);
        Assert.Equal("test", options.InstructionsOverride);
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
<<<<<<< HEAD
>>>>>>> main
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
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
>>>>>>> main
>>>>>>> Stashed changes
=======
>>>>>>> main
>>>>>>> Stashed changes
>>>>>>> head
        Assert.Null(options.Temperature);
=======
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
        Assert.Null(options.NucleusSamplingFactor);
        Assert.Equal("test", options.InstructionsOverride);
        Assert.Equal(0.5F, options.Temperature);
    }

    /// <summary>
    /// Verify run options generation with <see cref="OpenAIAssistantInvocationOptions"/> override.
    /// </summary>
    [Fact]
    public void AssistantRunOptionsFactoryExecutionOptionsOverrideTest()
    {
        // Arrange
        RunCreationOptions defaultOptions =
            new()
            {
                ModelOverride = "gpt-anything",
                Temperature = 0.5F,
                TruncationStrategy = RunTruncationStrategy.CreateLastMessagesStrategy(5),
            };

        RunCreationOptions invocationOptions =
            new()
            {
                ModelOverride = "gpt-anything",
                AdditionalInstructions = "test2",
                Temperature = 0.9F,
                TruncationStrategy = RunTruncationStrategy.CreateLastMessagesStrategy(8),
                ResponseFormat = AssistantResponseFormat.JsonObject,
            };

        // Act
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        RunCreationOptions options = AssistantRunOptionsFactory.GenerateOptions(definition, invocationOptions);
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
<<<<<<< HEAD
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
        RunCreationOptions options = AssistantRunOptionsFactory.GenerateOptions(definition, invocationOptions);
=======
        RunCreationOptions options = AssistantRunOptionsFactory.GenerateOptions(definition, null, invocationOptions);
        RunCreationOptions options = AssistantRunOptionsFactory.GenerateOptions(definition, invocationOptions);
        RunCreationOptions options = AssistantRunOptionsFactory.GenerateOptions(definition, null, invocationOptions);
>>>>>>> main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
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
        RunCreationOptions options = AssistantRunOptionsFactory.GenerateOptions(definition, null, invocationOptions);
        RunCreationOptions options = AssistantRunOptionsFactory.GenerateOptions(definition, invocationOptions);
        RunCreationOptions options = AssistantRunOptionsFactory.GenerateOptions(definition, null, invocationOptions);
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
        RunCreationOptions options = AssistantRunOptionsFactory.GenerateOptions(definition, null, invocationOptions);
        RunCreationOptions options = AssistantRunOptionsFactory.GenerateOptions(definition, invocationOptions);
        RunCreationOptions options = AssistantRunOptionsFactory.GenerateOptions(definition, null, invocationOptions);
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> head
=======
        RunCreationOptions options = AssistantRunOptionsFactory.GenerateOptions(defaultOptions, null, invocationOptions);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

        // Assert
        Assert.NotNull(options);
        Assert.Equal(0.9F, options.Temperature);
        Assert.Equal(8, options.TruncationStrategy.LastMessages);
        Assert.Equal("test2", options.AdditionalInstructions);
        Assert.Equal(AssistantResponseFormat.JsonObject, options.ResponseFormat);
        Assert.Null(options.NucleusSamplingFactor);
    }

    /// <summary>
    /// Verify run options generation with <see cref="OpenAIAssistantInvocationOptions"/> metadata.
    /// </summary>
    [Fact]
    public void AssistantRunOptionsFactoryExecutionOptionsMetadataTest()
    {
        // Arrange
        RunCreationOptions defaultOptions =
            new()
            {
                ModelOverride = "gpt-anything",
                Temperature = 0.5F,
                TruncationStrategy = RunTruncationStrategy.CreateLastMessagesStrategy(5),
            };

        RunCreationOptions invocationOptions =
            new()
            {
                Metadata =
                {
                    { "key1", "value" },
                    { "key2", null! },
                },
            };

        // Act
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        RunCreationOptions options = AssistantRunOptionsFactory.GenerateOptions(definition, invocationOptions);
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
<<<<<<< HEAD
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
        RunCreationOptions options = AssistantRunOptionsFactory.GenerateOptions(definition, invocationOptions);
=======
        RunCreationOptions options = AssistantRunOptionsFactory.GenerateOptions(definition, null, invocationOptions);
        RunCreationOptions options = AssistantRunOptionsFactory.GenerateOptions(definition, invocationOptions);
        RunCreationOptions options = AssistantRunOptionsFactory.GenerateOptions(definition, null, invocationOptions);
>>>>>>> main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
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
        RunCreationOptions options = AssistantRunOptionsFactory.GenerateOptions(definition, null, invocationOptions);
        RunCreationOptions options = AssistantRunOptionsFactory.GenerateOptions(definition, invocationOptions);
        RunCreationOptions options = AssistantRunOptionsFactory.GenerateOptions(definition, null, invocationOptions);
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
=======
        RunCreationOptions options = AssistantRunOptionsFactory.GenerateOptions(defaultOptions, null, invocationOptions);
>>>>>>> 6829cc1483570aacfbb75d1065c9f2de96c1d77e

        // Assert
        Assert.Equal(2, options.Metadata.Count);
        Assert.Equal("value", options.Metadata["key1"]);
        Assert.Equal(string.Empty, options.Metadata["key2"]);
    }

    /// <summary>
    /// Verify run options generation with <see cref="OpenAIAssistantInvocationOptions"/> metadata.
    /// </summary>
    [Fact]
    public void AssistantRunOptionsFactoryExecutionOptionsMessagesTest()
    {
        // Arrange
        RunCreationOptions defaultOptions =
            new()
            {
                ModelOverride = "gpt-anything",
            };

        ChatMessageContent message = new(AuthorRole.User, "test message");
        RunCreationOptions invocationOptions =
            new()
            {
                AdditionalMessages = { message.ToThreadInitializationMessage() },
            };

        // Act
        RunCreationOptions options = AssistantRunOptionsFactory.GenerateOptions(defaultOptions, null, invocationOptions);

        // Assert
        Assert.Single(options.AdditionalMessages);
    }

    /// <summary>
    /// Verify run options generation with <see cref="OpenAIAssistantInvocationOptions"/> metadata.
    /// </summary>
    [Fact]
    public void AssistantRunOptionsFactoryExecutionOptionsMaxTokensTest()
    {
        // Arrange
        RunCreationOptions defaultOptions =
            new()
            {
                ModelOverride = "gpt-anything",
                Temperature = 0.5F,
                MaxOutputTokenCount = 4096,
                MaxInputTokenCount = 1024,
            };

        // Act
        RunCreationOptions options = AssistantRunOptionsFactory.GenerateOptions(defaultOptions, null, null);

        // Assert
        Assert.Equal(1024, options.MaxInputTokenCount);
        Assert.Equal(4096, options.MaxOutputTokenCount);
    }
}
