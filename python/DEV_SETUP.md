# Dev Setup

This document describes how to setup your environment with Python and uv,
if you're working on new features or a bug fix for Semantic Kernel, or simply
want to run the tests included.

## System setup
<<<<<<< div
=======
<<<<<<< main
>>>>>>> main
## LLM setup

Make sure you have an
[OpenAI API Key](https://platform.openai.com) or
[Azure OpenAI service key](https://learn.microsoft.com/azure/cognitive-services/openai/quickstart?pivots=rest-api)

There are two methods to manage keys, secrets, and endpoints:

1. Store them in environment variables. SK Python leverages pydantic settings to load keys, secrets, and endpoints. This means that there is a first attempt to load them from environment variables. The `.env` file naming applies to how the names should be stored as environment variables.
2. If you'd like to use the `.env` file, you will need to configure the `.env` file with the following keys into a `.env` file (see the `.env.example` file):

```sh {"id":"01J6KNPX0HTGAZ4YDQ34296TT7"}
OPENAI_API_KEY=""
OPENAI_ORG_ID=""
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=""
AZURE_OPENAI_TEXT_DEPLOYMENT_NAME=""
AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME=""
AZURE_OPENAI_ENDPOINT=""
AZURE_OPENAI_API_KEY=""
```
# System setup

To get started, you'll need VSCode and a local installation of Python 3.x.

You can run:

    python3 --version ; pip3 --version ; code -v

to verify that you have the required dependencies.

## If you're on WSL

Check that you've cloned the repository to `~/workspace` or a similar folder.
Avoid `/mnt/c/` and prefer using your WSL user's home directory.
```python {"id":"01J6KNPX0HTGAZ4YDQ353PQS4G"}
chat_completion = OpenAIChatCompletion(service_id="test", env_file_path=<path_to_file>)
```
<<<<<<< div
=======
=======
>>>>>>> main

## If you're on WSL

Check that you've cloned the repository to `~/workspace` or a similar folder.
Avoid `/mnt/c/` and prefer using your WSL user's home directory.
<<<<<<< div
=======
>>>>>>> ms/features/bugbash-prep
>>>>>>> main

Ensure you have the WSL extension for VSCode installed.

## Using uv

uv allows us to use SK from the local files, without worrying about paths, as
if you had SK pip package installed.

To install SK and all the required tools in your system, first, navigate to the directory containing
this DEV_SETUP using your chosen shell.
<<<<<<< div

### For windows (non-WSL)

Check the [uv documentation](https://docs.astral.sh/uv/getting-started/installation/) for the installation instructions. At the time of writing this is the command to install uv:

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```python {"id":"01J6KNPX0HTGAZ4YDQ3625T9E4"}
    python3 --version ; pip3 --version ; code -v
```

You can then run the following commands manually:

```powershell
# Install Python 3.10, 3.11, and 3.12
uv python install 3.10 3.11 3.12
# Create a virtual environment with Python 3.10 (you can change this to 3.11 or 3.12)
$PYTHON_VERSION = "3.10"
uv venv --python $PYTHON_VERSION
# Install SK and all dependencies
uv sync --all-extras --dev
# Install pre-commit hooks
uv run pre-commit install -c python/.pre-commit-config.yaml
```

Or you can then either install [`make`](https://gnuwin32.sourceforge.net/packages/make.htm) and then follow the guide for Mac and Linux, or run the following commands, the commands are shown as bash but should work in powershell as well.

### For Mac and Linux (both native and WSL)

It is super simple to get started, run the following commands:

```bash
make install
```

This will install uv, python, Semantic Kernel and all dependencies and the pre-commit config. It uses python 3.10 by default, if you want to change that set the `PYTHON_VERSION` environment variable to the desired version (currently supported are 3.10, 3.11, 3.12). For instance for 3.12"
    
```bash
make install PYTHON_VERSION=3.12
```
```bash {"id":"01J6KNPX0HTGAZ4YDQ366SG3QM"}
sudo apt-get update && sudo apt-get install python3 python3-pip
```

ℹ️ __Note__: if you don't have your PATH setup to find executables installed by `pip3`,
=======
>>>>>>> main

### For windows (non-WSL)

Check the [uv documentation](https://docs.astral.sh/uv/getting-started/installation/) for the installation instructions. At the time of writing this is the command to install uv:

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
<<<<<<< main
```python {"id":"01J6KNPX0HTGAZ4YDQ3625T9E4"}
    python3 --version ; pip3 --version ; code -v
=======
>>>>>>> ms/features/bugbash-prep
```

You can then run the following commands manually:

```powershell
# Install Python 3.10, 3.11, and 3.12
uv python install 3.10 3.11 3.12
# Create a virtual environment with Python 3.10 (you can change this to 3.11 or 3.12)
$PYTHON_VERSION = "3.10"
uv venv --python $PYTHON_VERSION
# Install SK and all dependencies
uv sync --all-extras --dev
# Install pre-commit hooks
uv run pre-commit install -c python/.pre-commit-config.yaml
```

Or you can then either install [`make`](https://gnuwin32.sourceforge.net/packages/make.htm) and then follow the guide for Mac and Linux, or run the following commands, the commands are shown as bash but should work in powershell as well.

### For Mac and Linux (both native and WSL)
<<<<<<< main

It is super simple to get started, run the following commands:

```bash
make install
```

This will install uv, python, Semantic Kernel and all dependencies and the pre-commit config. It uses python 3.10 by default, if you want to change that set the `PYTHON_VERSION` environment variable to the desired version (currently supported are 3.10, 3.11, 3.12). For instance for 3.12"
    
```bash
make install PYTHON_VERSION=3.12
```
```bash {"id":"01J6KNPX0HTGAZ4YDQ366SG3QM"}
sudo apt-get update && sudo apt-get install python3 python3-pip
```

ℹ️ __Note__: if you don't have your PATH setup to find executables installed by `pip3`,
=======
>>>>>>> ms/features/bugbash-prep

It is super simple to get started, run the following commands:

```bash
make install
```

<<<<<<< div

### For windows (non-WSL)

Check the [uv documentation](https://docs.astral.sh/uv/getting-started/installation/) for the installation instructions. At the time of writing this is the command to install uv:

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```python {"id":"01J6KNPX0HTGAZ4YDQ3625T9E4"}
    python3 --version ; pip3 --version ; code -v
```

You can then run the following commands manually:

```powershell
# Install Python 3.10, 3.11, and 3.12
uv python install 3.10 3.11 3.12
# Create a virtual environment with Python 3.10 (you can change this to 3.11 or 3.12)
$PYTHON_VERSION = "3.10"
uv venv --python $PYTHON_VERSION
# Install SK and all dependencies
uv sync --all-extras --dev
# Install pre-commit hooks
uv run pre-commit install -c python/.pre-commit-config.yaml
```

Or you can then either install [`make`](https://gnuwin32.sourceforge.net/packages/make.htm) and then follow the guide for Mac and Linux, or run the following commands, the commands are shown as bash but should work in powershell as well.

### For Mac and Linux (both native and WSL)

It is super simple to get started, run the following commands:

```bash
make install
```

=======
>>>>>>> main
This will install uv, python, Semantic Kernel and all dependencies and the pre-commit config. It uses python 3.10 by default, if you want to change that set the `PYTHON_VERSION` environment variable to the desired version (currently supported are 3.10, 3.11, 3.12). For instance for 3.12"
    
```bash
make install PYTHON_VERSION=3.12
```
<<<<<<< div
```bash {"id":"01J6KNPX0HTGAZ4YDQ366SG3QM"}
sudo apt-get update && sudo apt-get install python3 python3-pip
```

ℹ️ __Note__: if you don't have your PATH setup to find executables installed by `pip3`,

It is super simple to get started, run the following commands:

```bash
make install
```

To install Poetry in your system, first, navigate to the directory containing
this README using your chosen shell. You will need to have Python 3.10, 3.11, or 3.12
installed.

If you want to change python version (without installing uv, python and pre-commit), you can use the same parameter, but do:
This will install uv, python, Semantic Kernel and all dependencies and the pre-commit config. It uses python 3.10 by default, if you want to change that set the `PYTHON_VERSION` environment variable to the desired version (currently supported are 3.10, 3.11, 3.12). For instance for 3.12"
    
```bash
make install PYTHON_VERSION=3.12
```

If you want to change python version (without installing uv, python and pre-commit), you can use the same parameter, but do:
=======

If you want to change python version (without installing uv, python and pre-commit), you can use the same parameter, but do:
<<<<<<< main
>>>>>>> main

```bash
make install-sk PYTHON_VERSION=3.12
```
<<<<<<< div

ℹ️ **Note**: Running the install or install-sk command will wipe away your existing virtual environment and create a new one.

Alternatively you can run the VSCode task `Python: Install` to run the same command.
It is best to install Poetry using their
[official installer](https://python-poetry.org/docs/#installing-with-the-official-installer).

On MacOS, you might find that `python` commands are not recognized by default,
and you can only use `python3`. To make it easier to run `python ...` commands
(which Poetry requires), you can create an alias in your shell configuration file.

## VSCode Setup

Open the workspace in [VSCode](https://code.visualstudio.com/docs/editor/workspaces).
> The workspace for python should be rooted in the `./python` folder.

Open any of the `.py` files in the project and run the `Python: Select Interpreter`
command from the command palette. Make sure the virtual env (default path is `.venv`) created by
`uv` is selected.

If prompted, install `ruff`. (It should have been installed as part of `uv sync --dev`).

You also need to install the `ruff` extension in VSCode so that auto-formatting uses the `ruff` formatter on save.
Read more about the extension [here](https://github.com/astral-sh/ruff-vscode).

## LLM setup
1. **Open your shell configuration file**:

   - For __Bash__: `nano ~/.bash_profile` or `nano ~/.bashrc`
   - For **Zsh** (default on macOS Catalina and later): `nano ~/.zshrc`

2. **Add the alias**:

```sh {"id":"01J6KNPX0HTGAZ4YDQ37NQ12T9"}
alias python='python3'
```

3. **Save the file and exit**:

   - In `nano`, press `CTRL + X`, then `Y`, and hit `Enter`.

4. **Apply the changes**:

   - For __Bash__: `source ~/.bash_profile` or `source ~/.bashrc`
   - For **Zsh**: `source ~/.zshrc`

After these steps, you should be able to use `python` in your terminal to run
Python 3 commands.

Make sure you have an
[OpenAI API Key](https://platform.openai.com) or
[Azure OpenAI service key](https://learn.microsoft.com/azure/cognitive-services/openai/quickstart?pivots=rest-api)

There are two methods to manage keys, secrets, and endpoints:
```bash {"id":"01J6KNPX0HTGAZ4YDQ3BB96MAY"}
# Install poetry package if not choosing to install via their official installer
pip3 install poetry

1. Store them in environment variables. SK Python leverages pydantic settings to load keys, secrets, and endpoints from the environment. 
    > When you are using VSCode and have the python extension setup, it automatically loads environment variables from a `.env` file, so you don't have to manually set them in the terminal.
    > During runtime on different platforms, environment settings set as part of the deployments should be used.

2. Store them in a separate `.env` file, like `dev.env`, you can then pass that name into the constructor for most services, to the `env_file_path` parameter, see below.
    > Do not store `*.env` files in your repository, and make sure to add them to your `.gitignore` file.

There are a lot of settings, for a more extensive list of settings, see [ALL_SETTINGS.md](./samples/concepts/setup/ALL_SETTINGS.md).

### Example for file-based setup with OpenAI Chat Completions
To configure a `.env` file with just the keys needed for OpenAI Chat Completions, you can create a `openai.env` (this name is just as an example, a single `.env` with all required keys is more common) file in the root of the `python` folder with the following content:

Content of `openai.env`:
```env
OPENAI_API_KEY=""
OPENAI_CHAT_MODEL_ID="gpt-4o-mini"
```

You will then configure the ChatCompletion class with the keyword argument `env_file_path`:
## VSCode Setup

Open the [workspace](https://code.visualstudio.com/docs/editor/workspaces) in VSCode.

> The Python workspace is the `./python` folder if you are at the root of the repository.

ℹ️ **Note**: Running the install or install-sk command will wipe away your existing virtual environment and create a new one.

Alternatively you can run the VSCode task `Python: Install` to run the same command.
It is best to install Poetry using their
[official installer](https://python-poetry.org/docs/#installing-with-the-official-installer).

On MacOS, you might find that `python` commands are not recognized by default,
and you can only use `python3`. To make it easier to run `python ...` commands
(which Poetry requires), you can create an alias in your shell configuration file.

## VSCode Setup

Open the workspace in [VSCode](https://code.visualstudio.com/docs/editor/workspaces).
> The workspace for python should be rooted in the `./python` folder.

Open any of the `.py` files in the project and run the `Python: Select Interpreter`
command from the command palette. Make sure the virtual env (default path is `.venv`) created by
`uv` is selected.

If prompted, install `ruff`. (It should have been installed as part of `uv sync --dev`).

You also need to install the `ruff` extension in VSCode so that auto-formatting uses the `ruff` formatter on save.
Read more about the extension [here](https://github.com/astral-sh/ruff-vscode).

## LLM setup
1. **Open your shell configuration file**:

   - For __Bash__: `nano ~/.bash_profile` or `nano ~/.bashrc`
   - For **Zsh** (default on macOS Catalina and later): `nano ~/.zshrc`

2. **Add the alias**:

=======

ℹ️ **Note**: Running the install or install-sk command will wipe away your existing virtual environment and create a new one.

Alternatively you can run the VSCode task `Python: Install` to run the same command.
It is best to install Poetry using their
[official installer](https://python-poetry.org/docs/#installing-with-the-official-installer).

On MacOS, you might find that `python` commands are not recognized by default,
and you can only use `python3`. To make it easier to run `python ...` commands
(which Poetry requires), you can create an alias in your shell configuration file.

## VSCode Setup

Open the workspace in [VSCode](https://code.visualstudio.com/docs/editor/workspaces).
> The workspace for python should be rooted in the `./python` folder.

Open any of the `.py` files in the project and run the `Python: Select Interpreter`
command from the command palette. Make sure the virtual env (default path is `.venv`) created by
`uv` is selected.

If prompted, install `ruff`. (It should have been installed as part of `uv sync --dev`).

You also need to install the `ruff` extension in VSCode so that auto-formatting uses the `ruff` formatter on save.
Read more about the extension [here](https://github.com/astral-sh/ruff-vscode).

## LLM setup
1. **Open your shell configuration file**:

   - For __Bash__: `nano ~/.bash_profile` or `nano ~/.bashrc`
   - For **Zsh** (default on macOS Catalina and later): `nano ~/.zshrc`

2. **Add the alias**:

>>>>>>> main
```sh {"id":"01J6KNPX0HTGAZ4YDQ37NQ12T9"}
alias python='python3'
```

3. **Save the file and exit**:

   - In `nano`, press `CTRL + X`, then `Y`, and hit `Enter`.

4. **Apply the changes**:

   - For __Bash__: `source ~/.bash_profile` or `source ~/.bashrc`
   - For **Zsh**: `source ~/.zshrc`

After these steps, you should be able to use `python` in your terminal to run
Python 3 commands.
<<<<<<< div
=======
=======
>>>>>>> main

```bash
make install-sk PYTHON_VERSION=3.12
```

ℹ️ **Note**: Running the install or install-sk command will wipe away your existing virtual environment and create a new one.

Alternatively you can run the VSCode task `Python: Install` to run the same command.

## VSCode Setup

Open the workspace in [VSCode](https://code.visualstudio.com/docs/editor/workspaces).
> The workspace for python should be rooted in the `./python` folder.

Open any of the `.py` files in the project and run the `Python: Select Interpreter`
command from the command palette. Make sure the virtual env (default path is `.venv`) created by
`uv` is selected.

If prompted, install `ruff`. (It should have been installed as part of `uv sync --dev`).

You also need to install the `ruff` extension in VSCode so that auto-formatting uses the `ruff` formatter on save.
Read more about the extension [here](https://github.com/astral-sh/ruff-vscode).

## LLM setup
<<<<<<< div
=======
>>>>>>> ms/features/bugbash-prep
>>>>>>> main

Make sure you have an
[OpenAI API Key](https://platform.openai.com) or
[Azure OpenAI service key](https://learn.microsoft.com/azure/cognitive-services/openai/quickstart?pivots=rest-api)

There are two methods to manage keys, secrets, and endpoints:
<<<<<<< div
```bash {"id":"01J6KNPX0HTGAZ4YDQ3BB96MAY"}
# Install poetry package if not choosing to install via their official installer
pip3 install poetry
```bash {"id":"01J6KNPX0HTGAZ4YDQ3BB96MAY"}
# Install poetry package if not choosing to install via their official installer
pip3 install poetry
=======
<<<<<<< main
```bash {"id":"01J6KNPX0HTGAZ4YDQ3BB96MAY"}
# Install poetry package if not choosing to install via their official installer
pip3 install poetry
=======
>>>>>>> ms/features/bugbash-prep
>>>>>>> main

1. Store them in environment variables. SK Python leverages pydantic settings to load keys, secrets, and endpoints from the environment. 
    > When you are using VSCode and have the python extension setup, it automatically loads environment variables from a `.env` file, so you don't have to manually set them in the terminal.
    > During runtime on different platforms, environment settings set as part of the deployments should be used.

2. Store them in a separate `.env` file, like `dev.env`, you can then pass that name into the constructor for most services, to the `env_file_path` parameter, see below.
    > Do not store `*.env` files in your repository, and make sure to add them to your `.gitignore` file.

There are a lot of settings, for a more extensive list of settings, see [ALL_SETTINGS.md](./samples/concepts/setup/ALL_SETTINGS.md).

### Example for file-based setup with OpenAI Chat Completions
To configure a `.env` file with just the keys needed for OpenAI Chat Completions, you can create a `openai.env` (this name is just as an example, a single `.env` with all required keys is more common) file in the root of the `python` folder with the following content:

Content of `openai.env`:
```env
OPENAI_API_KEY=""
OPENAI_CHAT_MODEL_ID="gpt-4o-mini"
```

You will then configure the ChatCompletion class with the keyword argument `env_file_path`:
<<<<<<< div
=======
<<<<<<< main
>>>>>>> main
## VSCode Setup

Open the [workspace](https://code.visualstudio.com/docs/editor/workspaces) in VSCode.

> The Python workspace is the `./python` folder if you are at the root of the repository.

<<<<<<< div

=======
=======

>>>>>>> ms/features/bugbash-prep
>>>>>>> main
```python
chat_completion = OpenAIChatCompletion(service_id="test", env_file_path="openai.env")
```

## Tests

You can run the unit tests under the [tests/unit](tests/unit/) folder.

```bash
    uv run pytest tests/unit
<<<<<<< div
```bash {"id":"01J6KNPX0HTGAZ4YDQ3CVYSJC6"}
    poetry install --with unit-tests
    poetry run pytest tests/unit
=======
<<<<<<< main
>>>>>>> main
```bash {"id":"01J6KNPX0HTGAZ4YDQ3CVYSJC6"}
    poetry install --with unit-tests
    poetry run pytest tests/unit
=======
>>>>>>> ms/features/bugbash-prep
```

Alternatively, you can run them using VSCode Tasks. Open the command palette
(`Ctrl+Shift+P`) and type `Tasks: Run Task`. Select `Python: Tests - Unit` or `Python: Tests - Code Coverage` from the list.

You can run the integration tests under the [tests/integration](tests/integration/) folder.

```bash
    uv run pytest tests/integration
<<<<<<< div
```bash {"id":"01J6KNPX0HTGAZ4YDQ3ETP16N9"}
    poetry install --with tests
    poetry run pytest tests/integration
=======
<<<<<<< main
>>>>>>> main
```bash {"id":"01J6KNPX0HTGAZ4YDQ3ETP16N9"}
    poetry install --with tests
    poetry run pytest tests/integration
=======
>>>>>>> ms/features/bugbash-prep
```

You can also run all the tests together under the [tests](tests/) folder.

```bash
    uv run pytest tests
<<<<<<< div
```bash {"id":"01J6KNPX0HTGAZ4YDQ3GYN6VJR"}
    poetry install
    poetry run pytest tests
=======
<<<<<<< main
>>>>>>> main
```bash {"id":"01J6KNPX0HTGAZ4YDQ3GYN6VJR"}
    poetry install
    poetry run pytest tests
=======
>>>>>>> ms/features/bugbash-prep
```

Alternatively, you can run them using VSCode Tasks. Open the command palette
(`Ctrl+Shift+P`) and type `Tasks: Run Task`. Select `Python: Tests - All` from the list.


## Implementation Decisions

### Asynchronous programming

It's important to note that most of this library is written with asynchronous in mind. The
developer should always assume everything is asynchronous. One can use the function signature
with either `async def` or `def` to understand if something is asynchronous or not.

### Documentation

Each file should have a single first line containing: # Copyright (c) Microsoft. All rights reserved.

We follow the [Google Docstring](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#383-functions-and-methods) style guide for functions and methods.
They are currently not checked for private functions (functions starting with '_').

They should contain:

- Single line explaining what the function does, ending with a period.
- If necessary to further explain the logic a newline follows the first line and then the explanation is given.
- The following three sections are optional, and if used should be separated by a single empty line.
- Arguments are then specified after a header called `Args:`, with each argument being specified in the following format:
    - `arg_name`: Explanation of the argument.
    - if a longer explanation is needed for a argument, it should be placed on the next line, indented by 4 spaces.
    - Type and default values do not have to be specified, they will be pulled from the definition.
<<<<<<< div
=======
<<<<<<< main
>>>>>>> main
   - `arg_name` (`arg_type`): Explanation of the argument, arg_type is optional, as long as you are consistent.
   - if a longer explanation is needed for a argument, it should be placed on the next line, indented by 4 spaces.
   - Default values do not have to be specified, they will be pulled from the definition.

<<<<<<< div
=======
=======
>>>>>>> ms/features/bugbash-prep
>>>>>>> main
- Returns are specified after a header called `Returns:` or `Yields:`, with the return type and explanation of the return value.
- Finally, a header for exceptions can be added, called `Raises:`, with each exception being specified in the following format:
   - `ExceptionType`: Explanation of the exception.
   - if a longer explanation is needed for a exception, it should be placed on the next line, indented by 4 spaces.

Putting them all together, gives you at minimum this:

```python {"id":"01J6KNPX0HTGAZ4YDQ3GZ160F4"}
def equal(arg1: str, arg2: str) -> bool:
    """Compares two strings and returns True if they are the same."""
    ...
```
<<<<<<< div

Or a complete version of this:

```python {"id":"01J6KNPX0HTGAZ4YDQ3JGT3D67"}
def equal(arg1: str, arg2: str) -> bool:
    """Compares two strings and returns True if they are the same.

```python {"id":"01J6KNPX0HTGAZ4YDQ3JGT3D67"}
def equal(arg1: str, arg2: str) -> bool:
    """Compares two strings and returns True if they are the same.

    Here is extra explanation of the logic involved.

    Args:
        arg1: The first string to compare.
        arg2: The second string to compare.
            This string requires extra explanation.

    Returns:
        True if the strings are the same, False otherwise.

    Raises:
        ValueError: If one of the strings is empty.
    """
    ...
```

If in doubt, use the link above to read much more considerations of what to do and when, or use common sense.

## Pydantic and Serialization

This section describes how one can enable serialization for their class using Pydantic.
For more info you can refer to the [Pydantic Documentation](https://docs.pydantic.dev/latest/).

```bash
    uv run pytest tests
```bash {"id":"01J6KNPX0HTGAZ4YDQ3GYN6VJR"}
    poetry install
    poetry run pytest tests
```

Alternatively, you can run them using VSCode Tasks. Open the command palette
(`Ctrl+Shift+P`) and type `Tasks: Run Task`. Select `Python: Tests - All` from the list.


## Implementation Decisions

### Asynchronous programming

It's important to note that most of this library is written with asynchronous programming in mind. The
developer should always assume everything is asynchronous. One can use the function signature
with either `async def` or `def` to understand if something is asynchronous or not.

### Documentation

Each file should have a single first line containing: # Copyright (c) Microsoft. All rights reserved.

We follow the [Google Docstring](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#383-functions-and-methods) style guide for functions and methods.
They are currently not checked for private functions (functions starting with '_').

They should contain:

- Single line explaining what the function does, ending with a period.
- If necessary to further explain the logic a newline follows the first line and then the explanation is given.
- The following three sections are optional, and if used should be separated by a single empty line.
- Arguments are then specified after a header called `Args:`, with each argument being specified in the following format:
    - `arg_name`: Explanation of the argument.
    - if a longer explanation is needed for a argument, it should be placed on the next line, indented by 4 spaces.
    - Type and default values do not have to be specified, they will be pulled from the definition.
   - `arg_name` (`arg_type`): Explanation of the argument, arg_type is optional, as long as you are consistent.
   - if a longer explanation is needed for a argument, it should be placed on the next line, indented by 4 spaces.
   - Default values do not have to be specified, they will be pulled from the definition.

- Returns are specified after a header called `Returns:` or `Yields:`, with the return type and explanation of the return value.
- Finally, a header for exceptions can be added, called `Raises:`, with each exception being specified in the following format:
   - `ExceptionType`: Explanation of the exception.
   - if a longer explanation is needed for a exception, it should be placed on the next line, indented by 4 spaces.

Putting them all together, gives you at minimum this:

```python {"id":"01J6KNPX0HTGAZ4YDQ3GZ160F4"}
def equal(arg1: str, arg2: str) -> bool:
    """Compares two strings and returns True if they are the same."""
    ...
```

Or a complete version of this:

```python {"id":"01J6KNPX0HTGAZ4YDQ3JGT3D67"}
def equal(arg1: str, arg2: str) -> bool:
    """Compares two strings and returns True if they are the same.

    Here is extra explanation of the logic involved.

    Args:
        arg1: The first string to compare.
        arg2: The second string to compare.
            This string requires extra explanation.

    Returns:
        True if the strings are the same, False otherwise.

    Raises:
        ValueError: If one of the strings is empty.
    """
    ...
```

If in doubt, use the link above to read much more considerations of what to do and when, or use common sense.

## Pydantic and Serialization

=======

Or a complete version of this:

```python {"id":"01J6KNPX0HTGAZ4YDQ3JGT3D67"}
def equal(arg1: str, arg2: str) -> bool:
    """Compares two strings and returns True if they are the same.

    Here is extra explanation of the logic involved.

    Args:
        arg1: The first string to compare.
        arg2: The second string to compare.
            This string requires extra explanation.

    Returns:
        True if the strings are the same, False otherwise.

    Raises:
        ValueError: If one of the strings is empty.
    """
    ...
```

If in doubt, use the link above to read much more considerations of what to do and when, or use common sense.

## Pydantic and Serialization

>>>>>>> main
This section describes how one can enable serialization for their class using Pydantic.
For more info you can refer to the [Pydantic Documentation](https://docs.pydantic.dev/latest/).

### Upgrading existing classes to use Pydantic

Let's take the following example:

```python {"id":"01J6KNPX0HTGAZ4YDQ3JKQTX8W"}
class A:
    def __init__(self, a: int, b: float, c: List[float], d: dict[str, tuple[float, str]] = {}):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
```

You would convert this to a Pydantic class by sub-classing from the `KernelBaseModel` class.

```python {"id":"01J6KNPX0HTGAZ4YDQ3JZ43C10"}
from pydantic import Field
from semantic_kernel.kernel_pydantic import KernelBaseModel

class A(KernelBaseModel):
    # The notation for the fields is similar to dataclasses.
    a: int
    b: float
    c: list[float]
    # Only, instead of using dataclasses.field, you would use pydantic.Field
    d: dict[str, tuple[float, str]] = Field(default_factory=dict)
```

#### Classes with data that need to be serialized, and some of them are Generic types

Let's take the following example:

```python {"id":"01J6KNPX0HTGAZ4YDQ3PC4NBD0"}
from typing import TypeVar

T1 = TypeVar("T1")
T2 = TypeVar("T2", bound=<some class>)

class A:
    def __init__(a: int, b: T1, c: T2):
        self.a = a
        self.b = b
        self.c = c
```

You can use the `KernelBaseModel` to convert these to pydantic serializable classes.

```python
from typing import Generic, TypeVar
<<<<<<< div
=======
<<<<<<< main
>>>>>>> main
```python {"id":"01J6KNPX0HTGAZ4YDQ3R7VE7KV"}
from typing import Generic
=======
>>>>>>> ms/features/bugbash-prep

from semantic_kernel.kernel_pydantic import KernelBaseModel
<<<<<<< div
```python {"id":"01J6KNPX0HTGAZ4YDQ3R7VE7KV"}
from typing import Generic

from semantic_kernel.kernel_pydantic import KernelBaseModel

T1 = TypeVar("T1")
T2 = TypeVar("T2", bound=<some class>)

=======

>>>>>>> main
T1 = TypeVar("T1")
T2 = TypeVar("T2", bound=<some class>)

class A(KernelBaseModel, Generic[T1, T2]):
    # T1 and T2 must be specified in the Generic argument otherwise, pydantic will
    # NOT be able to serialize this class
    a: int
    b: T1
    c: T2
```

## Code quality checks

To run the same checks that run during a commit and the GitHub Action `Python Code Quality Checks`, you can use this command, from the [python](../python) folder:

```bash
    uv run pre-commit run -a
<<<<<<< div
```bash {"id":"01J6KNPX0HTGAZ4YDQ3RB8FHQJ"}
    poetry run pre-commit run -a
```bash {"id":"01J6KNPX0HTGAZ4YDQ3RB8FHQJ"}
    poetry run pre-commit run -a
```bash {"id":"01J6KNPX0HTGAZ4YDQ3RB8FHQJ"}
    poetry run pre-commit run -a
=======
<<<<<<< main
```bash {"id":"01J6KNPX0HTGAZ4YDQ3RB8FHQJ"}
    poetry run pre-commit run -a
=======
>>>>>>> ms/features/bugbash-prep
>>>>>>> main
```

or use the following task (using `Ctrl+Shift+P`):

- `Python - Run Checks` to run the checks on the whole project.
- `Python - Run Checks - Staged` to run the checks on the currently staged files only.

Ideally you should run these checks before committing any changes, when you install using the instructions above the pre-commit hooks should be installed already.

## Code Coverage

We try to maintain a high code coverage for the project. To run the code coverage on the unit tests, you can use the following command:

```bash
    uv run pytest --cov=semantic_kernel --cov-report=term-missing:skip-covered tests/unit/
<<<<<<< div
```bash {"id":"01J6KNPX0HTGAZ4YDQ3V7S5W7V"}
    poetry run pytest --cov=semantic_kernel --cov-report=term-missing:skip-covered tests/unit/
```bash {"id":"01J6KNPX0HTGAZ4YDQ3V7S5W7V"}
    poetry run pytest --cov=semantic_kernel --cov-report=term-missing:skip-covered tests/unit/
```bash {"id":"01J6KNPX0HTGAZ4YDQ3V7S5W7V"}
    poetry run pytest --cov=semantic_kernel --cov-report=term-missing:skip-covered tests/unit/
=======
<<<<<<< main
```bash {"id":"01J6KNPX0HTGAZ4YDQ3V7S5W7V"}
    poetry run pytest --cov=semantic_kernel --cov-report=term-missing:skip-covered tests/unit/
=======
>>>>>>> ms/features/bugbash-prep
>>>>>>> main
```

or use the following task (using `Ctrl+Shift+P`):

- `Python: Tests - Code Coverage` to run the code coverage on the whole project.

This will show you which files are not covered by the tests, including the specific lines not covered. Make sure to consider the untested lines from the code you are working on, but feel free to add other tests as well, that is always welcome!

## Catching up with the latest changes

There are many people committing to Semantic Kernel, so it is important to keep your local repository up to date. To do this, you can run the following commands:

```bash {"id":"01J6KNPX0J3RHKXXPZZ2645V13"}
    git fetch upstream main
    git rebase upstream/main
    git push --force-with-lease
```

or:

```bash {"id":"01J6KNPX0J3RHKXXPZZ3T5EN1R"}
    git fetch upstream main
    git merge upstream/main
    git push
<<<<<<< div
```

This is assuming the upstream branch refers to the main repository. If you have a different name for the upstream branch, you can replace `upstream` with the name of your upstream branch.

After running the rebase command, you may need to resolve any conflicts that arise. If you are unsure how to resolve a conflict, please refer to the [GitHub's documentation on resolving conflicts](https://docs.github.com/en/get-started/using-git/resolving-merge-conflicts-after-a-git-rebase), or for [VSCode](https://code.visualstudio.com/docs/sourcecontrol/overview#_merge-conflicts).
# LLM setup

Make sure you have an
[Open AI API Key](https://openai.com/api/) or
[Azure Open AI service key](https://learn.microsoft.com/azure/cognitive-services/openai/quickstart?pivots=rest-api)

ℹ️ **Note**: Azure OpenAI support is work in progress, and will be available soon.

Copy those keys into a `.env` file like this:

```
OPENAI_API_KEY=""
OPENAI_ORG_ID=""
AZURE_OPENAI_API_KEY=""
AZURE_OPENAI_ENDPOINT=""
```

=======
```

This is assuming the upstream branch refers to the main repository. If you have a different name for the upstream branch, you can replace `upstream` with the name of your upstream branch.

After running the rebase command, you may need to resolve any conflicts that arise. If you are unsure how to resolve a conflict, please refer to the [GitHub's documentation on resolving conflicts](https://docs.github.com/en/get-started/using-git/resolving-merge-conflicts-after-a-git-rebase), or for [VSCode](https://code.visualstudio.com/docs/sourcecontrol/overview#_merge-conflicts).
# LLM setup

Make sure you have an
[Open AI API Key](https://openai.com/api/) or
[Azure Open AI service key](https://learn.microsoft.com/azure/cognitive-services/openai/quickstart?pivots=rest-api)

ℹ️ **Note**: Azure OpenAI support is work in progress, and will be available soon.

Copy those keys into a `.env` file like this:

```
OPENAI_API_KEY=""
OPENAI_ORG_ID=""
AZURE_OPENAI_API_KEY=""
AZURE_OPENAI_ENDPOINT=""
```

>>>>>>> main
We suggest adding a copy of the `.env` file under these folders:

- [python/tests](tests)
- [samples/notebooks/python](../samples/notebooks/python).

# Quickstart with Poetry

Poetry allows to use SK from the current repo, without worrying about paths, as
if you had SK pip package installed. SK pip package will be published after
porting all the major features and ensuring cross-compatibility with C# SDK.

To install Poetry in your system:

    pip3 install poetry

The following command install the project dependencies:

    poetry install

And the following activates the project virtual environment, to make it easier
running samples in the repo and developing apps using Python SK.

    poetry shell

To run the same checks that are run during the Azure Pipelines build, you can run:

    poetry run pre-commit run -c .conf/.pre-commit-config.yaml -a

# VSCode Setup

Open any of the `.py` files in the project and run the `Python: Select Interpreter` command
from the command palette. Make sure the virtual env (venv) created by `poetry` is selected.
The python you're looking for should be under `~/.cache/pypoetry/virtualenvs/semantic-kernel-.../bin/python`.

If prompted, install `black` and `flake8` (if VSCode doesn't find those packages,
it will prompt you to install them).

# Tests

You should be able to run the example under the [tests](tests) folder.
