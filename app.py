import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

from utils.data_loader import load_dataset
from utils.charts import create_chart
from utils.report_generator import generate_pdf_report

from rag.vector_store import build_vector_db
from rag.retriever import retrieve_context

from agents.eda_agent import run_eda
from agents.kpi_agent import generate_kpis
from agents.insight_agent import generate_insight
from agents.sql_agent import generate_sql
from agents.forecast_agent import forecast_column

load_dotenv()

st.set_page_config(
    page_title="IntelliAnalyst AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ─── Reset & Base ─────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #060d1a;
    color: #dce8f8;
}

#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding: 0 2.5rem 5rem;
    max-width: 1600px;
}

/* ─── Sidebar ───────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: #07111f;
    border-right: 1px solid rgba(56, 100, 180, 0.18);
}

section[data-testid="stSidebar"] .stButton button {
    background: transparent !important;
    border: none !important;
    border-radius: 10px !important;
    color: #7e9cbf !important;
    font-size: 13.5px !important;
    font-weight: 500 !important;
    text-align: left !important;
    padding: 0.55rem 0.9rem !important;
    transition: all 0.18s ease !important;
    width: 100%;
}

section[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(59, 130, 246, 0.1) !important;
    color: #93c5fd !important;
}

/* Active sidebar item */
section[data-testid="stSidebar"] .active-nav button {
    background: rgba(59, 130, 246, 0.15) !important;
    color: #60a5fa !important;
    border-left: 2px solid #3b82f6 !important;
    font-weight: 700 !important;
}

/* ─── Hero Banner ───────────────────────────────────────── */
.hero-wrap {
    background: linear-gradient(135deg, #0d1f3c 0%, #091527 60%, #07111f 100%);
    border-bottom: 1px solid rgba(59, 130, 246, 0.2);
    padding: 2.6rem 3rem 2.2rem;
    margin: 0 -2.5rem 2.5rem;
    position: relative;
    overflow: hidden;
}

.hero-wrap::before {
    content: "";
    position: absolute;
    top: -80px; right: -80px;
    width: 420px; height: 420px;
    background: radial-gradient(circle, rgba(59,130,246,0.12) 0%, transparent 70%);
    pointer-events: none;
}

.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.16em;
    color: #3b82f6;
    text-transform: uppercase;
    margin-bottom: 0.7rem;
}

.hero-title {
    font-size: 42px;
    font-weight: 900;
    color: #f0f8ff;
    line-height: 1.15;
    margin-bottom: 0.8rem;
    letter-spacing: -0.02em;
}

.hero-title span {
    background: linear-gradient(90deg, #60a5fa, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-subtitle {
    font-size: 15.5px;
    color: #7e9cbf;
    max-width: 680px;
    line-height: 1.75;
    font-weight: 400;
}

.hero-pills {
    display: flex;
    gap: 0.6rem;
    flex-wrap: wrap;
    margin-top: 1.4rem;
}

.pill {
    background: rgba(59,130,246,0.1);
    border: 1px solid rgba(59,130,246,0.25);
    color: #93c5fd;
    font-size: 12px;
    font-weight: 600;
    padding: 0.28rem 0.75rem;
    border-radius: 999px;
    font-family: 'JetBrains Mono', monospace;
}

/* ─── Page Header ───────────────────────────────────────── */
.page-header {
    padding: 1.8rem 0 0.2rem;
    margin-bottom: 0.2rem;
    border-bottom: 1px solid rgba(56, 100, 180, 0.12);
}

.page-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10.5px;
    letter-spacing: 0.18em;
    color: #3b82f6;
    text-transform: uppercase;
    margin-bottom: 0.45rem;
}

.page-title {
    font-size: 28px;
    font-weight: 800;
    color: #f0f8ff;
    margin-bottom: 0.3rem;
    letter-spacing: -0.015em;
}

.page-subtitle {
    color: #7a93b0;
    font-size: 14.5px;
    line-height: 1.6;
    margin-bottom: 0;
}

/* ─── Stepper ───────────────────────────────────────────── */
.stepper-outer {
    display: flex;
    align-items: center;
    gap: 0;
    margin: 1.6rem 0 2rem;
    padding: 0.9rem 1.2rem;
    background: rgba(10,20,38,0.7);
    border: 1px solid rgba(56,100,180,0.14);
    border-radius: 16px;
    overflow-x: auto;
}

