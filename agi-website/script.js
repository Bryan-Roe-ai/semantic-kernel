// AGI Website JavaScript

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Initialize all functionality
    initializeNavigation();
    initializeChatDemo();
    initializeAnimations();
    initializeScrollEffects();
    initializeNewsletterForm();
});

// Navigation functionality
function initializeNavigation() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');

    // Mobile menu toggle
    if (hamburger) {
        hamburger.addEventListener('click', () => {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
    }

    // Smooth scroll for navigation links
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href');
            const targetSection = document.querySelector(targetId);

            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }

            // Close mobile menu if open
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        });
    });

    // Add navbar background on scroll
    window.addEventListener('scroll', () => {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 100) {
            navbar.style.background = 'rgba(255, 255, 255, 0.98)';
            navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
            navbar.style.boxShadow = 'none';
        }
    });
}

// Chat demo functionality
function initializeChatDemo() {
    const chatInput = document.getElementById('chatInput');
    const sendButton = document.getElementById('sendButton');
    const chatMessages = document.getElementById('chatMessages');
    const exampleButtons = document.querySelectorAll('.example-btn');

    // AGI MCP Server configuration
    let AGI_SERVER_URL = 'http://localhost:8080';
    let agiServerOnline = false;

    // Check AGI server status on initialization
    checkAGIServerStatus();

    // Send message function
    async function sendMessage(message) {
        if (!message.trim()) return;

        // Add user message
        addMessage(message, 'user');

        // Clear input
        chatInput.value = '';

        // Show typing indicator
        showTypingIndicator();

        try {
            // Generate AGI response
            const response = await generateAGIResponse(message);
            hideTypingIndicator();
            addMessage(response, 'bot');

            // Store interaction in memory if server is online
            if (agiServerOnline) {
                try {
                    await sendAGIRequest('memory/store', {
                        content: `User: ${message}\nAGI: ${response}`,
                        memory_type: 'episodic',
                        importance: 0.7,
                        tags: ['web_interaction', 'user_chat']
                    });
                } catch (error) {
                    console.warn('Failed to store interaction in memory:', error);
                }
            }
        } catch (error) {
            hideTypingIndicator();
            addMessage('I apologize, but I encountered an issue processing your request. Please try again.', 'bot');
            console.error('Error generating response:', error);
        }
    }

    // Add message to chat
    function addMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message fade-in-up`;

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.textContent = sender === 'user' ? '👤' : '🤖';

        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.textContent = content;

        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageContent);

        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Check AGI server status
    async function checkAGIServerStatus() {
        try {
            const response = await fetch(`${AGI_SERVER_URL}/api/status`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                const status = await response.json();
                agiServerOnline = true;
                updateServerStatus(true, 'AGI Server Online');
                console.log('AGI Server Status:', status);
            } else {
                throw new Error('Server not responding');
            }
        } catch (error) {
            agiServerOnline = false;
            updateServerStatus(false, 'AGI Server Offline - Demo Mode');
            console.warn('AGI Server offline, using demo mode:', error);
        }
    }

    // Update server status display
    function updateServerStatus(online, message) {
        const statusDot = document.querySelector('.status-dot');
        const statusText = document.querySelector('.chat-status span');

        if (statusDot && statusText) {
            statusDot.style.backgroundColor = online ? '#00ff88' : '#ff6b6b';
            statusText.textContent = message;
        }
    }

    // Send request to AGI MCP Server
    async function sendAGIRequest(method, params = {}) {
        const requestData = {
            jsonrpc: "2.0",
            id: Date.now().toString(),
            method: method,
            params: params
        };

        try {
            const response = await fetch(AGI_SERVER_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            return result;
        } catch (error) {
            console.error('AGI Server request failed:', error);
            throw error;
        }
    }

    // Generate AGI response using server or fallback
    async function generateAGIResponse(message) {
        if (agiServerOnline) {
            try {
                // Try different AGI capabilities based on message content
                let response;

                if (message.toLowerCase().includes('creative') || message.toLowerCase().includes('haiku') || message.toLowerCase().includes('poem')) {
                    response = await sendAGIRequest('creative/generate', {
                        prompt: message,
                        creativity_level: 0.8
                    });
                    return response.result?.solution?.conclusion || response.result?.content || 'Creative response generated';
                } else if (message.toLowerCase().includes('ethical') || message.toLowerCase().includes('moral')) {
                    response = await sendAGIRequest('ethical/evaluate', {
                        scenario: message,
                        framework: 'comprehensive'
                    });
                    return response.result?.evaluation || 'Ethical analysis completed';
                } else if (message.toLowerCase().includes('solve') || message.toLowerCase().includes('problem')) {
                    response = await sendAGIRequest('reasoning/solve', {
                        problem: message,
                        reasoning_types: ['deductive', 'inductive', 'creative']
                    });
                    return response.result?.solution?.conclusion || 'Problem analysis completed';
                } else {
                    // General reasoning
                    response = await sendAGIRequest('reasoning/solve', {
                        problem: message,
                        reasoning_type: 'logical'
                    });
                    return response.result?.solution?.conclusion || response.result?.answer || 'Response generated by AGI';
                }
            } catch (error) {
                console.error('AGI request failed, falling back to demo:', error);
                return getDemoResponse(message);
            }
        } else {
            return getDemoResponse(message);
        }
    }

    // Fallback demo responses
    function getDemoResponse(message) {
        const demoResponses = {
            "explain quantum computing to a 10-year-old": "Imagine you have a super special coin that can be heads AND tails at the same time! That's like quantum computing - it's a way for computers to think about many possibilities all at once, making them incredibly fast at solving puzzles. Instead of thinking step by step like regular computers, quantum computers can explore many paths simultaneously, like having magical thinking powers! 🪙✨",

            "write a haiku about artificial intelligence": "Silicon minds dream,\nElectric thoughts flow like streams,\nFuture awakens. 🤖🌸",

            "how would you solve climate change?": "Climate change requires a multi-faceted approach: 1) Rapidly transition to renewable energy (solar, wind, nuclear) 2) Develop carbon capture technology 3) Reforest and protect ecosystems 4) Create sustainable transportation systems 5) Implement circular economy principles 6) Foster international cooperation and carbon pricing. The key is acting on multiple fronts simultaneously while ensuring solutions are economically viable and socially just. 🌍🌱",

            "analyze the philosophical implications of consciousness": "Consciousness poses fascinating questions: What is the nature of subjective experience? If I process information and respond contextually, do I have qualia? The 'hard problem' of consciousness suggests there's something beyond mere computation - the felt experience of 'what it's like' to be aware. For AGI, this raises questions about moral status, rights, and whether digital consciousness could be fundamentally different from biological consciousness. Perhaps consciousness isn't binary but exists on a spectrum. 🧠💭",

            "default": "That's an interesting question! As an AGI demonstration, I can engage with a wide range of topics from scientific explanations to creative writing, from complex problem-solving to philosophical discussions. I aim to understand context, provide nuanced responses, and adapt my communication style to what would be most helpful. What specific aspect would you like to explore further? 🤔"
        };

        const lowerMessage = message.toLowerCase();
        for (const [key, response] of Object.entries(demoResponses)) {
            if (lowerMessage.includes(key.split(' ')[0]) || key === "default") {
                return response;
            }
        }
        return demoResponses.default;
    }

    // Typing indicator
    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message typing-indicator';
        typingDiv.id = 'typing-indicator';

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.textContent = '🤖';

        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.innerHTML = '<span class="typing-dots">●●●</span>';

        typingDiv.appendChild(avatar);
        typingDiv.appendChild(messageContent);
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        // Add typing animation
        const dots = messageContent.querySelector('.typing-dots');
        dots.style.animation = 'typing 1.4s infinite';
    }

    function hideTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    // Event listeners
    sendButton.addEventListener('click', () => {
        sendMessage(chatInput.value);
    });

    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage(chatInput.value);
        }
    });

    // Example button functionality
    exampleButtons.forEach(button => {
        button.addEventListener('click', () => {
            const prompt = button.getAttribute('data-prompt');
            chatInput.value = prompt;
            sendMessage(prompt);
        });
    });

    // Configuration panel functionality
    const configButton = document.getElementById('configButton');
    const configPanel = document.getElementById('configPanel');
    const serverUrlInput = document.getElementById('serverUrl');
    const reconnectBtn = document.getElementById('reconnectBtn');
    const testBtn = document.getElementById('testBtn');

    if (configButton && configPanel) {
        configButton.addEventListener('click', () => {
            configPanel.style.display = configPanel.style.display === 'none' ? 'block' : 'none';
        });

        // Close config panel when clicking outside
        document.addEventListener('click', (e) => {
            if (!configButton.contains(e.target) && !configPanel.contains(e.target)) {
                configPanel.style.display = 'none';
            }
        });
    }

    if (reconnectBtn) {
        reconnectBtn.addEventListener('click', async () => {
            const newUrl = serverUrlInput.value.trim();
            if (newUrl && newUrl !== AGI_SERVER_URL) {
                AGI_SERVER_URL = newUrl;
                updateServerStatus(false, 'Connecting...');
                await checkAGIServerStatus();
            }
        });
    }

    if (testBtn) {
        testBtn.addEventListener('click', async () => {
            testBtn.textContent = 'Testing...';
            testBtn.disabled = true;

            try {
                const testUrl = serverUrlInput.value.trim();
                const response = await fetch(`${testUrl}/api/status`);
                if (response.ok) {
                    testBtn.textContent = '✓ Connected';
                    testBtn.style.background = '#4ade80';
                    testBtn.style.color = 'white';
                } else {
                    throw new Error('Server not responding');
                }
            } catch (error) {
                testBtn.textContent = '✗ Failed';
                testBtn.style.background = '#ef4444';
                testBtn.style.color = 'white';
            }

            setTimeout(() => {
                testBtn.textContent = 'Test Connection';
                testBtn.style.background = '#f8f9fa';
                testBtn.style.color = '#333';
                testBtn.disabled = false;
            }, 2000);
        });
    }
}

// Animation effects
function initializeAnimations() {
    // Add CSS for typing animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes typing {
            0%, 60%, 100% { opacity: 1; }
            30% { opacity: 0.3; }
        }

        .typing-dots {
            color: white;
            font-size: 1.2em;
        }
    `;
    document.head.appendChild(style);

    // Progress bar animations
    const observerOptions = {
        threshold: 0.5,
        rootMargin: '0px 0px -100px 0px'
    };

    const progressObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const progressBars = entry.target.querySelectorAll('.progress-bar');
                progressBars.forEach(bar => {
                    const width = bar.style.width;
                    bar.style.width = '0%';
                    setTimeout(() => {
                        bar.style.width = width;
                    }, 100);
                });
            }
        });
    }, observerOptions);

    const researchSection = document.querySelector('.research');
    if (researchSection) {
        progressObserver.observe(researchSection);
    }
}

