SHELL = /bin/bash

.PHONY: help install install-uv install-python install-pre-commit install-sk clean build
.SILENT:  # not strictly required, but included per the original example
all: install

ifeq ($(PYTHON_VERSION),)
    PYTHON_VERSION = 3.10
endif

# Detect uv on PATH
UV_VERSION := $(shell command -v uv 2> /dev/null)

##############################
#  HELP
##############################
.ONESHELL:
help:
	echo -e "\033[1mUSAGE:\033[0m"
	echo "  make [target]"
	echo ""
	echo -e "\033[1mTARGETS:\033[0m"
	echo "  help                 - show this help message"
	echo "  install              - install uv, python, Semantic Kernel, and all dependencies"
	echo "                        This is the default and will use Python 3.10."
	echo "  install-uv           - install uv"
	echo "  install-python       - install multiple python distributions"
	echo "  install-sk           - install Semantic Kernel and all dependencies"
	echo "  install-pre-commit   - install pre-commit hooks"
	echo "  clean                - remove the virtualenvs"
	echo "  build                - build the project"
	echo ""
	echo -e "\033[1mVARIABLES:\033[0m"
	echo "  PYTHON_VERSION       - Python version to use. Default is 3.10"
	echo "                        By default, 3.10, 3.11, 3.12 and 3.13 are installed as well."

##############################
#  INSTALL
##############################
install:
	make install-uv
	make install-python
	make install-sk
	make install-pre-commit

##############################
#  INSTALL-UV
##############################
install-uv:
	# If uv is not found AND we haven't already re-invoked with CONTINUE=1...
ifneq ($(UV_VERSION),)
	echo "uv found at: $(UV_VERSION)"
	echo "running uv self update"
	uv self update
else ifeq ($(CONTINUE),1)
	echo "Skipping uv re-install; continuing with the rest of the steps."
else
	echo "uv could not be found."
	echo "Installing uv..."
	if [ -n "$$VIRTUAL_ENV" ]; then \
	    echo "Detected virtual environment at $$VIRTUAL_ENV, installing uv there..."; \
	    curl -LsSf https://astral.sh/uv/install.sh | INSTALL_DIR="$$VIRTUAL_ENV/bin" sh; \
	else \
	    echo "No virtual environment detected, installing uv globally..."; \
	    curl -LsSf https://astral.sh/uv/install.sh | sh; \
	fi
	echo "uv installed."
	echo "Re-executing shell so uv is immediately available on PATH..."
	exec $$SHELL -c 'make install CONTINUE=1'
endif

##############################
#  INSTALL-PYTHON
##############################
.ONESHELL:
install-python:
	echo "Installing python versions"
	uv python install 3.10 3.11 3.12 3.13

##############################
#  INSTALL-PRE-COMMIT
##############################
.ONESHELL:
install-pre-commit:
	echo "Installing pre-commit hooks"
	uv run pre-commit install -c python/.pre-commit-config.yaml

##############################
#  INSTALL-SK
##############################
.ONESHELL:
install-sk:
	echo "Creating and activating venv for python $(PYTHON_VERSION)"
	uv venv --python $(PYTHON_VERSION)
	echo "Installing Semantic Kernel and all dependencies"
	uv sync --all-extras --dev --prerelease=if-necessary-or-explicit

##############################
#  CLEAN
##############################
.ONESHELL:
clean:
	rm -rf .venv

##############################
#  BUILD
##############################
build:
	uvx --from build pyproject-build --installer uv
SHELL = bash

.PHONY: help install clean build
.SILENT:
all: install

ifeq ($(PYTHON_VERSION),)
    PYTHON_VERSION="3.10"
endif

