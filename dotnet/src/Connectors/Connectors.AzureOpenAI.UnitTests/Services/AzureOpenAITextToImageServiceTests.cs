﻿// Copyright (c) Microsoft. All rights reserved.

using System;
<<<<<<< HEAD
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
using System.IO;
using System.Net.Http;
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< HEAD
using System.IO;
using System.Net.Http;
=======
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
using System.IO;
using System.Net.Http;
=======
>>>>>>> Stashed changes
=======
using System.IO;
using System.Net.Http;
=======
>>>>>>> Stashed changes
using System.ClientModel;
using System.IO;
using System.Net.Http;
using System.Text;
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< HEAD
>>>>>>> main
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
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> main
>>>>>>> Stashed changes
=======
>>>>>>> main
>>>>>>> Stashed changes
using System.Text.Json;
using System.Text.Json.Nodes;
using System.Threading.Tasks;
using Azure.AI.OpenAI;
using Azure.Core;
using Microsoft.Extensions.Logging;
using Microsoft.SemanticKernel.Connectors.AzureOpenAI;
<<<<<<< HEAD
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
using Microsoft.SemanticKernel.Services;
using Moq;
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< HEAD
using Microsoft.SemanticKernel.Services;
using Moq;
=======
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
using Microsoft.SemanticKernel.Services;
using Moq;
=======
>>>>>>> Stashed changes
=======
using Microsoft.SemanticKernel.Services;
using Moq;
=======
>>>>>>> Stashed changes
using Microsoft.SemanticKernel.Connectors.OpenAI;
using Microsoft.SemanticKernel.Services;
using Microsoft.SemanticKernel.TextToImage;
using Moq;
using OpenAI.Images;

#pragma warning disable CS0618 // Type or member is obsolete
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< HEAD
>>>>>>> main
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
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> main
>>>>>>> Stashed changes
=======
>>>>>>> main
>>>>>>> Stashed changes

namespace SemanticKernel.Connectors.AzureOpenAI.UnitTests.Services;

/// <summary>
/// Unit tests for <see cref="AzureOpenAITextToImageService"/> class.
/// </summary>
public sealed class AzureOpenAITextToImageServiceTests : IDisposable
{
    private readonly HttpMessageHandlerStub _messageHandlerStub;
    private readonly HttpClient _httpClient;
    private readonly Mock<ILoggerFactory> _mockLoggerFactory;

    public AzureOpenAITextToImageServiceTests()
    {
        this._messageHandlerStub = new()
        {
            ResponseToReturn = new HttpResponseMessage(System.Net.HttpStatusCode.OK)
            {
<<<<<<< HEAD
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
                Content = new StringContent(File.ReadAllText("./TestData/text-to-image-response.txt"))
=======
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
                Content = new StringContent(File.ReadAllText("./TestData/text-to-image-response.txt"))
=======
                Content = new StringContent(File.ReadAllText("./TestData/text-to-image-response.json"))
>>>>>>> main
<<<<<<< Updated upstream
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
                Content = new StringContent(File.ReadAllText("./TestData/text-to-image-response.json"))
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
            }
        };
        this._httpClient = new HttpClient(this._messageHandlerStub, false);
        this._mockLoggerFactory = new Mock<ILoggerFactory>();
    }

    [Fact]
    public void ConstructorsAddRequiredMetadata()
    {
        // Case #1
        var sut = new AzureOpenAITextToImageService("deployment", "https://api-host/", "api-key", "model", loggerFactory: this._mockLoggerFactory.Object);
        Assert.Equal("deployment", sut.Attributes[AzureClientCore.DeploymentNameKey]);
        Assert.Equal("model", sut.Attributes[AIServiceExtensions.ModelIdKey]);

        // Case #2
        sut = new AzureOpenAITextToImageService("deployment", "https://api-hostapi/", new Mock<TokenCredential>().Object, "model", loggerFactory: this._mockLoggerFactory.Object);
        Assert.Equal("deployment", sut.Attributes[AzureClientCore.DeploymentNameKey]);
        Assert.Equal("model", sut.Attributes[AIServiceExtensions.ModelIdKey]);

        // Case #3
<<<<<<< HEAD
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        sut = new AzureOpenAITextToImageService("deployment", new AzureOpenAIClient(new Uri("https://api-host/"), "api-key"), "model", loggerFactory: this._mockLoggerFactory.Object);
=======
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
        sut = new AzureOpenAITextToImageService("deployment", new AzureOpenAIClient(new Uri("https://api-host/"), "api-key"), "model", loggerFactory: this._mockLoggerFactory.Object);
=======
        sut = new AzureOpenAITextToImageService("deployment", new AzureOpenAIClient(new Uri("https://api-host/"), new ApiKeyCredential("api-key")), "model", loggerFactory: this._mockLoggerFactory.Object);
>>>>>>> main
<<<<<<< Updated upstream
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
        sut = new AzureOpenAITextToImageService("deployment", new AzureOpenAIClient(new Uri("https://api-host/"), new ApiKeyCredential("api-key")), "model", loggerFactory: this._mockLoggerFactory.Object);
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
        Assert.Equal("deployment", sut.Attributes[AzureClientCore.DeploymentNameKey]);
        Assert.Equal("model", sut.Attributes[AIServiceExtensions.ModelIdKey]);
    }

