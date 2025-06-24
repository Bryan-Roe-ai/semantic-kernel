# Microsoft.SemanticKernel.Connectors.MongoDB

This connector uses [MongoDB Atlas Vector Search](https://www.mongodb.com/products/platform/atlas-vector-search) to implement Semantic Memory.

## Quick Start

1. Create [Atlas cluster](https://www.mongodb.com/docs/atlas/getting-started/)
2. Create a [collection](https://www.mongodb.com/docs/atlas/atlas-ui/collections/)
3. Create [Vector Search Index](https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-overview/) for the collection. The index has to be defined on a field called `embedding`. For example:

```json {"id":"01J6KPS9K898EKX8242YK9Z46Z"}
{
  "type": "vectorSearch",
  "fields": [
    {
      "numDimensions": <number-of-dimensions>,
      "path": "embedding",
      "similarity": "euclidean | cosine | dotProduct",
      "type": "vector"
    }
  ]
}
```

4. Create the MongoDB memory store
   > See [Example 14](../../../samples/Concepts/Memory/SemanticTextMemory_Building.cs) and [Example 15](../../../samples/Concepts/Memory/TextMemoryPlugin_MultipleMemoryStore.cs) for more memory usage examples with the kernel.

```csharp {"id":"01J6KPS9K898EKX82432G8NQAE"}
var connectionString = "MONGODB ATLAS CONNECTION STRING"
MongoDBMemoryStore memoryStore = new(connectionString, "MyDatabase");

var embeddingGenerator = new OpenAITextEmbeddingGenerationService("text-embedding-ada-002", apiKey);

SemanticTextMemory textMemory = new(memoryStore, embeddingGenerator);

var memoryPlugin = kernel.ImportPluginFromObject(new TextMemoryPlugin(textMemory));
```

> Guide to find the connection string: https://www.mongodb.com/docs/manual/reference/connection-string/


---

## 👨‍💻 Author & Attribution

**Created by Bryan Roe**  
Copyright (c) 2025 Bryan Roe  
Licensed under the MIT License

This is part of the Semantic Kernel - Advanced AI Development Framework.
For more information, see the main project repository.
