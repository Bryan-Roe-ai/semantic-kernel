// Copyright (c) Microsoft. All rights reserved.

using System.Text.Json;
using Microsoft.SemanticKernel.Data;
using Microsoft.SemanticKernel.Plugins.Web.Tavily;

namespace Search;

/// <summary>
/// This example shows how to create and use a <see cref="TavilyTextSearch"/>.
/// </summary>
public class Tavily_TextSearch(ITestOutputHelper output) : BaseTest(output)
{
    /// <summary>
    /// Show how to create a <see cref="TavilyTextSearch"/> and use it to perform a text search.
    /// </summary>
    [Fact]
    public async Task UsingTavilyTextSearch()
    {
        // Create a logging handler to output HTTP requests and responses
        LoggingHandler handler = new(new HttpClientHandler(), this.Output);
        using HttpClient httpClient = new(handler);

        // Create an ITextSearch instance using Tavily search
        var textSearch = new TavilyTextSearch(apiKey: TestConfiguration.Tavily.ApiKey, options: new() { HttpClient = httpClient, IncludeRawContent = true });

        var query = "What is the Semantic Kernel?";

        // Search and return results as a string items
        IAsyncEnumerable<string> stringResults = textSearch.SearchAsync(query, 4);
        Console.WriteLine("--- String Results ---\n");
        await foreach (string result in stringResults)
        {
            Console.WriteLine(result);
            WriteHorizontalRule();
        }

        // Search and return results as TextSearchResult items
        IAsyncEnumerable<TextSearchResult> textResults = textSearch.GetTextSearchResultsAsync(query, 4);
        Console.WriteLine("\n--- Text Search Results ---\n");
        await foreach (TextSearchResult result in textResults)
        {
            Console.WriteLine($"Name:  {result.Name}");
            Console.WriteLine($"Value: {result.Value}");
            Console.WriteLine($"Link:  {result.Link}");
            WriteHorizontalRule();
        }

        // Search and return s results as TavilySearchResult items
        IAsyncEnumerable<object> fullResults = textSearch.GetSearchResultsAsync(query, 4);
        Console.WriteLine("\n--- Tavily Web Page Results ---\n");
        await foreach (TavilySearchResult result in fullResults)
        {
            Console.WriteLine($"Name:            {result.Title}");
            Console.WriteLine($"Content:         {result.Content}");
            Console.WriteLine($"Url:             {result.Url}");
            Console.WriteLine($"RawContent:      {result.RawContent}");
            Console.WriteLine($"Score:           {result.Score}");
            WriteHorizontalRule();
        }
    }

    /// <summary>
    /// Show how to create a <see cref="TavilyTextSearch"/> and use it to perform a text search which returns an answer.
    /// </summary>
    [Fact]
    public async Task UsingTavilyTextSearchToGetAnAnswer()
    {
        // Create a logging handler to output HTTP requests and responses
        LoggingHandler handler = new(new HttpClientHandler(), this.Output);
        using HttpClient httpClient = new(handler);

        // Create an ITextSearch instance using Tavily search
        var textSearch = new TavilyTextSearch(apiKey: TestConfiguration.Tavily.ApiKey, options: new() { HttpClient = httpClient, IncludeAnswer = true });

        var query = "What is the Semantic Kernel?";

        // Search and return results as a string items
        IAsyncEnumerable<string> stringResults = textSearch.SearchAsync(query, 1);
        Console.WriteLine("--- String Results ---\n");
        await foreach (string result in stringResults)
        {
            Console.WriteLine(result);
            WriteHorizontalRule();
        }
    }

