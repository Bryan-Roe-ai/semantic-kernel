import * as vscode from "vscode";

interface AgentResponse {
    content: string;
    reasoning?: string;
    confidence: number;
}

export function activate(context: vscode.ExtensionContext) {
    console.log("AGI Chat Assistant is now active!");

    // Create AGI Chat participant (like GitHub Copilot)
    const agiChatParticipant = vscode.chat.createChatParticipant(
        "agi",
        (request, context, stream, token) =>
            handleChatRequest(request, context, stream, token)
    );

    agiChatParticipant.iconPath = vscode.Uri.joinPath(
        context.extensionUri,
        "media",
        "robot.svg"
    );

    // Register commands
    const openChatCommand = vscode.commands.registerCommand(
        "agiChat.openChat",
        () => {
            vscode.commands.executeCommand(
                "workbench.panel.chat.view.copilot.focus"
            );
            vscode.commands.executeCommand("workbench.action.chat.open", {
                query: "@agi Hello! I'd like to chat with the AGI system.",
            });
        }
    );

    const switchAgentCommand = vscode.commands.registerCommand(
        "agiChat.switchAgent",
        async () => {
            const agents = [
                "neural-symbolic",
                "reasoning",
                "creative",
                "analytical",
                "general",
            ];
            const selected = await vscode.window.showQuickPick(agents, {
                placeHolder: "Select an AGI agent type",
            });

            if (selected) {
                vscode.window.showInformationMessage(
                    `Switched to ${selected} agent`
                );
                // Store the selected agent in workspace state
                await context.workspaceState.update("selectedAgent", selected);
            }
        }
    );

    // Status bar item
    const statusBarItem = vscode.window.createStatusBarItem(
        vscode.StatusBarAlignment.Right,
        100
    );
    statusBarItem.text = "$(robot) AGI Chat";
    statusBarItem.command = "agiChat.openChat";
    statusBarItem.tooltip = "Open AGI Chat Assistant (Ctrl+Shift+A)";
    statusBarItem.show();

    context.subscriptions.push(
        agiChatParticipant,
        openChatCommand,
        switchAgentCommand,
        statusBarItem
    );

    // Show welcome message
    vscode.window
        .showInformationMessage(
            "AGI Chat Assistant activated! Use @agi in the chat or click the robot icon to start.",
            "Open Chat"
        )
        .then((selection) => {
            if (selection === "Open Chat") {
                vscode.commands.executeCommand("agiChat.openChat");
            }
        });
}

async function handleChatRequest(
    request: vscode.ChatRequest,
    context: vscode.ChatContext,
    stream: vscode.ChatResponseStream,
    token: vscode.CancellationToken
): Promise<vscode.ChatResult> {
    try {
        // Get the current selected agent
        const selectedAgent = await vscode.workspace
            .getConfiguration("agiChat")
            .get("defaultAgent", "neural-symbolic");
        const endpoint = await vscode.workspace
            .getConfiguration("agiChat")
            .get("semanticKernelEndpoint", "http://localhost:8000");

        stream.progress(`🧠 Processing with ${selectedAgent} agent...`);

        // Prepare request to AGI backend
        const agiRequest = {
            message: request.prompt,
            agent_type: selectedAgent,
            history: [], // Could be populated from context.history
            capabilities: [],
        };

        // Make request to AGI backend
        const response = await fetch(`${endpoint}/agi/chat`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(agiRequest),
        });

        if (!response.ok) {
            throw new Error(
                `AGI backend error: ${response.status} ${response.statusText}`
            );
        }

        const agiResponse: AgentResponse = await response.json();

        // Stream the response
        stream.markdown(
            `**AGI Response (${selectedAgent} agent, confidence: ${(
                agiResponse.confidence * 100
            ).toFixed(1)}%)**\\n\\n`
        );
        stream.markdown(agiResponse.content);

        if (agiResponse.reasoning) {
            stream.markdown(`\\n\\n*Reasoning:* ${agiResponse.reasoning}`);
        }

        return { metadata: { command: "agi-chat" } };
    } catch (error) {
        const errorMessage =
            error instanceof Error ? error.message : "Unknown error occurred";

        stream.markdown(
            `❌ **Error connecting to AGI system:**\\n\\n${errorMessage}\\n\\n`
        );
        stream.markdown(
            `Please ensure the AGI backend is running at \`${vscode.workspace
                .getConfiguration("agiChat")
                .get("semanticKernelEndpoint")}\``
        );

        return { metadata: { command: "agi-chat", error: errorMessage } };
    }
}

export function deactivate() {
    console.log("AGI Chat Assistant deactivated");
}
