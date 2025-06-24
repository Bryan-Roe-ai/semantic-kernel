#!/usr/bin/env python3
"""
Cloud Deploy module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# Cloud Deployment Automation - Auto-created by setup.py
import os
import sys
import time
import json
import logging
import argparse
import subprocess
from pathlib import Path

logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s',
                   handlers=[logging.FileHandler("cloud_deploy.log"),
                             logging.StreamHandler()])

class CloudDeployer:
    """Handles deployment to various cloud platforms"""
    
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.config_path = self.base_dir / "cloud_deploy_config.json"
        self.load_config()
    
    def load_config(self):
        """Load deployment configuration"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    self.config = json.load(f)
                logging.info(f"Loaded configuration from {self.config_path}")
            except Exception as e:
                logging.error(f"Error loading configuration: {e}")
                self.config = {}
        else:
            logging.warning(f"No configuration found at {self.config_path}, using defaults")
            # Default configuration
            self.config = {
                "azure": {
                    "resource_group": "ai-chat-app-rg",
                    "app_name": "ai-chat-app",
                    "location": "eastus",
                    "sku": "F1"
                },
                "aws": {
                    "s3_bucket": "ai-chat-app-bucket",
                    "region": "us-east-1"
                },
                "docker": {
                    "image_name": "ai-chat-app",
                    "tag": "latest"
                }
            }
            # Save default config
            self.save_config()
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            logging.info(f"Configuration saved to {self.config_path}")
        except Exception as e:
            logging.error(f"Error saving configuration: {e}")
    
    def create_dockerfile(self):
        """Create Dockerfile for containerization"""
        docker_path = self.base_dir / "Dockerfile"
        if not docker_path.exists():
            try:
                with open(docker_path, 'w') as f:
                    f.write("""FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY . .

# Expose the port
EXPOSE 8000

# Start the application
CMD ["python", "backend.py"]
""")
                logging.info(f"Created Dockerfile at {docker_path}")
            except Exception as e:
                logging.error(f"Error creating Dockerfile: {e}")
                return False
        return True
    
    def build_docker_image(self):
        """Build Docker image from Dockerfile"""
        if not self.create_dockerfile():
            return False
            
        image_name = f"{self.config['docker']['image_name']}:{self.config['docker']['tag']}"
        logging.info(f"Building Docker image: {image_name}")
        
        try:
            result = subprocess.run(
                ["docker", "build", "-t", image_name, "."],
                cwd=str(self.base_dir),
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            logging.info("Docker image built successfully")
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f"Docker build failed: {e.stderr.decode()}")
            return False
        except Exception as e:
            logging.error(f"Error building Docker image: {e}")
            return False
    
    def deploy_to_azure(self):
        """Deploy application to Azure App Service"""
        logging.info("Starting deployment to Azure")
        
        # Check Azure CLI is installed
        try:
            subprocess.run(["az", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except:
            logging.error("Azure CLI not installed. Please install it first.")
            return False
        
        # Login to Azure (if needed)
        try:
            subprocess.run(["az", "account", "show"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except:
            logging.info("Please log in to Azure...")
            subprocess.run(["az", "login"], check=True)
        
        rg = self.config["azure"]["resource_group"]
        app_name = self.config["azure"]["app_name"]
        location = self.config["azure"]["location"]
        sku = self.config["azure"]["sku"]
        
        # Create resource group if it doesn't exist
        try:
            subprocess.run(
                ["az", "group", "create", "--name", rg, "--location", location],
                check=True,
                stdout=subprocess.PIPE
            )
            logging.info(f"Resource group '{rg}' created or already exists")
        except Exception as e:
            logging.error(f"Failed to create resource group: {e}")
            return False
        
        # Deploy as App Service
        try:
            # Create App Service plan
            subprocess.run(
                ["az", "appservice", "plan", "create", "--name", f"{app_name}-plan",
                 "--resource-group", rg, "--sku", sku],
                check=True,
                stdout=subprocess.PIPE
            )
            # Create Web App
            subprocess.run(
                ["az", "webapp", "create", "--name", app_name,
                 "--resource-group", rg, "--plan", f"{app_name}-plan",
                 "--runtime", "PYTHON:3.10"],
                check=True,
                stdout=subprocess.PIPE
            )
            # Deploy code
            subprocess.run(
                ["az", "webapp", "up", "--name", app_name, "--resource-group", rg],
                check=True,
                cwd=str(self.base_dir),
                stdout=subprocess.PIPE
            )
            logging.info(f"Web App deployed to https://{app_name}.azurewebsites.net")
            return True
        except Exception as e:
            logging.error(f"Azure deployment failed: {e}")
            return False
    
    def deploy_to_aws(self):
        """Deploy application to AWS (basic S3 static hosting)"""
        logging.info("Starting deployment to AWS")
        
        # Check AWS CLI is installed
        try:
            subprocess.run(["aws", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except:
            logging.error("AWS CLI not installed. Please install it first.")
            return False
        
        bucket = self.config["aws"]["s3_bucket"]
        region = self.config["aws"]["region"]
        
        # Create bucket if it doesn't exist
        try:
            subprocess.run(
                ["aws", "s3", "mb", f"s3://{bucket}", "--region", region],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        except:
            logging.info(f"Bucket {bucket} might already exist")
        
        # Enable website hosting
        try:
            subprocess.run(
                ["aws", "s3", "website", f"s3://{bucket}",
                 "--index-document", "ai-chat-launcher.html"],
                check=True,
                stdout=subprocess.PIPE
            )
            logging.info(f"S3 website hosting enabled on bucket {bucket}")
        except Exception as e:
            logging.error(f"Failed to enable website hosting: {e}")
            return False
        
        # Sync files
        try:
            # Upload HTML files
            for html_file in self.base_dir.glob("*.html"):
                subprocess.run(
                    ["aws", "s3", "cp", str(html_file), f"s3://{bucket}/",
                     "--acl", "public-read"],
                    check=True,
                    stdout=subprocess.PIPE
                )
            logging.info(f"Deployed static files to http://{bucket}.s3-website-{region}.amazonaws.com/")
            return True
        except Exception as e:
            logging.error(f"AWS deployment failed: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description="Cloud Deployment Tool")
    parser.add_argument("--target", choices=["azure", "aws", "docker"], 
                      help="Deployment target")
    args = parser.parse_args()
    
    base_dir = Path(__file__).parent
    deployer = CloudDeployer(base_dir)
    
    if not args.target:
        print("Please specify a deployment target: azure, aws, or docker")
        return
    
    if args.target == "azure":
        deployer.deploy_to_azure()
    elif args.target == "aws":
        deployer.deploy_to_aws()
    elif args.target == "docker":
        deployer.build_docker_image()

if __name__ == "__main__":
    main()
