#!/usr/bin/env node

const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const PORT = process.env.PORT || 8000;

// MIME types for different file extensions
const mimeTypes = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon',
    '.woff': 'font/woff',
    '.woff2': 'font/woff2',
    '.ttf': 'font/ttf',
    '.eot': 'font/eot'
};

// Create HTTP server
const server = http.createServer((req, res) => {
    // Parse URL
    const parsedUrl = url.parse(req.url);
    let pathname = parsedUrl.pathname;

    // Default to index.html for root path
    if (pathname === '/') {
        pathname = '/index.html';
    }

    // Construct file path
    const filePath = path.join(__dirname, pathname);

    // Check if file exists
    fs.access(filePath, fs.constants.F_OK, (err) => {
        if (err) {
            // File not found
            res.writeHead(404, { 'Content-Type': 'text/html' });
            res.end(`
                <!DOCTYPE html>
                <html>
                <head>
                    <title>404 - Page Not Found</title>
                    <style>
                        body {
                            font-family: 'Inter', sans-serif;
                            text-align: center;
                            padding: 50px;
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            color: white;
                            min-height: 100vh;
                            margin: 0;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            flex-direction: column;
                        }
                        h1 { font-size: 4rem; margin-bottom: 1rem; }
                        p { font-size: 1.2rem; margin-bottom: 2rem; }
                        a {
                            color: white;
                            text-decoration: none;
                            padding: 1rem 2rem;
                            border: 2px solid white;
                            border-radius: 50px;
                            transition: all 0.3s ease;
                        }
                        a:hover {
                            background: white;
                            color: #667eea;
                        }
                    </style>
                </head>
                <body>
                    <h1>🤖 404</h1>
                    <p>Oops! This page seems to have achieved AGI and disappeared.</p>
                    <a href="/">← Back to AGI Hub</a>
                </body>
                </html>
            `);
            return;
        }

        // Read file
        fs.readFile(filePath, (err, data) => {
            if (err) {
                res.writeHead(500, { 'Content-Type': 'text/plain' });
                res.end('Internal Server Error');
                return;
            }

            // Get file extension and set content type
            const ext = path.extname(filePath).toLowerCase();
            const contentType = mimeTypes[ext] || 'application/octet-stream';

            // Set headers
            res.writeHead(200, {
                'Content-Type': contentType,
                'Cache-Control': 'public, max-age=3600', // Cache for 1 hour
                'X-Powered-By': 'AGI Hub Server'
            });

            // Send file content
            res.end(data);
        });
    });
});

// Start server
server.listen(PORT, () => {
    console.log(`
🧠 AGI Website Server Started!
================================
🌐 Server running at: http://localhost:${PORT}
📁 Serving files from: ${__dirname}
🚀 Ready to demonstrate AGI capabilities!

Press Ctrl+C to stop the server.
    `);
});

// Handle server shutdown gracefully
process.on('SIGINT', () => {
    console.log('\n\n🛑 Server shutting down gracefully...');
    server.close(() => {
        console.log('✅ Server stopped. Thanks for exploring AGI!');
        process.exit(0);
    });
});

// Handle uncaught exceptions with better logging
process.on('uncaughtException', (err) => {
    console.error('❌ Uncaught Exception Details:');
    console.error('  Message:', err.message);
    console.error('  Stack:', err.stack);
    console.error('  Time:', new Date().toISOString());

    // Log to file if possible
    const errorLog = `[${new Date().toISOString()}] Uncaught Exception: ${err.message}\nStack: ${err.stack}\n\n`;
    fs.appendFile('error.log', errorLog, (writeErr) => {
        if (writeErr) console.error('Failed to write to error log:', writeErr);
    });

    // Graceful shutdown
    console.log('🔄 Attempting graceful shutdown...');
    server.close(() => {
        console.log('💀 Server closed due to uncaught exception');
        process.exit(1);
    });

    // Force exit after 10 seconds if graceful shutdown fails
    setTimeout(() => {
        console.error('💥 Force exiting after timeout');
        process.exit(1);
    }, 10000);
});

process.on('unhandledRejection', (reason, promise) => {
    console.error('❌ Unhandled Promise Rejection Details:');
    console.error('  Promise:', promise);
    console.error('  Reason:', reason);
    console.error('  Time:', new Date().toISOString());

    // Log to file if possible
    const errorLog = `[${new Date().toISOString()}] Unhandled Rejection: ${reason}\nPromise: ${promise}\n\n`;
    fs.appendFile('error.log', errorLog, (writeErr) => {
        if (writeErr) console.error('Failed to write to error log:', writeErr);
    });

    // For now, just log it but don't exit (more forgiving for development)
    console.log('⚠️  Application will continue running despite unhandled promise rejection');
});

// Handle SIGTERM for better container support
process.on('SIGTERM', () => {
    console.log('\n\n🔄 Received SIGTERM, shutting down gracefully...');
    server.close(() => {
        console.log('✅ Server stopped gracefully');
        process.exit(0);
    });
});

// Monitor server health
let connectionCount = 0;

server.on('connection', (socket) => {
    connectionCount++;
    console.log(`📈 New connection established. Total connections: ${connectionCount}`);

    socket.on('close', () => {
        connectionCount--;
        console.log(`📉 Connection closed. Total connections: ${connectionCount}`);
    });
});

// Log server errors
server.on('error', (err) => {
    console.error('🚨 Server Error:', err.message);

    if (err.code === 'EADDRINUSE') {
        console.error(`💥 Port ${PORT} is already in use. Please choose a different port or stop the existing process.`);
        process.exit(1);
    }

    if (err.code === 'EACCES') {
        console.error(`🔒 Permission denied. You may need elevated privileges to bind to port ${PORT}.`);
        process.exit(1);
    }
});

// Add request logging middleware
const originalCreateServer = server.listeners('request')[0];
server.removeAllListeners('request');

server.on('request', (req, res) => {
    const startTime = Date.now();
    const clientIP = req.connection.remoteAddress || req.socket.remoteAddress;

    console.log(`📝 ${new Date().toISOString()} - ${req.method} ${req.url} from ${clientIP}`);

    // Override res.end to log response details
    const originalEnd = res.end;
    res.end = function (...args) {
        const duration = Date.now() - startTime;
        console.log(`✅ ${req.method} ${req.url} - ${res.statusCode} (${duration}ms)`);
        originalEnd.apply(this, args);
    };

    // Call the original request handler
    originalCreateServer(req, res);
});
