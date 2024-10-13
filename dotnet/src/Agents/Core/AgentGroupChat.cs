// Copyright (c) Microsoft. All rights reserved.
using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Logging.Abstractions;
using Microsoft.SemanticKernel.Agents.Chat;

namespace Microsoft.SemanticKernel.Agents;

/// <summary>
/// A an <see cref="AgentChat"/> that supports multi-turn interactions.
/// </summary>
public sealed class AgentGroupChat : AgentChat
{
    private readonly HashSet<string> _agentIds; // Efficient existence test O(1) vs O(n) for list.
    private readonly List<Agent> _agents; // Maintain order the agents joined the chat

    /// <summary>
    /// Indicates if completion criteria has been met.  If set, no further
    /// agent interactions will occur.  Clear to enable more agent interactions.
    /// </summary>
    public bool IsComplete { get; set; }

    /// <summary>
    /// Settings for defining chat behavior.
    /// </summary>
    public AgentGroupChatSettings ExecutionSettings { get; set; } = new AgentGroupChatSettings();

    /// <summary>
    /// The agents participating in the chat.
    /// </summary>
<<<<<<< HEAD
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    public IReadOnlyList<Agent> Agents => this._agents.AsReadOnly();
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
>>>>>>> Stashed changes
<<<<<<< HEAD
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
    public IReadOnlyList<Agent> Agents => this._agents.AsReadOnly();
=======
    public override IReadOnlyList<Agent> Agents => this._agents.AsReadOnly();
>>>>>>> main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
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
    public override IReadOnlyList<Agent> Agents => this._agents.AsReadOnly();
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< div
=======
    public override IReadOnlyList<Agent> Agents => this._agents.AsReadOnly();
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
=======
>>>>>>> head

    /// <summary>
    /// Add a <see cref="Agent"/> to the chat.
    /// </summary>
    /// <param name="agent">The <see cref="KernelAgent"/> to add.</param>
    public void Add(Agent agent)
    {
        if (this._agentIds.Add(agent.Id))
        {
            this._agents.Add(agent);
        }
    }

