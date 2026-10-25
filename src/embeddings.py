from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class EmbeddingService:
    """
    Generate embeddings for code and questions.
    """

    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)

    def embed_documents(self, texts):
        """
        Convert a list of code snippets into vectors.
        """

        return self.model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True,
        )

    def embed_query(self, question):
        """
        Convert a question into a vector.
        """

        return self.model.encode(
            question,
            normalize_embeddings=True,
            convert_to_numpy=True,
        )