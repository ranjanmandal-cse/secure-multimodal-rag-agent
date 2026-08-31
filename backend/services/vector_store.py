import faiss
import numpy as np


class VectorStore:
    def __init__(self, dimension: int):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.documents = []

    def add(self, embeddings, documents):
        if len(embeddings) == 0:
            return

        vectors = np.asarray(
            embeddings,
            dtype="float32"
        )

        self.index.add(vectors)
        self.documents.extend(documents)

    def search(self, query_embedding, top_k: int = 3):
        if self.index.ntotal == 0:
            return []

        query_vector = np.asarray(
            [query_embedding],
            dtype="float32"
        )

        distances, indices = self.index.search(
            query_vector,
            min(top_k, self.index.ntotal)
        )

        results = []

        for distance, index in zip(
            distances[0],
            indices[0]
        ):
            if index == -1:
                continue

            results.append({
                "document": self.documents[index],
                "distance": float(distance)
            })

        return results