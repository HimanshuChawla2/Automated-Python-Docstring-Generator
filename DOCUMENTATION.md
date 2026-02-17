# pydocstringGenerator - Complete API Documentation

Complete reference guide for all functions available in the `pydocstringGenerator` library (imported as `milestone2`).

---

## Table of Contents

1. [Configuration Functions](#configuration-functions)
2. [AST Analysis Functions](#ast-analysis-functions)
3. [Docstring Generation Functions](#docstring-generation-functions)
4. [Code Modification Functions](#code-modification-functions)
5. [Validation Functions](#validation-functions)
6. [Complete Examples](#complete-examples)

---

## Configuration Functions

### `load_pyproject()`

Load project configuration from `pyproject.toml` in the current directory.

**Signature:**
```python
def load_pyproject() -> dict
```

**Returns:**
- `dict`: Configuration dictionary with keys like `style`, `rewrite`, `module_doc`, `coverage_min`
- Returns empty dict `{}` if file doesn't exist or fails to parse

**Example:**
```python
from pydocstringGenerator import load_pyproject

config = load_pyproject()
style = config.get("style", "Google")
should_rewrite = config.get("rewrite", False)
min_coverage = config.get("coverage_min", 90)

print(f"Using {style} style")
print(f"Rewrite mode: {should_rewrite}")
print(f"Minimum coverage: {min_coverage}%")
```

**Config File Example (pyproject.toml):**
```toml
[tool.docgen]
style = "Google"        # Google | NumPy | reST
rewrite = false         # false = only missing
module_doc = true       # auto insert module docstring
coverage_min = 90       # minimum coverage %
```

---

## AST Analysis Functions

### `attach_parents(tree)`

Add parent references to all nodes in an AST tree. **Required before using `map_nodes()`.**

**Signature:**
```python
def attach_parents(tree: ast.AST) -> None
```

**Parameters:**
- `tree` (ast.AST): An AST tree from `ast.parse()`

**Returns:**
- `None` (modifies tree in-place)

**Example:**
```python
import ast
from pydocstringGenerator import attach_parents

code = "def hello(): pass"
tree = ast.parse(code)
attach_parents(tree)  # Now all nodes have .parent attribute

# You can now traverse up the tree
for node in ast.walk(tree):
    if hasattr(node, 'parent'):
        print(f"Node {node} has parent: {node.parent}")
```

---

### `extract_parameters(node)`

Extract parameter names from a function or method node.

**Signature:**
```python
def extract_parameters(node: ast.AST) -> list[str]
```

**Parameters:**
- `node` (ast.AST): A function definition node (`ast.FunctionDef` or `ast.AsyncFunctionDef`)

**Returns:**
- `list[str]`: List of parameter names (excluding `self` and `cls`)

**Example:**
```python
import ast
from pydocstringGenerator import extract_parameters

code = "def calculate(a, b, c=10): pass"
tree = ast.parse(code)
func_node = tree.body[0]

params = extract_parameters(func_node)
print(params)  # Output: ['a', 'b', 'c']
```

---

### `map_nodes(tree)`

Analyze an AST tree and create a mapping of all functions and classes with metadata.

**Signature:**
```python
def map_nodes(tree: ast.AST) -> dict
```

**Parameters:**
- `tree` (ast.AST): A parsed AST tree (from `ast.parse()`)

**Returns:**
- `dict`: Structure:
  ```python
  {
      "functions": [
          {
              "node": ast.FunctionDef,
              "name": str,
              "params": list[str],
              "has_doc": bool
          },
          ...
      ],
      "classes": [
          {
              "node": ast.ClassDef,
              "name": str,
              "params": list,
              "has_doc": bool,
              "methods": [
                  {
                      "node": ast.FunctionDef,
                      "name": str,
                      "params": list[str],
                      "has_doc": bool
                  },
                  ...
              ]
          },
          ...
      ]
  }
  ```

**Example:**
```python
import ast
from pydocstringGenerator import attach_parents, map_nodes

code = '''
def greet(name):
    """Say hello."""
    print(f"Hello {name}")

class Greeter:
    def __init__(self):
        """Initialize greeter."""
        pass
    
    def wave(self):
        print("wave")
'''

tree = ast.parse(code)
attach_parents(tree)
node_map = map_nodes(tree)

# Access functions
for func in node_map["functions"]:
    print(f"Function: {func['name']}, Documented: {func['has_doc']}")

# Access classes and their methods
for cls in node_map["classes"]:
    print(f"Class: {cls['name']}")
    for method in cls["methods"]:
        print(f"  - Method: {method['name']}, Documented: {method['has_doc']}")
```

**Output:**
```
Function: greet, Documented: True
Class: Greeter
  - Method: __init__, Documented: True
  - Method: wave, Documented: False
```

---

### `detect_raises(node)`

Detect all exception types raised in a function.

**Signature:**
```python
def detect_raises(node: ast.AST) -> list[str]
```

**Parameters:**
- `node` (ast.AST): A function definition node

**Returns:**
- `list[str]`: List of exception class names

**Example:**
```python
import ast
from pydocstringGenerator import detect_raises

code = '''
def divide(a, b):
    if b == 0:
        raise ValueError("Division by zero")
    return a / b
'''

tree = ast.parse(code)
func = tree.body[0]
raises = detect_raises(func)
print(raises)  # Output: ['ValueError']
```

---

### `detect_yields(node)`

Check if a function uses yield statements (generator function).

**Signature:**
```python
def detect_yields(node: ast.AST) -> bool
```

**Parameters:**
- `node` (ast.AST): A function definition node

**Returns:**
- `bool`: `True` if function contains `yield` or `yield from`, `False` otherwise

**Example:**
```python
import ast
from pydocstringGenerator import detect_yields, attach_parents, map_nodes

code = '''
def regular_function():
    return [1, 2, 3]

def generator_function():
    for i in range(5):
        yield i
'''

tree = ast.parse(code)
attach_parents(tree)
node_map = map_nodes(tree)

for func in node_map["functions"]:
    is_generator = detect_yields(func["node"])
    print(f"{func['name']}: Generator={is_generator}")
```

**Output:**
```
regular_function: Generator=False
generator_function: Generator=True
```

---

### `detect_attributes(class_node)`

Extract all attributes (class variables and instance attributes) from a class.

**Signature:**
```python
def detect_attributes(class_node: ast.ClassDef) -> list[str]
```

**Parameters:**
- `class_node` (ast.ClassDef): A class definition node

**Returns:**
- `list[str]`: List of unique attribute names

**Example:**
```python
import ast
from pydocstringGenerator import detect_attributes

code = '''
class Person:
    species = "Homo sapiens"  # class variable
    
    def __init__(self, name, age):
        self.name = name      # instance attribute
        self.age = age        # instance attribute
    
    def set_email(self, email):
        self.email = email    # instance attribute
'''

tree = ast.parse(code)
cls = tree.body[0]
attrs = detect_attributes(cls)
print(sorted(attrs))  # Output: ['age', 'email', 'name', 'species']
```

---

## Docstring Generation Functions

### `generate_docstring_google(name, params)`

Generate a Google-style docstring template.

**Signature:**
```python
def generate_docstring_google(name: str, params: list[str]) -> str
```

**Parameters:**
- `name` (str): Function or class name
- `params` (list[str]): List of parameter names

**Returns:**
- `str`: Google-style docstring template

**Example:**
```python
from pydocstringGenerator import generate_docstring_google

docstring = generate_docstring_google("calculate_total", ["price", "tax"])
print(docstring)
```

**Output:**
```
"""Calculate total.

Args:
    price: Description.
    tax: Description.
Returns:
    Description.
"""
```

---

### `generate_docstring_numpy(name, params)`

Generate a NumPy-style docstring template.

**Signature:**
```python
def generate_docstring_numpy(name: str, params: list[str]) -> str
```

**Parameters:**
- `name` (str): Function or class name
- `params` (list[str]): List of parameter names

**Returns:**
- `str`: NumPy-style docstring template

**Example:**
```python
from pydocstringGenerator import generate_docstring_numpy

docstring = generate_docstring_numpy("calculate_total", ["price", "tax"])
print(docstring)
```

**Output:**
```
"""Calculate total.

Parameters
----------
price : type
    Description.
tax : type
    Description.

Returns
-------
type
    Description.
"""
```

---

### `generate_docstring_rest(name, params)`

Generate a reST (Sphinx) style docstring template.

**Signature:**
```python
def generate_docstring_rest(name: str, params: list[str]) -> str
```

**Parameters:**
- `name` (str): Function or class name
- `params` (list[str]): List of parameter names

**Returns:**
- `str`: reST-style docstring template

**Example:**
```python
from pydocstringGenerator import generate_docstring_rest

docstring = generate_docstring_rest("calculate_total", ["price", "tax"])
print(docstring)
```

**Output:**
```
"""Calculate total.

:param price: Description.
:param tax: Description.

:returns: Description.
"""
```

---

### `build_docstring(format_type, name, params)`

Build a docstring in the specified format. **Use this instead of the specific format functions.**

**Signature:**
```python
def build_docstring(format_type: str, name: str, params: list[str]) -> str
```

**Parameters:**
- `format_type` (str): One of `"Google"`, `"NumPy"`, or `"reST"`
- `name` (str): Function or class name
- `params` (list[str]): List of parameter names

**Returns:**
- `str`: Formatted docstring template

**Example:**
```python
from pydocstringGenerator import build_docstring

# Generate in different formats
google_doc = build_docstring("Google", "add", ["a", "b"])
numpy_doc = build_docstring("NumPy", "add", ["a", "b"])
rest_doc = build_docstring("reST", "add", ["a", "b"])

print("=== Google ===")
print(google_doc)
print("\n=== NumPy ===")
print(numpy_doc)
print("\n=== reST ===")
print(rest_doc)
```

---

## Code Modification Functions

### `add_module_docstring(code)`

Insert a module-level docstring at the top of Python code if it's missing.

**Signature:**
```python
def add_module_docstring(code: str) -> str
```

**Parameters:**
- `code` (str): Python source code as string

**Returns:**
- `str`: Code with module docstring added (if it was missing)

**Example:**
```python
from pydocstringGenerator import add_module_docstring

code = '''
def hello():
    """Say hello."""
    print("Hello")
'''

updated = add_module_docstring(code)
print(updated)
```

**Output:**
```python
"""Module description."""

def hello():
    """Say hello."""
    print("Hello")
```

---

### `insert_docstrings_into_code(code, node_map, format_type, mode)`

Insert or replace docstrings in Python code while maintaining proper indentation.

**Signature:**
```python
def insert_docstrings_into_code(
    code: str,
    node_map: dict,
    format_type: str,
    mode: str
) -> str
```

**Parameters:**
- `code` (str): Python source code
- `node_map` (dict): Output from `map_nodes()` (requires pre-parsed tree)
- `format_type` (str): `"Google"`, `"NumPy"`, or `"reST"`
- `mode` (str): 
  - `"missing"` - Only add docstrings where they're missing
  - `"rewrite"` - Replace all docstrings

**Returns:**
- `str`: Updated code with docstrings

**Example:**
```python
import ast
from pydocstringGenerator import attach_parents, map_nodes, insert_docstrings_into_code

code = '''
def add(a, b):
    return a + b

class Calculator:
    def multiply(self, x, y):
        return x * y
'''

# Parse and analyze
tree = ast.parse(code)
attach_parents(tree)
node_map = map_nodes(tree)

# Add missing docstrings only
updated = insert_docstrings_into_code(code, node_map, "Google", "missing")
print(updated)
```

**Output:**
```python
def add(a, b):
    """Add.

    Args:
        a: Description.
        b: Description.
    Returns:
        Description.
    """
    return a + b

class Calculator:
    """Calculator."""

    def multiply(self, x, y):
        """Multiply.

        Args:
            x: Description.
            y: Description.
        Returns:
            Description.
        """
        return x * y
```

---

## Validation Functions

### `check_pep257(code)`

Check Python code against PEP-257 docstring conventions using pydocstyle.

**Signature:**
```python
def check_pep257(code: str) -> list
```

**Parameters:**
- `code` (str): Python source code

**Returns:**
- `list`: List of violation objects with attributes:
  - `.filename` - File name (temporary file)
  - `.line` - Line number of violation
  - `.code` - Error code (e.g., "D100", "D203")
  - `.message` - Description of violation

**Example:**
```python
from pydocstringGenerator import check_pep257

code = '''
def hello():
    print("hi")

class Person:
    def greet(self):
        print("hello")
'''

violations = check_pep257(code)

print(f"Found {len(violations)} violations:")
for v in violations:
    print(f"  Line {v.line}: {v.code} - {v.message}")
```

**Output:**
```
Found 3 violations:
  Line 1: D100 - Missing docstring in public module
  Line 2: D103 - Missing docstring in public function
  Line 5: D101 - Missing docstring in public class
```

---

## Complete Examples

### Example 1: Analyze Code Coverage

```python
import ast
from pydocstringGenerator import attach_parents, map_nodes

code = '''
def greet(name):
    """Say hello."""
    print(f"Hello {name}")

def goodbye(name):
    print(f"Goodbye {name}")

class Person:
    """Represents a person."""
    
    def __init__(self, name):
        """Initialize person."""
        self.name = name
    
    def introduce(self):
        print(f"I am {self.name}")
'''

tree = ast.parse(code)
attach_parents(tree)
node_map = map_nodes(tree)

# Count documentation
total_items = 0
documented = 0

for func in node_map["functions"]:
    total_items += 1
    if func["has_doc"]:
        documented += 1
    print(f"Function '{func['name']}': {func['has_doc']}")

for cls in node_map["classes"]:
    total_items += 1
    if cls["has_doc"]:
        documented += 1
    print(f"Class '{cls['name']}': {cls['has_doc']}")
    
    for method in cls["methods"]:
        total_items += 1
        if method["has_doc"]:
            documented += 1
        print(f"  - Method '{method['name']}': {method['has_doc']}")

coverage = (documented / total_items * 100) if total_items else 0
print(f"\nDocumentation Coverage: {documented}/{total_items} ({coverage:.1f}%)")
```

---

### Example 2: Auto-generate and Validate Docstrings

```python
import ast
from pydocstringGenerator import (
    attach_parents,
    map_nodes,
    insert_docstrings_into_code,
    check_pep257,
)

code = '''
def calculate_sum(numbers):
    return sum(numbers)

class DataProcessor:
    def process(self, data):
        return [x * 2 for x in data]
'''

# Step 1: Parse
tree = ast.parse(code)
attach_parents(tree)
node_map = map_nodes(tree)

# Step 2: Check before
print("BEFORE:")
violations_before = check_pep257(code)
print(f"Violations: {len(violations_before)}")

# Step 3: Generate docstrings
updated = insert_docstrings_into_code(code, node_map, "Google", "missing")

# Step 4: Validate after
print("\nAFTER:")
violations_after = check_pep257(updated)
print(f"Violations: {len(violations_after)}")

print("\n" + "="*50)
print("UPDATED CODE:")
print("="*50)
print(updated)
```

---

### Example 3: Full Project Analysis

```python
import ast
from pathlib import Path
from pydocstringGenerator import (
    attach_parents,
    map_nodes,
    detect_raises,
    detect_yields,
    detect_attributes,
    check_pep257,
)

def analyze_file(filepath):
    """Analyze a single Python file."""
    with open(filepath) as f:
        code = f.read()
    
    tree = ast.parse(code)
    attach_parents(tree)
    node_map = map_nodes(tree)
    
    # Stats
    func_count = len(node_map["functions"])
    class_count = len(node_map["classes"])
    documented = sum(1 for f in node_map["functions"] if f["has_doc"])
    documented += sum(1 for c in node_map["classes"] if c["has_doc"])
    
    # Violations
    violations = check_pep257(code)
    warnings = sum(1 for v in violations if v.code.startswith("D2"))
    errors = len(violations) - warnings
    
    return {
        "file": filepath,
        "functions": func_count,
        "classes": class_count,
        "documented": documented,
        "violations": len(violations),
        "warnings": warnings,
        "errors": errors,
    }

# Analyze all .py files in current directory
for py_file in Path(".").glob("*.py"):
    stats = analyze_file(py_file)
    print(f"\n{stats['file']}:")
    print(f"  Functions: {stats['functions']}")
    print(f"  Classes: {stats['classes']}")
    print(f"  Documented: {stats['documented']}")
    print(f"  PEP-257 Violations: {stats['violations']} (âš ï¸ {stats['warnings']}, âŒ {stats['errors']})")
```

---

## Tips and Best Practices

1. **Always call `attach_parents()` before `map_nodes()`** - Required for proper parent tracking
2. **Use `build_docstring()` instead of specific format functions** - More flexible and maintainable
3. **Check PEP-257 before and after** - Validate your improvements
4. **Re-parse after modifications** - If modifying AST-dependent code
5. **Load configuration with `load_pyproject()`** - Keep settings in one place

---

## Error Handling

```python
import ast
from pydocstringGenerator import attach_parents, map_nodes

try:
    code = "def broken(: pass"  # Invalid syntax
    tree = ast.parse(code)
except SyntaxError as e:
    print(f"Syntax Error: {e}")

# load_pyproject() gracefully returns {} on error
from pydocstringGenerator import load_pyproject
config = load_pyproject()  # Won't crash if file missing
```

---

## Need Help?

- ðŸ“– Check [README.md](README.md) for overview
- ðŸ’¬ Open an issue on [GitHub](https://github.com/himanshu-chawla/pydocstringGenerator)
- ðŸ“§ Contact: himanshu@example.com
