from services.knowledge_loader import load_documents
from services.chunking import chunk_text


documents = load_documents()

print("===== CHUNKING TEST =====")

for document in documents:
    chunks = chunk_text(document["text"])

    print()
    print("FILE:", document["filename"])
    print("NUMBER OF CHUNKS:", len(chunks))

    for index, chunk in enumerate(chunks):
        print()
        print(f"CHUNK {index + 1}:")
        print(chunk)