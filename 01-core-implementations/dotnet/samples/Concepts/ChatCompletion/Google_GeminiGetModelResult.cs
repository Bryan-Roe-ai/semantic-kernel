// Copyright (c        Console.WriteLine("======== Inline Function Definition + Invocation ========"); Microsoft. All rights reserved.

using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Connectors.Google;

namespace ChatCompletion;

/// <summary>
/// Represents an example class for Gemini Embedding Generation with volatile memory store.
/// </summary>
public sealed class Google_GeminiGetModelResult(ITestOutputHelper output) : BaseTest(output)
{
    [Fact]
    public async Task GetTokenUsageMetadata()
    {
        Console.WriteLine("======== Inline Function Definition + Invocation ========");

        Assert.NotNull(TestConfiguration.VertexAI.BearerKey);
        Assert.NotNull(TestConfiguration.VertexAI.Location);
        Assert.NotNull(TestConfiguration.VertexAI.ProjectId);
        Assert.NotNull(TestConfiguration.VertexAI.Gemini.ModelId);

        // Create kernel
        Kernel kernel = Kernel.CreateBuilder()
            .AddVertexAIGeminiChatCompletion(
                modelId: TestConfiguration.VertexAI.Gemini.ModelId,
                bearerKey: TestConfiguration.VertexAI.BearerKey,
                location: TestConfiguration.VertexAI.Location,
                projectId: TestConfiguration.VertexAI.ProjectId)
            .Build();

        // To generate bearer key, you need installed google sdk or use google web console with command:
        //
        //   gcloud auth print-access-token
        //
        // Above code pass bearer key as string, it is not recommended way in production code,
        // especially if IChatCompletionService will be long lived, tokens generated by google sdk lives for 1 hour.
        // You should use bearer key provider, which will be used to generate token on demand:
        //
        // Example:
        //
        // Kernel kernel = Kernel.CreateBuilder()
        //     .AddVertexAIGeminiChatCompletion(
        //         modelId: TestConfiguration.VertexAI.Gemini.ModelId,
        //         bearerKeyProvider: () =>
        //         {
        //             // This is just example, in production we recommend using Google SDK to generate your BearerKey token.
        //             // This delegate will be called on every request,
        //             // when providing the token consider using caching strategy and refresh token logic when it is expired or close to expiration.
        //             return GetBearerKey();
        //         },
        //         location: TestConfiguration.VertexAI.Location,
        //         projectId: TestConfiguration.VertexAI.ProjectId)

        string prompt = "Hi, give me 5 book suggestions about: travel";

        // Invoke function through kernel
        FunctionResult result = await kernel.InvokePromptAsync(prompt);

        // Display results
        var geminiMetadata = result.Metadata as GeminiMetadata;
        Console.WriteLine(result.GetValue<string>());
        Console.WriteLine(geminiMetadata?.AsJson());
    }
}
