# Quick Start Guide

Get started with `pydocstringGenerator` in 2 minutes.

## Installation

```bash
pip install pydocstringGenerator
```

## 5-Minute Hello World

### Option 1: Check Your Documentation Coverage

```python
import ast
from pydocstringGenerator import attach_parents, map_nodes

# Your Python code
code = '''
def hello(name):
    """Say hello."""
    print(f"Hello {name}")

def goodbye():
    print("Goodbye")
'''

# Parse
tree = ast.parse(code)
attach_parents(tree)
node_map = map_nodes(tree)

# Check documentation
for func in node_map["functions"]:
    status = "âœ…" if func["has_doc"] else "âŒ"
    print(f"{status} {func['name']}: documented={func['has_doc']}")
```

**Output:**
```
âœ… hello: documented=True
âŒ goodbye: documented=False
```

---

### Option 2: Auto-generate Missing Docstrings

```python
import ast
from pydocstringGenerator import attach_parents, map_nodes, insert_docstrings_into_code

code = '''
def add(a, b):
    return a + b

def multiply(x, y):
    """Multiply two numbers."""
    return x * y
'''

# Parse
tree = ast.parse(code)
attach_parents(tree)
node_map = map_nodes(tree)

# Generate missing docstrings
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

def multiply(x, y):
    """Multiply two numbers."""
    return x * y
```

---

### Option 3: Check PEP-257 Compliance

```python
from pydocstringGenerator import check_pep257

code = "def hello(): print('hi')"

violations = check_pep257(code)
print(f"Found {len(violations)} PEP-257 violations")

for v in violations:
    print(f"  Line {v.line}: {v.code} - {v.message}")
```

**Output:**
```
Found 2 PEP-257 violations
  Line 1: D100 - Missing docstring in public module
  Line 1: D103 - Missing docstring in public function
```

---

## The 3 Most Common Tasks

### Task 1: Analyze a File

```python
import ast
from pydocstringGenerator import attach_parents, map_nodes, check_pep257

filename = "my_script.py"

with open(filename) as f:
    code = f.read()

tree = ast.parse(code)
attach_parents(tree)
node_map = map_nodes(tree)

# Count items
funcs = len(node_map["functions"])
classes = len(node_map["classes"])
documented = sum(1 for f in node_map["functions"] if f["has_doc"])

print(f"Functions: {funcs}")
print(f"Classes: {classes}")
print(f"Documented: {documented}/{funcs}")

# Check compliance
violations = check_pep257(code)
print(f"PEP-257 Violations: {len(violations)}")
```

### Task 2: Auto-fix Docstrings

```python
import ast
from pydocstringGenerator import attach_parents, map_nodes, insert_docstrings_into_code

with open("code.py") as f:
    code = f.read()

tree = ast.parse(code)
attach_parents(tree)
node_map = map_nodes(tree)

# Add missing docstrings
updated = insert_docstrings_into_code(code, node_map, "Google", "missing")

# Save
with open("code_updated.py", "w") as f:
    f.write(updated)

print("âœ… Docstrings added!")
```

### Task 3: Find Undocumented Code

```python
import ast
from pydocstringGenerator import attach_parents, map_nodes

with open("code.py") as f:
    code = f.read()

tree = ast.parse(code)
attach_parents(tree)
node_map = map_nodes(tree)

print("Missing documentation:")

for func in node_map["functions"]:
    if not func["has_doc"]:
        print(f"  Function: {func['name']}")

for cls in node_map["classes"]:
    if not cls["has_doc"]:
        print(f"  Class: {cls['name']}")
```

---

## Import Cheat Sheet

all available functions you can import:

```python
from pydocstringGenerator import (
    # Configuration
    load_pyproject,
    
    # Analysis
    attach_parents,
    extract_parameters,
    map_nodes,
    detect_raises,
    detect_yields,
    detect_attributes,
    
    # Docstring generation
    build_docstring,
    generate_docstring_google,
    generate_docstring_numpy,
    generate_docstring_rest,
    
    # Code modification
    add_module_docstring,
    insert_docstrings_into_code,
    
    # Validation
    check_pep257,
)
```

---

## What Each Function Does

| Function | Purpose |
|----------|---------|
| `attach_parents()` | **REQUIRED** before using map_nodes - adds parent references |
| `map_nodes()` | Analyze code structure - returns functions and classes |
| `build_docstring()` | Generate docstring template |
| `insert_docstrings_into_code()` | Add/replace docstrings in code |
| `check_pep257()` | Check docstring compliance |
| `detect_raises()` | Find exceptions in function |
| `detect_yields()` | Check if function is generator |
| `detect_attributes()` | Find class attributes |
| `extract_parameters()` | Get function parameters |
| `add_module_docstring()` | Add module-level docstring |
| `load_pyproject()` | Load configuration from pyproject.toml |

---

## Next Steps

1. **Run examples:** See [EXAMPLES.md](EXAMPLES.md) for copy-paste code
2. **API reference:** Check [DOCUMENTATION.md](DOCUMENTATION.md) for detailed function docs
3. **README:** Read [README.md](README.md) for overview and features

---

## Troubleshooting

### Import Error: Cannot import 'milestone2'

Make sure the library is installed:
```bash
pip install pydocstringGenerator
```

Then import as `milestone2`:
```python
from pydocstringGenerator import map_nodes
```

### SyntaxError when parsing code

The code you're trying to parse must be valid Python:
```python
import ast

try:
    tree = ast.parse(code)
except SyntaxError as e:
    print(f"Invalid Python: {e}")
```

### Need to call `attach_parents()` first

Always do this sequence:
```python
import ast
from pydocstringGenerator import attach_parents, map_nodes

tree = ast.parse(code)
attach_parents(tree)              # âš ï¸ Required!
node_map = map_nodes(tree)        # Now this works
```

---

## Common Workflows

### Workflow 1: Add Docstrings to Existing Code

```bash
# 1. Write Python code without docstrings
# 2. Run this script:
```

```python
import ast
from pydocstringGenerator import attach_parents, map_nodes, insert_docstrings_into_code

with open("my_code.py") as f:
    code = f.read()

tree = ast.parse(code)
attach_parents(tree)
node_map = map_nodes(tree)

updated = insert_docstrings_into_code(code, node_map, "Google", "missing")

with open("my_code.py", "w") as f:
    f.write(updated)
```

### Workflow 2: Check Code Quality

```python
import ast
from pydocstringGenerator import attach_parents, map_nodes, check_pep257

files = ["module1.py", "module2.py", "module3.py"]

for filepath in files:
    with open(filepath) as f:
        code = f.read()
    
    violations = check_pep257(code)
    status = "âœ…" if not violations else "âŒ"
    print(f"{status} {filepath}: {len(violations)} violations")
```

---

## Video Tutorial (Text Version)

```
Step 1: Import library
  from pydocstringGenerator import attach_parents, map_nodes
  
Step 2: Read your Python code
  with open("code.py") as f:
      code = f.read()
  
Step 3: Parse and attach parents
  tree = ast.parse(code)
  attach_parents(tree)
  
Step 4: Analyze
  node_map = map_nodes(tree)
  
Step 5: Use the results
  functions = node_map["functions"]
  classes = node_map["classes"]
  
That's it! ðŸŽ‰
```

---

## Help & Support

- ðŸ“– Full docs: https://github.com/himanshu-chawla/pydocstringGenerator
- ðŸ’¬ Issues: https://github.com/himanshu-chawla/pydocstringGenerator/issues
- ðŸ“§ Email: himanshu@example.com

Happy documenting! ðŸš€
