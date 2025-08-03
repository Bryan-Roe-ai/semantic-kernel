# Agent Lifecycle and State Transitions

This document describes the typical lifecycle of a Semantic Kernel agent and how state transitions are handled. Understanding these phases is helpful when implementing custom agents or hosting agents in long running services.

## Lifecycle Phases

1. **Created** – An agent instance is constructed. The associated `AgentThread` has not yet been created on the service.
2. **Active** – The agent is participating in a conversation. Messages sent to the agent create or resume an `AgentThread` which manages conversation state.
3. **Suspended** – Conversation processing is paused. The host calls `OnSuspendAsync` on the current `AgentThread` so that state can be persisted.
4. **Resumed** – A suspended conversation resumes when the host calls `OnResumeAsync`. The thread reloads any saved state before processing further messages.
5. **Deleted** – The conversation is terminated. `DeleteAsync` removes the `AgentThread` and any related state so the thread can no longer be used.

## State Management

`InProcessRuntime` (defined in the `SemanticKernel.Runtime` namespace) exposes methods such as `SaveAgentStateAsync` and `LoadAgentStateAsync` to persist agent state between runs. Unit tests like `AgentStateLifecycleTest` (located in `tests/AgentStateLifecycleTest.cs`) demonstrate saving state from one runtime instance and restoring it in another.

## Runtime Start and Stop

The runtime itself has its own lifecycle. `StartAsync` begins message processing and `StopAsync` initiates shutdown. `RunUntilIdleAsync` waits for all queued messages to be delivered before stopping. Attempting to start or stop the runtime in an invalid state results in an `InvalidOperationException`.

