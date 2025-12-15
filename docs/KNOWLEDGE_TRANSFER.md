# PyClassStruct - Knowledge Transfer Document

## Overview

**PyClassStruct** is a Python CLI tool that converts simple Python scripts into well-organized, class-based structures. It analyzes Python code, detects function relationships, and generates structured class files.

---

## Architecture

```
pyclassstruct/
├── src/pyclassstruct/
│   ├── __init__.py          # Package initialization, exports
│   ├── __main__.py           # Entry point for `python -m pyclassstruct`
│   ├── cli.py                # Click-based CLI commands
│   ├── analyzer/             # Code analysis module
│   │   ├── __init__.py       # Analyzer exports
│   │   ├── models.py         # Data models (dataclasses)
│   │   ├── ast_parser.py     # AST-based code parsing
│   │   ├── dependency.py     # Dependency analysis & grouping
│   │   ├── keyword_matcher.py # Advanced keyword matching (commented out)
│   │   └── keywords.json     # Keyword config (for future use)
│   ├── generator/            # Code generation module
│   │   ├── __init__.py       # Generator exports
│   │   ├── naming.py         # Naming utilities (snake_case, CamelCase)
│   │   ├── class_builder.py  # Builds Python class source code
│   │   └── structure.py      # Orchestrates conversion process
│   ├── reporter/             # Report generation module
│   │   ├── __init__.py       # Reporter exports
│   │   └── report.py         # Generates report.txt and classes.txt
│   └── utils/                # Utility functions
│       ├── __init__.py       # Utils exports
│       └── file_ops.py       # File operations
├── tests/sample_scripts/     # Test input files
├── docs/                     # Documentation
├── pyproject.toml            # Package configuration
├── README.md                 # User documentation
└── LICENSE                   # MIT License
```

---

## Module Details

### 1. CLI Module (`cli.py`)

**Purpose**: Provides the command-line interface using the `click` library.

**Commands**:

| Command          | Description                                                   |
| ---------------- | ------------------------------------------------------------- |
| `analyze <path>` | Analyze Python files, generate `report.txt` and `classes.txt` |
| `convert <path>` | Convert scripts to structured classes in `structured/` folder |
| `info <path>`    | Quick overview of functions and proposed classes              |

**Key Options**:
- `--force` / `-f`: Overwrite existing files without prompting
- `--classes <file>`: Specify custom classes.txt path
- `--output <dir>`: Specify output directory name

**Flow**:
```
User runs command
    ↓
cli.py parses arguments
    ↓
Calls analyzer to analyze files
    ↓
Calls reporter/generator based on command
    ↓
Outputs results
```

---

### 2. Analyzer Module (`analyzer/`)

#### 2.1 Models (`models.py`)

**Purpose**: Defines data structures using Python `dataclasses`.

| Class            | Description                                                         |
| ---------------- | ------------------------------------------------------------------- |
| `FunctionInfo`   | Stores function metadata (name, args, calls, docstring, decorators) |
| `GlobalVarInfo`  | Stores global variable info (name, type, value)                     |
| `ImportInfo`     | Stores import statement info                                        |
| `ClassProposal`  | Proposed class structure with methods and properties                |
| `FileAnalysis`   | Analysis result for a single file                                   |
| `FolderAnalysis` | Analysis result for a folder (multiple files)                       |

**Example `FunctionInfo`**:
```python
@dataclass
class FunctionInfo:
    name: str                    # Function name
    args: List[str]             # Function arguments
    calls: Set[str]             # Functions this function calls
    global_reads: Set[str]      # Global variables read
    global_writes: Set[str]     # Global variables written
    docstring: Optional[str]    # Function docstring
    decorators: List[str]       # Applied decorators
    is_async: bool              # Is async function
    line_start: int             # Starting line number
    line_end: int               # Ending line number
```

#### 2.2 AST Parser (`ast_parser.py`)

**Purpose**: Uses Python's `ast` module to parse source code and extract information.

**Key Class**: `CodeParser`