/* ─── Cards ─────────────────────────────────────────────── */
.card {
    background: rgba(10, 19, 35, 0.9);
    border: 1px solid rgba(56, 100, 180, 0.18);
    border-radius: 18px;
    padding: 1.6rem 1.7rem;
    margin-bottom: 1.2rem;
    transition: border-color 0.2s;
}

.card:hover {
    border-color: rgba(59, 130, 246, 0.35);
}

.card-icon {
    font-size: 28px;
    margin-bottom: 0.75rem;
}

.card-title {
    font-size: 15px;
    font-weight: 700;
    color: #e2edfc;
    margin-bottom: 0.5rem;
    letter-spacing: -0.01em;
}

.card-sub {
    font-size: 13.5px;
    color: #6b87a8;
    line-height: 1.65;
}

/* Feature cards on Home */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.1rem;
    margin: 1.8rem 0;
}

.feature-card {
    background: rgba(10, 19, 35, 0.9);
    border: 1px solid rgba(56, 100, 180, 0.18);
    border-radius: 18px;
    padding: 1.6rem;
    transition: all 0.2s;
}

.feature-card:hover {
    border-color: rgba(59, 130, 246, 0.38);
    background: rgba(15, 26, 48, 0.95);
    transform: translateY(-2px);
}

/* ─── Metric Cards ──────────────────────────────────────── */
.metric-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 1.8rem;
}

.metric-card {
    background: rgba(10, 19, 35, 0.92);
    border: 1px solid rgba(56, 100, 180, 0.2);
    border-radius: 16px;
    padding: 1.25rem 1.4rem;
    position: relative;
    overflow: hidden;
}

.metric-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #3b82f6, #38bdf8);
    opacity: 0.6;
}

.metric-label {
    color: #5a7898;
    font-size: 10.5px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-family: 'JetBrains Mono', monospace;
}

.metric-value {
    color: #f0f8ff;
    font-size: 32px;
    font-weight: 800;
    margin-top: 0.3rem;
    line-height: 1;
    letter-spacing: -0.02em;
}

/* ─── Buttons ───────────────────────────────────────────── */
.stButton button {
    border-radius: 11px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    border: 1px solid rgba(59, 130, 246, 0.4) !important;
    background: linear-gradient(135deg, #1d4ed8 0%, #0369a1 100%) !important;
    color: white !important;
    min-height: 44px !important;
    letter-spacing: 0.01em !important;
    transition: all 0.18s ease !important;
    box-shadow: 0 2px 12px rgba(29, 78, 216, 0.3) !important;
}

.stButton button:hover {
    box-shadow: 0 4px 20px rgba(29, 78, 216, 0.5) !important;
    transform: translateY(-1px) !important;
}

.stButton button:disabled {
    background: rgba(59, 130, 246, 0.18) !important;
    border-color: rgba(59, 130, 246, 0.35) !important;
    color: #60a5fa !important;
    cursor: default !important;
    transform: none !important;
    box-shadow: none !important;
}

.stDownloadButton button {
    border-radius: 11px !important;
    font-weight: 700 !important;
    border: 1px solid rgba(34, 197, 94, 0.4) !important;
    background: rgba(34, 197, 94, 0.12) !important;
    color: #4ade80 !important;
}

/* ─── Upload zone ───────────────────────────────────────── */
.stFileUploader {
    background: rgba(10, 19, 35, 0.8);
    border-radius: 14px;
    padding: 0.4rem;
}

[data-testid="stFileUploaderDropzone"] {
    background: rgba(10, 19, 35, 0.7) !important;
    border: 1.5px dashed rgba(59, 130, 246, 0.3) !important;
    border-radius: 12px !important;
}

/* ─── DataFrames ────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid rgba(56, 100, 180, 0.18) !important;
}

/* ─── Inputs ────────────────────────────────────────────── */
.stTextArea textarea, .stSelectbox select {
    background: rgba(10, 19, 35, 0.9) !important;
    border-color: rgba(56, 100, 180, 0.22) !important;
    color: #dce8f8 !important;
    border-radius: 12px !important;
}

/* ─── Alerts ────────────────────────────────────────────── */
.warning-box {
    background: rgba(245, 158, 11, 0.1);
    border: 1px solid rgba(245, 158, 11, 0.3);
    color: #fbbf24;
    padding: 1rem 1.2rem;
    border-radius: 14px;
    font-weight: 600;
    font-size: 14px;
}

.info-box {
    background: rgba(59, 130, 246, 0.08);
    border: 1px solid rgba(59, 130, 246, 0.22);
    color: #93c5fd;
    padding: 1rem 1.2rem;
    border-radius: 14px;
    font-size: 14px;
    line-height: 1.65;
}

.success-box {
    background: rgba(34, 197, 94, 0.08);
    border: 1px solid rgba(34, 197, 94, 0.25);
    color: #4ade80;
    padding: 0.8rem 1.1rem;
    border-radius: 12px;
    font-size: 13.5px;
    font-weight: 600;
}

/* ─── Section Dividers ──────────────────────────────────── */
.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #3b82f6;
    margin-bottom: 0.8rem;
}

