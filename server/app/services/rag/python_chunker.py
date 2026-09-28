import ast
from pathlib import Path


def chunk_python_file(file_path: str):
    path = Path(file_path)

    with open(path, "r", encoding="utf-8") as f:
        source_code = f.read()

    tree = ast.parse(source_code)

    lines = source_code.splitlines()

    chunks = []

    for node in ast.walk(tree):

        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
                ast.ClassDef,
            ),
        ):

            start = node.lineno
            end = getattr(node, "end_lineno", start)

            content = "\n".join(lines[start - 1 : end])

            chunks.append(
                {
                    "id": f"{path.stem}_{node.name}_{start}",
                    "language": "python",
                    "type": type(node).__name__,
                    "name": node.name,
                    "file": str(path),
                    "start_line": start,
                    "end_line": end,
                    "content": content,
                }
            )

    return chunks
