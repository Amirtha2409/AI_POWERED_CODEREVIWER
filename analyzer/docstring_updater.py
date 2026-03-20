import ast


def apply_docstring_to_function(code, function_name, new_docstring):
    """
    Insert AI generated docstring into a function.
    """

    lines = code.split("\n")
    tree = ast.parse(code)

    for node in ast.walk(tree):

        if isinstance(node, ast.FunctionDef) and node.name == function_name:

            insert_line = node.body[0].lineno - 1

            indent = " " * (node.col_offset + 4)

            formatted_doc = [
                indent + '"""',
                indent + new_docstring.strip(),
                indent + '"""'
            ]

            lines[insert_line:insert_line] = formatted_doc

            break

    return "\n".join(lines)