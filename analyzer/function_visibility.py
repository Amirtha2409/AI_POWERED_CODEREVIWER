import ast


def detect_visibility(code):

    tree = ast.parse(code)

    visibility = []

    for node in ast.walk(tree):

        if isinstance(node, ast.FunctionDef):

            if node.name.startswith("_"):
                v = "Private"
            else:
                v = "Public"

            visibility.append({
                "function": node.name,
                "visibility": v
            })

    return visibility