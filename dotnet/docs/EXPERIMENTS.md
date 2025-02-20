# Experiments

The following capabilities are marked experimental in the .NET SDK. Once the APIs for these features are stable, the experimental attribute will be removed. In the meantime, these features are subject to change.

You can use the following diagnostic IDs to ignore warnings or errors for a particular experimental feature. For example, to ignore warnings for the embedding services, add `SKEXP0001` to your list of ignored warnings in your .NET project file as well as the ID for the embedding service you want to use. For example:

<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
<<<<<<< main
>>>>>>> Stashed changes
=======
<<<<<<< main
<<<<<<< main
>>>>>>> Stashed changes
```xml {"id":"01J6KNVXZHXHYS15JPS6S743K4"}
=======
```xml {"id":"01J60JDT3YV637KKDXXWHNG3JR"}
>>>>>>> origin/Bryan-Roe/issue389
<PropertyGroup>
  <NoWarn>SKEXP0001,SKEXP0010</NoWarn>
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
```xml {"id":"01J6KNVXZHXHYS15JPS6S743K4"}
```xml {"id":"01J60JDT3YV637KKDXXWHNG3JR"}
<PropertyGroup>
  <NoWarn>$(NoWarn);SKEXP0001,SKEXP0010</NoWarn>
>>>>>>> origin/main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
<<<<<<< div
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> head
```xml {"id":"01J6KNVXZHXHYS15JPS6S743K4"}
```xml {"id":"01J60JDT3YV637KKDXXWHNG3JR"}
<PropertyGroup>
  <NoWarn>$(NoWarn);SKEXP0001,SKEXP0010</NoWarn>
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
>>>>>>> head
</PropertyGroup>
```

## Experimental Feature Codes

| SKEXP​    | Experimental Features Category​​  |
| --------- | --------------------------------- |
| SKEXP0001 | Semantic Kernel core features     |
| SKEXP0010 | OpenAI and Azure OpenAI services  |
| SKEXP0020 | Memory connectors                 |
| SKEXP0040 | Function types                    |
| SKEXP0050 | Out-of-the-box plugins            |
| SKEXP0060 | Planners                          |
| SKEXP0070 | AI connectors                     |
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
| SKEXP0100 | Advanced Semantic Kernel features |
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< main
| SKEXP0100 | Advanced Semantic Kernel features |
=======
=======
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
<<<<<<< main
| SKEXP0100 | Advanced Semantic Kernel features |
=======
>>>>>>> Stashed changes
=======
<<<<<<< main
| SKEXP0100 | Advanced Semantic Kernel features |
=======
>>>>>>> Stashed changes
>>>>>>> head
| SKEX| SKEXP​ | Experimental Features Category​​ |
| SKEXP | Experimental Features Category |
|-------|--------------------------------|
| SKEXP0001 | Semantic Kernel core features |
| SKEXP0010 | OpenAI and Azure OpenAI services |
| SKEXP0020 | Memory connectors |
| SKEXP0040 | Function types |
| SKEXP0050 | Out-of-the-box plugins |
| SKEXP0060 | Planners |
| SKEXP0070 | AI connectors |
| SKEXP0080 | Processes |
<<<<<<< main
<<<<<<< main
| Advanced Semantic Kernel features |
=======
>>>>>>> ms/main
| SKEXP0100 | Advanced Semantic Kernel features |
| SKEXP0110 | Semantic Kernel Agents |
<<<<<<< main
<<<<<<< main
=======
>>>>>>> origin/main
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
>>>>>>> origin/main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
<<<<<<< div
>>>>>>> main
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> origin/main
>>>>>>> head
<<<<<<< main
=======
| SKEXP0120 | Native-AOT |
>>>>>>> upstream/main
=======
>>>>>>> origin/main

## Experimental Features Tracking

| SKEXP​    | Features​​                          | API docs​​ | Learn docs​​ | Samples​​ | Issues​​ | Implementations​ |
| --------- | ----------------------------------- | ---------- | ------------ | --------- | -------- | ---------------- |
| SKEXP0001 | Embedding services                  |            |              |           |          |                  |
| SKEXP0001 | Image services                      |            |              |           |          |                  |
| SKEXP0001 | Memory connectors                   |            |              |           |          |                  |
| SKEXP0001 | Kernel filters                      |            |              |           |          |                  |
| SKEXP0001 | Audio services                      |            |              |           |          |                  |
|           |                                     |            |              |           |          |                  |
| SKEXP0010 | Azure OpenAI with your data service |            |              |           |          |                  |
| SKEXP0010 | OpenAI embedding service            |            |              |           |          |                  |
| SKEXP0010 | OpenAI image service                |            |              |           |          |                  |
| SKEXP0010 | OpenAI parameters                   |            |              |           |          |                  |
| SKEXP0010 | OpenAI chat history extension       |            |              |           |          |                  |
| SKEXP0010 | OpenAI file service                 |            |              |           |          |                  |
|           |                                     |            |              |           |          |                  |
| SKEXP0020 | Hugging Face AI connector           |            |              |           |          |                  |
| SKEXP0020 | Azure AI Search memory connector    |            |              |           |          |                  |
| SKEXP0020 | Chroma memory connector             |            |              |           |          |                  |
| SKEXP0020 | DuckDB memory connector             |            |              |           |          |                  |
| SKEXP0020 | Kusto memory connector              |            |              |           |          |                  |
| SKEXP0020 | Milvus memory connector             |            |              |           |          |                  |
| SKEXP0020 | Qdrant memory connector             |            |              |           |          |                  |
| SKEXP0020 | Redis memory connector              |            |              |           |          |                  |
| SKEXP0020 | Sqlite memory connector             |            |              |           |          |                  |
| SKEXP0020 | Weaviate memory connector           |            |              |           |          |                  |
| SKEXP0020 | MongoDB memory connector            |            |              |           |          |                  |
| SKEXP0020 | Pinecone memory connector           |            |              |           |          |                  |
| SKEXP0020 | Postgres memory connector           |            |              |           |          |                  |
|           |                                     |            |              |           |          |                  |
| SKEXP0040 | GRPC functions                      |            |              |           |          |                  |
| SKEXP0040 | Markdown functions                  |            |              |           |          |                  |
| SKEXP0040 | OpenAPI functions                   |            |              |           |          |                  |
| SKEXP0040 | OpenAPI function extensions         |            |              |           |          |                  |
|           |                                     |            |              |           |          |                  |
| SKEXP0050 | Core plugins                        |            |              |           |          |                  |
| SKEXP0050 | Document plugins                    |            |              |           |          |                  |
| SKEXP0050 | Memory plugins                      |            |              |           |          |                  |
| SKEXP0050 | Microsoft 365 plugins               |            |              |           |          |                  |
| SKEXP0050 | Web plugins                         |            |              |           |          |                  |
| SKEXP0050 | Text chunker plugin                 |            |              |           |          |                  |
|           |                                     |            |              |           |          |                  |
| SKEXP0060 | Handlebars planner                  |            |              |           |          |                  |
| SKEXP0060 | OpenAI Stepwise planner             |            |              |           |          |                  |
|           |                                     |            |              |           |          |                  |
| SKEXP0070 | Ollama AI connector                 |            |              |           |          |                  |
| SKEXP0070 | Gemini AI connector                 |            |              |           |          |                  |
| SKEXP0070 | Mistral AI connector                |            |              |           |          |                  |
| SKEXP0070 | Assembly AI connector               |            |              |           |          |                  |
|           |                                     |            |              |           |          |                  |
| SKEXP0101 | Experiment with Assistants          |            |              |           |          |                  |
| SKEXP0101 | Experiment with Flow Orchestration  |            |              |           |          |                  |
| SKEXP​ | Features​​ |
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< main
=======
<<<<<<< div
=======
>>>>>>> main
=======
>>>>>>> head
=======
>>>>>>> origin/main
=======
=======
<<<<<<< main
=======
=======
>>>>>>> Stashed changes
=======
<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
>>>>>>> Stashed changes
<<<<<<< main
=======
=======
>>>>>>> Stashed changes
| SKEXP0100 | Advanced Semantic Kernel features |
| SKEXP0110 | Semantic Kernel Agents |

## Experimental Features Tracking

| SKEXP | Features |
>>>>>>> ms/feature-connectors-assemblyai
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
>>>>>>> origin/main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
<<<<<<< div
>>>>>>> main
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> origin/main
>>>>>>> head
|-------|----------|
| SKEXP0001 | Embedding services |
| SKEXP0001 | Image services |
| SKEXP0001 | Memory connectors |
| SKEXP0001 | Kernel filters |
| SKEXP0001 | Audio services |
| | | | | | | |
| SKEXP0010 | Azure OpenAI with your data service |
| SKEXP0010 | OpenAI embedding service |
| SKEXP0010 | OpenAI image service |
| SKEXP0010 | OpenAI parameters |
| SKEXP0010 | OpenAI chat history extension |
| SKEXP0010 | OpenAI file service |
| | | | | | | |
| SKEXP0020 | Azure AI Search memory connector |
| SKEXP0020 | Chroma memory connector |
| SKEXP0020 | DuckDB memory connector |
| SKEXP0020 | Kusto memory connector |
| SKEXP0020 | Milvus memory connector |
| SKEXP0020 | Qdrant memory connector |
| SKEXP0020 | Redis memory connector |
| SKEXP0020 | Sqlite memory connector |
| SKEXP0020 | Weaviate memory connector |
| SKEXP0020 | MongoDB memory connector |
| SKEXP0020 | Pinecone memory connector |
| SKEXP0020 | Postgres memory connector |
| | | | | | | |
| SKEXP0040 | GRPC functions |
| SKEXP0040 | Markdown functions |
| SKEXP0040 | OpenAPI functions |
| SKEXP0040 | OpenAPI function extensions |
| SKEXP0040 | Prompty Format support |
| | | | | | | |
| SKEXP0050 | Core plugins |
| SKEXP0050 | Document plugins |
| SKEXP0050 | Memory plugins |
| SKEXP0050 | Microsoft 365 plugins |
| SKEXP0050 | Web plugins |
| SKEXP0050 | Text chunker plugin |
| | | | | | | |
| SKEXP0060 | Handlebars planner |
| SKEXP0060 | OpenAI Stepwise planner |
| | | | | | | |
| SKEXP0070 | Ollama AI connector |
| SKEXP0070 | Gemini AI connector |
| SKEXP0070 | Mistral AI connector |
| SKEXP0070 | ONNX AI connector |
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
| SKEXP0070 | Hugging Face AI connector |
| | | | | | | |
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< main
| SKEXP0070 | Hugging Face AI connector |
| | | | | | | |
=======
<<<<<<< div
=======
>>>>>>> main
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
| SKEXP0070 | Assembly AI connector               |            |              |           |          |                  |
| SKEXP0070 | Hugging Face AI connector |
| | | | | | | |
| SKEXP0080 | Process Framework |
| | | | | | | |
<<<<<<< div
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
>>>>>>> head
>>>>>>> origin/main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
<<<<<<< div
>>>>>>> main
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> origin/main
>>>>>>> head
| SKEXP0101 | Experiment with Assistants |
| SKEXP0101 | Experiment with Flow Orchestration |
| | | | | | | |
| SKEXP0110 | Agent Framework |
<<<<<<< main
<<<<<<< main
=======
| | | | | | | |
| SKEXP0120 | Native-AOT |
>>>>>>> upstream/main
=======
>>>>>>> origin/main

# Experiments

The following capabilities are marked experimental in the .NET SDK. Once the APIs for these features are stable, the experimental attribute will be removed. In the meantime, these features are subject to change.

You can use the following diagnostic IDs to ignore warnings or errors for a particular experimental feature. For example, to ignore warnings for the embedding services, add `SKEXP0001` to your list of ignored warnings in your .NET project file as well as the ID for the embedding service you want to use. For example:

```xml
<PropertyGroup>
  <NoWarn>SKEXP0001,SKEXP0010</NoWarn>
