#!/usr/bin/env python3
"""
Test module for backend

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

# AI Chat Backend Test Script
# This script tests if the backend server is running and accessible

import requests
import time
import os
import sys
from pathlib import Path

def main():
    print("=============================")
    print("  Backend Connection Tester  ")
    print("=============================")
    print()
    
    # Get backend URL from .env file or use default
    backend_url = "http://localhost:8000"
    lm_studio_url = "http://localhost:1234"
    
    # Check .env file for custom URLs
    base_dir = Path(__file__).parent.absolute()
    env_file = base_dir / ".env"
    if env_file.exists():
        print("Reading configuration from .env file...")
        with open(env_file, 'r') as f:
            for line in f:
                if "=" in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    if key.strip() == "LM_STUDIO_URL":
                        value = value.strip().strip('"').strip("'")
                        # Extract hostname and port from URL
                        if "://" in value:
                            lm_studio_url = value.split("/v1/")[0]
                        print(f"Found LM Studio URL: {lm_studio_url}")
    
    print("\nTesting backend connection...")
    backend_ok = False
    try:
        response = requests.get(f"{backend_url}/ping", timeout=5)
        if response.status_code == 200:
            backend_ok = True
            print("✓ Backend server is running and responding!")
        else:
            print(f"✗ Backend server returned status code: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to backend server")
        print(f"  - Is the server running at {backend_url}?")
        print("  - Try running: python -m uvicorn backend:app --reload")
    except Exception as e:
        print(f"✗ Error testing backend: {str(e)}")
    
    print("\nTesting LM Studio connection...")
    lm_studio_ok = False
    try:
        response = requests.get(f"{lm_studio_url}/v1/models", timeout=5)
        if response.status_code == 200:
            lm_studio_ok = True
            models = response.json()
            if models.get("data"):
                print(f"✓ LM Studio is running with {len(models['data'])} models available!")
                # Print first few models
                for i, model in enumerate(models["data"][:3]):
                    print(f"  - {model.get('id', 'Unknown')}")
                if len(models["data"]) > 3:
                    print(f"  - ...and {len(models['data']) - 3} more")
            else:
                print("✓ LM Studio is running (no models found)")
        else:
            print(f"✗ LM Studio returned status code: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to LM Studio")
        print(f"  - Is LM Studio running at {lm_studio_url}?")
        print("  - Open LM Studio and start the server from the API tab")
    except Exception as e:
        print(f"✗ Error testing LM Studio: {str(e)}")
    
    # Test chat functionality if both services are running
    if backend_ok and lm_studio_ok:
        print("\nTesting chat functionality...")
        try:
            chat_data = {
                "message": "Hello, this is a test message",
                "system": "You are a helpful assistant",
                "temperature": 0.7,
                "max_tokens": 100
            }
            response = requests.post(f"{backend_url}/api/chat", json=chat_data, timeout=15)
            if response.status_code == 200 and "reply" in response.json():
                print("✓ Chat functionality is working!")
                reply = response.json().get("reply", "")
                if len(reply) > 100:
                    print(f"  Response: {reply[:100]}...")
                else:
                    print(f"  Response: {reply}")
            else:
                print(f"✗ Chat test failed with status code: {response.status_code}")
        except Exception as e:
            print(f"✗ Error testing chat: {str(e)}")
    
    print("\nSummary:")
    if backend_ok:
        print("✓ Backend server: RUNNING")
    else:
        print("✗ Backend server: NOT RUNNING")
        
    if lm_studio_ok:
        print("✓ LM Studio: RUNNING")
    else:
        print("✗ LM Studio: NOT RUNNING")
    
    if backend_ok and lm_studio_ok:
        print("\n✅ All systems operational! You can use the chat application.")
    else:
        print("\n❌ Some components are not running correctly. Please fix the issues above.")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nTest interrupted.")
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        input("Press Enter to exit...")
