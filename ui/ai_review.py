import streamlit as st
from llm_groq import llm_review

def show(code):
    st.markdown("## 🤖 AI Code Review")

    if not code:
        st.info("Please upload or select a file to analyze.")
        return

    with st.container():
        st.markdown(
            """
            <div style="
                background: rgba(255,255,255,0.04);
                padding: 20px;
                border-radius: 15px;
                border: 1px solid rgba(255,255,255,0.08);
                margin-bottom: 20px;">
            """,
            unsafe_allow_html=True
        )

        with st.spinner("Analyzing with AI..."):
            review = llm_review(code)

        st.success("AI Review Completed!")

        st.markdown(
            f"""
            <div style="
                background: rgba(0,0,0,0.4);
                padding: 15px;
                border-radius: 10px;
                font-size: 15px;
                line-height: 1.6;">
                {review}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.download_button(
            "📥 Download Report",
            review,
            file_name="ai_review.txt",
            use_container_width=True
        )

        st.markdown("</div>", unsafe_allow_html=True)
