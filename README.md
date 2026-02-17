# pydocstringGenerator

A powerful Python library for analyzing, validating, and automatically generating docstrings in multiple formats. Perfect for improving code documentation quality and ensuring PEP-257 compliance.

[![PyPI version](https://img.shields.io/pypi/v/pydocstringGenerator.svg)](https://pypi.org/project/pydocstringGenerator/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

**Multiple Docstring Formats**
- Google style
- NumPy style  
- reST (Sphinx) style

**Code Analysis**
- Parse and analyze Python AST
- Detect functions, classes, and methods
- Extract function parameters
- Identify exception raises, yields, and class attributes
- Calculate documentation coverage

**PEP-257 Validation**
- Check docstring compliance using pydocstyle
- Generate detailed compliance reports
- Identify warnings and errors

**Intelligent Docstring Generation**
- Generate missing docstrings automatically
- Rewrite existing docstrings (optional)
- Maintain proper indentation
- Preserve code structure

## Installation

Install from PyPI:

```bash
pip install pydocstringGenerator
```

## Quick Start

```python
import ast
from pydocstringGenerator import map_nodes, check_pep257, build_docstring, insert_docstrings_into_code

# Read your Python file
with open("your_file.py", "r") as f:
    code = f.read()

# Parse and analyze
tree = ast.parse(code)
node_map = map_nodes(tree)

# Check PEP-257 compliance
violations = check_pep257(code)
print(f"Found {len(violations)} docstring issues")

# Generate missing docstrings (Google style)
updated_code = insert_docstrings_into_code(code, node_map, "Google", "missing")

# Save the updated code
with open("your_file_updated.py", "w") as f:
    f.write(updated_code)
```

---

## Complete API Documentation

This README provides a quick overview. For **detailed documentation on all available functions**, their parameters, return values, and complete examples, see:

- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute quick start guide with basic examples Start here!
- **[EXAMPLES.md](EXAMPLES.md)** - 12+ practical, copy-paste ready code examples for common tasks
- **[DOCUMENTATION.md](DOCUMENTATION.md)** - Full API reference with all 14 functions and detailed examples

**Recommended Flow:** QUICKSTART.md EXAMPLES.md DOCUMENTATION.md

---

## API Reference (Quick Overview)

#### `map_nodes(tree)`
Analyzes an AST tree and returns a mapping of all functions and classes with metadata.

**Args:**
- `tree` (ast.AST): Parsed AST from `ast.parse()`

**Returns:**
- `dict`: Contains 'functions' and 'classes' lists with name, params, and docstring status

```python
import ast
from pydocstringGenerator import attach_parents, map_nodes

code = '''
def greet(name, age):
    """Say hello."""
    print(f"Hello {name}")

class Person:
    def __init__(self):
        pass
'''

tree = ast.parse(code)
attach_parents(tree)
node_map = map_nodes(tree)

print(node_map['functions'])  # [{'name': 'greet', 'params': ['name', 'age'], ...}]
print(node_map['classes'])    # [{'name': 'Person', 'methods': [...], ...}]
```

#### `build_docstring(format_type, name, params)`
Generates a docstring template in the specified format.

**Args:**
- `format_type` (str): One of "Google", "NumPy", or "reST"
- `name` (str): Function or class name
- `params` (list): List of parameter names

**Returns:**
- `str`: Formatted docstring

```python
from pydocstringGenerator import build_docstring

docstring = build_docstring("Google", "calculate_sum", ["a", "b"])
print(docstring)
# Output:
# """Calculate sum.
# 
# Args:
#     a: Description.
#     b: Description.
# Returns:
#     Description.
# """
```

#### `check_pep257(code)`
Validates Python code against PEP-257 docstring conventions.

**Args:**
- `code` (str): Python source code

**Returns:**
- `list`: Violation objects from pydocstyle

```python
from pydocstringGenerator import check_pep257

code = "def hello(): print('hi')"
violations = check_pep257(code)

for v in violations:
    print(f"{v.filename}:{v.line} - {v.code}: {v.message}")
```

#### `insert_docstrings_into_code(code, node_map, format_type, mode)`
Inserts generated docstrings into Python source code.

**Args:**
- `code` (str): Python source code
- `node_map` (dict): Output from `map_nodes()`
- `format_type` (str): "Google", "NumPy", or "reST"
- `mode` (str): "missing" to add only missing docstrings, or "rewrite" to replace all

**Returns:**
- `str`: Updated code with docstrings

```python
import ast
from pydocstringGenerator import attach_parents, map_nodes, insert_docstrings_into_code

code = '''
def add(x, y):
    return x + y

class Calculator:
    def multiply(self, a, b):
        return a * b
'''

tree = ast.parse(code)
attach_parents(tree)
node_map = map_nodes(tree)

# Add missing docstrings only
updated = insert_docstrings_into_code(code, node_map, "Google", "missing")
print(updated)
```

### Helper Functions

#### `attach_parents(tree)`
Adds parent references to all AST nodes (required before using map_nodes).

#### `extract_parameters(node)`
Extracts parameter names from a function node.

#### `detect_raises(node)`
Returns list of exceptions raised in a function.

#### `detect_yields(node)`
Returns True if function contains yield statements.

#### `detect_attributes(class_node)`
Returns list of class attributes (both class variables and instance attributes).

## Configuration

Create a `pyproject.toml` in your project with optional settings:

```toml
[tool.docgen]
style = "Google"        # Google | NumPy | reST
rewrite = false         # false = only missing docstrings
module_doc = true       # auto insert module docstring
coverage_min = 90       # minimum documentation coverage %
```

Load configuration with:

```python
from pydocstringGenerator import load_pyproject

config = load_pyproject()
style = config.get("style", "Google")
```

## Supported Python Versions

- Python 3.9+
- Python 3.10
- Python 3.11
- Python 3.12

## Dependencies

- `pydocstyle` - PEP-257 docstring validation
- `streamlit` - Web UI (optional, for standalone app)
- `plotly` - Visualization (optional, for standalone app)
- `tomli` - TOML parsing (Python < 3.11)

## Use Cases

1. **Improve Code Quality** - Automatically add missing docstrings to legacy code
2. **Enforce Standards** - Validate docstrings against PEP-257
3. **Documentation Coverage** - Calculate and track documentation metrics
4. **Code Review** - Identify undocumented functions and classes
5. **Onboarding** - Help new developers understand code structure

## Example: Full Workflow

```python
import ast
from pydocstringGenerator import (
    attach_parents,
    map_nodes,
    check_pep257,
    insert_docstrings_into_code,
)

# Read Python file
with open("my_script.py") as f:
    code = f.read()

# 1. Analyze code structure
tree = ast.parse(code)
attach_parents(tree)
node_map = map_nodes(tree)

# Count documentation
documented = sum(1 for f in node_map["functions"] if f["has_doc"])
total = len(node_map["functions"])
print(f"Documentation: {documented}/{total} functions documented")

# 2. Check compliance
violations = check_pep257(code)
print(f"PEP-257 violations: {len(violations)}")

# 3. Generate docstrings
updated_code = insert_docstrings_into_code(
    code, node_map, "Google", mode="missing"
)

# 4. Validate updated code
violations_after = check_pep257(updated_code)
print(f"Violations after update: {len(violations_after)}")

# 5. Save result
with open("my_script_updated.py", "w") as f:
    f.write(updated_code)
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

MIT License - see LICENSE file for details

## Author

Created by Himanshu Chawla under Infosys Springboard Internship

## Support

For issues, questions, or suggestions:
- GitHub Issues: [Report a bug](https://github.com/himanshu-chawla/pydocstringGenerator/issues)
- Documentation: [Full docs](https://github.com/himanshu-chawla/pydocstringGenerator#readme)
