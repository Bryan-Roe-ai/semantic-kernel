<<<<<<< HEAD
<<<<<<< Updated upstream
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
using System;
using System.ClientModel;
using System.ClientModel.Primitives;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Threading;
using Azure.AI.OpenAI;
using Azure.Core;
using Microsoft.SemanticKernel.Http;
using OpenAI;

namespace Microsoft.SemanticKernel.Agents.OpenAI;

/// <summary>
/// Provides an <see cref="OpenAIClient"/> for use by <see cref="OpenAIAssistantAgent"/>.
/// </summary>
public sealed class OpenAIClientProvider
{
    /// <summary>
    /// Avoids an exception from OpenAI Client when a custom endpoint is provided without an API key.
    /// </summary>
    private const string SingleSpaceKey = " ";

    /// <summary>
    /// An active client instance.
    /// </summary>
    public OpenAIClient Client { get; }

    /// <summary>
    /// Configuration keys required for <see cref="AgentChannel"/> management.
    /// </summary>
    internal IReadOnlyList<string> ConfigurationKeys { get; }

    private OpenAIClientProvider(OpenAIClient client, IEnumerable<string> keys)
    {
        this.Client = client;
        this.ConfigurationKeys = keys.ToArray();
    }

    /// <summary>
    /// Produce a <see cref="OpenAIClientProvider"/> based on <see cref="AzureOpenAIClient"/>.
    /// </summary>
    /// <param name="apiKey">The API key</param>
    /// <param name="endpoint">The service endpoint</param>
    /// <param name="httpClient">Custom <see cref="HttpClient"/> for HTTP requests.</param>
    public static OpenAIClientProvider ForAzureOpenAI(ApiKeyCredential apiKey, Uri endpoint, HttpClient? httpClient = null)
    {
        Verify.NotNull(apiKey, nameof(apiKey));
        Verify.NotNull(endpoint, nameof(endpoint));

        AzureOpenAIClientOptions clientOptions = CreateAzureClientOptions(httpClient);

        return new(new AzureOpenAIClient(endpoint, apiKey!, clientOptions), CreateConfigurationKeys(endpoint, httpClient));
    }

    /// <summary>
    /// Produce a <see cref="OpenAIClientProvider"/> based on <see cref="AzureOpenAIClient"/>.
    /// </summary>
    /// <param name="credential">The credentials</param>
    /// <param name="endpoint">The service endpoint</param>
    /// <param name="httpClient">Custom <see cref="HttpClient"/> for HTTP requests.</param>
    public static OpenAIClientProvider ForAzureOpenAI(TokenCredential credential, Uri endpoint, HttpClient? httpClient = null)
    {
        Verify.NotNull(credential, nameof(credential));
        Verify.NotNull(endpoint, nameof(endpoint));

        AzureOpenAIClientOptions clientOptions = CreateAzureClientOptions(httpClient);

        return new(new AzureOpenAIClient(endpoint, credential, clientOptions), CreateConfigurationKeys(endpoint, httpClient));
    }

    /// <summary>
    /// Produce a <see cref="OpenAIClientProvider"/> based on <see cref="OpenAIClient"/>.
    /// </summary>
    /// <param name="endpoint">An optional endpoint</param>
    /// <param name="httpClient">Custom <see cref="HttpClient"/> for HTTP requests.</param>
    public static OpenAIClientProvider ForOpenAI(Uri? endpoint = null, HttpClient? httpClient = null)
    {
        OpenAIClientOptions clientOptions = CreateOpenAIClientOptions(endpoint, httpClient);
<<<<<<< HEAD
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        return new(new OpenAIClient(SingleSpaceKey, clientOptions), CreateConfigurationKeys(endpoint, httpClient));
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
        return new(new OpenAIClient(SingleSpaceKey, clientOptions), CreateConfigurationKeys(endpoint, httpClient));
=======
        return new(new OpenAIClient(new ApiKeyCredential(SingleSpaceKey), clientOptions), CreateConfigurationKeys(endpoint, httpClient));
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
        return new(new OpenAIClient(new ApiKeyCredential(SingleSpaceKey), clientOptions), CreateConfigurationKeys(endpoint, httpClient));
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
    }

