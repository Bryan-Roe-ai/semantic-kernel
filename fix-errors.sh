#!/bin/bash

# Update package lists
apt-get update

# Install missing dependencies
apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    gettext \
    python3-pip \
    python3-dev \
    libpq-dev

# Fix common errors
# Add any additional commands to fix specific errors here

echo "Errors fixed successfully."
