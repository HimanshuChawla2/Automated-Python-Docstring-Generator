# Common Use Cases and Examples

Quick copy-paste examples for common tasks with `pydocstringGenerator`.

---

## 1. Quick Documentation Coverage Check

```python
import ast
from pydocstringGenerator import attach_parents, map_nodes

# Read a Python file
with open("your_script.py") as f:
    code = f.read()

# Analyze
tree = ast.parse(code)
attach_parents(tree)
node_map = map_nodes(tree)

# Calculate coverage
total = len(node_map["functions"]) + len(node_map["classes"])
documented = sum(1 for f in node_map["functions"] if f["has_doc"])
documented += sum(1 for c in node_map["classes"] if c["has_doc"])

coverage = (documented / total * 100) if total else 0
print(f"Documentation Coverage: {documented}/{total} ({coverage:.1f}%)")
```

---

## 2. Add Missing Docstrings (Google Style)

```python
import ast
from pydocstringGenerator import attach_parents, map_nodes, insert_docstrings_into_code

# Read code
with open("code.py") as f:
    code = f.read()

# Parse and analyze
tree = ast.parse(code)
attach_parents(tree)
node_map = map_nodes(tree)

# Add docstrings
updated_code = insert_docstrings_into_code(code, node_map, "Google", "missing")

# Save
with open("code_updated.py", "w") as f:
    f.write(updated_code)

print("âœ… Docstrings added successfully!")
```

---

## 3. Check PEP-257 Compliance

```python
from pydocstringGenerator import check_pep257

with open("my_module.py") as f:
    code = f.read()

violations = check_pep257(code)

if violations:
    print(f"âŒ Found {len(violations)} violations:\n")
    for v in violations:
        print(f"  Line {v.line}: {v.code} - {v.message}")
else:
    print("âœ… Fully PEP-257 compliant!")
```

---

## 4. Generate Docstrings in All Formats

```python
from pydocstringGenerator import build_docstring

name = "calculate_average"
params = ["numbers", "exclude_outliers"]

# Generate in 3 formats
print("GOOGLE:")
print(build_docstring("Google", name, params))

print("\nNUMPY:")
print(build_docstring("NumPy", name, params))

print("\nREST:")
print(build_docstring("reST", name, params))
```

---

## 5. Find All Functions Without Docstrings

```python
import ast
from pydocstringGenerator import attach_parents, map_nodes

with open("script.py") as f:
    code = f.read()

tree = ast.parse(code)
attach_parents(tree)
node_map = map_nodes(tree)

print("Functions missing docstrings:")
for func in node_map["functions"]:
    if not func["has_doc"]:
        params = ", ".join(func["params"]) if func["params"] else ""
        print(f"  - {func['name']}({params})")

print("\nClasses missing docstrings:")
for cls in node_map["classes"]:
    if not cls["has_doc"]:
        print(f"  - {cls['name']}")
    
    # Also check methods
    for method in cls["methods"]:
        if not method["has_doc"]:
            print(f"      - {method['name']}")
```

---

## 6. Batch Process Multiple Files

```python
import ast
from pathlib import Path
from pydocstringGenerator import (
    attach_parents,
    map_nodes,
    insert_docstrings_into_code,
    check_pep257,
)

def process_file(filepath, style="Google"):
    """Process a single Python file."""
    print(f"Processing: {filepath}")
    
    with open(filepath) as f:
        code = f.read()
    
    tree = ast.parse(code)
    attach_parents(tree)
    node_map = map_nodes(tree)
    
    # Check before
    violations_before = check_pep257(code)
    
    # Add docstrings
    updated = insert_docstrings_into_code(code, node_map, style, "missing")
    
    # Check after
    violations_after = check_pep257(updated)
    
    # Save
    output_file = filepath.parent / f"{filepath.stem}_documented.py"
    with open(output_file, "w") as f:
        f.write(updated)
    
    print(f"  âœ… Saved to: {output_file}")
    print(f"  ðŸ“Š Violations before: {len(violations_before)} â†’ after: {len(violations_after)}\n")

# Process all .py files in current directory
for py_file in Path(".").glob("*.py"):
    if py_file.stem not in ["test_", "setup"]:
        process_file(py_file, style="Google")
```

---

## 7. Analyze Exceptions in Functions

```python
import ast
from pydocstringGenerator import attach_parents, map_nodes, detect_raises

with open("code.py") as f:
    code = f.read()

tree = ast.parse(code)
attach_parents(tree)
node_map = map_nodes(tree)

print("Functions that raise exceptions:\n")
for func in node_map["functions"]:
    exceptions = detect_raises(func["node"])
    if exceptions:
        print(f"{func['name']}():")
        for exc in exceptions:
            print(f"  - raises {exc}")
```

---

## 8. Find Generator Functions

```python
import ast
from pydocstringGenerator import attach_parents, map_nodes, detect_yields

with open("code.py") as f:
    code = f.read()

tree = ast.parse(code)
attach_parents(tree)
node_map = map_nodes(tree)

print("Generator functions:\n")
for func in node_map["functions"]:
    if detect_yields(func["node"]):
        print(f"  - {func['name']}()")
```

---

## 9. Extract Class Attributes

```python
import ast
from pydocstringGenerator import detect_attributes

code = '''
class Employee:
    company = "ACME Corp"  # class variable
    
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
    
    def give_raise(self, amount):
        self.salary += amount
        self.last_raise = amount
'''

tree = ast.parse(code)
cls = tree.body[0]
attrs = detect_attributes(cls)

print("Class attributes:", sorted(attrs))
```

---

## 10. Load Configuration and Use It

