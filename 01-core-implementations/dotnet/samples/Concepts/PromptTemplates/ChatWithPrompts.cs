// Copyright (c) Microsoft. All rights reserved.

using System.Globalization;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;
using Microsoft.SemanticKernel.Plugins.Core;
using Resources;

namespace PromptTemplates;

/// <summary>
/// Scenario:
///  - the user is reading a wikipedia page, they select a piece of text and they ask AI to extract some information.
///  - the app explicitly uses the Chat model to get a result.
///
/// The following example shows how to:
///
/// - Use the prompt template engine to render prompts, without executing them.
///   This can be used to leverage the template engine (which executes functions internally)
///   to generate prompts and use them programmatically, without executing them like prompt functions.
///
/// - Use rendered prompts to create the context of System and User messages sent to Chat models
///   like "gpt-3.5-turbo"
///
/// Note: normally you would work with Prompt Functions to automatically send a prompt to a model
///       and get a response. In this case we use the Chat model, sending a chat history object, which
///       includes some instructions, some context (the text selected), and the user query.
///
///       We use the prompt template engine to craft the strings with all of this information.
///
///       Out of scope and not in the example: if needed, one could go further and use a semantic
///       function (with extra cost) asking AI to generate the text to send to the Chat model.
/// </summary>
public class ChatWithPrompts(ITestOutputHelper output) : BaseTest(output)
{
    [Fact]
    public async Task RunAsync()
    {
        Console.WriteLine("======== Chat with prompts ========");

        /* Load 3 files:
         * - 30-system-prompt.txt: the system prompt, used to initialize the chat session.
         * - 30-user-context.txt:  the user context, e.g. a piece of a document the user selected and is asking to process.
         * - 30-user-prompt.txt:   the user prompt, just for demo purpose showing that one can leverage the same approach also to augment user messages.
         */

        var systemPromptTemplate = EmbeddedResource.Read("30-system-prompt.txt");
        var selectedText = EmbeddedResource.Read("30-user-context.txt");
        var userPromptTemplate = EmbeddedResource.Read("30-user-prompt.txt");

        Kernel kernel = Kernel.CreateBuilder()
            .AddOpenAIChatCompletion(TestConfiguration.OpenAI.ChatModelId, TestConfiguration.OpenAI.ApiKey, serviceId: "chat")
            .Build();

        // As an example, we import the time plugin, which is used in system prompt to read the current date.
        // We could also use a variable, this is just to show that the prompt can invoke functions.
        kernel.ImportPluginFromType<TimePlugin>("time");

        // Adding required arguments referenced by the prompt templates.
        var arguments = new KernelArguments
        {
            // Put the selected document into the variable used by the system prompt (see 30-system-prompt.txt).
            ["selectedText"] = selectedText,

            // Demo another variable, e.g. when the chat started, used by the system prompt (see 30-system-prompt.txt).
            ["startTime"] = DateTimeOffset.Now.ToString("hh:mm:ss tt zz", CultureInfo.CurrentCulture),

            // This is the user message, store it in the variable used by 30-user-prompt.txt
            ["userMessage"] = "extract locations as a bullet point list"
        };

        // Instantiate the prompt template factory, which we will use to turn prompt templates
        // into strings, that we will store into a Chat history object, which is then sent
        // to the Chat Model.
        var promptTemplateFactory = new KernelPromptTemplateFactory();

        // Render the system prompt. This string is used to configure the chat.
        // This contains the context, ie a piece of a wikipedia page selected by the user.
        string systemMessage = await promptTemplateFactory.Create(new PromptTemplateConfig(systemPromptTemplate)).RenderAsync(kernel, arguments);
        Console.WriteLine($"------------------------------------\n{systemMessage}");

        // Render the user prompt. This string is the query sent by the user
        // This contains the user request, ie "extract locations as a bullet point list"
        string userMessage = await promptTemplateFactory.Create(new PromptTemplateConfig(userPromptTemplate)).RenderAsync(kernel, arguments);
        Console.WriteLine($"------------------------------------\n{userMessage}");

        // Client used to request answers
        var chatCompletion = kernel.GetRequiredService<IChatCompletionService>();

        // The full chat history. Depending on your scenario, you can pass the full chat if useful,
        // or create a new one every time, assuming that the "system message" contains all the
        // information needed.
        var chatHistory = new ChatHistory(systemMessage);

        // Add the user query to the chat history
        chatHistory.AddUserMessage(userMessage);

        // Finally, get the response from AI
        var answer = await chatCompletion.GetChatMessageContentAsync(chatHistory);
        Console.WriteLine($"------------------------------------\n{answer}");

        /*

        Output:

        ------------------------------------
        You are an AI assistant that helps people find information.
        The chat started at: 09:52:12 PM -07
        The current time is: Thursday, April 27, 2023 9:52 PM
        Text selected:
        The central Sahara is hyperarid, with sparse vegetation. The northern and southern reaches of the desert, along with the highlands, have areas of sparse grassland and desert shrub, with trees and taller shrubs in wadis, where moisture collects. In the central, hyperarid region, there are many subdivisions of the great desert: Tanezrouft, the T�n�r�, the Libyan Desert, the Eastern Desert, the Nubian Desert and others. These extremely arid areas often receive no rain for years.
        ------------------------------------
        Thursday, April 27, 2023 2:34 PM: extract locations as a bullet point list
        ------------------------------------
        Sure, here are the locations mentioned in the text:

        - Tanezrouft
        - T�n�r�
        - Libyan Desert
        - Eastern Desert
        - Nubian Desert

        */
    }
}
