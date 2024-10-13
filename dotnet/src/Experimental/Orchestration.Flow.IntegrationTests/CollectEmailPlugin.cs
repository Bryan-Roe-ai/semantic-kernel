﻿// Copyright (c) Microsoft. All rights reserved.

<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
<<<<<<< main
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
<<<<<<< main
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
<<<<<<< main
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
<<<<<<< main
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
<<<<<<< main
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
<<<<<<< HEAD
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
<<<<<<< main
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
<<<<<<< main
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
>>>>>>> head
using System.ComponentModel;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;
using Microsoft.SemanticKernel.Connectors.OpenAI;
using Microsoft.SemanticKernel.Experimental.Orchestration;

namespace SemanticKernel.Experimental.Orchestration.Flow.IntegrationTests;

public sealed partial class CollectEmailPlugin
{
    private const string Goal = "Collect email from user";

    private const string EmailPattern = /*lang=regex*/ @"^([\w\.\-]+)@([\w\-]+)((\.(\w){2,3})+)$";

    private const string SystemPrompt =
        $"""
        I am AI assistant and will only answer questions related to collect email.
        The email should conform to the regex: {EmailPattern}

        If I cannot answer, say that I don't know.
        Do not expose the regex unless asked.
        """;

    private readonly IChatCompletionService _chat;

    private int MaxTokens { get; set; } = 256;

    private readonly PromptExecutionSettings _chatRequestSettings;

