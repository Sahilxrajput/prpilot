from pathlib import Path

from app.services.rag.python_chunker import (
    chunk_python_file,
)

from app.services.rag.js_chunker import (
    chunk_javascript_file,
)

from app.services.rag.ts_chunker import (
    chunk_typescript_file,
)

SUPPORTED_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
}


def chunk_file(file_path: str):

    suffix = Path(file_path).suffix.lower()

    if suffix == ".py":
        return chunk_python_file(file_path)

    if suffix in [".js", ".jsx"]:
        return chunk_javascript_file(file_path)

    if suffix in [".ts", ".tsx"]:
        return chunk_typescript_file(file_path)

    return []


def chunk_repository(repo_path: Path):

    all_chunks = []

    ignore_dirs = {
        ".git",
        "node_modules",
        "dist",
        "build",
        ".next",
        ".venv",
        "venv",
    }

    repo_path = Path(repo_path)

    for file in repo_path.rglob("*"):

        if not file.is_file():
            continue

        if any(ignored in file.parts for ignored in ignore_dirs):
            continue

        if file.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        try:
            chunks = chunk_file(str(file))
            all_chunks.extend(chunks)

        except Exception as e:
            print(f"Failed chunking {file}: {e}")

    return all_chunks
