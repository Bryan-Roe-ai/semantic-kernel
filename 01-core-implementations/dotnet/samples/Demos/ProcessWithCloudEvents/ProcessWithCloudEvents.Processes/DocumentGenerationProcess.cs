// Copyright (c) Microsoft. All rights reserved.

using Microsoft.SemanticKernel;
using ProcessWithCloudEvents.Processes.Steps;

namespace ProcessWithCloudEvents.Processes;

/// <summary>
/// Components related to the SK Process for generating documentation
/// </summary>
public static class DocumentGenerationProcess
{
    /// <summary>
    /// The key that the process will be registered with in the SK process runtime.
    /// </summary>
    public static string Key => nameof(DocumentGenerationProcess);

    /// <summary>
    /// SK Process events emitted by <see cref="DocumentGenerationProcess"/>
    /// </summary>
    public static class DocGenerationEvents
    {
        /// <summary>
        /// Event to start the document generation process
        /// </summary>
        public const string StartDocumentGeneration = nameof(StartDocumentGeneration);
        /// <summary>
        /// Event emitted when the user rejects the document
        /// </summary>
        public const string UserRejectedDocument = nameof(UserRejectedDocument);
        /// <summary>
        /// Event emitted when the user approves the document
        /// </summary>
        public const string UserApprovedDocument = nameof(UserApprovedDocument);
    }

    /// <summary>
    /// SK Process topics emitted by <see cref="DocumentGenerationProcess"/>
    /// Topics are used to emit events to external systems
    /// </summary>
    public static class DocGenerationTopics
    {
        /// <summary>
        /// Request user review document generation topic
        /// </summary>
        public const string RequestUserReview = nameof(RequestUserReview);
        /// <summary>
        /// Publish documentat generated topic
        /// </summary>
        public const string PublishDocumentation = nameof(PublishDocumentation);
    }

    /// <summary>
    /// Creates a process builder for the Document Generation SK Process
    /// </summary>
    /// <param name="processName">name of the SK Process</param>
    /// <returns>instance of <see cref="ProcessBuilder"/></returns>
    public static ProcessBuilder CreateProcessBuilder(string processName = "DocumentationGeneration")
    {
        // Create the process builder
        ProcessBuilder processBuilder = new(processName);

        // Add the steps
        var infoGatheringStep = processBuilder.AddStepFromType<GatherProductInfoStep>();
        var docsGenerationStep = processBuilder.AddStepFromType<GenerateDocumentationStep>();
        var docsProofreadStep = processBuilder.AddStepFromType<ProofReadDocumentationStep>();
        var docsPublishStep = processBuilder.AddStepFromType<PublishDocumentationStep>();

        var proxyStep = processBuilder.AddProxyStep(id: processName, [DocGenerationTopics.RequestUserReview, DocGenerationTopics.PublishDocumentation]);

        // Orchestrate the external input events
        processBuilder
            .OnInputEvent(DocGenerationEvents.StartDocumentGeneration)
            .SendEventTo(new(infoGatheringStep));

        processBuilder
            .OnInputEvent(DocGenerationEvents.UserRejectedDocument)
            .SendEventTo(new(docsGenerationStep, functionName: GenerateDocumentationStep.ProcessFunctions.ApplySuggestions));

        //processBuilder
        //    .OnInputEvent(DocGenerationEvents.UserApprovedDocument)
        //    .SendEventTo(new(docsPublishStep, parameterName: "userApproval"));

        // Hooking up the rest of the process steps
        infoGatheringStep
            .OnFunctionResult()
            .SendEventTo(new ProcessFunctionTargetBuilder(docsGenerationStep, functionName: GenerateDocumentationStep.ProcessFunctions.GenerateDocs));

        docsGenerationStep
            .OnEvent(GenerateDocumentationStep.OutputEvents.DocumentationGenerated)
            .SendEventTo(new ProcessFunctionTargetBuilder(docsProofreadStep));

        docsProofreadStep
            .OnEvent(ProofReadDocumentationStep.OutputEvents.DocumentationRejected)
            .SendEventTo(new ProcessFunctionTargetBuilder(docsGenerationStep, functionName: GenerateDocumentationStep.ProcessFunctions.ApplySuggestions));

        // When the proofreader approves the documentation, send it to the 'docs' parameter of the docsPublishStep
        // Additionally, the generated document is emitted externally for user approval using the pre-configured proxyStep
        docsProofreadStep
            .OnEvent(ProofReadDocumentationStep.OutputEvents.DocumentationApproved)
            .EmitExternalEvent(proxyStep, DocGenerationTopics.RequestUserReview);
        //.SendEventTo(new ProcessFunctionTargetBuilder(docsPublishStep, parameterName: "document"));

        processBuilder
            .ListenFor()
            .AllOf([
                new(messageType: ProofReadDocumentationStep.OutputEvents.DocumentationApproved, docsProofreadStep),
                new(messageType: DocGenerationEvents.UserApprovedDocument, processBuilder),
            ])
            .SendEventTo(new ProcessStepTargetBuilder(docsPublishStep, inputMapping: (inputEvents) =>
            {
                return new() {
                    { "document", inputEvents[docsProofreadStep.GetFullEventId(ProofReadDocumentationStep.OutputEvents.DocumentationApproved)] },
                    { "userApproval", inputEvents[processBuilder.GetFullEventId(DocGenerationEvents.UserApprovedDocument)] },
                };
            }));

        // When event is approved by user, it gets published externally too
        docsPublishStep
            .OnFunctionResult()
            .EmitExternalEvent(proxyStep, DocGenerationTopics.PublishDocumentation);

        return processBuilder;
    }
}
