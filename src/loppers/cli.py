"""CLI tool for concatenating files with skeleton extraction."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from loppers.loppers import extract
from loppers.mapping import EXTENSION_TO_LANGUAGE, get_language


def collect_files(
    paths: list[str | Path],
    recursive: bool = False,
    verbose: bool = False,
) -> list[Path]:
    """Collect files from paths, expanding directories if requested.

    Args:
        paths: List of file paths or directory paths
        recursive: If True, recursively traverse directories
        verbose: Print debug information to stderr

    Returns:
        Sorted list of file paths to process
    """
    collected: set[Path] = set()

    for path_item in paths:
        path = Path(path_item)

        if path.is_file():
            collected.add(path)
        elif path.is_dir():
            if recursive:
                # Recursively find all supported files in the directory
                for ext in EXTENSION_TO_LANGUAGE:
                    for file_path in path.rglob(f"*{ext}"):
                        if file_path.is_file():
                            collected.add(file_path)
            else:
                # Only find files in the directory (non-recursive)
                for file_path in path.iterdir():
                    if file_path.is_file():
                        ext = file_path.suffix.lower()
                        if ext in EXTENSION_TO_LANGUAGE:
                            collected.add(file_path)
                        elif verbose:
                            print(
                                f"⊘ Skipping unsupported file: {file_path.name}",
                                file=sys.stderr,
                            )
        else:
            if verbose:
                print(f"Warning: Path not found: {path}", file=sys.stderr)

    # Return sorted list for consistent output
    return sorted(collected)


def concatenate_files(
    file_paths: list[str | Path],
    recursive: bool = False,
    verbose: bool = False,
) -> str:
    """Concatenate files with skeleton extraction and file headers.

    Accepts files and/or directories. Attempts to extract skeleton from each
    file using its language. If extraction fails, includes the original file
    content. Files are separated with headers indicating their names.

    Args:
        file_paths: List of file and/or directory paths
        recursive: If True, recursively traverse directories for supported files
        verbose: Print debug information to stderr

    Returns:
        Concatenated content with file headers and skeletons
    """
    # Collect all files to process
    files_to_process = collect_files(file_paths, recursive=recursive, verbose=verbose)

    if not files_to_process:
        if verbose:
            print("Warning: No files to process", file=sys.stderr)
        return ""

    results: list[str] = []

    for file_path in files_to_process:
        path = Path(file_path)

        # Check if file exists
        if not path.exists():
            if verbose:
                print(f"Warning: File not found: {path}", file=sys.stderr)
            continue

        # Read file content
        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, IOError) as e:
            if verbose:
                print(f"Warning: Could not read {path}: {e}", file=sys.stderr)
            continue

        # Create header
        header = f"--- {path}\n"

        # Attempt skeleton extraction
        language = get_language(str(path.suffix))

        if language:
            try:
                skeleton = extract(content, language)
                body = skeleton
                if verbose:
                    print(f"✓ Extracted skeleton from {path.name}", file=sys.stderr)
            except Exception as e:
                if verbose:
                    print(
                        f"⚠ Could not extract skeleton from {path.name}: {e}",
                        file=sys.stderr,
                    )
                body = content
        else:
            if verbose:
                print(f"⚠ Unknown language for {path.name}, keeping as-is", file=sys.stderr)
            body = content

        results.append(header + body + "\n")

    return "\n".join(results).rstrip()


def main() -> None:
    """CLI entry point for concatenating files with skeleton extraction.

    Processes files and directories, extracting code skeletons.
    """
    parser = argparse.ArgumentParser(
        description="Concatenate files with skeleton extraction",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  loppers file1.py file2.js              # Multiple files
  loppers src/                           # Directory (non-recursive)
  loppers -r src/                        # Recursively process directory
  loppers -r src/ tests/                 # Multiple directories
  loppers -o skeletons.txt -r .          # All supported files from current dir
  loppers -v *.py                        # Verbose output
  loppers -o combined.txt -r src/        # Recursive with output file
        """,
    )

    parser.add_argument(
        "files",
        nargs="+",
        help="Files and/or directories to process",
    )

    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Recursively traverse directories for supported files",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Output file (default: stdout)",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print verbose output to stderr",
    )

    args = parser.parse_args()

    # Concatenate files
    result = concatenate_files(
        args.files,
        recursive=args.recursive,
        verbose=args.verbose,
    )

    # Output result
    if args.output:
        Path(args.output).write_text(result, encoding="utf-8")
        if args.verbose:
            print(f"✓ Written to {args.output}", file=sys.stderr)
    else:
        print(result)


if __name__ == "__main__":
    main()
