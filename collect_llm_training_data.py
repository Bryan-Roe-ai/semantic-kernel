# This script collects text from selected files in your workspace for LLM fine-tuning.
# It concatenates the contents of .py, .md, .txt, and .html files into a single training file.

import os

# File extensions to include
EXTENSIONS = [".py", ".md", ".txt", ".html"]

# Root directory (adjust if needed)
ROOT = os.path.dirname(os.path.abspath(__file__))

# Output file
OUTPUT = os.path.join(ROOT, "llm_training_data.txt")

with open(OUTPUT, "w", encoding="utf-8") as outfile:
    for dirpath, _, filenames in os.walk(ROOT):
        for filename in filenames:
            if any(filename.endswith(ext) for ext in EXTENSIONS):
                full_path = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(full_path, ROOT)
                try:
                    with open(
                        full_path, "r", encoding="utf-8", errors="ignore"
                    ) as infile:
                        outfile.write(f"\n\n--- FILE: {rel_path} ---\n\n")
                        outfile.write(infile.read())
                except Exception as e:
                    print(f"Could not read {rel_path}: {e}")

print(f"Training data written to {OUTPUT}")
