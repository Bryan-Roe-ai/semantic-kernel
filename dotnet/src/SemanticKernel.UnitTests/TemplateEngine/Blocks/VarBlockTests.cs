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
=======
// Copyright (c) Microsoft. All rights reserved.
>>>>>>> Stashed changes
=======
// Copyright (c) Microsoft. All rights reserved.
>>>>>>> Stashed changes
=======
// Copyright (c) Microsoft. All rights reserved.
>>>>>>> Stashed changes
=======
// Copyright (c) Microsoft. All rights reserved.
>>>>>>> Stashed changes
=======
// Copyright (c) Microsoft. All rights reserved.
>>>>>>> Stashed changes
=======
// Copyright (c) Microsoft. All rights reserved.
<<<<<<< Updated upstream
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
// Copyright (c) Microsoft. All rights reserved.
>>>>>>> Stashed changes
=======
// Copyright (c) Microsoft. All rights reserved.
>>>>>>> Stashed changes
>>>>>>> head
=======
>>>>>>> Stashed changes
>>>>>>> Stashed changes

using System;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.TemplateEngine;
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
=======
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
<<<<<<< main
=======
>>>>>>> Stashed changes
=======
<<<<<<< main
=======
>>>>>>> Stashed changes
>>>>>>> head
using Microsoft.SemanticKernel.Diagnostics;
using Microsoft.SemanticKernel.Orchestration;
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

public class VarBlockTests
{
    [Fact]
    public void ItHasTheCorrectType()
    {
        // Act
        var target = new VarBlock("");

        // Assert
        Assert.Equal(BlockTypes.Variable, target.Type);
    }

    [Fact]
    public void ItTrimsSpaces()
    {
        // Act + Assert
        Assert.Equal("$", new VarBlock("  $  ").Content);
    }

    [Fact]
    public void ItIgnoresSpacesAround()
    {
        // Act
        var target = new VarBlock("  $var \n ");

        // Assert
        Assert.Equal("$var", target.Content);
    }

    [Fact]
    public void ItRendersToNullWithNoArgument()
    {
        // Arrange
        var target = new VarBlock("$var");

        // Act
        var result = target.Render([]);

        // Assert
        Assert.Null(result);
    }

    [Fact]
    public void ItRendersToNullWithNullArgument()
    {
        // Arrange
        var target = new VarBlock("$var");
        var arguments = new KernelArguments()
        {
            ["$var"] = null
        };

        // Act
        var result = target.Render(arguments);

        // Assert
        Assert.Null(result);
    }

    [Fact]
    public void ItRendersToArgumentValueWhenAvailable()
    {
        // Arrange
        var target = new VarBlock("  $var \n ");
        var arguments = new KernelArguments()
        {
            ["foo"] = "bar",
            ["var"] = "able",
        };

        // Act
        var result = target.Render(arguments);

        // Assert
        Assert.Equal("able", result);
    }

    [Fact]
    public void ItRendersWithOriginalArgumentValueAndType()
    {
        // Arrange
        var target = new VarBlock(" $var ");
        var arguments = new KernelArguments()
        {
            ["var"] = DayOfWeek.Tuesday,
        };

        // Act
        var result = target.Render(arguments);

        // Assert
        Assert.IsType<DayOfWeek>(result);
        Assert.Equal(DayOfWeek.Tuesday, result);
    }

    [Fact]
    public void ItThrowsIfTheVarNameIsEmpty()
    {
        // Arrange
        var arguments = new KernelArguments()
        {
            ["foo"] = "bar",
            ["var"] = "able",
        };
        var target = new VarBlock(" $ ");

        // Act + Assert
        Assert.Throws<KernelException>(() => target.Render(arguments));
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
        Assert.Throws<SKException>(() => target.Render(variables));
        Assert.Throws<SKException>(() => target.Render(variables));
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
        Assert.Throws<SKException>(() => target.Render(variables));
        Assert.Throws<SKException>(() => target.Render(variables));
>>>>>>> Stashed changes
=======
        Assert.Throws<SKException>(() => target.Render(variables));
        Assert.Throws<SKException>(() => target.Render(variables));
>>>>>>> Stashed changes
=======
        Assert.Throws<SKException>(() => target.Render(variables));
        Assert.Throws<SKException>(() => target.Render(variables));
>>>>>>> Stashed changes
=======
        Assert.Throws<SKException>(() => target.Render(variables));
        Assert.Throws<SKException>(() => target.Render(variables));
>>>>>>> Stashed changes
=======
        Assert.Throws<SKException>(() => target.Render(variables));
        Assert.Throws<SKException>(() => target.Render(variables));
<<<<<<< div
>>>>>>> main
=======
>>>>>>> origin/main
=======
        Assert.Throws<SKException>(() => target.Render(variables));
        Assert.Throws<SKException>(() => target.Render(variables));
>>>>>>> Stashed changes
=======
        Assert.Throws<SKException>(() => target.Render(variables));
        Assert.Throws<SKException>(() => target.Render(variables));
>>>>>>> Stashed changes
>>>>>>> head
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
    [InlineData(".", false)]
    [InlineData("-", false)]
    [InlineData("a b", false)]
    [InlineData("a\nb", false)]
    [InlineData("a\tb", false)]
    [InlineData("a\rb", false)]
    [InlineData("a.b", false)]
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
    public void ItAllowsUnderscoreLettersAndDigits(string name, bool isValid)
    {
        // Arrange
        var target = new VarBlock($" ${name} ");
        var arguments = new KernelArguments { [name] = "value" };

        // Act
        var result = target.Render(arguments);

        // Assert
        Assert.Equal(isValid, target.IsValid(out _));
        if (isValid) { Assert.Equal("value", result); }
    }
}
