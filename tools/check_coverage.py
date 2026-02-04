"""Coverage enforcement script used by pre-commit hooks."""

import ast
import sys
import pathlib


THRESHOLD = 90


def calc_coverage(path: pathlib.Path) -> float:
    """Calculate docstring coverage percentage for a Python file."""
    code = pathlib.Path(path).read_text(encoding="utf-8", errors="ignore")

    tree = ast.parse(code)

    total = 0
    documented = 0

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            total += 1
        if ast.get_docstring(node):
            documented += 1

        return (documented / total * 100) if total else 100.0


if __name__ == "__main__":
    project = pathlib.Path(".")
    py_files = list(project.rglob("*.py"))

    coverages = [calc_coverage(path) for path in py_files]
    overall = sum(coverages) / len(coverages)

    if overall < THRESHOLD:
        print(f"Docstring Coverage Failed: {overall:.2f}% < {THRESHOLD}%")
        sys.exit(1)

    print(f"Docstring Coverage OK: {overall:.2f}%")
