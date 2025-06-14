// Copyright (c) Microsoft. All rights reserved.

using System.ClientModel;
using Azure.Identity;
using Events;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging.Abstractions;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Agents;
using Microsoft.SemanticKernel.Agents.Chat;
using Microsoft.SemanticKernel.Agents.OpenAI;
using Microsoft.SemanticKernel.ChatCompletion;
using Microsoft.SemanticKernel.Connectors.OpenAI;
using OpenAI;
using SharedSteps;
using Step04.Plugins;
using Step04.Steps;

namespace Step04;

/// <summary>
/// Demonstrate creation of a <see cref="KernelProcess"/> that orchestrates an <see cref="Agent"/> conversation.
/// For visual reference of the process check <see href="https://github.com/microsoft/semantic-kernel/tree/main/dotnet/samples/GettingStartedWithProcesses/README.md#step04_agentorchestration" >diagram</see>.
/// </summary>
public class Step04_AgentOrchestration : BaseTest
{
    public Step04_AgentOrchestration(ITestOutputHelper output) : base(output, redirectSystemConsoleOutput: true)
    {
        this.Client =
    this.UseOpenAIConfig ?
        OpenAIAssistantAgent.CreateOpenAIClient(new ApiKeyCredential(this.ApiKey ?? throw new ConfigurationNotFoundException("OpenAI:ApiKey"))) :
        !string.IsNullOrWhiteSpace(this.ApiKey) ?
            OpenAIAssistantAgent.CreateAzureOpenAIClient(new ApiKeyCredential(this.ApiKey), new Uri(this.Endpoint!)) :
            OpenAIAssistantAgent.CreateAzureOpenAIClient(new AzureCliCredential(), new Uri(this.Endpoint!));
    }

    protected OpenAIClient Client { get; init; }

    // Target Open AI Services
    protected override bool ForceOpenAI => true;

    /// <summary>
    /// Orchestrates a single agent gathering user input and then delegating to a group of agents.
    /// The group of agents provide a response back to the single agent who continues to
    /// interact with the user.
    /// </summary>
    [Fact]
    public async Task DelegatedGroupChatAsync()
    {
        // Define process
        KernelProcess process = SetupAgentProcess<BasicAgentChatUserInput>(nameof(DelegatedGroupChatAsync));

        // Execute process
        await RunProcessAsync(process);
    }

    [Fact]
    public async Task SingleTeacherStudentAgentCallAsync()
    {
        // Define process
        KernelProcess process = SetupSingleAgentProcess<BasicTeacherAgentInput>(nameof(SingleTeacherStudentAgentCallAsync));

        // Setup kernel with OpenAI Client
        Kernel kernel = SetupKernel();

        // Execute process
        await using LocalKernelProcessContext localProcess =
            await process.StartAsync(
                kernel,
                new KernelProcessEvent()
                {
                    Id = AgentOrchestrationEvents.StartProcess
                });

        // Cleaning up created agents
        var processState = await localProcess.GetStateAsync();
        var agentState = (KernelProcessStepState<KernelProcessAgentExecutorState>)processState.Steps.Where(step => step.State.StepId == "Student").FirstOrDefault()!.State;
        var agentId = agentState?.State?.AgentId;
        if (agentId != null)
        {
            await this.Client.GetAssistantClient().DeleteAssistantAsync(agentId);
        }
    }

    private sealed class BasicAgentChatUserInput : ScriptedUserInputStep
    {
        public BasicAgentChatUserInput()
        {
            this.SuppressOutput = true;
        }

        public override void PopulateUserInputs(UserInputState state)
        {
            state.UserInputs.Add("Hi");
            state.UserInputs.Add("List the upcoming events on my calendar for the next week");
            state.UserInputs.Add("Correct");
            state.UserInputs.Add("When is an open time to go camping near home for 4 days after the end of this week?");
            state.UserInputs.Add("Yes, and I'd prefer nice weather.");
            state.UserInputs.Add("Sounds good, add the soonest option without conflicts to my calendar");
            state.UserInputs.Add("Correct");
            state.UserInputs.Add("That's all, thank you");
        }
    }

    private sealed class BasicTeacherAgentInput : ScriptedUserInputStep
    {
        public BasicTeacherAgentInput()
        {
            this.SuppressOutput = true;
        }