</PropertyGroup>
<PropertyGroup>
  <NoWarn>$(NoWarn);SKEXP0001,SKEXP0010</NoWarn>
</PropertyGroup>
<PropertyGroup>
  <NoWarn>$(NoWarn);SKEXP0001,SKEXP0010</NoWarn>
</PropertyGroup>
```

## Experimental Feature Codes

| SKEXP​    | Experimental Features Category​​  |
| --------- | --------------------------------- |
| SKEXP0001 | Semantic Kernel core features     |
| SKEXP0010 | OpenAI and Azure OpenAI services  |
| SKEXP0020 | Memory connectors                 |
| SKEXP0040 | Function types                    |
| SKEXP0050 | Out-of-the-box plugins            |
| SKEXP0060 | Planners                          |
| SKEXP0070 | AI connectors                     |
| SKEXP0100 | Advanced Semantic Kernel features |
| SKEXP​    | Experimental Features Category​​  |
| SKEXP0010 | OpenAI and Azure OpenAI services |
| SKEXP0020 | Memory connectors |
| SKEXP0040 | Function types |
| SKEXP0050 | Out-of-the-box plugins |
| SKEXP0060 | Planners |
| SKEXP0070 | AI connectors |
| SKEXP0080 | Processes                          |
| SKEXP0100 | Advanced Semantic Kernel features  |
| SKEXP0110 | Semantic Kernel Agents |

## Experimental Features Tracking

| SKEXP0001 | Embedding services                  |            |              |           |          |                  |
| SKEXP0001 | Image services                      |            |              |           |          |                  |
| SKEXP0001 | Memory connectors                   |            |              |           |          |                  |
| SKEXP0001 | Kernel filters                      |            |              |           |          |                  |
| SKEXP0001 | Audio services                      |            |              |           |          |                  |
|           |                                     |            |              |           |          |                  |
| SKEXP0010 | Azure OpenAI with your data service |            |              |           |          |                  |
| SKEXP0010 | OpenAI embedding service            |            |              |           |          |                  |
| SKEXP0010 | OpenAI image service                |            |              |           |          |                  |
| SKEXP0010 | OpenAI parameters                   |            |              |           |          |                  |
| SKEXP0010 | OpenAI chat history extension       |            |              |           |          |                  |
| SKEXP0010 | OpenAI file service                 |            |              |           |          |                  |
|           |                                     |            |              |           |          |                  |
| SKEXP0020 | Hugging Face AI connector           |            |              |           |          |                  |
| SKEXP0020 | Azure AI Search memory connector    |            |              |           |          |                  |
| SKEXP0020 | Chroma memory connector             |            |              |           |          |                  |
| SKEXP0020 | DuckDB memory connector             |            |              |           |          |                  |
| SKEXP0020 | Kusto memory connector              |            |              |           |          |                  |
| SKEXP0020 | Milvus memory connector             |            |              |           |          |                  |
| SKEXP0020 | Qdrant memory connector             |            |              |           |          |                  |
| SKEXP0020 | Redis memory connector              |            |              |           |          |                  |
| SKEXP0020 | Sqlite memory connector             |            |              |           |          |                  |
| SKEXP0020 | Weaviate memory connector           |            |              |           |          |                  |
| SKEXP0020 | MongoDB memory connector            |            |              |           |          |                  |
| SKEXP0020 | Pinecone memory connector           |            |              |           |          |                  |
| SKEXP0020 | Postgres memory connector           |            |              |           |          |                  |
|           |                                     |            |              |           |          |                  |
| SKEXP0040 | GRPC functions                      |            |              |           |          |                  |
| SKEXP0040 | Markdown functions                  |            |              |           |          |                  |
| SKEXP0040 | OpenAPI functions                   |            |              |           |          |                  |
| SKEXP0040 | OpenAPI function extensions         |            |              |           |          |                  |
|           |                                     |            |              |           |          |                  |
| SKEXP0050 | Core plugins                        |            |              |           |          |                  |
| SKEXP0050 | Document plugins                    |            |              |           |          |                  |
| SKEXP0050 | Memory plugins                      |            |              |           |          |                  |
| SKEXP0050 | Microsoft 365 plugins               |            |              |           |          |                  |
| SKEXP0050 | Web plugins |
| SKEXP0050 | Text chunker plugin                 |            |              |           |          |                  |
|           |                                     |            |              |           |          |                  |
| SKEXP0060 | Handlebars planner                  |            |              |           |          |                  |
| SKEXP0060 | OpenAI Stepwise planner             |            |              |           |          |                  |
|           |                                     |            |              |           |          |                  |
| SKEXP0070 | Ollama AI connector                 |            |              |           |          |                  |
| SKEXP0070 | Gemini AI connector                 |            |              |           |          |                  |
| SKEXP0070 | Mistral AI connector                |            |              |           |          |                  |
|           |                                     |            |              |           |          |                  |
| SKEXP0101 | Experiment with Assistants          |            |              |           |          |                  |
| SKEXP0101 | Experiment with Flow Orchestration  |            |              |           |          |                  |

| SKEXP​    | Features​​                          | API docs​​ | Learn docs​​ | Samples​​ | Issues​​ | Implementations​ |
| --------- | ----------------------------------- | ---------- | ------------ | --------- | -------- | ---------------- |

## Complete Features List

| SKEXP | Features |
|-------|----------|
| SKEXP0001 | Embedding services |
| SKEXP0001 | Image services |
| SKEXP0001 | Memory connectors |
| SKEXP0001 | Kernel filters |
| SKEXP0001 | Audio services |
| SKEXP0010 | OpenAI embedding service |
| SKEXP0010 | OpenAI image service |
| SKEXP0010 | OpenAI parameters |
| SKEXP0010 | OpenAI chat history extension |
| SKEXP0010 | OpenAI file service |
| SKEXP0020 | Azure AI Search memory connector |
| SKEXP0020 | Chroma memory connector |
| SKEXP0020 | DuckDB memory connector |
| SKEXP0020 | Milvus memory connector |
| SKEXP0020 | Qdrant memory connector |
| SKEXP0020 | Redis memory connector |
| SKEXP0020 | Sqlite memory connector |
| SKEXP0020 | Weaviate memory connector |
| SKEXP0020 | MongoDB memory connector |
| SKEXP0020 | Pinecone memory connector |
| SKEXP0020 | Postgres memory connector |
| | |
| SKEXP0040 | GRPC functions |
| SKEXP0040 | Markdown functions |
| SKEXP0040 | OpenAPI functions |
| SKEXP0040 | OpenAPI function extensions - API Manifest |
| SKEXP0040 | OpenAPI function extensions - Copilot Agent Plugin |
| SKEXP0040 | Prompty Format support |
| | |
| SKEXP0050 | Core plugins |
| SKEXP0050 | Document plugins |
| SKEXP0050 | Memory plugins |
| SKEXP0050 | Microsoft 365 plugins |
| SKEXP0050 | Web plugins |
| SKEXP0050 | Text chunker plugin |
| | |
| SKEXP0060 | Handlebars planner |
| SKEXP0060 | OpenAI Stepwise planner |
| | |
| SKEXP0070 | Ollama AI connector |
| SKEXP0070 | Gemini AI connector |
| SKEXP0070 | Hugging Face AI connector |
| SKEXP0070 | Assembly AI connector |
| SKEXP0070 | Hugging Face AI connector |
| SKEXP0101 | Experiment with Assistants |
| SKEXP0101 | Experiment with Flow Orchestration |
| | |
| SKEXP0110 | Agent Framework |
<<<<<<< HEAD
| | |
=======
| | | | | | | |
>>>>>>> 5ae74d7dd619c0f30c1db7a041ecac0f679f9377
| SKEXP0120 | Native-AOT |
