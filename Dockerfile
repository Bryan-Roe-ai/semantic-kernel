# Docker image for Hugging Face chat UI with text generation inference
# Optimized for Azure deployments

# Define ARG variables with default values for better configurability
ARG MODEL_NAME="mistralai/Mixtral-8x7B-Instruct-v0.1"
ARG MODEL_PARAMS='{"temperature":0.7,"max_new_tokens":1024,"repetition_penalty":1.1}'
ARG MODEL_PROMPT_TEMPLATE="<s>[INST] {{ prompt }} [/INST]"
ARG APP_COLOR="#1D4ED8"
ARG APP_NAME="Mixtral-8x7B Chat"

# First stage: Build the chat UI
FROM node:20-slim as chatui-builder
ARG MODEL_NAME
ARG MODEL_PARAMS
ARG APP_COLOR
ARG APP_NAME
ARG MODEL_PROMPT_TEMPLATE

WORKDIR /app

# Use --no-install-recommends to reduce image size and limit attack surface
# Combine RUN commands to reduce layers and clear cache in the same layer
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    git \
    gettext \
    ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    git clone --depth 1 https://github.com/huggingface/chat-ui.git

WORKDIR /app/chat-ui

COPY .env.local.template .env.local.template

# Set up defaults directory with proper permissions
RUN mkdir -p /defaults
COPY defaults /defaults
RUN chmod -R 755 /defaults

# Use multi-stage secrets management with fallbacks
# Setting environment variables in one layer reduces image size
RUN --mount=type=secret,id=MONGODB_URL,mode=0400 \
    MODEL_NAME="${MODEL_NAME:="$(cat /defaults/MODEL_NAME 2>/dev/null || echo "mistralai/Mixtral-8x7B-Instruct-v0.1")"}" && export MODEL_NAME && \
    MODEL_PARAMS="${MODEL_PARAMS:="$(cat /defaults/MODEL_PARAMS 2>/dev/null || echo '{\"temperature\":0.7,\"max_new_tokens\":1024,\"repetition_penalty\":1.1}')"}" && export MODEL_PARAMS && \
    MODEL_PROMPT_TEMPLATE="${MODEL_PROMPT_TEMPLATE:="$(cat /defaults/MODEL_PROMPT_TEMPLATE 2>/dev/null || echo "<s>[INST] {{ prompt }} [/INST]")"}" && export MODEL_PROMPT_TEMPLATE && \
    APP_COLOR="${APP_COLOR:="$(cat /defaults/APP_COLOR 2>/dev/null || echo "#1D4ED8")"}" && export APP_COLOR && \
    APP_NAME="${APP_NAME:="$(cat /defaults/APP_NAME 2>/dev/null || echo "Mixtral-8x7B Chat")"}" && export APP_NAME && \
    MONGODB_URL="$(cat /run/secrets/MONGODB_URL 2>/dev/null || cat /defaults/MONGODB_URL 2>/dev/null || echo "mongodb://localhost:27017/chatui")" && export MONGODB_URL && \
    envsubst < ".env.local.template" > ".env.local" && \
    rm -f .env.local.template

# Use cache mounting for npm to speed up builds
RUN --mount=type=cache,target=/app/.npm \
    npm set cache /app/.npm && \
    npm ci --production && \
    npm run build

# Final stage: Create the application image
FROM ghcr.io/huggingface/text-generation-inference:latest

ARG MODEL_NAME
ARG MODEL_PARAMS
ARG MODEL_PROMPT_TEMPLATE
ARG APP_COLOR
ARG APP_NAME

ENV TZ=UTC \
    PORT=3000 \
    NODE_ENV=production

# Install only necessary packages
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    gnupg \
    curl \
    gettext \
    ca-certificates \
    libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh.template entrypoint.sh.template

# Set up defaults directory with proper permissions
RUN mkdir -p /defaults
COPY defaults /defaults
RUN chmod -R 755 /defaults

# Use multi-stage secrets management with fallbacks
RUN --mount=type=secret,id=MONGODB_URL,mode=0400 \
    MODEL_NAME="${MODEL_NAME:="$(cat /defaults/MODEL_NAME 2>/dev/null || echo "mistralai/Mixtral-8x7B-Instruct-v0.1")"}" && export MODEL_NAME && \
    MODEL_PARAMS="${MODEL_PARAMS:="$(cat /defaults/MODEL_PARAMS 2>/dev/null || echo '{\"temperature\":0.7,\"max_new_tokens\":1024,\"repetition_penalty\":1.1}')"}" && export MODEL_PARAMS && \
    MODEL_PROMPT_TEMPLATE="${MODEL_PROMPT_TEMPLATE:="$(cat /defaults/MODEL_PROMPT_TEMPLATE 2>/dev/null || echo "<s>[INST] {{ prompt }} [/INST]")"}" && export MODEL_PROMPT_TEMPLATE && \
    APP_COLOR="${APP_COLOR:="$(cat /defaults/APP_COLOR 2>/dev/null || echo "#1D4ED8")"}" && export APP_COLOR && \
    APP_NAME="${APP_NAME:="$(cat /defaults/APP_NAME 2>/dev/null || echo "Mixtral-8x7B Chat")"}" && export APP_NAME && \
    MONGODB_URL="$(cat /run/secrets/MONGODB_URL 2>/dev/null || cat /defaults/MONGODB_URL 2>/dev/null || echo "mongodb://localhost:27017/chatui")" && export MONGODB_URL && \
    envsubst < "entrypoint.sh.template" > "entrypoint.sh" && \
    chmod +x entrypoint.sh && \
    rm -f entrypoint.sh.template

# Add MongoDB repository and install MongoDB using best practices
RUN curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
    gpg --dearmor -o /usr/share/keyrings/mongodb-server-7.0.gpg

RUN echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | \
    tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Install MongoDB and Node.js in a single layer to reduce image size
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    mongodb-org \
    nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create directories with appropriate permissions
RUN mkdir -p /data/db /app && \
    chown -R 1000:1000 /data /app

# Create non-root user for security
RUN useradd -m -u 1000 -s /bin/bash user

# Switch to the "user" user (non-root for security)
USER user

# Set environment variables for the user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Install PM2 globally for the user
RUN npm config set prefix /home/user/.local && \
    npm install -g pm2

# Copy application files from builder stage
COPY --from=chatui-builder --chown=1000:1000 /app/chat-ui/build /app/build
COPY --from=chatui-builder --chown=1000:1000 /app/chat-ui/node_modules /app/node_modules
COPY --from=chatui-builder --chown=1000:1000 /app/chat-ui/package.json /app/package.json

# Copy configuration files
COPY --chown=1000:1000 .env /app/.env
COPY --chown=1000:1000 config.json /app/config.json

# Set working directory
WORKDIR /app

# Healthcheck to ensure container is running properly
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:${PORT:-3000}/ || exit 1

# Set the entrypoint and default command
ENTRYPOINT ["/bin/bash"]
CMD ["entrypoint.sh"]

# Azure-specific labels
LABEL com.microsoft.azure.container="true"
LABEL org.opencontainers.image.vendor="Microsoft"
LABEL org.opencontainers.image.title="HuggingFace Chat UI"
LABEL org.opencontainers.image.description="Chat UI with Text Generation Inference for Azure"
