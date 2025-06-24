#!/usr/bin/env python3
"""
Copyright and Attribution Status Report

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This script generates a comprehensive report of the copyright and attribution status.
"""

import json
from pathlib import Path
from datetime import datetime


class CopyrightStatusReport:
    """Generate comprehensive copyright and attribution status report."""
    
    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root
        self.author = "Bryan Roe"
        self.year = "2025"
    
    def check_key_files(self):
        """Check status of key attribution files."""
        key_files = {
            'LICENSE': 'Main license file',
            'ATTRIBUTION.md': 'Attribution and credits',
            'COPYRIGHT.md': 'Copyright notice',
            'CONTRIBUTORS.md': 'Contributors information',
            'NOTICE': 'Distribution notice',
            'README.md': 'Main project documentation'
        }
        
        status = {}
        for filename, description in key_files.items():
            file_path = self.workspace_root / filename
            status[filename] = {
                'exists': file_path.exists(),
                'description': description,
                'size': file_path.stat().st_size if file_path.exists() else 0,
                'has_bryan_roe': False
            }
            
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        status[filename]['has_bryan_roe'] = 'Bryan Roe' in content
                except:
                    pass
        
        return status
    
    def count_files_with_headers(self):
        """Count files that have copyright headers."""
        counts = {
            'python': {'total': 0, 'with_header': 0},
            'javascript': {'total': 0, 'with_header': 0},
            'typescript': {'total': 0, 'with_header': 0},
            'csharp': {'total': 0, 'with_header': 0}
        }
        
        # Sample key directories only to avoid processing too many files
        sample_dirs = [
            '',  # Root
            '02-ai-workspace',
            '03-development-tools',
            '09-agi-development'
        ]
        
        for dir_name in sample_dirs:
            if dir_name:
                base_path = self.workspace_root / dir_name
            else:
                base_path = self.workspace_root
            
            if not base_path.exists():
                continue
            
            # Python files
            for file_path in base_path.glob('*.py'):
                if self._is_key_file(file_path):
                    counts['python']['total'] += 1
                    if self._has_copyright_header(file_path):
                        counts['python']['with_header'] += 1
            
            # JavaScript files
            for file_path in base_path.glob('*.js'):
                if self._is_key_file(file_path):
                    counts['javascript']['total'] += 1
                    if self._has_copyright_header(file_path):
                        counts['javascript']['with_header'] += 1
            
            # TypeScript files
            for file_path in base_path.glob('*.ts'):
                if self._is_key_file(file_path):
                    counts['typescript']['total'] += 1
                    if self._has_copyright_header(file_path):
                        counts['typescript']['with_header'] += 1
            
            # C# files
            for file_path in base_path.glob('*.cs'):
                if self._is_key_file(file_path):
                    counts['csharp']['total'] += 1
                    if self._has_copyright_header(file_path):
                        counts['csharp']['with_header'] += 1
        
        return counts
    
    def _is_key_file(self, file_path: Path) -> bool:
        """Check if this is a key file to analyze."""
        skip_patterns = ['__pycache__', 'node_modules', '.git', 'bin', 'obj']
        path_str = str(file_path)
        
        for pattern in skip_patterns:
            if pattern in path_str:
                return False
        
        # Focus on key files
        key_patterns = ['cli', 'runner', 'processor', 'manager', 'setup', 'demo', 'test', 'main', 'app', 'server']
        filename = file_path.name.lower()
        
        return any(pattern in filename for pattern in key_patterns)
    
    def _has_copyright_header(self, file_path: Path) -> bool:
        """Check if file has copyright header."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read(1000)
                return f'Copyright (c) {self.year} {self.author}' in content
        except:
            return False
    
    def check_package_json_attribution(self):
        """Check package.json files for proper attribution."""
        package_files = list(self.workspace_root.rglob('package.json'))
        
        # Filter out archived and node_modules
        package_files = [
            f for f in package_files 
            if '08-archived-versions' not in str(f) and 'node_modules' not in str(f)
        ]
        
        with_attribution = 0
        total = len(package_files)
        
        for package_file in package_files[:10]:  # Sample first 10
            try:
                with open(package_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if ('author' in data and 
                        isinstance(data['author'], dict) and 
                        data['author'].get('name') == self.author):
                        with_attribution += 1
            except:
                pass
        
        return {'total': total, 'with_attribution': with_attribution, 'sample_size': min(10, total)}
    
    def generate_report(self):
        """Generate comprehensive status report."""
        print("🔍 COMPREHENSIVE COPYRIGHT & ATTRIBUTION STATUS REPORT")
        print("=" * 60)
        print(f"📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📁 Workspace: {self.workspace_root}")
        print(f"👤 Author: {self.author}")
        print(f"📅 Copyright Year: {self.year}")
        
        # Check key files
        print("\n📋 KEY ATTRIBUTION FILES STATUS")
        print("-" * 35)
        key_files_status = self.check_key_files()
        
        for filename, info in key_files_status.items():
            status_icon = "✅" if info['exists'] else "❌"
            bryan_icon = "👤" if info['has_bryan_roe'] else "❓"
            size_kb = info['size'] / 1024 if info['size'] > 0 else 0
            
            print(f"{status_icon} {bryan_icon} {filename:<15} ({size_kb:.1f}KB) - {info['description']}")
        
        # Check file headers (sample)
        print("\n📝 COPYRIGHT HEADERS STATUS (Sample)")
        print("-" * 38)
        header_counts = self.count_files_with_headers()
        
        for file_type, counts in header_counts.items():
            if counts['total'] > 0:
                percentage = (counts['with_header'] / counts['total']) * 100
                print(f"{file_type.capitalize():<12}: {counts['with_header']:>3}/{counts['total']:<3} ({percentage:>5.1f}%) with headers")
        
        # Check package.json files
        print("\n📦 PACKAGE.JSON ATTRIBUTION STATUS")
        print("-" * 35)
        package_status = self.check_package_json_attribution()
        print(f"Sample checked: {package_status['sample_size']}/{package_status['total']} files")
        print(f"With attribution: {package_status['with_attribution']}/{package_status['sample_size']}")
        
        # Summary
        print(f"\n✨ SUMMARY")
        print("-" * 10)
        
        critical_files = ['LICENSE', 'ATTRIBUTION.md', 'COPYRIGHT.md', 'README.md']
        critical_exists = sum(1 for f in critical_files if key_files_status[f]['exists'])
        critical_has_bryan = sum(1 for f in critical_files if key_files_status[f]['has_bryan_roe'])
        
        print(f"Critical files exist: {critical_exists}/{len(critical_files)}")
        print(f"Critical files have Bryan Roe attribution: {critical_has_bryan}/{len(critical_files)}")
        
        total_sample_files = sum(counts['total'] for counts in header_counts.values())
        total_with_headers = sum(counts['with_header'] for counts in header_counts.values())
        
        if total_sample_files > 0:
            header_percentage = (total_with_headers / total_sample_files) * 100
            print(f"Key source files with headers: {total_with_headers}/{total_sample_files} ({header_percentage:.1f}%)")
        
        # Recommendations
        print(f"\n🎯 RECOMMENDATIONS")
        print("-" * 16)
        
        if critical_exists < len(critical_files):
            print("❗ Missing critical attribution files - run setup script")
        
        if critical_has_bryan < len(critical_files):
            print("❗ Some critical files missing Bryan Roe attribution")
        
        if total_sample_files > 0 and header_percentage < 80:
            print("💡 Consider adding copyright headers to more source files")
        
        print("\n🔗 NEXT STEPS")
        print("-" * 11)
        print("1. Review all generated attribution files")
        print("2. Update any placeholder URLs or contact information")
        print("3. Consider adding headers to remaining source files")
        print("4. Commit all attribution changes to preserve them")
        print("5. Share repository URL in attribution files")
        
        print(f"\n🎉 COPYRIGHT SETUP FOR {self.author.upper()} IS COMPLETE!")


def main():
    """Main function."""
    workspace_root = Path(__file__).parent
    reporter = CopyrightStatusReport(workspace_root)
    reporter.generate_report()


if __name__ == "__main__":
    main()
