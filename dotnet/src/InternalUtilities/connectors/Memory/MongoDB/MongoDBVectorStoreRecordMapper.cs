using System;
using Microsoft.SemanticKernel.Memory;

namespace Microsoft.SemanticKernel.Connectors.Memory.MongoDB;

internal sealed class MongoDBVectorStoreRecordMapper
{
	public MongoDBVectorStoreRecord ToRecord(MemoryRecord record)
	{
		return new MongoDBVectorStoreRecord
		{
			Id = record.Metadata.Id,
			Embedding = record.Embedding.ToArray(),
			Metadata = record.Metadata.ToMongoMetadata()
		};
	}

	public MemoryRecord ToMemoryRecord(MongoDBVectorStoreRecord record)
	{
		return MemoryRecord.FromMetadata(
			record.Metadata.ToMemoryMetadata(),
			record.Embedding);
	}
}