```python
from pydocstringGenerator import load_pyproject, attach_parents, map_nodes, insert_docstrings_into_code
import ast

# Load from pyproject.toml
config = load_pyproject()
style = config.get("style", "Google")
should_rewrite = config.get("rewrite", False)
min_coverage = config.get("coverage_min", 90)

print(f"Configuration loaded:")
print(f"  Style: {style}")
print(f"  Rewrite: {should_rewrite}")
print(f"  Min Coverage: {min_coverage}%")

# Use the configuration
with open("code.py") as f:
    code = f.read()

tree = ast.parse(code)
attach_parents(tree)
node_map = map_nodes(tree)

mode = "rewrite" if should_rewrite else "missing"
updated = insert_docstrings_into_code(code, node_map, style, mode)

print("\nâœ… Applied configuration!")
```

---

## 11. Generate Detailed Report

```python
import ast
from pydocstringGenerator import (
    attach_parents,
    map_nodes,
    detect_raises,
    detect_yields,
    detect_attributes,
    check_pep257,
)

def generate_report(filepath):
    """Generate a detailed code analysis report."""
    
    with open(filepath) as f:
        code = f.read()
    
    tree = ast.parse(code)
    attach_parents(tree)
    node_map = map_nodes(tree)
    
    # Counts
    func_count = len(node_map["functions"])
    class_count = len(node_map["classes"])
    method_count = sum(len(cls["methods"]) for cls in node_map["classes"])
    
    # Documentation
    func_doc = sum(1 for f in node_map["functions"] if f["has_doc"])
    class_doc = sum(1 for c in node_map["classes"] if c["has_doc"])
    method_doc = sum(
        1 for c in node_map["classes"] 
        for m in c["methods"] if m["has_doc"]
    )
    
    # Special features
    generators = sum(1 for f in node_map["functions"] if detect_yields(f["node"]))
    total_exceptions = sum(
        len(detect_raises(f["node"])) for f in node_map["functions"]
    )
    total_attributes = sum(
        len(detect_attributes(c["node"])) for c in node_map["classes"]
    )
    
    # Compliance
    violations = check_pep257(code)
    warnings = sum(1 for v in violations if v.code.startswith("D2"))
    errors = len(violations) - warnings
    
    # Report
    print(f"\n{'='*60}")
    print(f"CODE ANALYSIS REPORT: {filepath}")
    print(f"{'='*60}\n")
    
    print("STRUCTURE:")
    print(f"  Functions:    {func_count}")
    print(f"  Classes:      {class_count}")
    print(f"  Methods:      {method_count}")
    print(f"  Total Items:  {func_count + class_count + method_count}")
    
    print("\nDOCUMENTATION:")
    total_items = func_count + class_count + method_count
    documented = func_doc + class_doc + method_doc
    coverage = (documented / total_items * 100) if total_items else 0
    print(f"  Functions:    {func_doc}/{func_count}")
    print(f"  Classes:      {class_doc}/{class_count}")
    print(f"  Methods:      {method_doc}/{method_count}")
    print(f"  Coverage:     {documented}/{total_items} ({coverage:.1f}%)")
    
    print("\nFEATURES:")
    print(f"  Generators:   {generators}")
    print(f"  Exceptions:   {total_exceptions}")
    print(f"  Attributes:   {total_attributes}")
    
    print("\nCOMPLIANCE (PEP-257):")
    print(f"  Violations:   {len(violations)}")
    print(f"  âš ï¸  Warnings:   {warnings}")
    print(f"  âŒ Errors:     {errors}")
    
    if violations:
        print("\nVIOLATION DETAILS:")
        for v in violations[:5]:  # Show first 5
            print(f"  Line {v.line}: {v.code} - {v.message}")
        if len(violations) > 5:
            print(f"  ... and {len(violations) - 5} more")

# Run report
generate_report("your_file.py")
```

---

## 12. Interactive Docstring Editor

```python
import ast
from pydocstringGenerator import attach_parents, map_nodes, build_docstring

with open("code.py") as f:
    code = f.read()

tree = ast.parse(code)
attach_parents(tree)
node_map = map_nodes(tree)

functions = node_map["functions"]

# Interactive selection
for i, func in enumerate(functions, 1):
    print(f"{i}. {func['name']}({', '.join(func['params'])})")
    if func["has_doc"]:
        print("   âœ… Already documented")
    else:
        print("   âš ï¸  Missing docstring")

# Get user choice
choice = int(input("\nSelect function to generate docstring for (number): ")) - 1
selected_func = functions[choice]

# Show choice
print(f"\nGenerated docstring for {selected_func['name']}:\n")
docstring = build_docstring("Google", selected_func['name'], selected_func['params'])
print(docstring)
```

---

## Tips for Integration

### In a CI/CD Pipeline

```python
# validate.py - Run before commit
import sys
from pydocstringGenerator import check_pep257

with open("my_module.py") as f:
    code = f.read()

violations = check_pep257(code)
if violations:
    print(f"âŒ PEP-257 violations found: {len(violations)}")
    sys.exit(1)
else:
    print("âœ… Code is PEP-257 compliant")
    sys.exit(0)
```

### As a Pre-commit Hook

```python
# pre-commit.py - Run before git commit
import subprocess
import sys
from pathlib import Path

# Get all modified Python files
result = subprocess.run(
    ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
    capture_output=True,
    text=True
)

files = [f for f in result.stdout.split('\n') if f.endswith('.py')]

for file in files:
    print(f"Checking {file}...")
    # Your validation logic here

sys.exit(0)
```

---

For more details on each function, see [DOCUMENTATION.md](DOCUMENTATION.md).
