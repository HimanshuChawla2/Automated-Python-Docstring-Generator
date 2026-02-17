"""Automated Python Docstring Generator.

A library for analyzing Python code documentation and generating missing
docstrings in various formats (Google, NumPy, reST).
"""

import ast
import tempfile
import os
from pathlib import Path
import pydocstyle

__version__ = "1.0.0"
__author__ = "Himanshu Chawla"
__all__ = [
    "load_pyproject",
    "attach_parents",
    "extract_parameters",
    "map_nodes",
    "add_module_docstring",
    "detect_raises",
    "detect_yields",
    "detect_attributes",
    "generate_docstring_google",
    "generate_docstring_numpy",
    "generate_docstring_rest",
    "build_docstring",
    "insert_docstrings_into_code",
    "check_pep257",
]


def load_pyproject():
    """Loading project configuration from pyproject.toml."""
    config_path = Path("pyproject.toml")
    if not config_path.exists():
        return {}
    try:
        import tomllib

        with open(config_path, "rb") as f:
            return tomllib.load(f).get("tool", {}).get("docgen", {})
    except Exception:
        return {}


def attach_parents(tree):
    """Attach parent pointers to all AST nodes.

    Args:
        tree: AST tree to process.

    Returns:
        None. Modifies tree in-place.
    """
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node


def extract_parameters(node):
    """Return safe parameter list for functions and methods.

    Args:
        node: AST node to extract parameters from.

    Returns:
        List of parameter names.
    """
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return [a.arg for a in node.args.args]
    return []


def map_nodes(tree):
    """Create mapping of classes and functions including docstring presence.

    Args:
        tree: AST tree to analyze.

    Returns:
        Dictionary with 'functions' and 'classes' keys containing metadata.
    """
    node_map = {"functions": [], "classes": []}

    for node in ast.walk(tree):

        # -------- Functions --------
        if isinstance(node, ast.FunctionDef) and not isinstance(getattr(node, "parent", None), ast.ClassDef):
            node_map["functions"].append(
                {
                    "node": node,
                    "name": node.name,
                    "params": extract_parameters(node),
                    "has_doc": ast.get_docstring(node) is not None,
                }
            )

        # -------- Classes --------
        if isinstance(node, ast.ClassDef):
            class_entry = {
                "node": node,
                "name": node.name,
                "params": [],
                "has_doc": ast.get_docstring(node) is not None,
                "methods": [],
            }

            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    class_entry["methods"].append(
                        {
                            "node": item,
                            "name": item.name,
                            "params": extract_parameters(item),
                            "has_doc": ast.get_docstring(item) is not None,
                        }
                    )

            node_map["classes"].append(class_entry)

    return node_map


def add_module_docstring(code):
    """Insert a module-level docstring at the top if missing.

    Args:
        code: Python source code as string.

    Returns:
        Code with module docstring added if missing.
    """
    try:
        tree = ast.parse(code)
        if ast.get_docstring(tree) is not None:
            return code
    except SyntaxError:
        return code

    module_doc = '"""Module description."""\n\n'
    return module_doc + code


def detect_raises(node):
    """Return a list of exceptions raised inside a function.

    Args:
        node: AST node to analyze.

    Returns:
        List of exception class names found in raise statements.
    """
    raises = []
    for n in ast.walk(node):
        if isinstance(n, ast.Raise) and n.exc:
            if isinstance(n.exc, ast.Call):
                raises.append(n.exc.func.id)
            elif isinstance(n.exc, ast.Name):
                raises.append(n.exc.id)
    return raises


def detect_yields(node):
    """Return True if function contains yield statements.

    Args:
        node: AST node to analyze.

    Returns:
        Boolean indicating if node contains yield/yieldfrom.
    """
    for n in ast.walk(node):
        if isinstance(n, (ast.Yield, ast.YieldFrom)):
            return True
    return False


def detect_attributes(class_node):
    """Return assigned class attributes (class vars + self.x).

    Args:
        class_node: AST ClassDef node to analyze.

    Returns:
        List of unique attribute names found in the class.
    """
    attrs = []

    for n in class_node.body:
        # class variable assignments: x = 10
        if isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Name):
                    attrs.append(t.id)

        # inside functions: self.x = ...
        if isinstance(n, ast.FunctionDef):
            for inner in ast.walk(n):
                if isinstance(inner, ast.Assign):
                    for t in inner.targets:
                        if isinstance(t, ast.Attribute) and isinstance(t.value, ast.Name) and t.value.id == "self":
                            attrs.append(t.attr)
    return list(set(attrs))


