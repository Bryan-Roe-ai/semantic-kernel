﻿// Copyright (c) Microsoft. All rights reserved.
using System;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using VerifyTests;
using Xunit;

namespace Microsoft.SemanticKernel.Process.Core.UnitTests;

/// <summary>
/// Unit tests for <see cref="ProcessMapBuilder"/>.
/// </summary>
public class ProcessMapBuilderTests
{
    /// <summary>
    /// Verify initialization based on <see cref="ProcessStepBuilder"/>.
    /// </summary>
    [Fact]
    public void ProcessMapBuilderFromStep()
    {
        // Arrange
        ProcessStepBuilder<SimpleTestStep> step = new($"One{nameof(SimpleTestStep)}");

        // Act
        ProcessMapBuilder map = new(new ProcessFunctionTargetBuilder(step));

        // Assert
        Assert.NotNull(map.Id);
        Assert.NotNull(map.Name);
        Assert.Contains(nameof(SimpleTestStep), map.Name);
        Assert.NotNull(map._mapTarget);
        Assert.Equal(nameof(SimpleTestStep.TestFunction), map._mapTarget.FunctionName);
        Assert.Equal("value", map._mapTarget.ParameterName);
    }

    /// <summary>
    /// Verify initialization based on <see cref="ProcessBuilder"/>.
    /// </summary>
    [Fact]
    public void ProcessMapBuilderFromProcess()
    {
        // Arrange
        ProcessBuilder process = new("MapOperation");
        ProcessStepBuilder step = process.AddStepFromType<SimpleTestStep>($"One{nameof(SimpleTestStep)}");
        process.OnInputEvent("ComputeMapValue").SendEventTo(new ProcessFunctionTargetBuilder(step));

        // Act
        ProcessMapBuilder map = new(process.WhereInputEventIs("ComputeMapValue"));

        // Assert
        Assert.NotNull(map.Id);
        Assert.NotNull(map.Name);
        Assert.Contains(process.Name, map.Name);
        Assert.NotNull(map._mapTarget);
        Assert.Equal(nameof(SimpleTestStep.TestFunction), map._mapTarget.FunctionName);
        Assert.Equal("value", map._mapTarget.ParameterName);
    }

    /// <summary>
    /// Verify initialization based on <see cref="ProcessStepBuilder"/>.
    /// </summary>
    [Fact]
    public void ProcessMapBuilderIsValidTarget()
    {
        // Arrange
        ProcessStepBuilder<SimpleTestStep> step = new($"One{nameof(SimpleTestStep)}");
        ProcessMapBuilder map = new(new ProcessFunctionTargetBuilder(step));

        // Act
        ProcessStepBuilder<SimpleTestStep> step2 = new($"Two{nameof(SimpleTestStep)}");
        step2.OnEvent("Any").SendEventTo(map);

        // Assert
        Assert.Single(step2.Edges);
        Assert.Single(step2.Edges.Single().Value);
        Assert.NotNull(step2.Edges.Single().Value[0].Target);
        Assert.Equal(map, step2.Edges.Single().Value[0].Target!.Step);
    }

    /// <summary>
    /// Verify initialization based on <see cref="ProcessStepBuilder"/>.
    /// </summary>
    [Fact]
    public void ProcessMapBuilderCanTargetStep()
    {
        // Arrange
        ProcessStepBuilder<SimpleTestStep> step = new($"One{nameof(SimpleTestStep)}");
        ProcessMapBuilder map = new(new ProcessFunctionTargetBuilder(step));

        // Act
        ProcessStepBuilder<SimpleTestStep> step2 = new($"Two{nameof(SimpleTestStep)}");
        map.OnEvent("Any").SendEventTo(new ProcessFunctionTargetBuilder(step2));

        // Assert
        Assert.Single(map.Edges);
        Assert.Single(map.Edges.Single().Value);
        Assert.NotNull(map.Edges.Single().Value[0].Target);
        Assert.Equal(step2, map.Edges.Single().Value[0].Target!.Step);

        // Act
        KernelProcessStepInfo processMap = map.BuildStep();

        // Assert
        Assert.NotNull(processMap);
        Assert.Equal(processMap.Edges.Count, map.Edges.Count);
        Assert.Equal(processMap.Edges.Single().Value.Count, map.Edges.First().Value.Count);
        Assert.Equal(processMap.Edges.Single().Value.Single().OutputTarget!.StepId, map.Edges.Single().Value[0].Target!.Step.Id);
    }

