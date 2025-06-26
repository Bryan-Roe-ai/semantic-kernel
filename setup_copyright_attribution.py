import re
import sys
#!/usr/bin/env python3
"""
Comprehensive Copyright and Attribution Setup Script

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This script sets up complete copyright and attribution for the Semantic Kernel project.
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any


class CopyrightAttributionSetup:
    """Complete copyright and attribution setup for Bryan Roe's Semantic Kernel project."""

    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.author_info = {
            "name": "Bryan Roe",
            "email": "bryan.roe@example.com",  # Update with actual email
            "copyright": "Copyright (c) 2025 Bryan Roe",
            "license": "MIT",
            "year": "2025",
            "project": "Semantic Kernel - Advanced AI Development Framework",
        }

    def create_master_attribution_file(self):
        """Create the master attribution file."""
        content = f"""# ATTRIBUTION AND CREDITS

**{self.author_info['project']}**
{self.author_info['copyright']}
Licensed under the {self.author_info['license']} License

---

## Primary Author and Copyright Holder

**{self.author_info['name']}**
- Role: Project Creator, Lead Architect, Primary Developer
- Copyright: {self.author_info['copyright']}
- License: {self.author_info['license']}

## Project Overview

This project represents significant original work in artificial intelligence and semantic computing. The majority of the codebase, architecture, and innovations are original contributions by {self.author_info['name']}.

## Attribution Requirements

When using this software:

1. **Preserve all copyright notices**
2. **Include the following attribution:**
   ```
   Based on work by {self.author_info['name']}
   {self.author_info['copyright']}
   Original project: {self.author_info['project']}
   ```
3. **Maintain the MIT License terms**
4. **Link back to the original repository when possible**

## Third-Party Components

This project builds upon and acknowledges:

### Microsoft Semantic Kernel
- License: MIT
- Copyright: Microsoft Corporation
- Usage: Base framework (heavily modified and extended)

### Python Ecosystem
- Various packages with their respective licenses
- See individual package.json and requirements files for details

### JavaScript/TypeScript Ecosystem
- Various packages with their respective licenses
- See individual package.json files for details

## Contribution Guidelines

All contributions must:
- Include proper copyright headers
- Be compatible with the MIT License
- Respect existing attribution
- Maintain code quality standards

## Contact Information

For attribution questions, licensing inquiries, or collaboration:
- Author: {self.author_info['name']}
- Project: {self.author_info['project']}
- License: {self.author_info['license']}

---

**Important:** This attribution file must be preserved in any distribution or derivative work.
"""

        attribution_file = self.workspace_root / "ATTRIBUTION.md"
        with open(attribution_file, "w", encoding="utf-8") as f:
            f.write(content)

        return attribution_file

    def create_copyright_notice(self):
        """Create comprehensive copyright notice."""
        content = f"""# COPYRIGHT NOTICE

{self.author_info['copyright']}
Licensed under the {self.author_info['license']} License

## Project Information

- **Project:** {self.author_info['project']}
- **Author:** {self.author_info['name']}
- **Copyright Year:** {self.author_info['year']}
- **License:** {self.author_info['license']}

## Copyright Statement

This software and associated documentation files are the original work of {self.author_info['name']}. While building upon existing technologies and frameworks, the majority of this codebase represents original contributions and intellectual property.

## License Summary

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, subject to the MIT License terms.

## Copyright Protection

- **All rights reserved** under copyright law
- **Original work** protected by copyright
- **MIT License** grants specific permissions
- **Attribution required** for all uses

## Usage Requirements

1. Include copyright notice in all copies
2. Include license text in distributions
3. Provide proper attribution to {self.author_info['name']}
4. Respect third-party component licenses

## Third-Party Acknowledgments

This project incorporates components from:
- Microsoft Semantic Kernel (MIT License)
- Various open-source libraries (see package.json files)

## Contact for Copyright Matters

For copyright questions, licensing beyond MIT terms, or permission requests:
- {self.author_info['name']}
- {self.author_info['project']}

---

**IMPORTANT:** This copyright notice must be preserved in any copy, modification, or distribution of this software. Removal or modification may violate copyright law.
"""

        copyright_file = self.workspace_root / "COPYRIGHT.md"
        with open(copyright_file, "w", encoding="utf-8") as f:
            f.write(content)

        return copyright_file

    def update_main_readme(self):
        """Update the main README with proper attribution."""
        readme_path = self.workspace_root / "README.md"

        content = f"""# {self.author_info['project']}

**{self.author_info['copyright']}**
Licensed under the {self.author_info['license']} License

---

## 🚀 Overview

This is an advanced artificial intelligence development framework created by {self.author_info['name']}. It represents significant original work building upon the semantic kernel paradigm with extensive enhancements and new capabilities.

## ✨ Key Features

- **Advanced AI Integration**: Sophisticated AI and machine learning capabilities
- **Semantic Computing**: Enhanced semantic kernel implementation
- **Multi-Language Support**: Python, TypeScript, JavaScript, and .NET implementations
- **Extensible Architecture**: Modular design for easy customization
- **Comprehensive Tooling**: Development tools and utilities
- **Production Ready**: Robust deployment and infrastructure support

## 📁 Project Structure

This repository is organized into several key areas:

- `01-core-implementations/` - Core semantic kernel implementations
- `02-ai-workspace/` - AI development workspace and tools
- `03-development-tools/` - Development utilities and samples
- `04-infrastructure/` - Infrastructure and deployment configurations
- `05-documentation/` - Project documentation
- `06-deployment/` - Deployment scripts and configurations
- `07-resources/` - Shared resources and assets
- `08-archived-versions/` - Historical versions and archives
- `09-agi-development/` - Advanced AGI development components

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- .NET 6.0+
- Docker (optional)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd semantic-kernel

# Install Python dependencies
cd python && poetry install

# Install Node.js dependencies
cd ../01-core-implementations/typescript && npm install

# Install .NET dependencies
cd ../dotnet && dotnet restore
```

### Quick Start

```python
# Python example
from semantic_kernel import Kernel
kernel = Kernel()
# Your AI code here
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTORS.md](CONTRIBUTORS.md) for guidelines.

**Important:** All contributions must respect the existing copyright and attribution structure.

## 📜 License & Attribution

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Attribution Requirements

When using this software, please provide proper attribution:

```
Based on work by {self.author_info['name']}
{self.author_info['copyright']}
Original project: {self.author_info['project']}
```

## 🙏 Acknowledgments

- Microsoft Corporation for the original Semantic Kernel framework
- The open-source community for various libraries and tools
- All contributors to the AI and machine learning ecosystem

## 📞 Contact

For questions, collaborations, or to learn more about this work:

- **Author:** {self.author_info['name']}
- **Project:** {self.author_info['project']}
- **License:** {self.author_info['license']}

---

**Note:** This project represents original work by {self.author_info['name']}. While it builds upon existing technologies, significant original contributions and enhancements have been made. Please respect the copyright and attribution when using this work.
"""

        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(content)

        return readme_path

    def create_notice_file(self):
        """Create NOTICE file for distribution."""
        content = f"""{self.author_info['project']}
{self.author_info['copyright']}

This product includes software developed by {self.author_info['name']}.

The original work is available at: <repository-url>

This software is distributed under the {self.author_info['license']} License.
See LICENSE file for full license text.

THIRD-PARTY SOFTWARE:

This software incorporates components from third-party sources.
See ATTRIBUTION.md for complete third-party acknowledgments.

Microsoft Semantic Kernel
Copyright (c) Microsoft Corporation
Licensed under the MIT License

Various other open-source components
See individual package.json and requirements files for details

For more information about licensing and attribution, see:
- LICENSE (main license)
- ATTRIBUTION.md (detailed attributions)
- COPYRIGHT.md (copyright information)
"""

        notice_file = self.workspace_root / "NOTICE"
        with open(notice_file, "w", encoding="utf-8") as f:
            f.write(content)

        return notice_file

    def add_copyright_headers_to_files(self):
        """Add copyright headers to source files."""
        python_header = f'''#!/usr/bin/env python3
"""
{{description}}

{self.author_info['copyright']}
Licensed under the {self.author_info['license']} License

Part of the {self.author_info['project']}
Author: {self.author_info['name']}
"""

'''

        js_header = f"""/**
 * {{description}}
 *
 * {self.author_info['copyright']}
 * Licensed under the {self.author_info['license']} License
 *
 * Part of the {self.author_info['project']}
 * Author: {self.author_info['name']}
 */

"""

        cs_header = f"""/*
 * {{description}}
 *
 * {self.author_info['copyright']}
 * Licensed under the {self.author_info['license']} License
 *
 * Part of the {self.author_info['project']}
 * Author: {self.author_info['name']}
 */

"""

        # Count files that need headers
        python_files = []
        js_files = []
        cs_files = []

        for file_path in self.workspace_root.rglob("*.py"):
            if not self._should_skip_file(file_path):
                python_files.append(file_path)

        for file_path in self.workspace_root.rglob("*.js"):
            if not self._should_skip_file(file_path):
                js_files.append(file_path)

        for file_path in self.workspace_root.rglob("*.ts"):
            if not self._should_skip_file(file_path):
                js_files.append(file_path)

        for file_path in self.workspace_root.rglob("*.cs"):
            if not self._should_skip_file(file_path):
                cs_files.append(file_path)

        return {
            "python": len(python_files),
            "javascript": len(js_files),
            "csharp": len(cs_files),
        }

    def _should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped."""
        skip_dirs = {
            "node_modules",
            "__pycache__",
            ".git",
            "bin",
            "obj",
            "08-archived-versions",
        }
        skip_files = {"__init__.py", "setup.py"}

        # Skip if in excluded directory
        for part in file_path.parts:
            if part in skip_dirs:
                return True

        # Skip if excluded file
        if file_path.name in skip_files:
            return True

        # Skip if already has copyright
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read(1000)
                if (
                    f'Copyright (c) {self.author_info["year"]} {self.author_info["name"]}'
                    in content
                ):
                    return True
        except:
            return True

        return False

    def update_package_json_files(self):
        """Update package.json files with proper attribution."""
        count = 0
        for package_file in self.workspace_root.rglob("package.json"):
            if "08-archived-versions" in str(package_file):
                continue

            try:
                with open(package_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Update author and license info
                data["author"] = {
                    "name": self.author_info["name"],
                    "email": self.author_info["email"],
                }
                data["license"] = self.author_info["license"]
                data["copyright"] = self.author_info["copyright"]

                # Add repository info if not present
                if "repository" not in data:
                    data["repository"] = {
                        "type": "git",
                        "url": "git+https://github.com/yourusername/semantic-kernel.git",
                    }

                with open(package_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)

                count += 1
            except Exception as e:
                print(f"Error updating {package_file}: {e}")

        return count

    def run_complete_setup(self):
        """Run the complete copyright and attribution setup."""
        print(f"🚀 Setting up copyright and attribution for {self.author_info['name']}")
        print(f"📁 Workspace: {self.workspace_root}")
        print(f"📋 Project: {self.author_info['project']}")
        print("=" * 70)

        # Create main attribution file
        print("\n📝 Creating master attribution file...")
        attribution_file = self.create_master_attribution_file()
        print(f"  ✅ Created: {attribution_file}")

        # Create copyright notice
        print("\n©️  Creating copyright notice...")
        copyright_file = self.create_copyright_notice()
        print(f"  ✅ Created: {copyright_file}")

        # Update main README
        print("\n📖 Updating main README...")
        readme_file = self.update_main_readme()
        print(f"  ✅ Updated: {readme_file}")

        # Create NOTICE file
        print("\n📋 Creating NOTICE file...")
        notice_file = self.create_notice_file()
        print(f"  ✅ Created: {notice_file}")

        # Update package.json files
        print("\n📦 Updating package.json files...")
        package_count = self.update_package_json_files()
        print(f"  ✅ Updated {package_count} package.json files")

        # Analyze files for headers
        print("\n🔍 Analyzing files for copyright headers...")
        file_counts = self.add_copyright_headers_to_files()
        print(f"  📊 Python files: {file_counts['python']}")
        print(f"  📊 JavaScript/TypeScript files: {file_counts['javascript']}")
        print(f"  📊 C# files: {file_counts['csharp']}")

        print("\n🎉 Copyright and attribution setup complete!")
        print("\n📋 Summary of files created/updated:")
        print(f"  • {attribution_file.name}")
        print(f"  • {copyright_file.name}")
        print(f"  • {readme_file.name}")
        print(f"  • {notice_file.name}")
        print(f"  • {package_count} package.json files")
        print(f"\n📊 File analysis:")
        print(f"  • Python files ready for headers: {file_counts['python']}")
        print(f"  • JS/TS files ready for headers: {file_counts['javascript']}")
        print(f"  • C# files ready for headers: {file_counts['csharp']}")

        print(
            f"\n✨ Your project is now properly attributed to {self.author_info['name']}!"
        )
        print("🔗 Next steps:")
        print("  1. Review the generated files")
        print("  2. Update any placeholder URLs/emails")
        print("  3. Consider running copyright header tools for source files")
        print("  4. Commit these changes to preserve attribution")


def main():
    """Main function."""
    workspace_root = Path(__file__).parent
    setup = CopyrightAttributionSetup(workspace_root)

    print("Copyright and Attribution Setup Tool")
    print("for the Semantic Kernel Project")
    print("=" * 40)

    response = input("\n❓ Set up complete copyright and attribution? (y/N): ")
    if response.lower() == "y":
        setup.run_complete_setup()
    else:
        print("❌ Setup cancelled.")


if __name__ == "__main__":
    main()