    [Theory]
    [InlineData(256, 256, "dall-e-2")]
    [InlineData(512, 512, "dall-e-2")]
    [InlineData(1024, 1024, "dall-e-2")]
    [InlineData(1024, 1024, "dall-e-3")]
    [InlineData(1024, 1792, "dall-e-3")]
    [InlineData(1792, 1024, "dall-e-3")]
    [InlineData(123, 321, "custom-model-1")]
    [InlineData(179, 124, "custom-model-2")]
    public async Task GenerateImageWorksCorrectlyAsync(int width, int height, string modelId)
    {
        // Arrange
        var sut = new AzureOpenAITextToImageService("deployment", "https://api-host", "api-key", modelId, this._httpClient, loggerFactory: this._mockLoggerFactory.Object);

        // Act 
        var result = await sut.GenerateImageAsync("description", width, height);

        // Assert
        Assert.Equal("https://image-url/", result);

        var request = JsonSerializer.Deserialize<JsonObject>(this._messageHandlerStub.RequestContent); // {"prompt":"description","model":"deployment","response_format":"url","size":"179x124"}
        Assert.NotNull(request);
        Assert.Equal("description", request["prompt"]?.ToString());
        Assert.Equal("deployment", request["model"]?.ToString());
<<<<<<< HEAD
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        Assert.Equal("url", request["response_format"]?.ToString());
=======
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
        Assert.Equal("url", request["response_format"]?.ToString());
=======
        Assert.Null(request["response_format"]);
>>>>>>> main
<<<<<<< Updated upstream
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
        Assert.Null(request["response_format"]);
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
        Assert.Equal($"{width}x{height}", request["size"]?.ToString());
    }

    [Theory]
    [InlineData(true)]
    [InlineData(false)]
    public async Task ItShouldUseProvidedEndpoint(bool useTokeCredential)
    {
        // Arrange
        var sut = useTokeCredential ?
            new AzureOpenAITextToImageService("deployment", endpoint: "https://api-host", new Mock<TokenCredential>().Object, "dall-e-3", this._httpClient) :
            new AzureOpenAITextToImageService("deployment", endpoint: "https://api-host", "api-key", "dall-e-3", this._httpClient);

        // Act
        var result = await sut.GenerateImageAsync("description", 1024, 1024);

        // Assert
        Assert.StartsWith("https://api-host", this._messageHandlerStub.RequestUri?.AbsoluteUri);
    }

    [Theory]
    [InlineData(true, "")]
    [InlineData(true, null)]
    [InlineData(false, "")]
    [InlineData(false, null)]
    public async Task ItShouldUseHttpClientUriIfNoEndpointProvided(bool useTokeCredential, string? endpoint)
    {
        // Arrange
        this._httpClient.BaseAddress = new Uri("https://api-host");

        var sut = useTokeCredential ?
            new AzureOpenAITextToImageService("deployment", endpoint: endpoint!, new Mock<TokenCredential>().Object, "dall-e-3", this._httpClient) :
            new AzureOpenAITextToImageService("deployment", endpoint: endpoint!, "api-key", "dall-e-3", this._httpClient);

        // Act
        var result = await sut.GenerateImageAsync("description", 1024, 1024);

        // Assert
        Assert.StartsWith("https://api-host", this._messageHandlerStub.RequestUri?.AbsoluteUri);
    }

