
import chromadb


COLLECTION_NAME = "codementor_code"


class CodeVectorStore:
    """
    Store code chunks and search them using ChromaDB.
    """

    def __init__(self, database_path="chroma_db"):
        self.client = chromadb.PersistentClient(
            path=database_path
        )

        self.collection = (
            self.client.get_or_create_collection(
                name=COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"},
            )
        )

    def add_chunks(self, chunks, embeddings):
        """
        Save code chunks and their embeddings.
        """

        if not chunks:
            return

        self.collection.upsert(
            ids=[chunk["id"] for chunk in chunks],
            embeddings=embeddings.tolist(),
            documents=[chunk["code"] for chunk in chunks],
            metadatas=[
                {
                    "file_path": chunk["file_path"],
                    "name": chunk["name"],
                    "start_line": chunk["start_line"],
                    "end_line": chunk["end_line"],
                }
                for chunk in chunks
            ],
        )

    def search(self, query_embedding, top_k=5):
        """
        Retrieve the most relevant code chunks.
        """

        total = self.collection.count()

        if total == 0:
            return []

        results = self.collection.query(
            query_embeddings=[
                query_embedding.tolist()
            ],
            n_results=min(top_k, total),
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )

        matches = []

        for index in range(len(results["ids"][0])):
            matches.append(
                {
                    "id": results["ids"][0][index],
                    "code": results["documents"][0][index],
                    "metadata": results["metadatas"][0][index],
                    "distance": results["distances"][0][index],
                }
            )

        return matches
