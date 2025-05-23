# This script collects text from selected files in your workspace for LLM fine-tuning.
# It concatenates the contents of .py, .md, .txt, and .html files into a single training file.

import glob
import os

# File extensions to include
EXTENSIONS = [".py", ".md", ".txt", ".html"]

# Root directory (adjust if needed)
ROOT = os.path.dirname(os.path.abspath(__file__))

# Output file
OUTPUT = os.path.join(ROOT, "llm_training_data.txt")

with open(OUTPUT, "w", encoding="utf-8") as outfile:
    for ext in EXTENSIONS:
        for filepath in glob.glob(f"**/*{ext}", root_dir=ROOT, recursive=True):
            full_path = os.path.join(ROOT, filepath)
            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as infile:
                    outfile.write(f"\n\n--- FILE: {filepath} ---\n\n")
                    outfile.write(infile.read())
            except Exception as e:
                print(f"Could not read {filepath}: {e}")

print(f"Training data written to {OUTPUT}")
