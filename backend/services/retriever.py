from services.knowledge_loader import load_documents
from services.chunking import chunk_text
from services.embedding_service import create_embeddings
from services.vector_store import VectorStore


class Retriever:
    def __init__(self):
        self.chunks = []
        self.store = None

        self._build_index()

    def _build_index(self):
        documents = load_documents()

        for document in documents:
            chunks = chunk_text(document["text"])

            for chunk in chunks:
                self.chunks.append({
                    "filename": document["filename"],
                    "text": chunk
                })

        if not self.chunks:
            return

        texts = [
            chunk["text"]
            for chunk in self.chunks
        ]

        embeddings = create_embeddings(texts)

        dimension = embeddings.shape[1]

        self.store = VectorStore(dimension)

        self.store.add(
            embeddings,
            self.chunks
        )

    def retrieve(self, query: str, top_k: int = 3):
        if not query or not self.store:
            return []

        query_embedding = create_embeddings(
            [query]
        )[0]

        return self.store.search(
            query_embedding,
            top_k=top_k
        )