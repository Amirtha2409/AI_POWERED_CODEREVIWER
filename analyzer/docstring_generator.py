import ast


def extract_function_code(code, lineno):
    lines = code.split("\n")
    return lines[lineno - 1]


def generate_ai_docstring(name, params, style="google"):
    """
    Simulated AI docstring generator
    (Later we will connect LLM)
    """

    description = f"Performs the operation of {name.replace('_',' ')}."

    if style == "google":

        doc = f'"""{description}\n\n'

        if params:
            doc += "Args:\n"
            for p in params:
                doc += f"    {p} (type): description of {p}\n"

        doc += "\nReturns:\n"
        doc += "    result: output of the function\n"
        doc += '"""'

    elif style == "numpy":

        doc = f'"""{description}\n\nParameters\n----------\n'

        for p in params:
            doc += f"{p} : type\n    description of {p}\n"

        doc += "\nReturns\n-------\nresult\n    output of the function\n"
        doc += '"""'

    else:  # rst

        doc = f'"""{description}\n\n'

        for p in params:
            doc += f":param {p}: description of {p}\n"

        doc += ":return: output of the function\n"
        doc += '"""'

    return doc