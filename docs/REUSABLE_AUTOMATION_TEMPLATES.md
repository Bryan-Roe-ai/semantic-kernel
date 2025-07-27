# Reusable Automation Templates

This repository provides a set of reusable GitHub Actions workflows that simplify common CI/CD tasks.
These templates live in `.github/workflows/templates` and can be referenced from other workflows using `workflow_call`.

## Available Templates

- **`build.yml`** – Builds .NET, Python, and Node projects. Enable languages by passing inputs `dotnet`, `python`, or `node`.
- **`test.yml`** – Runs unit tests for the selected languages.
- **`deploy.yml`** – Builds a Docker image and deploys it to Azure App Service.

## Usage Example

Create a workflow that calls the build and test templates:

```yaml
name: CI
on: [push]

jobs:
  build:
    uses: ./.github/workflows/templates/build.yml
    with:
      dotnet: true
      python: true
  test:
    needs: build
    uses: ./.github/workflows/templates/test.yml
    with:
      dotnet: true
      python: true
```

These templates can be composed to create sophisticated automation pipelines while keeping your workflow files concise.
