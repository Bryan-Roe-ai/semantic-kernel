# 🧪 Semantic Kernel Auto Test System

> **Complete automated testing solution for the Semantic Kernel workspace with multi-framework support, CI/CD integration, and comprehensive reporting.**

## 🚀 Quick Start

### 1. Check Prerequisites
```bash
./test-automation-guide.sh check
```

### 2. Discover Tests
```bash
./simple-auto-tests.sh discover
```

### 3. Run Tests
```bash
# Run Python unit tests
./vscode-task-runner.sh python-unit

# Run all .NET tests  
./simple-auto-tests.sh dotnet

# Run everything
./simple-auto-tests.sh all
```

## 📁 Files Created

### Core Test Runners
- **`simple-auto-tests.sh`** - Main test runner with basic functionality
- **`vscode-task-runner.sh`** - Integration with VS Code tasks
- **`test-automation-guide.sh`** - Interactive guide and help system

### Advanced Runners (Comprehensive)
- **`run-auto-tests.sh`** - Full-featured bash runner with watch mode
- **`run-auto-tests.ps1`** - PowerShell cross-platform runner
- **`AutoTestRunner.cs`** - .NET test discovery and execution engine
- **`AutoTestProgram.cs`** - Console application for automated testing

### Configuration & CI/CD
- **`.github/workflows/auto-tests.yml`** - GitHub Actions workflow
- **`auto-test-config.json`** - Comprehensive configuration schema
- **`AUTO_TEST_README.md`** - Detailed documentation

## 🎯 Key Features

### ✅ Multi-Framework Support
- **🏗️ .NET**: xUnit, NUnit, MSTest (79 projects discovered)
- **🐍 Python**: pytest with poetry (unit, integration, end-to-end)
- **📜 TypeScript**: Jest, Mocha, npm test runners

### ⚡ Smart Execution
- **Parallel Testing**: Multi-core test execution
- **Pattern Matching**: Run specific test subsets
- **Watch Mode**: Automatic re-runs on file changes
- **Coverage Collection**: Code coverage for all frameworks

### 🔄 CI/CD Ready
- **GitHub Actions**: Complete workflow with matrix builds
- **Cross-Platform**: Linux, Windows, macOS support
- **Scheduled Runs**: Daily automated testing
- **PR Integration**: Automatic test validation

## 📊 Test Discovery Results

```
📊 Test Discovery Results:
  🏗️ .NET Projects: 79
  🐍 Python Test Dirs: 3

📦 Sample .NET Test Projects:
  • AzureAISearch.UnitTests
  • PgVector.UnitTests  
  • Redis.ConformanceTests
  • Weaviate.ConformanceTests
  • SqlServer.ConformanceTests
```

## 🔧 Usage Examples

### Basic Testing
```bash
# Discover all test projects
./simple-auto-tests.sh discover

# Run .NET tests with coverage
./simple-auto-tests.sh dotnet --coverage

# Run Python integration tests
./simple-auto-tests.sh python-int --verbose

# Run everything
./simple-auto-tests.sh all
```

### VS Code Task Integration
```bash
# Setup Python environment
./vscode-task-runner.sh setup-python

# Run Python unit tests
./vscode-task-runner.sh python-unit

# Run all Python tests
./vscode-task-runner.sh python-all
```

### Advanced Usage (if available)
```bash
# Watch mode for development
./run-auto-tests.sh watch --pattern "OpenAI"

# Run specific pattern with coverage
./run-auto-tests.sh run "Unit" --coverage --verbose

# PowerShell version
./run-auto-tests.ps1 run-all -Coverage -Verbose
```

## 🛠️ Setup Instructions

### 1. Prerequisites
- **.NET SDK 8.0+** (for .NET tests)
- **Python 3.10+** (for Python tests)  
- **Poetry** (for Python dependency management)
- **Node.js 18+** (for TypeScript tests)

### 2. Install Missing Tools
```bash
# Install Poetry (if missing)
curl -sSL https://install.python-poetry.org | python3 -

# Install .NET SDK (Ubuntu/Debian)
wget https://packages.microsoft.com/config/ubuntu/22.04/packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
sudo apt update && sudo apt install -y dotnet-sdk-8.0
```

### 3. Setup Python Environment
```bash
cd python
poetry install
```

### 4. Make Scripts Executable
```bash
chmod +x *.sh
```