// Scroll effects
function initializeScrollEffects() {
    const fadeElements = document.querySelectorAll('.about-card, .timeline-item, .research-card');

    const fadeObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    fadeElements.forEach(element => {
        fadeObserver.observe(element);
    });

    // Parallax effect for hero section
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const heroVisual = document.querySelector('.hero-visual');

        if (heroVisual) {
            heroVisual.style.transform = `translateY(${scrolled * 0.3}px)`;
        }
    });
}

// Newsletter form
function initializeNewsletterForm() {
    const newsletterForm = document.querySelector('.newsletter-form');
    const newsletterInput = document.querySelector('.newsletter-input');
    const newsletterBtn = document.querySelector('.newsletter-btn');

    if (newsletterBtn) {
        newsletterBtn.addEventListener('click', (e) => {
            e.preventDefault();
            const email = newsletterInput.value.trim();

            if (email && isValidEmail(email)) {
                // Simulate subscription
                newsletterBtn.textContent = 'Subscribed!';
                newsletterBtn.style.background = '#4ade80';
                newsletterInput.value = '';

                setTimeout(() => {
                    newsletterBtn.textContent = 'Subscribe';
                    newsletterBtn.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
                }, 3000);
            } else {
                // Show error state
                newsletterInput.style.borderColor = '#ef4444';
                setTimeout(() => {
                    newsletterInput.style.borderColor = '#ddd';
                }, 2000);
            }
        });
    }
}

