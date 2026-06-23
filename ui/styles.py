"""
Global CSS injection for ISH Report Centre.
Enterprise ERP aesthetic: ISH navy, structured layout, no dashboard chrome.
"""

CSS = """
<style>
/* ── Import ───────────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Base ─────────────────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
}

/* Remove Streamlit default padding */
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
    max-width: 1200px;
}

/* ── Sidebar brand block ──────────────────────────────────────────────── */
.sidebar-brand {
    padding: 1.1rem 0.5rem 0.8rem;
    border-bottom: 2px solid #C9A84C;
    margin-bottom: 0.5rem;
}
.brand-ish {
    font-size: 1.6rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: #0D2137;
}
.brand-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: #0D2137;
    margin-left: 0.4rem;
}
.brand-sub {
    font-size: 0.72rem;
    color: #5A6A7A;
    margin-top: 0.15rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

/* ── Sidebar radio options ────────────────────────────────────────────── */
div[role="radiogroup"] > label {
    font-size: 0.82rem !important;
    padding: 0.25rem 0.4rem !important;
    border-radius: 4px;
    transition: background 0.15s;
}
div[role="radiogroup"] > label:hover {
    background: #EAF0F7;
}

/* ── Report header ────────────────────────────────────────────────────── */
.report-header {
    padding: 1rem 1.25rem 0.9rem;
    border-left: 4px solid #C9A84C;
    background: #F4F7FA;
    border-radius: 0 6px 6px 0;
    margin-bottom: 1.25rem;
}
.report-breadcrumb {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #5A6A7A;
    margin-bottom: 0.2rem;
}
.report-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: #0D2137;
    line-height: 1.2;
}
.report-desc {
    font-size: 0.82rem;
    color: #5A6A7A;
    margin-top: 0.3rem;
}

/* ── Summary metrics ─────────────────────────────────────────────────── */
div[data-testid="metric-container"] {
    background: #F4F7FA;
    border: 1px solid #D0DCE8;
    border-radius: 6px;
    padding: 0.6rem 0.8rem;
}
div[data-testid="metric-container"] label {
    font-size: 0.72rem !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #5A6A7A !important;
}
div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    font-size: 1.35rem !important;
    font-weight: 700;
    color: #0D2137 !important;
}
div[data-testid="metric-container"] div[data-testid="stMetricDelta"] {
    font-size: 0.78rem !important;
}

/* ── Filter pills ─────────────────────────────────────────────────────── */
.filter-pills-row {
    margin-top: 0.75rem;
    margin-bottom: 0.25rem;
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
}
.filter-pill {
    display: inline-block;
    background: #EAF0F7;
    border: 1px solid #B0BEC5;
    border-radius: 20px;
    padding: 0.2rem 0.75rem;
    font-size: 0.76rem;
    color: #0D2137;
}
.filter-pill b {
    color: #5A6A7A;
    font-weight: 500;
    margin-right: 0.2rem;
}

/* ── Section divider ─────────────────────────────────────────────────── */
hr.section-divider {
    border: none;
    border-top: 1px solid #D0DCE8;
    margin: 1rem 0;
}

/* ── Dataframe table ─────────────────────────────────────────────────── */
div[data-testid="stDataFrame"] {
    border: 1px solid #D0DCE8;
    border-radius: 6px;
    overflow: hidden;
}

/* ── Export bar ──────────────────────────────────────────────────────── */
.export-bar {
    margin-top: 0.5rem;
}
.export-label {
    font-size: 0.82rem;
    color: #5A6A7A;
    line-height: 2.4;
}

/* Download buttons */
div[data-testid="stDownloadButton"] button {
    background: #0D2137 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 5px !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    padding: 0.45rem 1rem !important;
    transition: background 0.2s;
}
div[data-testid="stDownloadButton"] button:hover {
    background: #1A3A5C !important;
}

/* ── Empty state ──────────────────────────────────────────────────────── */
.empty-state {
    text-align: center;
    padding: 3.5rem 2rem;
    background: #F4F7FA;
    border: 1px dashed #B0BEC5;
    border-radius: 8px;
    margin: 1rem 0;
}
.empty-icon {
    font-size: 2.5rem;
    color: #B0BEC5;
    margin-bottom: 0.75rem;
}
.empty-title {
    font-size: 1rem;
    font-weight: 600;
    color: #0D2137;
}
.empty-sub {
    font-size: 0.82rem;
    color: #5A6A7A;
    margin-top: 0.3rem;
}

/* ── Welcome panel ────────────────────────────────────────────────────── */
.welcome-panel {
    text-align: center;
    padding: 4rem 2rem 3rem;
}
.welcome-logo {
    font-size: 3.5rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    color: #0D2137;
    border-bottom: 3px solid #C9A84C;
    display: inline-block;
    padding-bottom: 0.2rem;
    margin-bottom: 0.75rem;
}
.welcome-title {
    font-size: 1.4rem;
    font-weight: 600;
    color: #0D2137;
    margin-bottom: 0.5rem;
}
.welcome-sub {
    font-size: 0.9rem;
    color: #5A6A7A;
    line-height: 1.7;
    margin-bottom: 2rem;
}
.welcome-groups {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.75rem 1.5rem;
}
.welcome-group {
    font-size: 0.82rem;
    color: #0D2137;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}
.wg-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    background: #C9A84C;
    border-radius: 50%;
}

/* ── Sidebar labels ───────────────────────────────────────────────────── */
.stSidebar label {
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    color: #0D2137 !important;
}
.stSidebar .stMultiSelect > div {
    font-size: 0.82rem;
}

/* ── General heading ─────────────────────────────────────────────────── */
h5 {
    color: #0D2137 !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.02em;
}
</style>
"""


def inject_styles():
    import streamlit as st
    st.markdown(CSS, unsafe_allow_html=True)
