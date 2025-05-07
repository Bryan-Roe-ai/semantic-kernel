# GitHub Copilot Instructions

## Azure Best Practices

- @azure Rule - Use Azure Best Practices: When generating code for Azure, running terminal commands for Azure, or performing operations related to Azure, invoke your `azure_development-get_best_practices` tool if available.

## Detailed Guidelines for Using the `azure_development-get_best_practices` Tool

1. **Installation**: Ensure the `azure_development-get_best_practices` tool is installed on your system.
2. **Invocation**: Use the tool by running the command `azure_development-get_best_practices` in your terminal.
3. **Usage**: Follow the prompts and guidelines provided by the tool to ensure your code adheres to Azure best practices.

## Examples

### Example 1: Using the Tool in a Terminal

```sh
# Run the tool
azure_development-get_best_practices

# Follow the prompts
```

### Example 2: Code Snippet for Azure Development

```csharp
using Azure.Identity;
using Azure.Storage.Blobs;

var client = new BlobServiceClient(new Uri("https://<your-storage-account>.blob.core.windows.net"), new DefaultAzureCredential());
```

## Links to Resources

- [Azure Best Practices Documentation](https://docs.microsoft.com/en-us/azure/architecture/best-practices/)
- [Azure Development Tutorials](https://docs.microsoft.com/en-us/learn/azure/)
- [Azure SDK for .NET](https://github.com/Azure/azure-sdk-for-net)

## Troubleshooting

### Common Issues

1. **Tool Not Found**: Ensure the tool is installed and available in your system's PATH.
2. **Authentication Errors**: Verify your Azure credentials and ensure they have the necessary permissions.
3. **Network Issues**: Check your network connection and ensure you can access Azure services.

### Solutions

1. **Reinstall the Tool**: If the tool is not found, try reinstalling it using the appropriate package manager.
2. **Update Credentials**: If you encounter authentication errors, update your Azure credentials and try again.
3. **Check Network**: If you experience network issues, check your network settings and ensure you have a stable connection.