    /// <summary>
    /// Process a series of interactions between the <see cref="AgentGroupChat.Agents"/> that have joined this <see cref="AgentGroupChat"/>.
    /// The interactions will proceed according to the <see cref="SelectionStrategy"/> and the <see cref="TerminationStrategy"/>
    /// defined via <see cref="AgentGroupChat.ExecutionSettings"/>.
    /// In the absence of an <see cref="AgentGroupChatSettings.SelectionStrategy"/>, this method will not invoke any agents.
    /// Any agent may be explicitly selected by calling <see cref="AgentGroupChat.InvokeAsync(Agent, CancellationToken)"/>.
    /// </summary>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>Asynchronous enumeration of messages.</returns>
    public override async IAsyncEnumerable<ChatMessageContent> InvokeAsync([EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        this.EnsureStrategyLoggerAssignment();
        this.EnsureCompletionStatus();

        this.Logger.LogAgentGroupChatInvokingAgents(nameof(InvokeAsync), this.Agents);

<<<<<<< HEAD
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
<<<<<<< Updated upstream
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
>>>>>>> Stashed changes
<<<<<<< HEAD
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
        bool isComplete = false;

>>>>>>> main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
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
        bool isComplete = false;

>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
        for (int index = 0; index < this.ExecutionSettings.TerminationStrategy.MaximumIterations; index++)
        {
            // Identify next agent using strategy
            Agent agent = await this.SelectAgentAsync(cancellationToken).ConfigureAwait(false);

            // Invoke agent and process messages along with termination
            await foreach (var message in this.InvokeAsync(agent, cancellationToken).ConfigureAwait(false))
            {
                yield return message;
            }

            if (this.IsComplete)
            {
                break;
            }
        }

        this.Logger.LogAgentGroupChatYield(nameof(InvokeAsync), this.IsComplete);
    }

    /// <summary>
    /// Process a series of interactions between the <see cref="AgentGroupChat.Agents"/> that have joined this <see cref="AgentGroupChat"/>.
    /// The interactions will proceed according to the <see cref="SelectionStrategy"/> and the <see cref="TerminationStrategy"/>
    /// defined via <see cref="AgentGroupChat.ExecutionSettings"/>.
    /// In the absence of an <see cref="AgentGroupChatSettings.SelectionStrategy"/>, this method will not invoke any agents.
    /// Any agent may be explicitly selected by calling <see cref="AgentGroupChat.InvokeAsync(Agent, CancellationToken)"/>.
    /// </summary>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>Asynchronous enumeration of streaming messages.</returns>
    public override async IAsyncEnumerable<StreamingChatMessageContent> InvokeStreamingAsync([EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        this.EnsureStrategyLoggerAssignment();
        this.EnsureCompletionStatus();

        this.Logger.LogAgentGroupChatInvokingAgents(nameof(InvokeAsync), this.Agents);

        for (int index = 0; index < this.ExecutionSettings.TerminationStrategy.MaximumIterations; index++)
        {
            // Identify next agent using strategy
            Agent agent = await this.SelectAgentAsync(cancellationToken).ConfigureAwait(false);

            // Invoke agent and process messages along with termination
            await foreach (var message in this.InvokeStreamingAsync(agent, cancellationToken).ConfigureAwait(false))
            {
<<<<<<< HEAD
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
<<<<<<< Updated upstream
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
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
                yield return message;
            }

            if (this.IsComplete)
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
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
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
=======
>>>>>>> Stashed changes
=======
=======
>>>>>>> Stashed changes
>>>>>>> head
                if (message.Role == AuthorRole.Assistant)
                {
                    var task = this.ExecutionSettings.TerminationStrategy.ShouldTerminateAsync(agent, this.History, cancellationToken);
                    isComplete = await task.ConfigureAwait(false);
                }

                yield return message;
            }

            if (isComplete)
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
<<<<<<< HEAD
>>>>>>> main
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
>>>>>>> Stashed changes
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
>>>>>>> main
>>>>>>> Stashed changes
=======
>>>>>>> main
>>>>>>> Stashed changes
>>>>>>> head
            {
                break;
            }
        }

<<<<<<< HEAD
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
<<<<<<< Updated upstream
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
>>>>>>> Stashed changes
<<<<<<< HEAD
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
        this.IsComplete = isComplete;

>>>>>>> main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
=======
>>>>>>> Stashed changes
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
        this.IsComplete = isComplete;

>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
        this.Logger.LogAgentGroupChatYield(nameof(InvokeAsync), this.IsComplete);
    }

    /// <summary>
    /// Process a single interaction between a given <see cref="Agent"/> an a <see cref="AgentGroupChat"/>.
    /// </summary>
    /// <param name="agent">The agent actively interacting with the chat.</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>Asynchronous enumeration of messages.</returns>
    /// <remark>
    /// Specified agent joins the chat.
    /// </remark>>
    public async IAsyncEnumerable<ChatMessageContent> InvokeAsync(
        Agent agent,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        this.EnsureStrategyLoggerAssignment();

        this.Logger.LogAgentGroupChatInvokingAgent(nameof(InvokeAsync), agent.GetType(), agent.Id);

<<<<<<< main
<<<<<<< HEAD
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
<<<<<<< main
>>>>>>> origin/main
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
>>>>>>> Stashed changes
<<<<<<< HEAD
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> origin/main
=======
>>>>>>> main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
=======
>>>>>>> Stashed changes
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
        if (isJoining)
        {
            this.Add(agent);
        }
<<<<<<< HEAD
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
<<<<<<< Updated upstream
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
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< main
        this.AddAgent(agent);
=======
=======
        this.AddAgent(agent);
>>>>>>> upstream/main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
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
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
        this.AddAgent(agent);
=======
        this.AddAgent(agent);
>>>>>>> main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
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
        this.AddAgent(agent);
=======
        this.AddAgent(agent);
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
>>>>>>> origin/main

        await foreach (ChatMessageContent message in base.InvokeAgentAsync(agent, cancellationToken).ConfigureAwait(false))
        {
            yield return message;
        }

        this.IsComplete = await this.ExecutionSettings.TerminationStrategy.ShouldTerminateAsync(agent, this.History, cancellationToken).ConfigureAwait(false);

        this.Logger.LogAgentGroupChatYield(nameof(InvokeAsync), this.IsComplete);
    }

    /// <summary>
    /// Process a single interaction between a given <see cref="Agent"/> an a <see cref="AgentGroupChat"/>.
    /// </summary>
    /// <param name="agent">The agent actively interacting with the chat.</param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>Asynchronous enumeration of messages.</returns>
    /// <remark>
    /// Specified agent joins the chat.
    /// </remark>
    public async IAsyncEnumerable<StreamingChatMessageContent> InvokeStreamingAsync(
        Agent agent,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        this.EnsureStrategyLoggerAssignment();

        this.Logger.LogAgentGroupChatInvokingAgent(nameof(InvokeAsync), agent.GetType(), agent.Id);

        this.AddAgent(agent);

        await foreach (StreamingChatMessageContent message in base.InvokeStreamingAgentAsync(agent, cancellationToken).ConfigureAwait(false))
        {
            yield return message;
        }

        this.IsComplete = await this.ExecutionSettings.TerminationStrategy.ShouldTerminateAsync(agent, this.History, cancellationToken).ConfigureAwait(false);

        this.Logger.LogAgentGroupChatYield(nameof(InvokeAsync), this.IsComplete);
    }

    /// <summary>
<<<<<<< HEAD
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
<<<<<<< Updated upstream
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
>>>>>>> Stashed changes
<<<<<<< HEAD
=======
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
=======
>>>>>>> Stashed changes
=======
=======
>>>>>>> Stashed changes
>>>>>>> head
    /// Convenience method to create a <see cref="KernelFunction"/> for a given strategy without HTML encoding the specified parameters.
    /// </summary>
    /// <param name="template">The prompt template string that defines the prompt.</param>
    /// <param name="templateFactory">
    /// On optional <see cref="IPromptTemplateFactory"/> to use when interpreting the <paramref name="template"/>.
    /// The default factory will be used when none is provided.
    /// </param>
    /// <param name="safeParameterNames">The parameter names to exclude from being HTML encoded.</param>
    /// <returns>A <see cref="KernelFunction"/> created via <see cref="KernelFunctionFactory"/> using the specified template.</returns>
    /// <remarks>
    /// This is particularly targeted to easily avoid encoding the history used by <see cref="KernelFunctionSelectionStrategy"/>
    /// or <see cref="KernelFunctionTerminationStrategy"/>.
    /// </remarks>
    public static KernelFunction CreatePromptFunctionForStrategy(string template, IPromptTemplateFactory? templateFactory = null, params string[] safeParameterNames)
    {
        PromptTemplateConfig config =
            new(template)
            {
                InputVariables = safeParameterNames.Select(parameterName => new InputVariable { Name = parameterName, AllowDangerouslySetContent = true }).ToList()
            };

        return KernelFunctionFactory.CreateFromPrompt(config, promptTemplateFactory: templateFactory);
    }

    /// <summary>
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
<<<<<<< HEAD
>>>>>>> main
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
>>>>>>> Stashed changes
=======
>>>>>>> eab985c52d058dc92abc75034bc790079131ce75
<<<<<<< div
=======
=======
>>>>>>> main
>>>>>>> Stashed changes
=======
>>>>>>> main
>>>>>>> Stashed changes
>>>>>>> head
    /// Initializes a new instance of the <see cref="AgentGroupChat"/> class.
    /// </summary>
    /// <param name="agents">The agents initially participating in the chat.</param>
    public AgentGroupChat(params Agent[] agents)
    {
        this._agents = new(agents);
        this._agentIds = new(this._agents.Select(a => a.Id));
    }

    private void EnsureStrategyLoggerAssignment()
    {
        // Only invoke logger factory when required.
        if (this.ExecutionSettings.SelectionStrategy.Logger == NullLogger.Instance)
        {
            this.ExecutionSettings.SelectionStrategy.Logger = this.LoggerFactory.CreateLogger(this.ExecutionSettings.SelectionStrategy.GetType());
        }

        if (this.ExecutionSettings.TerminationStrategy.Logger == NullLogger.Instance)
        {
            this.ExecutionSettings.TerminationStrategy.Logger = this.LoggerFactory.CreateLogger(this.ExecutionSettings.TerminationStrategy.GetType());
        }
    }

    private void EnsureCompletionStatus()
    {
        if (this.IsComplete)
        {
            // Throw exception if chat is completed and automatic-reset is not enabled.
            if (!this.ExecutionSettings.TerminationStrategy.AutomaticReset)
            {
                throw new KernelException("Agent Failure - Chat has completed.");
            }

            this.IsComplete = false;
        }
    }

    private async Task<Agent> SelectAgentAsync(CancellationToken cancellationToken)
    {
        this.Logger.LogAgentGroupChatSelectingAgent(nameof(InvokeAsync), this.ExecutionSettings.SelectionStrategy.GetType());

        Agent agent;
        try
        {
            agent = await this.ExecutionSettings.SelectionStrategy.NextAsync(this.Agents, this.History, cancellationToken).ConfigureAwait(false);
        }
        catch (Exception exception)
        {
            this.Logger.LogAgentGroupChatNoAgentSelected(nameof(InvokeAsync), exception);
            throw;
        }

        this.Logger.LogAgentGroupChatSelectedAgent(nameof(InvokeAsync), agent.GetType(), agent.Id, this.ExecutionSettings.SelectionStrategy.GetType());

        return agent;
    }
}
