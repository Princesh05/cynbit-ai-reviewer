
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from app.ai.knowledge_base import load_python_knowledge


EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

_vector_store = None


def create_vector_store():
    """Initialize ChromaDB only once and reuse it."""

    global _vector_store

    if _vector_store is not None:
        return _vector_store

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    vector_store = Chroma(
        collection_name="cynbit_python_knowledge_v2",
        embedding_function=embeddings,
        persist_directory="./data/chroma_db"
    )

    # Add knowledge only if the collection is empty
    if vector_store._collection.count() == 0:
        documents = load_python_knowledge()
        vector_store.add_documents(documents)

    _vector_store = vector_store

    return _vector_store


def search_knowledge(question: str, k: int = 3):
    """Retrieve relevant knowledge documents."""

    vector_store = create_vector_store()

    results = vector_store.similarity_search(
        question,
        k=k
    )

    return results
