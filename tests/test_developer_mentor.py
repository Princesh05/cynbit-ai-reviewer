
from unittest.mock import patch

from app.ai.developer_mentor import mentor_developer


def test_mentor_developer():
    question = "Why am I getting a syntax error after defining a function?"

    with patch(
        "app.ai.developer_mentor.generate_ai_response"
    ) as mock_ai:

        mock_ai.return_value = {
            "success": True,
            "provider": "Gemini",
            "response": (
                "A syntax error occurs because the function "
                "definition is missing a colon."
            )
        }

        result = mentor_developer(question)

    assert result["success"] is True
    assert result["provider"] == "Gemini"
    assert "Python Syntax Errors" in result["retrieved_knowledge"]
    assert result["mentor_response"] != ""

    mock_ai.assert_called_once()


def test_mentor_empty_question():
    result = mentor_developer("")

    assert result["success"] is False
    assert "message" in result
