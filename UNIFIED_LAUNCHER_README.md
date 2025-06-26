---
runme:
  id: 01JYN4Q5G6VEAM9DA68KPBGWM7
  version: v3
---

#

**Made with ❤️ for the Semantic Kernel community**

---

The launcher will automatically discover and categorize new scripts!

5. Test with the unified launcher
6. Add to appropriate directory structure
7. Use descriptive file names
8. Add main function with `if __name__ == "__main__"` guard
9. Include proper docstrings

When adding new scripts to the workspace:

## Contributing

```sh {"id":"01JYN4Q62K3E0V5YXMECDCNP40"}
./launch --category tests
# In another terminal, run tests

./launch --script friendly_dashboard.py
# Start development session
```bash

```

./launch --setup

# Full setup for new environment

./launch --fix && ./launch --category automation

# Daily maintenance

```bash {"id":"01JYN4Q62K3E0V5YXMECQ1GFXA"}

```

./launch --category tests

# Run all tests

./launch --category servers

# List all servers

./launch --category ai_agents

# Show all AI agents

```bash {"id":"01JYN4Q62K3E0V5YXMEG4AS08T"}

## Examples

- Command line: Use as default project runner
- PyCharm: Add as an external tool
- VS Code: Add as a task in `.vscode/tasks.json`
The launcher can be integrated with IDEs:

- `LOG_LEVEL`: Set logging verbosity
- `WORKSPACE_ROOT`: Override workspace location
- `PYTHON_PATH`: Override Python interpreter
The launcher respects these environment variables:

- Organizing files in appropriate directories
- Adding clear docstrings
- Using descriptive file names
Scripts are automatically categorized, but you can influence categorization by:

## Advanced Usage

4. Use `--list` to see all available scripts
3. Check the logs directory for detailed error information
2. Run with `--help` for command line options
1. Use the interactive menu for guided access


- Run as administrator on Windows if needed
- Run `chmod +x launch` on Linux/macOS
**Permission errors**

- Check that scripts have proper main functions
- Run "Refresh script list" from the interactive menu
**Scripts not showing up**

- Ensure Python is in your PATH
- Install Python 3.8 or higher
**"Python not found"**

- Check file permissions
- Ensure `unified_launcher.py` exists in the workspace root
**"Unified launcher not found"**


## Troubleshooting

- Consistent development environment
- Reduced setup time for new developers
- Faster startup and execution

- Detailed descriptions for each script
- Easy discovery of available functionality
- Clear categorization of all scripts

- Handles environment setup automatically
- Keeps code clean and consistent
- Fixes issues before they cause problems

- Consistent interface across the entire workspace
- No need to remember individual script locations
- Single entry point for all functionality

## Benefits

- Basic syntax problems
- Trailing whitespace and formatting issues
- Missing main guards (`if __name__ == "__main__"`)
- Missing imports (Path, typing, common modules)
- Duplicate or incorrect shebang lines
Common issues that get fixed automatically:

- Suggests installation commands
- Tracks dependencies between scripts
- Identifies missing packages
- Analyzes import statements
For each script, the launcher:

- Directory structure
- Content analysis
- File names
- File path patterns
Scripts are automatically categorized based on:

- Any files with main functions or runnable entry points
- Shell scripts (*.sh)
- Python scripts (*.py)
The launcher automatically scans the workspace for:

## How It Works

```

└── [all other workspace files]
├── venv/ # Virtual environment (auto-created)
├── logs/ # Launcher logs
├── launch.bat # Windows batch script
├── launch # Linux/macOS shell script
├── run_new.py # Simple Python runner
├── unified_launcher.py # Main unified launcher
workspace/

```md {"id":"01JYN4Q62K3E0V5YXMEH1J6668"}

## File Structure

- **Refresh script list**: Re-scan workspace for new scripts
- **Stop all processes**: Gracefully stop all background processes
- **Show running processes**: Display currently running scripts
- **Create virtual environment**: Sets up isolated Python environment
- **Install dependencies**: Installs packages from all requirements files
- **Fix all files**: Automatically fixes common issues in Python files

```

./launch --help

# Get help

./launch --category ai_agents

# Show scripts in category

./launch --script demo_showcase.py

# Run specific script

./launch --list

# List all available scripts

./launch --install

# Install dependencies only

./launch --setup

# Setup complete environment

./launch --fix

# Fix all files in the workspace

```bash {"id":"01JYN4Q62K3E0V5YXMEHN3H4SR"}

Shows a menu with all available scripts organized by category.
```

./launch

```bash {"id":"01JYN4Q62K3E0V5YXMEMPFZT47"}

## Commands

- **Core**: Core Semantic Kernel implementations
- **Automation**: Automated workflows and scripts
- **Tests**: Test runners and validation scripts
- **Setup**: Installation and configuration scripts
- **Tools**: Utilities and helper scripts
- **Monitoring**: Dashboards, status checkers, and monitors
- **AI Agents**: Intelligent agents and cognitive systems
- **Demos**: Example applications and demonstrations
- **Servers**: API servers, backends, and services
- **Launchers**: Main entry points and startup scripts

- Shows which scripts are ready to run
- Provides descriptions for each script
- Categorizes scripts by functionality
- Finds all runnable scripts automatically

- Handles missing dependencies gracefully
- Creates virtual environments when needed
- Installs common packages automatically
- Scans all requirements files

- Adds missing main guards
- Removes trailing whitespace
- Fixes common syntax issues
- Adds missing imports automatically
- Removes duplicate shebang lines

## Features

```

python3 run_new.py

# Or use the simple runner

python3 unified_launcher.py

# Interactive mode

```bash {"id":"01JYN4Q62K3E0V5YXMENGJHJN4"}

```

launch.bat

# Double-click or run from command prompt

```cmd {"id":"01JYN4Q62K3E0V5YXMEQJ4QJE1"}

```

./launch
chmod +x launch

# Make executable and run

```bash {"id":"01JYN4Q62K3E0V5YXMESVVJYGP"}

## Quick Start

The Unified Launcher is a comprehensive solution that fixes all files in the workspace and provides a centralized way to run everything from one place. It automatically handles dependencies, fixes common issues, and presents an organized interface to all functionality.

## Overview
 🚀 Semantic Kernel Unified Launcher
```