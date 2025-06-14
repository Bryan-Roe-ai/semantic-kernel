# Connectors.Memory.SqlServer

This connector uses the SQL Server database engine to implement [Vector Store](https://learn.microsoft.com/semantic-kernel/concepts/vector-store-connectors/?pivots=programming-language-csharp) capability in Semantic Kernel. 

> [!IMPORTANT]  
> The features needed to use this connector are available in preview in Azure SQL only at the moment. Please take a look at the [Public Preview of Native Vector Support in Azure SQL Database](https://devblogs.microsoft.com/azure-sql/exciting-announcement-public-preview-of-native-vector-support-in-azure-sql-database/) for more information.

## Quick start

Create a new .NET console application:

```bash {"id":"01J6KPRBHYWTEEVJ1Q4YNYT197"}
dotnet new console --framework net8.0 -n MySemanticMemoryApp
```

Add the Semantic Kernel packages needed to create a Chatbot:

```bash {"id":"01J6KPRBHYWTEEVJ1Q4ZVP8AMF"}
dotnet add package Microsoft.SemanticKernel
dotnet add package Microsoft.SemanticKernel.Connectors.OpenAI
```

Add `Microsoft.SemanticKernel.Connectors.SqlServer` to give your Chatbot memories:

```bash {"id":"01J6KPRBHYWTEEVJ1Q503BCJ7Z"}
dotnet add package Microsoft.SemanticKernel.Connectors.SqlServer --prerelease
```

Then you can use the following code to create a Chatbot with a memory that uses SQL Server:

```csharp {"id":"01J6KPRBHYWTEEVJ1Q52PMJRDK"}
using System.Text;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;
using Microsoft.SemanticKernel.Connectors.OpenAI;
using Microsoft.SemanticKernel.Connectors.SqlServer;
using Microsoft.SemanticKernel.Memory;

#pragma warning disable SKEXP0001, SKEXP0010, SKEXP0020

// Replace with your Azure OpenAI endpoint
const string AzureOpenAIEndpoint = "https://.openai.azure.com/";

// Replace with your Azure OpenAI API key
const string AzureOpenAIApiKey = "";

// Replace with your Azure OpenAI embedding deployment name
const string EmbeddingModelDeploymentName = "text-embedding-3-small";

// Replace with your Azure OpenAI chat completion deployment name
const string ChatModelDeploymentName = "gpt-4";

// Complete with your Azure SQL connection string
const string ConnectionString = "Data Source=.database.windows.net;Initial Catalog=;Authentication=Active Directory Default;Connection Timeout=30";

// Table where memories will be stored
const string TableName = "ChatMemories";


var kernel = Kernel.CreateBuilder()
    .AddAzureOpenAIChatCompletion(ChatModelDeploymentName, AzureOpenAIEndpoint, AzureOpenAIApiKey)
    .Build();

var memory = new MemoryBuilder()
    .WithSqlServerMemoryStore(ConnectionString, 1536)
    .WithAzureOpenAITextEmbeddingGeneration(EmbeddingModelDeploymentName, AzureOpenAIEndpoint, AzureOpenAIApiKey)
    .Build();

await memory.SaveInformationAsync(TableName, "With the new connector Microsoft.SemanticKernel.Connectors.SqlServer it is possible to efficiently store and retrieve memories thanks to the newly added vector support", "semantic-kernel-mssql");
await memory.SaveInformationAsync(TableName, "At the moment Microsoft.SemanticKernel.Connectors.SqlServer can be used only with Azure SQL", "semantic-kernel-azuresql");
await memory.SaveInformationAsync(TableName, "Azure SQL support for vectors is in Early Adopter Preview.", "azuresql-vector-eap");
await memory.SaveInformationAsync(TableName, "Pizza is one of the favourite food in the world.", "pizza-favourite-food");

var ai = kernel.GetRequiredService<IChatCompletionService>();
var chat = new ChatHistory("You are an AI assistant that helps people find information.");
var builder = new StringBuilder();
while (true)
Here's an example of how to use the SQL Server Vector Store connector in your Semantic Kernel application:

```csharp
/*
    Vector store schema    
*/
public sealed class BlogPost
{
    [VectorStoreRecordKey]
    public int Id { get; set; }

    [VectorStoreRecordData]
    public string? Title { get; set; }

    [VectorStoreRecordData]
    public string? Url { get; set; }

    [VectorStoreRecordData]
    public string? Content { get; set; }

    [VectorStoreRecordVector(Dimensions: 1536)]
    public ReadOnlyMemory<float> ContentEmbedding { get; set; }
}

/*
 * Build the kernel and configure the embedding provider
 */
var builder = Kernel.CreateBuilder();
builder.AddAzureOpenAITextEmbeddingGeneration(AZURE_OPENAI_EMBEDDING_MODEL, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY);
var kernel = builder.Build();

/*
 * Define vector store
 */
var vectorStore = new SqlServerVectorStore(AZURE_SQL_CONNECTION_STRING);

/*
 * Get a collection instance using vector store
 */
var collection = vectorStore.GetCollection<int, BlogPost>("SemanticKernel_VectorStore_BlogPosts");
await collection.CreateCollectionIfNotExistsAsync();

/*
 * Get blog posts to vectorize
 */
var blogPosts = await GetBlogPosts('https://devblogs.microsoft.com/azure-sql/');

/*
 * Generate embeddings for each glossary item
 */
var tasks = blogPosts.Select(b => Task.Run(async () =>
{    
    b.ContentEmbedding = await textEmbeddingGenerationService.GenerateEmbeddingAsync(b.Content);
}));
await Task.WhenAll(tasks);

/*
 * Upsert the data into the vector store
 */
await collection.UpsertBatchAsync(blogPosts);

/*
 * Query the vector store
 */
var searchVector = await textEmbeddingGenerationService.GenerateEmbeddingAsync("How to use vector search in Azure SQL");
var searchResult = await collection.VectorizedSearchAsync(searchVector);
```

You can get a fully working sample using this connector in the following repository:

- [Vector Store sample](https://github.com/Azure-Samples/azure-sql-db-vector-search/tree/main/SemanticKernel/dotnet)


