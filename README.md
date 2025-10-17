# Loppers

**Extract source file skeletons using tree-sitter queries.**

Removes function implementations while preserving structure, signatures, and docstrings. Supports 17 programming languages with a clean, fully-typed Python API and comprehensive CLI.

**Requires: tree-sitter >= 0.25**

## Features

- ✅ **17 Languages** - Python, JS/TS, Java, Kotlin, Go, Rust, C/C++, C#, Ruby, PHP, Swift, Lua, Scala, Groovy, Objective-C
- ✅ **Smart Extraction** - Functions, methods, constructors, arrow functions, getters/setters
- ✅ **Preserved Elements** - Signatures, class definitions, imports, docstrings, decorators
- ✅ **All File Types** - Process any non-binary text files (code, markdown, JSON, YAML, etc.)
- ✅ **Binary Detection** - Automatically skips binary files
- ✅ **Ignore Patterns** - Built-in + custom .gitignore support
- ✅ **Fully Typed** - Complete type hints throughout
- ✅ **CLI & Library** - Use as command-line tool or Python library

## Quick Start

### Installation

```bash
# With uv (recommended)
uv pip install loppers

# With pip
pip install loppers
```

## Python API

The public API consists of 4 core functions:

### 1. `extract_skeleton(source: str, language: str) -> str`

Extract skeleton from source code by language identifier.

```python
from loppers import extract_skeleton

code = """
def calculate(x: int, y: int) -> int:
    '''Calculate sum.'''
    result = x + y
    return result
"""

skeleton = extract_skeleton(code, "python")
print(skeleton)
```

Output:
```python
def calculate(x: int, y: int) -> int:
    '''Calculate sum.'''
```

### 2. `get_skeleton(file_path: Path | str, *, add_header: bool = False) -> str`

Extract skeleton from a file by auto-detecting language from extension.

```python
from loppers import get_skeleton

skeleton = get_skeleton("src/main.py")
print(skeleton)

# With header showing file path
skeleton = get_skeleton("src/main.py", add_header=True)
# Output: "--- /path/to/src/main.py\n..."
```

**Raises:**
- `FileNotFoundError` - If file doesn't exist
- `ValueError` - If file language is unsupported

### 3. `find_files(root: str | Path, *, recursive: bool = True, ignore_patterns: Sequence[str] | None = None, use_default_ignore: bool = True, respect_gitignore: bool = True) -> list[str]`

Collect all non-binary text files from a root directory.

```python
from loppers import find_files

# Find all text files in src/ recursively (default)
files = find_files("src/")

# Returns file paths relative to root:
# ['main.py', 'utils.py', 'config.yaml', 'README.md']

# Non-recursive
files = find_files("src/", recursive=False)

# Custom ignore patterns (gitignore syntax)
files = find_files(
    "src/",
    ignore_patterns=["*.test.py", "venv/"],
    use_default_ignore=True,  # Still applies built-in patterns
    respect_gitignore=True,   # Still respects .gitignore
)
```

**Features:**
- Takes single root directory (not multiple paths)
- Returns file paths relative to root
- Automatically excludes binary files (images, archives, etc.)
- Respects `.gitignore` by default
- Supports custom gitignore-style ignore patterns
- Built-in patterns exclude node_modules, .git, __pycache__, build artifacts, etc.
- Works with ALL non-binary text files (code, markdown, JSON, YAML, etc.)

### 4. `get_tree(root: str | Path, *, recursive: bool = True, ignore_patterns: Sequence[str] | None = None, use_default_ignore: bool = True, respect_gitignore: bool = True) -> str`

Display formatted directory tree from a root directory.

```python
from loppers import get_tree

# Display tree of src/ directory recursively
tree = get_tree("src/")
print(tree)

# Non-recursive tree
tree = get_tree("src/", recursive=False)

# With custom ignore patterns
tree = get_tree("src/", ignore_patterns=["*.test.py"])
```

Output:
```
.
└─ main.py
   ├─ utils.py
   ├─ config.yaml
   └─ models/
      └─ user.py
```

### Utility Function

**`get_language(extension: str) -> str | None`** - Get language identifier from file extension.

```python
from loppers import get_language

get_language(".py")    # "python"
get_language(".js")    # "javascript"
get_language(".json")  # None (no extraction for data files)
```

## Command-Line Interface

Loppers provides 4 subcommands for common tasks.

### Basic Usage

```bash
loppers --version
loppers --help
```

### 1. `extract` - Extract skeleton from file or stdin

Extract a single file's skeleton:
```bash
# From file
loppers extract file.py
loppers extract file.py -o skeleton.py

# From stdin with explicit language
echo 'def foo(): pass' | loppers extract -l python

# Verbose output
loppers extract file.py -v
```

