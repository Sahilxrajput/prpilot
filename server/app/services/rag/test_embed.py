from server.app.services.rag.embedder import embed_text


vector = embed_text("def login(username, password): pass")

print(type(vector))
print(len(vector))
print(vector[:5])
