// Copyright (c) Microsoft. All rights reserved.
using System;
using Xunit;

namespace Microsoft.SemanticKernel.Process.UnitTests;

/// <summary>
/// Unit testing of <see cref="KernelProcessMap"/>.
/// </summary>
public class KernelProcessMapTests
{
    /// <summary>
    /// Verify initialization.
    /// </summary>
    [Fact]
    public void KernelProcessMapStateInitialization()
    {
        // Arrange
<<<<<<< HEAD
        KernelProcessState processState = new("Operation");
        KernelProcess process = new(processState, [], []);
        KernelProcessMapState state = new(nameof(KernelProcessMapStateInitialization), Guid.NewGuid().ToString());
=======
        KernelProcessState processState = new("Operation", "vTest");
        KernelProcess process = new(processState, [], []);
        KernelProcessMapState state = new(nameof(KernelProcessMapStateInitialization), "vTest", Guid.NewGuid().ToString());
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377

        // Act
        KernelProcessMap map = new(state, process, []);

        // Assert
        Assert.Equal(state, map.State);
<<<<<<< HEAD
        //Assert.Equal("values", map.InputParameterName);
=======
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
        Assert.Equivalent(process, map.Operation);
        Assert.Empty(map.Edges);
    }

    /// <summary>
    /// Verify <see cref="KernelProcessMapState"/> requires a name and id
    /// </summary>
    [Fact]
<<<<<<< HEAD
    public void KernelProcessMapStateRequiresNameAndId()
    {
        // Act & Assert
        Assert.Throws<ArgumentNullException>(() => new KernelProcessMapState(name: null!, "testid"));
        Assert.Throws<ArgumentNullException>(() => new KernelProcessMapState("testname", null!));
=======
    public void KernelProcessMapStateRequiredProperties()
    {
        // Act & Assert
        Assert.Throws<ArgumentNullException>(() => new KernelProcessMapState(name: null!, "vTest", "testid"));
        Assert.Throws<ArgumentNullException>(() => new KernelProcessMapState(name: "testname", null!, "testid"));
        Assert.Throws<ArgumentNullException>(() => new KernelProcessMapState("testname", "vTest", null!));
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
    }
}