**Options:**
- `FILE` - File to extract (omit for stdin)
- `-l, --language` - Language identifier (auto-detected from extension if FILE provided, required for stdin)
- `-o, --output` - Output file (default: stdout)
- `-v, --verbose` - Print status to stderr

### 2. `concatenate` - Concatenate files with optional skeleton extraction

Process root directory with automatic skeleton extraction:

```bash
# Recursive (default)
loppers concatenate src/

# Non-recursive
loppers concatenate --no-recursive src/

# Save to file
loppers concatenate src/ -o combined.txt

# Verbose with progress
loppers concatenate -v src/

# Include original files without extraction
loppers concatenate --no-extract src/

# Custom ignore patterns
loppers concatenate -I "*.test.py" -I "venv/" src/

# Disable default ignores
loppers concatenate --no-default-ignore src/

# Don't respect .gitignore
loppers concatenate --no-gitignore src/
```

**Features:**
- Processes a single root directory (paths relative to root)
- Includes ALL non-binary text files (code, markdown, JSON, YAML, etc.)
- Automatically extracts skeletons for supported code files
- Includes original content for unsupported file types (graceful degradation)
- Each file prefixed with `--- filepath` header (relative path)
- Verbose mode shows extraction status for each file

**Options:**
- `root` - Root directory to process (required)
- `-o, --output` - Output file (default: stdout)
- `--no-extract` - Include original files without extraction
- `-I, --ignore-pattern` - Add custom ignore pattern (gitignore syntax, can be used multiple times)
- `--no-default-ignore` - Disable built-in ignore patterns
- `--no-gitignore` - Don't respect .gitignore
- `--no-recursive` - Don't recursively traverse directories
- `-v, --verbose` - Print status to stderr

### 3. `tree` - Show directory tree of discovered files

Display a formatted tree of all discovered files:

```bash
# Recursive tree (default)
loppers tree src/

# Non-recursive
loppers tree --no-recursive src/

# Save tree to file
loppers tree src/ -o tree.txt

# With ignore patterns
loppers tree -I "*.test.py" src/
```

**Options:**
- `root` - Root directory to process (required)
- `-o, --output` - Output file (default: stdout)
- `-I, --ignore-pattern` - Add custom ignore pattern
- `--no-default-ignore` - Disable built-in ignore patterns
- `--no-gitignore` - Don't respect .gitignore
- `--no-recursive` - Non-recursive tree
- `-v, --verbose` - Print status to stderr

### 4. `files` - List all discovered files

Print one discovered file per line (relative to root):

```bash
# List all files recursively (default)
loppers files src/

# Save list to file
loppers files src/ -o file_list.txt

# Non-recursive
loppers files --no-recursive src/

# With custom ignores
loppers files -I "*.md" src/
```

**Options:**
- `root` - Root directory to process (required)
- `-o, --output` - Output file (default: stdout)
- `-I, --ignore-pattern` - Add custom ignore pattern
- `--no-default-ignore` - Disable built-in ignore patterns
- `--no-gitignore` - Don't respect .gitignore
- `--no-recursive` - Non-recursive listing
- `-v, --verbose` - Print status to stderr

## Examples: Before and After

### Python Example

**Before:**
```python
class Calculator:
    def __init__(self, name: str):
        """Initialize calculator."""
        self.name = name
        self._setup()

    def process(self, data):
        """Process data."""
        result = []
        for item in data:
            result.append(item * 2)
        return result
```

**After:**
```python
class Calculator:
    def __init__(self, name: str):
        """Initialize calculator."""

    def process(self, data):
        """Process data."""
```

### JavaScript/TypeScript Example

**Before:**
```typescript
class UserService {
    constructor(baseUrl: string) {
        this.baseUrl = baseUrl;
        this.cache = {};
    }

    async getUser(id: string) {
        if (this.cache[id]) return this.cache[id];
        const user = await fetch(this.baseUrl + '/' + id);
        return user.json();
    }
}
```

**After:**
```typescript
class UserService {
    constructor(baseUrl: string) {
    }

    async getUser(id: string) {
    }
}
```

### Java Example

**Before:**
```java
public class UserService {
    private String baseUrl;

    public UserService(String baseUrl) {
        this.baseUrl = baseUrl;
        this.validate();
    }

    public User getUserById(String id) {
        Database db = new Database();
        return db.query(id);
    }

    private void validate() {
        if (baseUrl == null) {
            throw new IllegalArgumentException("BaseUrl required");
        }
    }
}
```

**After:**
```java
public class UserService {
    private String baseUrl;

    public UserService(String baseUrl) {
    }

    public User getUserById(String id) {
    }

    private void validate() {
    }
}
```

## Supported Languages

