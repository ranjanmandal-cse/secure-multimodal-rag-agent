from services.knowledge_loader import load_documents
from services.chunking import chunk_text
from services.embedding_service import create_embeddings


documents = load_documents()

all_chunks = []

for document in documents:
    chunks = chunk_text(document["text"])

    for chunk in chunks:
        all_chunks.append({
            "filename": document["filename"],
            "text": chunk
        })


texts = [item["text"] for item in all_chunks]

embeddings = create_embeddings(texts)

print("===== EMBEDDING TEST =====")

print("Number of chunks:", len(texts))

print("Embedding shape:", embeddings.shape)

print("First embedding:")
print(embeddings[0])