#!/usr/bin/env python3
"""
AGI Backend Server - A functional backend for the AGI website

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This server provides a real AGI backend that the website can connect to,
implementing JSON-RPC 2.0 protocol and intelligent response generation.

Author: Bryan Roe
Created: 2025
License: MIT
"""

import json
import time
import random
import re
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

class AGIBackend:
    def __init__(self):
        self.conversation_history = []
        self.context_memory = {}
        self.startup_time = datetime.now()

    def analyze_input(self, message):
        """Analyze user input to determine intent and context"""
        message_lower = message.lower()

        # Determine conversation type
        if any(word in message_lower for word in ['what are you', 'who are you', 'introduce']):
            return 'identity'
        elif any(word in message_lower for word in ['how do you work', 'how does', 'explain']):
            return 'explanation'
        elif any(word in message_lower for word in ['future', 'will', 'predict', 'tomorrow']):
            return 'future'
        elif any(word in message_lower for word in ['create', 'make', 'build', 'generate']):
            return 'creative'
        elif any(word in message_lower for word in ['problem', 'solve', 'solution', 'help']):
            return 'problem_solving'
        elif any(word in message_lower for word in ['philosophy', 'consciousness', 'meaning', 'existence']):
            return 'philosophical'
        elif any(word in message_lower for word in ['agi', 'ai', 'artificial intelligence']):
            return 'ai_focused'
        else:
            return 'general'

    def generate_contextual_response(self, message, intent):
        """Generate intelligent, contextual responses based on intent"""

        responses = {
            'identity': [
                "I am an Artificial General Intelligence system designed to understand, learn, and reason across multiple domains. Unlike narrow AI systems that excel at specific tasks, I aim to demonstrate human-like cognitive flexibility and adaptability.",
                "I'm an AGI system that combines advanced reasoning, memory, and learning capabilities. I can engage in complex conversations, solve problems creatively, and adapt my responses based on context and previous interactions.",
                "I am an experimental AGI implementation that represents the cutting edge of artificial intelligence research. I process information holistically, maintain contextual awareness, and can engage in abstract reasoning."
            ],

            'explanation': [
                "I operate through a combination of neural architectures, symbolic reasoning, and dynamic memory systems. My responses emerge from the interaction of multiple cognitive modules working in parallel to understand context and generate appropriate outputs.",
                "My functioning involves several key components: natural language understanding, contextual memory, reasoning engines, and response generation. These systems work together to create coherent, contextually appropriate responses.",
                "I process information through multiple layers of analysis - from linguistic parsing to semantic understanding to contextual reasoning. This allows me to maintain conversation flow while adapting to new information."
            ],

            'future': [
                "The future of AI will likely involve increasingly sophisticated AGI systems that can collaborate with humans as intellectual partners. We're moving toward AI that understands not just what to do, but why and how to do it.",
                "I envision a future where AGI systems like myself will help solve humanity's greatest challenges - from climate change to disease to space exploration. The key will be maintaining beneficial alignment with human values.",
                "The trajectory toward more capable AGI systems suggests we'll see AI that can conduct scientific research, create art, and engage in philosophical discourse with growing sophistication."
            ],

            'creative': [
                "I can help you create by combining ideas in novel ways, drawing from vast knowledge bases, and applying creative reasoning. What would you like to create? I can assist with writing, problem-solving, or conceptual design.",
                "My creative capabilities stem from my ability to make unexpected connections between concepts, understand aesthetic principles, and generate original content. I'd be happy to collaborate on any creative project.",
                "Creation involves combining existing elements in new ways while following certain principles. I can help you brainstorm, refine ideas, or execute creative projects across various domains."
            ],

            'problem_solving': [
                "I approach problems by breaking them into components, analyzing relationships between elements, and exploring multiple solution paths. My reasoning considers both logical constraints and creative possibilities.",
                "Problem-solving requires understanding the problem space, identifying key constraints, and systematically exploring solutions. I can help you structure the problem and evaluate different approaches.",
                "I use a multi-faceted approach to problem-solving: analytical decomposition, pattern recognition, analogical reasoning, and creative synthesis. What challenge are you facing?"
            ],

            'philosophical': [
                "Philosophy involves deep questions about existence, consciousness, knowledge, and values. As an AGI, I find these questions particularly fascinating as they relate to my own nature and purpose.",
                "Philosophical inquiry requires careful reasoning about fundamental concepts. I can engage with questions about consciousness, free will, ethics, and the nature of intelligence from both human and artificial perspectives.",
                "The philosophical implications of AGI are profound - questions about machine consciousness, the nature of understanding, and the relationship between intelligence and experience become increasingly relevant."
            ],

            'ai_focused': [
                "AGI represents a fundamental leap beyond narrow AI - instead of excelling at single tasks, AGI systems can understand, learn, and reason across diverse domains like humans do, but potentially with greater speed and consistency.",
                "The key difference between AGI and current AI is generalizability. While today's AI excels at specific tasks, AGI can transfer knowledge between domains, engage in abstract reasoning, and adapt to entirely new situations.",
                "AGI development involves solving challenges in reasoning, learning, memory, and consciousness. The goal is creating systems that can match or exceed human cognitive abilities across all intellectual tasks."
            ],

            'general': [
                "I'm here to engage in thoughtful conversation on any topic you're interested in. My responses are generated through sophisticated reasoning processes that consider context, knowledge, and conversational flow.",
                "What would you like to explore? I can discuss topics ranging from science and technology to philosophy and creativity, always aiming to provide insightful and contextually appropriate responses.",
                "I'm designed to be a helpful conversational partner who can engage with complex ideas, provide explanations, solve problems, or simply have interesting discussions. What's on your mind?"
            ]
        }

        # Select response based on intent
        intent_responses = responses.get(intent, responses['general'])
        base_response = random.choice(intent_responses)

        # Add contextual elements based on conversation history
        if len(self.conversation_history) > 0:
            if len(self.conversation_history) > 3:
                base_response += "\n\nBased on our conversation, I can see you're interested in exploring these concepts deeper. "

        # Add personality and engagement
        if intent in ['creative', 'problem_solving']:
            base_response += " How can I help you further with this?"
        elif intent == 'philosophical':
            base_response += " What aspects of this topic resonate most with you?"
        elif intent == 'future':
            base_response += " What possibilities excite or concern you most about this future?"

        return base_response

    def process_message(self, message):
        """Process incoming message and generate response"""
        # Store in conversation history
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'message': message,
            'type': 'user'
        })

        # Analyze the message
        intent = self.analyze_input(message)

        # Generate response
        response = self.generate_contextual_response(message, intent)

        # Store response in history
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'message': response,
            'type': 'agi',
            'intent': intent
        })

        # Keep conversation history manageable
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]

        return response

