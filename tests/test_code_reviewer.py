
from unittest.mock import patch

from app.ai.code_reviewer import review_code


def test_review_valid_code():
    code = """
def add(a, b):
    return a + b
"""

    with patch(
        "app.ai.code_reviewer.generate_ai_response"
    ) as mock_ai:
        mock_ai.return_value = {
            "success": True,
            "provider": "Groq",
            "response": "The code looks good."
        }

        result = review_code(code)

    assert result["success"] is True
    assert result["provider"] == "Groq"
    assert result["static_analysis"]["valid"] is True


def test_review_empty_code():
    result = review_code("")

    assert result["success"] is False
    assert "message" in result


def test_review_ai_failure():
    code = """
def add(a, b):
    return a + b
"""

    with patch(
        "app.ai.code_reviewer.generate_ai_response"
    ) as mock_ai:
        mock_ai.return_value = {
            "success": False,
            "provider": None,
            "response": "Both AI providers failed."
        }

        result = review_code(code)

    assert result["success"] is False
    assert result["provider"] is None


def test_review_invalid_python():
    code = """
def add(a, b)
    return a + b
"""

    with patch("app.ai.code_reviewer.generate_ai_response") as mock_ai:
        result = review_code(code)

    assert result["success"] is False
    assert result["static_analysis"]["valid"] is False
    assert result["provider"] is None
    assert "syntax errors" in result["ai_review"]

    # Confirm that Gemini/Groq was not called
    mock_ai.assert_not_called()