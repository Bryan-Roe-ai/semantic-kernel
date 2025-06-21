const vscode = require('vscode');

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
    console.log('AGI Chat Assistant is now active!');

    // Create the chat participant
    const agiParticipant = vscode.chat.createChatParticipant('agi', handleChatRequest);
    agiParticipant.iconPath = new vscode.ThemeIcon('robot');

    // Register commands
    const openChatCommand = vscode.commands.registerCommand('agiChat.openChat', () => {
        vscode.commands.executeCommand('workbench.panel.chat.view.copilot.focus');
        vscode.commands.executeCommand('workbench.action.chat.open', {
            query: '@agi Hello! I would like to chat with the AGI system.'
        });
    });

    // Create status bar item
    const statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBarItem.text = "$(robot) AGI Chat";
    statusBarItem.command = 'agiChat.openChat';
    statusBarItem.tooltip = 'Open AGI Chat (Ctrl+Shift+A)';
    statusBarItem.show();

    context.subscriptions.push(agiParticipant, openChatCommand, statusBarItem);

    // Show welcome message
    vscode.window.showInformationMessage(
        'AGI Chat Assistant activated! Use @agi in chat or press Ctrl+Shift+A',
        'Open Chat'
    ).then(selection => {
        if (selection === 'Open Chat') {
            vscode.commands.executeCommand('agiChat.openChat');
        }
    });
}

/**
 * Handle chat requests from the @agi participant
 * @param {vscode.ChatRequest} request
 * @param {vscode.ChatContext} context
 * @param {vscode.ChatResponseStream} stream
 * @param {vscode.CancellationToken} token
 */
async function handleChatRequest(request, context, stream, token) {
    try {
        // Get configuration
        const config = vscode.workspace.getConfiguration('agiChat');
        const endpoint = config.get('endpoint', 'http://localhost:8000');
        const defaultAgent = config.get('defaultAgent', 'neural-symbolic');

        // Parse command and agent from request
        let agentType = defaultAgent;
        let message = request.prompt;

        // Check for agent specification in the prompt
        const agentMatch = message.match(/^(neural-symbolic|reasoning|creative|analytical|general)\\s+(.+)$/i);
        if (agentMatch) {
            agentType = agentMatch[1].toLowerCase();
            message = agentMatch[2];
        }

        stream.progress(`🧠 Processing with ${agentType} agent...`);

        // Prepare the request
        const agiRequest = {
            message: message,
            agent_type: agentType,
            history: [],
            capabilities: []
        };

        // Make request to AGI backend
        const response = await fetch(`${endpoint}/agi/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(agiRequest)
        });

        if (!response.ok) {
            throw new Error(`AGI backend error: ${response.status} ${response.statusText}`);
        }

        const agiResponse = await response.json();

        // Stream the response
        stream.markdown(`**${agentType.charAt(0).toUpperCase() + agentType.slice(1)} AGI Agent**`);
        stream.markdown(`*Confidence: ${(agiResponse.confidence * 100).toFixed(1)}%*\\n\\n`);

        // Stream the main content
        stream.markdown(agiResponse.content);

        // Add reasoning if available
        if (agiResponse.reasoning) {
            stream.markdown(`\\n\\n---\\n**Reasoning Process:**\\n${agiResponse.reasoning}`);
        }

        return { metadata: { command: 'agi-chat', agent: agentType } };

    } catch (error) {
        const errorMessage = error.message || 'Unknown error occurred';

        stream.markdown(`❌ **Error connecting to AGI system:**\\n\\n\`${errorMessage}\`\\n\\n`);
        stream.markdown(`Please ensure the AGI backend is running. You can start it with:\\n`);
        stream.markdown(`\`\`\`bash\\ncd agi-backend-server\\npython3 main.py\\n\`\`\``);

        // Suggest using the web interface
        stream.markdown(`\\n💡 **Alternative:** You can also use the web interface by running:\\n`);
        stream.markdown(`\`\`\`bash\\n./launch_agi_chat.sh\\n\`\`\``);

        return { metadata: { command: 'agi-chat', error: errorMessage } };
    }
}

function deactivate() {
    console.log('AGI Chat Assistant deactivated');
}

module.exports = {
    activate,
    deactivate
};
