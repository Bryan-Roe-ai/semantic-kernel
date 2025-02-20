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
﻿// Copyright (c) Microsoft. All rights reserved.

using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.TemplateEngine;
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
// Copyright (c) Microsoft. All rights reserved.

using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.TemplateEngine;
<<<<<<< main
=======
<<<<<<< div
=======
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> head
=======
// Copyright (c) Microsoft. All rights reserved.

using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.TemplateEngine;
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
>>>>>>> head
using Microsoft.Extensions.Logging.Abstractions;
using Microsoft.SemanticKernel.Diagnostics;
using Microsoft.SemanticKernel.TemplateEngine.Blocks;
>>>>>>> origin/main
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
=======
>>>>>>> Stashed changes
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
using Xunit;

namespace SemanticKernel.UnitTests.TemplateEngine;

public class FunctionIdBlockTests
{
    [Fact]
    public void ItHasTheCorrectType()
    {
        // Act
        var target = new FunctionIdBlock("");

        // Assert
        Assert.Equal(BlockTypes.FunctionId, target.Type);
    }

    [Fact]
    public void ItTrimsSpaces()
    {
        // Act + Assert
        Assert.Equal("aa", new FunctionIdBlock("  aa  ").Content);
    }

    [Theory]
    [InlineData("0", true)]
    [InlineData("1", true)]
    [InlineData("a", true)]
    [InlineData("_", true)]
    [InlineData("01", true)]
    [InlineData("01a", true)]
    [InlineData("a01", true)]
    [InlineData("_0", true)]
    [InlineData("a01_", true)]
    [InlineData("_a01", true)]
    [InlineData(".", true)]
    [InlineData("a.b", true)]
    [InlineData("-", false)]
    [InlineData("a b", false)]
    [InlineData("a\nb", false)]
    [InlineData("a\tb", false)]
    [InlineData("a\rb", false)]
    [InlineData("a,b", false)]
    [InlineData("a-b", false)]
    [InlineData("a+b", false)]
    [InlineData("a~b", false)]
    [InlineData("a`b", false)]
    [InlineData("a!b", false)]
    [InlineData("a@b", false)]
    [InlineData("a#b", false)]
    [InlineData("a$b", false)]
    [InlineData("a%b", false)]
    [InlineData("a^b", false)]
    [InlineData("a*b", false)]
    [InlineData("a(b", false)]
    [InlineData("a)b", false)]
    [InlineData("a|b", false)]
    [InlineData("a{b", false)]
    [InlineData("a}b", false)]
    [InlineData("a[b", false)]
    [InlineData("a]b", false)]
    [InlineData("a:b", false)]
    [InlineData("a;b", false)]
    [InlineData("a'b", false)]
    [InlineData("a\"b", false)]
    [InlineData("a<b", false)]
    [InlineData("a>b", false)]
    [InlineData("a/b", false)]
    [InlineData("a\\b", false)]
    public void ItAllowsUnderscoreDotsLettersAndDigits(string name, bool isValid)
    {
        // Arrange
        var target = new FunctionIdBlock($" {name} ");

        // Act + Assert
        Assert.Equal(isValid, target.IsValid(out _));
    }

    [Fact]
    public void ItAllowsOnlyOneDot()
    {
        // Arrange
        var target1 = new FunctionIdBlock("functionName");
        var target2 = new FunctionIdBlock("pluginName.functionName");
        Assert.Throws<KernelException>(() => new FunctionIdBlock("foo.pluginName.functionName"));
<<<<<<< div
<<<<<<< div
=======
>>>>>>> head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
        var target2 = new FunctionIdBlock("skillName.functionName");
        Assert.Throws<SKException>(() => new FunctionIdBlock("foo.skillName.functionName"));
>>>>>>> Stashed changes
=======
        var target2 = new FunctionIdBlock("skillName.functionName");
        Assert.Throws<SKException>(() => new FunctionIdBlock("foo.skillName.functionName"));
>>>>>>> Stashed changes
=======
        var target2 = new FunctionIdBlock("skillName.functionName");
        Assert.Throws<SKException>(() => new FunctionIdBlock("foo.skillName.functionName"));
>>>>>>> Stashed changes
=======
        var target2 = new FunctionIdBlock("skillName.functionName");
        Assert.Throws<SKException>(() => new FunctionIdBlock("foo.skillName.functionName"));
>>>>>>> Stashed changes
=======
        var target2 = new FunctionIdBlock("skillName.functionName");
        Assert.Throws<SKException>(() => new FunctionIdBlock("foo.skillName.functionName"));
>>>>>>> Stashed changes
=======
        var target2 = new FunctionIdBlock("skillName.functionName");
        Assert.Throws<SKException>(() => new FunctionIdBlock("foo.skillName.functionName"));
>>>>>>> Stashed changes
=======
        var target2 = new FunctionIdBlock("skillName.functionName");
        Assert.Throws<SKException>(() => new FunctionIdBlock("foo.skillName.functionName"));
>>>>>>> origin/main
=======
        var target2 = new FunctionIdBlock("skillName.functionName");
        Assert.Throws<SKException>(() => new FunctionIdBlock("foo.skillName.functionName"));
>>>>>>> Stashed changes
=======
        var target2 = new FunctionIdBlock("skillName.functionName");
        Assert.Throws<SKException>(() => new FunctionIdBlock("foo.skillName.functionName"));
>>>>>>> Stashed changes
<<<<<<< div
=======
        var target2 = new FunctionIdBlock("skillName.functionName");
        Assert.Throws<SKException>(() => new FunctionIdBlock("foo.skillName.functionName"));
>>>>>>> main
=======
>>>>>>> head

        // Act + Assert
        Assert.True(target1.IsValid(out _));
        Assert.True(target2.IsValid(out _));
    }
}
