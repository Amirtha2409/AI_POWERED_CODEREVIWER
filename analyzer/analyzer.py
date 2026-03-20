import ast
from radon.complexity import cc_visit
from radon.metrics import mi_visit

def analyze_code(code):

    tree = ast.parse(code)

    functions = []
    total_lines = len(code.splitlines())

    complexity_results = cc_visit(code)
    complexity_dict = {c.name: c.complexity for c in complexity_results}

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append({
                "name": node.name,
                "start_line": node.lineno,
                "end_line": node.end_lineno,
                "complexity": complexity_dict.get(node.name, 0),
                "has_docstring": ast.get_docstring(node) is not None
            })

    total_complexity = sum(complexity_dict.values())
    maintainability = round(mi_visit(code, True), 2)

    return {
        "lines_of_code": total_lines,
        "functions_count": len(functions),
        "functions": functions,
        "total_complexity": total_complexity,
        "maintainability_index": maintainability
    }