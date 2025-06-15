# Multi-stage Docker build for AI Workspace
# Optimized for production use with Semantic Kernel and AI development

# =============================================================================
# Stage 1: Base Dependencies
# =============================================================================
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    nodejs \
    npm \
    supervisor \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# =============================================================================
# Stage 2: Python Dependencies
# =============================================================================
FROM base as python-deps

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install Python dependencies
COPY requirements.txt /tmp/
RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt

# =============================================================================
# Stage 3: Application Build
# =============================================================================
FROM python-deps as app-build

# Set working directory
WORKDIR /app

# Copy the organized workspace
COPY . /app/

# Create necessary directories
RUN mkdir -p /app/logs /app/data /app/uploads /app/models \
    && chmod +x /app/scripts/*.sh || true \
    && chmod +x /app/*.sh

# =============================================================================
# Stage 4: Production Runtime
# =============================================================================
FROM python-deps as runtime

# Create non-root user
RUN groupadd -r aiuser && useradd -r -g aiuser aiuser

# Set working directory
WORKDIR /app

# Copy application from build stage
COPY --from=app-build --chown=aiuser:aiuser /app /app

# Copy virtual environment
COPY --from=python-deps /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create configuration files
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY docker/nginx.conf /etc/nginx/sites-available/default
COPY docker/entrypoint.sh /usr/local/bin/entrypoint.sh

# Make scripts executable
RUN chmod +x /usr/local/bin/entrypoint.sh

# Expose ports
EXPOSE 8000 8888 3000 80

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Switch to non-root user
USER aiuser

# Set entrypoint
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
