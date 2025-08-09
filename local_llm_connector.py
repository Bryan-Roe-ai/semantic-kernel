#!/usr/bin/env python3
"""
Local LLM Connector - Universal connector for local AI models

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

import requests
import json
import asyncio
import aiohttp
from typing import Dict, List, Optional, Any, AsyncIterator
from dataclasses import dataclass
from enum import Enum

class LocalLLMProvider(Enum):
    """Supported local LLM providers"""
    LM_STUDIO = "lm_studio"
    OLLAMA = "ollama"
    OOBABOOGA = "oobabooga"
    LLAMA_CPP = "llama_cpp"
    KOBOLD = "kobold"

@dataclass
class LocalLLMConfig:
    """Configuration for local LLM connection"""
    provider: LocalLLMProvider
    base_url: str
    model_name: Optional[str] = None
    api_key: Optional[str] = None
    timeout: int = 30

class LocalLLMConnector:
    """Universal connector for local LLM providers"""

    def __init__(self, config: LocalLLMConfig):
        self.config = config
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.config.timeout))
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def _get_endpoint_info(self) -> Dict[str, str]:
        """Get endpoint information for the provider"""
        endpoints = {
            LocalLLMProvider.LM_STUDIO: {
                "chat": "/v1/chat/completions",
                "models": "/v1/models",
                "completions": "/v1/completions"
            },
            LocalLLMProvider.OLLAMA: {
                "chat": "/api/chat",
                "models": "/api/tags",
                "generate": "/api/generate"
            },
            LocalLLMProvider.OOBABOOGA: {
                "chat": "/v1/chat/completions",
                "models": "/v1/models",
                "completions": "/v1/completions"
            },
            LocalLLMProvider.LLAMA_CPP: {
                "chat": "/v1/chat/completions",
                "models": "/v1/models",
                "completions": "/v1/completions"
            },
            LocalLLMProvider.KOBOLD: {
                "generate": "/api/v1/generate",
                "models": "/api/v1/model"
            }
        }
        return endpoints.get(self.config.provider, {})

    async def test_connection(self) -> bool:
        """Test if the LLM provider is accessible"""
        try:
            endpoints = self._get_endpoint_info()
            models_endpoint = endpoints.get("models", "/")

            if not self.session:
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
                    async with session.get(f"{self.config.base_url}{models_endpoint}") as response:
                        return response.status == 200
            else:
                async with self.session.get(f"{self.config.base_url}{models_endpoint}") as response:
                    return response.status == 200
        except Exception:
            return False

    async def get_available_models(self) -> List[str]:
        """Get list of available models"""
        try:
            endpoints = self._get_endpoint_info()
            models_endpoint = endpoints.get("models", "/")

            if not self.session:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{self.config.base_url}{models_endpoint}") as response:
                        data = await response.json()
            else:
                async with self.session.get(f"{self.config.base_url}{models_endpoint}") as response:
                    data = await response.json()

            # Parse based on provider
            if self.config.provider == LocalLLMProvider.OLLAMA:
                return [model["name"] for model in data.get("models", [])]
            elif self.config.provider in [LocalLLMProvider.LM_STUDIO, LocalLLMProvider.OOBABOOGA]:
                return [model["id"] for model in data.get("data", [])]
            else:
                return [data.get("result", "unknown")]

        except Exception as e:
            print(f"Error getting models: {e}")
            return []

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        stream: bool = False
    ) -> Dict[str, Any]:
        """Generate chat completion"""

        model = model or self.config.model_name or "default"
        endpoints = self._get_endpoint_info()

        # Prepare request based on provider
        if self.config.provider == LocalLLMProvider.OLLAMA:
            endpoint = endpoints["chat"]
            payload = {
                "model": model,
                "messages": messages,
                "stream": stream,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            }
        else:  # OpenAI-compatible providers
            endpoint = endpoints.get("chat", "/v1/chat/completions")
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": stream
            }

        headers = {"Content-Type": "application/json"}
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"

        if not self.session:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.config.base_url}{endpoint}",
                    json=payload,
                    headers=headers
                ) as response:
                    return await response.json()
        else:
            async with self.session.post(
                f"{self.config.base_url}{endpoint}",
                json=payload,
                headers=headers
            ) as response:
                return await response.json()

    async def text_completion(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """Generate text completion"""

        # Convert to chat format for consistent interface
        messages = [{"role": "user", "content": prompt}]
        result = await self.chat_completion(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )

        # Extract text based on provider response format
        if self.config.provider == LocalLLMProvider.OLLAMA:
            return result.get("message", {}).get("content", "")
        else:
            choices = result.get("choices", [])
            if choices:
                return choices[0].get("message", {}).get("content", "")

        return ""

class LocalLLMManager:
    """Manager for multiple local LLM connections"""

    def __init__(self):
        self.connectors: Dict[str, LocalLLMConnector] = {}
        self.configs: Dict[str, LocalLLMConfig] = {}

    def add_provider(self, name: str, config: LocalLLMConfig):
        """Add a local LLM provider"""
        self.configs[name] = config
        self.connectors[name] = LocalLLMConnector(config)

    async def test_all_connections(self) -> Dict[str, bool]:
        """Test all configured providers"""
        results = {}
        for name, connector in self.connectors.items():
            async with connector:
                results[name] = await connector.test_connection()
        return results

    async def get_available_providers(self) -> List[str]:
        """Get list of available (working) providers"""
        test_results = await self.test_all_connections()
        return [name for name, working in test_results.items() if working]

    async def auto_detect_providers(self) -> Dict[str, LocalLLMConfig]:
        """Auto-detect running local LLM providers"""
        potential_configs = [
            ("LM Studio", LocalLLMConfig(LocalLLMProvider.LM_STUDIO, "http://localhost:1234")),
            ("Ollama", LocalLLMConfig(LocalLLMProvider.OLLAMA, "http://localhost:11434")),
            ("Oobabooga", LocalLLMConfig(LocalLLMProvider.OOBABOOGA, "http://localhost:5000")),
            ("Llama.cpp", LocalLLMConfig(LocalLLMProvider.LLAMA_CPP, "http://localhost:8080")),
            ("KoboldAI", LocalLLMConfig(LocalLLMProvider.KOBOLD, "http://localhost:5001")),
        ]

        detected = {}
        for name, config in potential_configs:
            connector = LocalLLMConnector(config)
            async with connector:
                if await connector.test_connection():
                    detected[name] = config
                    print(f"✓ Detected {name} at {config.base_url}")

        return detected

# Convenience functions for quick setup
def create_lm_studio_connector(base_url: str = "http://localhost:1234", model: Optional[str] = None) -> LocalLLMConnector:
    """Create LM Studio connector"""
    config = LocalLLMConfig(
        provider=LocalLLMProvider.LM_STUDIO,
        base_url=base_url,
        model_name=model
    )
    return LocalLLMConnector(config)

def create_ollama_connector(base_url: str = "http://localhost:11434", model: Optional[str] = None) -> LocalLLMConnector:
    """Create Ollama connector"""
    config = LocalLLMConfig(
        provider=LocalLLMProvider.OLLAMA,
        base_url=base_url,
        model_name=model
    )
    return LocalLLMConnector(config)

async def quick_test():
    """Quick test function"""
    print("🔍 Auto-detecting local LLM providers...")

    manager = LocalLLMManager()
    detected = await manager.auto_detect_providers()

    if not detected:
        print("❌ No local LLM providers detected")
        print("💡 Make sure one of these is running:")
        print("   • LM Studio (port 1234)")
        print("   • Ollama (port 11434)")
        print("   • Oobabooga (port 5000)")
        return

    # Test the first detected provider
    name, config = next(iter(detected.items()))
    print(f"\n🧪 Testing {name}...")

    async with LocalLLMConnector(config) as connector:
        # Get models
        models = await connector.get_available_models()
        print(f"📋 Available models: {', '.join(models[:3])}{'...' if len(models) > 3 else ''}")

        # Test chat
        if models:
            response = await connector.chat_completion(
                messages=[{"role": "user", "content": "Hello! Please respond briefly."}],
                model=models[0] if models else None,
                max_tokens=50
            )

            # Extract response based on provider
            if config.provider == LocalLLMProvider.OLLAMA:
                text = response.get("message", {}).get("content", "No response")
            else:
                choices = response.get("choices", [])
                text = choices[0].get("message", {}).get("content", "No response") if choices else "No response"

            print(f"💬 Test response: {text[:100]}{'...' if len(text) > 100 else ''}")

if __name__ == "__main__":
    asyncio.run(quick_test())
