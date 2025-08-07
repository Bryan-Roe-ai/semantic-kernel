#!/usr/bin/env python3
"""
Quick Development Environment Setup for Semantic Kernel
"""

import subprocess
import sys
import os
from pathlib import Path

class QuickSetup:
    def __init__(self):
        self.python_path = "/workspaces/semantic-kernel/.python/bin/python"
        self.workspace_root = Path("/workspaces/semantic-kernel")

    def install_packages(self):
        """Install essential packages"""
        packages = [
            "jupyter",
            "notebook",
            "ipykernel",
            "fastapi",
            "uvicorn",
            "requests",
            "numpy",
            "pandas",
            "matplotlib",
            "plotly",
            "pydantic",
            "aiofiles",
            "websockets",
            "pytest",
            "black",
            "ruff"
        ]

        print("🔧 Installing essential packages...")
        for package in packages:
            try:
                subprocess.run([
                    self.python_path, "-m", "pip", "install", package
                ], check=True, capture_output=True, text=True)
                print(f"✅ Installed {package}")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install {package}: {e}")

    def setup_jupyter(self):
        """Setup Jupyter kernel"""
        print("🔧 Setting up Jupyter kernel...")
        try:
            subprocess.run([
                self.python_path, "-m", "ipykernel", "install",
                "--user", "--name", "semantic-kernel",
                "--display-name", "Semantic Kernel"
            ], check=True, capture_output=True, text=True)
            print("✅ Jupyter kernel configured")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to setup Jupyter: {e}")

    def create_env_file(self):
        """Create basic .env file"""
        env_file = self.workspace_root / ".env"
        if not env_file.exists():
            print("🔧 Creating .env file...")
            env_content = """# Semantic Kernel Configuration
OPENAI_API_KEY=your_openai_key_here
AZURE_OPENAI_API_KEY=your_azure_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=your-deployment-name
AZURE_OPENAI_API_VERSION=2024-02-01

# Development Settings
DEBUG=true
LOG_LEVEL=INFO
ENVIRONMENT=development
"""
            with open(env_file, "w") as f:
                f.write(env_content)
            print("✅ Created .env template")
        else:
            print("✅ .env file already exists")

    def run_setup(self):
        """Run complete setup"""
        print("🚀 Setting up Semantic Kernel Development Environment")
        print("=" * 60)

        self.install_packages()
        self.setup_jupyter()
        self.create_env_file()

        print("\n" + "=" * 60)
        print("✅ Setup completed! You can now:")
        print("  📓 Open and run Jupyter notebooks")
        print("  🧪 Run tests and experiments")
        print("  🚀 Start backend services")
        print("  🔧 Configure API keys in .env file")
        print("=" * 60)

if __name__ == "__main__":
    setup = QuickSetup()
    setup.run_setup()
