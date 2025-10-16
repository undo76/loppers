# Loppers

Simplified library for extracting source file skeletons using tree-sitter queries.

Removes function implementations while preserving structure and signatures.

**Requires tree-sitter >= 0.25**

## Features

- ✅ **Functions & Methods** - All regular and async functions
- ✅ **Constructors** - Python `__init__`, Java/TS `constructor()`
- ✅ **Arrow Functions** - JavaScript/TypeScript arrow functions
- ✅ **Class Methods** - Instance, static, class methods
- ✅ **Docstrings** - Python docstrings preserved
- ✅ **Decorators** - Preserved (Python, Java)
- ✅ **Type Hints** - Fully typed library
- ✅ **12 Languages** - Python, JS/TS, Java, Kotlin, Go, Rust, C/C++, C#, Ruby, PHP

See [HANDLED_CASES.md](HANDLED_CASES.md) for comprehensive list of supported cases.

## Installation

### With uv (recommended)

```bash
# Install from source
uv pip install -e .

# Or sync with pyproject.toml
uv sync

# Install with dev dependencies
uv sync --extra dev
```

### With pip

```bash
pip install tree-sitter>=0.25.0 tree-sitter-language-pack
```

## Usage

```python
from loppers import extract

source: str = '''
def calculate(x: int, y: int) -> int:
    """Calculate sum."""
    result: int = x + y
    return result
'''

skeleton: str = extract(source, "python")
print(skeleton)
```

Output:
```python
def calculate(x: int, y: int) -> int:
    """Calculate sum."""
```

### Concatenate Files

The library includes utilities for concatenating files with optional skeleton extraction:

```python
from loppers import concatenate_files

# Concatenate all text files in directories, extracting skeletons
result = concatenate_files(
    ["src/", "tests/"],          # Mix of files and directories
    recursive=True,              # Recursively traverse
    extract_skeletons=True,      # Extract code skeletons
    verbose=True,                # Print progress
)
print(result)
```

**Features**:
- Automatically detects and skips binary files
- Extracts code skeletons for supported languages
- Includes original content for unsupported file types
- Files separated by `---` headers

**Binary File Detection**: Uses the `binaryornot` library for simple, reliable binary file detection.

## Supported Languages

- Python (with docstring preservation)
- JavaScript / TypeScript (including arrow functions)
- Java (including constructors)
- Kotlin (functions, getters, setters)
- Go
- Rust
- C / C++
- C#
- Ruby
- PHP

## Development

### Setup

```bash
# Create environment and install dev dependencies
uv sync --extra dev
```

### Testing with pytest

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run with coverage
uv run pytest --cov=loppers --cov-report=html

# Run specific test
uv run pytest test_loppers.py::TestSkeletonExtractor::test_python_extraction

# Run with markers
uv run pytest -m "not slow"
```

### Code Quality with ruff

```bash
# Check code style
uv run ruff check .

# Fix issues automatically
uv run ruff check . --fix

# Format code (included in check --fix)
uv run ruff format .

# Run all checks
uv run ruff check . && uv run ruff format .
```

### Release & Publishing

This project uses [Python Semantic Release](https://python-semantic-release.readthedocs.io/) for automated versioning and publishing to PyPI.

#### Prerequisites

- GitHub repository with branch protection rules (if desired)
- PyPI account with a token
- GitHub token (for pushing version commits)

#### Publish to PyPI

```bash
# Requires: GITHUB_TOKEN and PYPI_TOKEN environment variables set
# The command will:
# 1. Analyze commits since last release using conventional commits
# 2. Bump version automatically (major/minor/patch)
# 3. Build package distributions (sdist + wheel)
# 4. Publish to PyPI

uv run semantic-release publish
```

#### Manual Build (without publishing)

```bash
# Build distributions locally (creates dist/ folder)
uv run python -m build

# View built files
ls -lh dist/
```

#### Configuration

Release settings are in `pyproject.toml` under `[tool.semantic_release]`:
- Version pattern, branch, build command, etc.
- See [DEVELOPMENT.md](DEVELOPMENT.md) for detailed configuration

#### Commit Message Format

Uses [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` - New feature (bumps minor version)
- `fix:` - Bug fix (bumps patch version)
- `BREAKING CHANGE:` - Major version bump
- `docs:`, `chore:`, `refactor:` - No version bump

