using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Threading.Tasks;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Functions.OpenAPI.Authentication;
using Microsoft.SemanticKernel.Functions.OpenAPI.Extensions;
using Microsoft.SemanticKernel.Orchestration;

using Newtonsoft.Json;
using RepoUtils;

/// <summary>
/// This sample shows how to connect the Semantic Kernel to Jira as an Open Api plugin based on the Open Api schema.
/// This format of registering the plugin and its operations, and subsequently executing those operations can be applied
/// to an Open Api plugin that follows the Open Api Schema.
/// </summary>
// ReSharper disable once InconsistentNaming
public static class Example24_OpenApiPlugin_Jira
{
    public static async Task RunAsync()
    {
        var kernel = new KernelBuilder().WithLoggerFactory(ConsoleLogger.LoggerFactory).Build();
        var contextVariables = new ContextVariables();

        // Change <your-domain> to a jira instance you have access to with your authentication credentials
        string serverUrl = $"https://{TestConfiguration.Jira.Domain}.atlassian.net/rest/api/latest/";
        contextVariables.Set("server-url", serverUrl);

        IDictionary<string, ISKFunction> jiraFunctions;
        var tokenProvider = new BasicAuthenticationProvider(() =>
        {
            string s = $"{TestConfiguration.Jira.Email}:{TestConfiguration.Jira.ApiKey}";
            return Task.FromResult(s);
        });

        using HttpClient httpClient = new();

        // The bool useLocalFile can be used to toggle the ingestion method for the openapi schema between a file path and a URL
        bool useLocalFile = true;
        if (useLocalFile)
        {
            var apiPluginFile = "./../../../Plugins/JiraPlugin/openapi.json";
            jiraFunctions = await kernel.ImportPluginFunctionsAsync("jiraPlugin", apiPluginFile, new OpenApiFunctionExecutionParameters(authCallbackProvider: (_) => tokenProvider.AuthenticateRequestAsync));
        }
        else
        {
            var apiPluginRawFileURL = new Uri("https://raw.githubusercontent.com/microsoft/PowerPlatformConnectors/dev/certified-connectors/JIRA/apiDefinition.swagger.json");
            jiraFunctions = await kernel.ImportPluginFunctionsAsync("jiraPlugin", apiPluginRawFileURL, new OpenApiFunctionExecutionParameters(authCallbackProvider: (_) => tokenProvider.AuthenticateRequestAsync));
        }

        // GetIssue Function
        {
            // Set Properties for the Get Issue operation in the openAPI.swagger.json
            contextVariables.Set("issueKey", "SKTES-2");

            // Run operation via the semantic kernel
            var result = await kernel.RunAsync(contextVariables, jiraFunctions["GetIssue"]);

            Console.WriteLine("\n\n\n");
            var formattedContent = JsonConvert.SerializeObject(JsonConvert.DeserializeObject(result.GetValue<string>()!), Formatting.Indented);
            Console.WriteLine("GetIssue jiraPlugin response: \n{0}", formattedContent);
        }

        // AddComment Function
        {
            // Set Properties for the AddComment operation in the openAPI.swagger.json
            contextVariables.Set("issueKey", "SKTES-1");
            contextVariables.Set("body", "Here is a rad comment");

            // Run operation via the semantic kernel
            var result = await kernel.RunAsync(contextVariables, jiraFunctions["AddComment"]);

            Console.WriteLine("\n\n\n");
            var formattedContent = JsonConvert.SerializeObject(JsonConvert.DeserializeObject(result.GetValue<string>()!), Formatting.Indented);
            Console.WriteLine("AddComment jiraPlugin response: \n{0}", formattedContent);
        }

        // CreateBase64Content Function
        {
            contextVariables.Set("content", Convert.ToBase64String(System.Text.Encoding.UTF8.GetBytes("Sample content")));
            contextVariables.Set("repository", "sample-repo");
            contextVariables.Set("path", "sample-path");

            var result = await kernel.RunAsync(contextVariables, jiraFunctions["createContent"]);

            Console.WriteLine("\n\n\n");
            var formattedContent = JsonConvert.SerializeObject(JsonConvert.DeserializeObject(result.GetValue<string>()!), Formatting.Indented);
            Console.WriteLine("CreateBase64Content jiraPlugin response: \n{0}", formattedContent);
        }

        // ModifyBase64Content Function
        {
            contextVariables.Set("content", Convert.ToBase64String(System.Text.Encoding.UTF8.GetBytes("Updated content")));
            contextVariables.Set("repository", "sample-repo");
            contextVariables.Set("path", "sample-path");

            var result = await kernel.RunAsync(contextVariables, jiraFunctions["modifyContent"]);

            Console.WriteLine("\n\n\n");
            var formattedContent = JsonConvert.SerializeObject(JsonConvert.DeserializeObject(result.GetValue<string>()!), Formatting.Indented);
            Console.WriteLine("ModifyBase64Content jiraPlugin response: \n{0}", formattedContent);
        }

        // DeleteBase64Content Function
        {
            contextVariables.Set("repository", "sample-repo");
            contextVariables.Set("path", "sample-path");

            var result = await kernel.RunAsync(contextVariables, jiraFunctions["deleteContent"]);

            Console.WriteLine("\n\n\n");
            var formattedContent = JsonConvert.SerializeObject(JsonConvert.DeserializeObject(result.GetValue<string>()!), Formatting.Indented);
            Console.WriteLine("DeleteBase64Content jiraPlugin response: \n{0}", formattedContent);
        }
    }

