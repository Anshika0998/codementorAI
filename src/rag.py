from pathlib import Path

from src.embeddings import EmbeddingService
from src.vector_store import CodeVectorStore
from src.llm import generate_answer


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATABASE_PATH = PROJECT_ROOT / "chroma_db"


class CodeMentorRAG:
    """
    Connect semantic code search with LLM-based explanations.
    """

    def __init__(self):
        self.embedding_service = EmbeddingService()

        self.vector_store = CodeVectorStore(
            database_path=str(DATABASE_PATH)
        )

    def ask(self, question, top_k=5):
        """
        Retrieve relevant code and generate an answer.
        """

        if not question or not question.strip():
            return {
                "answer": "Please enter a question.",
                "sources": [],
            }

        # Step 1: Convert the question into an embedding.
        query_embedding = self.embedding_service.embed_query(
            question.strip()
        )

        # Step 2: Retrieve relevant code snippets.
        matches = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        if not matches:
            return {
                "answer": (
                    "No indexed code was found. "
                    "Please index a repository first."
                ),
                "sources": [],
            }

        # Step 3: Build the context for the language model.
        context_parts = []
        sources = []

        for index, match in enumerate(matches, start=1):
            metadata = match["metadata"]

            file_path = metadata.get(
                "file_path",
                "Unknown file",
            )

            name = metadata.get(
                "name",
                "Unknown symbol",
            )

            start_line = metadata.get("start_line", "?")
            end_line = metadata.get("end_line", "?")

            code = match["code"]

            context_parts.append(
                f"""
Source {index}
File: {file_path}
Symbol: {name}
Lines: {start_line}-{end_line}

Code:
{code}
"""
            )

            sources.append(
                {
                    "file_path": file_path,
                    "name": name,
                    "start_line": start_line,
                    "end_line": end_line,
                    "distance": match.get("distance"),
                    "code": code,
                }
            )

        context = "\n".join(context_parts)

        # Step 4: Ask the LLM to explain the retrieved code.
        answer = generate_answer(
            question=question.strip(),
            context=context,
        )

        # Step 5: Return the answer and source metadata.
        return {
            "answer": answer,
            "sources": sources,
        }