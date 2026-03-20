import ast


def check_param_mismatch(code):

    tree = ast.parse(code)

    mismatches = []

    for node in ast.walk(tree):

        if isinstance(node, ast.FunctionDef):

            params = [a.arg for a in node.args.args]

            doc = ast.get_docstring(node)

            if not doc:
                continue

            missing = []

            for p in params:
                if p not in doc:
                    missing.append(p)

            if missing:
                mismatches.append({
                    "function": node.name,
                    "missing_params": missing
                })

    return mismatches