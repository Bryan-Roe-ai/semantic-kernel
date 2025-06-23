import * as vscode from "vscode";
import { AGIAgent, AGIAgentResponse } from "../agents/AGIAgent";
import { ConversationManager } from "../managers/ConversationManager";

export class ChatWebviewProvider implements vscode.WebviewViewProvider {
    public static readonly viewType = "agiChatView";
    private _view?: vscode.WebviewView;

    constructor(
        private readonly _extensionUri: vscode.Uri,
        private conversationManager: ConversationManager,
        private agiAgent: AGIAgent
    ) {}

    public resolveWebviewView(
        webviewView: vscode.WebviewView,
        context: vscode.WebviewViewResolveContext,
        _token: vscode.CancellationToken
    ) {
        this._view = webviewView;

        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [this._extensionUri],
        };

        webviewView.webview.html = this._getHtmlForWebview(webviewView.webview);

        webviewView.webview.onDidReceiveMessage(async (data) => {
            switch (data.type) {
                case "sendMessage":
                    await this.handleUserMessage(data.message);
                    break;
                case "clearChat":
                    this.conversationManager.createNewConversation();
                    this.updateChatView();
                    break;
                case "switchAgent":
                    this.agiAgent.switchAgent(data.agentType);
                    this.sendMessage({
                        type: "agentSwitched",
                        agentType: data.agentType,
                    });
                    break;
                case "requestHistory":
                    this.sendChatHistory();
                    break;
            }
        });

