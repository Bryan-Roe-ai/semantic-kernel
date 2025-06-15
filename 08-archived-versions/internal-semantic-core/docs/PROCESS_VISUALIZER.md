# Process Visualizer Plugin

The Process Visualizer plugin for VS Code helps you visualize and track processes happening behind the scenes in your development environment. This guide will explain how to install, configure, and use the plugin.

## Installation

1. Clone the repository to your local machine.
2. Navigate to the `semantic-kernel/.vscode-plugins/process-visualizer` directory.
3. Run `npm install` to install the necessary dependencies.
4. Run `npm run build` to compile the plugin.

## Configuration

To configure the Process Visualizer plugin, add the following settings to your `.vscode/settings.json` file:

```json
{
  "processTracking.enable": true,
  "processTracking.behavior": {
    "showInStatusBar": true,
    "logToOutputWindow": true
  },
  "aiAutoRun.enable": true
}
```

## Usage

### Enabling the Plugin

To enable the Process Visualizer plugin, ensure that the `processTracking.enable` setting is set to `true` in your `.vscode/settings.json` file.

### Running the Process Tracking Task

To run the process tracking task, add the following task to your `.vscode/tasks.json` file:

```json
{
  "label": "show-processes",
  "type": "shell",
  "command": "echo",
  "args": ["Showing processes..."],
  "group": "build",
  "problemMatcher": [],
  "runOptions": {
    "runOn": "fileSave"
  }
}
```

### Running the AI Auto-Run Task

To run the AI auto-run task, add the following task to your `.vscode/tasks.json` file:

```json
{
  "label": "ai-auto-run",
  "type": "shell",
  "command": "python",
  "args": ["path/to/your/ai_script.py"],
  "group": "build",
  "problemMatcher": [],
  "runOptions": {
    "runOn": "folderOpen"
  }
}
```

### Viewing Processes

Once the plugin is enabled and the task is configured, you can view the processes by running the `show-processes` task. The processes will be displayed in the VS Code output window.

## Screenshots

Here are some screenshots of the Process Visualizer plugin in action:

![Process Visualizer](images/process-visualizer.png)

## Additional Configuration

You can further customize the behavior of the Process Visualizer plugin by modifying the `processTracking.behavior` settings in your `.vscode/settings.json` file. For example, you can choose to only show processes in the status bar or only log them to the output window.

## Troubleshooting

If you encounter any issues with the Process Visualizer plugin, try the following steps:

1. Ensure that the plugin is installed and compiled correctly.
2. Check that the necessary settings are added to your `.vscode/settings.json` file.
3. Verify that the task is configured correctly in your `.vscode/tasks.json` file.
4. Restart VS Code to apply the changes.

If the issue persists, please open an issue on the repository's GitHub page.

## Contributing

We welcome contributions to the Process Visualizer plugin. If you would like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them to your branch.
4. Open a pull request with a description of your changes.

Thank you for contributing!

## License

The Process Visualizer plugin is licensed under the MIT License. See the `LICENSE` file for more information.