.ONESHELL:
help:
	echo -e "\033[1mUSAGE:\033[0m"
	echo "  make [target]"
	echo ""
	echo -e "\033[1mTARGETS:\033[0m"
	echo "  help                 - show this help message"
	echo "  install              - install uv, python, Semantic Kernel and all dependencies"
	echo "      This is the default and will use Python 3.10."
	echo "  install-uv           - install uv"
	echo "  install-python       - install python distributions"
	echo "  install-sk           - install Semantic Kernel and all dependencies"
	echo "  install-pre-commit   - install pre-commit hooks"
	echo "  clean                - remove the virtualenvs"
	echo "  build                - build the project"
	echo ""
	echo -e "\033[1mVARIABLES:\033[0m"
	echo "  PYTHON_VERSION       - Python version to use. Default is 3.10"
	echo "      By default, 3.10, 3.11 and 3.12 are installed as well."

install:
	make install-uv
	make install-python
	make install-sk
	make install-pre-commit

UV_VERSION = $(shell uv --version 2> /dev/null)
install-uv:
# Check if uv is installed
ifdef UV_VERSION
	echo "uv found $(UV_VERSION)"
	echo "running uv update"
	uv self update 
else
	echo "uv could not be found"
	echo "Installing uv"
	curl -LsSf https://astral.sh/uv/install.sh | sh
endif

.ONESHELL:
install-python:
	echo "Installing python 3.10, 3.11, 3.12"
	uv python install 3.10 3.11 3.12

.ONESHELL:
install-pre-commit:
	echo "Installing pre-commit hooks"
	uv run pre-commit install -c python/.pre-commit-config.yaml


.ONESHELL:
install-sk:
	echo "Creating and activating venv for python $(PYTHON_VERSION)"
	uv venv --python $(PYTHON_VERSION)
	echo "Installing Semantic Kernel and all dependencies"
	uv sync --all-extras --dev
	
.ONESHELL:
clean:
	# Remove the virtualenv
	rm -rf .venv

build:
	uvx --from build pyproject-build --installer uv
SHELL = bash

.PHONY: help install clean build
.SILENT:
all: install

ifeq ($(PYTHON_VERSION),)
    PYTHON_VERSION="3.10"
endif

.ONESHELL:
help:
	echo -e "\033[1mUSAGE:\033[0m"
	echo "  make [target]"
	echo ""
	echo -e "\033[1mTARGETS:\033[0m"
	echo "  help                 - show this help message"
	echo "  install              - install uv, python, Semantic Kernel and all dependencies"
	echo "      This is the default and will use Python 3.10."
	echo "  install-uv           - install uv"
	echo "  install-python       - install python distributions"
	echo "  install-sk           - install Semantic Kernel and all dependencies"
	echo "  install-pre-commit   - install pre-commit hooks"
	echo "  clean                - remove the virtualenvs"
	echo "  build                - build the project"
	echo ""
	echo -e "\033[1mVARIABLES:\033[0m"
	echo "  PYTHON_VERSION       - Python version to use. Default is 3.10"
	echo "      By default, 3.10, 3.11 and 3.12 are installed as well."

install:
	make install-uv
	make install-python
	make install-sk
	make install-pre-commit

UV_VERSION = $(shell uv --version 2> /dev/null)
install-uv:
# Check if uv is installed
ifdef UV_VERSION
	echo "uv found $(UV_VERSION)"
	echo "running uv update"
	uv self update 
else
	echo "uv could not be found"
	echo "Installing uv"
	curl -LsSf https://astral.sh/uv/install.sh | sh
endif

.ONESHELL:
install-python:
	echo "Installing python 3.10, 3.11, 3.12"
	uv python install 3.10 3.11 3.12

.ONESHELL:

.PHONY: help install clean build
.SILENT:
all: install

ifeq ($(PYTHON_VERSION),)
    PYTHON_VERSION="3.10"
endif

.ONESHELL:
help:
	echo -e "\033[1mUSAGE:\033[0m"
	echo "  make [target]"
	echo ""
	echo -e "\033[1mTARGETS:\033[0m"
	echo "  help                 - show this help message"
	echo "  install              - install uv, python, Semantic Kernel and all dependencies"
	echo "      This is the default and will use Python 3.10."
	echo "  install-uv           - install uv"
	echo "  install-python       - install python distributions"
	echo "  install-sk           - install Semantic Kernel and all dependencies"
	echo "  install-pre-commit   - install pre-commit hooks"
	echo "  clean                - remove the virtualenvs"
	echo "  build                - build the project"
	echo ""
	echo -e "\033[1mVARIABLES:\033[0m"
	echo "  PYTHON_VERSION       - Python version to use. Default is 3.10"
	echo "      By default, 3.10, 3.11 and 3.12 are installed as well."

