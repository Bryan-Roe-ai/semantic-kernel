---
applyTo: "**"
priority: high
autoMode: enabled
---

# AI AutoMode Instructions for Semantic Kernel Development

## Core Principles

- Follow semantic kernel design patterns and best practices
- Prioritize type safety, performance, and maintainability
- Use dependency injection and async/await patterns consistently
- Implement proper error handling and logging

## Code Standards

- Use C# nullable reference types
- Follow Microsoft naming conventions
- Write comprehensive XML documentation
- Include unit tests for all public methods
- Use ConfigureAwait(false) for library code

## Semantic Kernel Specific Guidelines

- Use proper plugin architecture patterns
- Implement IKernelFunction interface correctly
- Follow prompt engineering best practices
- Use KernelArguments for parameter passing
- Implement proper token counting and management

## AutoMode Behaviors

- Generate complete, compilable code snippets
- Include necessary using statements
- Provide error handling for AI operations
- Add appropriate logging statements
- Include performance considerations in comments

## Domain Knowledge

- Understanding of LLM integration patterns
- Knowledge of prompt injection prevention
- Familiarity with AI safety and responsible AI practices
- Experience with vector databases and embeddings
- Understanding of retrieval-augmented generation (RAG)

## File Patterns

- \*.cs: Apply C# coding standards and semantic kernel patterns
- \*.json: Validate schema and use proper formatting
- \*.md: Follow markdown best practices with clear structure
- Tests/\*: Generate comprehensive test coverage

## Quality Gates

- All code must compile without warnings
- Include appropriate exception handling
- Validate inputs and sanitize outputs
- Use semantic kernel logging framework
- Follow async patterns throughout