    [Theory]
    [InlineData(true, "")]
    [InlineData(true, null)]
    [InlineData(false, "")]
    [InlineData(false, null)]
    public void ItShouldThrowExceptionIfNoEndpointProvided(bool useTokeCredential, string? endpoint)
    {
        // Arrange
        this._httpClient.BaseAddress = null;

        // Act & Assert
        if (useTokeCredential)
        {
            Assert.Throws<ArgumentException>(() => new AzureOpenAITextToImageService("deployment", endpoint: endpoint!, new Mock<TokenCredential>().Object, "dall-e-3", this._httpClient));
        }
        else
        {
            Assert.Throws<ArgumentException>(() => new AzureOpenAITextToImageService("deployment", endpoint: endpoint!, "api-key", "dall-e-3", this._httpClient));
        }
    }

<<<<<<< HEAD
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
<<<<<<< HEAD
=======
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
=======
>>>>>>> Stashed changes
=======
=======
>>>>>>> Stashed changes
    [Theory]
    [InlineData(null, null)]
    [InlineData("uri", "url")]
    [InlineData("url", "url")]
    [InlineData("GeneratedImage.Uri", "url")]
    [InlineData("bytes", "b64_json")]
    [InlineData("b64_json", "b64_json")]
    [InlineData("GeneratedImage.Bytes", "b64_json")]
    public async Task GetUriImageContentsResponseFormatRequestWorksCorrectlyAsync(string? responseFormatOption, string? expectedResponseFormat)
    {
        // Arrange
        object? responseFormatObject = null;

        switch (responseFormatOption)
        {
            case "GeneratedImage.Uri": responseFormatObject = GeneratedImageFormat.Uri; break;
            case "GeneratedImage.Bytes": responseFormatObject = GeneratedImageFormat.Bytes; break;
            default: responseFormatObject = responseFormatOption; break;
        }

        this._httpClient.BaseAddress = new Uri("https://api-host");
        var sut = new AzureOpenAITextToImageService("deployment", endpoint: null!, credential: new Mock<TokenCredential>().Object, "dall-e-3", this._httpClient);

        // Act
        var result = await sut.GetImageContentsAsync("my prompt", new OpenAITextToImageExecutionSettings { ResponseFormat = responseFormatObject });

        // Assert
        Assert.NotNull(result);
        Assert.NotNull(this._messageHandlerStub.RequestContent);

        var requestBody = UTF8Encoding.UTF8.GetString(this._messageHandlerStub.RequestContent);
        if (expectedResponseFormat is not null)
        {
            Assert.Contains($"\"response_format\":\"{expectedResponseFormat}\"", requestBody);
        }
        else
        {
            // Then no response format is provided, it should not be included in the request body
            Assert.DoesNotContain("response_format", requestBody);
        }
    }

    [Theory]
    [InlineData(null, null)]
    [InlineData("hd", "hd")]
    [InlineData("high", "hd")]
    [InlineData("standard", "standard")]
    public async Task GetUriImageContentsImageQualityRequestWorksCorrectlyAsync(string? quality, string? expectedQuality)
    {
        // Arrange
        this._httpClient.BaseAddress = new Uri("https://api-host");
        var sut = new AzureOpenAITextToImageService("deployment", endpoint: null!, credential: new Mock<TokenCredential>().Object, "dall-e-3", this._httpClient);

        // Act
        var result = await sut.GetImageContentsAsync("my prompt", new OpenAITextToImageExecutionSettings { Quality = quality });

        // Assert
        Assert.NotNull(result);
        Assert.NotNull(this._messageHandlerStub.RequestContent);

        var requestBody = UTF8Encoding.UTF8.GetString(this._messageHandlerStub.RequestContent);
        if (expectedQuality is not null)
        {
            Assert.Contains($"\"quality\":\"{expectedQuality}\"", requestBody);
        }
        else
        {
            // Then no quality is provided, it should not be included in the request body
            Assert.DoesNotContain("quality", requestBody);
        }
    }

    [Theory]
    [InlineData(null, null)]
    [InlineData("vivid", "vivid")]
    [InlineData("natural", "natural")]
    public async Task GetUriImageContentsImageStyleRequestWorksCorrectlyAsync(string? style, string? expectedStyle)
    {
        // Arrange
        this._httpClient.BaseAddress = new Uri("https://api-host");
        var sut = new AzureOpenAITextToImageService("deployment", endpoint: null!, credential: new Mock<TokenCredential>().Object, "dall-e-3", this._httpClient);

        // Act
        var result = await sut.GetImageContentsAsync("my prompt", new OpenAITextToImageExecutionSettings { Style = style });

        // Assert
        Assert.NotNull(result);
        Assert.NotNull(this._messageHandlerStub.RequestContent);

        var requestBody = UTF8Encoding.UTF8.GetString(this._messageHandlerStub.RequestContent);
        if (expectedStyle is not null)
        {
            Assert.Contains($"\"style\":\"{expectedStyle}\"", requestBody);
        }
        else
        {
            // Then no style is provided, it should not be included in the request body
            Assert.DoesNotContain("style", requestBody);
        }
    }