.divider {
    height: 1px;
    background: rgba(56, 100, 180, 0.14);
    margin: 1.8rem 0;
}

/* ─── Expander ──────────────────────────────────────────── */
details {
    background: rgba(10, 19, 35, 0.8) !important;
    border: 1px solid rgba(56, 100, 180, 0.18) !important;
    border-radius: 14px !important;
    margin-bottom: 0.8rem !important;
}

/* ─── Code blocks ───────────────────────────────────────── */
code, pre {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important;
}

/* ─── Scrollbar ─────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #07111f; }
::-webkit-scrollbar-thumb { background: rgba(59,130,246,0.35); border-radius: 999px; }

/* ─── Workflow strip ────────────────────────────────────── */
.workflow-strip {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 0.5rem;
    background: rgba(10, 19, 35, 0.85);
    border: 1px solid rgba(56, 100, 180, 0.16);
    border-radius: 16px;
    padding: 0.85rem 1rem;
    margin: 1.4rem 0 2rem;
}

/* ─── Radio ─────────────────────────────────────────────── */
.stRadio label {
    color: #9db4d3 !important;
    font-size: 14px !important;
}

/* ─── Slider ────────────────────────────────────────────── */
.stSlider {
    padding: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)


# ─── Page Registry ───────────────────────────────────────────────────────────

PAGES = [
    ("Home",             "🏠"),
    ("Upload Data",      "📂"),
    ("Explore EDA",      "🔬"),
    ("KPI Board",        "📌"),
    ("Ask AI Analyst",   "🧠"),
    ("Chart Lab",        "📈"),
    ("Forecast & Report","⚡"),
]

PAGE_NAMES = [p[0] for p in PAGES]

# ─── Session State ────────────────────────────────────────────────────────────