        public override void PopulateUserInputs(UserInputState state)
        {
            state.UserInputs.Add("What is 2+2");
            state.UserInputs.Add("What is 2+2");
            state.UserInputs.Add("What is the name of a shape with 3 consecutive sides");
            state.UserInputs.Add("What is the internal angle of a square");
            state.UserInputs.Add("What is a parallellogram");
        }
    }

    private async Task RunProcessAsync(KernelProcess process)
    {
        // Initialize services
        ChatHistory history = [];
        Kernel kernel = SetupKernel(history);

        // Execute process
        await using LocalKernelProcessContext localProcess =
            await process.StartAsync(
                kernel,
                new KernelProcessEvent()
                {
                    Id = AgentOrchestrationEvents.StartProcess
                });

        // Demonstrate history is maintained independent of process state
        this.WriteHorizontalRule();
        foreach (ChatMessageContent message in history)
        {
            RenderMessageStep.Render(message);
        }
    }

    private KernelProcess SetupSingleAgentProcess<TUserInputStep>(string processName) where TUserInputStep : ScriptedUserInputStep
    {
        ProcessBuilder process = new(processName);

        var userInputStep = process.AddStepFromType<TUserInputStep>();
        var renderMessageStep = process.AddStepFromType<RenderMessageStep>();
        var agentStep = process.AddStepFromAgent(new()
        {
            Name = "Student",
            // On purpose not assigning AgentId, if not provided a new agent is created
            Description = "Solves problem given",
            Instructions = "Solve the problem given, if the question is repeated mention something like I already answered but here is the answer with a bit of humor",
            Model = new()
            {
                Id = "gpt-4o",
            },
            Type = OpenAIAssistantAgentFactory.OpenAIAssistantAgentType,
        });

        // Entry point
        process.OnInputEvent(AgentOrchestrationEvents.StartProcess)
            .SendEventTo(new(userInputStep));

        // Pass user input to primary agent
        userInputStep
            .OnEvent(CommonEvents.UserInputReceived)
            .SendEventTo(new ProcessFunctionTargetBuilder(agentStep))
            .SendEventTo(new ProcessFunctionTargetBuilder(renderMessageStep, RenderMessageStep.ProcessStepFunctions.RenderUserText));

        agentStep
            .OnFunctionResult()
            .SendEventTo(new ProcessFunctionTargetBuilder(userInputStep))
            .SendEventTo(new ProcessFunctionTargetBuilder(renderMessageStep, RenderMessageStep.ProcessStepFunctions.RenderMessage));

        agentStep
            .OnFunctionError()
            .SendEventTo(new ProcessFunctionTargetBuilder(renderMessageStep, RenderMessageStep.ProcessStepFunctions.RenderError))
            .StopProcess();

        return process.Build();
    }

