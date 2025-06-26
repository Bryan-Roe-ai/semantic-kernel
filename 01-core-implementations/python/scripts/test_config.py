#!/usr/bin/env python3
"""
Test module for config

Copyright (c) 2025 Bryan Roe
Licensed under the MIT License

This file is part of the Semantic Kernel - Advanced AI Development Framework.
Original work by Bryan Roe.

Author: Bryan Roe
Created: 2025
License: MIT
"""

import os
from pathlib import Path
from typing import Dict, List, Optional

# Test configuration
TEST_CONFIG = {
    # Directories
    "test_dirs": {
        "unit": "tests/unit",
        "integration": "tests/integration",
        "samples": "tests/samples"
    },

    # Test patterns
    "test_patterns": {
        "default": "test_*.py",
        "integration": "test_*_integration.py",
        "unit": "test_*.py"
    },

    # Timeouts (in seconds)
    "timeouts": {
        "unit": 60,
        "integration": 300,
        "samples": 180,
        "default": 120
    },

    # Coverage settings
    "coverage": {
        "min_percentage": 80,
        "include": ["semantic_kernel/*"],
        "exclude": [
            "semantic_kernel/tests/*",
            "semantic_kernel/samples/*"
        ],
        "omit": [
            "*/tests/*",
            "*/test_*",
            "*/__pycache__/*"
        ]
    },

    # Parallel execution settings
    "parallel": {
        "enabled": True,
        "max_workers": None,  # None = auto-detect CPU cores
        "chunk_size": 10
    },

    # Pytest options
    "pytest_options": {
        "unit": [
            "-v",
            "--tb=short",
            "-ra",
            "--strict-markers",
            "--disable-warnings"
        ],
        "integration": [
            "-v",
            "--tb=short",
            "-ra",
            "--strict-markers",
            "--disable-warnings",
            "-x"  # Stop on first failure for integration tests
        ],
        "samples": [
            "-v",
            "--tb=short",
            "-ra",
            "--strict-markers"
        ]
    },

    # Environment variables for tests
    "env_vars": {
        "PYTHONPATH": ".",
        "PYTEST_CURRENT_TEST": "1",
        "SK_TEST_MODE": "1"
    },

    # Test markers
    "markers": {
        "unit": "Unit tests",
        "integration": "Integration tests",
        "slow": "Slow running tests",
        "azure": "Tests requiring Azure services",
        "openai": "Tests requiring OpenAI API",
        "ollama": "Tests requiring Ollama service",
        "onnx": "Tests requiring ONNX runtime",
        "experimental": "Experimental feature tests"
    },

    # Quality gates
    "quality_gates": {
        "coverage_threshold": 80,
        "max_test_duration": 1800,  # 30 minutes
        "max_failures": 5,
        "required_checks": [
            "unit_tests",
            "linting",
            "type_checking"
        ]
    },

    # Reporting
    "reporting": {
        "formats": ["json", "xml", "html"],
        "output_dir": "test_reports",
        "include_coverage": True,
        "include_timing": True
    }
}

# CI/CD specific configurations
CI_CONFIG = {
    "github_actions": {
        "python_versions": ["3.10", "3.11", "3.12"],
        "os_matrix": ["ubuntu-latest", "windows-latest", "macos-latest"],
        "timeout_minutes": 45,
        "retry_attempts": 2
    },

    "pre_commit": {
        "hooks": [
            "ruff-check",
            "ruff-format",
            "mypy",
            "pytest-fast"
        ]
    }
}

# Test data and fixtures
TEST_DATA_CONFIG = {
    "fixtures_dir": "tests/fixtures",
    "mock_data_dir": "tests/data",
    "sample_files": [
        "tests/test_plugins/TestPlugin/TestFunction/config.json",
        "tests/test_skills/TestSkill/TestFunction/config.json"
    ]
}


def get_test_config(section: Optional[str] = None) -> Dict:
    """Get test configuration."""
    if section:
        return TEST_CONFIG.get(section, {})
    return TEST_CONFIG


def get_ci_config(provider: str = "github_actions") -> Dict:
    """Get CI/CD configuration."""
    return CI_CONFIG.get(provider, {})


def get_env_vars() -> Dict[str, str]:
    """Get environment variables for tests."""
    env_vars = TEST_CONFIG["env_vars"].copy()

    # Add current environment variables
    for key, value in os.environ.items():
        if key.startswith(("AZURE_", "OPENAI_", "SK_")):
            env_vars[key] = value

    return env_vars


def get_pytest_args(test_type: str = "unit", include_coverage: bool = True) -> List[str]:
    """Get pytest arguments for test type."""
    args = TEST_CONFIG["pytest_options"].get(test_type, [])

    if include_coverage and test_type in ["unit", "integration"]:
        coverage_args = [
            "--cov=semantic_kernel",
            "--cov-report=term-missing",
            f"--cov-report=xml:test_reports/coverage_{test_type}.xml",
            f"--cov-report=html:test_reports/htmlcov_{test_type}"
        ]
        args.extend(coverage_args)

    # Add timeout
    timeout = TEST_CONFIG["timeouts"].get(test_type, TEST_CONFIG["timeouts"]["default"])
    args.extend([f"--timeout={timeout}"])

    return args


def get_test_markers() -> List[str]:
    """Get list of test markers."""
    return list(TEST_CONFIG["markers"].keys())


def validate_config() -> bool:
    """Validate test configuration."""
    required_sections = ["test_dirs", "timeouts", "coverage"]

    for section in required_sections:
        if section not in TEST_CONFIG:
            return False

    # Validate paths exist
    for test_dir in TEST_CONFIG["test_dirs"].values():
        if not Path(test_dir).exists():
            print(f"Warning: Test directory {test_dir} does not exist")

    return True
