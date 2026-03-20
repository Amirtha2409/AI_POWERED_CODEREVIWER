def apply_docstring(code, lineno, docstring):

    lines = code.split("\n")

    indent = len(lines[lineno-1]) - len(lines[lineno-1].lstrip())
    indent_space = " " * (indent + 4)

    doc_lines = [indent_space + line if line else "" for line in docstring.split("\n")]

    lines.insert(lineno, "\n".join(doc_lines))

    return "\n".join(lines)