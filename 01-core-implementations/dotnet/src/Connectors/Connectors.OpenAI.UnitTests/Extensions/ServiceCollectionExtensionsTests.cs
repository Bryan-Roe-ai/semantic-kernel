// Copyright (c) Microsoft. All rights reserved.

using System;
using System.ClientModel;
using Microsoft.Extensions.AI;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.AudioToText;
using Microsoft.SemanticKernel.ChatCompletion;
using Microsoft.SemanticKernel.Connectors.OpenAI;
using Microsoft.SemanticKernel.Embeddings;
using Microsoft.SemanticKernel.Services;
using Microsoft.SemanticKernel.TextGeneration;
using Microsoft.SemanticKernel.TextToAudio;
using Microsoft.SemanticKernel.TextToImage;
using OpenAI;
using Xunit;

namespace SemanticKernel.Connectors.OpenAI.UnitTests.Extensions;

public class ServiceCollectionExtensionsTests
{
    private const string ObsoleteMessage = "This test is in a deprecated feature will be removed in a future version.";

    #region Chat completion

    [Theory]
    [InlineData(InitializationType.ApiKey)]
    [InlineData(InitializationType.ClientInline)]
    [InlineData(InitializationType.ClientInServiceProvider)]
    public void ItCanAddChatCompletionService(InitializationType type)
    {
        // Arrange
        var client = new OpenAIClient("key");
        var client = new OpenAIClient("key");
        var client = new OpenAIClient(new ApiKeyCredential("key"));
        var client = new OpenAIClient(new ApiKeyCredential("key"));
        var client = new OpenAIClient(new ApiKeyCredential("key"));
        var client = new OpenAIClient(new ApiKeyCredential("key"));
        var builder = Kernel.CreateBuilder();

        builder.Services.AddSingleton(client);

        // Act
        IServiceCollection collection = type switch
        {
            InitializationType.ApiKey => builder.Services.AddOpenAIChatCompletion("deployment-name", "https://endpoint", "api-key"),
            InitializationType.ClientInline => builder.Services.AddOpenAIChatCompletion("deployment-name", client),
            InitializationType.ClientInServiceProvider => builder.Services.AddOpenAIChatCompletion("deployment-name"),
            _ => builder.Services
        };

        // Assert
        var chatCompletionService = builder.Build().GetRequiredService<IChatCompletionService>();
        Assert.True(chatCompletionService is OpenAIChatCompletionService);

        var textGenerationService = builder.Build().GetRequiredService<ITextGenerationService>();
        Assert.True(textGenerationService is OpenAIChatCompletionService);
    }

    #endregion

    [Fact]
    [Obsolete(ObsoleteMessage)]
    public void ItCanAddTextEmbeddingGenerationService()
    {
        // Arrange
        var sut = new ServiceCollection();

        // Act
        var service = sut.AddOpenAITextEmbeddingGeneration("model", "key")
            .BuildServiceProvider()
            .GetRequiredService<ITextEmbeddingGenerationService>();

        // Assert
        Assert.Equal("model", service.Attributes[AIServiceExtensions.ModelIdKey]);
    }

    [Fact]
    [Obsolete(ObsoleteMessage)]
    public void ItCanAddTextEmbeddingGenerationServiceWithOpenAIClient()
    {
        // Arrange
        var sut = new ServiceCollection();

        // Act
        var service = sut.AddOpenAITextEmbeddingGeneration("model", new OpenAIClient("key"))
        var service = sut.AddOpenAITextEmbeddingGeneration("model", new OpenAIClient("key"))
        var service = sut.AddOpenAITextEmbeddingGeneration("model", new OpenAIClient(new ApiKeyCredential("key")))
        var service = sut.AddOpenAITextEmbeddingGeneration("model", new OpenAIClient(new ApiKeyCredential("key")))
        var service = sut.AddOpenAITextEmbeddingGeneration("model", new OpenAIClient(new ApiKeyCredential("key")))
        var service = sut.AddOpenAITextEmbeddingGeneration("model", new OpenAIClient(new ApiKeyCredential("key")))
            .BuildServiceProvider()
            .GetRequiredService<ITextEmbeddingGenerationService>();

        // Assert
        Assert.Equal("model", service.Attributes[AIServiceExtensions.ModelIdKey]);
    }