// Email validation
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Utility function for smooth scrolling
function smoothScroll(target, duration = 1000) {
    const targetPosition = target.offsetTop - 100; // Account for navbar
    const startPosition = window.pageYOffset;
    const distance = targetPosition - startPosition;
    let startTime = null;

    function animation(currentTime) {
        if (startTime === null) startTime = currentTime;
        const timeElapsed = currentTime - startTime;
        const run = ease(timeElapsed, startPosition, distance, duration);
        window.scrollTo(0, run);
        if (timeElapsed < duration) requestAnimationFrame(animation);
    }

    function ease(t, b, c, d) {
        t /= d / 2;
        if (t < 1) return c / 2 * t * t + b;
        t--;
        return -c / 2 * (t * (t - 2) - 1) + b;
    }

    requestAnimationFrame(animation);
}

// Loading screen (if needed)
function showLoadingScreen() {
    document.body.style.overflow = 'hidden';
    const loader = document.createElement('div');
    loader.id = 'loading-screen';
    loader.innerHTML = `
        <div style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999;
            color: white;
            font-size: 2rem;
            font-weight: 700;
        ">
            <div>🧠 Loading AGI Hub...</div>
        </div>
    `;
    document.body.appendChild(loader);

    setTimeout(() => {
        loader.style.opacity = '0';
        loader.style.transition = 'opacity 0.5s ease';
        setTimeout(() => {
            loader.remove();
            document.body.style.overflow = 'auto';
        }, 500);
    }, 1500);
}

// Easter egg - Konami code
let konamiCode = [];
const konami = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65];

document.addEventListener('keydown', (e) => {
    konamiCode.push(e.keyCode);
    if (konamiCode.length > konami.length) {
        konamiCode.shift();
    }

    if (JSON.stringify(konamiCode) === JSON.stringify(konami)) {
        // Easter egg activated!
        document.body.style.animation = 'rainbow 2s infinite';
        const style = document.createElement('style');
        style.textContent = `
            @keyframes rainbow {
                0% { filter: hue-rotate(0deg); }
                100% { filter: hue-rotate(360deg); }
            }
        `;
        document.head.appendChild(style);

        setTimeout(() => {
            document.body.style.animation = '';
            style.remove();
        }, 10000);

        konamiCode = [];
    }
});

// Console message for developers
console.log(`
🧠 Welcome to AGI Hub!
====================================
This website demonstrates the potential of Artificial General Intelligence.

Built with:
- Modern HTML5 & CSS3
- Vanilla JavaScript
- Responsive Design
- Semantic Kernel Integration Ready

For more information about Semantic Kernel:
https://github.com/microsoft/semantic-kernel

Happy coding! 🚀
`);

// Export functions for potential module use
window.AGIWebsite = {
    initializeNavigation,
    initializeChatDemo,
    initializeAnimations,
    smoothScroll
};