    [Theory]
    [InlineData(null, null, null)]
    [InlineData(1, 2, "1x2")]
    public async Task GetUriImageContentsImageSizeRequestWorksCorrectlyAsync(int? width, int? height, string? expectedSize)
    {
        // Arrange
        this._httpClient.BaseAddress = new Uri("https://api-host");
        var sut = new AzureOpenAITextToImageService("deployment", endpoint: null!, credential: new Mock<TokenCredential>().Object, "dall-e-3", this._httpClient);

        // Act
        var result = await sut.GetImageContentsAsync("my prompt", new OpenAITextToImageExecutionSettings
        {
            Size = width.HasValue && height.HasValue
            ? (width.Value, height.Value)
            : null
        });

        // Assert
        Assert.NotNull(result);
        Assert.NotNull(this._messageHandlerStub.RequestContent);

        var requestBody = UTF8Encoding.UTF8.GetString(this._messageHandlerStub.RequestContent);
        if (expectedSize is not null)
        {
            Assert.Contains($"\"size\":\"{expectedSize}\"", requestBody);
        }
        else
        {
            // Then no size is provided, it should not be included in the request body
            Assert.DoesNotContain("size", requestBody);
        }
    }

    [Fact]
    public async Task GetByteImageContentsResponseWorksCorrectlyAsync()
    {
        // Arrange
        this._messageHandlerStub.ResponseToReturn = new HttpResponseMessage(System.Net.HttpStatusCode.OK)
        {
            Content = new StringContent(File.ReadAllText("./TestData/text-to-image-b64_json-format-response.json"))
        };

        this._httpClient.BaseAddress = new Uri("https://api-host");
        var sut = new AzureOpenAITextToImageService("deployment", endpoint: null!, credential: new Mock<TokenCredential>().Object, "dall-e-3", this._httpClient);

        // Act
        var result = await sut.GetImageContentsAsync("my prompt", new OpenAITextToImageExecutionSettings { ResponseFormat = "b64_json" });

        // Assert
        Assert.NotNull(result);
        Assert.Single(result);
        var imageContent = result[0];
        Assert.NotNull(imageContent);
        Assert.True(imageContent.CanRead);
        Assert.Equal("image/png", imageContent.MimeType);
        Assert.NotNull(imageContent.InnerContent);
        Assert.IsType<GeneratedImage>(imageContent.InnerContent);

        var breakingGlass = imageContent.InnerContent as GeneratedImage;
        Assert.Equal("my prompt", breakingGlass!.RevisedPrompt);
    }

    [Fact]
    public async Task GetUrlImageContentsResponseWorksCorrectlyAsync()
    {
        // Arrange
        this._httpClient.BaseAddress = new Uri("https://api-host");
        var sut = new AzureOpenAITextToImageService("deployment", endpoint: null!, credential: new Mock<TokenCredential>().Object, "dall-e-3", this._httpClient);

        // Act
        var result = await sut.GetImageContentsAsync("my prompt", new OpenAITextToImageExecutionSettings { ResponseFormat = "url" });

        // Assert
        Assert.NotNull(result);
        Assert.Single(result);
        var imageContent = result[0];
        Assert.NotNull(imageContent);
        Assert.False(imageContent.CanRead);
        Assert.Equal(new Uri("https://image-url/"), imageContent.Uri);
        Assert.NotNull(imageContent.InnerContent);
        Assert.IsType<GeneratedImage>(imageContent.InnerContent);

        var breakingGlass = imageContent.InnerContent as GeneratedImage;
        Assert.Equal("my prompt", breakingGlass!.RevisedPrompt);
    }

<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< HEAD
>>>>>>> main
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
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> main
>>>>>>> Stashed changes
=======
>>>>>>> main
>>>>>>> Stashed changes
    public void Dispose()
    {
        this._httpClient.Dispose();
        this._messageHandlerStub.Dispose();
    }
}