    public CollectEmailPlugin(Kernel kernel)
    {
        this._chat = kernel.GetRequiredService<IChatCompletionService>();
        this._chatRequestSettings = new OpenAIPromptExecutionSettings
        {
            MaxTokens = this.MaxTokens,
            StopSequences = ["Observation:"],
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
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
=======
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
=======
using System.Collections.Generic;
>>>>>>> origin/main
using System.ComponentModel;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using Microsoft.SemanticKernel;
<<<<<<< main
using Microsoft.SemanticKernel.ChatCompletion;
using Microsoft.SemanticKernel.Connectors.OpenAI;
using Microsoft.SemanticKernel.Experimental.Orchestration;
=======
using Microsoft.SemanticKernel.AI;
using Microsoft.SemanticKernel.AI.ChatCompletion;
using Microsoft.SemanticKernel.Connectors.AI.OpenAI;
using Microsoft.SemanticKernel.Experimental.Orchestration;
using Microsoft.SemanticKernel.Orchestration;
<<<<<<< div
<<<<<<< div
>>>>>>> origin/main
=======
>>>>>>> main
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> origin/main
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> origin/main
>>>>>>> head

namespace SemanticKernel.Experimental.Orchestration.Flow.IntegrationTests;

public sealed partial class CollectEmailPlugin
{
    private const string Goal = "Collect email from user";

    private const string EmailPattern = /*lang=regex*/ @"^([\w\.\-]+)@([\w\-]+)((\.(\w){2,3})+)$";

    private const string SystemPrompt =
        $"""
        I am AI assistant and will only answer questions related to collect email.
        The email should conform to the regex: {EmailPattern}

        If I cannot answer, say that I don't know.
        Do not expose the regex unless asked.
        """;

    private readonly IChatCompletionService _chat;

    private int MaxTokens { get; set; } = 256;

    private readonly AIRequestSettings _chatRequestSettings;

    public CollectEmailPlugin(IKernel kernel)
    {
<<<<<<< div
<<<<<<< div
<<<<<<< main
        this._chat = kernel.GetRequiredService<IChatCompletionService>();
        this._chatRequestSettings = new OpenAIPromptExecutionSettings
=======
        this._chat = kernel.GetService<IChatCompletion>();
        this._chatRequestSettings = new OpenAIRequestSettings
>>>>>>> main
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
<<<<<<< main
        this._chat = kernel.GetRequiredService<IChatCompletionService>();
        this._chatRequestSettings = new OpenAIPromptExecutionSettings
=======
        this._chat = kernel.GetService<IChatCompletion>();
        this._chatRequestSettings = new OpenAIRequestSettings
>>>>>>> origin/main
=======
<<<<<<< main
        this._chat = kernel.GetRequiredService<IChatCompletionService>();
        this._chatRequestSettings = new OpenAIPromptExecutionSettings
>>>>>>> Stashed changes
=======
<<<<<<< main
        this._chat = kernel.GetRequiredService<IChatCompletionService>();
        this._chatRequestSettings = new OpenAIPromptExecutionSettings
>>>>>>> Stashed changes
>>>>>>> head
        {
            MaxTokens = this.MaxTokens,
            StopSequences = ["Observation:"],
=======
        this._chat = kernel.GetService<IChatCompletion>();
        this._chatRequestSettings = new OpenAIRequestSettings
        {
            MaxTokens = this.MaxTokens,
            StopSequences = new List<string>() { "Observation:" },
>>>>>>> 9cfcc609b1cbe6e1d6975df1d665fa0b064c5624
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
>>>>>>> origin/main
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
<<<<<<< div
>>>>>>> main
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> origin/main
>>>>>>> head
            Temperature = 0
        };
    }

<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
<<<<<<< HEAD
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
=======
<<<<<<< HEAD
>>>>>>> Stashed changes
>>>>>>> head
    [KernelFunction("ConfigureEmailAddress")]
    [Description("Useful to assist in configuration of email address, must be called after email provided")]
    public async Task<string> CollectEmailAsync(
        [Description("The email address provided by the user, pass no matter what the value is")]
        // ReSharper disable once InconsistentNaming
#pragma warning disable CA1707 // Identifiers should not contain underscores
        string email_address,
#pragma warning restore CA1707 // Identifiers should not contain underscores
        KernelArguments arguments)
<<<<<<< div
<<<<<<< div
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
<<<<<<< main
=======
>>>>>>> Stashed changes
>>>>>>> head
=======
<<<<<<< main
=======
>>>>>>> Stashed changes
=======
<<<<<<< main
=======
>>>>>>> Stashed changes
=======
<<<<<<< main
=======
>>>>>>> Stashed changes
=======
<<<<<<< main
=======
>>>>>>> Stashed changes
=======
<<<<<<< div
=======
=======
>>>>>>> head
<<<<<<< main
=======
>>>>>>> Stashed changes
=======
<<<<<<< div
=======
<<<<<<< main
=======
>>>>>>> Stashed changes
>>>>>>> head
    {
        var chat = new ChatHistory(SystemPrompt);
        chat.AddUserMessage(Goal);

        ChatHistory? chatHistory = arguments.GetChatHistory();
        if (chatHistory?.Count > 0)
        {
            chat.AddRange(chatHistory);
        }

        if (!string.IsNullOrEmpty(email_address) && EmailRegex().IsMatch(email_address))
        {
            return "Thanks for providing the info, the following email would be used in subsequent steps: " + email_address;
        }

        // invalid email, prompt user to provide a valid email
        arguments["email_address"] = string.Empty;
        arguments.PromptInput();

        var response = await this._chat.GetChatMessageContentAsync(chat).ConfigureAwait(false);

        return response.Content ?? string.Empty;
    }

#if NET
    [GeneratedRegex(EmailPattern)]
    private static partial Regex EmailRegex();
#else
    private static Regex EmailRegex() => s_emailRegex;
    private static readonly Regex s_emailRegex = new(EmailPattern, RegexOptions.Compiled);
#endif
=======
    [SKFunction]
    [Description("Useful to assist in configuration of email address, must be called after email provided")]
    [SKName("ConfigureEmailAddress")]
    public async Task<string> CollectEmailAsync(
        [SKName("email_address")] [Description("The email address provided by the user, pass no matter what the value is")]
        string email,
        SKContext context)
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
>>>>>>> head
    {
        var chat = new ChatHistory(SystemPrompt);
        chat.AddUserMessage(Goal);

<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
        ChatHistory? chatHistory = arguments.GetChatHistory();
        if (chatHistory?.Count > 0)
=======
        ChatHistory? chatHistory = context.GetChatHistory();
        if (chatHistory?.Any() ?? false)
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
>>>>>>> head
        {
            chat.Messages.AddRange(chatHistory);
        }

<<<<<<< div
<<<<<<< div
=======
<<<<<<< head
>>>>>>> head
        if (!string.IsNullOrEmpty(email_address) && EmailRegex().IsMatch(email_address))
        {
            return "Thanks for providing the info, the following email would be used in subsequent steps: " + email_address;
        }

        // invalid email, prompt user to provide a valid email
        arguments["email_address"] = string.Empty;
        arguments.PromptInput();

        var response = await this._chat.GetChatMessageContentAsync(chat).ConfigureAwait(false);

        return response.Content ?? string.Empty;
    }

#if NET
    [GeneratedRegex(EmailPattern)]
    private static partial Regex EmailRegex();
#else
    private static Regex EmailRegex() => s_emailRegex;
    private static readonly Regex s_emailRegex = new(EmailPattern, RegexOptions.Compiled);
#endif
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
=======
    [SKFunction]
    [Description("Useful to assist in configuration of email address, must be called after email provided")]
    [SKName("ConfigureEmailAddress")]
    public async Task<string> CollectEmailAsync(
        [SKName("email_address")] [Description("The email address provided by the user, pass no matter what the value is")]
        string email,
        SKContext context)
>>>>>>> origin/main
    {
        var chat = new ChatHistory(SystemPrompt);
        chat.AddUserMessage(Goal);

=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< main
        ChatHistory? chatHistory = arguments.GetChatHistory();
        if (chatHistory?.Count > 0)
=======
        ChatHistory? chatHistory = context.GetChatHistory();
        if (chatHistory?.Any() ?? false)
>>>>>>> origin/main
        {
            chat.Messages.AddRange(chatHistory);
        }

<<<<<<< main
        if (!string.IsNullOrEmpty(email_address) && EmailRegex().IsMatch(email_address))
        {
            return "Thanks for providing the info, the following email would be used in subsequent steps: " + email_address;
        }

        // invalid email, prompt user to provide a valid email
        arguments["email_address"] = string.Empty;
        arguments.PromptInput();
=======
        if (!string.IsNullOrEmpty(email) && IsValidEmail(email))
        {
            context.Variables["email_address"] = email;

            return "Thanks for providing the info, the following email would be used in subsequent steps: " + email;
        }

        // invalid email, prompt user to provide a valid email
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
=======
        if (!string.IsNullOrEmpty(email) && IsValidEmail(email))
        {
            context.Variables["email_address"] = email;

            return "Thanks for providing the info, the following email would be used in subsequent steps: " + email;
        }

        // invalid email, prompt user to provide a valid email
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
        context.Variables["email_address"] = string.Empty;
        context.PromptInput();
        return await this._chat.GenerateMessageAsync(chat, this._chatRequestSettings).ConfigureAwait(false);
    }
>>>>>>> origin/main

        var response = await this._chat.GetChatMessageContentAsync(chat).ConfigureAwait(false);

        return response.Content ?? string.Empty;
    }
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
<<<<<<< main

#if NET
    [GeneratedRegex(EmailPattern)]
    private static partial Regex EmailRegex();
#else
    private static Regex EmailRegex() => s_emailRegex;
    private static readonly Regex s_emailRegex = new(EmailPattern, RegexOptions.Compiled);
#endif
=======
>>>>>>> 9cfcc609b1cbe6e1d6975df1d665fa0b064c5624
>>>>>>> origin/main
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
>>>>>>> 9cfcc609b1cbe6e1d6975df1d665fa0b064c5624
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
>>>>>>> 9cfcc609b1cbe6e1d6975df1d665fa0b064c5624
>>>>>>> main
=======
>>>>>>> head
}
