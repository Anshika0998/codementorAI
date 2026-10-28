from pathlib import Path

import streamlit as st

from src.indexer import index_repository
from src.rag import CodeMentorRAG


PROJECT_ROOT = Path(__file__).resolve().parent

DEFAULT_REPOSITORY = PROJECT_ROOT / "data" / "sample_repo"


st.set_page_config(
    page_title="CodeMentor AI",
    page_icon="💻",
    layout="wide",
)


st.title("💻 CodeMentor AI")

st.markdown(
    """
    ### Your AI-powered codebase assistant

    Explore an unfamiliar codebase, understand functions,
    and ask questions about how your project works.

    **Powered by RAG, semantic search, ChromaDB, and Ollama.**
    """
)


with st.sidebar:
    st.header("⚙️ Repository Settings")

    repository_path = st.text_input(
        "Repository folder path",
        value=str(DEFAULT_REPOSITORY),
        help=(
            "Enter the absolute path to a local repository "
            "that you want to analyze."
        ),
    )

    st.caption(
        "Use a local folder you trust. Avoid indexing secrets, "
        "API keys, passwords, or private files."
    )

    if st.button("📂 Index Repository", use_container_width=True):
        try:
            with st.spinner("Indexing repository..."):
                result = index_repository(repository_path)

            st.session_state["indexed_repository"] = str(
                Path(repository_path).expanduser().resolve()
            )

            st.success("Repository indexed successfully!")

            st.write(f"Files processed: {result['files']}")
            st.write(f"Code chunks created: {result['chunks']}")

        except Exception as error:
            st.error(f"Indexing failed: {error}")


st.divider()

st.subheader("💬 Ask a question about your code")

st.write(
    "First click **Index Repository** in the sidebar. "
    "Then ask a question below."
)

question = st.text_area(
    "Your question",
    placeholder=(
        "Example: How does the login function work?\n"
        "Example: Which function connects to the database?\n"
        "Example: Explain the flow of app.py."
    ),
    height=110,
)

if st.button("✨ Explain Code", type="primary"):
    if not question.strip():
        st.warning("Please enter a question first.")

    elif not st.session_state.get("indexed_repository"):
        st.warning("Please index a repository first.")

    else:
        try:
            with st.spinner(
                "Searching your code and generating an explanation..."
            ):
                assistant = CodeMentorRAG()
                result = assistant.ask(question)

            st.subheader("🧠 AI Explanation")

            st.markdown(result["answer"])

            st.subheader("📚 Retrieved Sources")

            if not result["sources"]:
                st.info("No source snippets were retrieved.")

            for index, source in enumerate(
                result["sources"],
                start=1,
            ):
                title = (
                    f"{index}. {source['file_path']} — "
                    f"{source['name']}"
                )

                with st.expander(title):
                    st.write(
                        "Lines: "
                        f"{source['start_line']}-"
                        f"{source['end_line']}"
                    )

                    st.code(
                        source["code"],
                        language="python",
                    )

                    distance = source.get("distance")

                    if distance is not None:
                        st.caption(
                            "Vector distance: "
                            f"{distance:.4f}"
                        )

        except Exception as error:
            st.error(f"Something went wrong: {error}")


st.divider()

st.caption(
    "CodeMentor AI is a prototype. Review generated explanations "
    "against the actual source code before relying on them."
)
