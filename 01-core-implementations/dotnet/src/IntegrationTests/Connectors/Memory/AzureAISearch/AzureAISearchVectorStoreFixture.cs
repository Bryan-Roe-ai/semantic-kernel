// Copyright (c) Microsoft. All rights reserved.

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using Azure;
using Azure.AI.OpenAI;
using Azure.Identity;
using Azure.Search.Documents;
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;
using Azure.Search.Documents.Models;
using Microsoft.Extensions.AI;
using Microsoft.Extensions.Configuration;
using Microsoft.SemanticKernel.Data;
using Microsoft.SemanticKernel.Connectors.AzureOpenAI;
using Microsoft.SemanticKernel.Data;
using Microsoft.SemanticKernel.Embeddings;
using SemanticKernel.IntegrationTests.TestSettings;
using Microsoft.Extensions.VectorData;
using SemanticKernel.IntegrationTests.TestSettings;
using SemanticKernel.IntegrationTests.TestSettings.Memory;
using Xunit;

namespace SemanticKernel.IntegrationTests.Connectors.Memory.AzureAISearch;

/// <summary>
/// Helper class for setting up and tearing down Azure AI Search indexes for testing purposes.
/// </summary>
public class AzureAISearchVectorStoreFixture : IAsyncLifetime
{
    /// <summary>
    /// Test index name which consists out of "hotels-" and the machine name with any non-alphanumeric characters removed.
    /// </summary>
    private readonly string _testIndexName = "hotels-" + TestIndexPostfix;

    /// <summary>
    /// Gets the test index name postfix that is derived from the local machine name used to avoid clashes between test runs from different callers.
    /// </summary>
#pragma warning disable CA1308 // Normalize strings to uppercase
    public static string TestIndexPostfix { get; private set; } = new Regex("[^a-zA-Z0-9]").Replace(Environment.MachineName.ToLowerInvariant(), "");
#pragma warning restore CA1308 // Normalize strings to uppercase

    /// <summary>
    /// Test Configuration setup.
    /// </summary>
    private static readonly IConfigurationRoot s_configuration = new ConfigurationBuilder()
        .AddJsonFile(path: "testsettings.json", optional: false, reloadOnChange: true)
        .AddJsonFile(path: "testsettings.development.json", optional: true, reloadOnChange: true)
        .AddEnvironmentVariables()
        .AddUserSecrets<AzureAISearchVectorStoreFixture>()
    private readonly IConfigurationRoot _configuration = new ConfigurationBuilder()
    private static readonly IConfigurationRoot s_configuration = new ConfigurationBuilder()
        .AddJsonFile(path: "testsettings.json", optional: false, reloadOnChange: true)
        .AddJsonFile(path: "testsettings.development.json", optional: true, reloadOnChange: true)
        .AddEnvironmentVariables()
        .AddUserSecrets<AzureAISearchVectorStoreFixture>()
        .Build();

    /// <summary>
    /// Get the test configuration for Azure AI Search.
    /// </summary>
    public static AzureAISearchConfiguration? GetAzureAISearchConfiguration()
    {
        return s_configuration.GetSection("AzureAISearch").Get<AzureAISearchConfiguration>();
        return s_configuration.GetRequiredSection("AzureAISearch").Get<AzureAISearchConfiguration>();
    }

