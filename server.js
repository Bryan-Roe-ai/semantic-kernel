const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const expressRateLimit = require('express-rate-limit');
const expressCompression = require('compression');

// Create Express app
const app = express();

// Configure rate limiting
const limiter = expressRateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  standardHeaders: true,
  legacyHeaders: false,
  message: 'Too many requests from this IP, please try again later'
});

// Add middleware
app.use(limiter);
app.use(expressCompression({
  level: 6,
  threshold: 100 * 1024
}));

// Add request logging
app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} ${req.method} ${req.url}`);
  next();
});

// Add request timeout
app.use((req, res, next) => {
  req.setTimeout(5000);
  res.setTimeout(5000);
  next();
});

// Configure middleware with enhanced security
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"],
      styleSrc: ["'self'"],
      imgSrc: ["'self'"]
    }
  },
  crossOriginEmbedderPolicy: true,
  crossOriginOpenerPolicy: true,
  crossOriginResourcePolicy: true,
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true
  }
}));
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || '*',
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));
app.use(express.json({ limit: '1mb' }));
app.use(express.urlencoded({ extended: true, limit: '1mb' }));

// Basic health check route
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'OK' });
});

// Improve error handling middleware
app.use((err, req, res, next) => {
  const statusCode = err.status || 500;
  const message = err.message || 'Internal Server Error';
  console.error(`[Error] ${statusCode}: ${message}\n`, err.stack);
  res.status(statusCode).json({ error: message });
});

// Port configuration
const port = process.env.PORT || 3000;

// Create server instance for graceful shutdown
const server = app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
}).on('error', (err) => {
  console.error('Failed to start server:', err);
  process.exit(1);
});

// Handle graceful shutdown
process.on('SIGTERM', gracefulShutdown);
process.on('SIGINT', gracefulShutdown);

function gracefulShutdown() {
  console.log('Received shutdown signal, closing server...');
  server.close(() => {
    console.log('Server closed');
    process.exit(0);
  });
  
  // Force close after 10s
  setTimeout(() => {
    console.error('Could not close connections in time, forcefully shutting down');
    process.exit(1);
  }, 10000);
}