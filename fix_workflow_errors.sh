#!/bin/sh
# Script to apply workflow fixes

# Set the base directories
WORKFLOW_DIR="/workspaces/semantic-kernel/04-infrastructure/.github/workflows"
DOCKER_DIR="/workspaces/semantic-kernel/08-archived-versions/internal-semantic-core"

# Fix Dockerfile
# Note: Already fixed directly via editor

# Fix workflow files
if [ -f "${WORKFLOW_DIR}/lint.yml.fixed" ]; then
  echo "Applying lint.yml fix..."
  mv "${WORKFLOW_DIR}/lint.yml.fixed" "${WORKFLOW_DIR}/lint.yml"
fi

if [ -f "${WORKFLOW_DIR}/close-inactive-issues.yml.fixed" ]; then
  echo "Applying close-inactive-issues.yml fix..."
  mv "${WORKFLOW_DIR}/close-inactive-issues.yml.fixed" "${WORKFLOW_DIR}/close-inactive-issues.yml"
fi

if [ -f "${WORKFLOW_DIR}/greetings.yml.fixed" ]; then
  echo "Applying greetings.yml fix..."
  mv "${WORKFLOW_DIR}/greetings.yml.fixed" "${WORKFLOW_DIR}/greetings.yml"
fi

echo "Fixes have been applied successfully."
