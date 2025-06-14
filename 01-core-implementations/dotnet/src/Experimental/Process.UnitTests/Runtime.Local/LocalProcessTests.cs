// Copyright (c) Microsoft. All rights reserved.

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;
using System.Threading.Tasks;
using Microsoft.SemanticKernel.Process.Models;
using Microsoft.SemanticKernel.Process.Models.Storage;
using SemanticKernel.Process.TestsShared.Services;
using SemanticKernel.Process.TestsShared.Services.Storage;
using SemanticKernel.Process.TestsShared.Setup;
using SemanticKernel.Process.TestsShared.Steps;
using Xunit;

namespace Microsoft.SemanticKernel.Process.Runtime.Local.UnitTests;

/// <summary>
/// Unit tests for the <see cref="LocalProcess"/> class.
/// </summary>
public class LocalProcessTests
{
    private readonly IReadOnlyDictionary<string, KernelProcess> _keyedProcesses = CommonProcesses.GetCommonProcessesKeyedDictionary();

    /// <summary>
    /// Validates that the <see cref="LocalProcess"/> constructor initializes the steps correctly.
    /// </summary>
    [Fact]
    public async Task ExecuteAsyncInitializesCorrectlyAsync()
    {
        // Arrange
        var processState = new KernelProcessState(name: "TestProcess", version: "v1", id: "123");
        var mockKernelProcess = new KernelProcess(processState,
        [
            new(typeof(TestStep), new KernelProcessState(name: "Step1", version: "v1", id: "1"), []),
            new(typeof(TestStep), new KernelProcessState(name: "Step2", version: "v1", id: "2"), [])
        ], []);

        var mockKernel = new Kernel();
        await using var localProcess = new LocalProcess(mockKernelProcess, mockKernel);
        // Act
        await localProcess.StartAsync();

        // Assert
        Assert.Equal(2, localProcess._steps.Count);
        Assert.Contains(localProcess._steps, s => s.Name == "Step1");
        Assert.Contains(localProcess._steps, s => s.Name == "Step2");
    }

    /// <summary>
    /// Validates that the <see cref="LocalProcess"/> assigns and Id to the process if one is not already set.
    /// </summary>
    [Fact]
    public async Task ProcessWithMissingIdIsAssignedAnIdAsync()
    {
        // Arrange
        var mockKernel = new Kernel();
        var processState = new KernelProcessState(name: "TestProcess", version: "v1");
        var mockKernelProcess = new KernelProcess(processState,
        [
            new(typeof(TestStep), new KernelProcessState(name: "Step1", version: "v1", id: "1"), []),
            new(typeof(TestStep), new KernelProcessState(name: "Step2", version: "v1", id: "2"), [])
        ], []);

        // Act
        await using var localProcess = new LocalProcess(mockKernelProcess, mockKernel);

        // Assert
        Assert.NotEmpty(localProcess.Id);
    }

    /// <summary>
    /// Validates that the <see cref="LocalProcess"/> assigns and Id to the process if one is not already set.
    /// </summary>
    [Fact]
    public async Task ProcessWithAssignedIdIsNotOverwrittenIdAsync()
    {
        // Arrange
        var processId = "AlreadySet";
        var mockKernel = new Kernel();
        var processState = new KernelProcessState(name: "TestProcess", version: "v1");
        var mockKernelProcess = new KernelProcess(processState,
        [
            new(typeof(TestStep), new KernelProcessState(name: "Step1", version: "v1", id: "1"), []),
            new(typeof(TestStep), new KernelProcessState(name: "Step2", version: "v1", id: "2"), [])
        ], []);

        // Act
        await using var localProcess = new LocalProcess(mockKernelProcess, mockKernel, instanceId: processId);

        // Assert
        Assert.NotEmpty(localProcess.Id);
        Assert.Equal("AlreadySet", localProcess.Id);
    }

