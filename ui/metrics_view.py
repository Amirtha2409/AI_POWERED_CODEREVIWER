import streamlit as st
import os
from analyzer.analyzer import analyze_code

def show(code=None, samples_path="samples"):
    # -----------------------------
    # 1. DIRECT METRICS SECTION
    # -----------------------------
    # This analyzes the code currently in your session state immediately.
    if not code or code.strip() == "":
        st.warning("⚠ No code found in session. Please go to the editor and enter some code first.")
    else:
        st.markdown("### 📋 Function Metrics")
        results = analyze_code(code)
        
        tab1, tab2 = st.tabs(["Table View", "JSON View"])

        with tab1:
            if "functions" in results and results["functions"]:
                # Displays the analysis results in a clean table
                st.dataframe(results["functions"], use_container_width=True)
            else:
                st.info("No specific functions detected for analysis in the current session.")

        with tab2:
            st.json(results)

    # -----------------------------
    # 2. COMPARISON SECTION
    # -----------------------------
    st.divider()
    st.markdown("## 🔍 Compare Saved Files")

    # Ensure the samples directory exists before trying to list files
    if not samples_path or not os.path.exists(samples_path):
        st.info(f"Directory '{samples_path}' not found. Create a folder named 'samples' and add .py files to compare.")
        return

    # Filter for Python files only
    sample_files = [f for f in os.listdir(samples_path) if f.endswith(".py")]

    if len(sample_files) < 2:
        st.warning("Comparison requires at least 2 files in the samples folder.")
        return

    # Selection UI for comparison
    col1, col2 = st.columns(2)
    with col1:
        file1 = st.selectbox("Select First File", sample_files, key="file_comp_1")
    with col2:
        file2 = st.selectbox("Select Second File", sample_files, key="file_comp_2")

    if st.button("⚡ Run Comparison", use_container_width=True):
        if file1 == file2:
            st.warning("Please select two different files to compare.")
        else:
            # Paths to the selected files
            path1 = os.path.join(samples_path, file1)
            path2 = os.path.join(samples_path, file2)

            # Analyze both files
            with open(path1, "r", encoding="utf-8") as f:
                res1 = analyze_code(f.read())
            with open(path2, "r", encoding="utf-8") as f:
                res2 = analyze_code(f.read())

            st.success("✅ Comparison Complete")

            # Side-by-Side Metric Display
            c1, c2 = st.columns(2)
            
            # Helper to display metrics for each file
            def display_file_metrics(column, res, filename, delta_res=None):
                with column:
                    st.subheader(f"📄 {filename}")
                    if delta_res:
                        st.metric("Lines of Code", res.get("lines_of_code", 0), 
                                  delta=int(res.get("lines_of_code", 0) - delta_res.get("lines_of_code", 0)))
                        st.metric("Complexity", res.get("total_complexity", 0),
                                  delta=int(res.get("total_complexity", 0) - delta_res.get("total_complexity", 0)))
                    else:
                        st.metric("Lines of Code", res.get("lines_of_code", 0))
                        st.metric("Complexity", res.get("total_complexity", 0))
                    st.metric("Functions Count", res.get("functions_count", 0))

            display_file_metrics(c1, res1, file1)
            display_file_metrics(c2, res2, file2, delta_res=res1)

            st.divider()
            st.info("💡 **Tip:** The green/red 'delta' values in the second column show the difference relative to the first file.")


