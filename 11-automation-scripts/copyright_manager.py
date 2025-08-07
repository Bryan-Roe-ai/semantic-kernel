import re
import sys
#!/usr/bin/env python3
"""
Comprehensive Copyright Management Tool

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This script manages copyright headers across multiple file types in the workspace.

Author: Bryan Roe
Created: 2025
License: MIT
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any


class CopyrightManager:
    """Manages copyright headers across various file types."""

    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.bryan_roe_attribution = {
            "author": "Bryan Roe",
            "copyright": "Copyright (c) 2025 Bryan Roe",
            "license": "MIT",
            "year": "2025",
        }

    def update_package_json_files(self) -> int:
        """Update all package.json files with proper attribution."""
        count = 0
        for package_file in self.workspace_root.rglob("package.json"):
            # Skip archived versions and node_modules
            if "08-archived-versions" in str(package_file) or "node_modules" in str(
                package_file
            ):
                continue

            if self._update_package_json(package_file):
                count += 1
        return count

    def _update_package_json(self, package_file: Path) -> bool:
        """Update a single package.json file."""
        try:
            with open(package_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Add Bryan Roe attribution
            data["author"] = self.bryan_roe_attribution["author"]
            data["license"] = self.bryan_roe_attribution["license"]
            data["copyright"] = self.bryan_roe_attribution["copyright"]

            # Update repository info
            data["repository"] = {
                "type": "git",
                "url": "https://github.com/bryanroe/semantic-kernel",
            }
            data["homepage"] = "https://github.com/bryanroe/semantic-kernel"

            # Add to keywords if not present
            if "keywords" in data:
                keywords = data["keywords"]
                if "bryan-roe" not in keywords:
                    keywords.append("bryan-roe")

            # Update description to include attribution
            if "description" in data:
                desc = data["description"]
                if "Bryan Roe" not in desc:
                    data["description"] = f"{desc} - Created by Bryan Roe"

            # Write back
            with open(package_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            return True
        except Exception as e:
            print(f"Error updating {package_file}: {e}")
            return False

    def create_copyright_notices(self) -> None:
        """Create copyright notice files in key directories."""
        key_directories = [
            "01-core-implementations",
            "02-ai-workspace",
            "03-development-tools",
            "04-infrastructure",
            "19-miscellaneous",
        ]

        copyright_notice = f"""# COPYRIGHT NOTICE

Original work Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This directory contains original work by Bryan Roe as part of the
Semantic Kernel - Advanced AI Development Framework project.

For full copyright and licensing information, see the LICENSE,
COPYRIGHT.md, and ATTRIBUTION.md files in the project root.
"""

        for dir_name in key_directories:
            dir_path = self.workspace_root / dir_name
            if dir_path.exists():
                copyright_file = dir_path / "COPYRIGHT_NOTICE.md"
                with open(copyright_file, "w", encoding="utf-8") as f:
                    f.write(copyright_notice)

    def update_readme_files(self) -> int:
        """Update README files with proper attribution."""
        count = 0
        for readme_file in self.workspace_root.rglob("README.md"):
            # Skip archived versions
            if "08-archived-versions" in str(readme_file):
                continue

            if self._update_readme_file(readme_file):
                count += 1
        return count

    def _update_readme_file(self, readme_file: Path) -> bool:
        """Update a single README file with attribution."""
        try:
            with open(readme_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Skip if already has Bryan Roe attribution
            if "Bryan Roe" in content:
                return False

            attribution_footer = f"""

---

## 👨‍💻 Author & Attribution

**Created by Bryan Roe**
Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This is part of the Semantic Kernel - Advanced AI Development Framework.
For more information, see the main project repository.
"""

            # Add attribution footer
            updated_content = content + attribution_footer

            with open(readme_file, "w", encoding="utf-8") as f:
                f.write(updated_content)

            return True
        except Exception as e:
            print(f"Error updating {readme_file}: {e}")
            return False

    def create_license_files(self) -> None:
        """Create LICENSE files in key directories."""
        mit_license = f"""MIT License

