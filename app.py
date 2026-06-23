"""
ISH Information Systems — Admissions Report Centre
Entry point. Orchestrates sidebar → load → filter → display → export.
"""

import streamlit as st

# ── Page config (must be first st call) ─────────────────────────────────────
st.set_page_config(
    page_title="ISH Report Centre",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

from config.report_registry import REPORTS
from core.data_loader import load_report
from core.filter_engine import render_filters
from ui.styles import inject_styles
from ui.components import (
    render_sidebar,
    render_report_header,
    render_summary_bar,
    render_data_table,
    render_export_panel,
    render_welcome,
    section_divider,
)

# ── Inject global styles ─────────────────────────────────────────────────────
inject_styles()

# ── Sidebar: report selection ─────────────────────────────────────────────────
selected_key = render_sidebar()

# ── Main area ─────────────────────────────────────────────────────────────────
if not selected_key:
    render_welcome()
    st.stop()

meta = REPORTS[selected_key]

# ── Load data ─────────────────────────────────────────────────────────────────
with st.spinner("Loading report data…"):
    df = load_report(selected_key, meta)

if df.empty:
    render_report_header(meta)
    st.error(
        f"⚠ Data file not found: `data/{meta['file']}`  \n"
        "Place the CSV exports from the admissions portal into the `data/` folder and reload."
    )
    st.stop()

# ── Sidebar: filters (rendered after data is loaded) ─────────────────────────
st.sidebar.markdown("##### Filters")
df_filtered, active_filters = render_filters(df, meta, selected_key)

# Clear filters button
if active_filters:
    if st.sidebar.button("✕ Clear All Filters", use_container_width=True):
        st.rerun()

# ── Main: report header ───────────────────────────────────────────────────────
render_report_header(meta)

# ── Main: summary bar ─────────────────────────────────────────────────────────
render_summary_bar(df, df_filtered, active_filters, meta)

section_divider()

# ── Main: export panel ────────────────────────────────────────────────────────
render_export_panel(df_filtered, meta["label"], active_filters)

section_divider()

# ── Main: data table ──────────────────────────────────────────────────────────
render_data_table(df_filtered, meta)