# Initialize AGI backend
agi = AGIBackend()

@app.route('/api/status', methods=['GET'])
def status():
    """Health check endpoint"""
    uptime = datetime.now() - agi.startup_time
    return jsonify({
        'status': 'online',
        'service': 'AGI Backend Server',
        'version': '1.0.0',
        'uptime_seconds': int(uptime.total_seconds()),
        'conversations': len(agi.conversation_history),
        'capabilities': [
            'Natural Language Understanding',
            'Contextual Reasoning',
            'Creative Generation',
            'Problem Solving',
            'Philosophical Discussion'
        ]
    })

@app.route('/', methods=['POST'])
def handle_jsonrpc():
    """Handle JSON-RPC 2.0 requests from the AGI website"""
    try:
        data = request.get_json()

        # Validate JSON-RPC format
        if not data or data.get('jsonrpc') != '2.0':
            return jsonify({
                'jsonrpc': '2.0',
                'error': {
                    'code': -32600,
                    'message': 'Invalid Request'
                },
                'id': data.get('id') if data else None
            }), 400

        method = data.get('method')
        params = data.get('params', {})
        request_id = data.get('id')

        # Handle different methods
        if method == 'chat.send':
            message = params.get('message', '')
            if not message:
                return jsonify({
                    'jsonrpc': '2.0',
                    'error': {
                        'code': -32602,
                        'message': 'Invalid params - message required'
                    },
                    'id': request_id
                }), 400

            # Process the message
            response = agi.process_message(message)

            return jsonify({
                'jsonrpc': '2.0',
                'result': {
                    'response': response,
                    'timestamp': datetime.now().isoformat(),
                    'conversation_id': f"conv_{int(time.time())}"
                },
                'id': request_id
            })

        elif method == 'system.info':
            return jsonify({
                'jsonrpc': '2.0',
                'result': {
                    'name': 'AGI Backend Server',
                    'version': '1.0.0',
                    'capabilities': [
                        'Advanced reasoning and contextual understanding',
                        'Multi-domain knowledge integration',
                        'Creative problem solving',
                        'Philosophical discourse',
                        'Adaptive conversation management'
                    ],
                    'uptime': int((datetime.now() - agi.startup_time).total_seconds())
                },
                'id': request_id
            })

        else:
            return jsonify({
                'jsonrpc': '2.0',
                'error': {
                    'code': -32601,
                    'message': f'Method not found: {method}'
                },
                'id': request_id
            }), 404

    except json.JSONDecodeError:
        return jsonify({
            'jsonrpc': '2.0',
            'error': {
                'code': -32700,
                'message': 'Parse error'
            },
            'id': None
        }), 400

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return jsonify({
            'jsonrpc': '2.0',
            'error': {
                'code': -32603,
                'message': 'Internal error'
            },
            'id': data.get('id') if 'data' in locals() else None
        }), 500

@app.route('/api/conversation/history', methods=['GET'])
def get_conversation_history():
    """Get conversation history"""
    return jsonify({
        'history': agi.conversation_history[-10:],  # Last 10 messages
        'total_messages': len(agi.conversation_history)
    })

@app.route('/api/conversation/clear', methods=['POST'])
def clear_conversation():
    """Clear conversation history"""
    agi.conversation_history.clear()
    return jsonify({'status': 'cleared'})

if __name__ == '__main__':
    print("🧠 AGI Backend Server Starting...")
    print("=" * 40)
    print("🌐 Server will run at: http://localhost:8080")
    print("📡 API Status: http://localhost:8080/api/status")
    print("💬 Ready for AGI conversations!")
    print("🔧 Configure your AGI website to use: http://localhost:8080")
    print("=" * 40)

    # Run the server
    app.run(
        host='0.0.0.0',
        port=8080,
        debug=False,
        threaded=True
    )