    /// <summary>
    /// Show how to create a <see cref="TavilyTextSearch"/> and use it to perform a text search.
    /// </summary>
    [Fact]
    public async Task UsingTavilyTextSearchAndIncludeEverything()
    {
        // Create a logging handler to output HTTP requests and responses
        LoggingHandler handler = new(new HttpClientHandler(), this.Output);
        using HttpClient httpClient = new(handler);

        // Create an ITextSearch instance using Tavily search
        var textSearch = new TavilyTextSearch(
            apiKey: TestConfiguration.Tavily.ApiKey,
            options: new()
            {
                HttpClient = httpClient,
                IncludeRawContent = true,
                IncludeImages = true,
                IncludeImageDescriptions = true,
                IncludeAnswer = true,
            });

        var query = "What is the Semantic Kernel?";

        // Search and return s results as TavilySearchResult items
        IAsyncEnumerable<object> fullResults = textSearch.GetSearchResultsAsync(query, 4, new() { Skip = 0 });
        Console.WriteLine("\n--- Tavily Web Page Results ---\n");
        await foreach (TavilySearchResult result in fullResults)
        {
            Console.WriteLine($"Name:            {result.Title}");
            Console.WriteLine($"Content:         {result.Content}");
            Console.WriteLine($"Url:             {result.Url}");
            Console.WriteLine($"RawContent:      {result.RawContent}");
            Console.WriteLine($"Score:           {result.Score}");
            WriteHorizontalRule();
        }
    }

    /// <summary>
    /// Show how to create a <see cref="TavilyTextSearch"/> with a custom mapper and use it to perform a text search.
    /// </summary>
    [Fact]
    public async Task UsingTavilyTextSearchWithACustomMapperAsync()
    {
        // Create a logging handler to output HTTP requests and responses
        LoggingHandler handler = new(new HttpClientHandler(), this.Output);
        using HttpClient httpClient = new(handler);

        // Create an ITextSearch instance using Tavily search
        var textSearch = new TavilyTextSearch(apiKey: TestConfiguration.Tavily.ApiKey, options: new()
        {
            HttpClient = httpClient,
            StringMapper = new TestTextSearchStringMapper(),
        });

        var query = "What is the Semantic Kernel?";

        // Search with TextSearchResult textResult type
        IAsyncEnumerable<string> stringResults = textSearch.SearchAsync(query, 2);
        Console.WriteLine("--- Serialized JSON Results ---");
        await foreach (string result in stringResults)
        {
            Console.WriteLine(result);
            WriteHorizontalRule();
        }
    }

    /// <summary>
    /// Show how to create a <see cref="TavilyTextSearch"/> with a custom mapper and use it to perform a text search.
    /// </summary>
    [Fact]
    public async Task UsingTavilyTextSearchWithAnIncludeDomainFilterAsync()
    {
        // Create a logging handler to output HTTP requests and responses
        LoggingHandler handler = new(new HttpClientHandler(), this.Output);
        using HttpClient httpClient = new(handler);

        // Create an ITextSearch instance using Tavily search
        var textSearch = new TavilyTextSearch(apiKey: TestConfiguration.Tavily.ApiKey, options: new()
        {
            HttpClient = httpClient,
            StringMapper = new TestTextSearchStringMapper(),
        });

        var query = "What is the Semantic Kernel?";

        // Search with TextSearchResult textResult type
        TextSearchOptions searchOptions = new() { Filter = new TextSearchFilter().Equality("include_domain", "devblogs.microsoft.com") };
        IAsyncEnumerable<TextSearchResult> textResults = textSearch.GetTextSearchResultsAsync(query, 4, searchOptions);
        Console.WriteLine("--- Microsoft Developer Blogs Results ---");
        await foreach (TextSearchResult result in textResults)
        {
            Console.WriteLine(result.Link);
            WriteHorizontalRule();
        }
    }

    #region private
    /// <summary>
    /// Test mapper which converts an arbitrary search result to a string using JSON serialization.
    /// </summary>
    private sealed class TestTextSearchStringMapper : ITextSearchStringMapper
    {
        /// <inheritdoc />
        public string MapFromResultToString(object result)
        {
            return JsonSerializer.Serialize(result);
        }
    }
    #endregion
}
