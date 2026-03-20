import ast

def check_docstrings(code):

    tree = ast.parse(code)

    violations = []
    total = 0

    for node in ast.walk(tree):

        if isinstance(node, ast.FunctionDef):

            total += 1

            doc = ast.get_docstring(node)

            if not doc:
                violations.append({
                    "function": node.name,
                    "issue": "Missing docstring"
                })

    return violations, total