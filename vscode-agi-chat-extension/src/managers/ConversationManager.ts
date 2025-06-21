import * as vscode from "vscode";

export interface AGIMessage {
    id: string;
    content: string;
    role: "user" | "assistant" | "system";
    timestamp: number;
    agentType?: string;
    reasoning?: string;
    confidence?: number;
}

export interface AGIConversation {
    id: string;
    title: string;
    messages: AGIMessage[];
    createdAt: number;
    updatedAt: number;
    agentType: string;
}

export class ConversationManager {
    private conversations: AGIConversation[] = [];
    private currentConversationId: string | null = null;
    private readonly storageKey = "agiChatConversations";

    constructor(private context: vscode.ExtensionContext) {
        this.loadConversations();
    }

    createNewConversation(
        agentType: string = "neural-symbolic"
    ): AGIConversation {
        const conversation: AGIConversation = {
            id: this.generateId(),
            title: `AGI Chat ${new Date().toLocaleString()}`,
            messages: [],
            createdAt: Date.now(),
            updatedAt: Date.now(),
            agentType,
        };

        this.conversations.unshift(conversation);
        this.currentConversationId = conversation.id;
        this.saveConversations();

        return conversation;
    }

    getCurrentConversation(): AGIConversation | null {
        if (!this.currentConversationId) {
            return this.createNewConversation();
        }

        return (
            this.conversations.find(
                (c) => c.id === this.currentConversationId
            ) || null
        );
    }

    addMessage(message: Omit<AGIMessage, "id" | "timestamp">): AGIMessage {
        const conversation = this.getCurrentConversation();
        if (!conversation) {
            throw new Error("No active conversation");
        }

        const newMessage: AGIMessage = {
            ...message,
            id: this.generateId(),
            timestamp: Date.now(),
        };

        conversation.messages.push(newMessage);
        conversation.updatedAt = Date.now();

        // Update title based on first user message
        if (conversation.messages.length === 1 && message.role === "user") {
            conversation.title =
                message.content.substring(0, 50) +
                (message.content.length > 50 ? "..." : "");
        }

        this.saveConversations();
        return newMessage;
    }

    getAllConversations(): AGIConversation[] {
        return [...this.conversations];
    }

    getConversation(id: string): AGIConversation | null {
        return this.conversations.find((c) => c.id === id) || null;
    }

    setCurrentConversation(id: string): boolean {
        const conversation = this.getConversation(id);
        if (conversation) {
            this.currentConversationId = id;
            return true;
        }
        return false;
    }

    deleteConversation(id: string): boolean {
        const index = this.conversations.findIndex((c) => c.id === id);
        if (index !== -1) {
            this.conversations.splice(index, 1);

            if (this.currentConversationId === id) {
                this.currentConversationId =
                    this.conversations.length > 0
                        ? this.conversations[0].id
                        : null;
            }

            this.saveConversations();
            return true;
        }
        return false;
    }

    clearHistory(): void {
        this.conversations = [];
        this.currentConversationId = null;
        this.saveConversations();
    }

    private loadConversations(): void {
        try {
            const stored = this.context.globalState.get<AGIConversation[]>(
                this.storageKey
            );
            if (stored && Array.isArray(stored)) {
                this.conversations = stored;
                if (this.conversations.length > 0) {
                    this.currentConversationId = this.conversations[0].id;
                }
            }
        } catch (error) {
            console.error("Failed to load conversations:", error);
        }
    }

    private saveConversations(): void {
        try {
            // Keep only the most recent 50 conversations
            const conversationsToSave = this.conversations.slice(0, 50);
            this.context.globalState.update(
                this.storageKey,
                conversationsToSave
            );
        } catch (error) {
            console.error("Failed to save conversations:", error);
        }
    }

    private generateId(): string {
        return (
            Date.now().toString(36) + Math.random().toString(36).substring(2)
        );
    }
}
