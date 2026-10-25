from pathlib import Path

from src.ingest import load_repository
from src.chunker import chunk_document
from src.embeddings import EmbeddingService
from src.vector_store import CodeVectorStore


PROJECT_ROOT = Path(__file__).resolve().parent.parent

SAMPLE_REPOSITORY = (
    PROJECT_ROOT / "data" / "sample_repo"
)

DATABASE_PATH = PROJECT_ROOT / "chroma_db"


def build_index():
    """
    Read the sample repository, chunk its code,
    generate embeddings, and store them in ChromaDB.
    """

    print("Loading repository...")

    documents = load_repository(
        SAMPLE_REPOSITORY
    )

    print(f"Loaded {len(documents)} files.")

    chunks = []

    for document in documents:
        chunks.extend(
            chunk_document(document)
        )

    print(f"Created {len(chunks)} code chunks.")

    if not chunks:
        print("No code chunks were found.")
        return

    print("Loading embedding model...")

    embedding_service = EmbeddingService()

    code_texts = [
        (
            f"File: {chunk['file_path']}\n"
            f"Symbol: {chunk['name']}\n"
            f"{chunk['code']}"
        )
        for chunk in chunks
    ]

    embeddings = embedding_service.embed_documents(
        code_texts
    )

    print("Connecting to ChromaDB...")

    vector_store = CodeVectorStore(
        database_path=str(DATABASE_PATH)
    )

    vector_store.add_chunks(
        chunks,
        embeddings,
    )

    print("Indexing completed successfully!")


def search_code(question):
    """
    Search the indexed repository for relevant code.
    """

    embedding_service = EmbeddingService()

    vector_store = CodeVectorStore(
        database_path=str(DATABASE_PATH)
    )

    query_embedding = embedding_service.embed_query(
        question
    )

    matches = vector_store.search(
        query_embedding=query_embedding,
        top_k=5,
    )

    return matches


def main():
    """
    Command-line interface for semantic code search.
    """

    build_index()

    print("\nCodeMentor AI semantic search is ready.")

    while True:

        question = input(
            "\nAsk a question about the code "
            "(or type 'exit'): "
        ).strip()

        if question.lower() in {
            "exit",
            "quit",
        }:
            print("Goodbye!")
            break

        if not question:
            print("Please enter a question.")
            continue

        matches = search_code(question)

        if not matches:
            print("No indexed code was found.")
            continue

        print("\nRelevant code snippets:\n")

        for index, match in enumerate(
            matches,
            start=1,
        ):

            metadata = match["metadata"]

            print(f"Result {index}")
            print(
                f"File: {metadata['file_path']}"
            )
            print(
                f"Symbol: {metadata['name']}"
            )
            print(
                f"Lines: {metadata['start_line']}"
                f"-{metadata['end_line']}"
            )
            print(
                f"Distance: {match['distance']:.4f}"
            )
            print("Code:")
            print(match["code"])
            print("-" * 50)


if __name__ == "__main__":
    main()