    /// <summary>
    /// Validates that the <see cref="LocalProcess"/> assigns and Id to the process if one is not already set.
    /// Verify that the function  level error handler is called when a function fails.
    /// </summary>
    [Fact]
    public async Task ProcessFunctionErrorHandledAsync()
    {
        // Arrange
        ProcessBuilder process = new(nameof(ProcessFunctionErrorHandledAsync));

        ProcessStepBuilder testStep = process.AddStepFromType<FailedStep>();
        process.OnInputEvent("Start").SendEventTo(new ProcessFunctionTargetBuilder(testStep));

        ProcessStepBuilder errorStep = process.AddStepFromType<ErrorStep>();
        testStep.OnFunctionError(nameof(FailedStep.TestFailure)).SendEventTo(new ProcessFunctionTargetBuilder(errorStep, nameof(ErrorStep.FunctionErrorHandler)));

        KernelProcess processInstance = process.Build();
        Kernel kernel = new();

        // Act
        await using LocalKernelProcessContext runningProcess = await processInstance.StartAsync(kernel, new KernelProcessEvent() { Id = "Start" });

        // Assert
        Assert.True(kernel.Data.ContainsKey("error-function"));
        Assert.IsType<KernelProcessError>(kernel.Data["error-function"]);
    }

    /// <summary>
    /// Verify that the process level error handler is called when a function fails.
    /// </summary>
    [Fact]
    public async Task ProcessGlobalErrorHandledAsync()
    {
        // Arrange
        ProcessBuilder process = new(nameof(ProcessFunctionErrorHandledAsync));

        ProcessStepBuilder testStep = process.AddStepFromType<FailedStep>();
        process.OnInputEvent("Start").SendEventTo(new ProcessFunctionTargetBuilder(testStep));

        ProcessStepBuilder errorStep = process.AddStepFromType<ErrorStep>();
        process.OnError().SendEventTo(new ProcessFunctionTargetBuilder(errorStep, nameof(ErrorStep.GlobalErrorHandler)));

        KernelProcess processInstance = process.Build();
        Kernel kernel = new();

        // Act
        await using LocalKernelProcessContext runningProcess = await processInstance.StartAsync(kernel, new KernelProcessEvent() { Id = "Start" });

        // Assert
        Assert.True(kernel.Data.ContainsKey("error-global"));
        Assert.IsType<KernelProcessError>(kernel.Data["error-global"]);
    }

    /// <summary>
    /// Verify that the function level error handler has precedence over the process level error handler.
    /// </summary>
    [Fact]
    public async Task FunctionErrorHandlerTakesPrecedenceAsync()
    {
        // Arrange
        ProcessBuilder process = new(nameof(ProcessFunctionErrorHandledAsync));

        ProcessStepBuilder testStep = process.AddStepFromType<FailedStep>();
        process.OnInputEvent("Start").SendEventTo(new ProcessFunctionTargetBuilder(testStep));

        ProcessStepBuilder errorStep = process.AddStepFromType<ErrorStep>();
        testStep.OnFunctionError(nameof(FailedStep.TestFailure)).SendEventTo(new ProcessFunctionTargetBuilder(errorStep, nameof(ErrorStep.FunctionErrorHandler)));
        process.OnError().SendEventTo(new ProcessFunctionTargetBuilder(errorStep, nameof(ErrorStep.GlobalErrorHandler)));

        KernelProcess processInstance = process.Build();
        Kernel kernel = new();

        // Act
        await using LocalKernelProcessContext runningProcess = await processInstance.StartAsync(kernel, new KernelProcessEvent() { Id = "Start" });

        // Assert
        Assert.False(kernel.Data.ContainsKey("error-global"));
        Assert.True(kernel.Data.ContainsKey("error-function"));
        Assert.IsType<KernelProcessError>(kernel.Data["error-function"]);
    }

    /// <summary>
    /// Verify that the process level error handler is called when a function fails.
    /// </summary>
    /// <returns></returns>
    [Fact]
    public async Task StartProcessWithKeyedProcessDictFailDueMissingKeyAsync()
    {
        // Arrange
        var processId = "myProcessId";
        var processKey = "someKeyThatDoesNotExist";

        CounterService counterService = new();
        Kernel kernel = KernelSetup.SetupKernelWithCounterService(counterService);

        // Act & Assert
        try
        {
            await using LocalKernelProcessContext runningProcess = await LocalKernelProcessFactory.StartAsync(
                kernel, this._keyedProcesses, processKey, processId, new KernelProcessEvent()
                {
                    Id = CommonProcesses.ProcessEvents.StartProcess,
                });
        }
        catch (ArgumentException ex)
        {
            // Assert
            Assert.Equal($"The process with key '{processKey}' is not registered.", ex.Message);
        }
    }

