import os
import time
from pathlib import Path
from collect_md_for_ai import collect_md_files


def generate_dataset(directory: str, num_files: int = 50, lines_per_file: int = 2000) -> None:
    """Generate a large set of markdown files for stress testing."""
    Path(directory).mkdir(parents=True, exist_ok=True)
    sample_line = "# Sample Text " * 50 + "\n"
    content = sample_line * lines_per_file
    for i in range(num_files):
        with open(Path(directory) / f"file_{i}.md", "w", encoding="utf-8") as f:
            f.write(content)

def main() -> None:
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    dataset_dir = f"stress_test_dataset_{timestamp}"
    print(f"Generating dataset in {dataset_dir}...")
    generate_dataset(dataset_dir)
    print("Processing markdown files...")
    start = time.time()
    result = collect_md_files(dataset_dir)
    elapsed = time.time() - start
    print(f"Processed {len(result)} characters in {elapsed:.2f}s")


if __name__ == "__main__":
    main()
