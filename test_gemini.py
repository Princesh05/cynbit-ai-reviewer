
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: Gemini API key not found in .env")
else:
    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents="Reply with: Gemini API connection successful."
        )

        print("SUCCESS: Gemini API is working!")
        print(response.text)

    except Exception as error:
        print("Gemini API test failed.")
        print(type(error).__name__)
        print(str(error)[:500])