    private KernelProcess SetupAgentProcess<TUserInputStep>(string processName) where TUserInputStep : ScriptedUserInputStep
    {
        ProcessBuilder process = new(processName);

        var userInputStep = process.AddStepFromType<TUserInputStep>();
        var renderMessageStep = process.AddStepFromType<RenderMessageStep>();
        var managerAgentStep = process.AddStepFromType<ManagerAgentStep>();
        var agentGroupStep = process.AddStepFromType<AgentGroupChatStep>();

        AttachErrorStep(
            userInputStep,
            ScriptedUserInputStep.ProcessStepFunctions.GetUserInput);

        AttachErrorStep(
            managerAgentStep,
            ManagerAgentStep.ProcessStepFunctions.InvokeAgent,
            ManagerAgentStep.ProcessStepFunctions.InvokeGroup,
            ManagerAgentStep.ProcessStepFunctions.ReceiveResponse);

        AttachErrorStep(
            agentGroupStep,
            AgentGroupChatStep.ProcessStepFunctions.InvokeAgentGroup);

        // Entry point
        process.OnInputEvent(AgentOrchestrationEvents.StartProcess)
            .SendEventTo(new ProcessFunctionTargetBuilder(userInputStep));

        // Pass user input to primary agent
        userInputStep
            .OnEvent(CommonEvents.UserInputReceived)
            .SendEventTo(new ProcessFunctionTargetBuilder(managerAgentStep, ManagerAgentStep.ProcessStepFunctions.InvokeAgent))
            .SendEventTo(new ProcessFunctionTargetBuilder(renderMessageStep, RenderMessageStep.ProcessStepFunctions.RenderUserText));

        // Process completed
        userInputStep
            .OnEvent(CommonEvents.UserInputComplete)
            .SendEventTo(new ProcessFunctionTargetBuilder(renderMessageStep, RenderMessageStep.ProcessStepFunctions.RenderDone))
            .StopProcess();

        // Render response from primary agent
        managerAgentStep
            .OnEvent(AgentOrchestrationEvents.AgentResponse)
            .SendEventTo(new ProcessFunctionTargetBuilder(renderMessageStep, RenderMessageStep.ProcessStepFunctions.RenderMessage));

        // Request is complete
        managerAgentStep
            .OnEvent(CommonEvents.UserInputComplete)
            .SendEventTo(new ProcessFunctionTargetBuilder(renderMessageStep, RenderMessageStep.ProcessStepFunctions.RenderDone))
            .StopProcess();

        // Request more user input
        managerAgentStep
            .OnEvent(AgentOrchestrationEvents.AgentResponded)
            .SendEventTo(new ProcessFunctionTargetBuilder(userInputStep));

        // Delegate to inner agents
        managerAgentStep
            .OnEvent(AgentOrchestrationEvents.AgentWorking)
            .SendEventTo(new ProcessFunctionTargetBuilder(managerAgentStep, ManagerAgentStep.ProcessStepFunctions.InvokeGroup));

        // Provide input to inner agents
        managerAgentStep
            .OnEvent(AgentOrchestrationEvents.GroupInput)
            .SendEventTo(new ProcessFunctionTargetBuilder(agentGroupStep));

        // Render response from inner chat (for visibility)
        agentGroupStep
            .OnEvent(AgentOrchestrationEvents.GroupMessage)
            .SendEventTo(new ProcessFunctionTargetBuilder(renderMessageStep, RenderMessageStep.ProcessStepFunctions.RenderInnerMessage));

        // Provide inner response to primary agent
        agentGroupStep
            .OnEvent(AgentOrchestrationEvents.GroupCompleted)
            .SendEventTo(new ProcessFunctionTargetBuilder(managerAgentStep, ManagerAgentStep.ProcessStepFunctions.ReceiveResponse));

        KernelProcess kernelProcess = process.Build();

        return kernelProcess;

        void AttachErrorStep(ProcessStepBuilder step, params string[] functionNames)
        {
            foreach (string functionName in functionNames)
            {
                step
                    .OnFunctionError(functionName)
                    .SendEventTo(new ProcessFunctionTargetBuilder(renderMessageStep, RenderMessageStep.ProcessStepFunctions.RenderError))
                    .StopProcess();
            }
        }
    }

    private Kernel SetupKernel()
    {
        IKernelBuilder builder = Kernel.CreateBuilder();
        // Add Chat Completion to Kernel
        this.AddChatCompletionToKernel(builder);
        builder.Services.AddSingleton<OpenAIClient>(this.Client);

        // NOTE: Uncomment to see process logging
        //builder.Services.AddSingleton<ILoggerFactory>(this.LoggerFactory);

        return builder.Build();
    }

    private Kernel SetupKernel(ChatHistory history)
    {
        IKernelBuilder builder = Kernel.CreateBuilder();

        // Add Chat Completion to Kernel
        this.AddChatCompletionToKernel(builder);

        // Inject agents into service collection
        SetupAgents(builder, builder.Build());
        // Inject history provider into service collection
        builder.Services.AddSingleton<IChatHistoryProvider>(new ChatHistoryProvider(history));

        // NOTE: Uncomment to see process logging
        //builder.Services.AddSingleton<ILoggerFactory>(this.LoggerFactory);

        return builder.Build();
    }

    private const string ManagerInstructions =
        """
        Capture information provided by the user for their scheduling request.
        Request confirmation without suggesting additional details.
        Once confirmed inform them you're working on the request.
        Never provide a direct answer to the user's request.
        """;

    private const string CalendarInstructions =
        """
        Evaluate the scheduled calendar events in response to the current direction.
        In the absence of specific dates, prioritize the earliest opportunity but do not restrict evaluation the current date.
        Never consider or propose scheduling that conflicts with existing events.
        """;

    private const string WeatherInstructions =
        """
        Provide weather information in response to the current direction.
        """;

    private const string ManagerSummaryInstructions =
        """
        Summarize the most recent user request in first person command form.
        """;

    private const string SuggestionSummaryInstructions =
        """
        Address the user directly with a summary of the response.
        """;

