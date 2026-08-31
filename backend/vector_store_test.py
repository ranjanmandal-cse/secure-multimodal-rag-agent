from services.knowledge_loader import load_documents
from services.chunking import chunk_text
from services.embedding_service import create_embeddings
from services.vector_store import VectorStore


documents = load_documents()

chunks = []

for document in documents:
    document_chunks = chunk_text(document["text"])

    for chunk in document_chunks:
        chunks.append({
            "filename": document["filename"],
            "text": chunk
        })


texts = [
    chunk["text"]
    for chunk in chunks
]

embeddings = create_embeddings(texts)

dimension = embeddings.shape[1]

store = VectorStore(dimension)

store.add(
    embeddings,
    chunks
)


query = """
Customer was asked to share an OTP.
"""

query_embedding = create_embeddings(
    [query]
)[0]

results = store.search(
    query_embedding,
    top_k=3
)


print("===== VECTOR SEARCH =====")

for result in results:
    print()
    print("FILE:", result["document"]["filename"])
    print("DISTANCE:", result["distance"])
    print("TEXT:")
    print(result["document"]["text"])