    /// <summary>
    /// Verify that the process runs correctly when using the context factory with process key.
    /// </summary>
    /// <returns></returns>
    [Fact]
    public async Task StartProcessWithKeyedProcessDictSuccessfullyAsync()
    {
        // Arrange
        var processId = "myProcessId";
        var processKey = CommonProcesses.ProcessKeys.CounterProcess;

        CounterService counterService = new();
        Kernel kernel = KernelSetup.SetupKernelWithCounterService(counterService);

        // Act
        await using LocalKernelProcessContext runningProcess = await LocalKernelProcessFactory.StartAsync(
            kernel, this._keyedProcesses, processKey, processId, new KernelProcessEvent()
            {
                Id = CommonProcesses.ProcessEvents.StartProcess,
            });

        // Assert
        var processState = await runningProcess.GetStateAsync();
        Assert.NotNull(processState);
        Assert.Equal(processKey, processState.State.StepId);
        Assert.Equal(processId, processState.State.RunId);
    }

    /// <summary>
    /// Verify that the process runs correctly when using the context factory with process key and a storage manager.
    /// </summary>
    /// <returns></returns>
    [Fact]
    public async Task StartProcessWithKeyedProcessDictAndStoreManagerAsync()
    {
        // Arrange
        var processId = "myProcessId";
        var processKey = CommonProcesses.ProcessKeys.CounterProcess;
        var counterName = "counterStep";

        var processStorage = new MockStorage();

        CounterService counterService = new();
        Kernel kernel = KernelSetup.SetupKernelWithCounterService(counterService);

        // Act - 1
        await using LocalKernelProcessContext runningProcess = await LocalKernelProcessFactory.StartAsync(
            kernel, this._keyedProcesses, processKey, processId, new KernelProcessEvent()
            {
                Id = CommonProcesses.ProcessEvents.StartProcess,
            }, storageConnector: processStorage);

        // Assert - 1
        var processState = await runningProcess.GetStateAsync();
        Assert.NotNull(processState);
        var counterState = processState.Steps.Where(s => s.State.StepId == counterName).FirstOrDefault();
        Assert.NotNull(counterState);
        Assert.Equal(1, ((KernelProcessStepState<CommonSteps.CounterState>)counterState.State).State?.Count);

        Assert.Equal(processKey, processState.State.StepId);
        Assert.Equal(processId, processState.State.RunId);

        // Act - 2
        counterService.SetCount(0);
        await using LocalKernelProcessContext runningProcess2 = await LocalKernelProcessFactory.StartAsync(
            kernel, this._keyedProcesses, processKey, processId, new KernelProcessEvent()
            {
                Id = CommonProcesses.ProcessEvents.StartProcess,
            }, storageConnector: processStorage);

        // Assert - 2
        var processState2 = await runningProcess2.GetStateAsync();
        Assert.NotNull(processState2);
        var counterState2 = processState2.Steps.Where(s => s.State.StepId == counterName).FirstOrDefault();
        Assert.NotNull(counterState2);
        Assert.Equal(2, ((KernelProcessStepState<CommonSteps.CounterState>)counterState2.State).State?.Count);

        Assert.Equal(processKey, processState2.State.StepId);
        Assert.Equal(processId, processState2.State.RunId);
    }

