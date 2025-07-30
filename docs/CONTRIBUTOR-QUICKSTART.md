# Contributor Quickstart

This short guide helps new contributors set up their environment and submit a pull request.

## 1. Fork and Clone

1. Fork the repository on GitHub.
2. Clone your fork locally.

```bash
git clone <your-fork-url>
cd <repository-name>
```

## 2. Install Dependencies

### Python
Navigate to the Python implementation and set up the virtual environment:

```bash
cd 01-core-implementations/python
make install
```

This installs all required packages and configures pre-commit hooks.

### TypeScript

```bash
cd 01-core-implementations/typescript
npm install
```

### .NET

```bash
cd 01-core-implementations/dotnet
bash build.sh    # or dotnet restore
```

## 3. Run Tests

Run the relevant tests before submitting code:

```bash
# Python
pytest

# TypeScript
yarn test

# .NET
dotnet test
```

## 4. Submit a Pull Request

1. Create a branch for your work.
2. Commit your changes.
3. Push the branch to your fork and open a pull request against the `main` branch.

For detailed guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).
