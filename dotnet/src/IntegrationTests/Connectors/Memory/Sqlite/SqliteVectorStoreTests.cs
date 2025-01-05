// Copyright (c) Microsoft. All rights reserved.

using System.Linq;
using System.Threading.Tasks;
using Microsoft.SemanticKernel.Connectors.Sqlite;
using Xunit;

namespace SemanticKernel.IntegrationTests.Connectors.Memory.Sqlite;

/// <summary>
/// Integration tests for <see cref="SqliteVectorStore"/> class.
/// </summary>
[Collection("SqliteVectorStoreCollection")]
public sealed class SqliteVectorStoreTests(SqliteVectorStoreFixture fixture)
    : BaseVectorStoreTests<string, SqliteHotel<string>>(new SqliteVectorStore(fixture.Connection!))
{
    private const string? SkipReason = "SQLite vector search extension is required";

    [Fact(Skip = SkipReason)]
    public override async Task ItCanGetAListOfExistingCollectionNamesAsync()
    {
        await base.ItCanGetAListOfExistingCollectionNamesAsync();
    }
}
