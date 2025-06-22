# 🧪 Semantic Kernel Automated Test System

This directory contains a comprehensive automated testing system for the Semantic Kernel workspace, supporting .NET, Python, and JavaScript/TypeScript projects with parallel execution, coverage collection, and continuous integration.

## 🚀 Quick Start

### Local Testing

#### Using the Bash Script (Linux/macOS)
```bash
# Make script executable (first time only)
chmod +x ./run-auto-tests.sh

# Discover all test projects
./run-auto-tests.sh discover

# Run all tests
./run-auto-tests.sh run-all

# Run specific tests by pattern
./run-auto-tests.sh run "Unit" --coverage

# Run tests in watch mode
./run-auto-tests.sh watch --pattern "OpenAI"
```

#### Using PowerShell (Windows/Cross-platform)
```powershell
# Discover all test projects
./run-auto-tests.ps1 discover

# Run all tests with verbose output
./run-auto-tests.ps1 run-all -Verbose

# Run unit tests with coverage
./run-auto-tests.ps1 run "Unit" -Coverage

# Run tests in watch mode
./run-auto-tests.ps1 watch -Pattern "Integration"
```

### Using the .NET Test Runner (Advanced)
```bash
# Compile and run the test runner
dotnet run --project AutoTestProgram.cs discover
dotnet run --project AutoTestProgram.cs run-all --verbose --coverage
```

## 📊 Features

### ✅ Multi-Framework Support
- **🏗️ .NET**: xUnit, NUnit, MSTest projects with dotnet test
- **🐍 Python**: pytest with poetry for dependency management
- **📜 TypeScript/JavaScript**: Jest, Mocha, and other npm test runners

### ⚡ Performance Optimizations
- **Parallel Execution**: Run tests concurrently across multiple cores
- **Smart Discovery**: Automatic test project detection
- **Incremental Testing**: Watch mode for development
- **Caching**: Dependency and build artifact caching

### 📈 Coverage & Reporting
- **Code Coverage**: Collect coverage for all supported frameworks
- **Multiple Formats**: XML, HTML, JSON, and console reports
- **Integration**: Codecov, SonarQube, and other platforms
- **Trend Analysis**: Historical coverage tracking

### 🔄 CI/CD Integration
- **GitHub Actions**: Complete workflow with matrix builds
- **Cross-Platform**: Linux, Windows, and macOS support
- **Scheduled Runs**: Daily automated test execution
- **PR Integration**: Automatic test runs on pull requests

## 🏗️ Architecture

### Test Project Discovery
The system automatically discovers test projects using configurable patterns:

```
01-core-implementations/dotnet/
├── src/
│   ├── SemanticKernel.UnitTests/          # Unit tests
│   ├── Extensions.UnitTests/               # Extension unit tests
│   ├── Connectors.OpenAI.UnitTests/       # Connector tests
│   └── IntegrationTests/                   # Integration tests
python/
├── tests/
│   ├── unit/                              # Python unit tests
│   ├── integration/                       # Python integration tests
│   └── end-to-end/                        # E2E tests
typescript/
├── packages/
│   └── */tests/                           # TypeScript tests
```

### Execution Pipeline
1. **Discovery Phase**: Scan workspace for test projects
2. **Classification**: Categorize as Unit/Integration/E2E tests
3. **Parallel Execution**: Run tests with optimal concurrency
4. **Result Aggregation**: Combine results across frameworks
5. **Reporting**: Generate comprehensive reports

### Configuration System
Tests are configured via `auto-test-config.json`:

```json
{
  "testFrameworks": {
    "dotnet": {
      "enabled": true,
      "configuration": "Release",
      "parallel": true,
      "coverage": { "enabled": true, "threshold": 80 }
    },
    "python": {
      "enabled": true,
      "versions": ["3.10", "3.11", "3.12"],
      "coverage": { "minCoverage": 80 }
    }
  },
  "execution": {
    "maxParallelism": 4,
    "timeout": { "unit": 5, "integration": 15 }
  }
}
```

## 🔧 Configuration

### Environment Variables
- `SK_TEST_MODE`: Set to `true` for test environment
- `SK_TEST_TIMEOUT`: Override default test timeouts
- `SK_COVERAGE_THRESHOLD`: Minimum coverage percentage
- `SK_PARALLEL_TESTS`: Enable/disable parallel execution

### Test Categories
Tests are organized by categories using attributes/decorators:

#### .NET (xUnit)
```csharp
[Fact]
[Trait("Category", "Unit")]
public void TestMethod() { }

[Fact]
[Trait("Category", "Integration")]
public void IntegrationTest() { }
```

#### Python (pytest)
```python
import pytest

@pytest.mark.unit
def test_function():
    pass

@pytest.mark.integration
def test_integration():
    pass
```

## 📝 Test Writing Guidelines

### .NET Tests
Follow Semantic Kernel testing patterns:

```csharp
public class MyServiceTests
{
    [Fact]
    public async Task Method_Should_ReturnExpectedResult_When_ValidInput()
    {
        // Arrange
        var service = new MyService();
        var input = "test";

        // Act
        var result = await service.ProcessAsync(input);

        // Assert
        Assert.NotNull(result);
        Assert.Equal("expected", result);
    }

    [Theory]
    [InlineData("input1", "output1")]
    [InlineData("input2", "output2")]
    public void Method_Should_HandleMultipleInputs(string input, string expected)
    {
        // Test implementation
    }
}
```

### Python Tests
Use pytest conventions:

```python
import pytest
from semantic_kernel import Kernel

class TestSemanticKernel:
    def test_kernel_creation(self):
        """Test basic kernel creation."""
        kernel = Kernel()
        assert kernel is not None

    @pytest.mark.asyncio
    async def test_async_operation(self):
        """Test asynchronous operations."""
        kernel = Kernel()
        result = await kernel.invoke_async("test")
        assert result is not None

    @pytest.mark.parametrize("input,expected", [
        ("hello", "HELLO"),
        ("world", "WORLD"),
    ])
    def test_parametrized(self, input, expected):
        """Test with multiple parameters."""
        result = input.upper()
        assert result == expected
```

## 🔍 Troubleshooting

### Common Issues

#### Tests Not Found
```bash
# Check discovery
./run-auto-tests.sh discover

# Verify project patterns
find . -name "*Tests.csproj" -o -name "pytest.ini" -o -name "package.json"
```

#### Coverage Issues
```bash
# .NET coverage
dotnet test --collect:"XPlat Code Coverage"

# Python coverage
poetry run pytest --cov=semantic_kernel --cov-report=html
```

#### Performance Issues
- Reduce parallelism: `--max-parallelism 2`
- Increase timeouts: `--timeout 20`
- Run specific categories: `--filter "Category=Unit"`

### Debug Mode
Enable verbose logging for detailed output:

```bash
./run-auto-tests.sh run-all --verbose
```

## 🚀 CI/CD Pipeline

### GitHub Actions Workflow
The automated pipeline includes:

1. **🔍 Discovery Job**: Finds all test projects
2. **🏗️ .NET Tests**: Matrix build across OS and frameworks
3. **🐍 Python Tests**: Multi-version testing with tox
4. **📜 TypeScript Tests**: Node.js testing with npm
5. **🔗 Integration Tests**: Cross-component testing
6. **🔒 Security Scans**: Vulnerability and dependency checks
7. **⚡ Performance Tests**: Benchmark execution (scheduled)
8. **📋 Reporting**: Aggregate results and notifications

### Pipeline Triggers
- **Push**: Feature branches and main/develop
- **Pull Request**: Automatic test validation
- **Schedule**: Daily comprehensive test runs
- **Manual**: On-demand execution with parameters

### Artifacts
- Test results (JUnit XML, TRX)
- Coverage reports (Cobertura XML, HTML)
- Performance benchmarks
- Security scan results

## 📊 Metrics & Monitoring

### Test Metrics
- **Test Count**: Total, passed, failed, skipped
- **Coverage**: Line, branch, and method coverage
- **Performance**: Execution time trends
- **Reliability**: Flaky test detection

### Dashboard Integration
Results can be integrated with:
- **Azure DevOps**: Test analytics and reporting
- **GitHub**: Status checks and PR comments
- **Codecov**: Coverage trending and insights
- **SonarQube**: Quality gates and technical debt

## 🔄 Best Practices

### Test Organization
1. **Separate Concerns**: Unit, integration, and E2E tests
2. **Naming Conventions**: Clear, descriptive test names
3. **Test Data**: Use builders and fixtures
4. **Mocking**: Isolate units under test

### Performance
1. **Parallel Execution**: Enable for independent tests
2. **Resource Management**: Clean up after tests
3. **Test Isolation**: Avoid shared state
4. **Efficient Assertions**: Use specific, fast assertions

### Maintainability
1. **DRY Principle**: Extract common test utilities
2. **Documentation**: Comment complex test scenarios
3. **Regular Cleanup**: Remove obsolete tests
4. **Refactoring**: Keep tests in sync with code changes

## 📚 Additional Resources

- [xUnit Documentation](https://xunit.net/docs)
- [pytest Documentation](https://docs.pytest.org/)
- [GitHub Actions Documentation](https://docs.github.com/actions)
- [Semantic Kernel Testing Guidelines](https://github.com/microsoft/semantic-kernel/blob/main/CONTRIBUTING.md)

## 🤝 Contributing

1. **Add Tests**: Include tests for all new features
2. **Maintain Coverage**: Keep coverage above 80%
3. **Update Documentation**: Document test patterns
4. **Follow Conventions**: Use established naming and structure

For questions or issues, please refer to the [Semantic Kernel Contributing Guide](https://github.com/microsoft/semantic-kernel/blob/main/CONTRIBUTING.md).