    [Fact]
    public void ItCanAddEmbeddingGenerator()
    {
        // Arrange
        var sut = new ServiceCollection();
        // Act
        var service = sut.AddOpenAIEmbeddingGenerator("model", "key")
            .BuildServiceProvider()
            .GetRequiredService<IEmbeddingGenerator<string, Embedding<float>>>();
        // Assert
        Assert.Equal("model", service.GetService<EmbeddingGeneratorMetadata>()!.DefaultModelId);
    }

    [Fact]
    public void ItCanAddEmbeddingGeneratorServiceWithOpenAIClient()
    {
        var sut = new ServiceCollection();

        var service = sut.AddOpenAIEmbeddingGenerator("model", openAIClient: new OpenAIClient(new ApiKeyCredential("key")))
            .BuildServiceProvider()
            .GetRequiredService<IEmbeddingGenerator<string, Embedding<float>>>();

        Assert.Equal("model", service.GetService<EmbeddingGeneratorMetadata>()!.DefaultModelId);
    }

    [Fact]
    public void ItCanAddImageToTextService()
    {
        // Arrange
        var sut = new ServiceCollection();

        // Act
        var service = sut.AddOpenAITextToImage("key", modelId: "model")
            .BuildServiceProvider()
            .GetRequiredService<ITextToImageService>();

        // Assert
        Assert.Equal("model", service.Attributes[AIServiceExtensions.ModelIdKey]);
    }

    [Fact]
    public void ItCanAddTextToAudioService()
    {
        // Arrange
        var sut = new ServiceCollection();

        // Act
        var service = sut.AddOpenAITextToAudio("model", "key")
            .BuildServiceProvider()
            .GetRequiredService<ITextToAudioService>();

        // Assert
        Assert.Equal("model", service.Attributes[AIServiceExtensions.ModelIdKey]);
    }

    [Fact]
    public void ItCanAddAudioToTextService()
    {
        // Arrange
        var sut = new ServiceCollection();

        // Act
        var service = sut.AddOpenAIAudioToText("model", "key")
            .BuildServiceProvider()
            .GetRequiredService<IAudioToTextService>();

        // Assert
        Assert.Equal("model", service.Attributes[AIServiceExtensions.ModelIdKey]);
    }

    [Fact]
    public void ItCanAddAudioToTextServiceWithOpenAIClient()
    {
        // Arrange
        var sut = new ServiceCollection();

        // Act
        var service = sut.AddOpenAIAudioToText("model", new OpenAIClient("key"))
        var service = sut.AddOpenAIAudioToText("model", new OpenAIClient("key"))
        var service = sut.AddOpenAIAudioToText("model", new OpenAIClient(new ApiKeyCredential("key")))
        var service = sut.AddOpenAIAudioToText("model", new OpenAIClient(new ApiKeyCredential("key")))
        var service = sut.AddOpenAIAudioToText("model", new OpenAIClient(new ApiKeyCredential("key")))
        var service = sut.AddOpenAIAudioToText("model", new OpenAIClient(new ApiKeyCredential("key")))
            .BuildServiceProvider()
            .GetRequiredService<IAudioToTextService>();

        // Assert
        Assert.Equal("model", service.Attributes[AIServiceExtensions.ModelIdKey]);
    }

    [Fact]
    [Obsolete(ObsoleteMessage)]
    public void ItCanAddFileService()
    {
        // Arrange
        var sut = new ServiceCollection();

        // Act
        var service = sut.AddOpenAIFiles("key")
            .BuildServiceProvider()
            .GetRequiredService<OpenAIFileService>();
    }

    public enum InitializationType
    {
        ApiKey,
        ClientInline,
        ClientInServiceProvider,
        ClientEndpoint,
    }
}