    private static void SetupAgents(IKernelBuilder builder, Kernel kernel)
    {
        // Create and inject primary agent into service collection
        ChatCompletionAgent managerAgent = CreateAgent("Manager", ManagerInstructions, kernel.Clone());
        builder.Services.AddKeyedSingleton(ManagerAgentStep.AgentServiceKey, managerAgent);

        // Create and inject group chat into service collection
        SetupGroupChat(builder, kernel);

        // Create and inject reducers into service collection
        builder.Services.AddKeyedSingleton(ManagerAgentStep.ReducerServiceKey, SetupReducer(kernel, ManagerSummaryInstructions));
        builder.Services.AddKeyedSingleton(AgentGroupChatStep.ReducerServiceKey, SetupReducer(kernel, SuggestionSummaryInstructions));
    }

    private static ChatHistorySummarizationReducer SetupReducer(Kernel kernel, string instructions) =>
         new(kernel.GetRequiredService<IChatCompletionService>(), 1)
         {
             SummarizationInstructions = instructions
         };

    private static void SetupGroupChat(IKernelBuilder builder, Kernel kernel)
    {
        const string CalendarAgentName = "CalendarAgent";
        ChatCompletionAgent calendarAgent = CreateAgent(CalendarAgentName, CalendarInstructions, kernel.Clone());
        calendarAgent.Kernel.Plugins.AddFromType<CalendarPlugin>();

        const string WeatherAgentName = "WeatherAgent";
        ChatCompletionAgent weatherAgent = CreateAgent(WeatherAgentName, WeatherInstructions, kernel.Clone());
        weatherAgent.Kernel.Plugins.AddFromType<WeatherPlugin>();
        weatherAgent.Kernel.Plugins.AddFromType<LocationPlugin>();

        KernelFunction selectionFunction =
            AgentGroupChat.CreatePromptFunctionForStrategy(
                $$$"""
                Determine which participant takes the next turn in a conversation based on the the most recent participant.
                State only the name of the participant to take the next turn.
                No participant should take more than one turn in a row.
                
                Choose only from these participants:
                - {{{CalendarAgentName}}}
                - {{{WeatherAgentName}}}
                
                Always follow these rules when selecting the next participant:
                - After user input, it is {{{CalendarAgentName}}}'s turn.
                - After {{{CalendarAgentName}}}, it is {{{WeatherAgentName}}}'s turn.
                - After {{{WeatherAgentName}}}, it is {{{CalendarAgentName}}}'s turn.
                                
                History:
                {{$history}}
                """,
                safeParameterNames: "history");

        KernelFunction terminationFunction =
            AgentGroupChat.CreatePromptFunctionForStrategy(
                $$$"""
                Evaluate if the a user's most recent calendar request has received a final response.
                If weather conditions are requested, {{{WeatherAgentName}}} is required to provide input.

                If all of these conditions are met, respond with a single word: yes

                History:
                {{$history}}
                """,
                safeParameterNames: "history");

        AgentGroupChat chat =
            new(calendarAgent, weatherAgent)
            {
                // NOTE: Replace logger when using outside of sample.
                // Use `this.LoggerFactory` to observe logging output as part of sample.
                LoggerFactory = NullLoggerFactory.Instance,
                ExecutionSettings = new()
                {
                    SelectionStrategy =
                        new KernelFunctionSelectionStrategy(selectionFunction, kernel)
                        {
                            HistoryVariableName = "history",
                            HistoryReducer = new ChatHistoryTruncationReducer(1),
                            ResultParser = (result) => result.GetValue<string>() ?? calendarAgent.Name!,
                        },
                    TerminationStrategy =
                        new KernelFunctionTerminationStrategy(terminationFunction, kernel)
                        {
                            HistoryVariableName = "history",
                            MaximumIterations = 12,
                            //HistoryReducer = new ChatHistoryTruncationReducer(2),
                            ResultParser = (result) => result.GetValue<string>()?.Contains("yes", StringComparison.OrdinalIgnoreCase) ?? false,
                        }
                }
            };
        builder.Services.AddSingleton(chat);
    }

    private static ChatCompletionAgent CreateAgent(string name, string instructions, Kernel kernel) =>
        new()
        {
            Name = name,
            Instructions = instructions,
            Kernel = kernel.Clone(),
            Arguments =
                new KernelArguments(
                    new OpenAIPromptExecutionSettings
                    {
                        FunctionChoiceBehavior = FunctionChoiceBehavior.Auto(),
                        Temperature = 0,
                    }),
        };
}
