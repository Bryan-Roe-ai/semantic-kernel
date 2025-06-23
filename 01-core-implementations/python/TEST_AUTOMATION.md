# Test Automation for Semantic Kernel Python

This document describes the comprehensive test automation setup for the Semantic Kernel Python project.

## 🎯 Overview

The test automation system provides:

- **Automatic test execution** on file changes
- **Comprehensive test coverage** with unit, integration, and sample tests
- **Quality gates** with linting, type checking, and security analysis
- **Performance monitoring** with benchmarks
- **CI/CD integration** with GitHub Actions
- **Developer-friendly tools** for local development

## 🚀 Quick Start

### Prerequisites

```bash
# Install development dependencies
make install-dev

# Or with uv directly
uv sync --all-extras --dev
```

### Running Tests

```bash
# Run all unit tests
make test

# Run specific test suites
make test-unit           # Unit tests only
make test-integration    # Integration tests
make test-samples        # Sample tests
make test-all           # All test suites

# Quick feedback
make test-fast          # Fast unit tests (no coverage)
make test-parallel      # Parallel execution

# Quality checks
make lint               # Code linting
make format            # Code formatting
make type-check        # Type checking
make security-check    # Security analysis
make quality-check     # All quality checks

# Coverage reporting
make coverage          # Generate coverage report
make coverage-html     # HTML coverage report
```

## 📁 Test Structure

```
tests/
├── unit/                    # Unit tests
│   ├── agents/             # Agent-related tests
│   ├── connectors/         # AI connector tests
│   ├── core_plugins/       # Core plugin tests
│   └── ...
├── integration/            # Integration tests
│   ├── completions/        # AI completion tests
│   ├── embeddings/         # Embedding tests
│   └── ...
├── samples/                # Sample and documentation tests
├── fixtures/               # Test fixtures and data
└── conftest.py            # Shared test configuration
```

## 🛠️ Test Automation Tools

### 1. Auto Test Runner (`scripts/auto_test_runner.py`)

Comprehensive test runner with advanced features:

```bash
# Run with auto test runner
python scripts/auto_test_runner.py

# Options
python scripts/auto_test_runner.py --unit-only        # Unit tests only
python scripts/auto_test_runner.py --no-coverage     # Skip coverage
python scripts/auto_test_runner.py --verbose         # Verbose output
```

Features:

- ✅ Parallel test execution
- ✅ Coverage reporting
- ✅ Quality checks integration
- ✅ Detailed reporting
- ✅ CI/CD compatibility

### 2. Test Watcher (`scripts/test_watcher.py`)

Continuous testing with file watching:

```bash
# Start test watcher
python scripts/test_watcher.py

# Commands while running:
# [Enter] - Run all tests
# f       - Run fast tests
# q       - Quit
```

Features:

- 🔄 Automatic test execution on file changes
- 🎯 Intelligent test selection
- ⚡ Fast feedback loop
- 📊 Real-time results

### 3. Changed Files Testing (`scripts/test_changed_files.py`)

Test only files that have changed:

```bash
# Test changed files (git-aware)
python scripts/test_changed_files.py

# Used automatically by pre-commit hooks
```

### 4. Makefile Integration

Comprehensive make targets for all testing needs:

```bash
make test-help          # Show all test commands
make test-watch         # Watch for changes
make test-debug         # Debug mode
make test-profile       # Performance profiling
make clean-test         # Clean test artifacts
```

## 📊 Coverage and Reporting

### Coverage Configuration

```bash
# Generate coverage reports
make coverage

# HTML reports (opens in browser)
make coverage-html

# Coverage thresholds configured in pyproject.toml
```

### Test Reports

Reports are generated in `test_reports/`:

```
test_reports/
├── coverage.xml           # Coverage XML report
├── coverage_unit.xml      # Unit test coverage
├── htmlcov/              # HTML coverage reports
├── junit_unit.xml        # JUnit test results
├── bandit_report.json    # Security analysis
├── mypy_report.xml       # Type checking results
└── test_report.json      # Comprehensive test report
```

## 🔧 Configuration

### pytest Configuration (`pyproject.toml`)

```toml
[tool.pytest.ini_options]
testpaths = 'tests'
addopts = "-ra -q -r fEX"
asyncio_mode = "auto"
timeout = 120
markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "slow: Slow running tests",
    "azure: Tests requiring Azure services",
    # ... more markers
]
```

### Test Markers

Use markers to categorize and run specific tests:

```python
import pytest

@pytest.mark.unit
def test_basic_functionality():
    """Basic unit test."""
    pass

@pytest.mark.integration
@pytest.mark.azure
def test_azure_integration():
    """Azure integration test."""
    pass

@pytest.mark.slow
def test_performance():
    """Slow performance test."""
    pass
```

Run specific markers:

```bash
# Run only unit tests
pytest -m unit

# Run integration tests except slow ones
pytest -m "integration and not slow"

# Run Azure-related tests
pytest -m azure
```

## 🔄 CI/CD Integration

### GitHub Actions

The project includes comprehensive GitHub Actions workflows:

- **`.github/workflows/python-auto-tests.yml`** - Main test automation
- **Triggers**: Push, PR, schedule, manual
- **Matrix testing**: Multiple Python versions and OS
- **Parallel execution**: Different test suites in parallel
- **Artifact collection**: Test reports and coverage

