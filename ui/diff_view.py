import streamlit as st


def show_diff(original, updated):

    st.subheader("Code Comparison")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Original Code")
        st.code(original, language="python")

    with col2:
        st.markdown("### Updated Code")
        st.code(updated, language="python")