    #region Example of authentication providers

    /// <summary>
    /// Retrieves authentication content (e.g. username/password, API key) via the provided delegate and
    /// applies it to HTTP requests using the "basic" authentication scheme.
    /// </summary>
    public class BasicAuthenticationProvider
    {
        private readonly Func<Task<string>> _credentials;

        /// <summary>
        /// Creates an instance of the <see cref="BasicAuthenticationProvider"/> class.
        /// </summary>
        /// <param name="credentials">Delegate for retrieving credentials.</param>
        public BasicAuthenticationProvider(Func<Task<string>> credentials)
        {
            this._credentials = credentials;
        }

        /// <summary>
        /// Applies the authentication content to the provided HTTP request message.
        /// </summary>
        /// <param name="request">The HTTP request message.</param>
        /// <param name="cancellationToken">The cancellation token.</param>
        public async Task AuthenticateRequestAsync(HttpRequestMessage request, CancellationToken cancellationToken = default)
        {
            // Base64 encode
            string encodedContent = Convert.ToBase64String(Encoding.UTF8.GetBytes(await this._credentials().ConfigureAwait(false)));
            request.Headers.Authorization = new AuthenticationHeaderValue("Basic", encodedContent);
        }
    }

    /// <summary>
    /// Retrieves a token via the provided delegate and applies it to HTTP requests using the
    /// "bearer" authentication scheme.
    /// </summary>
    public class BearerAuthenticationProvider
    {
        private readonly Func<Task<string>> _bearerToken;

        /// <summary>
        /// Creates an instance of the <see cref="BearerAuthenticationProvider"/> class.
        /// </summary>
        /// <param name="bearerToken">Delegate to retrieve the bearer token.</param>
        public BearerAuthenticationProvider(Func<Task<string>> bearerToken)
        {
            this._bearerToken = bearerToken;
        }

        /// <summary>
        /// Applies the token to the provided HTTP request message.
        /// </summary>
        /// <param name="request">The HTTP request message.</param>
        public async Task AuthenticateRequestAsync(HttpRequestMessage request)
        {
            var token = await this._bearerToken().ConfigureAwait(false);
            request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);
        }
    }

    /// <summary>
    /// Uses the Microsoft Authentication Library (MSAL) to authenticate HTTP requests.
    /// </summary>
    public class InteractiveMsalAuthenticationProvider : BearerAuthenticationProvider
    {
        /// <summary>
        /// Creates an instance of the <see cref="InteractiveMsalAuthenticationProvider"/> class.
        /// </summary>
        /// <param name="clientId">Client ID of the caller.</param>
        /// <param name="tenantId">Tenant ID of the target resource.</param>
        /// <param name="scopes">Requested scopes.</param>
        /// <param name="redirectUri">Redirect URI.</param>
        public InteractiveMsalAuthenticationProvider(string clientId, string tenantId, string[] scopes, Uri redirectUri)
            : base(() => GetTokenAsync(clientId, tenantId, scopes, redirectUri))
        {
        }

        /// <summary>
        /// Gets an access token using the Microsoft Authentication Library (MSAL).
        /// </summary>
        /// <param name="clientId">Client ID of the caller.</param>
        /// <param name="tenantId">Tenant ID of the target resource.</param>
        /// <param name="scopes">Requested scopes.</param>
        /// <param name="redirectUri">Redirect URI.</param>
        /// <returns>Access token.</returns>
        private static async Task<string> GetTokenAsync(string clientId, string tenantId, string[] scopes, Uri redirectUri)
        {
            IPublicClientApplication app = PublicClientApplicationBuilder.Create(clientId)
                .WithRedirectUri(redirectUri.ToString())
                .WithTenantId(tenantId)
                .Build();

            IEnumerable<IAccount> accounts = await app.GetAccountsAsync().ConfigureAwait(false);
            AuthenticationResult result;
            try
            {
                result = await app.AcquireTokenSilent(scopes, accounts.FirstOrDefault())
                    .ExecuteAsync().ConfigureAwait(false);
            }
            catch (MsalUiRequiredException)
            {
                // A MsalUiRequiredException happened on AcquireTokenSilent.
                // This indicates you need to call AcquireTokenInteractive to acquire a token
                result = await app.AcquireTokenInteractive(scopes)
                    .ExecuteAsync().ConfigureAwait(false);
            }

            return result.AccessToken;
        }
    }

    /// <summary>
    /// Retrieves authentication content (scheme and value) via the provided delegate and applies it to HTTP requests.
    /// </summary>
    public sealed class CustomAuthenticationProvider
    {
        private readonly Func<Task<string>> _header;
        private readonly Func<Task<string>> _value;

        /// <summary>
        /// Creates an instance of the <see cref="CustomAuthenticationProvider"/> class.
        /// </summary>
        /// <param name="header">Delegate for retrieving the header name.</param>
        /// <param name="value">Delegate for retrieving the value.</param>
        public CustomAuthenticationProvider(Func<Task<string>> header, Func<Task<string>> value)
        {
            this._header = header;
            this._value = value;
        }

        /// <summary>
        /// Applies the header and value to the provided HTTP request message.
        /// </summary>
        /// <param name="request">The HTTP request message.</param>
        public async Task AuthenticateRequestAsync(HttpRequestMessage request)
        {
            var header = await this._header().ConfigureAwait(false);
            var value = await this._value().ConfigureAwait(false);
            request.Headers.Add(header, value);
        }
    }

    #endregion
}