install:
	make install-uv
	make install-python
	make install-sk
	make install-pre-commit

UV_VERSION = $(shell uv --version 2> /dev/null)
install-uv:
# Check if uv is installed
ifdef UV_VERSION
	echo "uv found $(UV_VERSION)"
	echo "running uv update"
	uv self update 
else
	echo "uv could not be found"
	echo "Installing uv"
	curl -LsSf https://astral.sh/uv/install.sh | sh
endif

.ONESHELL:
install-python:
	echo "Installing python 3.10, 3.11, 3.12"
	uv python install 3.10 3.11 3.12

.ONESHELL:
install-pre-commit:
	echo "Installing pre-commit hooks"
	uv run pre-commit install -c python/.pre-commit-config.yaml


.ONESHELL:
install-sk:
	echo "Creating and activating venv for python $(PYTHON_VERSION)"
	uv venv --python $(PYTHON_VERSION)
	echo "Installing Semantic Kernel and all dependencies"
	uv sync --all-extras --dev
	
.ONESHELL:
clean:
	# Remove the virtualenv
	rm -rf .venv

build:
	uvx --from build pyproject-build --installer uv
SHELL = bash

.PHONY: help install clean build
.SILENT:
all: install

ifeq ($(PYTHON_VERSION),)
    PYTHON_VERSION="3.10"
endif

.ONESHELL:
help:
	echo -e "\033[1mUSAGE:\033[0m"
	echo "  make [target]"
	echo ""
	echo -e "\033[1mTARGETS:\033[0m"
	echo "  help                 - show this help message"
	echo "  install              - install uv, python, Semantic Kernel and all dependencies"
	echo "      This is the default and will use Python 3.10."
	echo "  install-uv           - install uv"
	echo "  install-python       - install python distributions"
	echo "  install-sk           - install Semantic Kernel and all dependencies"
	echo "  install-pre-commit   - install pre-commit hooks"
	echo "  clean                - remove the virtualenvs"
	echo "  build                - build the project"
	echo ""
	echo -e "\033[1mVARIABLES:\033[0m"
	echo "  PYTHON_VERSION       - Python version to use. Default is 3.10"
	echo "      By default, 3.10, 3.11 and 3.12 are installed as well."

install:
	make install-uv
	make install-python
	make install-sk
	make install-pre-commit

UV_VERSION = $(shell uv --version 2> /dev/null)
install-uv:
# Check if uv is installed
ifdef UV_VERSION
	echo "uv found $(UV_VERSION)"
	echo "running uv update"
	uv self update 
else
	echo "uv could not be found"
	echo "Installing uv"
	curl -LsSf https://astral.sh/uv/install.sh | sh
endif

.ONESHELL:
install-python:
	echo "Installing python 3.10, 3.11, 3.12"
	uv python install 3.10 3.11 3.12

.ONESHELL:
install-pre-commit:
	echo "Installing pre-commit hooks"
	uv run pre-commit install -c python/.pre-commit-config.yaml


.ONESHELL:
install-pre-commit:
	echo "Installing pre-commit hooks"
	uv run pre-commit install -c python/.pre-commit-config.yaml

SHELL = bash

.PHONY: help install recreate-env pre-commit

help:
	@echo -e "\033[1mUSAGE:\033[0m"
	@echo "  make [target]"
	@echo ""
	@echo -e "\033[1mTARGETS:\033[0m"
	@echo "  install              - install Poetry and project dependencies"
	@echo "  install-pre-commit   - install and configure pre-commit hooks"
	@echo "  pre-commit           - run pre-commit hooks on all files"
	@echo "  recreate-env         - destroy and recreate Poetry's virtualenv"

