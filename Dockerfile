# Semantic Kernel Development Container
# Based on Microsoft Universal DevContainer with additional tools

FROM mcr.microsoft.com/devcontainers/universal:2-linux

# Set environment variables
ENV DOTNET_CLI_TELEMETRY_OPTOUT=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Switch to root for installation
USER root

# Install additional dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    gnupg \
    software-properties-common \
    apt-transport-https \
    ca-certificates \
    lsb-release \
    && rm -rf /var/lib/apt/lists/*

# Install .NET 8.0 (ensure latest version)
RUN wget https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/packages-microsoft-prod.deb -O packages-microsoft-prod.deb \
    && dpkg -i packages-microsoft-prod.deb \
    && rm packages-microsoft-prod.deb \
    && apt-get update \
    && apt-get install -y dotnet-sdk-8.0 \
    && rm -rf /var/lib/apt/lists/*

# Install Azure Functions Core Tools
RUN wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | apt-key add - \
    && echo "deb [arch=amd64] https://packages.microsoft.com/repos/microsoft-ubuntu-$(lsb_release -cs)-prod $(lsb_release -cs) main" > /etc/apt/sources.list.d/dotnetdev.list \
    && apt-get update \
    && apt-get install -y azure-functions-core-tools-4 \
    && rm -rf /var/lib/apt/lists/*

# Install Python 3.12 and pip
RUN add-apt-repository ppa:deadsnakes/ppa -y \
    && apt-get update \
    && apt-get install -y python3.12 python3.12-dev python3.12-venv python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js (latest LTS)
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install MongoDB (for development/testing)
RUN curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | gpg --dearmor -o /usr/share/keyrings/mongodb-server-7.0.gpg \
    && echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-7.0.list \
    && apt-get update \
    && apt-get install -y mongodb-org \
    && rm -rf /var/lib/apt/lists/*

# Install additional development tools
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    vim \
    nano \
    jq \
    unzip \
    zip \
    tree \
    htop \
    && rm -rf /var/lib/apt/lists/*

# Set proper ownership for dotnet
RUN chown -R vscode:vscode /usr/share/dotnet \
    && chmod -R ug+rwX /usr/share/dotnet

# Switch back to vscode user
USER vscode

# Set working directory
WORKDIR /workspaces/semantic-kernel

# Copy requirements and install Python packages
COPY --chown=vscode:vscode python/pyproject.toml python/poetry.lock* ./python/
COPY --chown=vscode:vscode requirements*.txt ./

# Install Python dependencies
RUN python3.12 -m pip install --user --upgrade pip \
    && python3.12 -m pip install --user poetry \
    && if [ -f requirements.txt ]; then python3.12 -m pip install --user -r requirements.txt; fi

# Install .NET workloads (with error handling)
RUN dotnet workload restore || echo "Workload restore failed, continuing..."

# Expose common ports
EXPOSE 3000 5000 7071 8000 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/ || exit 1

# Default command
CMD ["/bin/bash"]
