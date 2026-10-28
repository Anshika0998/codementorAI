from pathlib import Path

from src.ingest import load_repository
from src.chunker import chunk_document
from src.embeddings import EmbeddingService
from src.vector_store import CodeVectorStore


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATABASE_PATH = PROJECT_ROOT / "chroma_db"


def index_repository(repository_path):
    """
    Read, chunk, embed, and store a repository.
    """

    repository = Path(repository_path).expanduser().resolve()

    if not repository.is_dir():
        raise ValueError(
            f"Repository directory does not exist: {repository}"
        )

    print(f"Reading repository: {repository}")

    documents = load_repository(repository)

    if not documents:
        raise ValueError(
            "No supported source files were found in the repository."
        )

    print(f"Loaded {len(documents)} files.")

    chunks = []

    for document in documents:
        chunks.extend(chunk_document(document))

    if not chunks:
        raise ValueError(
            "No code chunks were created from the repository."
        )

    print(f"Created {len(chunks)} code chunks.")

    embedding_service = EmbeddingService()

    texts = [
        (
            f"File: {chunk['file_path']}\n"
            f"Symbol: {chunk['name']}\n"
            f"{chunk['code']}"
        )
        for chunk in chunks
    ]

    print("Generating embeddings...")

    embeddings = embedding_service.embed_documents(texts)

    vector_store = CodeVectorStore(
        database_path=str(DATABASE_PATH)
    )

    vector_store.add_chunks(
        chunks=chunks,
        embeddings=embeddings,
    )

    return {
        "files": len(documents),
        "chunks": len(chunks),
        "database": str(DATABASE_PATH),
    }
