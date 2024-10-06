﻿// Copyright (c) Microsoft. All rights reserved.

using System;
using System.Linq;
<<<<<<< head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
<<<<<<< HEAD
>>>>>>> origin/main
using Microsoft.SemanticKernel.Experimental.Orchestration.Abstractions;

namespace Microsoft.SemanticKernel.Experimental.Orchestration;
=======
<<<<<<< head
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< HEAD
using Microsoft.SemanticKernel.Experimental.Orchestration.Abstractions;

namespace Microsoft.SemanticKernel.Experimental.Orchestration;
=======
=======
>>>>>>> origin/main
using Microsoft.SemanticKernel.Diagnostics;
using Microsoft.SemanticKernel.Experimental.Orchestration.Abstractions;

#pragma warning disable IDE0130
namespace Microsoft.SemanticKernel.Experimental.Orchestration;
#pragma warning restore IDE0130
>>>>>>> 9cfcc609b1cbe6e1d6975df1d665fa0b064c5624
<<<<<<< head
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
>>>>>>> origin/main

/// <summary>
/// The flow validator
/// </summary>
public class FlowValidator : IFlowValidator
{
    /// <inheritdoc/>
    public void Validate(Flow flow)
    {
        Verify.NotNullOrWhiteSpace(flow.Goal, nameof(flow.Goal));

        this.ValidateNonEmpty(flow);
        this.ValidatePartialOrder(flow);
        this.ValidateReferenceStep(flow);
        this.ValidateStartingMessage(flow);
        this.ValidatePassthroughVariables(flow);
    }

    private void ValidateStartingMessage(Flow flow)
    {
        foreach (var step in flow.Steps)
        {
            if (step.CompletionType is CompletionType.Optional or CompletionType.ZeroOrMore
                && string.IsNullOrEmpty(step.StartingMessage))
            {
                throw new ArgumentException(
                    $"Missing starting message for step={step.Goal} with completion type={step.CompletionType}");
            }
        }
    }

    private void ValidateNonEmpty(Flow flow)
    {
        if (flow.Steps.Count == 0)
        {
            throw new ArgumentException("Flow must contain at least one flow step.");
        }
    }

    private void ValidatePartialOrder(Flow flow)
    {
        try
        {
            var sorted = flow.SortSteps();
        }
        catch (Exception ex)
        {
            throw new ArgumentException("Flow steps must be a partial order set.", ex);
        }
    }

    private void ValidateReferenceStep(Flow flow)
    {
        var steps = flow.Steps
            .Select(step => step as ReferenceFlowStep)
<<<<<<< head
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
            .Where(step => step is not null);
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
<<<<<<< main
            .Where(step => step is not null);
=======
=======
>>>>>>> origin/main
<<<<<<< HEAD
            .Where(step => step is not null);
=======
            .Where(step => step != null);
>>>>>>> 9cfcc609b1cbe6e1d6975df1d665fa0b064c5624
<<<<<<< head
>>>>>>> origin/main
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
>>>>>>> origin/main

        foreach (var step in steps)
        {
            Verify.NotNullOrWhiteSpace(step!.FlowName);

            if (step.Requires.Any())
            {
                throw new ArgumentException("Reference flow step cannot have any direct requirements.");
            }

            if (step.Provides.Any())
            {
                throw new ArgumentException("Reference flow step cannot have any direct provides.");
            }

            if (step.Plugins?.Count != 0)
            {
                throw new ArgumentException("Reference flow step cannot have any direct plugins.");
            }
        }
    }

    private void ValidatePassthroughVariables(Flow flow)
    {
        foreach (var step in flow.Steps)
        {
            if (step.CompletionType != CompletionType.AtLeastOnce
                && step.CompletionType != CompletionType.ZeroOrMore
                && step.Passthrough.Any())
            {
                throw new ArgumentException(
                    $"step={step.Goal} with completion type={step.CompletionType} cannot have passthrough variables as that is only applicable for the AtLeastOnce or ZeroOrMore completion types");
            }
        }
    }
}
