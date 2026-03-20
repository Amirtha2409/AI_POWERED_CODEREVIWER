import streamlit as st
import ast
import matplotlib.pyplot as plt
import copy
from analyzer.docstring_checker import check_docstrings


# =====================================================
# 🔍 FUNCTION ANALYSIS
# =====================================================
def analyze_functions(code):

    tree = ast.parse(code)

    functions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):

            has_doc = ast.get_docstring(node) is not None

            functions.append({
                "name": node.name,
                "line": node.lineno,
                "doc": has_doc
            })

    return functions


# =====================================================
# 🤖 FIX SINGLE FUNCTION
# =====================================================
def fix_single_function(code, lineno):

    try:
        tree = ast.parse(code)
    except:
        return code

    lines = code.split("\n")

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.lineno == lineno:

            if ast.get_docstring(node):
                return code

            indent = len(lines[node.lineno - 1]) - \
                     len(lines[node.lineno - 1].lstrip())

            space = " " * (indent + 4)

            lines.insert(
                node.lineno,
                f'{space}"""AI generated docstring for {node.name}."""'
            )

            break

    return "\n".join(lines)

# =====================================================
# 🤖 FIX ALL
# =====================================================
def fix_all(code, functions):

    new_code = code

    offset = 0

    for f in functions:
        if not f["doc"]:
            new_code = fix_single_function(
                new_code,
                f["line"] + offset
            )
            offset += 1

    return new_code


# =====================================================
# 📊 BAR CHART
# =====================================================
def bar_chart(functions):

    names = [f["name"] for f in functions]
    values = [1 if f["doc"] else 0 for f in functions]

    fig, ax = plt.subplots(figsize=(10,4))

    ax.bar(names, values)

    ax.set_title("Function Docstring Validation")
    ax.set_ylabel("Documentation Status")
    ax.set_yticks([0,1])
    ax.set_yticklabels(["Missing","Present"])

    plt.xticks(rotation=30)
    st.pyplot(fig)
    plt.close(fig)


# =====================================================
# 🍩 DONUT CHART
# =====================================================
def donut_chart(functions):

    present = sum(f["doc"] for f in functions)
    missing = len(functions) - present

    fig, ax = plt.subplots()

    ax.pie(
        [present, missing],
        labels=["Documented","Missing"],
        autopct="%1.0f%%",
        wedgeprops=dict(width=0.4)
    )

    ax.set_title("Documentation Coverage")

    st.pyplot(fig)
    plt.close(fig)


# =====================================================
# 🚨 SEVERITY
# =====================================================
def severity_badge(missing_count):

    if missing_count >= 3:
        return "🔴 High Severity"
    elif missing_count == 2:
        return "🟠 Medium Severity"
    else:
        return "🟡 Low Severity"

# =====================================================
# ✅ MAIN VALIDATION UI
# =====================================================
def show_validation(code):

    st.title("✅ Validation Module")

    # ---------------------------
    # SESSION STATE
    # ---------------------------
    if "updated_code" not in st.session_state:
        st.session_state.updated_code = code

    working_code = st.session_state.updated_code

    functions = analyze_functions(working_code)

    # =====================================================
    # 📊 CHART SECTION
    # =====================================================
    
    col1, col2 = st.columns([2,1])

    with col1:
        bar_chart(functions)

    with col2:
        donut_chart(functions)

    # =====================================================
    # 🚨 PEP257 VALIDATIONS
    # =====================================================
    st.subheader("⚠ PEP-257 Violations")

    missing = [f for f in functions if not f["doc"]]

    if not missing:
        st.success("✅ NO PEP-257 Violations Remaining")
    else:

        for f in missing:

            c1, c2, c3 = st.columns([5,2,1])

            with c1:
                st.error(f"""
    🚨 **PEP-257 Violation Detected**

    Function: `{f['name']}`  
    Issue: Missing docstring  
    Impact: Reduces maintainability and readability  
    Recommendation: Add descriptive docstring explaining purpose, parameters, and return values.
    """)
                st.info(
                    f"""
    🤖 **AI Suggestion Preview**

    \"\"\"Describe what `{f['name']}` does,
    explain parameters and return values.\"\"\"
    """
                )
            with c2:
                st.markdown(severity_badge(len(missing)))

            with c3:
                if st.button(
                    "💡 Fix",
                    key=f"fix_{f['name']}"
                ):
                    st.session_state.updated_code = \
                        fix_single_function(
                            working_code,
                            f["line"]
                        )
                    st.rerun()

        # =================================================
        # 🤖 FIX ALL
        # =================================================
        if st.button("🤖 AI Fix All"):
            st.session_state.updated_code = \
                fix_all(working_code, functions)
            st.rerun()

    # =====================================================
    # 🔄 CODE COMPARISON
    # =====================================================
    st.subheader("🧾 Code Comparison")

    colA, colB = st.columns(2)

    with colA:
        st.markdown("### Original Code")
        st.code(code, language="python")

    with colB:
        st.markdown("### Updated Code")
        st.code(
            st.session_state.updated_code,
            language="python"
        )