# Stage 1: Build the Chat UI
FROM node:20.10.0-slim AS chatui-builder

ARG MODEL_NAME="mistralai/Mixtral-8x7B-Instruct-v0.1"
ARG MODEL_PARAMS='{"temperature":0.7,"max_new_tokens":1024,"repetition_penalty":1.1}'
ARG MODEL_PROMPT_TEMPLATE="<s>[INST] {{ prompt }} [/INST]"
ARG APP_COLOR="#1D4ED8"
ARG APP_NAME="Mixtral-8x7B Chat"

WORKDIR /app

# Install minimal dependencies, clean up to reduce image size
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    git gettext ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN git clone --depth 1 https://github.com/huggingface/chat-ui.git

WORKDIR /app/chat-ui
COPY .env.local.template .env.local.template

# Copy and set correct permissions for defaults directory
RUN mkdir -p /defaults
COPY defaults /defaults
RUN chmod -R 755 /defaults

# Expand environment variables into .env.local using envsubst
RUN MODEL_NAME="${MODEL_NAME:="$(cat /defaults/MODEL_NAME 2>/dev/null || echo "mistralai/Mixtral-8x7B-Instruct-v0.1")"}" && \
    MODEL_PARAMS="${MODEL_PARAMS:="$(cat /defaults/MODEL_PARAMS 2>/dev/null || echo '{\"temperature\":0.7,\"max_new_tokens\":1024,\"repetition_penalty\":1.1}')"}" && \
    MODEL_PROMPT_TEMPLATE="${MODEL_PROMPT_TEMPLATE:="$(cat /defaults/MODEL_PROMPT_TEMPLATE 2>/dev/null || echo "<s>[INST] {{ prompt }} [/INST]")"}" && \
    APP_COLOR="${APP_COLOR:="$(cat /defaults/APP_COLOR 2>/dev/null || echo "#1D4ED8")"}" && \
    APP_NAME="${APP_NAME:="$(cat /defaults/APP_NAME 2>/dev/null || echo "Mixtral-8x7B Chat")"}" && \
    export MODEL_NAME MODEL_PARAMS MODEL_PROMPT_TEMPLATE APP_COLOR APP_NAME && \
    envsubst < ".env.local.template" > ".env.local" && rm -f .env.local.template

# Use cache for npm, install dependencies, and build
RUN --mount=type=cache,target=/app/.npm \
    npm set cache /app/.npm && \
    npm ci --production && \
    npm run build

# Stage 2: Final Application Image
FROM ghcr.io/huggingface/text-generation-inference:v1.2.3

LABEL maintainer="your-email@example.com"
LABEL org.opencontainers.image.source="https://github.com/Bryan-Roe-ai/semantic-kernel"
LABEL com.microsoft.azure.container="true"
LABEL org.opencontainers.image.vendor="Microsoft"
LABEL org.opencontainers.image.title="HuggingFace Chat UI"
LABEL org.opencontainers.image.description="Chat UI with Text Generation Inference for Azure"

ARG MODEL_NAME
ARG MODEL_PARAMS
ARG MODEL_PROMPT_TEMPLATE
ARG APP_COLOR
ARG APP_NAME

ENV TZ=UTC \
    PORT=3000 \
    NODE_ENV=production

# Install only necessary system packages, then clean up
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    gnupg curl gettext ca-certificates libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh.template entrypoint.sh.template

# Copy and set correct permissions for defaults directory
RUN mkdir -p /defaults
COPY defaults /defaults
RUN chmod -R 755 /defaults

# Expand environment variables into entrypoint.sh using envsubst
RUN MODEL_NAME="${MODEL_NAME:="$(cat /defaults/MODEL_NAME 2>/dev/null || echo "mistralai/Mixtral-8x7B-Instruct-v0.1")"}" && \
    MODEL_PARAMS="${MODEL_PARAMS:="$(cat /defaults/MODEL_PARAMS 2>/dev/null || echo '{\"temperature\":0.7,\"max_new_tokens\":1024,\"repetition_penalty\":1.1}')"}" && \
    MODEL_PROMPT_TEMPLATE="${MODEL_PROMPT_TEMPLATE:="$(cat /defaults/MODEL_PROMPT_TEMPLATE 2>/dev/null || echo "<s>[INST] {{ prompt }} [/INST]")"}" && \
    APP_COLOR="${APP_COLOR:="$(cat /defaults/APP_COLOR 2>/dev/null || echo "#1D4ED8")"}" && \
    APP_NAME="${APP_NAME:="$(cat /defaults/APP_NAME 2>/dev/null || echo "Mixtral-8x7B Chat")"}" && \
    export MODEL_NAME MODEL_PARAMS MODEL_PROMPT_TEMPLATE APP_COLOR APP_NAME && \
    envsubst < "entrypoint.sh.template" > "entrypoint.sh" && chmod +x entrypoint.sh && rm -f entrypoint.sh.template

# MongoDB installation (with secure key handling)
RUN curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | gpg --dearmor -o /usr/share/keyrings/mongodb-server-7.0.gpg && \
    echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-7.0.list && \
    apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends mongodb-org && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Node.js installation (only runtime, not build tools)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Security: non-root user for all app processes, correct ownership
RUN useradd -m -u 1000 -s /bin/bash user
USER user

ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR /app

# Install PM2 globally for the user
RUN npm config set prefix /home/user/.local && npm install -g pm2

# Copy built application from builder stage, set correct ownership
COPY --from=chatui-builder --chown=1000:1000 /app/chat-ui/build /app/build
COPY --from=chatui-builder --chown=1000:1000 /app/chat-ui/node_modules /app/node_modules
COPY --from=chatui-builder --chown=1000:1000 /app/chat-ui/package.json /app/package.json

# Copy configuration and environment files
COPY --chown=1000:1000 .env /app/.env
COPY --chown=1000:1000 config.json /app/config.json

# Healthcheck for container
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:${PORT:-3000}/ || (echo 'Healthcheck failed' && exit 1)

# Entrypoint
ENTRYPOINT ["/bin/bash"]
CMD ["entrypoint.sh"]
