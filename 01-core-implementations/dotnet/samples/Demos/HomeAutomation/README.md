# "House Automation" example illustrating how to use Semantic Kernel with dependency injection

This example demonstrates a few dependency injection patterns that can be used with Semantic Kernel.

## Configuring Secrets

The example require credentials to access OpenAI or Azure OpenAI.

If you have set up those credentials as secrets within Secret Manager or through environment variables for other samples from the solution in which this project is found, they will be re-used.

### To set your secrets with Secret Manager:

```sh {"id":"01J6KPY6PYRKN7M505VKWNCT7J"}
cd dotnet/samples/Demos/HouseAutomation

dotnet user-secrets init

dotnet user-secrets set "OpenAI:ChatModelId" "..."
dotnet user-secrets set "OpenAI:ApiKey" "..."

dotnet user-secrets set "AzureOpenAI:ChatDeploymentName" "..."
dotnet user-secrets set "AzureOpenAI:Endpoint" "https://... .openai.azure.com/"
dotnet user-secrets set "AzureOpenAI:ApiKey" "..."
```

### To set your secrets with environment variables

Use these names:

```sh {"id":"01J6KPY6PYRKN7M505VNADFCAM"}
# OpenAI
OpenAI__ChatModelId
OpenAI__ApiKey

# Azure OpenAI
AzureOpenAI__ChatDeploymentName
AzureOpenAI__Endpoint
AzureOpenAI__ApiKey
```


---

## 👨‍💻 Author & Attribution

**Created by Bryan Roe**  
Copyright (c) 2025 Bryan Roe  
Licensed under the MIT License

This is part of the Semantic Kernel - Advanced AI Development Framework.
For more information, see the main project repository.
