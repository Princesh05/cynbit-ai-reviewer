
from app.ai.code_reviewer import review_code


sample_code = """
import os

def calculate_discount(price, discount):
    final_price = price - discount
    return final_price

print(calculate_discount(100, 10))
"""

result = review_code(sample_code)

print("\n========== CYNBIT AI CODE REVIEW ==========")

print("\nSuccess:", result["success"])
print("AI Provider:", result.get("provider"))

print("\nStatic Analysis:")
print(result["static_analysis"])

print("\nAI Code Review:")
print(result["ai_review"])
