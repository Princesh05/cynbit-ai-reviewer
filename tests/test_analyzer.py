from app.analyzer.code_analyzer import check_syntax
from app.analyzer.code_analyzer import check_long_lines
from app.analyzer.code_analyzer import check_unused_imports
from app.analyzer.code_analyzer import check_unused_variables
from app.analyzer.code_analyzer import analyze_code

def test_valid_python_code():
    code = "print('Hello Cynbit')"

    result = check_syntax(code)

    assert result["valid"] is True


def test_invalid_python_code():
    code = "print('Hello Cynbit'"

    result = check_syntax(code)

    assert result["valid"] is False

def test_long_line_detection():
    code = "x = '" + ("a" * 110) + "'"

    result = check_long_lines(code)

    assert len(result) == 1
    assert result[0]["type"] == "long_line"
    assert result[0]["line"] == 1


def test_unused_import_detection():
    code = """
import os
import math

print(math.sqrt(16))
"""

    result = check_unused_imports(code)

    assert len(result) == 1
    assert result[0]["type"] == "unused_import"
    assert "'os'" in result[0]["message"]


def test_unused_variable_detection():
    code = """
price = 100
tax = 10
discount = 5

print(price + tax)
"""

    result = check_unused_variables(code)

    assert len(result) == 1
    assert result[0]["type"] == "unused_variable"
    assert "discount" in result[0]["message"]


def test_complete_code_analysis():
    code = """
import os

price = 100
discount = 10

print(price)
"""

    result = analyze_code(code)

    assert result["valid"] is True
    assert result["total_issues"] == 2