### How It Works

Uses tree-sitter queries to find and remove function/method body nodes while keeping:
- Function signatures
- Class definitions
- Import statements
- **Python docstrings**
- Comments

## API

### `extract(source_code: str, language: str) -> str`

Extract skeleton from source code.

**Args:**
- `source_code`: Source code to process
- `language`: Programming language

**Returns:** Skeleton with implementations removed

**Raises:**
- `ValueError`: If language not supported

### `SkeletonExtractor(language: str)`

Create extractor for a specific language.

**Methods:**
- `extract(source_code: str) -> str`: Extract skeleton

**Raises:**
- `ValueError`: If language not supported

### `concatenate_files(file_paths, recursive=False, verbose=False, extract_skeletons=True) -> str`

Concatenate files with optional skeleton extraction.

**Args:**
- `file_paths`: List of file and/or directory paths
- `recursive`: Recursively traverse directories (default: False)
- `verbose`: Print debug information (default: False)
- `extract_skeletons`: Enable skeleton extraction (default: True)

**Returns:** Concatenated content with file headers

**Features:**
- Automatically detects and skips binary files
- Extracts skeletons for supported languages
- Includes full content for unsupported text files

### `collect_files(paths, recursive=False, verbose=False, include_all_text_files=True) -> list[Path]`

Collect files from paths, excluding binary files.

**Args:**
- `paths`: List of file and/or directory paths
- `recursive`: Recursively traverse directories
- `verbose`: Print debug information
- `include_all_text_files`: Include all text files or only recognized languages

**Returns:** Sorted list of file paths

### `is_binary_file(file_path) -> bool`

Detect if a file is binary using the `binaryornot` library.

**Args:**
- `file_path`: Path to file

**Returns:** True if binary, False if text

**Detection Method:**
Uses the `binaryornot` library which checks:
- Known binary file extensions
- Null bytes in file content
- UTF-8 decoding success

## Adding Languages

To add a new language, extend `LANGUAGE_CONFIGS` with a tree-sitter query:

```python
LANGUAGE_CONFIGS["newlang"] = LanguageConfig(
    name="newlang",
    body_query="(function_definition body: (block) @body)",
)
```

Find the correct query for your language by exploring the tree-sitter grammar.

## Type Hints

This project uses comprehensive type hints throughout. All functions are fully typed.

```python
# Example of type hints in use
def extract(source_code: str, language: str) -> str:
    """Extract skeleton from source code."""
    extractor: SkeletonExtractor = SkeletonExtractor(language)
    return extractor.extract(source_code)
```

## Configuration Files

- **pyproject.toml**: Project metadata, dependencies, pytest, and ruff configuration
- **HANDLED_CASES.md**: Comprehensive list of supported cases
- **.gitignore**: Git ignore rules
- **UV_GUIDE.md**: uv package manager quick reference
- **DEVELOPMENT.md**: Detailed development guide

```
.
├── loppers.py              # Core library (typed)
├── examples.py             # Usage examples (typed)
├── test_loppers.py         # Unit tests (typed)
├── pyproject.toml          # uv/pip + pytest + ruff config
├── .gitignore              # Git ignore rules
├── README.md               # This file
├── UV_GUIDE.md             # uv quick reference
└── requirements.txt        # Legacy requirements
```

## tree-sitter API Changes (>= 0.25)

Key changes in the code for tree-sitter >= 0.25:
- Language wrapping: `Language(tree_sitter_language_pack.get_language(...))`
- Parser language assignment: `parser.language = lang` (property instead of `set_language()`)

## References

- [tree-sitter](https://tree-sitter.github.io/)
- [tree-sitter-language-pack](https://github.com/grantjenks/py-tree-sitter-language-pack)
- [uv - Python packaging](https://github.com/astral-sh/uv)
- [pytest](https://docs.pytest.org/)
- [ruff](https://github.com/astral-sh/ruff)