    /// <summary>
    /// Verify that the process runs correctly when using the context factory with process key and a storage manager.
    /// Running same process twice to verify step parameters get persisted.
    /// </summary>
    /// <returns></returns>
    [Fact]
    public async Task StartProcessWithKeyedProcessAndUseOfAllOfAsync()
    {
        // Arrange
        var processId = "myProcessId";
        var mergeStepStorageEntry = "{0}.MergeStringsStep.StepEdgesData";
        var processKey = CommonProcesses.ProcessKeys.DelayedMergeProcess;

        var processStorage = new MockStorage();
        // To use local storage, comment line above and uncomment line below + replacing <TEST_DIR> with existing directory path
        //var processStorage = new JsonFileStorage("<TEST_DIR>");

        CounterService counterService = new();
        Kernel kernel = KernelSetup.SetupKernelWithCounterService(counterService);

        // Act - 1
        await using LocalKernelProcessContext runningProcess = await LocalKernelProcessFactory.StartAsync(
            kernel, this._keyedProcesses, processKey, processId, new KernelProcessEvent()
            {
                Id = CommonProcesses.ProcessEvents.StartProcess,
                Data = "Hello",
            }, storageConnector: processStorage);

        // Assert - 1
        var processState = await runningProcess.GetStateAsync();
        Assert.NotNull(processState);
        Assert.Equal(processId, processState.State.RunId);
        var mergeStepId = processState.Steps.Where(s => s.State.StepId == "MergeStringsStep").FirstOrDefault()?.State.RunId;
        Assert.NotNull(mergeStepId);
        var mergeStepFullEntry = string.Format(mergeStepStorageEntry, mergeStepId);
        processStorage._dbMock.TryGetValue(mergeStepFullEntry, out var entry);
        Assert.NotNull(entry?.Content);

        var edgeData = JsonSerializer.Deserialize<StorageStepEdgesData>(entry.Content);
        Assert.NotNull(edgeData);
        Assert.Single(edgeData.EdgesData);
        // Only 2/3 events in merge step should have arrived and persisted in stepEdgesData
        Assert.Equal(2, edgeData.EdgesData.First().Value?.Count);
        Assert.True(edgeData.EdgesData.First().Value?.ContainsKey("DelayedEchoStep22.DelayedEcho"));
        Assert.True(edgeData.EdgesData.First().Value?.ContainsKey("DelayedEchoStep33.DelayedEcho"));

        // Act - 2
        await using LocalKernelProcessContext runningProcess2 = await LocalKernelProcessFactory.StartAsync(
            kernel, this._keyedProcesses, processKey, processId, new KernelProcessEvent()
            {
                Id = CommonProcesses.ProcessEvents.OtherEvent,
                Data = "World",
            }, storageConnector: processStorage);

        // Assert - 2
        var processState2 = await runningProcess2.GetStateAsync();
        Assert.NotNull(processState2);
        Assert.Equal(processId, processState2.State.RunId);
        processStorage._dbMock.TryGetValue(mergeStepFullEntry, out var entry2);
        Assert.NotNull(entry2?.Content);
        Assert.IsType<string>(entry2?.Content);

        var edgeData2 = JsonSerializer.Deserialize<StorageStepEdgesData>(entry2.Content);
        Assert.NotNull(edgeData2);
        Assert.Single(edgeData2.EdgesData);
        // All parameters in merge step should have been processed and edge data should be empty
        Assert.Empty(edgeData2.EdgesData.First().Value!);
    }

