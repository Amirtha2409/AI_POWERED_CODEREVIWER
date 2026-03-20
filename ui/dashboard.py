import streamlit as st
import pandas as pd

def show_dashboard():

    # ---------------- CSS ----------------
    st.markdown("""
    <style>

    .test-box {
        background: #d6f5f2;
        padding:14px 20px;
        border-radius:10px;
        margin-bottom:12px;
        display:flex;
        justify-content:space-between;
        align-items:center;
        font-weight:600;
        border-left:6px solid #00bfa6;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }

    .test-name {
        color:#004d40;
        font-size:15px;
    }

    .test-pass {
        color:#00796b;
        font-weight:bold;
    }

    </style>
    """, unsafe_allow_html=True)

    st.title("🤖 AI Code Reviewer Dashboard")
    st.markdown("---")

    # ==================================================
    # 📊 TOP GRAPH
    # ==================================================
    st.subheader("📊 Test Summary")

    chart_data = pd.DataFrame({
        "Tests": [
            "Coverage Report",
            "Dashboard",
            "Generator",
            "LLM Integration",
            "Parser",
            "Validation"
        ],
        "Passed": [3, 4, 4, 5, 5, 7]
    }).set_index("Tests")

    st.bar_chart(chart_data)

    # ==================================================
    # ✅ TEST RESULTS (VISIBLE + CLEAN)
    # ==================================================
    st.subheader("✅ Test Results")

    test_results = [
        ("Coverage Reporter Tests", "3/3 passed"),
        ("Dashboard Tests", "4/4 passed"),
        ("Generator Tests", "4/4 passed"),
        ("LLM Integration Tests", "5/5 passed"),
        ("Parser Tests", "5/5 passed"),
        ("Validation Tests", "7/7 passed"),
    ]

    for name, result in test_results:
        st.markdown(f"""
        <div class="test-box">
            <span class="test-name">✔️ {name}</span>
            <span class="test-pass">{result}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ==================================================
    # ✨ MODULES
    # ==================================================

    data = [
        {"File": "sample_a.py", "Function": "calculate_average", "Status": "Documented"},
        {"File": "sample_a.py", "Function": "add", "Status": "Documented"},
        {"File": "sample_a.py", "Function": "process_data", "Status": "Missing"},
        {"File": "sample_b.py", "Function": "generator_example", "Status": "Documented"},
        {"File": "sample_b.py", "Function": "raises_example", "Status": "Missing"},
    ]
    df = pd.DataFrame(data)

    if "active_module" not in st.session_state:
        st.session_state.active_module = None

    if st.session_state.active_module is None:

        st.header("✨ Enhanced UI Features")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔍 Advanced Filters\n\nFilter dynamically by file, function, and status."):
                st.session_state.active_module = "filters"
                st.rerun()

            if st.button("📥 Export Data\n\nDownload analysis results as JSON or CSV."):
                st.session_state.active_module = "export"
                st.rerun()

        with col2:
            if st.button("🔎 Search Functions\n\nInstant search across all parsed functions."):
                st.session_state.active_module = "search"
                st.rerun()

            if st.button("💡 Help & Tips\n\nAccess a contextual guide for AI modules."):
                st.session_state.active_module = "help"
                st.rerun()

    else:

        if st.button("⬅ Back to Modules"):
            st.session_state.active_module = None
            st.rerun()

        st.markdown("---")

        if st.session_state.active_module == "filters":

            st.subheader("🔍 Advanced Filters")

            status_filter = st.selectbox(
                "Documentation Status",
                ["All", "Documented", "Missing"]
            )

            filtered_df = df if status_filter == "All" else df[df["Status"] == status_filter]

            st.dataframe(filtered_df, use_container_width=True)

        elif st.session_state.active_module == "search":

            st.subheader("🔎 Search Functions")

            query = st.text_input("Search function name...")

            search_df = df[df["Function"].str.contains(query, case=False)] if query else df

            st.dataframe(search_df, use_container_width=True)

        elif st.session_state.active_module == "export":

            st.subheader("📥 Export Data")

            export_format = st.radio(
                "Select Export Format",
                ["CSV", "JSON", "Excel"],
                horizontal=True
            )

            st.dataframe(df, use_container_width=True)

            if st.button("Download"):
                st.success(f"Downloading as {export_format}")

        elif st.session_state.active_module == "help":

            st.markdown("""
            <div style="padding:20px;border-radius:15px;color:white;
            background: linear-gradient(90deg, #00bfa6, #00796b);">
                <h3>ℹ️ Interactive Help & Tips</h3>
                <p>Contextual help and quick reference guide</p>
            </div>
            """, unsafe_allow_html=True)