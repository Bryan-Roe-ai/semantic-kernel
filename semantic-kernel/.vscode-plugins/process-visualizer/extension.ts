import * as vscode from 'vscode';
import { exec } from 'child_process';

function trackAndDisplayProcesses() {
    const command = 'ps aux'; // Command to list processes (Unix-based systems)
    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing command: ${error.message}`);
            return;
        }
        if (stderr) {
            console.error(`Error: ${stderr}`);
            return;
        }
        vscode.window.showInformationMessage(`Processes:\n${stdout}`);
    });
}

export function activate(context: vscode.ExtensionContext) {
    context.subscriptions.push(
        vscode.commands.registerCommand('extension.trackProcesses', trackAndDisplayProcesses)
    );
}
