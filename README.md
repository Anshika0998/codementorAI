# CodeMentor AI

An AI-powered codebase assistant that helps developers understand Python repositories using Retrieval-Augmented Generation (RAG).

## Overview

CodeMentor AI allows developers to ask natural-language questions about a codebase and receive explanations grounded in relevant source-code snippets.

Instead of sending an entire repository to a language model, the application indexes code, retrieves relevant sections through semantic search, and uses a locally hosted language model to generate answers.

## Features

* **Repository Ingestion:** Reads source files from a local repository.
* **Code Chunking:** Splits source code into smaller sections for retrieval.
* **Semantic Embeddings:** Uses Sentence Transformers to represent code as vectors.
* **Vector Search:** Stores and retrieves relevant code snippets using ChromaDB.
* **AI-Powered Explanations:** Uses a locally hosted language model through Ollama.
* **Interactive Interface:** Provides a Streamlit interface for indexing repositories and asking questions.
* **Source Snippets:** Displays retrieved code to help users understand the basis of an answer.

## Technology Stack

* Python
* Retrieval-Augmented Generation (RAG)
* Sentence Transformers
* ChromaDB
* Ollama
* Streamlit

## Architecture

1. The user provides a local repository path.
2. The ingestion module reads supported source files.
3. The chunking module divides the source code into smaller sections.
4. Sentence Transformers generates embeddings for the code chunks.
5. ChromaDB stores the embeddings and associated code.
6. A user's question is converted into an embedding.
7. Semantic search retrieves relevant code snippets.
8. The retrieved context and question are sent to the local language model.
9. Streamlit displays the generated explanation and source snippets.

## Prerequisites

* Python 3.11 or another Python version compatible with the project's dependencies.
* Ollama installed locally.
* A language model downloaded through Ollama.
* Internet access for downloading Python dependencies and the embedding model on first use.

## Installation

Clone the repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd codementorAI
```

Create and activate a virtual environment.

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Download the configured Ollama model:

```powershell
ollama pull qwen2.5:3b
```

Ensure the model name in `src/llm.py` matches the model installed in Ollama.

## Run the Application

From the project root:

```powershell
python -m streamlit run app.py --server.fileWatcherType none
```

Open the local URL displayed in the terminal, usually `http://localhost:8501`.

Enter a repository path, index the repository, and ask a question about its code.

## Project Structure

```text
codementorAI/
├── app.py
├── data/
│   └── sample_repo/
├── src/
│   ├── ingest.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── search.py
│   ├── llm.py
│   ├── rag.py
│   └── indexer.py
├── tests/
├── requirements.txt
├── README.md
└── .gitignore
```

## Limitations

* The application currently runs locally.
* AI-generated explanations depend on the availability of the configured Ollama model.
* Answers depend on the quality of the retrieved code snippets.
* The current implementation is intended as a prototype rather than a production-ready code analysis platform.

## Future Improvements

* Support additional programming languages.
* Improve code-aware chunking and retrieval.
* Add automated tests for ingestion, retrieval, and answer generation.
* Add repository change detection and incremental indexing.
* Evaluate retrieval quality and answer accuracy on a representative set of code questions.

## License

Choose an appropriate open-source license before distributing the project.