    /// <summary>
    /// Verify that the process runs correctly when using the context factory with process key and a storage manager.
    /// Running same process twice to verify step parameters get persisted.
    /// Making use of process input events directly to validate AllOf plumbing with process events
    /// </summary>
    /// <returns></returns>
    [Fact]
    public async Task StartProcessWithKeyedProcessUseOfAllOfAndAllEventsAreProcessInputsAsync()
    {
        // Arrange
        var processId = "myProcessId";
        var mergeStepStorageEntry = "{0}.MergeStringsStep.StepEdgesData";
        var processKey = CommonProcesses.ProcessKeys.SimpleMergeProcess;

        var processStorage = new MockStorage();
        // To use local storage, comment line above and uncomment line below + replacing <TEST_DIR> with existing directory path
        //var processStorage = new JsonFileStorage("<TEST_DIR>");

        Kernel kernel = new();

        // Act - 1
        await using LocalKernelProcessContext runningProcess = await LocalKernelProcessFactory.StartAsync(
            kernel, this._keyedProcesses, processKey, processId, new KernelProcessEvent()
            {
                Id = CommonProcesses.ProcessEvents.StartProcess,
                Data = "Hello",
            }, storageConnector: processStorage);

        // Assert - 1
        var processState = await runningProcess.GetStateAsync();
        Assert.NotNull(processState);
        Assert.Equal(processId, processState.State.RunId);
        var mergeStepId = processState.Steps.Where(s => s.State.StepId == "MergeStringsStep").FirstOrDefault()?.State.RunId;
        Assert.NotNull(mergeStepId);
        var mergeStepFullEntry = string.Format(mergeStepStorageEntry, mergeStepId);
        processStorage._dbMock.TryGetValue(mergeStepFullEntry, out var entry);
        Assert.NotNull(entry?.Content);
        Assert.IsType<string>(entry?.Content);

        var edgeData = JsonSerializer.Deserialize<StorageStepEdgesData>(entry.Content);
        Assert.NotNull(edgeData);
        Assert.Single(edgeData.EdgesData);
        // Only 1/2 events in merge step should have arrived and persisted in stepEdgesData
        Assert.Single(edgeData.EdgesData.First().Value);
        Assert.True(edgeData.EdgesData.First().Value?.ContainsKey("SimpleMergeProcess.StartProcess"));

        // Act - 2
        await using LocalKernelProcessContext runningProcess2 = await LocalKernelProcessFactory.StartAsync(
            kernel, this._keyedProcesses, processKey, processId, new KernelProcessEvent()
            {
                Id = CommonProcesses.ProcessEvents.OtherEvent,
                Data = "World",
            }, storageConnector: processStorage);

        // Assert - 2
        var processState2 = await runningProcess2.GetStateAsync();
        Assert.NotNull(processState2);
        processStorage._dbMock.TryGetValue(mergeStepFullEntry, out var entry2);
        Assert.NotNull(entry2?.Content);
        Assert.IsType<string>(entry2?.Content);

        var edgeData2 = JsonSerializer.Deserialize<StorageStepEdgesData>(entry2.Content);
        Assert.NotNull(edgeData2);
        Assert.Single(edgeData2.EdgesData);
        // All parameters in merge step should have been processed and edge data should be empty
        Assert.Empty(edgeData2.EdgesData.First().Value!);
    }

    [Fact]
    public async Task StartProcessWithKeyedProcessUseOfNestedStatefulStepsAndAllOfAsync()
    {
        // Arrange
        var processId = "myProcessId";
        var mergeStepStorageEntry = "{0}.MergeStringsStep.StepEdgesData";
        var outerCounterStorageEntry = "{0}.outerCounterStep.StepState";
        var innerCounterStorageEntry = "{0}.counterStep.StepState";
        var processKey = CommonProcesses.ProcessKeys.NestedCounterWithEvenDetectionAndMergeProcess;

        var processStorage = new MockStorage();
        // To use local storage, comment line above and uncomment line below + replacing <TEST_DIR> with existing directory path
        //var processStorage = new JsonFileStorage("<TEST_DIR>");

        Kernel kernel = new();
        var iterationCount = 4;
        string? outerCounterStepFullEntry = null;
        string? innerCounterStepFullEntry = null;
        string? mergeStepFullEntry = null;

        for (int i = 1; i < iterationCount; i++)
        {
            // Act - 1,2,3
            await using LocalKernelProcessContext runningProcess = await LocalKernelProcessFactory.StartAsync(
                kernel, this._keyedProcesses, processKey, processId, new KernelProcessEvent()
                {
                    Id = CommonProcesses.ProcessEvents.StartProcess,
                }, storageConnector: processStorage);

            // Assert - 1,2,3
            var processState = await runningProcess.GetStateAsync();
            Assert.NotNull(processState);
            Assert.Equal(processId, processState.State.RunId);

            outerCounterStepFullEntry ??= string.Format(outerCounterStorageEntry, processState.Steps.Where(s => s.State.StepId == "outerCounterStep").FirstOrDefault()?.State.RunId);
            this.AssertCounterState(processStorage, outerCounterStepFullEntry, i);

            var innerCounterStepId = (processState.Steps.Where(s => s.State.StepId == "innerCounterProcess").FirstOrDefault() as KernelProcess)?.Steps.Where(s => s.State.StepId == "counterStep").FirstOrDefault()?.State.RunId;
            if (i == 1)
            {
                Assert.Null(innerCounterStepId);
            }
            else
            {
                innerCounterStepFullEntry ??= string.Format(innerCounterStorageEntry, innerCounterStepId);
                this.AssertCounterState(processStorage, innerCounterStepFullEntry, i / 2);
            }

            // Merge Step entry should have parameter entries pending until iteration 4
            mergeStepFullEntry ??= string.Format(mergeStepStorageEntry, processState.Steps.Where(s => s.State.StepId == "MergeStringsStep").FirstOrDefault()?.State.RunId);
            processStorage._dbMock.TryGetValue(mergeStepFullEntry, out var mergeStorageEntry);
            Assert.NotNull(mergeStorageEntry?.Content);

            var mergeEdgeData = JsonSerializer.Deserialize<StorageStepEdgesData>(mergeStorageEntry.Content);
            Assert.NotNull(mergeEdgeData);
            Assert.Single(mergeEdgeData.EdgesData);
            Assert.NotEmpty(mergeEdgeData.EdgesData.Values);
        }

        // Act - 4
        await using LocalKernelProcessContext runningProcess2 = await LocalKernelProcessFactory.StartAsync(
            kernel, this._keyedProcesses, processKey, processId, new KernelProcessEvent()
            {
                Id = CommonProcesses.ProcessEvents.StartProcess,
            }, storageConnector: processStorage);

        // Assert - 4
        var processState2 = await runningProcess2.GetStateAsync();
        Assert.NotNull(processState2);
        Assert.Equal(processId, processState2.State.RunId);

        Assert.NotNull(outerCounterStepFullEntry);
        this.AssertCounterState(processStorage, outerCounterStepFullEntry, 4);

        Assert.NotNull(innerCounterStepFullEntry);
        this.AssertCounterState(processStorage, innerCounterStepFullEntry, 2);

        Assert.NotNull(mergeStepFullEntry);
        processStorage._dbMock.TryGetValue(mergeStepFullEntry, out var mergeStorageEntry2);
        Assert.NotNull(mergeStorageEntry2?.Content);

        var mergeEdgeData2 = JsonSerializer.Deserialize<StorageStepEdgesData>(mergeStorageEntry2.Content);
        Assert.NotNull(mergeEdgeData2);
        Assert.Single(mergeEdgeData2.EdgesData);
        Assert.Empty(mergeEdgeData2.EdgesData.Values.First());
    }

