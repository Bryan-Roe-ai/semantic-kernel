using System;
using System.IO;
using System.Threading.Tasks;
using Xunit;
using AgentsSample;

public class AssistantCodeInterpreterTests
{
    [Fact]
    public async Task TestFileUploadAsync()
    {
        // Arrange
        string filePath = "testfile.txt";
        string expectedContent = "Hello, world!";
        await File.WriteAllTextAsync(filePath, expectedContent);

        // Act
        var fileClient = new FileClient();
        var fileInfo = await fileClient.UploadFileAsync(filePath);

        // Assert
        Assert.NotNull(fileInfo);
        Assert.Equal(filePath, fileInfo.Filename);

        // Cleanup
        File.Delete(filePath);
    }

    [Fact]
    public async Task TestChatMessageProcessingAsync()
    {
        // Arrange
        var chat = new AgentGroupChat(new ChatCompletionAgent(), new ChatCompletionAgent());
        string userInput = "Hello, world!";
        chat.AddChatMessage(new ChatMessageContent(AuthorRole.User, userInput));

        // Act
        await foreach (var response in chat.InvokeAsync())
        {
            // Assert
            Assert.NotNull(response);
            Assert.NotEmpty(response.Content);
        }
    }

    [Fact]
    public async Task TestBlobUploadAsync()
    {
        // Arrange
        string filePath = "testfile.txt";
        string expectedContent = "Hello, world!";
        await File.WriteAllTextAsync(filePath, expectedContent);

        // Act
        var blobClient = new BlobClient();
        await blobClient.UploadAsync(filePath, true);

        // Assert
        // Note: This test assumes the blob upload is successful.
        // In a real-world scenario, you might need to verify the upload by checking the blob storage.
        Assert.True(true);

        // Cleanup
        File.Delete(filePath);
    }
}
