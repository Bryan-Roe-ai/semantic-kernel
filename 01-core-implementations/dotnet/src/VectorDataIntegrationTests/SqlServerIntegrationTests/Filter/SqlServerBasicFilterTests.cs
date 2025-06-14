// Copyright (c) Microsoft. All rights reserved.

using Microsoft.Extensions.VectorData;
using SqlServerIntegrationTests.Support;
using VectorDataSpecificationTests.Filter;
using VectorDataSpecificationTests.Support;
using Xunit;
using Xunit.Sdk;

namespace SqlServerIntegrationTests.Filter;

#pragma warning disable CS0252 // Possible unintended reference comparison; left hand side needs cast

public class SqlServerBasicFilterTests(SqlServerBasicFilterTests.Fixture fixture)
    : BasicFilterTests<int>(fixture), IClassFixture<SqlServerBasicFilterTests.Fixture>
{
    public override async Task Not_over_Or()
    {
        // Test sends: WHERE (NOT (("Int" = 8) OR ("String" = 'foo')))
        // There's a NULL string in the database, and relational null semantics in conjunction with negation makes the default implementation fail.
        await Assert.ThrowsAsync<FailException>(() => base.Not_over_Or());

        // Compensate by adding a null check:
        await this.TestFilterAsync(
            r => r.String != null && !(r.Int == 8 || r.String == "foo"),
            r => r["String"] != null && !((int)r["Int"]! == 8 || r["String"] == "foo"));
    }

    public override async Task NotEqual_with_string()
    {
        // As above, null semantics + negation
        await Assert.ThrowsAsync<FailException>(() => base.NotEqual_with_string());

        await this.TestFilterAsync(
            r => r.String != null && r.String != "foo",
            r => r["String"] != null && r["String"] != "foo");
    }

    public override Task Contains_over_field_string_array()
        => Assert.ThrowsAsync<InvalidOperationException>(() => base.Contains_over_field_string_array());

    public override Task Contains_over_field_string_List()
        => Assert.ThrowsAsync<InvalidOperationException>(() => base.Contains_over_field_string_List());

    [Fact(Skip = "Not supported")]
    [Obsolete("Legacy filters are not supported")]
    public override Task Legacy_And() => throw new NotSupportedException();

    [Fact(Skip = "Not supported")]
    [Obsolete("Legacy filters are not supported")]
    public override Task Legacy_AnyTagEqualTo_array() => throw new NotSupportedException();

    [Fact(Skip = "Not supported")]
    [Obsolete("Legacy filters are not supported")]
    public override Task Legacy_AnyTagEqualTo_List() => throw new NotSupportedException();

    [Fact(Skip = "Not supported")]
    [Obsolete("Legacy filters are not supported")]
    public override Task Legacy_equality() => throw new NotSupportedException();

    public new class Fixture : BasicFilterTests<int>.Fixture
    {
        private static readonly string s_uniqueName = Guid.NewGuid().ToString();

        public override TestStore TestStore => SqlServerTestStore.Instance;

        public override string CollectionName => s_uniqueName;

        // Override to remove the string collection properties, which aren't (currently) supported on SqlServer
        public override VectorStoreCollectionDefinition CreateRecordDefinition()
            => new()
            {
                Properties = base.CreateRecordDefinition().Properties.Where(p => p.Type != typeof(string[]) && p.Type != typeof(List<string>)).ToList()
            };
    }
}
