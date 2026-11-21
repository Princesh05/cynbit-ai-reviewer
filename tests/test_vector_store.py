
from app.ai.vector_store import search_knowledge


def test_search_python_syntax():
    results = search_knowledge(
        "Why am I getting a syntax error after defining a function?",
        k=2
    )

    assert len(results) > 0
    assert any(
        "SyntaxError" in document.page_content
        for document in results
    )

    print("\nRetrieved knowledge:")
    for document in results:
        print(document.metadata)
