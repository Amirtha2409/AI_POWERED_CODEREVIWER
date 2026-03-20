import streamlit as st


def save_version(code):

    if "doc_history" not in st.session_state:
        st.session_state.doc_history = []

    st.session_state.doc_history.append(code)


def show_history():

    if "doc_history" not in st.session_state:
        return

    if len(st.session_state.doc_history) == 0:
        return

    st.subheader("Docstring History")

    for i, version in enumerate(st.session_state.doc_history):

        if st.button(f"Restore Version {i+1}"):

            st.session_state.doc_code = version
            st.rerun()