## 🔄 GitHub Actions Workflow

The automated CI/CD pipeline includes:

### Jobs
1. **🔍 Discovery**: Find all test projects across frameworks
2. **🏗️ .NET Tests**: Matrix builds across OS (Ubuntu, Windows, macOS)
3. **🐍 Python Tests**: Multi-version testing (3.10, 3.11, 3.12)
4. **📜 TypeScript Tests**: Node.js testing with npm
5. **🔗 Integration Tests**: Cross-component validation
6. **🔒 Security Scans**: Vulnerability and dependency checks
7. **⚡ Performance Tests**: Benchmark execution (scheduled)
8. **📋 Reporting**: Aggregate results and notifications

### Triggers
- **Push**: Feature branches, main/develop
- **Pull Request**: Automatic validation
- **Schedule**: Daily at 2 AM UTC
- **Manual**: Workflow dispatch with parameters

### Features
- **Code Coverage**: Codecov integration
- **Test Reports**: JUnit XML, TRX formats
- **Artifact Upload**: Test results and coverage
- **PR Comments**: Automated test summaries
- **Failure Notifications**: Email/Slack integration

## 📈 Coverage & Reporting

### Coverage Collection
```bash
# .NET coverage
./simple-auto-tests.sh dotnet --coverage

# Python coverage  
./simple-auto-tests.sh python --coverage
```

### Report Formats
- **Console**: Real-time test results
- **XML**: JUnit, TRX, Cobertura formats
- **HTML**: Interactive coverage reports
- **JSON**: Machine-readable results

## 🎛️ Configuration

### Environment Variables
```bash
export SK_TEST_MODE=true
export SK_COVERAGE_THRESHOLD=80
export SK_PARALLEL_TESTS=true
export SK_TEST_TIMEOUT=300
```

### Configuration File
See `auto-test-config.json` for comprehensive settings:
- Test framework configuration
- Execution parameters
- Coverage thresholds
- CI/CD integration
- Security scanning

## 🔧 Troubleshooting

### Common Issues

#### Poetry Not Found
```bash
curl -sSL https://install.python-poetry.org | python3 -
# or
pip3 install poetry
```

#### .NET Tests Failing
```bash
dotnet restore
dotnet build --configuration Release
```

#### Permission Denied
```bash
chmod +x *.sh
```

#### Test Discovery Issues
Check project patterns in `auto-test-config.json`

### Debug Mode
```bash
./simple-auto-tests.sh discover --verbose
```

### Get Help
```bash
# Interactive guide
./test-automation-guide.sh

# Show all options
./test-automation-guide.sh all

# Quick start
./test-automation-guide.sh quick
```

## 🏗️ Architecture

### Test Discovery
- **Pattern-based**: Configurable file patterns
- **Multi-framework**: .NET, Python, TypeScript
- **Classification**: Unit, Integration, End-to-End
- **Metadata**: Framework, runner, capabilities

### Execution Engine
- **Parallel Processing**: Optimal core utilization
- **Timeout Management**: Per-test-type timeouts
- **Result Aggregation**: Cross-framework reporting
- **Error Handling**: Graceful failure management

### Integration Points
- **VS Code Tasks**: Seamless IDE integration
- **GitHub Actions**: Complete CI/CD pipeline
- **Coverage Tools**: Codecov, SonarQube support
- **Notification Systems**: Slack, Teams, email

## 🤝 Contributing

### Adding New Tests
1. Follow framework conventions (xUnit, pytest, Jest)
2. Include appropriate test categories/markers
3. Update discovery patterns if needed
4. Maintain coverage thresholds

### Extending Automation
1. Update configuration schema
2. Add new framework support in runners
3. Update GitHub Actions workflow
4. Document new features

### Best Practices
- **Test Isolation**: Independent, repeatable tests
- **Performance**: Efficient test execution
- **Coverage**: Meaningful test coverage
- **Documentation**: Clear test intentions

## 📚 Resources

- [Semantic Kernel Documentation](https://learn.microsoft.com/semantic-kernel/)
- [xUnit Testing Framework](https://xunit.net/)
- [pytest Documentation](https://docs.pytest.org/)
- [GitHub Actions Guide](https://docs.github.com/actions)
- [Poetry Documentation](https://python-poetry.org/)

---

🎉 **Happy Testing!** The Semantic Kernel auto test system provides comprehensive testing automation for confident development and deployment.
