// Copyright (c) Microsoft. All rights reserved.

using System;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.SemanticKernel.Plugins.MsGraph;
using Microsoft.SemanticKernel.Plugins.MsGraph.Models;
using Moq;
using Xunit;
using static Microsoft.SemanticKernel.Plugins.MsGraph.TaskListPlugin;

namespace SemanticKernel.Plugins.UnitTests.MsGraph;

public class TaskListPluginTests
{
    private readonly TaskManagementTaskList _anyTaskList = new(
        id: Guid.NewGuid().ToString(),
        name: Guid.NewGuid().ToString());

    private readonly TaskManagementTask _anyTask = new(
        id: Guid.NewGuid().ToString(),
        title: Guid.NewGuid().ToString(),
        reminder: (DateTimeOffset.Now + TimeSpan.FromDays(1)).ToString("o"),
        due: DateTimeOffset.Now.ToString("o"),
        isCompleted: false);

    [Fact]
    public async Task AddTaskAsyncNoReminderSucceedsAsync()
    {
        // Arrange
        string anyTitle = Guid.NewGuid().ToString();

        Mock<ITaskManagementConnector> connectorMock = new();
        connectorMock.Setup(c => c.GetDefaultTaskListAsync(It.IsAny<CancellationToken>()))
            .ReturnsAsync(this._anyTaskList);

        connectorMock.Setup(c => c.AddTaskAsync(It.IsAny<string>(), It.IsAny<TaskManagementTask>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync(this._anyTask);

        TaskListPlugin target = new(connectorMock.Object);

        // Act
        await target.AddTaskAsync(anyTitle);

        // Assert
        connectorMock.VerifyAll();
    }

    [Fact]
    public async Task AddTaskAsyncWithReminderSucceedsAsync()
    {
        // Arrange
        string anyTitle = Guid.NewGuid().ToString();

        Mock<ITaskManagementConnector> connectorMock = new();
        connectorMock.Setup(c => c.GetDefaultTaskListAsync(It.IsAny<CancellationToken>()))
            .ReturnsAsync(this._anyTaskList);

        connectorMock.Setup(c => c.AddTaskAsync(It.IsAny<string>(), It.IsAny<TaskManagementTask>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync(this._anyTask);

        string anyReminder = (DateTimeOffset.Now + TimeSpan.FromHours(1)).ToString("o");

        TaskListPlugin target = new(connectorMock.Object);

        // Act
        await target.AddTaskAsync(anyTitle, anyReminder);

        // Assert
        connectorMock.VerifyAll();
    }

    [Fact]
    public async Task AddTaskAsyncNoDefaultTaskListFailsAsync()
    {
        // Arrange
        string anyTitle = Guid.NewGuid().ToString();

        Mock<ITaskManagementConnector> connectorMock = new();
#pragma warning disable CS8600 // Converting null literal or possible null value to non-nullable type.
        connectorMock.Setup(c => c.GetDefaultTaskListAsync(It.IsAny<CancellationToken>()))
            .ReturnsAsync((TaskManagementTaskList)null);
#pragma warning restore CS8600 // Converting null literal or possible null value to non-nullable type.

        string anyReminder = (DateTimeOffset.Now + TimeSpan.FromHours(1)).ToString("o");

        TaskListPlugin target = new(connectorMock.Object);

        // Act/Assert
        await Assert.ThrowsAnyAsync<InvalidOperationException>(() =>
           target.AddTaskAsync(anyTitle, anyReminder));

        // Assert
        connectorMock.VerifyAll();
    }

    [Theory]
    [InlineData(DayOfWeek.Sunday)]
    [InlineData(DayOfWeek.Monday)]
    [InlineData(DayOfWeek.Tuesday)]
    [InlineData(DayOfWeek.Wednesday)]
    [InlineData(DayOfWeek.Thursday)]
    [InlineData(DayOfWeek.Friday)]
    [InlineData(DayOfWeek.Saturday)]
    public void GetNextDayOfWeekIsCorrect(DayOfWeek dayOfWeek)
    {
        // Arrange
        DateTimeOffset today = new(DateTime.Today);
        TimeSpan timeOfDay = TimeSpan.FromHours(13);

        // Act
        DateTimeOffset actual = GetNextDayOfWeek(dayOfWeek, timeOfDay);

        // Assert
        Assert.Equal(dayOfWeek, actual.DayOfWeek);
        Assert.True(today.ToUnixTimeSeconds() < actual.ToUnixTimeSeconds());
        Assert.Equal(timeOfDay.Hours, actual.Hour);
    }
}
