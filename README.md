# Loppers

**Extract source file skeletons using tree-sitter queries.**

Removes function implementations while preserving structure, signatures, and docstrings. Supports 12+ programming languages with a simple, fully-typed Python API.

**Requires: tree-sitter >= 0.25**

## Features

- ✅ **12 Languages** - Python, JS/TS, Java, Kotlin, Go, Rust, C/C++, C#, Ruby, PHP
- ✅ **Smart Extraction** - Functions, methods, constructors, arrow functions, getters/setters
- ✅ **Preserved Elements** - Signatures, class definitions, imports, docstrings, decorators
- ✅ **File Operations** - Concatenate files/directories with binary detection
- ✅ **Fully Typed** - Complete type hints throughout
- ✅ **CLI & Library** - Use as command-line tool or Python library

See [HANDLED_CASES.md](HANDLED_CASES.md) for comprehensive supported language features.

## Quick Start

### Installation

```bash
# With uv (recommended)
uv pip install loppers

# With pip
pip install loppers
```

### Extract Code Skeleton (Python API)

```python
from loppers import extract

source = '''
def calculate(x: int, y: int) -> int:
    """Calculate sum."""
    result = x + y
    return result
'''

skeleton = extract(source, "python")
print(skeleton)
```

Output:
```python
def calculate(x: int, y: int) -> int:
    """Calculate sum."""
```

### Concatenate Files (Python API)

```python
from loppers import concatenate_files

# Combine all text files with skeleton extraction
result = concatenate_files(
    ["src/", "tests/"],
    recursive=True,
    extract_skeletons=True,
    verbose=True,
)
print(result)
```

### Command Line Usage

```bash
# Extract single file
loppers myfile.py

# Process directory recursively
loppers -r src/ -o skeletons.txt

# Include original files (no extraction)
loppers -r src/ --no-extract

# Show progress
loppers -v -r .
```

**Common CLI Examples:**
```bash
# Multiple files
loppers file1.py file2.js file3.java

# Directory traversal
loppers src/                  # Non-recursive
loppers -r src/              # Recursive

# Mix files and directories
loppers -r src/ tests/ docs/

# Save to file
loppers -r . -o combined.txt

# Verbose output
loppers -v -r src/
```

## Supported Languages

| Language | Features |
|----------|----------|
| **Python** | Functions, methods, docstrings preserved |
| **JavaScript/TypeScript** | Functions, arrow functions, methods |
| **Java** | Functions, constructors, methods |
| **Kotlin** | Functions, properties (getters/setters) |
| **Go** | Functions, methods |
| **Rust** | Functions, methods, closures |
| **C/C++** | Functions, methods |
| **C#** | Methods, properties (get/set) |
| **Ruby** | Methods, singleton methods |
| **PHP** | Methods, functions |

## API Reference

### Skeleton Extraction

#### `extract(source_code: str, language: str) -> str`

Extract skeleton from source code.

**Example:**
```python
from loppers import extract

code = "def hello(): print('hi')"
skeleton = extract(code, "python")  # Returns: "def hello():"
```

#### `SkeletonExtractor(language: str)`

Create a language-specific extractor for reuse.

**Example:**
```python
from loppers import SkeletonExtractor

extractor = SkeletonExtractor("python")
skeleton1 = extractor.extract(code1)
skeleton2 = extractor.extract(code2)
```

### File Operations

#### `concatenate_files(file_paths, recursive=False, verbose=False, extract_skeletons=True) -> str`

Concatenate files with optional skeleton extraction.

**Args:**
- `file_paths` - List of file and/or directory paths
- `recursive` - Recursively traverse directories (default: False)
- `verbose` - Print progress to stderr (default: False)
- `extract_skeletons` - Extract code skeletons (default: True)

**Returns:** Concatenated content with `---` headers separating files

**Example:**
```python
from loppers import concatenate_files

result = concatenate_files(
    ["src/", "tests/"],
    recursive=True,
    extract_skeletons=True,
)
# Automatically skips binary files
# Extracts skeletons for supported languages
# Includes original content for unsupported types
```

#### `collect_files(paths, recursive=False, verbose=False, include_all_text_files=True) -> list[Path]`

Collect text files from paths, excluding binary files.

**Returns:** Sorted list of file paths

#### `is_binary_file(file_path: Path) -> bool`

Detect if a file is binary.

Uses the `binaryornot` library which checks:
- Known binary file extensions
- Null bytes in content
- UTF-8 decoding success

