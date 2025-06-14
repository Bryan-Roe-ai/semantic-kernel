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
<<<<<<< Updated upstream
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
