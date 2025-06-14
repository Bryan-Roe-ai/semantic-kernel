// Copyright (c) Microsoft. All rights reserved.
using System;
using System.Collections.Generic;
using Xunit;

namespace Microsoft.SemanticKernel.Process.Core.UnitTests;

/// <summary>
/// Unit tests for <see cref="ProcessProxyBuilder"/>.
/// </summary>
public class ProcessProxyBuilderTests
{
    private readonly string _testProcessName = "testProcess";
    private readonly string _proxyName = "proxyTestName";
    private readonly string _topicName1 = "testTopic1";
    private readonly string _topicName2 = "testTopic2";
    private readonly string _topicName3 = "testTopic3";

    /// <summary>
    /// Verify initialization based on <see cref="ProcessStepBuilder"/>.
    /// </summary>
    [Fact]
    public void ProcessProxyBuilderInitialization()
    {
        // Arrange & Act
        ProcessProxyBuilder proxy = new([this._topicName1, this._topicName2, this._topicName3], this._proxyName, null);

        // Assert
        Assert.NotNull(proxy.StepId);
        Assert.NotNull(proxy.StepId);
        Assert.Equal(this._proxyName, proxy.StepId);
        Assert.True(proxy._externalTopicUsage.Count > 0);
    }

    /// <summary>
    /// Verify registered topics are different
    /// </summary>
    [Fact]
    public void ProcessProxyBuilderInitializationEmptyTopicsThrows()
    {
        // Arrange
        List<string> repeatedTopics = [];

        // Act & Assert
        Assert.Throws<ArgumentException>(() => new ProcessProxyBuilder(repeatedTopics, this._proxyName, null));
    }

    /// <summary>
    /// Verify registered topics are different
    /// </summary>
    [Fact]
    public void ProcessProxyBuilderInitializationRepeatedTopicsThrows()
    {
        // Arrange
        List<string> repeatedTopics = [this._topicName1, this._topicName1];

        // Act & Assert
        Assert.Throws<ArgumentException>(() => new ProcessProxyBuilder(repeatedTopics, this._proxyName, null));
    }

    /// <summary>
    /// Verify <see cref="ProcessProxyBuilder.BuildStep"/> produces the
    /// expected <see cref="KernelProcessProxy"/>.
    /// </summary>
    [Fact]
    public void ProcessProxyBuilderWillBuild()
    {
        // Arrange
        ProcessProxyBuilder proxy = new([this._topicName1], this._proxyName, null);

        ProcessBuilder process = new(this._testProcessName, null);
        ProcessStepBuilder stepSource = process.AddStepFromType<SimpleTestStep>();
        stepSource.OnFunctionResult().EmitExternalEvent(proxy, this._topicName1);

        // Act
        var proxyInfo = proxy.BuildStep(new ProcessBuilder("Test", null));

        // Assert
        Assert.NotNull(proxyInfo);
        Assert.IsType<KernelProcessProxy>(proxyInfo);
        Assert.Equal(proxy.StepId, proxyInfo.State.StepId);
        Assert.Equal(proxy.StepId, proxyInfo.State.RunId);
        var processProxy = (KernelProcessProxy)proxyInfo;
        Assert.NotNull(processProxy?.ProxyMetadata);
        Assert.Equal(proxy._eventMetadata, processProxy.ProxyMetadata.EventMetadata);
    }

    /// <summary>
    /// Verify <see cref="ProcessProxyBuilder.BuildStep"/> fails building
    /// when is registered topics are not linked properly
    /// </summary>
    [Fact]
    public void ProcessProxyBuilderWillNotLinkDueMultipleLinkingToSameTopicThrows()
    {
        // Arrange
        ProcessProxyBuilder proxy = new([this._topicName1], this._proxyName, null);

        ProcessBuilder process = new(this._testProcessName, null);
        ProcessStepBuilder stepSource1 = process.AddStepFromType<SimpleTestStep>("step1");
        ProcessStepBuilder stepSource2 = process.AddStepFromType<SimpleTestStep>("step2");
        stepSource1.OnFunctionResult().EmitExternalEvent(proxy, this._topicName1);

        // Act & Assert
        Assert.Throws<InvalidOperationException>(() => stepSource2.OnFunctionResult().EmitExternalEvent(proxy, this._topicName1));
    }

    /// <summary>
    /// Verify <see cref="ProcessProxyBuilder.BuildStep"/> fails building
    /// when is registered topics are not linked properly
    /// </summary>
    [Fact]
    public void ProcessProxyBuilderWillNotBuildDueMissingLinking()
    {
        // Arrange
        ProcessProxyBuilder proxy = new([this._topicName1], this._proxyName, null);

        // Act & Assert
        Assert.Throws<InvalidOperationException>(() => proxy.BuildStep(new ProcessBuilder("Test", null)));
    }

    private sealed class SimpleTestStep : KernelProcessStep
    {
        [KernelFunction]
        public string TestFunction()
        {
            return "Test function message";
        }
    }
}
