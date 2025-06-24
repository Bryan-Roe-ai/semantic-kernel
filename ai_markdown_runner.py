#!/usr/bin/env python3
"""
AI Markdown Runner
A simple tool to execute markdown files with AI processing capabilities
"""

import httpx
import os
import re
import asyncio
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

LM_STUDIO_URL = os.environ.get(
    "LM_STUDIO_URL", "http://localhost:5272/v1/chat/completions"
)
LM_STUDIO_MODEL = os.environ.get("LM_STUDIO_MODEL", "mistral-7b-v02-int4-gpu")


class AIMarkdownRunner:
    """Run markdown files with AI processing"""

    def __init__(self):
        self.ai_pattern = re.compile(
            r"```ai(?:\s+(\w+))?\s*\n(.*?)\n```", re.DOTALL | re.MULTILINE
        )

    async def run_markdown(self, file_path: str) -> Dict[str, Any]:
        """Run a markdown file with AI processing"""
        path = Path(file_path)

        if not path.exists():
            return {"error": f"File not found: {file_path}"}

        # Read the markdown content
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # Find AI code blocks
        ai_blocks = self._find_ai_blocks(content)

        if not ai_blocks:
            return {
                "status": "no_ai_blocks",
                "message": "No AI processing blocks found in markdown",
                "content": content,
            }

        # Process each AI block
        results = []
        for block in ai_blocks:
            result = await self._process_ai_block(block, path)
            results.append(result)

        return {
            "status": "processed",
            "file": str(path),
            "ai_blocks_found": len(ai_blocks),
            "results": results,
            "processed_at": datetime.now().isoformat(),
        }

    def _find_ai_blocks(self, content: str) -> List[Dict[str, Any]]:
        """Find AI processing blocks in markdown"""
        blocks = []

        for match in self.ai_pattern.finditer(content):
            ai_type = match.group(1) or "execute"
            ai_content = match.group(2).strip()

            blocks.append(
                {
                    "type": ai_type,
                    "content": ai_content,
                    "start": match.start(),
                    "end": match.end(),
                }
            )

        return blocks

    async def _process_ai_block(
        self, block: Dict[str, Any], file_path: Path
    ) -> Dict[str, Any]:
        """Process an AI block"""
        ai_type = block["type"]
        content = block["content"]

        # Dispatch to appropriate handler
        handlers = {
            "execute": self._execute_command,
            "analyze": self._analyze_content,
            "generate": self._generate_content,
            "summarize": self._summarize_content,
            "enhance": self._enhance_content,
        }

        if ai_type in handlers:
            result = await handlers[ai_type](content, file_path)
        else:
            result = f"Unknown AI type: {ai_type}"

        return {
            "type": ai_type,
            "input": content,
            "output": result,
            "processed_at": datetime.now().isoformat(),
        }

    async def _execute_command(self, content: str, file_path: Path) -> str:
        """Execute AI command"""
        return f"""
🤖 AI EXECUTION RESULT
File: {file_path.name}
Command: {content}

Simulated AI processing...
This would normally execute the AI instruction and return results.
For real AI processing, integrate with:
- OpenAI API
- Local LLM
- AGI MCP Server
- Semantic Kernel

Result: Command processed successfully
"""

    async def _analyze_content(self, content: str, file_path: Path) -> str:
        """Analyze content with AI (OpenAI or LM Studio)"""
        prompt = (
            "Analyze the following content and provide insights, key points, and suggestions for improvement. "
            "Be concise and structured.\n\nContent:\n" + content.strip()
        )
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        if openai_api_key:
            try:
                headers = {
                    "Authorization": f"Bearer {openai_api_key}",
                    "Content-Type": "application/json",
                }
                payload = {
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a helpful AI assistant.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.5,
                    "max_tokens": 512,
                }
                async with httpx.AsyncClient(timeout=30) as client:
                    response = await client.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers=headers,
                        json=payload,
                    )
                    response.raise_for_status()
                    data = response.json()
                    if "choices" in data and data["choices"]:
                        return data["choices"][0]["message"]["content"]
                    return f"[ERROR] No choices in OpenAI response: {data}"
            except Exception as e:
                return f"[ERROR] Failed to call OpenAI API: {e}"
        # Fallback to LM Studio
        payload = {
            "model": LM_STUDIO_MODEL,
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.5,
            "max_tokens": 512,
        }
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(LM_STUDIO_URL, json=payload)
                response.raise_for_status()
                data = response.json()
                if "choices" in data and data["choices"]:
                    return data["choices"][0]["message"]["content"]
                return f"[ERROR] No choices in LM Studio response: {data}"
        except Exception as e:
            return f"[ERROR] Failed to call local LLM: {e}\nSet OPENAI_API_KEY for OpenAI, or start LM Studio."

    async def _generate_content(self, content: str, file_path: Path) -> str:
        """Generate content using Ollama's /api/generate endpoint"""
        import httpx
        import json

        prompt = content.strip()
        payload = {"model": "llama2", "prompt": prompt, "stream": False}
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    "http://localhost:11434/api/generate", json=payload
                )
                response.raise_for_status()
                data = response.json()
                if "response" in data:
                    return data["response"]
                return f"[ERROR] No response in Ollama output: {json.dumps(data)}"
        except Exception as e:
            return f"[ERROR] Failed to call Ollama /api/generate: {e}"

    async def _summarize_content(self, content: str, file_path: Path) -> str:
        """Summarize content with AI (OpenAI or LM Studio)"""
        prompt = (
            "Summarize the following content in a concise, clear, and structured way. "
            "Highlight the main points and key takeaways.\n\nContent:\n"
            + content.strip()
        )
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        if openai_api_key:
            try:
                headers = {
                    "Authorization": f"Bearer {openai_api_key}",
                    "Content-Type": "application/json",
                }
                payload = {
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a helpful AI assistant.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.5,
                    "max_tokens": 512,
                }
                async with httpx.AsyncClient(timeout=30) as client:
                    response = await client.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers=headers,
                        json=payload,
                    )
                    response.raise_for_status()
                    data = response.json()
                    if "choices" in data and data["choices"]:
                        return data["choices"][0]["message"]["content"]
                    return f"[ERROR] No choices in OpenAI response: {data}"
            except Exception as e:
                return f"[ERROR] Failed to call OpenAI API: {e}"
        # Fallback to LM Studio
        payload = {
            "model": LM_STUDIO_MODEL,
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.5,
            "max_tokens": 512,
        }
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(LM_STUDIO_URL, json=payload)
                response.raise_for_status()
                data = response.json()
                if "choices" in data and data["choices"]:
                    return data["choices"][0]["message"]["content"]
                return f"[ERROR] No choices in LM Studio response: {data}"
        except Exception as e:
            return f"[ERROR] Failed to call local LLM: {e}\nSet OPENAI_API_KEY for OpenAI, or start LM Studio."

    async def _enhance_content(self, content: str, file_path: Path) -> str:
        """Enhance content with AI (OpenAI or LM Studio)"""
        prompt = (
            "Improve and enhance the following content. "
            "Make it clearer, more detailed, and better structured.\n\nContent:\n"
            + content.strip()
        )
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        if openai_api_key:
            try:
                headers = {
                    "Authorization": f"Bearer {openai_api_key}",
                    "Content-Type": "application/json",
                }
                payload = {
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a helpful AI assistant.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.5,
                    "max_tokens": 512,
                }
                async with httpx.AsyncClient(timeout=30) as client:
                    response = await client.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers=headers,
                        json=payload,
                    )
                    response.raise_for_status()
                    data = response.json()
                    if "choices" in data and data["choices"]:
                        return data["choices"][0]["message"]["content"]
                    return f"[ERROR] No choices in OpenAI response: {data}"
            except Exception as e:
                return f"[ERROR] Failed to call OpenAI API: {e}"
        # Fallback to LM Studio
        payload = {
            "model": LM_STUDIO_MODEL,
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.5,
            "max_tokens": 512,
        }
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(LM_STUDIO_URL, json=payload)
                response.raise_for_status()
                data = response.json()
                if "choices" in data and data["choices"]:
                    return data["choices"][0]["message"]["content"]
                return f"[ERROR] No choices in LM Studio response: {data}"
        except Exception as e:
            return f"[ERROR] Failed to call local LLM: {e}\nSet OPENAI_API_KEY for OpenAI, or start LM Studio."

    def _load_llm_config(self):
        import json

        config = {}
        config_path = Path("llm_config.json")
        if config_path.exists():
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
            except Exception:
                pass
        # Fallback to env vars if not in config
        config.setdefault("custom_llm_url", os.environ.get("CUSTOM_LLM_URL"))
        config.setdefault(
            "custom_llm_payload_template", os.environ.get("CUSTOM_LLM_PAYLOAD_TEMPLATE")
        )
        config.setdefault(
            "custom_llm_response_path", os.environ.get("CUSTOM_LLM_RESPONSE_PATH")
        )
        return config

    async def _call_real_ai(self, prompt: str, purpose: str = "completion") -> str:
        import json

        config = self._load_llm_config()
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        lm_studio_url = os.environ.get(
            "LM_STUDIO_URL", "http://localhost:5272/v1/chat/completions"
        )
        lm_studio_model = os.environ.get("LM_STUDIO_MODEL", "mistral-7b-v02-int4-gpu")
        custom_llm_url = config.get("custom_llm_url")
        custom_llm_payload_template = config.get("custom_llm_payload_template")
        custom_llm_response_path = config.get("custom_llm_response_path")

        # 1. Custom LLM
        if custom_llm_url and custom_llm_payload_template:
            try:
                payload = json.loads(
                    custom_llm_payload_template.replace("{prompt}", prompt)
                )
                async with httpx.AsyncClient(timeout=30) as client:
                    response = await client.post(custom_llm_url, json=payload)
                    response.raise_for_status()
                    data = response.json()
                    # Traverse response path (dot notation)
                    if custom_llm_response_path:
                        val = data
                        for part in custom_llm_response_path.split("."):
                            val = val.get(part, None)
                            if val is None:
                                break
                        if val:
                            return str(val)
                        return f"[ERROR] Could not find response at path: {custom_llm_response_path}"
                    return str(data)
            except Exception as e:
                return f"[ERROR] Failed to call custom LLM: {e}"

        # 2. OpenAI
        if openai_api_key:
            try:
                headers = {
                    "Authorization": f"Bearer {openai_api_key}",
                    "Content-Type": "application/json",
                }
                payload = {
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a helpful AI assistant.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.7,
                    "max_tokens": 512,
                }
                async with httpx.AsyncClient(timeout=30) as client:
                    response = await client.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers=headers,
                        json=payload,
                    )
                    response.raise_for_status()
                    data = response.json()
                    if "choices" in data and data["choices"]:
                        return data["choices"][0]["message"]["content"]
                    return f"[ERROR] No choices in OpenAI response: {data}"
            except Exception as e:
                return f"[ERROR] Failed to call OpenAI API: {e}"

        # 3. LM Studio
        payload = {
            "model": lm_studio_model,
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7,
            "max_tokens": 512,
        }
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(lm_studio_url, json=payload)
                response.raise_for_status()
                data = response.json()
                if "choices" in data and data["choices"]:
                    return data["choices"][0]["message"]["content"]
                return f"[ERROR] No choices in LM Studio response: {data}"
        except Exception as e:
            # 4. Ollama (only for generate)
            if purpose == "generate":
                try:
                    ollama_url = os.environ.get(
                        "OLLAMA_URL", "http://localhost:11434/api/generate"
                    )
                    ollama_model = os.environ.get("OLLAMA_MODEL", "llama2")
                    ollama_payload = {
                        "model": ollama_model,
                        "prompt": prompt,
                        "stream": False,
                    }
                    async with httpx.AsyncClient(timeout=30) as client:
                        response = await client.post(ollama_url, json=ollama_payload)
                        response.raise_for_status()
                        data = response.json()
                        if "response" in data:
                            return data["response"]
                        return (
                            f"[ERROR] No response in Ollama output: {json.dumps(data)}"
                        )
                except Exception as e2:
                    return f"[ERROR] Failed to call Ollama /api/generate: {e2}"
            return f"[ERROR] Failed to call local LLM: {e}\nSet OPENAI_API_KEY for OpenAI, or start LM Studio."