**What it extracts**:
- Function definitions (name, args, body, decorators)
- Function calls within each function
- Global variable assignments
- Import statements
- Docstrings and type hints

**How it works**:
```python
import ast

class CodeParser(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
        # Extract function info
        pass
    
    def visit_Call(self, node):
        # Track function calls
        pass
    
    def visit_Assign(self, node):
        # Track global variables
        pass
```

#### 2.3 Dependency Analyzer (`dependency.py`)

**Purpose**: Analyzes function relationships and groups them into classes.

**Key Class**: `DependencyAnalyzer`

**Grouping Strategies** (in order):

1. **Strategy 1 - Common Prefix**: Functions with same prefix go together
   ```
   user_create, user_delete, user_update → UserManager
   ```

2. **Strategy 2 - Domain Keywords**: Uses keyword dictionary to find class names
   ```python
   keywords = {
       'user': 'UserManager',
       'database': 'DatabaseManager',
       'file': 'FileHandler',
       'validate': 'Validator',
       # ... 18 keywords total
   }
   ```

3. **Strategy 3 - Call Graph**: Functions that call each other are grouped
   ```
   If A calls B and B calls C → same class
   ```

4. **Strategy 4 - Advanced JSON Matcher** (commented out for v1.0):
   - Uses `keywords.json` config file
   - Supports stemming (validate/validation/validator)
   - Priority-weighted scoring

**Call Graph Building**:
```python
# Forward graph: who does this function call?
call_graph[func_name] = {called_func1, called_func2}

# Reverse graph: who calls this function?
reverse_call_graph[func_name] = {caller1, caller2}
```

---

### 3. Generator Module (`generator/`)

#### 3.1 Naming Utilities (`naming.py`)

**Purpose**: Handles naming convention conversions.

| Function                | Input            | Output              |
| ----------------------- | ---------------- | ------------------- |
| `to_snake_case()`       | `"UserManager"`  | `"user_manager"`    |
| `to_camel_case()`       | `"user_manager"` | `"UserManager"`     |
| `to_filename()`         | `"UserManager"`  | `"user_manager.py"` |
| `sanitize_identifier()` | `"123-test"`     | `"_123_test"`       |

#### 3.2 Class Builder (`class_builder.py`)

**Purpose**: Generates Python class source code from `ClassProposal` objects.

**Key Functions**:

| Function               | Purpose                                  |
| ---------------------- | ---------------------------------------- |
| `build_class()`        | Generate a single class file             |
| `build_module()`       | Generate file with multiple classes      |
| `_build_init_method()` | Generate `__init__` with properties      |
| `_build_method()`      | Convert function to method (adds `self`) |
| `_build_imports()`     | Generate import statements               |

**Generated Class Structure**:
```python
"""
Auto-generated class.
"""

class UserManager:
    """User management operations."""
    
    def __init__(self):
        """Initialize UserManager."""
        pass
    
    def create_user(self, username, email, password):
        """Create a new user."""
        # Implementation from original function
        pass
```

#### 3.3 Structure Generator (`structure.py`)

**Purpose**: Orchestrates the entire conversion process.

**Key Class**: `StructureGenerator`

**Features**:
- Reads `classes.txt` for user-defined structure
- Groups classes into files
- Generates individual class files
- **Merge Mode**: Preserves existing classes, adds only new methods

**Merge Workflow**:
```
1. Check if class file exists
2. If yes, extract existing method names
3. Compare with classes.txt methods
4. Add only NEW methods to existing file
5. Preserve all existing code
```

---

### 4. Reporter Module (`reporter/`)

#### 4.1 Report Generator (`report.py`)

**Purpose**: Generates analysis reports and class definition files.

**Key Class**: `ReportGenerator`

**Output Files**:

| File          | Content                                           |
| ------------- | ------------------------------------------------- |
| `report.txt`  | Statistics, functions list, proposed classes      |
| `classes.txt` | Editable class definitions for user customization |

