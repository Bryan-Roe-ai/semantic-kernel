---
title: Azure Best Practices and GitHub Copilot Instructions
---
# Azure Best Practices and GitHub Copilot Instructions

## Introduction

This document provides guidelines for using the `azure_development-get_best_practices` tool and instructions for improving code based on user requests, as discussed in the chat thread. The information is intended to help developers adhere to Azure best practices and utilize GitHub Copilot effectively.

## Azure Best Practices

### "@azure Rule" Explained

The "@azure Rule" refers to a guideline for developers working with Azure-related code or operations. It emphasizes the importance of following Azure best practices by leveraging the `azure_development-get_best_practices` tool whenever applicable.

- **Use Azure Best Practices**: When generating code for Azure, running terminal commands for Azure, or performing operations related to Azure, invoke your `azure_development-get_best_practices` tool if available.

### Detailed Guidelines for Using the `azure_development-get_best_practices` Tool

1. **Installation**: Ensure the `azure_development-get_best_practices` tool is installed on your system.
2. **Invocation**: Use the tool by running the command `azure_development-get_best_practices` in your terminal.
3. **Usage**: Follow the prompts and guidelines provided by the tool to ensure your code adheres to Azure best practices.

### Examples

#### Example 1: Using the Tool in a Terminal

```sh
# Run the tool
azure_development-get_best_practices

# Follow the prompts

#### Example 2: Code Snippet for Azure Development

```csharp
using Azure.Identity;
using Azure.Storage.Blobs;

var client = new BlobServiceClient(new Uri("https://<your-storage-account>.blob.core.windows.net"), new DefaultAzureCredential());
```

### Links to Resources

- [Azure Best Practices Documentation](https://docs.microsoft.com/en-us/azure/architecture/best-practices/)
- [Azure Development Tutorials](https://docs.microsoft.com/en-us/learn/azure/)
- [Azure SDK for .NET](https://github.com/Azure/azure-sdk-for-net)

### Troubleshooting

#### Common Issues

1. **Tool Not Found**: Ensure the tool is installed and available in your system's PATH.
2. **Authentication Errors**: Verify your Azure credentials and ensure they have the necessary permissions.
3. **Network Issues**: Check your network connection and ensure you can access Azure services.

#### Solutions

1. **Reinstall the Tool**: If the tool is not found, try reinstalling it using the appropriate package manager.
2. **Update Credentials**: If you encounter authentication errors, update your Azure credentials and try again.
3. **Check Network**: If you experience network issues, check your network settings and ensure you have a stable connection.

## GitHub Copilot Instructions

### Task Overview

- When the user requests improvements to a file or code, analyze the provided file(s), make all reasonable improvements (including bug fixes, performance, readability, security, and style enhancements) according to best practices for the relevant language and project.
- Do not output partial files, diffs, explanations, or comments unless they are code comments inside the improved files.
- Do not ask any questions or request clarification; always proceed with the best improvements you can make based on the provided content and common sense.

## Conclusion

This document serves as a comprehensive guide for using the `azure_development-get_best_practices` tool and outlines the instructions for GitHub Copilot to improve code effectively. Following these guidelines will ensure adherence to Azure best practices and enhance code quality.

<SwmMeta version="3.0.0"><sup>Powered by [Swimm](https://app.swimm.io/)</sup></SwmMeta>