        // Send initial data
        this.sendChatHistory();
    }

    public openChatWindow() {
        if (this._view) {
            this._view.show?.(true);
        }
    }

    public async sendMessage(message: any) {
        if (this._view) {
            this._view.webview.postMessage(message);
        }
    }

    private async handleUserMessage(content: string) {
        try {
            // Add user message
            const userMessage = this.conversationManager.addMessage({
                content,
                role: "user",
                agentType: this.agiAgent.getCurrentAgentType(),
            });

            this.sendMessage({
                type: "userMessage",
                message: userMessage,
            });

            // Show typing indicator
            this.sendMessage({
                type: "typing",
                isTyping: true,
            });

            // Get conversation history for context
            const conversation =
                this.conversationManager.getCurrentConversation();
            const history = conversation?.messages || [];

            // Process with AGI agent
            const response: AGIAgentResponse =
                await this.agiAgent.processMessage(content, history);

            // Add assistant response
            const assistantMessage = this.conversationManager.addMessage({
                content: response.content,
                role: "assistant",
                agentType: this.agiAgent.getCurrentAgentType(),
                reasoning: response.reasoning,
                confidence: response.confidence,
            });

            // Hide typing indicator and send response
            this.sendMessage({
                type: "typing",
                isTyping: false,
            });

            this.sendMessage({
                type: "assistantMessage",
                message: assistantMessage,
                response: response,
            });
        } catch (error) {
            this.sendMessage({
                type: "typing",
                isTyping: false,
            });

            this.sendMessage({
                type: "error",
                message: `Error processing message: ${error}`,
            });
        }
    }

    private sendChatHistory() {
        const conversation = this.conversationManager.getCurrentConversation();
        this.sendMessage({
            type: "chatHistory",
            messages: conversation?.messages || [],
            agentType: this.agiAgent.getCurrentAgentType(),
            capabilities: this.agiAgent.getCapabilities(),
        });
    }

    private updateChatView() {
        this.sendChatHistory();
    }

    private _getHtmlForWebview(webview: vscode.Webview) {
        const scriptUri = webview.asWebviewUri(
            vscode.Uri.joinPath(this._extensionUri, "media", "main.js")
        );
        const styleMainUri = webview.asWebviewUri(
            vscode.Uri.joinPath(this._extensionUri, "media", "main.css")
        );

        return `<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link href="${styleMainUri}" rel="stylesheet">
                <title>AGI Chat Assistant</title>
                <style>
                    body {
                        font-family: var(--vscode-font-family);
                        font-size: var(--vscode-font-size);
                        color: var(--vscode-foreground);
                        background-color: var(--vscode-editor-background);
                        margin: 0;
                        padding: 0;
                        height: 100vh;
                        display: flex;
                        flex-direction: column;
                    }

                    .chat-header {
                        padding: 10px;
                        border-bottom: 1px solid var(--vscode-panel-border);
                        background-color: var(--vscode-panel-background);
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                    }

                    .agent-selector {
                        background: var(--vscode-dropdown-background);
                        color: var(--vscode-dropdown-foreground);
                        border: 1px solid var(--vscode-dropdown-border);
                        padding: 4px 8px;
                        border-radius: 4px;
                        font-size: 12px;
                    }

                    .chat-container {
                        flex: 1;
                        overflow-y: auto;
                        padding: 10px;
                        display: flex;
                        flex-direction: column;
                        gap: 10px;
                    }

                    .message {
                        max-width: 80%;
                        padding: 10px;
                        border-radius: 8px;
                        word-wrap: break-word;
                        position: relative;
                    }

                    .message.user {
                        align-self: flex-end;
                        background-color: var(--vscode-button-background);
                        color: var(--vscode-button-foreground);
                    }

                    .message.assistant {
                        align-self: flex-start;
                        background-color: var(--vscode-textBlockQuote-background);
                        border-left: 4px solid var(--vscode-textBlockQuote-border);
                    }

                    .message.system {
                        align-self: center;
                        background-color: var(--vscode-panel-background);
                        border: 1px solid var(--vscode-panel-border);
                        font-style: italic;
                        text-align: center;
                        max-width: 60%;
                    }

                    .message-meta {
                        font-size: 11px;
                        opacity: 0.7;
                        margin-top: 5px;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                    }

                    .confidence-bar {
                        width: 50px;
                        height: 3px;
                        background-color: var(--vscode-progressBar-background);
                        border-radius: 2px;
                        overflow: hidden;
                    }

                    .confidence-fill {
                        height: 100%;
                        background-color: var(--vscode-progressBar-background);
                        transition: width 0.3s;
                    }

                    .typing-indicator {
                        display: none;
                        align-self: flex-start;
                        padding: 10px;
                        background-color: var(--vscode-textBlockQuote-background);
                        border-radius: 8px;
                        max-width: 80%;
                    }

                    .typing-dots {
                        display: flex;
                        gap: 4px;
                    }

                    .typing-dot {
                        width: 6px;
                        height: 6px;
                        background-color: var(--vscode-foreground);
                        border-radius: 50%;
                        opacity: 0.4;
                        animation: typingAnimation 1.4s infinite ease-in-out both;
                    }

                    .typing-dot:nth-child(1) { animation-delay: -0.32s; }
                    .typing-dot:nth-child(2) { animation-delay: -0.16s; }

                    @keyframes typingAnimation {
                        0%, 80%, 100% { opacity: 0.4; }
                        40% { opacity: 1; }
                    }

                    .input-container {
                        padding: 10px;
                        border-top: 1px solid var(--vscode-panel-border);
                        background-color: var(--vscode-panel-background);
                        display: flex;
                        gap: 8px;
                    }

                    .message-input {
                        flex: 1;
                        background: var(--vscode-input-background);
                        color: var(--vscode-input-foreground);
                        border: 1px solid var(--vscode-input-border);
                        padding: 8px 12px;
                        border-radius: 4px;
                        font-family: inherit;
                        font-size: inherit;
                        resize: none;
                        min-height: 20px;
                        max-height: 100px;
                    }

                    .message-input:focus {
                        outline: none;
                        border-color: var(--vscode-focusBorder);
                    }

                    .send-button {
                        background: var(--vscode-button-background);
                        color: var(--vscode-button-foreground);
                        border: none;
                        padding: 8px 16px;
                        border-radius: 4px;
                        cursor: pointer;
                        font-family: inherit;
                        font-size: inherit;
                    }

                    .send-button:hover {
                        background: var(--vscode-button-hoverBackground);
                    }

                    .send-button:disabled {
                        opacity: 0.5;
                        cursor: not-allowed;
                    }

                    .capabilities {
                        margin-top: 8px;
                        font-size: 11px;
                        opacity: 0.8;
                    }

                    .capability {
                        display: inline-block;
                        background: var(--vscode-badge-background);
                        color: var(--vscode-badge-foreground);
                        padding: 2px 6px;
                        border-radius: 10px;
                        margin-right: 4px;
                        margin-bottom: 2px;
                    }

                    .reasoning-details {
                        margin-top: 8px;
                        padding: 8px;
                        background: var(--vscode-editor-inactiveSelectionBackground);
                        border-radius: 4px;
                        font-size: 12px;
                        opacity: 0.9;
                    }

                    .empty-state {
                        flex: 1;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                        text-align: center;
                        opacity: 0.7;
                        padding: 20px;
                    }

                    .empty-state h3 {
                        margin-bottom: 10px;
                        color: var(--vscode-foreground);
                    }

                    .empty-state p {
                        color: var(--vscode-descriptionForeground);
                        margin-bottom: 20px;
                    }
                </style>
            </head>
            <body>
                <div class="chat-header">
                    <div>
                        <strong>🤖 AGI Chat Assistant</strong>
                        <div style="font-size: 11px; opacity: 0.8;">Neural-Symbolic Intelligence</div>
                    </div>
                    <select class="agent-selector" id="agentSelector">
                        <option value="neural-symbolic">🧠 Neural-Symbolic</option>
                        <option value="reasoning">🔍 Reasoning</option>
                        <option value="creative">🎨 Creative</option>
                        <option value="analytical">📊 Analytical</option>
                        <option value="general">💭 General</option>
                    </select>
                </div>

                <div class="chat-container" id="chatContainer">
                    <div class="empty-state">
                        <h3>Welcome to AGI Chat</h3>
                        <p>Start a conversation with your Neural-Symbolic AGI Assistant</p>
                        <div>
                            <div class="capability">Neural Networks</div>
                            <div class="capability">Symbolic Reasoning</div>
                            <div class="capability">Knowledge Graphs</div>
                            <div class="capability">Multi-Modal Processing</div>
                        </div>
                    </div>
                </div>

                <div class="typing-indicator" id="typingIndicator">
                    <div class="typing-dots">
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                    </div>
                    <span style="margin-left: 10px; font-size: 12px;">AGI is thinking...</span>
                </div>

                <div class="input-container">
                    <textarea
                        class="message-input"
                        id="messageInput"
                        placeholder="Ask your AGI assistant anything..."
                        rows="1"
                    ></textarea>
                    <button class="send-button" id="sendButton">Send</button>
                </div>

                <script>
                    const vscode = acquireVsCodeApi();
                    const chatContainer = document.getElementById('chatContainer');
                    const messageInput = document.getElementById('messageInput');
                    const sendButton = document.getElementById('sendButton');
                    const typingIndicator = document.getElementById('typingIndicator');
                    const agentSelector = document.getElementById('agentSelector');

                    let currentMessages = [];

                    // Auto-resize textarea
                    messageInput.addEventListener('input', function() {
                        this.style.height = 'auto';
                        this.style.height = Math.min(this.scrollHeight, 100) + 'px';
                    });

                    // Send message on Enter (but not Shift+Enter)
                    messageInput.addEventListener('keydown', function(e) {
                        if (e.key === 'Enter' && !e.shiftKey) {
                            e.preventDefault();
                            sendMessage();
                        }
                    });

                    sendButton.addEventListener('click', sendMessage);

                    agentSelector.addEventListener('change', function() {
                        vscode.postMessage({
                            type: 'switchAgent',
                            agentType: this.value
                        });
                    });

                    function sendMessage() {
                        const message = messageInput.value.trim();
                        if (!message) return;

                        vscode.postMessage({
                            type: 'sendMessage',
                            message: message
                        });

                        messageInput.value = '';
                        messageInput.style.height = 'auto';
                    }

                    function showTyping(show) {
                        typingIndicator.style.display = show ? 'block' : 'none';
                        if (show) {
                            chatContainer.scrollTop = chatContainer.scrollHeight;
                        }
                    }

                    function addMessage(message, response = null) {
                        const messageDiv = document.createElement('div');
                        messageDiv.className = \`message \${message.role}\`;

                        const contentDiv = document.createElement('div');
                        contentDiv.textContent = message.content;
                        messageDiv.appendChild(contentDiv);

                        if (message.role === 'assistant' && response) {
                            // Add reasoning details if available
                            if (response.reasoning) {
                                const reasoningDiv = document.createElement('div');
                                reasoningDiv.className = 'reasoning-details';
                                reasoningDiv.textContent = \`Reasoning: \${response.reasoning}\`;
                                messageDiv.appendChild(reasoningDiv);
                            }

                            // Add capabilities used
                            if (response.capabilities_used && response.capabilities_used.length > 0) {
                                const capabilitiesDiv = document.createElement('div');
                                capabilitiesDiv.className = 'capabilities';
                                response.capabilities_used.forEach(cap => {
                                    const capSpan = document.createElement('span');
                                    capSpan.className = 'capability';
                                    capSpan.textContent = cap.replace('_', ' ');
                                    capabilitiesDiv.appendChild(capSpan);
                                });
                                messageDiv.appendChild(capabilitiesDiv);
                            }
                        }

                        // Add metadata
                        const metaDiv = document.createElement('div');
                        metaDiv.className = 'message-meta';

                        const timeSpan = document.createElement('span');
                        timeSpan.textContent = new Date(message.timestamp).toLocaleTimeString();
                        metaDiv.appendChild(timeSpan);

                        if (message.role === 'assistant' && message.confidence) {
                            const confidenceDiv = document.createElement('div');
                            confidenceDiv.innerHTML = \`
                                <span style="margin-right: 8px;">Confidence: \${Math.round(message.confidence * 100)}%</span>
                                <div class="confidence-bar">
                                    <div class="confidence-fill" style="width: \${message.confidence * 100}%; background-color: \${message.confidence > 0.8 ? '#4CAF50' : message.confidence > 0.6 ? '#FF9800' : '#F44336'}"></div>
                                </div>
                            \`;
                            metaDiv.appendChild(confidenceDiv);
                        }

                        messageDiv.appendChild(metaDiv);
                        chatContainer.appendChild(messageDiv);
                        chatContainer.scrollTop = chatContainer.scrollHeight;
                    }

                    function clearChat() {
                        chatContainer.innerHTML = '';
                        currentMessages = [];
                    }

                    function updateEmptyState() {
                        const isEmpty = currentMessages.length === 0;
                        const emptyState = chatContainer.querySelector('.empty-state');
                        if (emptyState) {
                            emptyState.style.display = isEmpty ? 'flex' : 'none';
                        }
                    }

                    // Handle messages from extension
                    window.addEventListener('message', event => {
                        const message = event.data;

                        switch (message.type) {
                            case 'chatHistory':
                                clearChat();
                                currentMessages = message.messages || [];
                                agentSelector.value = message.agentType || 'neural-symbolic';

                                if (currentMessages.length === 0) {
                                    // Show empty state
                                    chatContainer.innerHTML = \`
                                        <div class="empty-state">
                                            <h3>Welcome to AGI Chat</h3>
                                            <p>Start a conversation with your Neural-Symbolic AGI Assistant</p>
                                            <div>
                                                <div class="capability">Neural Networks</div>
                                                <div class="capability">Symbolic Reasoning</div>
                                                <div class="capability">Knowledge Graphs</div>
                                                <div class="capability">Multi-Modal Processing</div>
                                            </div>
                                        </div>
                                    \`;
                                } else {
                                    currentMessages.forEach(msg => addMessage(msg));
                                }
                                break;

                            case 'userMessage':
                                currentMessages.push(message.message);
                                addMessage(message.message);
                                updateEmptyState();
                                break;

                            case 'assistantMessage':
                                currentMessages.push(message.message);
                                addMessage(message.message, message.response);
                                updateEmptyState();
                                break;

                            case 'typing':
                                showTyping(message.isTyping);
                                break;

                            case 'agentSwitched':
                                agentSelector.value = message.agentType;
                                const systemMessage = {
                                    id: 'system-' + Date.now(),
                                    content: \`Switched to \${message.agentType} agent\`,
                                    role: 'system',
                                    timestamp: Date.now()
                                };
                                addMessage(systemMessage);
                                break;

                            case 'error':
                                const errorMessage = {
                                    id: 'error-' + Date.now(),
                                    content: \`❌ \${message.message}\`,
                                    role: 'system',
                                    timestamp: Date.now()
                                };
                                addMessage(errorMessage);
                                break;
                        }
                    });

                    // Request initial chat history
                    vscode.postMessage({ type: 'requestHistory' });
                </script>
            </body>
            </html>`;
    }
}
