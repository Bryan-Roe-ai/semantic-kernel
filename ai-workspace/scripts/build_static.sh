#!/bin/bash

# Build script for static site deployment
set -e

echo "🔨 Building AI Workspace static site..."

# Create build directory
DIST_DIR="./dist"
rm -rf $DIST_DIR
mkdir -p $DIST_DIR

# Copy HTML files and resolve symlinks
echo "📁 Copying static files..."
cp 05-samples-demos/*.html $DIST_DIR/
cp 05-samples-demos/README.md $DIST_DIR/

# Copy backend for documentation
echo "🔗 Copying backend services..."
mkdir -p $DIST_DIR/backend
cp -r 06-backend-services/* $DIST_DIR/backend/

# Copy requirements
cp requirements-minimal.txt $DIST_DIR/

# Copy Docker files
cp Dockerfile $DIST_DIR/
cp docker-compose.yml $DIST_DIR/
cp docker-compose.dev.yml $DIST_DIR/ 2>/dev/null || true

# Copy documentation
cp README.md $DIST_DIR/README-workspace.md
cp SUCCESS_SUMMARY.md $DIST_DIR/ 2>/dev/null || true
cp ISSUE_RESOLUTION.md $DIST_DIR/ 2>/dev/null || true

# Create deployment info
echo "ℹ️ Creating deployment info..."
cat > $DIST_DIR/deployment-info.txt << EOF
AI Workspace Deployment
=====================

Build Date: $(date)
Build Host: $(hostname)
Working Directory: $(pwd)

Files included:
$(find $DIST_DIR -type f | sort)
EOF

echo "✅ Build complete! Static site ready in $DIST_DIR"
echo "🌐 Main page: $DIST_DIR/index.html"
echo "🤖 Studio page: $DIST_DIR/custom-llm-studio.html"
