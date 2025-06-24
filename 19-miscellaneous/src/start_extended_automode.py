#!/usr/bin/env python3
"""
Start Extended Automode module

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

import os
import sys
import json
import time
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import psutil


class ExtendedAutoModeStartup:
    """Startup manager for Extended AutoMode"""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.src_dir = base_dir / "src"
        self.config_file = self.src_dir / "auto_mode_extended_config.json"
        self.extended_script = self.src_dir / "auto_mode_extended_operation.py"
        self.state_dir = base_dir / ".extended_automode"

    def check_python_version(self) -> Tuple[bool, str]:
        """Check Python version compatibility"""
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            return False, f"Python 3.8+ required, found {version.major}.{version.minor}"
        return True, f"Python {version.major}.{version.minor}.{version.micro}"

    def check_dependencies(self) -> Tuple[bool, List[str]]:
        """Check required Python packages"""
        required_packages = [
            'psutil',
            'numpy',
            'sklearn',
            'schedule',
            'requests',
            'asyncio',
            'sqlite3',
            'matplotlib'
        ]

        missing = []
        for package in required_packages:
            try:
                if package == 'sklearn':
                    import sklearn
                elif package == 'sqlite3':
                    import sqlite3
                else:
                    __import__(package)
            except ImportError:
                missing.append(package)

        return len(missing) == 0, missing

    def check_system_resources(self) -> Dict[str, any]:
        """Check system resources for extended operation"""
        # Memory check
        memory = psutil.virtual_memory()
        memory_gb = memory.total / (1024**3)
        memory_available_gb = memory.available / (1024**3)

        # Disk check
        disk = psutil.disk_usage('/')
        disk_gb = disk.total / (1024**3)
        disk_free_gb = disk.free / (1024**3)

        # CPU check
        cpu_count = psutil.cpu_count()
        cpu_percent = psutil.cpu_percent(interval=1)

        return {
            "memory_total_gb": memory_gb,
            "memory_available_gb": memory_available_gb,
            "memory_percent": memory.percent,
            "disk_total_gb": disk_gb,
            "disk_free_gb": disk_free_gb,
            "disk_percent": disk.percent,
            "cpu_count": cpu_count,
            "cpu_percent": cpu_percent
        }

    def check_file_permissions(self) -> Tuple[bool, List[str]]:
        """Check file permissions for required files"""
        issues = []

        # Check if extended script exists and is executable
        if not self.extended_script.exists():
            issues.append(f"Extended script not found: {self.extended_script}")
        elif not os.access(self.extended_script, os.R_OK):
            issues.append(f"Extended script not readable: {self.extended_script}")

        # Check if config file exists and is readable
        if not self.config_file.exists():
            issues.append(f"Config file not found: {self.config_file}")
        elif not os.access(self.config_file, os.R_OK):
            issues.append(f"Config file not readable: {self.config_file}")

        # Check if we can create state directory
        try:
            self.state_dir.mkdir(exist_ok=True)
            test_file = self.state_dir / "test_write"
            test_file.write_text("test")
            test_file.unlink()
        except Exception as e:
            issues.append(f"Cannot write to state directory: {e}")

        return len(issues) == 0, issues

    def validate_configuration(self) -> Tuple[bool, List[str]]:
        """Validate configuration file"""
        issues = []

        try:
            with open(self.config_file) as f:
                config = json.load(f)

            # Check required configuration keys
            required_keys = [
                'check_interval',
                'max_memory_percent',
                'max_cpu_percent',
                'operation_mode'
            ]

            for key in required_keys:
                if key not in config:
                    issues.append(f"Missing required config key: {key}")

            # Validate value ranges
            if 'max_memory_percent' in config:
                if not 0 < config['max_memory_percent'] <= 100:
                    issues.append("max_memory_percent must be between 0 and 100")

            if 'check_interval' in config:
                if config['check_interval'] < 1:
                    issues.append("check_interval must be at least 1 second")

            if 'operation_mode' in config:
                valid_modes = ['conservative', 'balanced', 'aggressive', 'research']
                if config['operation_mode'] not in valid_modes:
                    issues.append(f"operation_mode must be one of: {valid_modes}")

        except json.JSONDecodeError as e:
            issues.append(f"Invalid JSON in config file: {e}")
        except Exception as e:
            issues.append(f"Error reading config file: {e}")

        return len(issues) == 0, issues

    def install_missing_dependencies(self, missing: List[str]) -> bool:
        """Install missing dependencies"""
        if not missing:
            return True

        print(f"🔧 Installing missing packages: {', '.join(missing)}")

        # Map sklearn to scikit-learn for pip
        pip_packages = []
        for package in missing:
            if package == 'sklearn':
                pip_packages.append('scikit-learn')
            elif package in ['asyncio', 'sqlite3']:
                # These are built-in, skip
                continue
            else:
                pip_packages.append(package)

        if not pip_packages:
            return True

        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install'
            ] + pip_packages)
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False

    def create_default_config(self):
        """Create default configuration if it doesn't exist"""
        if self.config_file.exists():
            return

        print("📝 Creating default configuration file...")

        default_config = {
            "_description": "Extended Operation AutoMode Configuration",
            "_version": "3.0",

            "check_interval": 45,
            "health_check_interval": 60,
            "metrics_collection_interval": 30,
            "deep_analysis_interval": 3600,

            "max_memory_percent": 75.0,
            "max_cpu_percent": 80.0,
            "max_disk_percent": 85.0,
            "memory_warning_threshold": 65.0,
            "cpu_warning_threshold": 70.0,

            "enable_predictive_analytics": True,
            "enable_trend_analysis": True,
            "enable_automatic_optimization": True,
            "enable_long_term_learning": True,

            "enable_metrics_database": True,
            "metrics_retention_days": 365,
            "enable_performance_modeling": True,

            "operation_mode": "balanced",
            "enable_adaptive_intervals": True,
            "min_check_interval": 15,
            "max_check_interval": 300
        }

        self.config_file.parent.mkdir(exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(default_config, f, indent=2)

        print(f"✅ Default configuration created: {self.config_file}")

    def setup_directories(self):
        """Setup required directories"""
        directories = [
            self.state_dir,
            self.state_dir / "analytics_reports",
            self.state_dir / "checkpoints",
            self.base_dir / "logs" / "extended"
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    def print_system_overview(self, resources: Dict[str, any]):
        """Print system overview"""
        print("\n📊 SYSTEM OVERVIEW")
        print("-" * 50)
        print(f"Memory:      {resources['memory_available_gb']:.1f}GB available / {resources['memory_total_gb']:.1f}GB total ({resources['memory_percent']:.1f}% used)")
        print(f"Disk:        {resources['disk_free_gb']:.1f}GB free / {resources['disk_total_gb']:.1f}GB total ({resources['disk_percent']:.1f}% used)")
        print(f"CPU:         {resources['cpu_count']} cores ({resources['cpu_percent']:.1f}% current load)")

    def print_recommendations(self, resources: Dict[str, any]):
        """Print system recommendations"""
        print("\n💡 RECOMMENDATIONS")
        print("-" * 50)

        # Memory recommendations
        if resources['memory_available_gb'] < 2.0:
            print("⚠️  Consider increasing available memory for extended operation")
        elif resources['memory_available_gb'] > 8.0:
            print("✅ Excellent memory availability for extended operation")

        # Disk recommendations
        if resources['disk_percent'] > 85:
            print("⚠️  High disk usage - consider cleanup or expansion")
        elif resources['disk_free_gb'] > 50:
            print("✅ Excellent disk space for extended operation")

        # CPU recommendations
        if resources['cpu_percent'] > 80:
            print("⚠️  High CPU load - consider conservative operation mode")
        elif resources['cpu_count'] >= 4:
            print("✅ Sufficient CPU cores for parallel operation")

        # Operation mode recommendations
        if resources['memory_available_gb'] < 4 or resources['cpu_count'] < 4:
            print("💡 Recommend 'conservative' operation mode for this system")
        elif resources['memory_available_gb'] > 8 and resources['cpu_count'] >= 8:
            print("💡 System suitable for 'aggressive' or 'research' operation mode")
        else:
            print("💡 Recommend 'balanced' operation mode for this system")

    def run_startup_check(self, install_deps: bool = True) -> bool:
        """Run comprehensive startup check"""
        print("🚀 Extended AutoMode Startup Check")
        print("=" * 60)

        all_checks_passed = True

        # Check Python version
        print("\n🐍 Checking Python version...")
        python_ok, python_info = self.check_python_version()
        if python_ok:
            print(f"✅ {python_info}")
        else:
            print(f"❌ {python_info}")
            all_checks_passed = False

        # Check dependencies
        print("\n📦 Checking dependencies...")
        deps_ok, missing_deps = self.check_dependencies()
        if deps_ok:
            print("✅ All required packages are available")
        else:
            print(f"⚠️  Missing packages: {', '.join(missing_deps)}")
            if install_deps:
                if self.install_missing_dependencies(missing_deps):
                    deps_ok, remaining_missing = self.check_dependencies()
                    if deps_ok:
                        print("✅ All dependencies now available")
                    else:
                        print(f"❌ Still missing: {', '.join(remaining_missing)}")
                        all_checks_passed = False
                else:
                    all_checks_passed = False
            else:
                all_checks_passed = False

        # Check file permissions
        print("\n📁 Checking file permissions...")
        perms_ok, perm_issues = self.check_file_permissions()
        if perms_ok:
            print("✅ File permissions are correct")
        else:
            print("❌ File permission issues:")
            for issue in perm_issues:
                print(f"   - {issue}")
            all_checks_passed = False

        # Create default config if needed
        self.create_default_config()

        # Check configuration
        print("\n⚙️  Checking configuration...")
        config_ok, config_issues = self.validate_configuration()
        if config_ok:
            print("✅ Configuration is valid")
        else:
            print("❌ Configuration issues:")
            for issue in config_issues:
                print(f"   - {issue}")
            all_checks_passed = False

        # Setup directories
        print("\n📂 Setting up directories...")
        self.setup_directories()
        print("✅ Directories created")

        # Check system resources
        print("\n💻 Checking system resources...")
        resources = self.check_system_resources()
        print("✅ System resource check completed")

        # Print system overview and recommendations
        self.print_system_overview(resources)
        self.print_recommendations(resources)

        # Final status
        print(f"\n{'='*60}")
        if all_checks_passed:
            print("🎉 ALL CHECKS PASSED - Ready for Extended AutoMode")
            print(f"\nTo start Extended AutoMode:")
            print(f"  ./launch_extended_automode.sh start")
            print(f"\nOr run directly:")
            print(f"  python3 {self.extended_script}")
        else:
            print("❌ SOME CHECKS FAILED - Please resolve issues before starting")

        print(f"{'='*60}")

        return all_checks_passed


def main():
    parser = argparse.ArgumentParser(description="Extended AutoMode Startup Check")
    parser.add_argument("--base-dir", type=Path, default=Path.cwd(),
                       help="Base directory path")
    parser.add_argument("--no-install", action="store_true",
                       help="Don't automatically install missing dependencies")
    parser.add_argument("--check-only", action="store_true",
                       help="Only check system, don't start AutoMode")

    args = parser.parse_args()

    startup = ExtendedAutoModeStartup(args.base_dir)

    # Run startup check
    checks_passed = startup.run_startup_check(install_deps=not args.no_install)

    if not args.check_only and checks_passed:
        # Optionally start Extended AutoMode here
        print("\n🚀 Starting Extended AutoMode...")
        try:
            import subprocess
            subprocess.run([
                sys.executable,
                str(startup.extended_script),
                "--config", str(startup.config_file),
                "--base-dir", str(args.base_dir)
            ])
        except KeyboardInterrupt:
            print("\n👋 Extended AutoMode interrupted by user")
        except Exception as e:
            print(f"\n❌ Error starting Extended AutoMode: {e}")

    return 0 if checks_passed else 1


if __name__ == "__main__":
    sys.exit(main())
