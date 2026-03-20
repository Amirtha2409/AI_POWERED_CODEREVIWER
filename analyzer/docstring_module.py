import ast


def extract_functions_and_classes(code):
    """
    Extract functions and classes from Python code
    """

    tree = ast.parse(code)

    items = []

    for node in ast.walk(tree):

        if isinstance(node, ast.FunctionDef):

            params = [arg.arg for arg in node.args.args]

            items.append({
                "type": "function",
                "name": node.name,
                "params": params,
                "lineno": node.lineno,
                "has_docstring": ast.get_docstring(node) is not None
            })

        elif isinstance(node, ast.ClassDef):

            items.append({
                "type": "class",
                "name": node.name,
                "params": [],
                "lineno": node.lineno,
                "has_docstring": ast.get_docstring(node) is not None
            })

    return items