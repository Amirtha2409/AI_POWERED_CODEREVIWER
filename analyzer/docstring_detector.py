import ast


# =====================================
# Extract all functions and classes
# =====================================
def extract_functions(code):
    """
    Extract all functions and classes from the file.
    """

    functions = []

    try:
        tree = ast.parse(code)
    except Exception:
        return functions

    for node in ast.walk(tree):

        if isinstance(node, ast.FunctionDef):

            functions.append({
                "name": node.name,
                "type": "function",
                "lineno": node.lineno,
                "docstring": ast.get_docstring(node)
            })

        elif isinstance(node, ast.ClassDef):

            functions.append({
                "name": node.name,
                "type": "class",
                "lineno": node.lineno,
                "docstring": ast.get_docstring(node)
            })

    return functions


# =====================================
# Detect missing docstrings
# =====================================
def detect_missing_docstrings(code):
    """
    Find functions/classes without docstrings.
    """

    results = []

    try:
        tree = ast.parse(code)
    except Exception:
        return results

    for node in ast.walk(tree):

        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):

            doc = ast.get_docstring(node)

            if not doc:

                results.append({
                    "name": node.name,
                    "type": "function" if isinstance(node, ast.FunctionDef) else "class",
                    "issue": "Missing Docstring",
                    "lineno": node.lineno
                })

    return results


# =====================================
# Detect incomplete docstrings
# =====================================
def detect_incomplete_docstrings(code):
    """
    Detect docstrings that exist but are too short.
    """

    issues = []

    try:
        tree = ast.parse(code)
    except Exception:
        return issues

    for node in ast.walk(tree):

        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):

            doc = ast.get_docstring(node)

            if doc:

                # Simple heuristic for incomplete docstring
                if len(doc.split()) < 5:

                    issues.append({
                        "name": node.name,
                        "type": "function" if isinstance(node, ast.FunctionDef) else "class",
                        "issue": "Incomplete Docstring",
                        "lineno": node.lineno
                    })

    return issues


# =====================================
# Detect private vs public
# =====================================
def is_private_function(name):
    """
    Detect private functions based on naming convention.
    """

    return name.startswith("_")


# =====================================
# Smart docstring analysis
# =====================================
def analyze_docstrings(code):
    """
    Combine all docstring checks.
    """

    results = []

    missing = detect_missing_docstrings(code)
    incomplete = detect_incomplete_docstrings(code)

    results.extend(missing)
    results.extend(incomplete)

    return results