    /// <summary>
    /// Initializes a new instance of the <see cref="AzureAISearchVectorStoreFixture"/> class.
    /// </summary>
    public AzureAISearchVectorStoreFixture()
    {
        var config = s_configuration.GetRequiredSection("AzureAISearch").Get<AzureAISearchConfiguration>();
        
        var config = this._configuration.GetRequiredSection("AzureAISearch").Get<AzureAISearchConfiguration>();
        var config = GetAzureAISearchConfiguration();
        var config = GetAzureAISearchConfiguration();
        Assert.NotNull(config);
        this.Config = config;
        this.SearchIndexClient = new SearchIndexClient(new Uri(config.ServiceUrl), new AzureKeyCredential(config.ApiKey));
        this.VectorStoreRecordDefinition = new VectorStoreCollectionDefinition
        {
            Properties = new List<VectorStoreProperty>
            {
                new VectorStoreKeyProperty("HotelId", typeof(string)),
                new VectorStoreDataProperty("HotelName", typeof(string)) { IsIndexed = true, IsFullTextIndexed = true },
                new VectorStoreDataProperty("Description", typeof(string)),
                new VectorStoreVectorProperty("DescriptionEmbedding", typeof(ReadOnlyMemory<float>?), 1536),
                new VectorStoreDataProperty("Tags", typeof(string[])) { IsIndexed = true },
                new VectorStoreDataProperty("ParkingIncluded", typeof(bool?)) { IsIndexed = true, StorageName = "parking_is_included" },
                new VectorStoreDataProperty("LastRenovationDate", typeof(DateTimeOffset?)) { IsIndexed = true },
                new VectorStoreDataProperty("Rating", typeof(double?))
            }
        };
                new VectorStoreRecordVectorProperty("DescriptionEmbedding", typeof(ReadOnlyMemory<float>?)) { Dimensions = 4 },
                new VectorStoreRecordDataProperty("Tags", typeof(string[])) { IsFilterable = true },
                new VectorStoreRecordDataProperty("ParkingIncluded", typeof(bool?)) { IsFilterable = true },
                new VectorStoreRecordDataProperty("LastRenovationDate", typeof(DateTimeOffset?)) { IsFilterable = true },
                new VectorStoreRecordDataProperty("Rating", typeof(float?))
            }
        };
        AzureOpenAIConfiguration? embeddingsConfig = s_configuration.GetSection("AzureOpenAIEmbeddings").Get<AzureOpenAIConfiguration>();
        Assert.NotNull(embeddingsConfig);
        Assert.NotEmpty(embeddingsConfig.DeploymentName);
        Assert.NotEmpty(embeddingsConfig.Endpoint);

        this.EmbeddingGenerator = new AzureOpenAIClient(new Uri(embeddingsConfig.Endpoint), new AzureCliCredential())
            .GetEmbeddingClient(embeddingsConfig.DeploymentName)
            .AsIEmbeddingGenerator();
    }

    /// <summary>
    /// Gets the Search Index Client to use for connecting to the Azure AI Search service.
    /// </summary>
    public SearchIndexClient SearchIndexClient { get; private set; }

    /// <summary>
    /// Gets the name of the index that this fixture sets up and tears down.
    /// </summary>
    public string TestIndexName { get => this._testIndexName; }

    /// <summary>
    /// Gets the manually created vector store record definition for our test model.
    /// </summary>
    public VectorStoreCollectionDefinition VectorStoreRecordDefinition { get; private set; }

    /// <summary>
    /// Gets the configuration for the Azure AI Search service.
    /// </summary>
    public AzureAISearchConfiguration Config { get; private set; }

    /// <summary>
    /// Gets the embedding generator to use for generating embeddings for text.
    /// </summary>
    public IEmbeddingGenerator<string, Embedding<float>> EmbeddingGenerator { get; private set; }

    /// <summary>
    /// Gets the embedding used for all test documents that the collection is seeded with.
    /// </summary>
    public ReadOnlyMemory<float> Embedding { get; private set; }

    /// <summary>
    /// Create / Recreate index and upload documents before test run.
    /// </summary>
    /// <returns>An async task.</returns>
    public async Task InitializeAsync()
    {
        await AzureAISearchVectorStoreFixture.DeleteIndexIfExistsAsync(this._testIndexName, this.SearchIndexClient);
        await AzureAISearchVectorStoreFixture.CreateIndexAsync(this._testIndexName, this.SearchIndexClient);
        AzureAISearchVectorStoreFixture.UploadDocuments(this.SearchIndexClient.GetSearchClient(this._testIndexName));
        AzureAISearchVectorStoreFixture.UploadDocuments(this.SearchIndexClient.GetSearchClient(this._testIndexName));
await AzureAISearchVectorStoreFixture.UploadDocumentsAsync(this.SearchIndexClient.GetSearchClient(this._testIndexName));
        AzureAISearchVectorStoreFixture.UploadDocuments(this.SearchIndexClient.GetSearchClient(this._testIndexName));
        await AzureAISearchVectorStoreFixture.UploadDocumentsAsync(this.SearchIndexClient.GetSearchClient(this._testIndexName), this.EmbeddingGenerator);
        await AzureAISearchVectorStoreFixture.UploadDocumentsAsync(this.SearchIndexClient.GetSearchClient(this._testIndexName));
        AzureAISearchVectorStoreFixture.UploadDocuments(this.SearchIndexClient.GetSearchClient(this._testIndexName));
        await AzureAISearchVectorStoreFixture.UploadDocumentsAsync(this.SearchIndexClient.GetSearchClient(this._testIndexName), this.EmbeddingGenerator);
        await AzureAISearchVectorStoreFixture.UploadDocumentsAsync(this.SearchIndexClient.GetSearchClient(this._testIndexName), this.EmbeddingGenerator);
        await this.UploadDocumentsAsync(this.SearchIndexClient.GetSearchClient(this._testIndexName), this.EmbeddingGenerator);
    }

    /// <summary>
    /// Delete the index after the test run.
    /// </summary>
    /// <returns>An async task.</returns>
    public async Task DisposeAsync()
    {
        await AzureAISearchVectorStoreFixture.DeleteIndexIfExistsAsync(this._testIndexName, this.SearchIndexClient);
    }

    /// <summary>
    /// Delete the index if it exists.
    /// </summary>
    /// <param name="indexName">The name of the index to delete.</param>
    /// <param name="adminClient">The search index client to use for deleting the index.</param>
    /// <returns>An async task.</returns>
    public static async Task DeleteIndexIfExistsAsync(string indexName, SearchIndexClient adminClient)
    {
        adminClient.GetIndexNames();
        {
            await adminClient.DeleteIndexAsync(indexName);
        }
    }

    /// <summary>
    /// Create an index with the given name.
    /// </summary>
    /// <param name="indexName">The name of the index to create.</param>
    /// <param name="adminClient">The search index client to use for creating the index.</param>
    /// <returns>An async task.</returns>
    public static async Task CreateIndexAsync(string indexName, SearchIndexClient adminClient)
    {
        AzureOpenAIConfiguration openAIConfiguration = s_configuration.GetRequiredSection("AzureOpenAIEmbeddings").Get<AzureOpenAIConfiguration>()!;

        // Build the list of fields from the model, and then replace the DescriptionEmbedding field with a vector field, to work around
        // issue where the field is not recognized as an array on parsing on the server side when apply the VectorSearchFieldAttribute.
        FieldBuilder fieldBuilder = new();
        var searchFields = fieldBuilder.Build(typeof(AzureAISearchHotel));
        var embeddingfield = searchFields.First(x => x.Name == "DescriptionEmbedding");
        searchFields.Remove(embeddingfield);
        searchFields.Add(new VectorSearchField("DescriptionEmbedding", 1536, "my-vector-profile"));

        // Create an index definition with a vectorizer to use when doing vector searches using text.
        var definition = new SearchIndex(indexName, searchFields)
        {
            VectorSearch = new VectorSearch()
        };
        definition.VectorSearch.Vectorizers.Add(new AzureOpenAIVectorizer("text-embedding-vectorizer")
        {
            Parameters = new AzureOpenAIVectorizerParameters
            {
                ResourceUri = new Uri(openAIConfiguration.Endpoint),
                DeploymentName = openAIConfiguration.DeploymentName,
                ApiKey = openAIConfiguration.ApiKey,
                ModelName = openAIConfiguration.EmbeddingModelId
            }
        });
        definition.VectorSearch.Algorithms.Add(new HnswAlgorithmConfiguration("my-hnsw-vector-config-1") { Parameters = new HnswParameters { Metric = VectorSearchAlgorithmMetric.Cosine } });
        definition.VectorSearch.Profiles.Add(new VectorSearchProfile("my-vector-profile", "my-hnsw-vector-config-1") { VectorizerName = "text-embedding-vectorizer" });
        searchFields.Add(new VectorSearchField("DescriptionEmbedding", 1536, "my-vector-profile"));

        // Create an index definition with a vectorizer to use when doing vector searches using text.
        var definition = new SearchIndex(indexName, searchFields);
        definition.VectorSearch = new VectorSearch();
        definition.VectorSearch.Vectorizers.Add(new AzureOpenAIVectorizer("text-embedding-vectorizer")
        {
            Parameters = new AzureOpenAIVectorizerParameters
            {
                ResourceUri = new Uri(openAIConfiguration.Endpoint),
                DeploymentName = openAIConfiguration.DeploymentName,
                ApiKey = openAIConfiguration.ApiKey,
                ModelName = openAIConfiguration.EmbeddingModelId
            }
        });
        definition.VectorSearch.Algorithms.Add(new HnswAlgorithmConfiguration("my-hnsw-vector-config-1") { Parameters = new HnswParameters { Metric = VectorSearchAlgorithmMetric.Cosine } });
        definition.VectorSearch.Profiles.Add(new VectorSearchProfile("my-vector-profile", "my-hnsw-vector-config-1") { VectorizerName = "text-embedding-vectorizer" });

        var suggester = new SearchSuggester("sg", new[] { "HotelName" });
        definition.Suggesters.Add(suggester);

        await adminClient.CreateOrUpdateIndexAsync(definition);
    }

    /// <summary>
    /// Upload test documents to the index.
    /// </summary>
    /// <param name="searchClient">The client to use for uploading the documents.</param>
    public static async Task UploadDocumentsAsync(SearchClient searchClient)
    /// <param name="embeddingGenerator">An instance of <see cref="ITextEmbeddingGenerationService"/> to generate embeddings.</param>
    public static async Task UploadDocumentsAsync(SearchClient searchClient, ITextEmbeddingGenerationService embeddingGenerator)
    /// <param name="embeddingGenerator">An instance of <see cref="IEmbeddingGenerator"/> to generate embeddings.</param>
    public async Task UploadDocumentsAsync(SearchClient searchClient, IEmbeddingGenerator<string, Embedding<float>> embeddingGenerator)
    {
        this.Embedding = (await embeddingGenerator.GenerateAsync("This is a great hotel")).Vector;

    public static void UploadDocuments(SearchClient searchClient)
    /// <param name="embeddingGenerator">An instance of <see cref="ITextEmbeddingGenerationService"/> to generate embeddings.</param>
    public static async Task UploadDocumentsAsync(SearchClient searchClient, ITextEmbeddingGenerationService embeddingGenerator)
    {
        var embedding = await embeddingGenerator.GenerateEmbeddingAsync("This is a great hotel");

        IndexDocumentsBatch<Hotel> batch = IndexDocumentsBatch.Create(
        IndexDocumentsBatch<AzureAISearchHotel> batch = IndexDocumentsBatch.Create(
                  IndexDocumentsAction.Upload(
                new AzureAISearchHotel()
                {
                    HotelId = "BaseSet-1",
                    HotelName = "Hotel 1",
                    Description = "This is a great hotel",
                    DescriptionEmbedding = embedding,
                    DescriptionEmbedding = new[] { 30f, 31f, 32f, 33f },
                    DescriptionEmbedding = this.Embedding,
                    Tags = new[] { "pool", "air conditioning", "concierge" },
                    ParkingIncluded = false,
                    LastRenovationDate = new DateTimeOffset(1970, 1, 18, 0, 0, 0, TimeSpan.Zero),
                    Rating = 3.6
                }),
            IndexDocumentsAction.Upload(
                new AzureAISearchHotel()
                {
                    HotelId = "BaseSet-2",
                    HotelName = "Hotel 2",
                    Description = "This is a great hotel",
                    DescriptionEmbedding = embedding,
                    DescriptionEmbedding = new[] { 30f, 31f, 32f, 33f },
                    DescriptionEmbedding = this.Embedding,
                    Tags = new[] { "pool", "free wifi", "concierge" },
                    ParkingIncluded = false,
                    LastRenovationDate = new DateTimeOffset(1979, 2, 18, 0, 0, 0, TimeSpan.Zero),
                    Rating = 3.60
                }),
            IndexDocumentsAction.Upload(
                new AzureAISearchHotel()
                {
                    HotelId = "BaseSet-3",
                    HotelName = "Hotel 3",
                    Description = "This is a great hotel",
                    DescriptionEmbedding = embedding,
                    DescriptionEmbedding = new[] { 30f, 31f, 32f, 33f },
                    DescriptionEmbedding = this.Embedding,
                    Tags = new[] { "air conditioning", "bar", "continental breakfast" },
                    ParkingIncluded = true,
                    LastRenovationDate = new DateTimeOffset(2015, 9, 20, 0, 0, 0, TimeSpan.Zero),
                    Rating = 4.80
                }),
            IndexDocumentsAction.Upload(
                new AzureAISearchHotel()
                {
                    HotelId = "BaseSet-4",
                    HotelName = "Hotel 4",
                    Description = "This is a great hotel",
                    DescriptionEmbedding = embedding,
                    DescriptionEmbedding = new[] { 30f, 31f, 32f, 33f },
                    DescriptionEmbedding = this.Embedding,
                    Tags = new[] { "concierge", "view", "24-hour front desk service" },
                    ParkingIncluded = true,
                    LastRenovationDate = new DateTimeOffset(1960, 2, 06, 0, 0, 0, TimeSpan.Zero),
                    Rating = 4.60
                })
            );

        await searchClient.IndexDocumentsAsync(batch);

        // Add some delay to allow time for the documents to get indexed and show up in search.
        await Task.Delay(5000);
    }

    /// <summary>
    /// Create a test embedding.
    /// </summary>
    /// <returns>The test embedding.</returns>
    public static float[] CreateTestEmbedding()
    {
        return Enumerable.Range(1, 1536).Select(x => (float)x).ToArray();
        searchClient.IndexDocuments(batch);
    }

#pragma warning disable CS8618 // Non-nullable field must contain a non-null value when exiting constructor. Consider declaring as nullable.
    public class Hotel
    {
        [SimpleField(IsKey = true, IsFilterable = true)]
        [VectorStoreRecordKey]
        public string HotelId { get; set; }

        [SearchableField(IsFilterable = true, IsSortable = true)]
        [VectorStoreRecordData(IsFilterable = true, IsFullTextSearchable = true)]
        public string HotelName { get; set; }

        [SearchableField(AnalyzerName = LexicalAnalyzerName.Values.EnLucene)]
        [VectorStoreRecordData]
        public string Description { get; set; }

        [VectorStoreRecordVector(1536)]
        public ReadOnlyMemory<float>? DescriptionEmbedding { get; set; }

        [SearchableField(IsFilterable = true, IsFacetable = true)]
        [VectorStoreRecordData(IsFilterable = true)]
#pragma warning disable CA1819 // Properties should not return arrays
        public string[] Tags { get; set; }
#pragma warning restore CA1819 // Properties should not return arrays

        [JsonPropertyName("parking_is_included")]
        [SimpleField(IsFilterable = true, IsSortable = true, IsFacetable = true)]
        [VectorStoreRecordData(IsFilterable = true)]
        public bool? ParkingIncluded { get; set; }

        [SimpleField(IsFilterable = true, IsSortable = true, IsFacetable = true)]
        [VectorStoreRecordData(IsFilterable = true)]
        public DateTimeOffset? LastRenovationDate { get; set; }

        [SimpleField(IsFilterable = true, IsSortable = true, IsFacetable = true)]
        [VectorStoreRecordData]
        public double? Rating { get; set; }
    }
#pragma warning restore CS8618 // Non-nullable field must contain a non-null value when exiting constructor. Consider declaring as nullable.
}
