const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const expressRateLimit = require('express-rate-limit');
const expressCompression = require('compression');
const morgan = require('morgan');
require('dotenv').config();

// Create Express app
const app = express();

// Trust proxy if behind reverse proxy
app.set('trust proxy', 1);

// Configure security middleware
app.use(helmet({
  contentSecurityPolicy: true,
  crossOriginEmbedderPolicy: true
}));

// Configure CORS
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || '*',
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

// Configure compression
app.use(expressCompression());

// Configure request logging
app.use(morgan('combined'));

// Configure rate limiting
const limiter = expressRateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  standardHeaders: true,
  legacyHeaders: false,
  message: 'Too many requests from this IP, please try again later'
});

// Apply the rate limiting middleware to all requests
app.use(limiter);

// Parse JSON payloads
app.use(express.json({ limit: '10kb' }));

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'healthy' });
});

// Handle 404 errors
app.use((req, res, next) => {
  res.status(404).json({ error: 'Not Found' });
});

// Global error handler
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    status: 'error',
    message: process.env.NODE_ENV === 'production' ? 'Internal server error' : err.message
  });
});

// Configure port
const PORT = process.env.PORT || 3000;

// Start server with graceful shutdown
const server = app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

// Graceful shutdown handling
const gracefulShutdown = () => {
  console.log('Received kill signal, shutting down gracefully.');
  server.close(() => {
    console.log('Closed out remaining connections.');
    process.exit(0);
  });

  // Force close server after 10 seconds
  setTimeout(() => {
    console.error('Could not close connections in time, forcefully shutting down');
    process.exit(1);
  }, 10000);
};

// Listen for termination signals
process.on('SIGTERM', gracefulShutdown);
process.on('SIGINT', gracefulShutdown);

module.exports = app;