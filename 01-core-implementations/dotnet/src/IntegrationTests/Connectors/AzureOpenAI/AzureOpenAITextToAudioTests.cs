// Copyright (c) Microsoft. All rights reserved.

using System.Threading.Tasks;
usi>>>>>>>+HEAD
tity;
ususing Azure.Identity;

ion;

// Copyright (c) Microsoft. All rights reserved.

using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;

using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.TextToAudio;
using SemanticKernel.IntegrationTests.TestSettings;
using Xunit;

namespace SemanticKernel.IntegrationTests.Connectors.AzureOpenAI;

public sealed class AzureOpenAITextToAudioTests
{
    private readonly IConfigurationRoot _configuration = new ConfigurationBuilder()
        .AddJsonFile(path: "testsettings.json", optional: true, reloadOnChange: true)
        .AddJsonFile(path: "testsettings.development.json", optional: true, reloadOnChange: true)
        .AddEnvironmentVariables()
        .AddUserSecrets<AzureOpenAITextToAudioTests>()
        .Build();

    [Fact]
    public async Task AzureOpenAITextToAudioTestAsync()
    {
        // Arrange
        AzureOpenAIConfiguration? azureOpenAIConfiguration = this._configuration.GetSection("AzureOpenAITextToAudio").Get<AzureOpenAIConfiguration>();
        Assert.NotNull(azureOpenAIConfiguration);

        var kernel = Kernel.CreateBuilder()
            .AddAzureOpenAITextToAudio(
                azureOpenAIConfigurat                azureOpenAIConfiguration.DeploymentName,
                azureOpenAIConfiguration.Endpoint,
                azureOpenAIConfiguration.ApiKey)

ration.D                deploymentName: azureOpenAIConfiguration.DeploymentName,
                endpoint: azureOpenAIConfiguration.Endpoint,
                credential: new AzureCliCredential())

ITextToAudioService>();

                azureOpenAIConfiguration.DeploymentName,
                azureOpenAIConfiguration.Endpoint,
                azureOpenAIConfiguration.ApiKey)
            .Build();

        var service = kernel.GetRequiredService<ITextToAudioService>();

        // Act
        var result = await service.GetAudioContentAsync("The sun rises in the east and sets in the west.");

        // Assert
        var audioData = result.Data!.Value;
        Assert.False(audioData.IsEmpty);
    }
}
