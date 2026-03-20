import streamlit as st
import os
from pathlib import Path
from analyzer.docstring_module import extract_functions_and_classes
from analyzer.docstring_apply import apply_docstring
from analyzer.ai_docstring_generator import generate_ai_docstring

def show_docstring_module(code):
    st.title("🧠 AI Docstring Generator")

    # --- 1. CONFIGURATION (At the top) ---
    st.subheader("⚙️ Settings")
    c1, c2, c3 = st.columns(3)
    with c1:
        style = st.selectbox("Docstring Style", ["google", "numpy", "rst"])
    with c2:
        model = st.selectbox("AI Model", ["Groq (Llama 3.3)", "OpenAI (GPT-4o)"])
    with c3:
        tone = st.selectbox("Docstring Tone", ["Professional", "Short", "Detailed"])

    st.markdown("---")

    # --- 2. VS CODE SYNC (Sidebar) ---
    # This automatically finds your sample files so you don't overwrite app.py
    current_dir = Path.cwd()
    py_files = [str(p.relative_to(current_dir)) for p in current_dir.rglob("*.py") 
                if "venv" not in str(p) and "__pycache__" not in str(p)]
    
    st.sidebar.header("📁 VS Code Sync")
    # Try to default to 'sample_a.py' if it exists in the list
    default_index = py_files.index("sample_a.py") if "sample_a.py" in py_files else 0
    selected_file = st.sidebar.selectbox("Select file to update in VS Code:", py_files, index=default_index)
    target_file_path = current_dir / selected_file

    if not code:
        st.info("Please upload a file or select one to begin.")
        return

    # Use session state to track code changes so the preview stays updated
    if "doc_code" not in st.session_state:
        st.session_state.doc_code = code

    # --- 3. GENERATION LOOP ---
    items = extract_functions_and_classes(st.session_state.doc_code)
    
    for item in items:
        if item["has_docstring"]:
            continue

        st.markdown(f"### 🛠 {item['type']}: `{item['name']}`")
        col1, col2 = st.columns([4, 1])

        with col2:
            if st.button("✨ Generate", key=f"gen_{item['name']}"):
                with st.spinner(f"Generating {style} docstring..."):
                    doc = generate_ai_docstring(item["name"], item["params"], style=style, model_type=model, tone=tone)
                    st.session_state[f"temp_{item['name']}"] = doc

        if f"temp_{item['name']}" in st.session_state:
            generated_doc = st.session_state[f"temp_{item['name']}"]
            st.code(generated_doc, language="python")

            if st.button("✅ Accept & Apply to VS Code", key=f"apply_{item['name']}"):
                # Update memory
                new_code = apply_docstring(st.session_state.doc_code, item["lineno"], generated_doc)
                st.session_state.doc_code = new_code
                
                # Update the SPECIFIC file in VS Code
                with open(target_file_path, "w", encoding="utf-8") as f:
                    f.write(new_code)
                
                st.success(f"Updated {selected_file} in VS Code!")
                st.rerun()

    st.markdown("---")
    st.subheader("📝 Updated Code Preview")
    st.code(st.session_state.doc_code, language="python")