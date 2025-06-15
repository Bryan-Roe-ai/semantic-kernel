# Custom LLM Integration with Semantic Kernel

This project demonstrates how to create a custom Large Language Model (LLM) implementation, train it, and integrate it with Microsoft's Semantic Kernel framework in Java.

## Overview

The example shows:

1. How to implement a custom text generation service (`MyCustomTextGenerationService`)
2. How to register the custom service with the Semantic Kernel
3. Different ways to invoke the service (direct generation, prompt functions, streaming)
4. How to train and fine-tune your custom LLM with training examples
5. How to integrate with Azure ML for more advanced training scenarios
6. How to use multiple LLMs in a single application

## Project Structure

- `MyCustomTextGenerationService.java` - Implementation of a custom text generation service with training capabilities
- `TrainableLLM.java` - Interface defining methods for LLM training and evaluation
- `CustomLLMExample.java` - Main class demonstrating basic usage of the custom LLM
- `TrainLLMExample.java` - Example showing how to train and evaluate the custom LLM
- `AzureLLMIntegration.java` - Example showing integration with Azure OpenAI services
- `AzureMLTrainingExample.java` - Example demonstrating integration with Azure ML for training
- `pom.xml` - Project dependencies and build configuration

## Prerequisites

- Java JDK 17 or higher
- Maven 3.6 or higher
- Access to Azure OpenAI service (optional for Azure integration example)

## Getting Started

### Setting Up Azure OpenAI (Optional)

To run the Azure integration example, set the following environment variables:

```bash
export AZURE_OPENAI_KEY=<your-azure-openai-key>
export AZURE_OPENAI_ENDPOINT=<your-azure-openai-endpoint>
export AZURE_OPENAI_DEPLOYMENT=<your-azure-openai-deployment-name>
```

### Building and Running the Project

1. Build the project with Maven:

```bash
mvn clean package
```

2. Run the basic example:

```bash
java -cp target/semantic-kernel-custom-llm-1.0-SNAPSHOT-jar-with-dependencies.jar com.microsoft.samples.CustomLLMExample
```

3. Run the basic LLM training example:

```bash
java -cp target/semantic-kernel-custom-llm-1.0-SNAPSHOT-jar-with-dependencies.jar com.microsoft.samples.TrainLLMExample
```

4. Run the Azure integration example:

```bash
java -cp target/semantic-kernel-custom-llm-1.0-SNAPSHOT-jar-with-dependencies.jar com.microsoft.samples.AzureLLMIntegration
```

5. Run the Azure ML training example:

```bash
java -cp target/semantic-kernel-custom-llm-1.0-SNAPSHOT-jar-with-dependencies.jar com.microsoft.samples.AzureMLTrainingExample
```

## Customizing the LLM

To customize the LLM behavior:

1. Modify the `MyCustomTextGenerationService` class to implement your own LLM logic
2. Adapt the response generation in `getTextContentAsync` and `getStreamingTextContentAsync` methods
3. Customize the training implementation in `trainAsync` and `trainFromFileAsync` methods
4. Implement more sophisticated training and evaluation metrics
5. Integrate with real model frameworks like PyTorch, TensorFlow, or commercial APIs

## Azure Best Practices

The `AzureLLMIntegration` and `AzureMLTrainingExample` classes demonstrate several Azure best practices:

- Secure handling of credentials using environment variables
- Using `AzureKeyCredential` for authentication
- Proper error handling for Azure service integration
- Implementation of service fallback strategies
- Configuration of service-specific parameters

## Training and Fine-tuning Capabilities

The training implementation demonstrates:

1. Creating a training interface (`TrainableLLM`) to extend LLM functionality
2. Implementing methods for training from examples and files
3. Creating training configurations with hyperparameters
4. Evaluating model performance with custom metrics
5. Saving and loading trained models
6. Integration with Azure ML for advanced training workflows

Training data is represented as prompt-completion pairs, allowing the model to learn specific responses for given inputs. The implementation includes:

- In-memory training data management
- File-based training data loading
- Simulated training loops with configurable hyperparameters
- Basic evaluation metrics calculation
- Model versioning and persistence

## Additional Resources

- [Semantic Kernel Documentation](https://learn.microsoft.com/en-us/semantic-kernel/overview/)
- [Semantic Kernel Java SDK Repository](https://github.com/microsoft/semantic-kernel/tree/main/java)
- [Azure OpenAI Services Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [Azure Machine Learning Documentation](https://learn.microsoft.com/en-us/azure/machine-learning/)
- [Fine-tuning Models with Azure OpenAI](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/fine-tuning)
- [Best Practices for ML Training on Azure](https://learn.microsoft.com/en-us/azure/architecture/data-guide/big-data/ai-machine-learning-training-optimization)
