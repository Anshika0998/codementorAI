import ast
import hashlib
from pathlib import Path


def make_chunk(
    file_path,
    name,
    start_line,
    end_line,
    code,
):
    """
    Create a code chunk with metadata.
    """

    chunk_id = hashlib.sha256(
        (
            f"{file_path}:{start_line}:"
            f"{end_line}:{code}"
        ).encode("utf-8")
    ).hexdigest()

    return {
        "id": chunk_id,
        "file_path": file_path,
        "name": name,
        "start_line": start_line,
        "end_line": end_line,
        "code": code,
    }


def chunk_python_file(file_path, content):
    """
    Split Python code into functions and classes.

    If parsing fails or the file has no functions/classes,
    use a simple line-based fallback.
    """

    try:
        tree = ast.parse(content)

    except SyntaxError:
        tree = None

    chunks = []

    if tree is not None:

        lines = content.splitlines()

        for node in ast.walk(tree):

            if not isinstance(
                node,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                    ast.ClassDef,
                ),
            ):
                continue

            start_line = node.lineno

            end_line = getattr(
                node,
                "end_lineno",
                start_line,
            )

            code = "\n".join(
                lines[start_line - 1:end_line]
            )

            chunks.append(
                make_chunk(
                    file_path=file_path,
                    name=node.name,
                    start_line=start_line,
                    end_line=end_line,
                    code=code,
                )
            )

    if not chunks:

        lines = content.splitlines()
        chunk_size = 40

        for start in range(
            0,
            len(lines),
            chunk_size,
        ):

            section = lines[
                start:start + chunk_size
            ]

            code = "\n".join(section)

            if not code.strip():
                continue

            chunks.append(
                make_chunk(
                    file_path=file_path,
                    name="file_section",
                    start_line=start + 1,
                    end_line=start + len(section),
                    code=code,
                )
            )

    return chunks


def chunk_document(document):
    """
    Convert a loaded document into searchable chunks.
    """

    file_path = document["file_path"]
    content = document["content"]

    extension = Path(file_path).suffix.lower()

    if extension == ".py":
        return chunk_python_file(
            file_path,
            content,
        )

    return [
        make_chunk(
            file_path=file_path,
            name="file_content",
            start_line=1,
            end_line=max(1, len(content.splitlines())),
            code=content,
        )
    ]