    /// <summary>
    /// Produce a <see cref="OpenAIClientProvider"/> based on <see cref="OpenAIClient"/>.
    /// </summary>
    /// <param name="apiKey">The API key</param>
    /// <param name="endpoint">An optional endpoint</param>
    /// <param name="httpClient">Custom <see cref="HttpClient"/> for HTTP requests.</param>
    public static OpenAIClientProvider ForOpenAI(ApiKeyCredential apiKey, Uri? endpoint = null, HttpClient? httpClient = null)
    {
        OpenAIClientOptions clientOptions = CreateOpenAIClientOptions(endpoint, httpClient);
<<<<<<< HEAD
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        return new(new OpenAIClient(apiKey ?? SingleSpaceKey, clientOptions), CreateConfigurationKeys(endpoint, httpClient));
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
        return new(new OpenAIClient(apiKey ?? SingleSpaceKey, clientOptions), CreateConfigurationKeys(endpoint, httpClient));
=======
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
        return new(new OpenAIClient(apiKey ?? SingleSpaceKey, clientOptions), CreateConfigurationKeys(endpoint, httpClient));
=======
>>>>>>> Stashed changes
=======
        return new(new OpenAIClient(apiKey ?? SingleSpaceKey, clientOptions), CreateConfigurationKeys(endpoint, httpClient));
=======
>>>>>>> Stashed changes
<<<<<<< HEAD
        return new(new OpenAIClient(apiKey, clientOptions), CreateConfigurationKeys(endpoint, httpClient));
        return new(new OpenAIClient(apiKey ?? SingleSpaceKey, clientOptions), CreateConfigurationKeys(endpoint, httpClient));
=======
        return new(new OpenAIClient(apiKey, clientOptions), CreateConfigurationKeys(endpoint, httpClient));
>>>>>>> ms/main
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
    }

    /// <summary>
    /// Directly provide a client instance.
    /// </summary>
    public static OpenAIClientProvider FromClient(OpenAIClient client)
    {
        return new(client, [client.GetType().FullName!, client.GetHashCode().ToString()]);
    }

    private static AzureOpenAIClientOptions CreateAzureClientOptions(HttpClient? httpClient)
    {
        AzureOpenAIClientOptions options = new()
        {
<<<<<<< HEAD
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
            ApplicationId = HttpHeaderConstant.Values.UserAgent
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
            ApplicationId = HttpHeaderConstant.Values.UserAgent
=======
            UserAgentApplicationId = HttpHeaderConstant.Values.UserAgent
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
            UserAgentApplicationId = HttpHeaderConstant.Values.UserAgent
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
        };

        ConfigureClientOptions(httpClient, options);

        return options;
    }

    private static OpenAIClientOptions CreateOpenAIClientOptions(Uri? endpoint, HttpClient? httpClient)
    {
        OpenAIClientOptions options = new()
        {
<<<<<<< HEAD
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
            ApplicationId = HttpHeaderConstant.Values.UserAgent,
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
            ApplicationId = HttpHeaderConstant.Values.UserAgent,
=======
            UserAgentApplicationId = HttpHeaderConstant.Values.UserAgent,
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
            UserAgentApplicationId = HttpHeaderConstant.Values.UserAgent,
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
            Endpoint = endpoint ?? httpClient?.BaseAddress,
        };

        ConfigureClientOptions(httpClient, options);

        return options;
    }

    private static void ConfigureClientOptions(HttpClient? httpClient, ClientPipelineOptions options)
    {
        options.AddPolicy(CreateRequestHeaderPolicy(HttpHeaderConstant.Names.SemanticKernelVersion, HttpHeaderConstant.Values.GetAssemblyVersion(typeof(OpenAIAssistantAgent))), PipelinePosition.PerCall);

        if (httpClient is not null)
        {
            options.Transport = new HttpClientPipelineTransport(httpClient);
            options.RetryPolicy = new ClientRetryPolicy(maxRetries: 0); // Disable retry policy if and only if a custom HttpClient is provided.
            options.NetworkTimeout = Timeout.InfiniteTimeSpan; // Disable default timeout
        }
    }

    private static GenericActionPipelinePolicy CreateRequestHeaderPolicy(string headerName, string headerValue)
        =>
            new((message) =>
            {
                if (message?.Request?.Headers?.TryGetValue(headerName, out string? _) == false)
                {
                    message.Request.Headers.Set(headerName, headerValue);
                }
            });

    private static IEnumerable<string> CreateConfigurationKeys(Uri? endpoint, HttpClient? httpClient)
    {
        if (endpoint != null)
        {
            yield return endpoint.ToString();
        }

        if (httpClient is not null)
        {
            if (httpClient.BaseAddress is not null)
            {
                yield return httpClient.BaseAddress.AbsoluteUri;
            }

            foreach (string header in httpClient.DefaultRequestHeaders.SelectMany(h => h.Value))
            {
                yield return header;
            }
        }
    }
}
