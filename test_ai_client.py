from app.ai.llm_client import generate_ai_response

prompt = """
You are an expert Python code reviewer.

Review this code:
def add(a, b):
    return a - b

Identify the bug and suggest the correction.
"""

result = generate_ai_response(prompt)

print("\nAI REVIEW RESULT")
print("----------------")
print("Success:", result["success"])
print("Provider:", result["provider"])
print("Response:", result["response"])