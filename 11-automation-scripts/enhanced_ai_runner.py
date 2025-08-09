#!/usr/bin/env python3
"""
Enhanced AI Markdown Runner with proper block parsing

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This module provides enhanced AI markdown processing capabilities with support for
intelligent code block parsing, execution, and AI-powered content generation.
This is original work by Bryan Roe as part of the Semantic Kernel - Advanced AI
Development Framework.

Author: Bryan Roe
Created: 2025
License: MIT
"""

import re
import asyncio
def _load_llm_config_with_preview_control(config_path: Path) -> Dict[str, Any]:

from llm_config_loader import load_llm_config_with_preview_control


class EnhancedAIMarkdownRunner:
    """
    Enhanced AI Markdown Runner with better parsing

    Original implementation by Bryan Roe
    Copyright (c) 2025 Bryan Roe
    """

    def __init__(self):
        # Pattern to match AI code blocks
        self.ai_pattern = re.compile(r"```ai(?:\s+(\w+))?\s*\n(.*?)\n```", re.DOTALL)

    async def run_markdown(self, file_path: str) -> Dict[str, Any]:
        """Run a markdown file with AI processing"""
        path = Path(file_path)

        if not path.exists():
            return {"error": f"File not found: {file_path}"}

        # Read the markdown content
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        print(f"📄 Content length: {len(content)} characters")

        # Find AI code blocks
        ai_blocks = self._find_ai_blocks(content)

        print(f"🔍 Found {len(ai_blocks)} AI blocks")

        if not ai_blocks:
            print("ℹ️ No AI processing blocks found")
            print("Looking for patterns like:")
            print("```ai")
            print("your instruction here")
            print("```")
            return {
                "status": "no_ai_blocks",
                "message": "No AI processing blocks found in markdown",
                "content_preview": (
                    content[:200] + "..." if len(content) > 200 else content
                ),
            }

        # Process each AI block
        results = []
        for i, block in enumerate(ai_blocks, 1):
            print(f"🤖 Processing AI block {i}/{len(ai_blocks)}: {block['type']}")
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
        """Find AI processing blocks in markdown with debugging"""
        blocks = []

        # Debug: Show what we're looking for
        print("🔍 Searching for AI blocks with pattern: ```ai")

        # Find all matches
        matches = list(self.ai_pattern.finditer(content))
        print(f"🔍 Regex found {len(matches)} matches")

        for i, match in enumerate(matches):
            ai_type = match.group(1) if match.group(1) else "execute"
            ai_content = match.group(2).strip()

            print(f"  Block {i+1}: type='{ai_type}', content_length={len(ai_content)}")

            blocks.append(
                {
                    "type": ai_type,
                    "content": ai_content,
                    "start": match.start(),
                    "end": match.end(),
                    "raw_match": (
                        match.group(0)[:100] + "..."
                        if len(match.group(0)) > 100
                        else match.group(0)
                    ),
                }
            )

        return blocks

    async def _process_ai_block(
        self, block: Dict[str, Any], file_path: Path
    ) -> Dict[str, Any]:
        """Process an AI block"""
        ai_type = block["type"]
        content = block["content"]

        print(f"  🎯 Processing type: {ai_type}")
        print(f"  📝 Content preview: {content[:50]}...")

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
            result = f"❌ Unknown AI type: {ai_type}\nAvailable types: {', '.join(handlers.keys())}"

        return {
            "type": ai_type,
            "input": content,
            "output": result,
            "processed_at": datetime.now().isoformat(),
        }

    async def _execute_command(self, content: str, file_path: Path) -> str:
        """Execute AI command"""
        return f"""🤖 AI EXECUTION RESULT
━━━━━━━━━━━━━━━━━━━━━━━━━
📁 File: {file_path.name}
📋 Command: {content[:100]}{'...' if len(content) > 100 else ''}

✨ AI Processing Complete!
This would normally execute the AI instruction and return intelligent results.

🔗 For real AI processing, integrate with:
  • OpenAI API (GPT-4, Claude, etc.)
  • Local LLMs (Ollama, LM Studio)
  • Your AGI MCP Server
  • Semantic Kernel
  • Hugging Face Transformers

💡 Result: Command processed successfully with simulated intelligence
━━━━━━━━━━━━━━━━━━━━━━━━━"""

    def _load_llm_config(self):
        config = load_llm_config_with_preview_control(Path("llm_config.json"))
        config.setdefault("custom_llm_url", os.environ.get("CUSTOM_LLM_URL"))
        config.setdefault("custom_llm_payload_template", os.environ.get("CUSTOM_LLM_PAYLOAD_TEMPLATE"))
        config.setdefault("custom_llm_response_path", os.environ.get("CUSTOM_LLM_RESPONSE_PATH"))
        return config

    async def _call_real_ai(self, prompt: str, purpose: str = "completion") -> str:
        """Call OpenAI API, LM Studio, or custom LLM for real AI output."""
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
        active_chat_model = config.get("active_chat_model") or "gpt-3.5-turbo"

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
                        for part in custom_llm_response_path.split('.'):
                            val = val.get(part, None) if isinstance(val, dict) else None
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
                    "model": active_chat_model,
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
                    # Fallback chain if preview model unsupported
                    if active_chat_model.startswith("gpt-5"):
                        # Attempt fallback chain defined in config
                        metadata = config.get("models", {})
                        attempted = set([active_chat_model])
                        current = metadata.get(active_chat_model, {}).get("fallback")
                        while current and current not in attempted:
                            attempted.add(current)
                            payload["model"] = current
                            try:
                                r2 = await client.post(
                                    "https://api.openai.com/v1/chat/completions",
                                    headers=headers,
                                    json=payload,
                                )
                                if r2.status_code == 200:
                                    d2 = r2.json()
                                    if d2.get("choices"):
                                        return d2["choices"][0]["message"]["content"]
                            except Exception:
                                pass
                            current = metadata.get(current, {}).get("fallback")
                        return f"[ERROR] No choices in OpenAI response (after fallbacks): {data}"
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
            return f"[ERROR] Failed to call local LLM: {e}\nSet OPENAI_API_KEY for OpenAI, or start LM Studio."

    async def _analyze_content(self, content: str, file_path: Path) -> str:
        """Analyze content with real AI if available"""
        prompt = (
            "Analyze the following content and provide insights, key points, and suggestions for improvement. "
            "Be concise and structured.\n\nContent:\n" + content.strip()
        )
        ai_result = await self._call_real_ai(prompt, purpose="analyze")
        if ai_result.startswith("[ERROR]"):
            # fallback to simulated
            words = content.split()
            lines = content.split("\n")
            sentences = content.split(".")
            return (
                f"[SIMULATED] {ai_result}\n\n"
                + f"📊 AI CONTENT ANALYSIS\n━━━━━━━━━━━━━━━━━━━━━━━━━\n📄 Content Statistics:\n  • Words: {len(words)}\n  • Lines: {len(lines)}\n  • Sentences: ~{len(sentences)}\n  • Characters: {len(content)}\n\n🧠 AI Analysis Insights:\n  • Content Type: Technical/Documentation\n  • Complexity Level: Medium\n  • Readability: Good structure detected\n  • Key Topics: {', '.join(words[:5])}...\n\n🎯 AI Recommendations:\n  • Add more examples for clarity\n  • Consider adding diagrams\n  • Structure looks well organized\n  • Content appears comprehensive\n\n💡 This is enhanced analysis. Real AI would provide:\n  • Sentiment analysis\n  • Topic modeling\n  • Technical accuracy verification\n  • Style and tone recommendations\n━━━━━━━━━━━━━━━━━━━━━━━━━"
            )
        return f"[REAL AI]\n📊 AI CONTENT ANALYSIS\n━━━━━━━━━━━━━━━━━━━━━━━━━\n{ai_result}\n━━━━━━━━━━━━━━━━━━━━━━━━━"

    async def _generate_content(self, content: str, file_path: Path) -> str:
        """Generate content with real AI if available"""
        prompt = content.strip()
        ai_result = await self._call_real_ai(prompt, purpose="generate")
        if ai_result.startswith("[ERROR]"):
            # fallback to simulated
            return (
                f"[SIMULATED] {ai_result}\n\n"
                + f"✨ AI CONTENT GENERATION\n━━━━━━━━━━━━━━━━━━━━━━━━━\n🎯 Prompt: {content[:80]}{'...' if len(content) > 80 else ''}\n\n🤖 Generated Content:\n\n# AI-Generated Section\n\nBased on your prompt, here's intelligently generated content:\n\n## Key Points\n- Advanced AI processing capabilities\n- Seamless integration with existing workflows\n- Enhanced productivity through automation\n- Intelligent content analysis and generation\n\n## Benefits\n- **Efficiency**: Automated content processing\n- **Quality**: AI-enhanced accuracy and consistency\n- **Scalability**: Handle large volumes of content\n- **Intelligence**: Deep understanding and insights\n\n## Implementation\nReal AI generation would create contextually relevant,\nhigh-quality content tailored to your specific needs.\n\n💡 For production use, connect to:\n  • GPT-4 for advanced text generation\n  • Claude for analytical content\n  • Local models for privacy-focused generation\n━━━━━━━━━━━━━━━━━━━━━━━━━"
            )
        return f"[REAL AI]\n✨ AI CONTENT GENERATION\n━━━━━━━━━━━━━━━━━━━━━━━━━\n{ai_result}\n━━━━━━━━━━━━━━━━━━━━━━━━━"

    async def _summarize_content(self, content: str, file_path: Path) -> str:
        """Summarize content with real AI if available"""
        prompt = (
            "Summarize the following content in a concise, clear, and structured way. "
            "Highlight the main points and key takeaways.\n\nContent:\n"
            + content.strip()
        )
        ai_result = await self._call_real_ai(prompt, purpose="summarize")
        if ai_result.startswith("[ERROR]"):
            # fallback to simulated
            sentences = [s.strip() for s in content.split(".") if s.strip()]
            key_sentences = sentences[:3] if len(sentences) >= 3 else sentences
            return (
                f"[SIMULATED] {ai_result}\n\n"
                + f"📝 AI CONTENT SUMMARY\n━━━━━━━━━━━━━━━━━━━━━━━━━\n📊 Original: {len(content)} characters, {len(sentences)} sentences\n\n🎯 Key Points Summary:\n{chr(10).join(f'• {sentence}.' for sentence in key_sentences)}\n\n🧠 AI Analysis:\n  • Main Theme: Technology and AI integration\n  • Tone: Professional and informative\n  • Complexity: Medium technical level\n  • Structure: Well-organized content\n\n💡 Enhanced Summary (Real AI would provide):\n  • Contextual understanding\n  • Key concept extraction\n  • Relationship mapping\n  • Actionable insights\n━━━━━━━━━━━━━━━━━━━━━━━━━"
            )
        return f"[REAL AI]\n📝 AI CONTENT SUMMARY\n━━━━━━━━━━━━━━━━━━━━━━━━━\n{ai_result}\n━━━━━━━━━━━━━━━━━━━━━━━━━"

    async def _enhance_content(self, content: str, file_path: Path) -> str:
        """Enhance content with real AI if available"""
        prompt = (
            "Improve and enhance the following content. "
            "Make it clearer, more detailed, and better structured.\n\nContent:\n"
            + content.strip()
        )
        ai_result = await self._call_real_ai(prompt, purpose="enhance")
        if ai_result.startswith("[ERROR]"):
            # fallback to simulated
            enhanced_content = content.replace("\n", "\n  ").strip()
            return (
                f"[SIMULATED] {ai_result}\n\n"
                + f"🚀 AI CONTENT ENHANCEMENT\n━━━━━━━━━━━━━━━━━━━━━━━━━\n📝 Original Content:\n{content[:100]}{'...' if len(content) > 100 else ''}\n\n✨ Enhanced Version:\n  {enhanced_content}\n\n🎯 AI Enhancements Applied:\n  • Improved formatting and structure\n  • Enhanced clarity and readability\n  • Better organization of ideas\n  • Professional tone optimization\n\n💡 Advanced Enhancements (Real AI would provide):\n  • Grammar and style improvements\n  • Technical accuracy verification\n  • Consistency checks\n  • SEO optimization\n  • Accessibility improvements\n━━━━━━━━━━━━━━━━━━━━━━━━━"
            )
        return f"[REAL AI]\n🚀 AI CONTENT ENHANCEMENT\n━━━━━━━━━━━━━━━━━━━━━━━━━\n{ai_result}\n━━━━━━━━━━━━━━━━━━━━━━━━━"


async def main():
    """Main function with enhanced interface"""
    import sys

    print("🤖 Enhanced AI Markdown Runner")
    print("═" * 60)

    if len(sys.argv) != 2:
        print("Usage: python enhanced_ai_runner.py <markdown_file>")
        print("\nExample markdown with AI blocks:")
        print("```ai execute")
        print("Analyze this content")
        print("```")
        print("\nSupported AI types: execute, analyze, generate, summarize, enhance")
        return

    file_path = sys.argv[1]
    runner = EnhancedAIMarkdownRunner()

    print(f"📂 Processing: {file_path}")
    print("─" * 60)

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
        analysis = await runner._analyze_content(
            result["content_preview"], Path(file_path)
        )
        print(analysis)

    print("\n" + "═" * 60)
    print("✅ Processing Complete!")
    print("═" * 60)


if __name__ == "__main__":
    asyncio.run(main())
