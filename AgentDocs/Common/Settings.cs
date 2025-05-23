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
    private TaskGeneratorSettings taskGenerator;
    private GeneralSettings general;
    private SecuritySettings security; // Pd25f
    private AdditionalServicesSettings additionalServices; // P045d
    private OpenIDConnectSettings openIDConnect; // P174c

    public AzureOpenAISettings AzureOpenAI => this.azureOpenAI ??= this.GetSettings<Settings.AzureOpenAISettings>();
    public OpenAISettings OpenAI => this.openAI ??= this.GetSettings<Settings.OpenAISettings>();
    public MongoDBSettings MongoDB => this.mongoDB ??= this.GetSettings<Settings.MongoDBSettings>();
    public AzureBlobStorageSettings AzureBlobStorage => this.azureBlobStorage ??= this.GetSettings<Settings.AzureBlobStorageSettings>();
    public AzureCognitiveServicesSettings AzureCognitiveServices => this.azureCognitiveServices ??= this.GetSettings<Settings.AzureCognitiveServicesSettings>();
    public AzureFunctionsSettings AzureFunctions => this.azureFunctions ??= this.GetSettings<Settings.AzureFunctionsSettings>();
    public CosmosDBSettings CosmosDB => this.cosmosDB ??= this.GetSettings<Settings.CosmosDBSettings>();
    public KeyVaultSettings KeyVault => this.keyVault ??= this.GetSettings<Settings.KeyVaultSettings>();
    public AzureDevOpsSettings AzureDevOps => this.azureDevOps ??= this.GetSettings<Settings.AzureDevOpsSettings>();
    public TaskGeneratorSettings TaskGenerator => this.taskGenerator ??= this.GetSettings<Settings.TaskGeneratorSettings>();
    public GeneralSettings General => this.general ??= this.GetSettings<Settings.GeneralSettings>();
    public SecuritySettings Security => this.security ??= this.GetSettings<Settings.SecuritySettings>(); // Pd25f
    public AdditionalServicesSettings AdditionalServices => this.additionalServices ??= this.GetSettings<Settings.AdditionalServicesSettings>(); // P045d
    public OpenIDConnectSettings OpenIDConnect => this.openIDConnect ??= this.GetSettings<Settings.OpenIDConnectSettings>(); // P174c

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
        public string ApiKey { get; set; } = string.Empty;
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

    public class TaskGeneratorSettings
    {
        public string Endpoint { get; set; } = string.Empty;
        public string ApiKey { get; set; } = string.Empty;
        public string Topic { get; set; } = string.Empty;
        public string DifficultyLevel { get; set; } = string.Empty;
        public string TaskType { get; set; } = string.Empty;
    }

    public class GeneralSettings
    {
        public string ApiKey { get; set; } = string.Empty;
        public string DatabaseUrl { get; set; } = string.Empty;
        public string SecretKey { get; set; } = string.Empty;
    }

    public class SecuritySettings // Pd25f
    {
        public string[] AllowedDomains { get; set; } = Array.Empty<string>();
        public RateLimitSettings RateLimit { get; set; } = new RateLimitSettings();
        public CorsPolicySettings CorsPolicy { get; set; } = new CorsPolicySettings();

        public class RateLimitSettings
        {
            public int WindowMs { get; set; } = 60000;
            public int MaxRequests { get; set; } = 100;
        }

        public class CorsPolicySettings
        {
            public string[] AllowedOrigins { get; set; } = Array.Empty<string>();
            public string[] AllowedMethods { get; set; } = Array.Empty<string>();
            public string[] AllowedHeaders { get; set; } = Array.Empty<string>();
        }
    }

    public class AdditionalServicesSettings // P045d
    {
        public AzureCognitiveServicesSettings AzureCognitiveServices { get; set; } = new AzureCognitiveServicesSettings();
        public AzureBlobStorageSettings AzureBlobStorage { get; set; } = new AzureBlobStorageSettings();
        public CosmosDBSettings CosmosDB { get; set; } = new CosmosDBSettings();
    }

    public class OpenIDConnectSettings // P174c
    {
        public string ClientId { get; set; } = string.Empty;
        public string ClientSecret { get; set; } = string.Empty;
        public string Scopes { get; set; } = "openid profile";
        public string ProviderUrl { get; set; } = "https://huggingface.co";
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
