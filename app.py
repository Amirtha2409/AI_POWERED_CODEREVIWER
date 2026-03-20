from matplotlib import style
import streamlit as st
import os
from ui.dashboard import show_dashboard
from ui.docstring_view import show_docstring_module
from ui.validation_view import show_validation
from ui.ask_ai import ask_ai
# ===============================
# SESSION STATE INITIALIZATION
# ===============================
if "code" not in st.session_state:
    st.session_state.code = ""

if "scan_clicked" not in st.session_state:
    st.session_state.scan_clicked = False

if "selected_file" not in st.session_state:
    st.session_state.selected_file = None

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

st.set_page_config(page_title="AI Code Reviewer", layout="wide")

# =========================
# 🎨 PREMIUM THEME
# =========================
st.markdown("""
<style>

/* ===== PREMIUM FONT ===== */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

html, body, [class*="css"]  {
    font-family: 'Poppins', sans-serif;
}

/* ===== MAIN BACKGROUND ===== */
.stApp {
    background: linear-gradient(135deg, #0b1120, #111827, #0f172a);
    color: #ffffff !important;
}

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] {
    background: #0f172a;
}

[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

/* Fix white uploader text */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] p {
    color: #ffffff !important;
}

/* ===== HEADER TEXT FIX ===== */
h1, h2, h3, h4, h5 {
    color: #ffffff !important;
    font-weight: 600;
}

/* ===== METRIC FIX ===== */
[data-testid="metric-container"] {
    background: rgba(255, 255, 255, 0.06);
    backdrop-filter: blur(15px);
    border-radius: 18px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.15);
}

[data-testid="metric-container"] label {
    color: #cbd5e1 !important;
    font-size: 14px;
}

[data-testid="metric-container"] div {
    color: #ffffff !important;
    font-size: 28px;
    font-weight: 700;
}

/* ===== GLASS CARDS ===== */
.glass-card {
    background: rgba(255, 255, 255, 0.07);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    padding: 25px;
    border: 1px solid rgba(255,255,255,0.2);
    box-shadow: 0 10px 40px rgba(0,0,0,0.5);
    color: white;
    margin-bottom: 20px;
}

/* ===== BUTTON ===== */
.stButton>button {
    background: linear-gradient(90deg, #6366f1, #a855f7);
    color: white;
    border-radius: 14px;
    font-weight: 600;
    border: none;
    padding: 8px 18px;
}

.stButton>button:hover {
    background: linear-gradient(90deg, #7c3aed, #c026d3);
}

/* ===== TABS PREMIUM ===== */
button[data-baseweb="tab"] {
    color: #cbd5e1 !important;
    font-weight: 500;
    font-size: 16px;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #ffffff !important;
    border-bottom: 3px solid #a855f7 !important;
}

/* ===== DATAFRAME FIX ===== */
[data-testid="stDataFrame"] {
    background-color: rgba(255,255,255,0.05);
    color: white !important;
    border-radius: 15px;
}


            /* ===== JSON WHITE FIX ===== */
[data-testid="stJson"] > div {
    background: rgba(255, 255, 255, 0.05) !important;
}

/* ===== SUCCESS MESSAGE FIX ===== */
[data-testid="stAlert"] {
    background: rgba(34,197,94,0.15);
    color: #22c55e !important;
    border-radius: 15px;
}

/* ===== GENERAL TEXT ===== */
p, span, div {
    color: #e2e8f0;
}

/* ===== SELECTBOX FIX ===== */
div[data-baseweb="select"] > div {
    background: rgba(255, 255, 255, 0.08) !important;
    color: white !important;
    border-radius: 15px !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
}

div[data-baseweb="select"] span {
    color: white !important;
}

/* ===== FILE UPLOADER FIX ===== */
[data-testid="stFileUploader"] {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 15px;
    border: 1px solid rgba(255,255,255,0.2);
    padding: 15px;
}

[data-testid="stFileUploader"] section {
    background: transparent !important;
}

[data-testid="stFileUploader"] button {
    background: linear-gradient(90deg, #6366f1, #a855f7);
    color: white;
    border-radius: 10px;
    border: none;
}

/* ===== INPUT BOX FIX ===== */
input, textarea {
    background: rgba(255, 255, 255, 0.08) !important;
    color: white !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
}
/* ===== MAIN CONTENT CONTAINER FIX ===== */
.main .block-container {
    background: rgba(255, 255, 255, 0.06);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    padding: 30px;
    border: 1px solid rgba(255,255,255,0.15);
}
/* ===== GLASS PASTEL GREEN DROPDOWN BAR ===== */
div[data-baseweb="select"] > div {
    background: rgba(209, 250, 229, 0.35) !important;  /* transparent pastel green */
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border-radius: 20px !important;
    border: 1px solid rgba(167, 243, 208, 0.6) !important;
    box-shadow: 0 8px 25px rgba(16, 185, 129, 0.18) !important;
    transition: all 0.3s ease !important;
}

/* Text inside dropdown */
div[data-baseweb="select"] span {
    color: #064e3b !important;
    font-weight: 500 !important;
}

/* Dropdown arrow */
div[data-baseweb="select"] svg {
    color: #059669 !important;
}

/* Hover effect */
div[data-baseweb="select"] > div:hover {
    background: rgba(209, 250, 229, 0.55) !important;
    box-shadow: 0 10px 30px rgba(16, 185, 129, 0.25) !important;
}

/* Focus glow */
div[data-baseweb="select"]:focus-within > div {
    box-shadow: 0 0 0 2px #6ee7b7 !important;
}

/* ===================================================== */
/* 🌑 DEEP MIDNIGHT GLASS DROPDOWN THEME */
/* ===================================================== */

/* ===== CLOSED DROPDOWN BAR ===== */
div[data-baseweb="select"] > div {
    background: rgba(30, 41, 59, 0.7) !important;  /* Deep slate glass to match background */
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important; /* Subtle border */
    box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.05) !important;
    transition: all 0.3s ease !important;
}

/* Text inside closed dropdown */
div[data-baseweb="select"] span {
    color: #e2e8f0 !important;   /* Clean off-white */
    font-weight: 400 !important;
}

/* Arrow icon */
div[data-baseweb="select"] svg {
    color: #94a3b8 !important;   /* Muted slate blue */
}

/* Hover effect */
div[data-baseweb="select"] > div:hover {
    background: rgba(51, 65, 85, 0.8) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
}

/* Focus glow */
div[data-baseweb="select"]:focus-within > div {
    border: 1px solid #6366f1 !important; /* Indigo focus line */
    box-shadow: 0 0 0 1px #6366f1 !important;
}


/* ===== OPENED DROPDOWN PANEL ===== */

div[data-baseweb="popover"] {
    background: transparent !important;
}

/* Inner panel */
div[data-baseweb="popover"] div {
    background: rgba(15, 23, 42, 0.95) !important;  /* Darker midnight for contrast */
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
}

/* Option rows */
div[role="option"] {
    background: transparent !important;
    color: #cbd5e1 !important;
    margin: 4px 8px !important;
    border-radius: 8px !important;
    transition: background 0.2s ease !important;
}

/* Hover / Selection effect */
div[role="option"]:hover {
    background: rgba(99, 102, 241, 0.2) !important; /* Soft indigo hover */
    color: #ffffff !important;
}

/* Currently selected option in the list */
div[aria-selected="true"] {
    background: rgba(99, 102, 241, 0.4) !important;
    color: #ffffff !important;
}
""", unsafe_allow_html=True)

