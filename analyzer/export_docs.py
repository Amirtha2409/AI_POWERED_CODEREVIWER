import ast
import streamlit as st


def export_markdown(code):

    tree = ast.parse(code)

    md = "# Project Documentation\n\n"

    for node in ast.walk(tree):

        if isinstance(node, ast.FunctionDef):

            doc = ast.get_docstring(node)

            md += f"## {node.name}\n\n"

            if doc:
                md += doc + "\n\n"

    return md

if st.button("Export Documentation"):

    md = export_markdown(st.session_state.doc_code)

    st.download_button(
        "Download Markdown",
        md,
        file_name="documentation.md"
    )