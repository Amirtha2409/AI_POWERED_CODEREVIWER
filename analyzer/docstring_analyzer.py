# analyzer/docstring_analyzer.py

import ast


def analyze_code_quality(code: str):
    """
    Analyze python code quality based on:
    - PEP257 docstring coverage
    - Function complexity
    - Maintainability index
    """

    try:
        tree = ast.parse(code)
    except Exception:
        return {
            "doc_coverage": 0,
            "avg_complexity": 0,
            "maintainability_index": 0
        }

    total_functions = 0
    documented_functions = 0
    complexities = []

    # -----------------------------------
    # Traverse AST
    # -----------------------------------
    for node in ast.walk(tree):

        if isinstance(node, ast.FunctionDef):
            total_functions += 1

            # Check docstring
            if ast.get_docstring(node):
                documented_functions += 1

            # Simple complexity calculation
            complexity = 1

            for child in ast.walk(node):
                if isinstance(
                    child,
                    (
                        ast.If,
                        ast.For,
                        ast.While,
                        ast.Try,
                        ast.With,
                        ast.BoolOp,
                    ),
                ):
                    complexity += 1

            complexities.append(complexity)

    # -----------------------------------
    # Docstring Coverage
    # -----------------------------------
    if total_functions == 0:
        doc_coverage = 100
    else:
        doc_coverage = int(
            (documented_functions / total_functions) * 100
        )

    # -----------------------------------
    # Average Complexity
    # -----------------------------------
    avg_complexity = (
        sum(complexities) / len(complexities)
        if complexities
        else 0
    )

    # -----------------------------------
    # Maintainability Index (Simple Model)
    # -----------------------------------
    maintainability_index = max(
        0,
        int(100 - (avg_complexity * 5) - (100 - doc_coverage) * 0.5),
    )

    return {
        "doc_coverage": doc_coverage,
        "avg_complexity": round(avg_complexity, 2),
        "maintainability_index": maintainability_index,
    }