def generate_docstring_google(name, params):
    """Google style docstring with summary on same line.

    Args:
        name: Function or class name.
        params: List of parameter names.

    Returns:
        Google-style docstring string.
    """
    summary = name.capitalize() + "."

    param_lines = "\n".join([f"    {p}: Description." for p in params])

    return f'''"""{summary}

Args:
{param_lines if params else "    None"}
Returns:
    Description.
"""'''


def generate_docstring_numpy(name, params):
    """Numpy style docstring with same-line summary.

    Args:
        name: Function or class name.
        params: List of parameter names.

    Returns:
        NumPy-style docstring string.
    """
    summary = name.capitalize() + "."

    param_lines = "\n".join([f"{p} : type\n    Description." for p in params])

    return f'''"""{summary}

Parameters
----------
{param_lines if params else "None"}

Returns
-------
type
    Description.
"""'''


def generate_docstring_rest(name, params):
    """Rest style docstring with same-line summary.

    Args:
        name: Function or class name.
        params: List of parameter names.

    Returns:
        reST-style docstring string.
    """
    summary = name.capitalize() + "."

    param_lines = "\n".join([f":param {p}: Description." for p in params])

    return f'''"""{summary}

{param_lines if params else ""}

:returns: Description.
"""'''


def build_docstring(format_type, name, params):
    """Build docstring based on format type.

    Args:
        format_type: One of "Google", "NumPy", "reST".
        name: Function or class name.
        params: List of parameter names.

    Returns:
        Formatted docstring string.
    """
    if format_type == "Google":
        return generate_docstring_google(name, params)
    if format_type == "NumPy":
        return generate_docstring_numpy(name, params)
    return generate_docstring_rest(name, params)


def insert_docstrings_into_code(code, node_map, format_type, mode):
    """Insert or rewrite docstrings safely with correct indentation.

    Args:
        code: Python source code as string.
        node_map: Mapping from map_nodes().
        format_type: Docstring format ("Google", "NumPy", "reST").
        mode: Either "missing" to only add missing docstrings or "rewrite" to replace all.

    Returns:
        Updated code with docstrings inserted/modified.
    """
    lines = code.split("\n")
    new_lines = lines.copy()

    # Sort nodes bottom to top
    all_nodes = []
    for fn in node_map["functions"]:
        all_nodes.append(fn)
    for cls in node_map["classes"]:
        all_nodes.append(cls)
        for m in cls["methods"]:
            all_nodes.append(m)

    all_nodes = sorted(all_nodes, key=lambda x: x["node"].lineno, reverse=True)

    for item in all_nodes:
        node = item["node"]
        name = item["name"]
        params = item.get("params", [])
        has_doc = item["has_doc"]

        # Skip rewriting docstrings if mode is "missing"
        if mode == "missing" and has_doc:
            continue

        doc = build_docstring(format_type, name, params)

        # Determine indentation level
        def_line = lines[node.lineno - 1]
        indent = len(def_line) - len(def_line.lstrip(" "))

        # Build formatted docstring lines
        doc_lines = []
        doc_content = [line for line in doc.split("\n")]

        # Remove empty first/last lines
        while doc_content and doc_content[0].strip() == "":
            doc_content.pop(0)
        while doc_content and doc_content[-1].strip() == "":
            doc_content.pop()

        doc_lines = [" " * (indent + 4) + line for line in doc_content]

        # Insert docstring immediately after def line
        insertion_index = node.lineno

        # If function/class already has docstring, remove it first
        if has_doc:
            first_stmt = node.body[0]
            if isinstance(first_stmt, ast.Expr) and isinstance(first_stmt.value, ast.Str):
                start = first_stmt.lineno - 1
                end = first_stmt.end_lineno
                del new_lines[start:end]
                insertion_index = start

        # Insert docstring block
        for lines in reversed(doc_lines):
            new_lines.insert(insertion_index, lines)

    return "\n".join(new_lines)


def check_pep257(code):
    """Run pydocstyle on a temporary file and return violations.

    Args:
        code: Python source code as string.

    Returns:
        List of pydocstyle violation objects.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w", encoding="utf-8") as tmp:
        tmp.write(code)
        tmp_path = tmp.name

    violations = list(pydocstyle.check([tmp_path]))
    os.remove(tmp_path)
    return violations
