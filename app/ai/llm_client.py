
import os

from dotenv import load_dotenv
from google import genai
from groq import Groq

load_dotenv()


def generate_with_gemini(prompt: str) -> str:
    """Generate a response using Gemini."""
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("Gemini API key is not configured.")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    return response.text


def generate_with_groq(prompt: str) -> str:
    """Generate a response using Groq."""
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("Groq API key is not configured.")

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content


def generate_ai_response(prompt: str) -> dict:
    """Try Gemini first, then fall back to Groq."""

    if os.getenv("GEMINI_API_KEY"):
        try:
            result = generate_with_gemini(prompt)

            return {
                "success": True,
                "provider": "Gemini",
                "response": result,
            }

        except Exception as error:
            print(f"Gemini failed: {type(error).__name__}")
    else:
        print("Gemini API key not configured. Skipping Gemini.")

    if os.getenv("GROQ_API_KEY"):
        try:
            result = generate_with_groq(prompt)

            return {
                "success": True,
                "provider": "Groq",
                "response": result,
            }

        except Exception as error:
            print(f"Groq failed: {type(error).__name__}")
    else:
        print("Groq API key not configured.")

    return {
        "success": False,
        "provider": None,
        "response": "Both AI providers failed. Please check API availability and configuration.",
    }