    private void AssertCounterState(MockStorage processStorage, string stepStorageEntry, int expectedCount)
    {
        processStorage._dbMock.TryGetValue(stepStorageEntry, out var outerCounterEntry);
        Assert.NotNull(outerCounterEntry?.Content);
        var outerCounterData = JsonSerializer.Deserialize<KernelProcessStepStateMetadata>(outerCounterEntry?.Content!);
        Assert.NotNull(outerCounterData?.State?.ToString());
        var counterStateData = JsonSerializer.Deserialize<KernelProcessEventData>(outerCounterData.State.ToString()!)?.ToObject();
        Assert.NotNull(counterStateData);
        Assert.IsType<CommonSteps.CounterState>(counterStateData);
        Assert.Equal(expectedCount, ((CommonSteps.CounterState)counterStateData).Count);
    }

    [Fact]
    public async Task StartProcessWithKeyedProcessUseOfInternalNestedStatefulStepsAndAllOfInternallyAndExternallyAsync()
    {
        // Arrange
        var processId = "myProcessId";
        var mergeStepStorageEntry = "{0}.MergeStringsStep.StepEdgesData";
        var processKey = CommonProcesses.ProcessKeys.InternalNestedCounterWithEvenDetectionAndMergeProcess;

        var processStorage = new MockStorage();
        // To use local storage, comment line above and uncomment line below + replacing <TEST_DIR> with existing directory path
        //var processStorage = new JsonFileStorage("<TEST_DIR>");

        Kernel kernel = new();
        var iterationCount = 4;

        string? mergeStepFullEntry = null;

        for (int i = 1; i <= iterationCount; i++)
        {
            // Act - 1,2,3,4
            await using LocalKernelProcessContext runningProcess = await LocalKernelProcessFactory.StartAsync(
                kernel, this._keyedProcesses, processKey, processId, new KernelProcessEvent()
                {
                    Id = CommonProcesses.ProcessEvents.StartProcess,
                    Data = i.ToString(),
                }, storageConnector: processStorage);

            // Assert - 1,2,3,4
            var processState = await runningProcess.GetStateAsync();
            Assert.NotNull(processState);
            Assert.Equal(processId, processState.State.RunId);

            mergeStepFullEntry ??= string.Format(mergeStepStorageEntry, processState.Steps.Where(s => s.State.StepId == "MergeStringsStep").FirstOrDefault()?.State.RunId);
            processStorage._dbMock.TryGetValue(mergeStepFullEntry, out var mergeStorageEntry);
            Assert.NotNull(mergeStorageEntry?.Content);

            var mergeEdgeData = JsonSerializer.Deserialize<StorageStepEdgesData>(mergeStorageEntry.Content);
            Assert.NotNull(mergeEdgeData);
            Assert.Single(mergeEdgeData.EdgesData);
            Assert.Single(mergeEdgeData.EdgesData.Values);
            if (i < 4)
            {
                // outer merge is waiting on missing parameters pending from internal nested subprocess
                // in the meantime on each iteration, the only piped event/parameter keeps changing
                Assert.Single(mergeEdgeData.EdgesData.Values.First().Values);
                var firstEventValue = mergeEdgeData.EdgesData.Values.First().Values.First()?.ToObject();
                Assert.Equal(i.ToString(), firstEventValue?.ToString());
            }
            else
            {
                // finally the missing event, that is piped for 2 parameters, arrived and now the merge edge data is empty since it was processed
                Assert.Empty(mergeEdgeData.EdgesData.Values.First().Values);
            }
        }
    }

