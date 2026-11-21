
from langchain_core.documents import Document


def load_python_knowledge():
    """Load Python programming knowledge for the developer mentor."""

    documents = [
        Document(
            page_content="""
            Python SyntaxError:
            A SyntaxError occurs when Python code violates Python's grammar rules.
            For example, forgetting a colon after a function definition causes
            a SyntaxError.

            Incorrect:
            def add(a, b)
                return a + b

            Correct:
            def add(a, b):
                return a + b

            Always check colons, brackets, indentation and quotation marks.
            """,
            metadata={"topic": "Python Syntax Errors"}
        ),

        Document(
            page_content="""
            Python Unused Imports:
            An unused import occurs when a module or function is imported
            but never used in the program.

            Example:
            import os

            def add(a, b):
                return a + b

            Here, os is imported but never used.
            Removing unused imports improves code readability.
            """,
            metadata={"topic": "Unused Imports"}
        ),

        Document(
            page_content="""
            Python Functions:
            Functions are reusable blocks of code that perform specific tasks.
            Use meaningful function names, parameters and return statements.

            Example:
            def calculate_total(price, quantity):
                return price * quantity

            Good functions should have a clear responsibility.
            Avoid unnecessarily long functions.
            """,
            metadata={"topic": "Python Functions"}
        ),

        Document(
            page_content="""
            Python Type Hints:
            Type hints describe the expected types of function arguments
            and return values. They improve readability and help developers
            understand how functions should be used.

            Example:
            def add(a: int, b: int) -> int:
                return a + b

            Type hints do not automatically enforce types at runtime.
            """,
            metadata={"topic": "Python Type Hints"}
        ),

        Document(
            page_content="""
            Python Exception Handling:
            Exceptions are runtime errors that can interrupt program execution.
            Use try and except blocks to handle expected errors.

            Example:
            try:
                result = 10 / 0
            except ZeroDivisionError:
                print("Cannot divide by zero")

            Catch specific exceptions instead of using a broad except clause
            whenever possible.
            """,
            metadata={"topic": "Exception Handling"}
        ),

        Document(
            page_content="""
            Python Code Quality:
            Write readable and maintainable code using meaningful variable names,
            consistent indentation, small functions and appropriate comments.
            Avoid duplicate code and unnecessary complexity.
            Follow established Python conventions such as PEP 8.
            """,
            metadata={"topic": "Code Quality"}
        )
    ]

    return documents
