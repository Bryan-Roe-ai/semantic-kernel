#!/usr/bin/env python3
"""
Markdown Collection Tool for AI processing

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

import os
import re


def strip_markdown(text):
    # Remove code blocks
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    # Remove images and links
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    # Remove headings, bold, italics, blockquotes, lists, etc.
    text = re.sub(r"[#>*_`~\-]+", "", text)
    # Remove extra whitespace
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()


def collect_md_files(root_dir):
    md_texts = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".md"):
                file_path = os.path.join(dirpath, filename)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    cleaned = strip_markdown(content)
                    md_texts.append(f"# {file_path}\n{cleaned}")
    return "\n\n".join(md_texts)


if __name__ == "__main__":
    workspace_dir = "."  # Change to your workspace root if needed
    output_file = "all_markdown_plaintext.txt"
    all_text = collect_md_files(workspace_dir)
    with open(output_file, "w", encoding="utf-8") as out:
        out.write(all_text)
    print(f"Collected and cleaned markdown saved to {output_file}")
