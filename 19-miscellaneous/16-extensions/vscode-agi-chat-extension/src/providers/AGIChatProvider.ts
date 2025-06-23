import * as vscode from "vscode";
import {
    AGIConversation,
    ConversationManager,
} from "../managers/ConversationManager";

export class AGIChatProvider
    implements vscode.TreeDataProvider<AGIConversationItem>
{
    private _onDidChangeTreeData: vscode.EventEmitter<
        AGIConversationItem | undefined | null | void
    > = new vscode.EventEmitter<
        AGIConversationItem | undefined | null | void
    >();
    readonly onDidChangeTreeData: vscode.Event<
        AGIConversationItem | undefined | null | void
    > = this._onDidChangeTreeData.event;

    constructor(
        private context: vscode.ExtensionContext,
        private conversationManager: ConversationManager
    ) {}

    refresh(): void {
        this._onDidChangeTreeData.fire();
    }

    getTreeItem(element: AGIConversationItem): vscode.TreeItem {
        return element;
    }

    getChildren(
        element?: AGIConversationItem
    ): Thenable<AGIConversationItem[]> {
        if (!element) {
            // Root level - return conversations
            const conversations =
                this.conversationManager.getAllConversations();
            return Promise.resolve(
                conversations.map(
                    (conv) =>
                        new AGIConversationItem(
                            conv.title,
                            vscode.TreeItemCollapsibleState.Collapsed,
                            conv,
                            "conversation"
                        )
                )
            );
        } else if (element.contextValue === "conversation") {
            // Return messages for this conversation
            const conversation = element.conversation;
            if (conversation) {
                return Promise.resolve(
                    conversation.messages
                        .slice(-5)
                        .map(
                            (msg) =>
                                new AGIConversationItem(
                                    `${msg.role}: ${msg.content.substring(
                                        0,
                                        50
                                    )}${msg.content.length > 50 ? "..." : ""}`,
                                    vscode.TreeItemCollapsibleState.None,
                                    undefined,
                                    "message",
                                    msg
                                )
                        )
                );
            }
        }

        return Promise.resolve([]);
    }
}

export class AGIConversationItem extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        public readonly collapsibleState: vscode.TreeItemCollapsibleState,
        public readonly conversation?: AGIConversation,
        public readonly contextValue?: string,
        public readonly message?: any
    ) {
        super(label, collapsibleState);

        this.tooltip = this.label;

        if (contextValue === "conversation") {
            this.iconPath = new vscode.ThemeIcon("comment-discussion");
            this.contextValue = "conversation";
            this.command = {
                command: "agiChat.selectConversation",
                title: "Select Conversation",
                arguments: [conversation?.id],
            };
        } else if (contextValue === "message") {
            this.iconPath = new vscode.ThemeIcon(
                message?.role === "user" ? "person" : "robot"
            );
            this.contextValue = "message";
        }
    }
}
