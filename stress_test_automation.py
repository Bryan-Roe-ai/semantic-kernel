import os
import time
from pathlib import Path
from collect_md_for_ai import collect_md_files


def generate_dataset(directory: str, num_files: int = 50, lines_per_file: int = 2000, repeats_per_line: int = 50) -> None:
    """Generate a large set of markdown files for stress testing."""
    Path(directory).mkdir(parents=True, exist_ok=True)
    sample_line = "# Sample Text " * repeats_per_line + "\n"
    content = sample_line * lines_per_file
    for i in range(num_files):
        with open(Path(directory) / f"file_{i}.md", "w", encoding="utf-8") as f:
            f.write(content)

def main() -> None:
    parser = argparse.ArgumentParser(description="Stress test automation script.")
    parser.add_argument(
        "--dataset-dir",
        type=str,
        default="stress_test_dataset",
        help="Directory to store the generated dataset (default: stress_test_dataset)."
    )
    args = parser.parse_args()
    dataset_dir = args.dataset_dir
    try:
        print(f"Generating dataset in {dataset_dir}...")
        generate_dataset(dataset_dir)
    except Exception as e:
        print(f"Error during dataset generation: {e}")
        return

    try:
        print("Processing markdown files...")
        start = time.time()
        result = collect_md_files(dataset_dir)
        elapsed = time.time() - start
        print(f"Processed {len(result)} characters in {elapsed:.2f}s")
    except Exception as e:
        print(f"Error during markdown file processing: {e}")
if __name__ == "__main__":
    main()
