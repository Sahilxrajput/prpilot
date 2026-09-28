from pathlib import Path
from tree_sitter import Parser, Language
from tree_sitter_typescript import (
    language_typescript,
)


def chunk_typescript_file(file_path: str):

    parser = Parser(Language(language_typescript()))

    path = Path(file_path)

    source_code = path.read_text(encoding="utf-8")

    tree = parser.parse(bytes(source_code, "utf8"))

    chunks = []

    stack = [tree.root_node]

    while stack:

        node = stack.pop()

        if node.type in [
            "function_declaration",
            "class_declaration",
            "method_definition",
            "interface_declaration",
            "type_alias_declaration",
        ]:

            content = source_code[node.start_byte : node.end_byte]

            chunks.append(
                {
                    "id": f"{path.stem}_{node.type}_{node.start_point[0]}",
                    "language": "typescript",
                    "type": node.type,
                    "name": node.type,
                    "file": str(path),
                    "start_line": node.start_point[0] + 1,
                    "end_line": node.end_point[0] + 1,
                    "content": content,
                }
            )

        stack.extend(node.children)

    return chunks
