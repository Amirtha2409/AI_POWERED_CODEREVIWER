import streamlit as st
from analyzer.analyzer import analyze_code
from analyzer.docstring_analyzer import analyze_code_quality

def show(code):

    st.title("Overview")

    if not code:
        st.info("Please upload or select a file to analyze.")
        return

    results = analyze_code(code)

    quality_data = analyze_code_quality(code)


    col1, col2, col3 = st.columns(3)

    col1.metric("Docstring Coverage %", f"{quality_data['doc_coverage']}%")
    col2.metric("Avg Function Complexity", quality_data["avg_complexity"])
    col3.metric("Maintainability Index", quality_data["maintainability_index"])

    st.progress(int(quality_data["doc_coverage"]))

    # Smart feedback
    if quality_data["maintainability_index"] > 80:
        st.success("Excellent maintainability.")
    elif quality_data["maintainability_index"] > 50:
        st.info("Moderate maintainability.")
    else:
        st.warning("Low maintainability. Refactor recommended.")
    
    # Add custom CSS once (top of file or before container)
    st.markdown("""
<style>
.glass-box {
    background: rgba(255,255,255,0.04);
    padding: 25px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

    # Create styled container properly
    with st.container():
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)

        st.subheader("📊 Code Quality Overview")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Lines of Code", results["lines_of_code"])
            st.metric("Functions", results["functions_count"])

        with col2:
            st.metric("Total Complexity", results["total_complexity"])
            st.metric("Maintainability Index", results["maintainability_index"])

        st.markdown('</div>', unsafe_allow_html=True)
       
        # download button
        import json

        report_data = json.dumps(quality_data, indent=4)

        st.download_button(
            label="📥 Download Docstring Coverage Report",
            data=report_data,
            file_name="docstring_coverage_report.json",
            mime="application/json"
        )