for key, default in [
    ("page", "Home"),
    ("df", None),
    ("dataset_name", None),
    ("vector_collection", None),
    ("kb_file_names", []),
    ("report_bytes", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default


def go_to(page):
    st.session_state.page = page
    st.rerun()


# ─── Sidebar ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style="padding: 1.4rem 0.2rem 1.8rem;">
        <div style="font-size: 13px; font-family: 'JetBrains Mono', monospace;
                    letter-spacing: 0.15em; color: #3b82f6; text-transform: uppercase;
                    margin-bottom: 0.4rem;">Analytics Platform</div>
        <div style="font-size: 23px; font-weight: 900; color: #f0f8ff;
                    letter-spacing: -0.02em;">IntelliAnalyst</div>
        <div style="font-size: 12px; color: #4a6a8a; margin-top: 0.2rem;">
            Agentic AI · RAG · Multi-Agent
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="height:1px;background:rgba(56,100,180,0.14);margin-bottom:0.8rem;"></div>', unsafe_allow_html=True)

    for page_name, icon in PAGES:
        is_active = st.session_state.page == page_name
        label = f"{icon}  {page_name}"
        if is_active:
            st.markdown(f"""
            <div style="background:rgba(59,130,246,0.14); border-left:2px solid #3b82f6;
                        border-radius:10px; padding:0.55rem 0.9rem;
                        color:#60a5fa; font-size:13.5px; font-weight:700;
                        margin-bottom:2px; cursor:default;">{label}</div>
            """, unsafe_allow_html=True)
        else:
            if st.button(label, use_container_width=True, key=f"side_{page_name}"):
                go_to(page_name)

    st.markdown('<div style="height:1px;background:rgba(56,100,180,0.14);margin:1rem 0 0.9rem;"></div>', unsafe_allow_html=True)

    # Dataset status
    if st.session_state.df is not None:
        st.markdown(f"""
        <div class="success-box" style="margin-bottom:0.6rem;">
            ✓ &nbsp;{st.session_state.dataset_name}<br>
            <span style="font-weight:400;color:#86efac;font-size:12px;">
            {st.session_state.df.shape[0]:,} rows · {st.session_state.df.shape[1]} cols</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-box" style="margin-bottom:0.6rem;">No dataset loaded</div>', unsafe_allow_html=True)

    if st.session_state.vector_collection is not None:
        st.markdown(f"""
        <div class="success-box" style="margin-bottom:0.6rem;">
            ✓ &nbsp;KB: {len(st.session_state.kb_file_names)} file(s) indexed
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-box" style="margin-bottom:0.6rem;">No knowledge base</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:1px;background:rgba(56,100,180,0.14);margin:0.8rem 0;"></div>', unsafe_allow_html=True)

    if st.button("🗑  Clear Dataset", use_container_width=True, key="clear_ds"):
        st.session_state.df = None
        st.session_state.dataset_name = None
        st.session_state.report_bytes = None
        st.rerun()

    if st.button("🗑  Clear Knowledge Base", use_container_width=True, key="clear_kb"):
        st.session_state.vector_collection = None
        st.session_state.kb_file_names = []
        st.rerun()


# ─── Helpers ──────────────────────────────────────────────────────────────────

def render_page_header(eyebrow, title, subtitle):
    st.markdown(f"""
    <div class="page-header">
        <div class="page-eyebrow">{eyebrow}</div>
        <div class="page-title">{title}</div>
        <div class="page-subtitle">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)
    render_stepper()


def render_stepper():
    st.markdown('<div class="workflow-strip">', unsafe_allow_html=True)
    cols = st.columns(len(PAGES))
    for i, (page_name, icon) in enumerate(PAGES):
        with cols[i]:
            is_active = st.session_state.page == page_name
            label = f"{icon} {page_name}" if not is_active else f"● {page_name}"
            if is_active:
                st.button(label, key=f"step_{page_name}", disabled=True, use_container_width=True)
            else:
                if st.button(label, key=f"step_{page_name}", use_container_width=True):
                    go_to(page_name)
    st.markdown('</div>', unsafe_allow_html=True)


def no_data_warning():
    st.markdown("""
    <div class="warning-box">
        ⚠ &nbsp;No dataset loaded — head to <strong>Upload Data</strong> first.
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("→ Go to Upload Data", use_container_width=False):
        go_to("Upload Data")


def try_parse_dates(df):
    parsed = df.copy()
    for col in parsed.columns:
        if parsed[col].dtype == "object":
            sample = parsed[col].dropna().astype(str).head(25)
            if len(sample) == 0:
                continue
            date_like = sample.str.match(r"^\d{4}[-/]\d{1,2}[-/]\d{1,2}").sum()
            if date_like >= max(1, int(len(sample) * 0.7)):
                parsed[col] = pd.to_datetime(parsed[col], errors="coerce")
    return parsed


def get_column_groups(df):
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    datetime_cols = df.select_dtypes(include=["datetime64[ns]", "datetime64[ns, UTC]"]).columns.tolist()
    categorical_cols = [c for c in df.columns if c not in numeric_cols and c not in datetime_cols]
    return numeric_cols, categorical_cols, datetime_cols


# ─── Page: Home ──────────────────────────────────────────────────────────────

page = st.session_state.page

if page == "Home":
    st.markdown("""
    <div class="hero-wrap">
        <div class="hero-eyebrow">📊 Agentic AI · RAG-Powered · Multi-Agent Analytics</div>
        <div class="hero-title">Turn raw data into<br><span>executive-grade insight</span></div>
        <div class="hero-subtitle">
            Upload datasets and company knowledge, then let specialized AI agents perform
            EDA, generate KPIs, answer business questions, create visualizations,
            forecast trends, and produce boardroom-ready PDF reports — all from one workspace.
        </div>
        <div class="hero-pills">
            <span class="pill">EDA Agent</span>
            <span class="pill">KPI Agent</span>
            <span class="pill">Insight Agent</span>
            <span class="pill">SQL Agent</span>
            <span class="pill">Forecast Agent</span>
            <span class="pill">RAG · Vector DB</span>
            <span class="pill">PDF Reports</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    render_stepper()

    st.markdown("""
    <div class="feature-grid">
        <div class="feature-card">
            <div class="card-icon">🧠</div>
            <div class="card-title">Multi-Agent Intelligence</div>
            <div class="card-sub">Six specialized agents — EDA, KPI, Insight, SQL, Forecast, and Report — each focused on one analytical job and doing it well.</div>
        </div>
        <div class="feature-card">
            <div class="card-icon">📚</div>
            <div class="card-title">RAG Knowledge Base</div>
            <div class="card-sub">Ground AI answers in your company's SOPs, policy files, previous reports, and domain documents uploaded as PDF, TXT, or DOCX.</div>
        </div>
        <div class="feature-card">
            <div class="card-icon">📈</div>
            <div class="card-title">Visual Analytics Suite</div>
            <div class="card-sub">Bar, line, scatter, histogram, box plots — built interactively with Plotly on a dark canvas styled for presentations.</div>
        </div>
        <div class="feature-card">
            <div class="card-icon">🔬</div>
            <div class="card-title">Automated EDA</div>
            <div class="card-sub">Instant profiling: shape, dtypes, missing values, duplicates, and descriptive statistics across every column.</div>
        </div>
        <div class="feature-card">
            <div class="card-icon">⚡</div>
            <div class="card-title">Time-Series Forecasting</div>
            <div class="card-sub">Project numeric columns forward with configurable horizon. Results render as an interactive chart and downloadable table.</div>
        </div>
        <div class="feature-card">
            <div class="card-icon">📄</div>
            <div class="card-title">PDF Report Generation</div>
            <div class="card-sub">One click produces a styled, downloadable PDF covering the dataset overview, EDA, KPI summary, and key column insights.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)




# ─── Page: Upload Data ────────────────────────────────────────────────────────

elif page == "Upload Data":
    render_page_header(
        "Step 01 · Ingest",
        "Upload Data",
        "Load a CSV or Excel dataset, and optionally attach company knowledge files for RAG-enhanced AI answers."
    )

    left, right = st.columns(2, gap="large")

    with left:
        st.markdown('<div class="section-label">Dataset — CSV or XLSX</div>', unsafe_allow_html=True)

        dataset_file = st.file_uploader(
            "Drop file here or click to browse",
            type=["csv", "xlsx"],
            key="dataset_uploader",
            label_visibility="collapsed"
        )

        if dataset_file is not None:
            if st.session_state.dataset_name != dataset_file.name:
                try:
                    df = load_dataset(dataset_file)
                    df = try_parse_dates(df)
                    st.session_state.df = df
                    st.session_state.dataset_name = dataset_file.name
                    st.session_state.report_bytes = None
                    st.success(f"✓  Loaded **{df.shape[0]:,}** rows and **{df.shape[1]}** columns.")
                except Exception as e:
                    st.error(f"Dataset loading failed: {e}")

        if st.session_state.df is not None:
            st.markdown(f"""
            <div style="background:rgba(59,130,246,0.06);border:1px solid rgba(59,130,246,0.18);
                        border-radius:12px;padding:0.8rem 1rem;margin:0.6rem 0 1rem;
                        font-family:'JetBrains Mono',monospace;font-size:12px;color:#7ca8d5;">
                {st.session_state.dataset_name} &nbsp;·&nbsp;
                {st.session_state.df.shape[0]:,} rows &nbsp;·&nbsp;
                {st.session_state.df.shape[1]} columns
            </div>
            """, unsafe_allow_html=True)
            st.dataframe(st.session_state.df.head(8), use_container_width=True)

    with right:
        st.markdown('<div class="section-label">Knowledge Base — PDF / TXT / DOCX</div>', unsafe_allow_html=True)

        kb_files = st.file_uploader(
            "Drop knowledge files here",
            type=["pdf", "txt", "docx"],
            accept_multiple_files=True,
            key="kb_uploader",
            label_visibility="collapsed"
        )

        kb_names = [f.name for f in kb_files] if kb_files else []

        if kb_files and kb_names != st.session_state.kb_file_names:
            try:
                with st.spinner("Indexing knowledge base into vector store…"):
                    st.session_state.vector_collection = build_vector_db(kb_files)
                    st.session_state.kb_file_names = kb_names
                st.success(f"✓  Indexed {len(kb_files)} file(s) into the knowledge base.")
            except Exception as e:
                st.error(f"Knowledge base indexing failed: {e}")

        if st.session_state.kb_file_names:
            st.markdown('<div class="section-label" style="margin-top:1rem;">Indexed Files</div>', unsafe_allow_html=True)
            for name in st.session_state.kb_file_names:
                st.markdown(f"""
                <div style="background:rgba(34,197,94,0.07);border:1px solid rgba(34,197,94,0.2);
                            border-radius:9px;padding:0.45rem 0.9rem;margin-bottom:0.4rem;
                            font-family:'JetBrains Mono',monospace;font-size:12px;color:#86efac;">
                    ✓ &nbsp;{name}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="info-box">
                Optional: Upload business rules, SOPs, product catalogs, or past reports. The AI Analyst
                will pull context from these files when answering your questions.
            </div>
            """, unsafe_allow_html=True)




# ─── Page: Explore EDA ───────────────────────────────────────────────────────

elif page == "Explore EDA":
    render_page_header(
        "Step 02 · Profile",
        "EDA Studio",
        "Understand dataset shape, data quality, column types, missing values, duplicates, and statistics."
    )

    if st.session_state.df is None:
        no_data_warning()
    else:
        df = st.session_state.df
        eda = run_eda(df)

        st.markdown('<div class="metric-row">', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        metrics = [
            ("Total Rows",      f"{eda['rows']:,}"),
            ("Total Columns",   f"{eda['columns']:,}"),
            ("Missing Values",  f"{eda['missing_values']:,}"),
            ("Duplicate Rows",  f"{eda['duplicate_rows']:,}"),
        ]
        for col, (label, value) in zip([c1, c2, c3, c4], metrics):
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-label">Column Information</div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(eda["column_info"]), use_container_width=True)

        st.markdown('<div class="section-label" style="margin-top:1.4rem;">Statistical Summary</div>', unsafe_allow_html=True)
        st.dataframe(eda["summary"], use_container_width=True)




# ─── Page: KPI Board ─────────────────────────────────────────────────────────

elif page == "KPI Board":
    render_page_header(
        "Step 03 · Measure",
        "KPI Board",
        "Auto-generated performance indicators across all numeric columns in your dataset."
    )

    if st.session_state.df is None:
        no_data_warning()
    else:
        kpis = generate_kpis(st.session_state.df)

        if not kpis:
            st.markdown('<div class="warning-box">⚠ No numeric columns found for KPI generation.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="font-family:'JetBrains Mono',monospace;font-size:12px;color:#4a6a8a;margin-bottom:1rem;">
                {len(kpis)} KPI groups generated from numeric columns
            </div>
            """, unsafe_allow_html=True)

            for col, values in kpis.items():
                with st.expander(f"📌  {col}", expanded=False):
                    items = list(values.items())
                    k1, k2, k3, k4 = st.columns(4)
                    for i, (key, value) in enumerate(items[:4]):
                        with [k1, k2, k3, k4][i]:
                            st.metric(key, value)
                    if len(items) > 4:
                        st.json(dict(items[4:]))




# ─── Page: Ask AI Analyst ─────────────────────────────────────────────────────

elif page == "Ask AI Analyst":
    render_page_header(
        "Step 04 · Interrogate",
        "AI Analyst Workspace",
        "Ask business questions in plain English. Get narrative insights or production-ready SQL."
    )

    if st.session_state.df is None:
        no_data_warning()
    else:
        left, right = st.columns([2, 1], gap="large")

        with left:
            question = st.text_area(
                "Your question",
                placeholder="e.g. Which product generated the highest profit and why? What's driving the Q3 dip in revenue?",
                height=130,
                label_visibility="collapsed"
            )

            st.markdown('<div class="section-label">Agent Mode</div>', unsafe_allow_html=True)
            agent = st.radio(
                "Agent",
                ["Insight Agent", "SQL Agent"],
                horizontal=True,
                label_visibility="collapsed"
            )

            if st.button("Generate AI Answer →", use_container_width=True):
                if not question.strip():
                    st.warning("Please enter a question first.")
                else:
                    context = ""
                    if st.session_state.vector_collection is not None:
                        try:
                            context = retrieve_context(st.session_state.vector_collection, question)
                        except Exception as e:
                            st.warning(f"RAG retrieval skipped. {e}")

                    try:
                        with st.spinner("Agent is working…"):
                            if agent == "Insight Agent":
                                answer = generate_insight(st.session_state.df, question, context)
                                st.markdown('<div class="section-label" style="margin-top:1.2rem;">AI Insight</div>', unsafe_allow_html=True)
                                st.markdown(f"""
                                <div style="background:rgba(10,19,35,0.85);border:1px solid rgba(56,100,180,0.2);
                                            border-radius:16px;padding:1.4rem 1.6rem;line-height:1.8;
                                            color:#cddff0;font-size:14.5px;">
                                {answer}
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                sql = generate_sql(st.session_state.df, question)
                                st.markdown('<div class="section-label" style="margin-top:1.2rem;">Generated SQL</div>', unsafe_allow_html=True)
                                st.code(sql, language="sql")
                    except Exception as e:
                        st.error(f"AI generation failed: {e}")

        with right:
            st.markdown('<div class="section-label">Suggested Questions</div>', unsafe_allow_html=True)
            suggestions = [
                "Which region has the highest profit margin?",
                "Which product is underperforming vs target?",
                "What are the top 3 business recommendations?",
                "Generate SQL for top 5 products by revenue.",
                "What KPI should management focus on first?",
                "Is there a seasonal pattern in the data?",
            ]
            for s in suggestions:
                st.markdown(f"""
                <div style="background:rgba(10,19,35,0.75);border:1px solid rgba(56,100,180,0.16);
                            border-radius:10px;padding:0.55rem 0.9rem;margin-bottom:0.45rem;
                            font-size:13px;color:#7e9cbf;cursor:pointer;
                            transition:border-color 0.2s;"
                     title="Click the text area above and type this">
                    → {s}
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            if st.session_state.vector_collection is not None:
                st.markdown("""
                <div class="success-box">✓ &nbsp;RAG context active — answers grounded in your knowledge base.</div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="info-box">
                    💡 Upload a knowledge base on the <strong>Upload Data</strong> page for stronger,
                    context-aware business answers.
                </div>
                """, unsafe_allow_html=True)


# ─── Page: Chart Lab ─────────────────────────────────────────────────────────

elif page == "Chart Lab":
    render_page_header(
        "Step 05 · Visualize",
        "Chart Lab",
        "Build interactive charts from your dataset — bar, line, scatter, histogram, and box plot."
    )

    if st.session_state.df is None:
        no_data_warning()
    else:
        df = st.session_state.df
        numeric_cols, categorical_cols, datetime_cols = get_column_groups(df)
        all_cols = df.columns.tolist()

        left, right = st.columns([1, 2.6], gap="large")

        with left:
            st.markdown('<div class="section-label">Chart Configuration</div>', unsafe_allow_html=True)

            chart_type = st.selectbox(
                "Chart Type",
                ["Bar Chart", "Line Chart", "Scatter Plot", "Histogram", "Box Plot"]
            )

            if chart_type == "Histogram":
                x_col = st.selectbox("Column", numeric_cols if numeric_cols else all_cols)
                y_col = None
            elif chart_type == "Scatter Plot":
                x_col = st.selectbox("X Axis", numeric_cols if numeric_cols else all_cols)
                y_col = st.selectbox("Y Axis", numeric_cols if numeric_cols else all_cols)
            elif chart_type == "Line Chart":
                x_col = st.selectbox("X Axis", datetime_cols + categorical_cols + numeric_cols)
                y_col = st.selectbox("Y Axis", numeric_cols) if numeric_cols else None
            elif chart_type == "Box Plot":
                x_col = st.selectbox("Group Column", categorical_cols if categorical_cols else all_cols)
                y_col = st.selectbox("Numeric Column", numeric_cols) if numeric_cols else None
            else:
                x_col = st.selectbox("X Axis", categorical_cols + datetime_cols + numeric_cols)
                y_col = st.selectbox("Y Axis", numeric_cols) if numeric_cols else None

            generate_chart = st.button("Generate Chart →", use_container_width=True)

        with right:
            if generate_chart:
                if chart_type != "Histogram" and y_col is None:
                    st.error("This chart type requires a numeric Y column.")
                else:
                    try:
                        if chart_type == "Histogram":
                            import plotly.express as px
                            fig = px.histogram(df, x=x_col, title=f"Distribution of {x_col}")
                        else:
                            fig = create_chart(df, chart_type, x_col, y_col)

                        fig.update_layout(
                            paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(6,13,26,0.8)",
                            font_color="#dce8f8",
                            font_family="Inter",
                            margin=dict(l=20, r=20, t=52, b=24),
                            title_font_size=17,
                            title_font_color="#f0f8ff",
                        )
                        fig.update_xaxes(gridcolor="rgba(56,100,180,0.1)", zerolinecolor="rgba(56,100,180,0.2)")
                        fig.update_yaxes(gridcolor="rgba(56,100,180,0.1)", zerolinecolor="rgba(56,100,180,0.2)")
                        st.plotly_chart(fig, use_container_width=True)

                    except Exception as e:
                        st.error(f"Chart generation failed: {e}")
            else:
                st.markdown("""
                <div style="height:340px;display:flex;align-items:center;justify-content:center;
                            background:rgba(10,19,35,0.6);border:1px dashed rgba(56,100,180,0.2);
                            border-radius:16px;color:#3a5a7a;font-size:15px;text-align:center;">
                    <div>
                        <div style="font-size:36px;margin-bottom:0.7rem;">📈</div>
                        Configure your chart and click <strong style="color:#4a7abf;">Generate Chart</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)




# ─── Page: Forecast & Report ──────────────────────────────────────────────────

elif page == "Forecast & Report":
    render_page_header(
        "Step 06 · Deliver",
        "Forecast & Report",
        "Project numeric trends forward and generate a downloadable PDF report."
    )

    if st.session_state.df is None:
        no_data_warning()
    else:
        df = st.session_state.df
        numeric_cols = df.select_dtypes(include="number").columns.tolist()

        left, right = st.columns([3, 2], gap="large")

        with left:
            st.markdown('<div class="section-label">Time-Series Forecasting</div>', unsafe_allow_html=True)

            if numeric_cols:
                forecast_col_sel = st.selectbox("Target Column", numeric_cols)
                periods = st.slider("Forecast Horizon (periods)", 3, 30, 7)

                if st.button("Run Forecast →", use_container_width=True):
                    try:
                        with st.spinner("Generating forecast…"):
                            forecast_df, fig = forecast_column(df, forecast_col_sel, periods)

                        fig.update_layout(
                            paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(6,13,26,0.8)",
                            font_color="#dce8f8",
                            font_family="Inter",
                            margin=dict(l=20, r=20, t=52, b=24),
                        )
                        fig.update_xaxes(gridcolor="rgba(56,100,180,0.1)")
                        fig.update_yaxes(gridcolor="rgba(56,100,180,0.1)")
                        st.plotly_chart(fig, use_container_width=True)
                        st.markdown('<div class="section-label" style="margin-top:0.5rem;">Forecast Table</div>', unsafe_allow_html=True)
                        st.dataframe(forecast_df, use_container_width=True)

                    except Exception as e:
                        st.error(f"Forecast failed: {e}")
            else:
                st.markdown('<div class="warning-box">⚠ No numeric columns available for forecasting.</div>', unsafe_allow_html=True)

        with right:
            st.markdown('<div class="section-label">PDF Report</div>', unsafe_allow_html=True)
            st.markdown("""
            <div class="card">
                <div class="card-icon">📄</div>
                <div class="card-title">What's in the Report</div>
                <div class="card-sub">
                    Dataset overview and shape<br>
                    EDA summary (missing, duplicates, types)<br>
                    KPI tables for all numeric columns<br>
                    Column-level statistical insights<br>
                    Formatted and downloadable as PDF
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Generate PDF Report →", use_container_width=True):
                try:
                    with st.spinner("Building report…"):
                        eda = run_eda(df)
                        kpis = generate_kpis(df)
                        report_path = generate_pdf_report(eda, kpis)
                    with open(report_path, "rb") as file:
                        st.session_state.report_bytes = file.read()
                    st.success("✓ Report generated successfully.")
                except Exception as e:
                    st.error(f"Report generation failed: {e}")

            if st.session_state.report_bytes:
                st.download_button(
                    label="⬇  Download PDF Report",
                    data=st.session_state.report_bytes,
                    file_name="intellianalyst_report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )