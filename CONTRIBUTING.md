---

# Contributing to Semantic Kernel

> ℹ️ **NOTE**: The Python SDK for Semantic Kernel is currently in preview. While most of the features available in the C# SDK have been ported, there may be bugs and we're working on some features still - these will come into the repo soon. We are also actively working on improving the code quality and developer experience, and we appreciate your support, input, and PRs!

## Table of Contents
1. [Reporting Issues](#reporting-issues)
2. [Contributing Changes](#contributing-changes)
3. [Breaking Changes](#breaking-changes)
4. [Suggested Workflow](#suggested-workflow)
5. [Development Scripts](#development-scripts)
6. [Adding Plugins and Memory Connectors](#adding-plugins-and-memory-connectors)
7. [Examples and Use Cases](#examples-and-use-cases)
8. [How to Contribute to the Repository](#how-to-contribute-to-the-repository)
9. [Setting Up CI/CD Pipelines](#setting-up-ci-cd-pipelines)
10. [Reporting Issues and Requesting Features](#reporting-issues-and-requesting-features)

## Reporting Issues

We always welcome bug reports, API proposals, and overall feedback. Here are a few tips on how you can make reporting your issue as effective as possible.

### Where to Report

New issues can be reported in our [list of issues](https://github.com/microsoft/semantic-kernel/issues).

Before filing a new issue, please search the list of issues to make sure it does not already exist.

If you do find an existing issue for what you wanted to report, please include your own feedback in the discussion. Do consider upvoting (👍 reaction) the original post, as this helps us prioritize popular issues in our backlog.

### Writing a Good Bug Report

Good bug reports make it easier for maintainers to verify and root cause the underlying problem. The better a bug report, the faster the problem will be resolved. Ideally, a bug report should contain the following information:

- A high-level description of the problem.
- A _minimal reproduction_, i.e., the smallest size of code/configuration required to reproduce the wrong behavior.
- A description of the _expected behavior_, contrasted with the _actual behavior_ observed.
- Information on the environment: OS/distribution, CPU architecture, SDK version, etc.
- Additional information, e.g., Is it a regression from previous versions? Are there any known workarounds?
# Contributing to Semantic Kernel

> ℹ️ **NOTE**: The Python SDK for Semantic Kernel is currently in preview. While most
> of the features available in the C# SDK have been ported, there may be bugs and
> we're working on some features still - these will come into the repo soon. We are
> also actively working on improving the code quality and developer experience,
> and we appreciate your support, input and PRs!

You can contribute to Semantic Kernel with issues and pull requests (PRs). Simply
filing issues for problems you encounter is a great way to contribute. Contributing
code is greatly appreciated.

## Reporting Issues

We always welcome bug reports, API proposals and overall feedback. Here are a few
tips on how you can make reporting your issue as effective as possible.

### Where to Report

New issues can be reported in our [list of issues](https://github.com/semantic-kernel/issues).

Before filing a new issue, please search the list of issues to make sure it does
not already exist.

If you do find an existing issue for what you wanted to report, please include
your own feedback in the discussion. Do consider upvoting (👍 reaction) the original
post, as this helps us prioritize popular issues in our backlog.

### Writing a Good Bug Report

Good bug reports make it easier for maintainers to verify and root cause the
underlying problem.
The better a bug report, the faster the problem will be resolved. Ideally, a bug
report should contain the following information:

-   A high-level description of the problem.
-   A _minimal reproduction_, i.e. the smallest size of code/configuration required
    to reproduce the wrong behavior.
-   A description of the _expected behavior_, contrasted with the _actual behavior_ observed.
-   Information on the environment: OS/distribution, CPU architecture, SDK version, etc.
-   Additional information, e.g. Is it a regression from previous versions? Are there
    any known workarounds?

## Contributing Changes

Project maintainers will merge accepted code changes from contributors.

### DOs and DON'Ts

**DO's:**

- **DO** follow the standard coding conventions
  - [.NET](https://learn.microsoft.com/dotnet/csharp/fundamentals/coding-style/coding-conventions)
  - [Python](https://pypi.org/project/black/)
  - [Typescript](https://typescript-eslint.io/rules/)/[React](https://github.com/jsx-eslint/eslint-plugin-react/tree/master/docs/rules)
- **DO** give priority to the current style of the project or file you're changing if it diverges from the general guidelines.
- **DO** include tests when adding new features. When fixing bugs, start with adding a test that highlights how the current behavior is broken.
- **DO** keep the discussions focused. When a new or related topic comes up, it's often better to create a new issue than to sidetrack the discussion.
- **DO** clearly state on an issue that you are going to take on implementing it.
- **DO** blog and tweet (or whatever) about your contributions, frequently!

**DON'Ts:**

- **DON'T** surprise us with big pull requests. Instead, file an issue and start a discussion so we can agree on a direction before you invest a large amount of time.
- **DON'T** commit code that you didn't write. If you find code that you think is a good fit to add to Semantic Kernel, file an issue and start a discussion before proceeding.
- **DON'T** submit PRs that alter licensing-related files or headers. If you believe there's a problem with them, file an issue and we'll be happy to discuss it.
- **DON'T** make new APIs without filing an issue and discussing with us first.

## Breaking Changes

Contributions must maintain API signature and behavioral compatibility. Contributions that include breaking changes will be rejected. Please file an issue to discuss your idea or change if you believe that a breaking change is warranted.
DO's:

-   **DO** follow the standard Python code style
-   **DO** give priority to the current style of the project or file you're changing
    if it diverges from the general guidelines.
-   **DO** include tests when adding new features. When fixing bugs, start with
    adding a test that highlights how the current behavior is broken.
-   **DO** keep the discussions focused. When a new or related topic comes up
    it's often better to create new issue than to side track the discussion.
-   **DO** clearly state on an issue that you are going to take on implementing it.
-   **DO** blog and tweet (or whatever) about your contributions, frequently!

DON'Ts:

-   **DON'T** surprise us with big pull requests. Instead, file an issue and start
    a discussion so we can agree on a direction before you invest a large amount of time.
-   **DON'T** commit code that you didn't write. If you find code that you think is a good
    fit to add to Semantic Kernel, file an issue and start a discussion before proceeding.
-   **DON'T** submit PRs that alter licensing related files or headers. If you believe
    there's a problem with them, file an issue and we'll be happy to discuss it.
-   **DON'T** make new APIs without filing an issue and discussing with us first.

### Breaking Changes

Contributions must maintain API signature and behavioral compatibility. Contributions
that include breaking changes will be rejected. Please file an issue to discuss
your idea or change if you believe that a breaking change is warranted.

### Suggested Workflow

We use and recommend the following workflow:

1. Create an issue for your work.
   - You can skip this step for trivial changes.
   - Reuse an existing issue on the topic, if there is one.
   - Get agreement from the team and the community that your proposed change is a good one.
   - Clearly state that you are going to take on implementing it, if that's the case. You can request that the issue be assigned to you. Note: The issue filer and the implementer don't have to be the same person.
2. Create a personal fork of the repository on GitHub (if you don't already have one).
3. In your fork, create a branch off of main (`git checkout -b mybranch`).
   - Name the branch so that it clearly communicates your intentions, such as "issue-123" or "githubhandle-issue".
4. Make and commit your changes to your branch.
5. Add new tests corresponding to your change, if applicable.
6. Run the relevant scripts in [the section below](https://github.com/microsoft/semantic-kernel/blob/main/CONTRIBUTING.md#dev-scripts) to ensure that your build is clean and all tests are passing.
7. Create a PR against the repository's **main** branch.
   - State in the description what issue or improvement your change is addressing.
   - Verify that all the Continuous Integration checks are passing.
8. Wait for feedback or approval of your changes from the code maintainers.
9. When area owners have signed off, and all checks are green, your PR will be merged.

### Development Scripts

The scripts below are used to build, test, and lint within the project.

- Python: see [python/DEV_SETUP.md](https://github.com/microsoft/semantic-kernel/blob/main/python/DEV_SETUP.md#pipeline-checks).
- .NET:
  - Build/Test: `run build.cmd` or `bash build.sh`
  - Linting (auto-fix): `dotnet format`
- Typescript:
  - Build/Test: `yarn build`
  - Linting (auto-fix): `yarn lint:fix`

### Adding Plugins and Memory Connectors

When considering contributions to plugins and memory connectors for Semantic Kernel, please note the following guidelines:

#### Plugins

We appreciate your interest in extending Semantic Kernel's functionality through plugins. However, we want to clarify our approach to hosting plugins within our GitHub repository. To maintain a clean and manageable codebase, we will not be hosting plugins directly in the Semantic Kernel GitHub repository. Instead, we encourage contributors to host their plugin code in separate repositories under their own GitHub accounts or organization. You can then provide a link to your plugin repository in the relevant discussions, issues, or documentation within the Semantic Kernel repository. This approach ensures that each plugin can be maintained independently and allows for easier tracking of updates and issues specific to each plugin.

#### Memory Connectors

For memory connectors, while we won't be directly adding hosting for them within the Semantic Kernel repository, we highly recommend building memory connectors as separate plugins. Memory connectors play a crucial role in interfacing with external memory systems, and treating them as plugins enhances modularity and maintainability.

### Examples and Use Cases

To help contributors understand how to use the repository effectively, we have included some examples and use cases below:

#### Example 1: Adding a New Feature

1. Identify the feature you want to add and create an issue to discuss it with the community.
2. Fork the repository and create a new branch for your feature.
3. Implement the feature in your branch, following the coding standards and guidelines.
4. Add tests to verify the new feature works as expected.
5. Run the development scripts to ensure your changes do not break the build or existing tests.
6. Create a pull request with a description of the feature and link to the issue.
7. Address any feedback from maintainers and community members.
8. Once approved, your feature will be merged into the main branch.

#### Example 2: Fixing a Bug

1. Identify the bug and create an issue to discuss it with the community.
2. Fork the repository and create a new branch for your bug fix.
3. Write a test that reproduces the bug.
4. Implement the fix in your branch.
5. Run the development scripts to ensure your changes do not break the build or existing tests.
6. Create a pull request with a description of the bug and the fix, and link to the issue.
7. Address any feedback from maintainers and community members.
8. Once approved, your bug fix will be merged into the main branch.

#### Example 3: Improving Documentation

1. Identify the documentation that needs improvement and create an issue to discuss it with the community.
2. Fork the repository and create a new branch for your documentation improvements.
3. Make the necessary changes to the documentation in your branch.
4. Run the development scripts to ensure your changes do not break the build or existing tests.
5. Create a pull request with a description of the documentation improvements and link to the issue.
6. Address any feedback from maintainers and community members.
7. Once approved, your documentation improvements will be merged into the main branch.

By following these examples and use cases, you can effectively contribute to the Semantic Kernel repository and help improve the project for everyone.

## How to Contribute to the Repository

We welcome contributions from the community! To contribute to this project, please follow these guidelines:

1. **Fork the repository**: Create a fork of the repository to work on your changes.

2. **Create a branch**: Create a new branch for your changes.

    ```bash
    git checkout -b my-feature-branch
    ```

3. **Make your changes**: Implement your changes in the new branch.

4. **Test your changes**: Ensure that your changes do not break any existing functionality and pass all tests.

5. **Commit your changes**: Commit your changes with a descriptive commit message.

    ```bash
    git commit -m "Add new feature"
    ```

6. **Push your changes**: Push your changes to your forked repository.

    ```bash
    git push origin my-feature-branch
    ```

7. **Create a pull request**: Open a pull request to merge your changes into the main repository.

8. **Review and feedback**: Address any feedback or comments from the maintainers during the review process.

9. **Merge**: Once your pull request is approved, it will be merged into the main repository.

Thank you for your contributions!

## Setting Up CI/CD Pipelines Using CircleCI, GitHub Actions, and Azure Pipelines

### CircleCI

The repository contains a CircleCI configuration file at `.circleci/config.yml`. This file defines a simple job that runs tests using a Docker image with Node.js and browsers. You can customize the configuration as needed.

### GitHub Actions

The repository has several GitHub Actions workflows in the `.github/workflows` directory. For example, the `.github/workflows/dotnet-build-and-test.yml` workflow builds and tests .NET projects. You can customize these workflows to fit your project's needs.

#### Configuring Secrets for GitHub Actions

To configure secrets for GitHub Actions workflows, follow these steps:

1. Navigate to the repository on GitHub.
2. Click on the "Settings" tab.
3. In the left sidebar, click on "Secrets and variables" and then "Actions".
4. Click the "New repository secret" button.
5. Add a name for the secret (e.g., `AZURE_WEBAPP_PUBLISH_PROFILE`).
6. Add the value for the secret.
7. Click "Add secret" to save it.

You can then reference these secrets in your GitHub Actions workflows using the `${{ secrets.SECRET_NAME }}` syntax. For example, in the `.github/workflows/azure-container-webapp.yml` workflow, the secret `AZURE_WEBAPP_PUBLISH_PROFILE` is used.

#### Customizing Workflows for Specific Project Needs

You can customize the existing workflows to fit your project's needs. Here are some ways to do it:

- Modify the existing workflows in the `.github/workflows` directory to suit your specific requirements. For example, you can adjust the triggers, add or remove steps, and change the configuration.
- Add new workflows to automate additional tasks, such as deploying to different environments, running additional tests, or integrating with other services.
- Use secrets to securely store sensitive information, such as API keys and credentials, and reference them in your workflows using the `${{ secrets.SECRET_NAME }}` syntax.
- Leverage the existing workflows as templates and create variations for different branches, environments, or project components.
- Utilize GitHub Actions marketplace to find and integrate additional actions that can help you achieve your CI/CD goals.

#### Troubleshooting Issues in GitHub Actions Workflows

To troubleshoot issues in GitHub Actions workflows, follow these steps:

- Check the workflow logs for errors and warnings. You can find the logs in the "Actions" tab of your repository.
- Verify that the secrets used in the workflows are correctly configured. For example, ensure that `AZURE_WEBAPP_PUBLISH_PROFILE` and `GITHUB_TOKEN` are set up correctly in the repository settings.
- Ensure that the syntax and structure of the workflow files in the `.github/workflows` directory are correct. For example, check the syntax of `.github/workflows/dotnet-build-and-test.yml` and `.github/workflows/azure-container-webapp.yml`.
- Confirm that the required permissions are set correctly in the workflow files. For example, the `permissions` section in `.github/workflows/Auto-merge.yml` and `.github/workflows/docker-image.yml` should be correctly configured.
- Verify that the necessary dependencies and actions are correctly specified in the workflow files. For example, ensure that the `actions/checkout@v4` and `docker/setup-buildx-action@v3.0.0` actions are correctly configured.
- Check for any conditional statements in the workflows that might be causing issues. For example, the `if` conditions in `.github/workflows/Auto-merge.yml` and `.github/workflows/dotnet-build-and-test.yml`.
- Ensure that the environment variables and secrets are correctly referenced in the workflows. For example, the `${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}` and `${{ secrets.GITHUB_TOKEN }}` references.
- Review the documentation and examples for the actions used in the workflows. For example, refer to the documentation for `azure/webapps-deploy@v2` and `docker/build-push-action@v5.0.0` to ensure correct usage.

#### Best Practices for Managing Secrets in GitHub Actions

Here are some best practices for managing secrets in GitHub Actions:

- **Use GitHub Secrets:** Store sensitive information such as API keys, credentials, and tokens in GitHub Secrets. Navigate to the repository's "Settings" tab, click on "Secrets and variables," and add your secrets there.
- **Limit Secret Access:** Only provide access to secrets to workflows and jobs that require them. For example, in the `.github/workflows/azure-container-webapp.yml` workflow, the `AZURE_WEBAPP_PUBLISH_PROFILE` secret is used with limited permissions.
- **Use Environment Variables:** Use environment variables to manage secrets and configuration settings. For example, in the `.github/workflows/dotnet-build-and-test.yml` workflow, environment variables are used to store sensitive information.
- **Rotate Secrets Regularly:** Regularly update and rotate secrets to minimize the risk of unauthorized access. Ensure that old secrets are removed from the repository settings.
- **Audit Secret Usage:** Regularly review and audit the usage of secrets in your workflows. Check the workflow logs and ensure that secrets are only used where necessary.
- **Use Least Privilege Principle:** Grant the minimum necessary permissions to secrets. For example, in the `.github/workflows/Auto-merge.yml` workflow, the `GITHUB_TOKEN` secret is used with limited permissions.
- **Avoid Hardcoding Secrets:** Never hardcode secrets directly in your workflow files. Always use GitHub Secrets to securely store and reference them.
- **Monitor for Leaks:** Use tools and services to monitor for potential secret leaks in your repository. GitHub provides secret scanning to detect and alert you about exposed secrets.

### Azure Pipelines

The repository includes an Azure Pipelines configuration file at `.github/workflows/azure-container-webapp.yml`. This workflow builds and pushes a Docker container to an Azure Web App. You can customize the configuration as needed.

## Reporting Issues and Requesting Features

If you encounter any issues or have feature requests, please follow these steps to report them:

1. **Search for existing issues**: Before creating a new issue, search the [list of issues](https://github.com/Bryan-Roe/semantic-kernel/issues) to see if the issue has already been reported. If you find an existing issue, add your feedback or upvote it.

2. **Create a new issue**: If you cannot find an existing issue, create a new one by clicking on the "New Issue" button. Provide a clear and concise title for the issue and include the following details:
   - A high-level description of the problem or feature request.
   - Steps to reproduce the issue (if applicable).
   - Expected behavior and actual behavior observed.
   - Any relevant logs, screenshots, or error messages.
   - Information about your environment, such as OS, SDK version, and any other relevant details.

    - You can skip this step for trivial changes.
    - Reuse an existing issue on the topic, if there is one.
    - Get agreement from the team and the community that your proposed change is
      a good one.
    - Clearly state that you are going to take on implementing it, if that's the case.
      You can request that the issue be assigned to you. Note: The issue filer and
      the implementer don't have to be the same person.
2. Create a personal fork of the repository on GitHub (if you don't already have one).
3. In your fork, create a branch off of main (`git checkout -b mybranch`).
    - Name the branch so that it clearly communicates your intentions, such as
      "issue-123" or "githubhandle-issue".
4. Make and commit your changes to your branch.
5. Add new tests corresponding to your change, if applicable.
6. Build the repository with your changes.
    - Make sure that the builds are clean.
    - Make sure that the tests are all passing, including your new tests.
7. Create a PR against the repository's **main** branch.
    - State in the description what issue or improvement your change is addressing.
    - Verify that all the Continuous Integration checks are passing.
8. Wait for feedback or approval of your changes from the code maintainers.
9. When area owners have signed off, and all checks are green, your PR will be merged.

### PR - CI Process

The continuous integration (CI) system will automatically perform the required
builds and run tests (including the ones you are expected to run) for PRs. Builds
and test runs must be clean.

If the CI build fails for any reason, the PR issue will be updated with a link
that can be used to determine the cause of the failure.
