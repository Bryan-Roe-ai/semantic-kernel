// Copyright (c) Microsoft. All rights reserved.

#pragma warning disable IDE0130
namespace Microsoft.SemanticKernel.Experimental.Orchestration;
#pragma warning restore IDE0130

/// <summary>
/// The flow step which references another flow.
/// </summary>
public sealed class ReferenceFlowStep : FlowStep
{
    /// <summary>
    /// Initializes a new instance of the <see cref="Flow"/> class.
    /// </summary>
    /// <param name="flowName">The name of referenced flow</param>
    public ReferenceFlowStep(string flowName) : base(string.Empty)
    {
        this.FlowName = flowName;
    }

    /// <summary>
    /// Only for deserialization.
    /// </summary>
    public ReferenceFlowStep() : this(string.Empty)
    {
    }

    /// <summary>
    /// Name of reference <see cref="Flow"/>.
    /// </summary>
    public string FlowName { get; set; }
}
