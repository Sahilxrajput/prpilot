from pathlib import Path

from app.services.rag.chunker import chunk_repository

chunks = chunk_repository(Path("."))

print(f"\nTotal Chunks: {len(chunks)}\n")

for chunk in chunks[:10]:
    print("=" * 50)
    print("Language :", chunk["language"])
    print("Type     :", chunk["type"])
    print("Name     :", chunk["name"])
    print("File     :", chunk["file"])
    print("Lines    :", f'{chunk["start_line"]}-{chunk["end_line"]}')
    print()
    print(chunk["content"][:300])
    print()

# from pathlib import Path

# from app.services.rag.chunker import chunk_repository

# chunks = chunk_repository(Path("./test_repo"))

# for chunk in chunks:
#     print(chunk["language"], chunk["type"], chunk["file"])