async def main():
    """Main function to run AI markdown processor"""

    if len(sys.argv) != 2:
        print("Usage: python ai_markdown_runner.py <markdown_file>")
        return

    file_path = sys.argv[1]
    runner = AIMarkdownRunner()

    print("🤖 AI Markdown Runner")
    print("=" * 50)
    print(f"Processing: {file_path}")
    print("-" * 50)

    result = await runner.run_markdown(file_path)

    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return

    print(f"📊 Status: {result['status']}")
    if "file" in result:
        print(f"📁 File: {result['file']}")
    if "ai_blocks_found" in result:
        print(f"🔍 AI blocks found: {result['ai_blocks_found']}")
    if "processed_at" in result:
        print(f"⏰ Processed at: {result['processed_at']}")
    print("=" * 50)

    for i, ai_result in enumerate(result.get("results", []), 1):
        print(f"\n🧠 AI Block {i}: {ai_result['type']}")
        print("-" * 30)
        print(ai_result["output"])

    # If no AI blocks, do a default AI analysis on the whole file
    if result.get("status") == "no_ai_blocks":
        print(
            "\n[INFO] No AI blocks found. Running default AI analysis on the file...\n"
        )
        runner = AIMarkdownRunner()
        analysis = await runner._analyze_content(result["content"], Path(file_path))
        print(analysis)


if __name__ == "__main__":
    asyncio.run(main())