**`report.txt` Sections**:
- Statistics (function count, class count, etc.)
- Functions Detected (with call relationships)
- Global Variables Detected
- Proposed Class Structure (visual tree)

**`classes.txt` Format**:
```txt
# PyClassStruct Class Definitions
# Format: ClassName: function1, function2, function3

FileHandler: read_file, write_file, delete_file
UserManager: create_user, update_user, delete_user
Utils: format_date, generate_id
```

---

### 5. Utils Module (`utils/`)

#### 5.1 File Operations (`file_ops.py`)

**Purpose**: Common file system utilities.

| Function              | Purpose                           |
| --------------------- | --------------------------------- |
| `check_file_exists()` | Check if a path exists            |
| `is_python_file()`    | Check if file has `.py` extension |
| `is_directory()`      | Check if path is a directory      |
| `ensure_directory()`  | Create directory if not exists    |

---

## Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                        USER INPUT                            │
│              (Python file or folder path)                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      CLI (cli.py)                            │
│                   Parse command & options                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   AST PARSER (ast_parser.py)                 │
│         Parse Python source → Extract functions/vars         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              DEPENDENCY ANALYZER (dependency.py)             │
│     Build call graph → Detect patterns → Propose classes     │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              │                               │
              ▼                               ▼
┌─────────────────────────┐     ┌─────────────────────────────┐
│  REPORTER (report.py)   │     │   GENERATOR (structure.py)  │
│  Generate report.txt    │     │   Generate class files      │
│  Generate classes.txt   │     │   Merge with existing       │
└─────────────────────────┘     └─────────────────────────────┘
              │                               │
              ▼                               ▼
┌─────────────────────────┐     ┌─────────────────────────────┐
│      report.txt         │     │      structured/            │
│      classes.txt        │     │   ├── user_manager.py       │
│                         │     │   ├── file_handler.py       │
│                         │     │   └── __init__.py           │
└─────────────────────────┘     └─────────────────────────────┘
```

---

## Key Design Decisions

### 1. AST-Based Parsing
**Why**: More reliable than regex, handles edge cases, provides accurate line numbers.

### 2. Dataclasses for Models
**Why**: Clean, immutable data structures with auto-generated `__init__`, `__repr__`.

### 3. Strategy Pattern for Grouping
**Why**: Multiple strategies ensure flexible class detection even with minimal patterns.

### 4. Merge Instead of Overwrite
**Why**: Users can iteratively add functions without losing manual edits.

### 5. Click for CLI
**Why**: Popular, well-documented, supports subcommands and options elegantly.

---

## Configuration

### Keywords Dictionary
Located in `dependency.py`, easily extendable:
```python
keywords = {
    'user': 'UserManager',
    'database': 'DatabaseManager', 
    'file': 'FileHandler',
    # Add more as needed
}
```

### Advanced Keywords (Future)
Located in `keywords.json`, supports:
- Categories with priorities
- Stem mappings (word variations)
- User customization

---

## Extending the Tool

### Adding New Keywords
Edit `dependency.py` Strategy 2 keywords dictionary.

### Adding New Grouping Strategy
Add a new method in `DependencyAnalyzer`:
```python
def _group_by_custom(self) -> Dict[str, Set[str]]:
    # Your custom grouping logic
    pass
```
Then add to `detect_class_proposals()`.

### Adding New CLI Command
Add to `cli.py`:
```python
@main.command()
@click.argument('path')
def newcommand(path):
    """Description of new command."""
    # Implementation
```

---

## Dependencies

| Package | Version | Purpose                 |
| ------- | ------- | ----------------------- |
| `click` | >=8.0.0 | CLI framework           |
| Python  | >=3.8   | Required Python version |

---

## Testing

### Sample Scripts
Located in `tests/sample_scripts/`:
- `user_management.py` - User/database functions
- `file_handler.py` - File I/O functions  
- `product_manager.py` - Magic method patterns

### Running Tests
```bash
# Analyze samples
pyclassstruct analyze ./tests/sample_scripts --force

# Convert samples
pyclassstruct convert ./tests/sample_scripts

