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

// Handle uncaught exceptions
process.on('uncaughtException', (err) => {
    console.error('❌ Uncaught Exception:', err);
    process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
    console.error('❌ Unhandled Rejection at:', promise, 'reason:', reason);
    process.exit(1);
});
