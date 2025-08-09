#!/usr/bin/env python3
"""Aggregate line coverage percentages for Python and .NET Cobertura reports.

Outputs two lines:
  PY_COV=##.##
  DN_COV=##.##
"""
from __future__ import annotations

import glob
import xml.etree.ElementTree as ET
from typing import Iterable, List
from pathlib import Path


def collect(patterns: Iterable[str]) -> tuple[float, int, int]:
    total_lines = 0
    total_covered = 0
    for pattern in patterns:
        for file in glob.glob(pattern, recursive=True):
            try:
                root = ET.parse(file).getroot()
            except ET.ParseError:
                continue
            for cls in root.findall(".//class"):
                try:
                    total_lines += int(cls.attrib.get("lines-valid", "0"))
                    total_covered += int(cls.attrib.get("lines-covered", "0"))
                except (TypeError, ValueError):
                    continue
    pct = 100.0 * total_covered / total_lines if total_lines else 0.0
    return pct, total_lines, total_covered


def build_combined_python_report(sources: Iterable[str], output: str) -> None:
    """Merge multiple Cobertura coverage.xml files into one (simple union of packages).

    Not a perfect semantic merge; adequate for aggregate line-rate computation.
    """
    files: List[str] = []
    for pattern in sources:
        files.extend(glob.glob(pattern))
    if not files:
        return
    first_root = None
    packages_parent = None
    total_lines = total_covered = 0
    for f in files:
        try:
            tree = ET.parse(f)
        except ET.ParseError:
            continue
        root = tree.getroot()
        if first_root is None:
            first_root = root
            packages_parent = root.find("packages")
        for cls in root.findall(".//class"):
            try:
                total_lines += int(cls.attrib.get("lines-valid", "0"))
                total_covered += int(cls.attrib.get("lines-covered", "0"))
            except (TypeError, ValueError):
                continue
        if root is not first_root and packages_parent is not None:
            pkgs = root.find("packages")
            if pkgs is not None:
                for p in pkgs.findall("package"):
                    packages_parent.append(p)
    if first_root is not None and total_lines:
        line_rate = total_covered / total_lines
        first_root.set("line-rate", f"{line_rate:.4f}")
        Path(output).parent.mkdir(parents=True, exist_ok=True)
        ET.ElementTree(first_root).write(output)


def main() -> None:
    python_patterns = ["python-artifacts-*/coverage.xml"]
    py_cov, py_lines, py_covered = collect(python_patterns)
    build_combined_python_report(python_patterns, "python-coverage-combined.xml")
    dn_cov, dn_lines, dn_covered = collect(
        ["dotnet-artifacts-*/TestResults/**/coverage.cobertura.xml"]
    )
    combined_pct = 0.0
    if (py_lines + dn_lines) > 0:
        combined_pct = 100.0 * (py_covered + dn_covered) / (py_lines + dn_lines)
    print(f"PY_COV={py_cov:.2f}")
    print(f"DN_COV={dn_cov:.2f}")
    print(f"PY_LINES={py_lines}")
    print(f"DN_LINES={dn_lines}")
    print(f"COMBINED_COV={combined_pct:.2f}")
    if Path("python-coverage-combined.xml").exists():
        print("PY_COMBINED=python-coverage-combined.xml")


if __name__ == "__main__":  # pragma: no cover
    main()
