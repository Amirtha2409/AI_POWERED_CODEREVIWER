import ast

def extract_functions(code):

    tree = ast.parse(code)
    functions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):

            doc = ast.get_docstring(node)

            functions.append({
                "name": node.name,
                "docstring": "Yes" if doc else "No"
            })

    return functions