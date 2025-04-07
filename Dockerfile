# Stage 1: Build the chat UI
FROM node:20 AS chatui-builder

ARG MODEL_NAME
ARG MODEL_PARAMS
ARG APP_COLOR
ARG APP_NAME
ARG MODEL_PROMPT_TEMPLATE

WORKDIR /app

# Install dependencies
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends git gettext && \
    rm -rf /var/lib/apt/lists/*

# Clone the chat-ui repository
RUN git clone https://github.com/huggingface/chat-ui.git

WORKDIR /app/chat-ui

COPY .env.local.template .env.local.template
RUN mkdir defaults && \
    ADD defaults /defaults && \
    chmod -R 777 /defaults

# Set environment variables and generate .env.local
RUN --mount=type=secret,id=MONGODB_URL,mode=0444 \
    export MODEL_NAME="${MODEL_NAME:="$(cat /defaults/MODEL_NAME)"}" && \
    export MODEL_PARAMS="${MODEL_PARAMS:="$(cat /defaults/MODEL_PARAMS)"}" && \
    export MODEL_PROMPT_TEMPLATE="${MODEL_PROMPT_TEMPLATE:="$(cat /defaults/MODEL_PROMPT_TEMPLATE)"}" && \
    export APP_COLOR="${APP_COLOR:="$(cat /defaults/APP_COLOR)"}" && \
    export APP_NAME="${APP_NAME:="$(cat /defaults/APP_NAME)"}" && \
    export MONGODB_URL=$(cat /run/secrets/MONGODB_URL || cat /defaults/MONGODB_URL) && \
    envsubst < ".env.local.template" > ".env.local" && \
    rm .env.local.template

RUN --mount=type=cache,target=/app/.npm \
    npm set cache /app/.npm && \
    npm ci && \
    npm run build

# Stage 2: Final image
FROM ghcr.io/huggingface/text-generation-inference:latest

ARG MODEL_NAME
ARG MODEL_PARAMS
ARG MODEL_PROMPT_TEMPLATE
ARG APP_COLOR
ARG APP_NAME

ENV TZ=Europe/Paris \
    PORT=3000

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends gnupg curl gettext && \
    rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh.template entrypoint.sh.template
RUN mkdir defaults && \
    ADD defaults /defaults && \
    chmod -R 777 /defaults

# Set environment variables and generate entrypoint.sh
RUN --mount=type=secret,id=MONGODB_URL,mode=0444 \
    export MODEL_NAME="${MODEL_NAME:="$(cat /defaults/MODEL_NAME)"}" && \
    export MODEL_PARAMS="${MODEL_PARAMS:="$(cat /defaults/MODEL_PARAMS)"}" && \
    export MODEL_PROMPT_TEMPLATE="${MODEL_PROMPT_TEMPLATE:="$(cat /defaults/MODEL_PROMPT_TEMPLATE)"}" && \
    export APP_COLOR="${APP_COLOR:="$(cat /defaults/APP_COLOR)"}" && \
    export APP_NAME="${APP_NAME:="$(cat /defaults/APP_NAME)"}" && \
    export MONGODB_URL=$(cat /run/secrets/MONGODB_URL || cat /defaults/MONGODB_URL) && \
    envsubst < "entrypoint.sh.template" > "entrypoint.sh" && \
    rm entrypoint.sh.template

RUN curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | gpg --dearmor -o /usr/share/keyrings/mongodb-server-7.0.gpg && \
    echo "deb [arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-7.0.list && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends mongodb-org && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /data/db && \
    chown -R 1000:1000 /data && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | /bin/bash - && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends nodejs && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /app && \
    chown -R 1000:1000 /app && \
    useradd -m -u 1000 user

USER user

ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

RUN npm config set prefix /home/user/.local && npm install -g pm2

COPY --from=chatui-builder --chown=1000 /app/chat-ui/node_modules /app/node_modules
COPY --from=chatui-builder --chown=1000 /app/chat-ui/package.json /app/package.json
COPY --from=chatui-builder --chown=1000 /app/chat-ui/build /app/build

ENTRYPOINT ["/bin/bash"]
CMD ["entrypoint.sh"]