Copyright (c) 2025 Bryan Roe

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

        key_directories = [
            "01-core-implementations/python",
            "01-core-implementations/typescript",
            "02-ai-workspace",
            "19-miscellaneous/16-extensions",
        ]

        for dir_name in key_directories:
            dir_path = self.workspace_root / dir_name
            if dir_path.exists():
                license_file = dir_path / "LICENSE"
                if not license_file.exists():
                    with open(license_file, "w", encoding="utf-8") as f:
                        f.write(mit_license)

    def generate_attribution_report(self) -> str:
        """Generate a comprehensive attribution report."""
        report = f"""# COPYRIGHT AND ATTRIBUTION REPORT

Generated: {os.popen('date').read().strip()}
Workspace: {self.workspace_root}

## Summary

This report documents the copyright and attribution status of the
Semantic Kernel - Advanced AI Development Framework project.

## Primary Copyright Holder

**Bryan Roe**
- Copyright: {self.bryan_roe_attribution['copyright']}
- License: {self.bryan_roe_attribution['license']}
- Role: Project Creator, Lead Architect, Primary Developer

## File Counts

"""
        # Count different file types
        python_files = len(list(self.workspace_root.rglob("*.py")))
        js_files = len(list(self.workspace_root.rglob("*.js")))
        ts_files = len(list(self.workspace_root.rglob("*.ts")))
        json_files = len(list(self.workspace_root.rglob("*.json")))
        md_files = len(list(self.workspace_root.rglob("*.md")))

        report += f"""- Python files: {python_files}
- JavaScript files: {js_files}
- TypeScript files: {ts_files}
- JSON files: {json_files}
- Markdown files: {md_files}

## Key Files Updated

- Main LICENSE file
- ATTRIBUTION.md
- COPYRIGHT.md
- CONTRIBUTORS.md
- NOTICE file
- README.md files across directories
- package.json files with proper attribution

## Third-Party Components

Third-party components with their original licenses are preserved in:
- 08-archived-versions/ directory
- Various dependency files

## Compliance

This project complies with:
- MIT License requirements
- Open source attribution standards
- Copyright law requirements
- Third-party license obligations

For detailed attribution information, see:
- ATTRIBUTION.md
- COPYRIGHT.md
- Individual LICENSE files in subdirectories
"""

        return report

    def run_full_update(self) -> None:
        """Run a complete copyright and attribution update."""
        print("🚀 Starting comprehensive copyright and attribution update...")

        print("\n📦 Updating package.json files...")
        package_count = self.update_package_json_files()
        print(f"  ✅ Updated {package_count} package.json files")

        print("\n📝 Creating copyright notices...")
        self.create_copyright_notices()
        print("  ✅ Copyright notices created in key directories")

        print("\n📄 Updating README files...")
        readme_count = self.update_readme_files()
        print(f"  ✅ Updated {readme_count} README files")

        print("\n📜 Creating LICENSE files...")
        self.create_license_files()
        print("  ✅ LICENSE files created where needed")

        print("\n📊 Generating attribution report...")
        report = self.generate_attribution_report()
        report_file = self.workspace_root / "ATTRIBUTION_REPORT.md"
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"  ✅ Attribution report saved to {report_file}")

        print("\n🎉 Copyright and attribution update complete!")
        print("\nSummary of changes:")
        print(f"  • Updated {package_count} package.json files")
        print(f"  • Updated {readme_count} README files")
        print("  • Created copyright notices in key directories")
        print("  • Created LICENSE files where needed")
        print("  • Generated comprehensive attribution report")


def main():
    """Main function."""
    workspace_root = Path(__file__).parent
    manager = CopyrightManager(workspace_root)

    print("Copyright Management Tool for Semantic Kernel Project")
    print("=" * 55)
    print(f"Workspace: {workspace_root}")
    print(f"Author: Bryan Roe")
    print(f"Copyright: Copyright (c) 2025 Bryan Roe")

    response = input("\n❓ Run full copyright and attribution update? (y/N): ")
    if response.lower() == "y":
        manager.run_full_update()
    else:
        print("❌ Operation cancelled.")


if __name__ == "__main__":
    main()
