import ast


def check_docstrings(code):
    """
    Check functions for missing docstrings.
    Returns list of violations and total functions.
    """

    violations = []
    total_functions = 0

    try:
        tree = ast.parse(code)

        for node in ast.walk(tree):

            if isinstance(node, ast.FunctionDef):

                total_functions += 1

                doc = ast.get_docstring(node)

                if not doc:
                    violations.append({
                        "function": node.name,
                        "issue": "Missing docstring"
                    })

        return violations, total_functions

    except Exception as e:
        return [], 0