| Language | Features |
|----------|----------|
| **Python** | Functions, methods, `__init__`, `@property`, docstrings |
| **JavaScript/TypeScript** | Functions, arrow functions, methods, async/await |
| **Java** | Methods, constructors, static methods, annotations |
| **Kotlin** | Functions, methods, properties (getters/setters) |
| **Go** | Functions, methods, closures |
| **Rust** | Functions, methods, closures |
| **C/C++** | Functions, methods, constructors |
| **C#** | Methods, properties (get/set), async/await |
| **Ruby** | Methods, singleton methods, blocks |
| **PHP** | Functions, methods, closures |
| **Swift** | Functions, methods, closures |
| **Lua** | Functions, local functions |
| **Scala** | Functions, methods, closures |
| **Groovy** | Functions, methods, closures |
| **Objective-C** | Methods, instance/class methods |

### What Gets Preserved

- ✅ Function/method signatures
- ✅ Parameter types and defaults
- ✅ Return types
- ✅ Class definitions
- ✅ Import statements
- ✅ Comments
- ✅ Python docstrings
- ✅ Decorators
- ✅ Access modifiers (public, private, protected)

### What Gets Removed

- ❌ Function/method bodies
- ❌ Local variable assignments
- ❌ Logic and implementation details
- ❌ Nested function implementations

### Known Limitations

- Concise arrow functions (`const f = x => x * 2`) - no body to remove
- Python lambdas - no body to remove
- Some edge cases with getters/setters in JavaScript/TypeScript

## How It Works

Loppers uses **tree-sitter** queries to parse source code into Abstract Syntax Trees (AST) and intelligently remove function/method bodies while preserving:

- Function/method signatures
- Class and interface definitions
- Import statements
- Python docstrings
- Comments
- Decorators
- Type hints

Each language has custom tree-sitter query patterns that capture function/method body nodes, which are then removed line-by-line.

## Development

### Setup

```bash
# Install with dev dependencies
uv sync
```

### Running Tests

```bash
# All tests
uv run pytest

# Verbose output
uv run pytest -v

# With coverage
uv run pytest --cov=loppers --cov-report=html

# Specific test
uv run pytest tests/test_loppers.py::test_python_extraction
```

### Code Quality

```bash
# Check and fix
uv run ruff check . --fix

# Format
uv run ruff format .

# All checks
uv run ruff check . --fix && uv run ruff format .
```

### Adding New Languages

To add support for a new language:

1. **Find the tree-sitter query** - Use the [tree-sitter playground](https://tree-sitter.github.io/tree-sitter/playground) to develop a query that captures function bodies

2. **Add to LANGUAGE_CONFIGS** in `src/loppers/loppers.py`:
   ```python
   LANGUAGE_CONFIGS["mylang"] = LanguageConfig(
       name="mylang",
       body_query="(function_definition body: (block) @body)",
   )
   ```

3. **Add file extensions** to `src/loppers/extensions.py`:
   ```python
   EXTENSION_TO_LANGUAGE = {
       ".ml": "mylang",
       ".mli": "mylang",
   }
   ```

4. **Write a test** in `tests/test_loppers.py`:
   ```python
   def test_mylang_extraction(self):
       code = "fun hello() { print('hi') }"
       skeleton = extract_skeleton(code, "mylang")
       assert "fun hello()" in skeleton
       assert "print" not in skeleton
   ```

5. **Run tests** to verify everything works

## Project Structure

```
loppers/
├── src/loppers/
│   ├── __init__.py              # Public API: extract_skeleton, get_skeleton, find_files, get_tree
│   ├── loppers.py               # Core extraction logic with SkeletonExtractor class
│   ├── source_utils.py          # Convenience API and file operations
│   ├── extensions.py            # Language extension mapping
│   ├── ignore_patterns.py       # Default ignore patterns
│   ├── mapping.py               # Backwards compatibility re-exports
│   └── cli.py                   # Command-line interface (4 subcommands)
├── tests/
│   └── test_loppers.py          # Unit tests (31 tests)
├── pyproject.toml               # Project configuration
├── README.md                    # This file
└── CLAUDE.md                    # Development guide for Claude Code
```

## Dependencies

**Runtime:**
- `tree-sitter>=0.25.0` - AST parsing library
- `tree-sitter-language-pack>=0.10.0` - Language grammars
- `binaryornot>=0.4.4` - Binary file detection
- `pathspec>=0.9.0` - .gitignore pattern matching

**Development:**
- `pytest>=7.0.0` - Testing framework
- `pytest-cov>=4.0.0` - Coverage reporting
- `ruff>=0.1.0` - Linting and formatting

## References

- [tree-sitter Documentation](https://tree-sitter.github.io/)
- [tree-sitter-language-pack](https://github.com/grantjenks/py-tree-sitter-language-pack)
- [binaryornot Library](https://github.com/audreyr/binaryornot)
- [pathspec Library](https://github.com/cpburnz/python-pathspec)
- [uv Package Manager](https://github.com/astral-sh/uv)

## License

MIT - See LICENSE file for details
