# Stage 1: Build the Chat UI
FROM node:20-slim AS chatui-builder

# Set the working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm ci

# Copy the rest of the source code and build the chat UI
COPY . .
RUN npm run build

# Stage 2: Base Image for Final Application
FROM python:3.9-slim

# Set up a non-root user for security
RUN useradd -m -u 1000 user
USER user

# Set working directory
WORKDIR /app

# Set environment variables
ENV PATH="/home/user/.local/bin:$PATH"

# Copy Python dependencies and install them
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy built files from the Chat UI build stage
COPY --from=chatui-builder /app/build /app/build

# Copy application source code and configuration files
COPY --chown=user . .
COPY .env /app/.env
COPY config.json /app/config.json

# Set permissions for the entrypoint script and add it
RUN chmod +x entrypoint.sh
COPY entrypoint.sh .

# Add a health check for the application
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl --fail http://localhost:3000 || exit 1

# Expose the application port
EXPOSE 3000

# Final command to start the application
ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