.ONESHELL:
install:
	@# Check to make sure Python is installed
	@if ! command -v python3 &> /dev/null
	then
		echo "Python could not be found"
		echo "Please install Python"
		exit 1
	fi

	@# Check if Poetry is installed
	@if ! command -v poetry &> /dev/null
	then
		echo "Poetry could not be found"
		echo "Installing Poetry"
		curl -sSL https://install.python-poetry.org | python3 -
	fi 

	# Install the dependencies
	poetry install

.ONESHELL:
recreate-env:
	# Stop the current virtualenv if active or alternative use
	# `exit` to exit from a Poetry shell session
	(deactivate || exit 0)

	# Remove all the files of the current environment of the folder we are in
	export POETRY_LOCATION=$$(poetry env info -p) 
	echo "Poetry is $${POETRY_LOCATION}"
	rm -rf "$${POETRY_LOCATION}"

pre-commit:
	poetry run pre-commit run --all-files -c .conf/.pre-commit-config.yaml

.ONESHELL:
install-pre-commit:
	poetry run pre-commit install
	# Edit the pre-commit config file to change the config path
	sed -i 's|\.pre-commit-config\.yaml|\.conf/\.pre-commit-config\.yaml|g' .git/hooks/pre-commit
install-sk:
	echo "Creating and activating venv for python $(PYTHON_VERSION)"
	uv venv --python $(PYTHON_VERSION)
	echo "Installing Semantic Kernel and all dependencies"
	uv sync --all-extras --dev
	
.ONESHELL:
clean:
	# Remove the virtualenv
	rm -rf .venv

build:
	uvx --from build pyproject-build --installer uv

##############################
#  TEST AUTOMATION
##############################

.PHONY: test test-unit test-integration test-samples test-all test-fast test-ci
.PHONY: lint format type-check security-check quality-check
.PHONY: coverage coverage-report coverage-html
.PHONY: test-parallel test-watch test-debug test-profile

# Variables for testing
PYTEST := uv run pytest
RUFF := uv run ruff
MYPY := uv run mypy
BANDIT := uv run bandit
SRC_DIR := semantic_kernel
TEST_DIR := tests
REPORTS_DIR := test_reports
SCRIPTS_DIR := scripts