### Workflow Jobs

1. **Lint and Format** - Fast feedback on code quality
2. **Security Analysis** - Security vulnerability scanning
3. **Unit Tests** - Core functionality testing with coverage
4. **Integration Tests** - External service integration
5. **Performance Benchmarks** - Performance regression detection
6. **Test Reporting** - Consolidated test results

### Pre-commit Hooks

Automatic quality checks before commits:

```bash
# Install pre-commit hooks
make install-pre-commit

# Run manually
pre-commit run --all-files
```

Hooks include:

- 🔍 Linting with ruff
- 🎨 Code formatting
- 🔒 Security scanning
- ⚡ Fast test execution
- 📝 Documentation checks

## 🎯 Best Practices

### Writing Tests

1. **Use descriptive test names**:

   ```python
   def test_kernel_function_should_execute_with_valid_arguments():
       """Test that kernel function executes successfully with valid arguments."""
       pass
   ```

2. **Organize tests by functionality**:

   ```
   tests/unit/connectors/openai/
   ├── test_openai_chat_completion.py
   ├── test_openai_text_completion.py
   └── test_openai_embeddings.py
   ```

3. **Use appropriate markers**:

   ```python
   @pytest.mark.unit
   def test_unit_functionality():
       pass

   @pytest.mark.integration
   @pytest.mark.azure
   def test_azure_integration():
       pass
   ```

4. **Mock external dependencies**:
   ```python
   @patch('semantic_kernel.connectors.openai.OpenAIClient')
   def test_with_mocked_client(mock_client):
       pass
   ```

### Test Configuration

1. **Environment Variables**:

   ```bash
   # .env.example
   AZURE_OPENAI_API_KEY=your_key_here
   AZURE_OPENAI_ENDPOINT=your_endpoint_here
   OPENAI_API_KEY=your_key_here
   ```

2. **Fixtures for Reusability**:

   ```python
   @pytest.fixture
   def kernel():
       return Kernel()

   @pytest.fixture
   def mock_completion_service():
       return Mock(spec=ChatCompletionClientBase)
   ```

3. **Parameterized Tests**:
   ```python
   @pytest.mark.parametrize("input,expected", [
       ("hello", "HELLO"),
       ("world", "WORLD"),
   ])
   def test_uppercase(input, expected):
       assert input.upper() == expected
   ```

## 🚨 Troubleshooting

### Common Issues

1. **Tests are slow**:

   ```bash
   # Run fast subset
   make test-fast

   # Use parallel execution
   make test-parallel

   # Run specific tests
   pytest tests/unit/specific_test.py
   ```

2. **Coverage is low**:

   ```bash
   # Check coverage report
   make coverage-html

   # Identify untested code
   make coverage-report
   ```

3. **Tests fail in CI but pass locally**:

   - Check environment variables
   - Verify dependencies
   - Check for timing issues
   - Review CI logs

4. **Pre-commit hooks are slow**:

   ```bash
   # Skip hooks temporarily
   git commit --no-verify

   # Run specific hooks
   pre-commit run ruff-check
   ```

### Debug Mode

```bash
# Run tests in debug mode
make test-debug

# Or with pytest directly
pytest tests/unit/test_specific.py -v --tb=long --capture=no
```

### Environment Checks

```bash
# Check test environment
make check-test-env

# Validate configuration
python scripts/test_config.py --validate
```

## 📈 Performance and Optimization

### Parallel Execution

```bash
# Automatic CPU detection
pytest -n auto

# Specific number of workers
pytest -n 4

# Or use make target
make test-parallel
```

### Test Selection

```bash
# Run only fast tests
pytest -m "not slow"

# Skip integration tests
pytest -m "not integration"

# Run changed files only
python scripts/test_changed_files.py
```

### Caching

```bash
# Clear pytest cache
make clean-test-cache

# Clear all test artifacts
make clean-test
```

## 🔗 Integration with IDEs

### VS Code

1. **Install Python Test Explorer**
2. **Configure settings.json**:
   ```json
   {
     "python.testing.pytestEnabled": true,
     "python.testing.pytestArgs": ["tests"],
     "python.testing.autoTestDiscoverOnSaveEnabled": true
   }
   ```

### PyCharm

1. **Configure Test Runner**: Settings → Tools → Python Integrated Tools → Testing
2. **Set Default Test Runner**: pytest
3. **Configure Coverage**: Run → Edit Configurations → Coverage

## 📚 Additional Resources

- [pytest Documentation](https://docs.pytest.org/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [Pre-commit Documentation](https://pre-commit.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## 🤝 Contributing

When contributing to the test suite:

1. **Add tests for new features**
2. **Maintain test coverage above 80%**
3. **Use appropriate test markers**
4. **Follow naming conventions**
5. **Update documentation**

### Pull Request Checklist

- [ ] Tests pass locally (`make test-all`)
- [ ] Code is formatted (`make format`)
- [ ] Linting passes (`make lint`)
- [ ] Type checking passes (`make type-check`)
- [ ] Coverage maintained (`make coverage`)
- [ ] Documentation updated

---

For more information or questions about the test automation system, please refer to the project documentation or open an issue.
