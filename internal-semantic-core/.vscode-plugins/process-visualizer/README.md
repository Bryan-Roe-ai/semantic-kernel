# Process Visualizer

The Process Visualizer is a VS Code plugin that shows processes happening behind the scenes. This plugin helps developers understand what processes are running and provides insights into the development environment.

## Features

* Visualize processes using VS Code's Webview API.
* Show processes in the status bar and output window.

## Installation

1. Clone the repository.
2. Navigate to the `semantic-kernel/.vscode-plugins/process-visualizer` directory.
3. Run `npm install` to install the dependencies.
4. Run `npm run build` to build the plugin.
5. Open the `semantic-kernel` directory in VS Code.
6. Press `F5` to start debugging the plugin.

## Configuration

Add the following settings to your `.vscode/settings.json` file to enable the Process Visualizer plugin:

```json
{
  "processTracking.enable": true,
  "processTracking.behavior": {
    "showInStatusBar": true,
    "logToOutputWindow": true
  }
}
```

## Usage

To use the Process Visualizer plugin, follow these steps:

1. Open a project in VS Code.
2. Press `Ctrl+Shift+P` to open the command palette.
3. Type `Track Processes` and select the command.
4. The processes will be displayed in the status bar and output window.

## Example

Here is an example of how the processes will be displayed:

```
Processes:
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.1 169260  1108 ?        Ss   10:00   0:00 /sbin/init
root         2  0.0  0.0      0     0 ?        S    10:00   0:00 [kthreadd]
root         3  0.0  0.0      0     0 ?        I<   10:00   0:00 [rcu_gp]
root         4  0.0  0.0      0     0 ?        I<   10:00   0:00 [rcu_par_gp]
```

## Contributing

If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