    /// <summary>
    /// A class that represents a step for testing.
    /// </summary>
    [Fact]
    public void ProcessWithSubprocessAndInvalidTargetThrows()
    public async Task ProcessWithSubprocessAndInvalidTargetThrowsAsync()
    {
        // Arrange
        ProcessBuilder process = new(nameof(ProcessWithSubprocessAndInvalidTargetThrows));
        ProcessBuilder process = new(nameof(ProcessWithSubprocessAndInvalidTargetThrowsAsync));

        ProcessBuilder subProcess = new("SubProcess");
        ProcessStepBuilder innerStep = subProcess.AddStepFromType<TestStep>("InnerStep");
        subProcess
            .OnInputEvent("Go")
            .SendEventTo(new ProcessFunctionTargetBuilder(innerStep));
        process
            .OnInputEvent("Start")
            .SendEventTo(subProcess.WhereInputEventIs("Go"));

        ProcessStepBuilder outerStep = process.AddStepFromType<TestStep>("OuterStep");
        innerStep
            .OnEvent(TestStep.EventId)
            .SendEventTo(new ProcessFunctionTargetBuilder(outerStep));

        KernelProcess processInstance = process.Build();
        Kernel kernel = new();

        // Act & Assert
        await Assert.ThrowsAsync<InvalidOperationException>(
            () =>
                processInstance.StartAsync(
                    kernel,
                    new KernelProcessEvent
                    {
                        Id = "Start"
                    }));

    }

    /// <summary>
    /// A class that represents a step for testing.
    /// </summary>
    private sealed class FailedStep : KernelProcessStep
    {
        /// <summary>
        /// A method that represents a function for testing.
        /// </summary>
        [KernelFunction]
        public void TestFailure()
        {
            throw new InvalidOperationException("I failed!");
        }
    }

    /// <summary>
    /// A class that represents a step for testing.
    /// </summary>
    private sealed class ErrorStep : KernelProcessStep
    {
        /// <summary>
        /// A method for unhandling failures at the process level.
        /// </summary>
        [KernelFunction]
        public void GlobalErrorHandler(KernelProcessError exception, Kernel kernel)
        {
            kernel.Data.Add("error-global", exception);
        }

        /// <summary>
        /// A method for unhandling failures at the function level.
        /// </summary>
        [KernelFunction]
        public void FunctionErrorHandler(KernelProcessError exception, Kernel kernel)
        {
            kernel.Data.Add("error-function", exception);
        }
    }

    /// <summary>
    /// A class that represents a step for testing.
    /// A class that represents a step for testing.
    /// </summary>
    private sealed class TestStep : KernelProcessStep
    {
        public const string EventId = "Next";
        public const string Name = nameof(TestStep);

        [KernelFunction]
        public async Task TestFunctionAsync(KernelProcessStepContext context)
        {
            await context.EmitEventAsync(new() { Id = EventId });
        }
    }
}