# Colors for output
RED := \033[31m
GREEN := \033[32m
YELLOW := \033[33m
BLUE := \033[34m
RESET := \033[0m

# Ensure reports directory exists
$(REPORTS_DIR):
	mkdir -p $(REPORTS_DIR)

# Testing targets
test: test-unit ## Run default tests (unit tests)

test-unit: $(REPORTS_DIR) ## Run unit tests with coverage
	@echo -e "$(GREEN)Running unit tests...$(RESET)"
	$(PYTEST) $(TEST_DIR)/unit \
		-v \
		--tb=short \
		--cov=$(SRC_DIR) \
		--cov-report=term-missing \
		--cov-report=xml:$(REPORTS_DIR)/coverage_unit.xml \
		--cov-report=html:$(REPORTS_DIR)/htmlcov_unit \
		--timeout=60 \
		--junit-xml=$(REPORTS_DIR)/junit_unit.xml

test-integration: $(REPORTS_DIR) ## Run integration tests
	@echo -e "$(GREEN)Running integration tests...$(RESET)"
	$(PYTEST) $(TEST_DIR)/integration \
		-v \
		--tb=short \
		--cov=$(SRC_DIR) \
		--cov-report=xml:$(REPORTS_DIR)/coverage_integration.xml \
		--cov-report=html:$(REPORTS_DIR)/htmlcov_integration \
		--timeout=300 \
		--junit-xml=$(REPORTS_DIR)/junit_integration.xml

test-samples: $(REPORTS_DIR) ## Run sample tests
	@echo -e "$(GREEN)Running sample tests...$(RESET)"
	$(PYTEST) $(TEST_DIR)/samples \
		-v \
		--tb=short \
		--timeout=180 \
		--junit-xml=$(REPORTS_DIR)/junit_samples.xml

test-fast: ## Run fast unit tests (no coverage)
	@echo -e "$(GREEN)Running fast unit tests...$(RESET)"
	$(PYTEST) $(TEST_DIR)/unit \
		-v \
		--tb=short \
		--timeout=30 \
		-x

test-parallel: $(REPORTS_DIR) ## Run tests in parallel
	@echo -e "$(GREEN)Running tests in parallel...$(RESET)"
	$(PYTEST) $(TEST_DIR)/unit \
		-v \
		--tb=short \
		--cov=$(SRC_DIR) \
		--cov-report=term-missing \
		-n auto \
		--timeout=60

test-all: test-unit test-integration test-samples ## Run all tests

test-ci: $(REPORTS_DIR) ## Run tests for CI/CD (includes quality checks)
	@echo -e "$(GREEN)Running CI tests...$(RESET)"
	uv run python $(SCRIPTS_DIR)/auto_test_runner.py

test-specific: ## Run specific test (usage: make test-specific TEST=path/to/test)
	@echo -e "$(GREEN)Running specific test: $(TEST)$(RESET)"
	$(PYTEST) $(TEST) -v --tb=short

test-watch: ## Watch for changes and run tests
	@echo -e "$(GREEN)Watching for changes...$(RESET)"
	uv run watchmedo auto-restart \
		--patterns="*.py" \
		--recursive \
		--signal SIGTERM \
		-- make test-fast

test-debug: ## Run tests with debugging enabled
	@echo -e "$(GREEN)Running tests with debugging...$(RESET)"
	$(PYTEST) $(TEST_DIR)/unit -v --tb=long --capture=no

test-profile: $(REPORTS_DIR) ## Profile test execution
	@echo -e "$(GREEN)Profiling test execution...$(RESET)"
	$(PYTEST) $(TEST_DIR)/unit \
		--profile \
		--profile-svg

# Quality checks
lint: ## Run linting with ruff
	@echo -e "$(GREEN)Running linting...$(RESET)"
	$(RUFF) check $(SRC_DIR) $(TEST_DIR) $(SCRIPTS_DIR)

lint-fix: ## Fix linting issues automatically
	@echo -e "$(GREEN)Fixing linting issues...$(RESET)"
	$(RUFF) check --fix $(SRC_DIR) $(TEST_DIR) $(SCRIPTS_DIR)

format: ## Format code with ruff
	@echo -e "$(GREEN)Formatting code...$(RESET)"
	$(RUFF) format $(SRC_DIR) $(TEST_DIR) $(SCRIPTS_DIR)

format-check: ## Check code formatting
	@echo -e "$(GREEN)Checking code formatting...$(RESET)"
	$(RUFF) format --check $(SRC_DIR) $(TEST_DIR) $(SCRIPTS_DIR)

type-check: $(REPORTS_DIR) ## Run type checking with mypy
	@echo -e "$(GREEN)Running type checking...$(RESET)"
	$(MYPY) $(SRC_DIR) \
		--strict \
		--show-error-codes \
		--junit-xml=$(REPORTS_DIR)/mypy_report.xml

security-check: $(REPORTS_DIR) ## Run security checks with bandit
	@echo -e "$(GREEN)Running security checks...$(RESET)"
	$(BANDIT) -r $(SRC_DIR) \
		-f json \
		-o $(REPORTS_DIR)/bandit_report.json \
		|| true

quality-check: lint type-check security-check ## Run all quality checks

# Coverage
coverage: $(REPORTS_DIR) ## Generate coverage report
	@echo -e "$(GREEN)Generating coverage report...$(RESET)"
	$(PYTEST) $(TEST_DIR)/unit \
		--cov=$(SRC_DIR) \
		--cov-report=term-missing \
		--cov-report=xml:$(REPORTS_DIR)/coverage.xml \
		--cov-report=html:$(REPORTS_DIR)/htmlcov

coverage-report: ## Show coverage report
	@echo -e "$(GREEN)Coverage Report:$(RESET)"
	@uv run coverage report --show-missing

coverage-html: $(REPORTS_DIR) ## Generate HTML coverage report
	@echo -e "$(GREEN)Generating HTML coverage report...$(RESET)"
	uv run coverage html -d $(REPORTS_DIR)/htmlcov
	@echo -e "$(GREEN)HTML coverage report generated at $(REPORTS_DIR)/htmlcov/index.html$(RESET)"

# Benchmarking and performance
benchmark: ## Run performance benchmarks
	@echo -e "$(GREEN)Running benchmarks...$(RESET)"
	$(PYTEST) $(TEST_DIR) -k "benchmark" --benchmark-only

performance-test: ## Run performance tests
	@echo -e "$(GREEN)Running performance tests...$(RESET)"
	$(PYTEST) $(TEST_DIR) -m "performance" -v

# Cleanup for tests
clean-test-cache: ## Clean pytest and coverage cache
	@echo -e "$(GREEN)Cleaning test caches...$(RESET)"
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true

clean-test-reports: ## Clean test reports
	@echo -e "$(GREEN)Cleaning test reports...$(RESET)"
	rm -rf $(REPORTS_DIR)

clean-pyc: ## Clean Python cache files
	@echo -e "$(GREEN)Cleaning Python cache files...$(RESET)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

clean-test: clean-test-cache clean-test-reports clean-pyc ## Clean all test artifacts

# Release helpers
version-check: ## Check version consistency
	@echo -e "$(GREEN)Checking version consistency...$(RESET)"
	uv run python $(SCRIPTS_DIR)/check_version.py

release-test: ## Run full test suite for release
	@echo -e "$(GREEN)Running release test suite...$(RESET)"
	$(MAKE) clean-test
	$(MAKE) install-sk
	$(MAKE) test-all
	$(MAKE) quality-check

# Environment checks
check-test-env: ## Check test environment
	@echo -e "$(GREEN)Checking test environment...$(RESET)"
	@echo "Python version: $$(uv run python --version)"
	@echo "Pytest version: $$(uv run pytest --version)"
	@echo "Ruff version: $$(uv run ruff --version)"
	@echo "MyPy version: $$(uv run mypy --version 2>/dev/null || echo 'MyPy not available')"
	@echo "Coverage version: $$(uv run coverage --version 2>/dev/null || echo 'Coverage not available')"

# Add test targets to help
test-help: ## Show test-specific help
	@echo -e "$(BLUE)Test Automation Commands$(RESET)"
	@echo "========================"
	@echo ""
	@echo -e "$(GREEN)Basic Testing:$(RESET)"
	@echo "  make test           - Run unit tests with coverage"
	@echo "  make test-fast      - Run unit tests quickly (no coverage)"
	@echo "  make test-all       - Run all test suites"
	@echo "  make test-ci        - Run comprehensive CI test suite"
	@echo ""
	@echo -e "$(GREEN)Test Suites:$(RESET)"
	@echo "  make test-unit      - Run unit tests"
	@echo "  make test-integration - Run integration tests"
	@echo "  make test-samples   - Run sample tests"
	@echo ""
	@echo -e "$(GREEN)Quality Checks:$(RESET)"
	@echo "  make lint           - Run code linting"
	@echo "  make format         - Format code"
	@echo "  make type-check     - Run type checking"
	@echo "  make security-check - Run security analysis"
	@echo "  make quality-check  - Run all quality checks"
	@echo ""
	@echo -e "$(GREEN)Coverage:$(RESET)"
	@echo "  make coverage       - Generate coverage report"
	@echo "  make coverage-html  - Generate HTML coverage report"
	@echo ""
	@echo -e "$(GREEN)Advanced:$(RESET)"
	@echo "  make test-parallel  - Run tests in parallel"
	@echo "  make test-watch     - Watch for changes and run tests"
	@echo "  make test-debug     - Run tests with debugging"
	@echo "  make benchmark      - Run performance benchmarks"
	@echo ""
	@echo -e "$(GREEN)Cleanup:$(RESET)"
	@echo "  make clean-test     - Clean all test artifacts"
	@echo "  make clean-test-cache - Clean test caches"
	@echo ""
	@echo -e "$(YELLOW)Examples:$(RESET)"
	@echo "  make test-specific TEST=tests/unit/test_kernel.py"
	@echo "  make test TEST_ARGS='-k test_specific_function'"
