#!/usr/bin/env python3
"""
AI Markdown Processor
Processes markdown files with AI capabilities, executing embedded instructions and generating intelligent responses.
"""

import os
import re
import json
import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import markdown
import yaml
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class AIInstruction:
    """Represents an AI instruction embedded in markdown"""

    type: str  # 'execute', 'analyze', 'generate', 'transform'
    content: str
    parameters: Dict[str, Any]
    line_number: int


@dataclass
class ProcessingResult:
    """Result of processing a markdown file"""

    original_content: str
    processed_content: str
    ai_outputs: List[Dict[str, Any]]
    execution_time: float
    status: str
    errors: List[str]


class AIMarkdownProcessor:
    """Main processor for AI-enhanced markdown files"""

    def __init__(self, workspace_path: str = "/home/broe/semantic-kernel"):
        self.workspace_path = Path(workspace_path)
        self.ai_instructions_pattern = re.compile(
            r"```ai(?:\s+(\w+))?\s*\n(.*?)\n```", re.DOTALL | re.MULTILINE
        )
        self.metadata_pattern = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

        # AI processing capabilities
        self.capabilities = {
            "execute": self._execute_ai_instruction,
            "analyze": self._analyze_content,
            "generate": self._generate_content,
            "transform": self._transform_content,
            "summarize": self._summarize_content,
            "enhance": self._enhance_content,
        }

    async def process_markdown_file(
        self, file_path: Union[str, Path]
    ) -> ProcessingResult:
        """Process a markdown file with AI capabilities"""
        start_time = datetime.now()
        file_path = Path(file_path)

        try:
            # Read the markdown file
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Extract metadata if present
            metadata = self._extract_metadata(content)

            # Find AI instructions
            ai_instructions = self._extract_ai_instructions(content)

            # Process each AI instruction
            ai_outputs = []
            processed_content = content

            for instruction in ai_instructions:
                try:
                    result = await self._process_instruction(
                        instruction, metadata, file_path
                    )
                    ai_outputs.append(result)

                    # Replace the AI instruction with the result
                    processed_content = self._replace_instruction_with_result(
                        processed_content, instruction, result
                    )
                except Exception as e:
                    logger.error(f"Error processing instruction: {e}")
                    ai_outputs.append(
                        {
                            "instruction": instruction,
                            "error": str(e),
                            "status": "failed",
                        }
                    )

            execution_time = (datetime.now() - start_time).total_seconds()

            return ProcessingResult(
                original_content=content,
                processed_content=processed_content,
                ai_outputs=ai_outputs,
                execution_time=execution_time,
                status="success",
                errors=[],
            )

        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return ProcessingResult(
                original_content="",
                processed_content="",
                ai_outputs=[],
                execution_time=execution_time,
                status="failed",
                errors=[str(e)],
            )

    def _extract_metadata(self, content: str) -> Dict[str, Any]:
        """Extract YAML metadata from markdown front matter"""
        match = self.metadata_pattern.match(content)
        if match:
            try:
                return yaml.safe_load(match.group(1))
            except yaml.YAMLError as e:
                logger.warning(f"Invalid YAML metadata: {e}")
        return {}

    def _extract_ai_instructions(self, content: str) -> List[AIInstruction]:
        """Extract AI instructions from markdown content"""
        instructions = []

        for match in self.ai_instructions_pattern.finditer(content):
            instruction_type = match.group(1) or "execute"
            instruction_content = match.group(2).strip()
            line_number = content[: match.start()].count("\n") + 1

            # Parse parameters from the instruction content
            parameters = {}
            lines = instruction_content.split("\n")
            content_lines = []

            for line in lines:
                if line.startswith("@") and ":" in line:
                    key, value = line[1:].split(":", 1)
                    parameters[key.strip()] = value.strip()
                else:
                    content_lines.append(line)

            instructions.append(
                AIInstruction(
                    type=instruction_type,
                    content="\n".join(content_lines),
                    parameters=parameters,
                    line_number=line_number,
                )
            )

        return instructions

    async def _process_instruction(
        self, instruction: AIInstruction, metadata: Dict[str, Any], file_path: Path
    ) -> Dict[str, Any]:
        """Process a single AI instruction"""
        if instruction.type in self.capabilities:
            handler = self.capabilities[instruction.type]
            result = await handler(instruction, metadata, file_path)

            return {
                "instruction": instruction,
                "result": result,
                "status": "success",
                "timestamp": datetime.now().isoformat(),
            }
        else:
            raise ValueError(f"Unknown AI instruction type: {instruction.type}")

    async def _execute_ai_instruction(
        self, instruction: AIInstruction, metadata: Dict[str, Any], file_path: Path
    ) -> str:
        """Execute a general AI instruction"""
        prompt = f"""
        You are an AI assistant processing a markdown document.

        File: {file_path}
        Metadata: {json.dumps(metadata, indent=2)}

        Instruction: {instruction.content}
        Parameters: {json.dumps(instruction.parameters, indent=2)}

        Please provide a comprehensive response to this instruction.
        """

        return await self._generate_ai_response(prompt)

    async def _analyze_content(
        self, instruction: AIInstruction, metadata: Dict[str, Any], file_path: Path
    ) -> str:
        """Analyze content with AI"""
        prompt = f"""
        Analyze the following content from {file_path}:

        Content to analyze: {instruction.content}

        Please provide a detailed analysis including:
        - Key themes and concepts
        - Technical accuracy (if applicable)
        - Suggestions for improvement
        - Potential applications
        """

        return await self._generate_ai_response(prompt)

    async def _generate_content(
        self, instruction: AIInstruction, metadata: Dict[str, Any], file_path: Path
    ) -> str:
        """Generate new content based on instruction"""
        topic = instruction.parameters.get("topic", instruction.content)
        style = instruction.parameters.get("style", "professional")
        length = instruction.parameters.get("length", "medium")

        prompt = f"""
        Generate {style} content about: {topic}

        Requirements:
        - Length: {length}
        - Style: {style}
        - Context: {instruction.content}
        - File context: {file_path}

        Additional parameters: {json.dumps(instruction.parameters, indent=2)}

        Please generate comprehensive, well-structured content.
        """

        return await self._generate_ai_response(prompt)

    async def _transform_content(
        self, instruction: AIInstruction, metadata: Dict[str, Any], file_path: Path
    ) -> str:
        """Transform existing content"""
        transformation = instruction.parameters.get("transformation", "improve")

        prompt = f"""
        Transform the following content using transformation type: {transformation}

        Original content: {instruction.content}

        Transformation parameters: {json.dumps(instruction.parameters, indent=2)}

        Please provide the transformed content.
        """

        return await self._generate_ai_response(prompt)

    async def _summarize_content(
        self, instruction: AIInstruction, metadata: Dict[str, Any], file_path: Path
    ) -> str:
        """Summarize content"""
        length = instruction.parameters.get("length", "medium")
        focus = instruction.parameters.get("focus", "general")

        prompt = f"""
        Summarize the following content:

        Content: {instruction.content}

        Summary requirements:
        - Length: {length}
        - Focus: {focus}
        - Maintain key information

        Please provide a clear, concise summary.
        """

        return await self._generate_ai_response(prompt)

    async def _enhance_content(
        self, instruction: AIInstruction, metadata: Dict[str, Any], file_path: Path
    ) -> str:
        """Enhance existing content"""
        enhancement_type = instruction.parameters.get("type", "general")

        prompt = f"""
        Enhance the following content with type: {enhancement_type}

        Original content: {instruction.content}

        Enhancement parameters: {json.dumps(instruction.parameters, indent=2)}

        Please provide enhanced, improved content.
        """

        return await self._generate_ai_response(prompt)

    async def _generate_ai_response(self, prompt: str) -> str:
        """Generate AI response (placeholder - integrate with your AI model)"""
        # This is a placeholder - integrate with your preferred AI model
        # For now, return a simulated response

        response = f"""
        AI Response Generated at {datetime.now().isoformat()}

        Prompt processed: {prompt[:100]}...

        This is a simulated AI response. To activate real AI processing:
        1. Integrate with OpenAI API
        2. Connect to your AGI MCP server
        3. Use local language models
        4. Configure Semantic Kernel

        Response would contain intelligent analysis and generation based on the prompt.
        """

        return response

    def _replace_instruction_with_result(
        self, content: str, instruction: AIInstruction, result: Dict[str, Any]
    ) -> str:
        """Replace AI instruction with its result in the content"""
        # Find the original instruction block
        pattern = f"```ai(?:\\s+{instruction.type})?\\s*\\n.*?\\n```"

        # Create replacement content
        replacement = f"""
<!-- AI Processing Result -->
**AI Instruction Type:** {instruction.type}
**Processed:** {result['timestamp']}
**Status:** {result['status']}

{result['result']}

<!-- End AI Processing Result -->
"""

        # Replace the first occurrence
        return re.sub(pattern, replacement, content, count=1, flags=re.DOTALL)

    def save_processed_file(
        self, result: ProcessingResult, output_path: Union[str, Path]
    ):
        """Save the processed markdown file"""
        output_path = Path(output_path)

        # Create output directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Add processing metadata
        processing_metadata = f"""---
processed_by: AI Markdown Processor
processing_time: {result.execution_time}s
processing_date: {datetime.now().isoformat()}
status: {result.status}
ai_instructions_processed: {len(result.ai_outputs)}
---

{result.processed_content}
"""

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(processing_metadata)

        logger.info(f"Processed file saved to: {output_path}")

    async def process_directory(
        self,
        directory_path: Union[str, Path],
        output_directory: Optional[Union[str, Path]] = None,
    ) -> List[ProcessingResult]:
        """Process all markdown files in a directory"""
        directory_path = Path(directory_path)
        output_directory = (
            Path(output_directory) if output_directory else directory_path / "processed"
        )

        markdown_files = list(directory_path.rglob("*.md"))
        results = []

        logger.info(
            f"Processing {len(markdown_files)} markdown files from {directory_path}"
        )

        for md_file in markdown_files:
            logger.info(f"Processing: {md_file}")

            result = await self.process_markdown_file(md_file)
            results.append(result)

            # Save processed file
            relative_path = md_file.relative_to(directory_path)
            output_path = output_directory / relative_path
            self.save_processed_file(result, output_path)

        return results


# Command-line interface
async def main():
    """Main function for command-line usage"""
    import argparse

    parser = argparse.ArgumentParser(description="AI Markdown Processor")
    parser.add_argument("input", help="Input markdown file or directory")
    parser.add_argument("-o", "--output", help="Output file or directory")
    parser.add_argument(
        "-w", "--workspace", default="/home/broe/semantic-kernel", help="Workspace path"
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    processor = AIMarkdownProcessor(args.workspace)
    input_path = Path(args.input)

    if input_path.is_file():
        # Process single file
        result = await processor.process_markdown_file(input_path)

        if args.output:
            processor.save_processed_file(result, args.output)
        else:
            print("=" * 50)
            print("AI PROCESSED MARKDOWN")
            print("=" * 50)
            print(result.processed_content)
            print("=" * 50)
            print(f"Processing time: {result.execution_time:.2f}s")
            print(f"AI instructions processed: {len(result.ai_outputs)}")

    elif input_path.is_dir():
        # Process directory
        results = await processor.process_directory(input_path, args.output)

        print(f"Processed {len(results)} files")
        for i, result in enumerate(results, 1):
            print(f"{i}. Status: {result.status}, Time: {result.execution_time:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
