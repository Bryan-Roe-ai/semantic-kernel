# Function Invocation Approval

This console application shows how to use function invocation filter (`IFunctionInvocationFilter`) to invoke a Kernel Function only if such operation was approved.
If function invocation was rejected, the result will contain the reason why, so the LLM can respond appropriately.

The application uses a sample plugin which builds software by following these development stages: collection of requirements, design, implementation, testing and deployment.

Each step can be approved or rejected. Based on that, the LLM will decide how to proceed.

## Configuring Secrets

The example requires credentials to access OpenAI or Azure OpenAI.

If you have set up those credentials as secrets within Secret Manager or through environment variables for other samples from the solution in which this project is found, they will be re-used.

### To set your secrets with Secret Manager:

```sh {"id":"01J6KPS0HPMPG43QDVTATB8YGM"}
cd dotnet/samples/Demos/FunctionInvocationApproval

dotnet user-secrets init

dotnet user-secrets set "OpenAI:ChatModelId" "..."
dotnet user-secrets set "OpenAI:ApiKey" "..."

dotnet user-secrets set "AzureOpenAI:ChatDeploymentName" "..."
dotnet user-secrets set "AzureOpenAI:Endpoint" "https://... .openai.azure.com/"
dotnet user-secrets set "AzureOpenAI:ApiKey" "..."
```

### To set your secrets with environment variables

Use these names:

```sh {"id":"01J6KPS0HPMPG43QDVTE6CNSZZ"}
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
