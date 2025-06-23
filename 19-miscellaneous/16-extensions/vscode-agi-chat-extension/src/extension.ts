import * as vscode from "vscode";
import { AGIAgent } from "./agents/AGIAgent";
import { ConversationManager } from "./managers/ConversationManager";
import { AGIChatProvider } from "./providers/AGIChatProvider";
import { ChatWebviewProvider } from "./webview/ChatWebviewProvider";

export function activate(context: vscode.ExtensionContext) {
    console.log("AGI Chat Assistant is now active!");

    // Initialize core components
    const conversationManager = new ConversationManager(context);
    const agiAgent = new AGIAgent();
    const chatWebviewProvider = new ChatWebviewProvider(
        context.extensionUri,
        conversationManager,
        agiAgent
    );
    const agiChatProvider = new AGIChatProvider(context, conversationManager);

    // Register webview provider
    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider(
            "agiChatView",
            chatWebviewProvider,
            {
                webviewOptions: {
                    retainContextWhenHidden: true,
                },
            }
        )
    );

    // Register tree data provider
    vscode.window.registerTreeDataProvider("agiChatView", agiChatProvider);

    // Register commands
    const commands = [
        vscode.commands.registerCommand("agiChat.openChat", () => {
            chatWebviewProvider.openChatWindow();
        }),

        vscode.commands.registerCommand("agiChat.newConversation", () => {
            conversationManager.createNewConversation();
            agiChatProvider.refresh();
            vscode.window.showInformationMessage(
                "New AGI conversation started!"
            );
        }),

        vscode.commands.registerCommand("agiChat.clearHistory", async () => {
            const result = await vscode.window.showWarningMessage(
                "Are you sure you want to clear all chat history?",
                "Yes",
                "No"
            );
            if (result === "Yes") {
                conversationManager.clearHistory();
                agiChatProvider.refresh();
                vscode.window.showInformationMessage("Chat history cleared!");
            }
        }),

        vscode.commands.registerCommand(
            "agiChat.exportConversation",
            async () => {
                const conversations = conversationManager.getAllConversations();
                if (conversations.length === 0) {
                    vscode.window.showInformationMessage(
                        "No conversations to export."
                    );
                    return;
                }

                const uri = await vscode.window.showSaveDialog({
                    filters: {
                        JSON: ["json"],
                        Text: ["txt"],
                    },
                    defaultUri: vscode.Uri.file("agi-conversations.json"),
                });

                if (uri) {
                    try {
                        const content = JSON.stringify(conversations, null, 2);
                        await vscode.workspace.fs.writeFile(
                            uri,
                            Buffer.from(content, "utf8")
                        );
                        vscode.window.showInformationMessage(
                            "Conversations exported successfully!"
                        );
                    } catch (error) {
                        vscode.window.showErrorMessage(
                            `Failed to export conversations: ${error}`
                        );
                    }
                }
            }
        ),

        vscode.commands.registerCommand("agiChat.switchAgent", async () => {
            const agents = [
                "neural-symbolic",
                "reasoning",
                "creative",
                "analytical",
                "general",
            ];
            const selected = await vscode.window.showQuickPick(agents, {
                placeHolder: "Select an AGI agent",
            });

            if (selected) {
                agiAgent.switchAgent(selected);
                vscode.window.showInformationMessage(
                    `Switched to ${selected} agent`
                );
            }
        }),

        vscode.commands.registerCommand("agiChat.configure", () => {
            vscode.commands.executeCommand(
                "workbench.action.openSettings",
                "agiChat"
            );
        }),

        vscode.commands.registerCommand(
            "agiChat.sendMessage",
            (message: string) => {
                chatWebviewProvider.sendMessage(message);
            }
        ),
    ];

    context.subscriptions.push(...commands);

    // Register status bar item
    const statusBarItem = vscode.window.createStatusBarItem(
        vscode.StatusBarAlignment.Right,
        100
    );
    statusBarItem.text = "$(robot) AGI Chat";
    statusBarItem.command = "agiChat.openChat";
    statusBarItem.tooltip = "Open AGI Chat Assistant";
    statusBarItem.show();
    context.subscriptions.push(statusBarItem);

    // Show welcome message
    vscode.window
        .showInformationMessage(
            "AGI Chat Assistant activated! Click the robot icon or use Ctrl+Shift+A to start.",
            "Open Chat"
        )
        .then((selection) => {
            if (selection === "Open Chat") {
                vscode.commands.executeCommand("agiChat.openChat");
            }
        });
}

export function deactivate() {
    console.log("AGI Chat Assistant deactivated");
}
