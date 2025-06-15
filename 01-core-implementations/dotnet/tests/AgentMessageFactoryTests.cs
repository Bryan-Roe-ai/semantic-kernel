using System;
using System.Collections.Generic;
using Microsoft.SemanticKernel.Agents.AzureAI.Internal;
using Microsoft.SemanticKernel.ChatCompletion;
using Xunit;

public class AgentMessageFactoryTests
{
    [Fact]
    public void Test_MetadataProcessing_ShouldPass()
    {
        // Arrange
        var message = new ChatMessageContent
        {
            Metadata = new Dictionary<string, object>
            {
                { "Key1", "Value1" },
                { "Key2", "Value2" }
            }
        };

        // Act
        var result = AgentMessageFactory.TestMetadataProcessing(message);

        // Assert
        Assert.True(result);
    }

    [Fact]
    public void Test_ToolRegistrationAndExecution_ShouldPass()
    {
        // Arrange
        var toolName = "TestTool";

        // Act
        var result = AgentMessageFactory.TestToolRegistrationAndExecution(toolName);

        // Assert
        Assert.True(result);
    }
}
