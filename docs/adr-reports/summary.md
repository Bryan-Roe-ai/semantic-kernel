# ADR Summary Report

This document provides a summary of the Architectural Decision Records (ADRs) in the repository.

## ADRs

### ADR-0001: Use Markdown Any Decision Records to track Semantic Kernel Architecture Decisions
- **Status**: accepted
- **Date**: 2023-05-29
- **Deciders**: dluc, shawncal, hathind, alliscode
- **Context and Problem Statement**: We have multiple different language versions of the Semantic Kernel under active development. We need a way to keep the implementations aligned with regard to key architectural decisions.
- **Decision Drivers**: Architecture changes and the associated decision-making process should be transparent to the community. Decision records are stored in the repository and are easily discoverable for teams involved in the various language ports.
- **Considered Options**: Use MADR format and store decision documents in the repository.
- **Decision Outcome**: Chosen option: Use MADR format and store decision documents in the repository.

### ADR-0002: Java Folder Structure
- **Status**: accepted
- **Date**: 2013-06-19
- **Deciders**: shawncal, johnoliver
- **Context and Problem Statement**: A port of the Semantic Kernel to Java is under development. The folder structure being used has diverged from the .Net implementation.
- **Decision Drivers**: The Java SK should follow the general design guidelines and conventions of Java. Different language versions should be consistent with the .Net implementation.
- **Considered Options**: Comparison of .Net and Java Folder structures.
- **Decision Outcome**: Follow guidelines for folder names and structure to match those used (or planned for .Net) but in the idiomatic Java folder naming convention.

### ADR-0003: Add support for multiple native function arguments of many types
- **Status**: accepted
- **Date**: 2023-06-16
- **Deciders**: shawncal, dluc
- **Context and Problem Statement**: Move native functions closer to a normal C# experience.
- **Decision Drivers**: Native skills can now have any number of parameters. The parameters are populated from context variables of the same name.
- **Considered Options**: Examples of before and after code for native functions.
- **Decision Outcome**: PR 1195

### ADR-0004: Error handling improvements
- **Status**: accepted
- **Date**: 2023-06-23
- **Deciders**: shawncal
- **Context and Problem Statement**: Enhance error handling in SK to simplify SK code and SK client code, ensuring consistency and maintainability.
- **Decision Drivers**: Exceptions should be propagated to the SK client code instead of being stored in the SKContext. The SK exception hierarchy should be designed following the principle of "less is more."
- **Considered Options**: Simplify existing SK exception hierarchy, use .NET standard exceptions, remove unnecessary exceptions, preserve original exception details.
- **Decision Outcome**: Implement the proposed changes to improve error handling in SK.

### ADR-0005: Kernel/Function Handlers - Phase 1
- **Status**: accepted
- **Date**: 2023-05-29
- **Deciders**: rogerbarreto, shawncal, stephentoub
- **Context and Problem Statement**: A Kernel function caller needs to handle/intercept any function execution in the Kernel before and after it was attempted.
- **Decision Drivers**: Architecture changes and the associated decision-making process should be transparent to the community. Decision records are stored in the repository and are easily discoverable for teams involved in the various language ports.
- **Considered Options**: Callback Registration + Recursive, Single Callback, Event Based Registration, Middleware, ISKFunction Event Support Interfaces.
- **Decision Outcome**: Chosen option: Event Base Registration (Kernel only).

### ADR-0006: Dynamic payload building for PUT and POST RestAPI operations and parameter namespacing
- **Status**: accepted
- **Date**: 2023-08-15
- **Deciders**: shawncal
- **Context and Problem Statement**: The SK OpenAPI does not allow the dynamic creation of payload/body for PUT and POST RestAPI operations.
- **Decision Drivers**: Create a mechanism that enables the dynamic construction of the payload/body for PUT and POST RestAPI operations. Develop a mechanism(namespacing) that allows differentiation of payload properties with identical names at various levels for PUT and POST RestAPI operations.
- **Considered Options**: Enable the dynamic creation of payload and/or namespacing by default. Enable the dynamic creation of payload and/or namespacing based on configuration.
- **Decision Outcome**: Chosen option: Enable the dynamic creation of payload and/or namespacing based on configuration.

