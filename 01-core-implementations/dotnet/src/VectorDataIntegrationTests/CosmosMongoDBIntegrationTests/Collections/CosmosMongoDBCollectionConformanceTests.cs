// Copyright (c) Microsoft. All rights reserved.

using CosmosMongoDBIntegrationTests.Support;
using VectorDataSpecificationTests.Collections;
using Xunit;

namespace CosmosMongoDBIntegrationTests.Collections;

public class CosmosMongoDBCollectionConformanceTests(CosmosMongoFixture fixture)
    : CollectionConformanceTests<string>(fixture), IClassFixture<CosmosMongoFixture>
{
}