# Check generated output
ls ./tests/sample_scripts/structured/
```

---

## Troubleshooting

| Issue                           | Solution                                   |
| ------------------------------- | ------------------------------------------ |
| "No class structures generated" | Check if input has valid Python functions  |
| Command not found               | Reinstall with `pip install -e .`          |
| Merge not working               | Delete `structured/` folder and regenerate |
| Wrong class names               | Edit `classes.txt` and re-run convert      |

---

## Version History

| Version | Changes                                              |
| ------- | ---------------------------------------------------- |
| 1.0.0   | Initial release with analyze, convert, info commands |
| 1.0.1   | Added incremental merge, improved documentation      |

---

## Development Guide (For Contributors)

### Setting Up Development Environment

#### 1. Clone the Repository
```bash
git clone https://github.com/Mirjan-Ali-Sha/pyclassstruct.git
cd pyclassstruct
```

#### 2. Create Virtual Environment
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux/Mac
python -m venv .venv
source .venv/bin/activate
```

#### 3. Install in Development Mode
```bash
pip install -e ".[dev]"
```
This installs the package in editable mode + development dependencies (pytest).

#### 4. Verify Installation
```bash
pyclassstruct --help
python -m pyclassstruct --help
```

---

### Project Structure for Development

```
pyclassstruct/
├── src/pyclassstruct/     # Main source code
│   ├── analyzer/          # ADD: New analysis features here
│   ├── generator/         # ADD: New generation features here
│   ├── reporter/          # ADD: New reporting features here
│   └── utils/             # ADD: New utilities here
├── tests/
│   ├── sample_scripts/    # ADD: New test input files here
│   └── test_*.py          # ADD: Unit tests here (TODO)
├── docs/                  # ADD: Documentation here
└── pyproject.toml         # Package configuration
```

---

### Development Workflow

#### Step 1: Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

#### Step 2: Make Changes
- Edit source files in `src/pyclassstruct/`
- Follow the coding standards below

#### Step 3: Test Locally
```bash
# Reinstall to pick up changes
pip install -e .

# Test with sample scripts
pyclassstruct analyze ./tests/sample_scripts --force
pyclassstruct convert ./tests/sample_scripts

# Check generated output
cat ./tests/sample_scripts/structured/*.py
```

#### Step 4: Commit Changes
```bash
git add .
git commit -m "feat: description of your feature"
```

#### Step 5: Push & Create Pull Request
```bash
git push origin feature/your-feature-name
```
Then create a PR on GitHub.

---

### Coding Standards

#### File/Class Naming
| Type      | Convention         | Example              |
| --------- | ------------------ | -------------------- |
| Files     | `snake_case.py`    | `class_builder.py`   |
| Classes   | `PascalCase`       | `StructureGenerator` |
| Functions | `snake_case`       | `build_class()`      |
| Constants | `UPPER_SNAKE_CASE` | `DEFAULT_OUTPUT_DIR` |

#### Docstrings
Use Google-style docstrings:
```python
def function_name(arg1: str, arg2: int) -> bool:
    """
    Brief description of function.
    
    Args:
        arg1: Description of arg1
        arg2: Description of arg2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When something is wrong
    """
    pass
```

#### Type Hints
Always use type hints for function signatures:
```python
from typing import List, Dict, Optional, Tuple

def analyze_file(filepath: str) -> Optional[FileAnalysis]:
    pass
```

#### Imports Order
1. Standard library imports
2. Third-party imports
3. Local imports

```python
# Standard library
import os
from pathlib import Path
from typing import List

# Third-party
import click

# Local
from pyclassstruct.analyzer import analyze_file
```

---

### Adding New Features

#### Adding a New CLI Command

1. Edit `src/pyclassstruct/cli.py`:
```python
@main.command()
@click.argument('path')
@click.option('--option', '-o', help='Description')
def yourcommand(path, option):
    """Command description shown in help."""
    # Your implementation
    click.echo("Done!")
```

2. Test:
```bash
pyclassstruct yourcommand ./path --option value
```