### ADR-0007: Extract the Prompt Template Engine from Semantic Kernel core
- **Status**: accepted
- **Date**: 2023-08-25
- **Deciders**: shawncal
- **Context and Problem Statement**: The Semantic Kernel includes a default prompt template engine which is used to render Semantic Kernel prompts. To reduce the complexity and API surface of the Semantic Kernel, the prompt template engine is going to be extracted and added to its own package.
- **Decision Drivers**: Reduce API surface and complexity of the Semantic Kernel core. Simplify the `IPromptTemplateEngine` interface to make it easier to implement a custom template engine. Make the change without breaking existing clients.
- **Considered Options**: Create a new package called `Microsoft.SemanticKernel.TemplateEngine`. Maintain the existing namespace for all prompt template engine code. Simplify the `IPromptTemplateEngine` interface to just require implementation of `RenderAsync`. Dynamically load the existing `PromptTemplateEngine` if the `Microsoft.SemanticKernel.TemplateEngine` assembly is available.
- **Decision Outcome**: Implement the proposed changes to extract the prompt template engine from the Semantic Kernel core.

### ADR-0008: Refactor to support generic LLM request settings
- **Status**: accepted
- **Date**: 2023-09-15
- **Deciders**: shawncal
- **Context and Problem Statement**: The Semantic Kernel abstractions package includes a number of classes that are used to support passing LLM request settings when invoking an AI service. The problem with these classes is they include OpenAI specific properties only.
- **Decision Drivers**: Semantic Kernel abstractions must be AI Service agnostic. Solution must continue to support loading Semantic Function configuration from `config.json`. Provide a good experience for developers and implementors of AI services.
- **Considered Options**: Use `dynamic` to pass request settings. Use `object` to pass request settings. Define a base class for AI request settings which all implementations must extend.
- **Decision Outcome**: Chosen option: Define a base class for AI request settings which all implementations must extend.

### ADR-0009: Add support for multiple named arguments in template function calls
- **Status**: accepted
- **Date**: 2013-06-16
- **Deciders**: shawncal, hario90
- **Context and Problem Statement**: Native functions now support multiple parameters, populated from context values with the same name. Semantic functions currently only support calling native functions with no more than 1 argument.
- **Decision Drivers**: Parity with Guidance. Readability. Similarity to languages familiar to SK developers. YAML compatibility.
- **Considered Options**: Syntax idea 1: Using commas. Syntax idea 2: JavaScript/C#-Style delimiter (colon). Syntax idea 3: Python/Guidance-Style delimiter. Syntax idea 4: Allow whitespace between arg name/value delimiter.
- **Decision Outcome**: Chosen options: "Syntax idea 3: Python/Guidance-Style keyword arguments" and "Syntax idea 4: Allow whitespace between arg name/value delimiter".

### ADR-0010: DotNet Project Structure for 1.0 Release
- **Status**: superseded by [ADR-0042](0042-samples-restructure.md)
- **Date**: 2023-09-29
- **Deciders**: SergeyMenshykh, dmytrostruk, RogerBarreto
- **Context and Problem Statement**: Provide a cohesive, well-defined set of assemblies that developers can easily combine based on their needs. Remove `Skills` naming from NuGet packages and replace with `Plugins`.
- **Decision Drivers**: Avoid having too many assemblies because of impact of signing these and to reduce complexity. Follow .Net naming guidelines.
- **Considered Options**: Option #1: New `planning`, `functions` and `plugins` project areas. Option #2: Folder naming matches assembly name.
- **Decision Outcome**: Chosen option: Option #2: Folder naming matches assembly name.