    /// <summary>
    /// Verify <see cref="ProcessMapBuilder.GetFunctionMetadataMap"/> always throws.
    /// </summary>
    [Fact]
    public void ProcessMapBuilderGetFunctionMetadataMapThrows()
    {
        // Arrange
        ProcessStepBuilder<SimpleTestStep> step = new($"One{nameof(SimpleTestStep)}");
        ProcessMapBuilder map = new(new ProcessFunctionTargetBuilder(step));

        // Act
        Assert.Throws<NotImplementedException>(() => map.GetFunctionMetadataMap());
    }

    /// <summary>
    /// Verify <see cref="ProcessMapBuilder.BuildStep"/> produces the
    /// expected <see cref="KernelProcessMap"/>.
    /// </summary>
    [Fact]
    public void ProcessMapBuilderWillBuild()
    {
        // Arrange
        ProcessStepBuilder<SimpleTestStep> step = new($"One{nameof(SimpleTestStep)}");
        ProcessMapBuilder map = new(new ProcessFunctionTargetBuilder(step));

        // Act
        KernelProcessStepInfo processMap = map.BuildStep();

        // Assert
        Assert.NotNull(processMap);
        Assert.IsType<KernelProcessMap>(processMap);
        Assert.Equal(map.Name, processMap.State.Name);
        Assert.Equal(map.Id, processMap.State.Id);
    }

    /// <summary>
    /// Verify <see cref="ProcessMapBuilder.BuildStep"/> throws an exception
    /// if the target is a <see cref="ProcessBuilder"/>> without the having
    /// <see cref="ProcessFunctionTargetBuilder.TargetEventId"/> defined.
    /// While this state should not be achievable by external callers, the
    /// underlying state contracts do permit this permutation.
    /// </summary>
    [Fact]
    public void ProcessMapBuilderFailsBuildForInvalidTarget()
    {
        // Arrange
        ProcessBuilder process = new(nameof(InvalidTestStep));
        ProcessStepBuilder step = process.AddStepFromType<SimpleTestStep>();
        process.OnInputEvent("Start").SendEventTo(new ProcessFunctionTargetBuilder(step));
        ProcessFunctionTargetBuilder stepTarget = new(step, nameof(SimpleTestStep.TestFunction));
        ProcessFunctionTargetBuilder invalidTarget = stepTarget with { Step = process };

        // Act & Assert
        Assert.Throws<InvalidOperationException>(() => new ProcessMapBuilder(invalidTarget));
    }

    // %%% PROVIDE MAP AS TARGET

    private sealed class SimpleTestStep : KernelProcessStep<TestState>
    {
        private TestState? _state;

        public override ValueTask ActivateAsync(KernelProcessStepState<TestState> state)
        {
            this._state = state.State;

            return ValueTask.CompletedTask;
        }

        [KernelFunction]
        public void TestFunction(Guid value)
        {
            Assert.NotNull(this._state);
        }
    }

    private sealed class InvalidTestStep : KernelProcessStep<TestState>
    {
        private TestState? _state;

        public override ValueTask ActivateAsync(KernelProcessStepState<TestState> state)
        {
            this._state = state.State;

            return ValueTask.CompletedTask;
        }

        [KernelFunction]
        public void TestFunction()
        {
            Assert.NotNull(this._state);
        }
    }

    private sealed class ComplexTestStep : KernelProcessStep<TestState>
    {
        private TestState? _state;

        public override ValueTask ActivateAsync(KernelProcessStepState<TestState> state)
        {
            this._state = state.State;

            return ValueTask.CompletedTask;
        }

        [KernelFunction]
        public void TestFunctionA(Guid value)
        {
            Assert.NotNull(this._state);
        }

        [KernelFunction]
        public void TestFunctionB(Guid value)
        {
            Assert.NotNull(this._state);
        }
    }

    private sealed class TestState
    {
        public Guid Value { get; set; }
    }
}
