import ast


def extract_param_types(code):

    tree = ast.parse(code)

    param_types = {}

    for node in ast.walk(tree):

        if isinstance(node, ast.FunctionDef):

            types = {}

            for arg in node.args.args:

                if arg.annotation:
                    types[arg.arg] = ast.unparse(arg.annotation)
                else:
                    types[arg.arg] = "Any"

            param_types[node.name] = types

    return param_types