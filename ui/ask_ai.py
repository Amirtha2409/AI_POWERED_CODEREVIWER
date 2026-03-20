import streamlit as st


def ask_ai(code, func_name):

    st.subheader(f"Ask AI About {func_name}")

    question = st.text_input("Ask anything about this function")

    if st.button("Ask AI"):

        prompt = f"""
Function Code:

{code}

User Question:
{question}
"""

        # send to LLM

        response = "AI explanation here"

        st.info(response)