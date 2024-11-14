// Copyright (c) Microsoft. All rights reserved.

using System.Reflection;
using Microsoft.Extensions.Configuration;

namespace AgentsSample;

public class Settings
{
    private readonly IConfigurationRoot configRoot;

    private AzureOpenAISettings azureOpenAI;
    private OpenAISettings openAI;
    private MongoDBSettings mongoDB;
    private AzureBlobStorageSettings azureBlobStorage;
    private AzureCognitiveServicesSettings azureCognitiveServices;
    private AzureFunctionsSettings azureFunctions;
    private CosmosDBSettings cosmosDB;
    private KeyVaultSettings keyVault;
    private AzureDevOpsSettings azureDevOps;

    public AzureOpenAISettings AzureOpenAI => this.azureOpenAI ??= this.GetSettings<Settings.AzureOpenAISettings>();
    public OpenAISettings OpenAI => this.openAI ??= this.GetSettings<Settings.OpenAISettings>();
    public MongoDBSettings MongoDB => this.mongoDB ??= this.GetSettings<Settings.MongoDBSettings>();
    public AzureBlobStorageSettings AzureBlobStorage => this.azureBlobStorage ??= this.GetSettings<Settings.AzureBlobStorageSettings>();
    public AzureCognitiveServicesSettings AzureCognitiveServices => this.azureCognitiveServices ??= this.GetSettings<Settings.AzureCognitiveServicesSettings>();
    public AzureFunctionsSettings AzureFunctions => this.azureFunctions ??= this.GetSettings<Settings.AzureFunctionsSettings>();
    public CosmosDBSettings CosmosDB => this.cosmosDB ??= this.GetSettings<Settings.CosmosDBSettings>();
    public KeyVaultSettings KeyVault => this.keyVault ??= this.GetSettings<Settings.KeyVaultSettings>();
    public AzureDevOpsSettings AzureDevOps => this.azureDevOps ??= this.GetSettings<Settings.AzureDevOpsSettings>();

    public class OpenAISettings
    {
        public string ChatModel { get; set; } = string.Empty;
        public string ApiKey { get; set; } = string.Empty;
    }

    public class AzureOpenAISettings
    {
        public string ChatModelDeployment { get; set; } = string.Empty;
        public string Endpoint { get; set; } = string.Empty;
        public string ApiKey { get; set; } = string.Empty;
    }

    public class MongoDBSettings
    {
        public string ConnectionString { get; set; } = string.Empty;
        public string DatabaseName { get; set; } = string.Empty;
        public bool DirectConnection { get; set; } = false;
    }

    public class AzureBlobStorageSettings
    {
        public string Endpoint { get; set; } = string.Empty;
    }

    public class AzureCognitiveServicesSettings
    {
        public string Endpoint { get; set; } = string.Empty;
    }

    public class AzureFunctionsSettings
    {
        public string Endpoint { get; set; } = string.Empty;
    }

    public class CosmosDBSettings
    {
        public string Endpoint { get; set; } = string.Empty;
    }

    public class KeyVaultSettings
    {
        public string Endpoint { get; set; } = string.Empty;
    }

    public class AzureDevOpsSettings
    {
        public string OrganizationUrl { get; set; } = string.Empty;
    }

    private TSettings GetSettings<TSettings>() =>
        this.configRoot.GetRequiredSection(typeof(TSettings).Name).Get<TSettings>()!;

    public Settings()
    {
        this.configRoot =
            new ConfigurationBuilder()
                .AddJsonFile("appsettings.json", optional: true, reloadOnChange: true)
                .AddJsonFile("appsettings.Development.json", optional: true, reloadOnChange: true)
                .AddEnvironmentVariables()
                .AddUserSecrets(Assembly.GetExecutingAssembly(), optional: true)
                .Build();
    }
}
