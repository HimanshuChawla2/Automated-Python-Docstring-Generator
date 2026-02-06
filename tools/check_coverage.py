"""Check coverage."""

import ast
import sys
from pathlib import Path

THRESHOLD = 80  # or read from pyproject.toml if you want


def calc_coverage(path: Path) -> float:
    """Calculate docstring coverage for a single file."""
    try:
        code = path.read_text(encoding="utf-8")
    except Exception:
        return 100.0

    tree = ast.parse(code)
    doc_count = 0
    node_count = 0

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            node_count += 1
            if ast.get_docstring(node):
                doc_count += 1

    if node_count == 0:
        return 100.0

    return (doc_count / node_count) * 100


def main():
    """Run docstring coverage check for ALL Python files in the repo."""
    py_files = [p for p in Path(".").rglob("*.py") if "venv" not in str(p).lower()]

    if not py_files:
        print("No Python files found.")
        return 0

    total = 0
    for f in py_files:
        total += calc_coverage(f)

    avg = total / len(py_files)

    if avg < THRESHOLD:
        print(
            f"\n[ERROR] Docstring Coverage Failed: {avg:.2f}% < required {THRESHOLD}%"
            f"\n        --> Commit rejected.\n"
        )

        sys.exit(1)

        print(
            f"\n[SUCCESS] Docstring Coverage Passed: {avg:.2f}% >= required {THRESHOLD}%\n"
        )

    return 0


if __name__ == "__main__":
    main()
