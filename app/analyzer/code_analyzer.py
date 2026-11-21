import ast


def check_syntax(code: str):
    try:
        ast.parse(code)

        return {
            "valid": True,
            "message": "No syntax errors found."
        }

    except SyntaxError as error:
        return {
            "valid": False,
            "message": error.msg,
            "line": error.lineno
        }

def check_long_lines(code: str, max_length: int = 100):
    issues = []

    for line_number, line in enumerate(code.splitlines(), start=1):
        if len(line) > max_length:
            issues.append({
                "type": "long_line",
                "line": line_number,
                "message": f"Line exceeds {max_length} characters."
            })

    return issues

def check_unused_imports(code: str):
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return []

    imported_names = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_names.append((alias.asname or alias.name.split(".")[0], node.lineno))

        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                imported_names.append((alias.asname or alias.name, node.lineno))

    used_names = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            used_names.add(node.id)

    issues = []

    for name, line in imported_names:
        if name not in used_names:
            issues.append({
                "type": "unused_import",
                "line": line,
                "message": f"'{name}' is imported but never used."
            })

    return issues



def check_unused_variables(code: str):
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return []

    assigned = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    assigned[target.id] = node.lineno

    used = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            used.add(node.id)

    issues = []

    for name, line in assigned.items():
        if name not in used:
            issues.append({
                "type": "unused_variable",
                "line": line,
                "message": f"Variable '{name}' is assigned but never used."
            })

    return issues


def analyze_code(code: str):
    syntax_result = check_syntax(code)

    if not syntax_result["valid"]:
        return {
            "valid": False,
            "issues": [syntax_result]
        }

    issues = []
    issues.extend(check_long_lines(code))
    issues.extend(check_unused_imports(code))
    issues.extend(check_unused_variables(code))

    return {
        "valid": True,
        "total_issues": len(issues),
        "issues": issues
    }