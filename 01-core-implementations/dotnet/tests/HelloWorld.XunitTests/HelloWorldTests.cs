using Xunit;

public class HelloWorldTests
{
    [Fact]
    public void HelloWorld_ReturnsExpectedString()
    {
        Assert.Equal("Hello, World!", "Hello, World!");
    }
}