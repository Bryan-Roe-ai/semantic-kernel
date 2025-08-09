#!/usr/bin/env python3
"""LM Studio Sample

Demonstrates using an LM Studio OpenAI-compatible server with Semantic Kernel style
patterns.

Requirements:
 1. Start LM Studio and enable the OpenAI server (default http://localhost:1234)
 2. Load/download a model in LM Studio UI (note the model id shown)
 3. (Optional) export LM_STUDIO_BASE_URL / LM_STUDIO_MODEL env vars

Flow:
    * List models (/v1/models)
    * Basic chat completion
    * Streaming chat completion (token stream)
    * Prompt-function style single sentence

Auth: not required, but if LM_STUDIO_API_KEY is set it is sent as Bearer.
"""
from __future__ import annotations
import os
import sys
import json
import asyncio
import aiohttp
from typing import Dict, Any, List, AsyncGenerator

BASE_URL = os.environ.get("LM_STUDIO_BASE_URL", "http://localhost:1234")
MODEL = os.environ.get("LM_STUDIO_MODEL")  # fallback to first model
API_KEY = os.environ.get("LM_STUDIO_API_KEY")
HEADERS = {"Content-Type": "application/json"}
if API_KEY:
    HEADERS["Authorization"] = f"Bearer {API_KEY}"

async def list_models(session: aiohttp.ClientSession) -> List[str]:
    url = f"{BASE_URL}/v1/models"
    async with session.get(url) as r:
        r.raise_for_status()
        data = await r.json()
    # LM Studio returns { data: [ {id: "model-id"}, ... ] }
    return [m.get("id") for m in data.get("data", [])]

async def chat_once(
    session: aiohttp.ClientSession,
    messages: List[Dict[str, str]],
    model: str,
) -> Dict[str, Any]:
    """Single (non-streaming) chat completion."""
    url = f"{BASE_URL}/v1/chat/completions"
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 256,
        "stream": False,
    }
    async with session.post(url, headers=HEADERS, json=payload) as resp:
        resp.raise_for_status()
        return await resp.json()


async def chat_stream(
    session: aiohttp.ClientSession,
    messages: List[Dict[str, str]],
    model: str,
) -> AsyncGenerator[Dict[str, Any], None]:
    """Streaming chat completion yielding OpenAI-style chunks."""
    url = f"{BASE_URL}/v1/chat/completions"
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 256,
        "stream": True,
    }
    async with session.post(url, headers=HEADERS, json=payload) as resp:
        resp.raise_for_status()
        async for line in resp.content:
            if not line:
                continue
            try:
                chunk_line = line.decode("utf-8").strip()
            except Exception:
                continue
            if not chunk_line or not chunk_line.startswith("data:"):
                continue
            if chunk_line == "data: [DONE]":
                break
            try:
                obj = json.loads(chunk_line[len("data:"):].strip())
            except json.JSONDecodeError:
                continue
            yield obj

async def main() -> None:
    print(f"🔗 Connecting to LM Studio at {BASE_URL}")
    timeout = aiohttp.ClientTimeout(total=120)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        models = await list_models(session)
        if not models:
            print(
                "❌ No models returned. Ensure LM Studio server is running "
                "and a model is loaded."
            )
            sys.exit(1)
        sample_models = ", ".join(models[:3])
        if len(models) > 3:
            sample_models += "..."
        print(f"✅ Models: {sample_models}")
        model = MODEL or models[0]
        print(f"🧠 Using model: {model}")

        # Basic chat
        print("\n=== Basic Chat Completion ===")
        basic = await chat_once(
            session,
            [
            {"role": "system", "content": "You are a concise assistant."},
            {
                "role": "user",
                "content": "List three benefits of local LLM inference.",
            },
            ],
            model,
        )
        text = basic.get("choices", [{}])[0].get("message", {}).get(
            "content", "<no content>"
        )
        print(text.strip())

        # Streaming chat
        print("\n=== Streaming Chat Completion ===")
        stream_messages = [
            {"role": "system", "content": "You stream responses."},
            {
                "role": "user",
                "content": "Explain semantic kernels in one paragraph.",
            },
        ]
        async for chunk in chat_stream(session, stream_messages, model):
            delta = chunk.get("choices", [{}])[0].get("delta", {}).get("content")
            if delta:
                print(delta, end="", flush=True)
        print("\n--- Done ---")

        # Minimal function-like prompt (Semantic Kernel style)
        print("\n=== Prompt Function Style ===")
        topic = "edge deployment of AI"
        function_prompt = f"Provide a single concise sentence about {topic}."
        pf = await chat_once(
            session,
            [{"role": "user", "content": function_prompt}],
            model,
        )
        pf_text = pf.get("choices", [{}])[0].get("message", {}).get(
            "content", "<no content>"
        ).strip()
        print(pf_text)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Interrupted.")