# =========================
# 🏷 THEMED TITLE BAR
# =========================
st.markdown("""
<div style="
    background: linear-gradient(90deg, #1e293b, #4338ca);
    padding: 20px;
    border-radius: 14px;
    text-align: center;
    font-size: 28px;
    font-weight: 700;
    color: #f8fafc;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    margin-bottom: 30px;
    letter-spacing: 1px;">
    <span style="margin-right: 10px;">🤖</span> AI Code Reviewer
</div>
""", unsafe_allow_html=True)

# =========================
# 📂 SIDEBAR
# =========================
import streamlit as st
import os

# ---- Import UI Pages ----
from ui.overview import show as show_overview
from ui.validation_view import show_validation
import ui.ai_review
import ui.metrics_view

# ===============================
#st SIDEBAR
# ===============================
st.sidebar.title("🤖 AI Code Reviewer")

# -------- PAGE DROPDOWN ----------
page = st.sidebar.selectbox(
    "📂 Select Module",
    [
        "Overview",
        "Metrics",
        "AI Review",
        "Validation",
        "Docstring",
        "Dashboard"
    ]
)

st.sidebar.divider()

# ===============================
# FILE SECTION
# ===============================
st.sidebar.subheader("📁 Uploaded Files")
uploaded_file = st.sidebar.file_uploader("Upload Python File",type=["py"])
sample_folder = "samples"
sample_files = []
if os.path.exists(sample_folder):
    sample_files = os.listdir(sample_folder)
selected_sample = st.sidebar.selectbox("Select Sample File",["None"] + sample_files) 
# ===============================
# LOAD CODE
# ===============================

code=None
# --- Upload File ---
# Check if the list is not empty before accessing index 0
if uploaded_file:  
    # Notice the 's' in uploaded_files to match your new sidebar variable
    code = uploaded_file.read().decode("utf-8")
    st.session_state.code = code
    st.sidebar.success(f"Loaded: {uploaded_file.name}")

# --- Sample File ---
elif selected_sample!= "None":

    sample_path = os.path.join(sample_folder, selected_sample)

    with open(sample_path, "r", encoding="utf-8") as f:
        st.session_state.code = f.read()

    st.session_state.selected_file = selected_sample
    st.sidebar.success(f"Loaded Sample: {selected_sample}")

# ===============================
# PAGE ROUTING
# ===============================
if page == "Overview":
    show_overview(st.session_state.code)

elif page == "Metrics":
    ui.metrics_view.show(
        code=st.session_state.get('code', ""),
        samples_path="samples"  
    )
elif page == "AI Review":
    ui.ai_review.show(st.session_state.code)
    

elif page == "Validation":
   show_validation(st.session_state.code)

elif page == "Docstring":
    show_docstring_module(st.session_state.code)

elif page == "Dashboard":
   show_dashboard()