#### Adding a New Keyword

1. Edit `src/pyclassstruct/analyzer/dependency.py`:
```python
keywords = {
    # ... existing keywords ...
    'yourkeyword': 'YourClassName',  # Add your keyword
}
```

2. Test with a sample script containing that keyword.

#### Adding a New Grouping Strategy

1. Add method in `DependencyAnalyzer` class:
```python
def _group_by_your_strategy(self) -> Dict[str, Set[str]]:
    """Group functions by your custom logic."""
    groups = {}
    # Your grouping logic
    return groups
```

2. Add to `detect_class_proposals()`:
```python
def detect_class_proposals(self):
    # ... existing strategies ...
    your_groups = self._group_by_your_strategy()
    merged = self._merge_groups(call_groups, naming_groups, state_groups, your_groups)
```

#### Adding a New Data Model

1. Edit `src/pyclassstruct/analyzer/models.py`:
```python
@dataclass
class YourModel:
    """Description of your model."""
    field1: str
    field2: int = 0
    field3: List[str] = field(default_factory=list)
```

2. Export from `__init__.py`:
```python
from .models import YourModel
```

---

### Testing Guidelines

#### Manual Testing
```bash
# Clean previous output
rm -rf ./tests/sample_scripts/structured/
rm -f ./tests/sample_scripts/report.txt
rm -f ./tests/sample_scripts/classes.txt

# Run full test cycle
pyclassstruct analyze ./tests/sample_scripts --force
pyclassstruct convert ./tests/sample_scripts

# Verify output
cat ./tests/sample_scripts/classes.txt
cat ./tests/sample_scripts/structured/file_handler.py
```

#### Adding Unit Tests (TODO)
Create test files in `tests/`:
```python
# tests/test_analyzer.py
import pytest
from pyclassstruct.analyzer import analyze_file

def test_analyze_simple_file():
    result = analyze_file("tests/sample_scripts/user_management.py")
    assert result is not None
    assert len(result.functions) > 0

def test_analyze_nonexistent_file():
    result = analyze_file("nonexistent.py")
    assert result is None
```

Run tests:
```bash
pytest tests/ -v
```

---

### Building & Publishing

#### Build Package
```bash
# Install build tools
pip install build twine

# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Build
python -m build

# Verify contents
ls dist/
# pyclassstruct-X.X.X-py3-none-any.whl
# pyclassstruct-X.X.X.tar.gz
```

#### Publish to PyPI
```bash
# Upload to TestPyPI first (optional)
python -m twine upload --repository testpypi dist/*

# Upload to PyPI
python -m twine upload dist/*

# When prompted:
# Username: __token__
# Password: <your-pypi-api-token>
```

#### Version Bumping
Edit `pyproject.toml`:
```toml
[project]
version = "1.0.2"  # Increment version
```

---

### Common Development Tasks

| Task             | Command                                     |
| ---------------- | ------------------------------------------- |
| Install dev mode | `pip install -e ".[dev]"`                   |
| Run CLI          | `pyclassstruct <command>`                   |
| Run as module    | `python -m pyclassstruct <command>`         |
| Clean outputs    | `rm -rf ./tests/sample_scripts/structured/` |
| Build package    | `python -m build`                           |
| Check package    | `twine check dist/*`                        |

---

### Debugging Tips

#### Enable Verbose Output
Add debug prints in your code:
```python
import click
click.echo(f"DEBUG: {variable}", err=True)
```

#### Check AST Parsing
```python
import ast
with open('yourfile.py') as f:
    tree = ast.parse(f.read())
    print(ast.dump(tree, indent=2))
```

#### Check Generated Proposals
Add to `cli.py` temporarily:
```python
for proposal in analysis.class_proposals:
    click.echo(f"Class: {proposal.name}")
    click.echo(f"  Methods: {proposal.method_names}")
```

---

## Contact

**Author**: Mirjan Ali Sha  
**Repository**: https://github.com/Mirjan-Ali-Sha/pyclassstruct  
**License**: MIT
