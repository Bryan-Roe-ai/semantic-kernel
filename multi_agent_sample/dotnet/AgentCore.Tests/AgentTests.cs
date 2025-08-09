using AgentCore;
using Xunit;
using System; // Added for ArgumentException

namespace AgentCore.Tests;

public class AgentTests
{
    [Fact]
    public void Echo_Works()
    {
        var agent = new Agent("DotNetAgent");
        var result = agent.SendMessage("hello");
        Assert.Equal("DotNetAgent: hello", result);
    }

    [Fact]
    public void EmptyMessage_Throws()
    {
        var agent = new Agent("A");
        Assert.Throws<ArgumentException>(() => agent.SendMessage(""));
    }

    [Fact]
    public void CustomFormat_Works()
    {
        var settings = new AgentSettings { EchoFormat = "[{0}] {1}!" };
        var agent = new Agent("AgentX", settings);
        var result = agent.SendMessage("go");
        Assert.Equal("[AgentX] go!", result);
    }
}