**Example:**
```python
from loppers import is_binary_file
from pathlib import Path

if not is_binary_file(Path("image.jpg")):
    process_as_text()
```

### Utility Functions

#### `get_language(extension: str) -> str | None`

Get language identifier from file extension.

**Example:**
```python
from loppers import get_language

get_language(".py")   # Returns: "python"
get_language(".java") # Returns: "java"
get_language(".txt")  # Returns: None
```

## How It Works

Loppers uses **tree-sitter** queries to parse source code into Abstract Syntax Trees (AST) and intelligently remove function/method bodies while preserving:

- Function/method signatures
- Class and interface definitions
- Import statements
- Python docstrings
- Comments
- Decorators
- Type hints

**Language-Specific Queries:**

Each language has a custom tree-sitter query pattern:

```python
# Python: Remove function body but keep docstrings
"(function_definition body: (block) @body)"

# JavaScript: Handle multiple function types
"[(function_declaration body: ...) (arrow_function body: ...) ...]"

# Kotlin: Extract functions and property getters/setters
"[(function_declaration (function_body) @body) (getter ...) (setter ...)]"
```

## Development

### Setup

```bash
# Install with dev dependencies
uv sync --extra dev
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
uv run pytest tests/test_loppers.py::TestSkeletonExtractor::test_python_extraction
```

### Code Quality

```bash
# Check and fix
uv run ruff check . --fix

# Format
uv run ruff format .

# All checks at once
uv run ruff check . --fix && uv run ruff format .
```

### Publishing to PyPI

This project uses [Python Semantic Release](https://python-semantic-release.readthedocs.io/) with conventional commits.

**Commit message format:**
- `feat:` - New feature (bumps minor version)
- `fix:` - Bug fix (bumps patch version)
- `BREAKING CHANGE:` - Major version bump
- `docs:`, `chore:`, `refactor:` - No version bump

**Automated release:**
```bash
# Push to main with conventional commit messages
# GitHub Actions will automatically:
# 1. Analyze commits
# 2. Bump version
# 3. Build distributions
# 4. Publish to PyPI
```

**Manual publishing:**
```bash
# Build locally
uv run python -m build

# View distributions
ls -lh dist/
```

## Adding New Languages

To add support for a new language:

1. **Find the tree-sitter query** - Use the [tree-sitter playground](https://tree-sitter.github.io/tree-sitter/playground) to develop a query that captures function bodies

2. **Add to LANGUAGE_CONFIGS** in `src/loppers/loppers.py`:
   ```python
   LANGUAGE_CONFIGS["mylang"] = LanguageConfig(
       name="mylang",
       body_query="(function_definition body: (block) @body)",
   )
   ```

3. **Add file extensions** to `src/loppers/mapping.py`:
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
       skeleton = extract(code, "mylang")
       self.assertIn("fun hello()", skeleton)
       self.assertNotIn("print", skeleton)
   ```

5. **Add example file** in `examples/sample.ml` showcasing language features

## Project Structure

```
loppers/
├── src/loppers/
│   ├── __init__.py              # Public API exports
│   ├── loppers.py               # Core extraction logic
│   ├── concatenator.py          # File concatenation
│   ├── mapping.py               # Language mapping
│   └── cli.py                   # Command-line interface
├── tests/
│   └── test_loppers.py          # Unit tests (24 tests)
├── examples/
│   ├── sample.py                # Python examples
│   ├── sample.kt                # Kotlin examples
│   └── ...                       # Other language samples
├── pyproject.toml               # Project configuration
├── README.md                    # This file
├── HANDLED_CASES.md             # Detailed language support
└── DEVELOPMENT.md               # Development guide
```

## Dependencies

**Runtime:**
- `tree-sitter>=0.25.0` - AST parsing library
- `tree-sitter-language-pack>=0.10.0` - Language grammars
- `binaryornot>=0.4.4` - Binary file detection

**Development:**
- `pytest>=7.0.0` - Testing framework
- `ruff>=0.1.0` - Linting and formatting
- `python-semantic-release>=8.0.0` - Release automation

## References

- [tree-sitter Documentation](https://tree-sitter.github.io/)
- [tree-sitter-language-pack](https://github.com/grantjenks/py-tree-sitter-language-pack)
- [binaryornot Library](https://github.com/audreyr/binaryornot)
- [uv Package Manager](https://github.com/astral-sh/uv)
- [Conventional Commits](https://www.conventionalcommits.org/)

## License

MIT - See LICENSE file for details
