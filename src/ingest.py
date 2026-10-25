from pathlib import Path

SUPPORTED_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".java",
    ".md",
}

IGNORED_DIRECTORIES = {
    ".git",
    "node_modules",
    "venv",
    ".venv",
    "__pycache__",
    "dist",
    "build",
}

IGNORED_FILES = {
    ".env",
    ".env.local",
}


def collect_code_files(repository_path):
    """
    Find supported source files inside a repository.
    """

    root = Path(repository_path).resolve()

    if not root.exists():
        raise FileNotFoundError(
            f"Repository not found: {root}"
        )

    if not root.is_dir():
        raise NotADirectoryError(
            f"Expected a directory: {root}"
        )

    code_files = []

    for file_path in root.rglob("*"):

        if not file_path.is_file():
            continue

        if any(
            part in IGNORED_DIRECTORIES
            for part in file_path.relative_to(root).parts
        ):
            continue

        if file_path.name in IGNORED_FILES:
            continue

        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        # Avoid indexing unexpectedly large files.
        if file_path.stat().st_size > 1_000_000:
            continue

        code_files.append(file_path)

    return sorted(code_files)


def read_code_file(file_path):
    """
    Read a source file as text.
    """

    try:
        return Path(file_path).read_text(
            encoding="utf-8",
            errors="replace",
        )

    except OSError as error:
        print(f"Could not read {file_path}: {error}")
        return ""


def load_repository(repository_path):
    """
    Load supported files and their contents.
    """

    root = Path(repository_path).resolve()
    files = collect_code_files(root)

    documents = []

    for file_path in files:

        content = read_code_file(file_path)

        if not content.strip():
            continue

        documents.append(
            {
                "file_path": file_path.relative_to(root).as_posix(),
                "content": content,
            }
        )

    return documents