"""
UI Components — reusable Streamlit rendering blocks.
Keep all st.* calls here; app.py orchestrates, components render.
"""

import io
import pandas as pd
import streamlit as st
from config.report_registry import REPORTS, GROUP_ORDER


# ── Sidebar ──────────────────────────────────────────────────────────────────

def render_sidebar() -> str | None:
    """
    Renders the report catalogue in the sidebar grouped by domain.
    Returns the selected report_key, or None if nothing selected.
    """
    st.sidebar.markdown(
        """
        <div class="sidebar-brand">
            <span class="brand-ish">ISH</span>
            <span class="brand-title">Information Systems</span>
            <div class="brand-sub">Admissions Report Centre</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.markdown("---")
    st.sidebar.markdown("##### Select Report")

    # Build radio options grouped by domain
    report_options = {"— Choose a report —": None}
    for group in GROUP_ORDER:
        reports_in_group = {
            k: v for k, v in REPORTS.items() if v["group"] == group
        }
        if reports_in_group:
            for key, meta in reports_in_group.items():
                display = f"{meta['label']}"
                report_options[f"[{group}]  {display}"] = key

    choice = st.sidebar.radio(
        "Reports",
        options=list(report_options.keys()),
        label_visibility="collapsed",
    )
    st.sidebar.markdown("---")

    selected_key = report_options.get(choice)
    return selected_key


# ── Report header ─────────────────────────────────────────────────────────────

def render_report_header(meta: dict):
    group = meta["group"]
    label = meta["label"]
    desc = meta.get("description", "")

    st.markdown(
        f"""
        <div class="report-header">
            <div class="report-breadcrumb">{group}</div>
            <div class="report-title">{label}</div>
            <div class="report-desc">{desc}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── Summary bar ───────────────────────────────────────────────────────────────

def render_summary_bar(df_full: pd.DataFrame, df_filtered: pd.DataFrame, active_filters: dict, meta: dict):
    total = len(df_full)
    showing = len(df_filtered)
    is_filtered = len(active_filters) > 0

    # KPI metrics
    kpi_cols = [c for c in meta.get("numeric_cols", []) if c in df_filtered.columns and c != "%"]

    cols = st.columns([1, 1, 1] + [1] * min(len(kpi_cols), 3))

    with cols[0]:
        st.metric("Total Records", f"{total:,}")
    with cols[1]:
        delta = f"{showing - total:,}" if is_filtered else None
        st.metric("Showing", f"{showing:,}", delta=delta)
    with cols[2]:
        st.metric("Filters Active", len(active_filters) if is_filtered else "None")

    for i, col in enumerate(kpi_cols[:3], start=3):
        with cols[i]:
            val = df_filtered[col].sum()
            st.metric(col, f"{int(val):,}" if val == int(val) else f"{val:,.1f}")

    # Active filter pills
    if active_filters:
        pills_html = "".join(
            f'<span class="filter-pill"><b>{k}:</b> '
            + (", ".join(str(x) for x in v) if isinstance(v, list) else str(v))
            + "</span>"
            for k, v in active_filters.items()
        )
        st.markdown(
            f'<div class="filter-pills-row">{pills_html}</div>',
            unsafe_allow_html=True,
        )


# ── Data table ────────────────────────────────────────────────────────────────

def render_data_table(df: pd.DataFrame, meta: dict):
    if df.empty:
        st.markdown(
            """
            <div class="empty-state">
                <div class="empty-icon">⊘</div>
                <div class="empty-title">No records match the current filters.</div>
                <div class="empty-sub">Adjust or clear filters in the sidebar to broaden results.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # Drop internal helper cols
    display_cols = [c for c in df.columns if not c.startswith("_") and c not in ("SNAP Test 1", "SNAP Test 2", "SNAP Test 3")]
    display_df = df[display_cols].copy()

    # Format date columns for display
    for col in meta.get("date_cols", []):
        if col in display_df.columns and pd.api.types.is_datetime64_any_dtype(display_df[col]):
            display_df[col] = display_df[col].dt.strftime("%d %b %Y")

    # Format % column
    if "%" in display_df.columns:
        display_df["%"] = display_df["%"].apply(
            lambda x: f"{x:.2f}%" if pd.notna(x) else "—"
        )

    # Format Conversion % if computed
    if "Conversion %" in display_df.columns:
        display_df["Conversion %"] = display_df["Conversion %"].apply(
            lambda x: f"{x:.2f}%" if pd.notna(x) else "—"
        )

    # Replace NaN with em-dash for display
    display_df = display_df.fillna("—")

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=min(40 + len(display_df) * 35, 600),
    )


# ── Export panel ──────────────────────────────────────────────────────────────

def render_export_panel(df: pd.DataFrame, report_label: str, active_filters: dict):
    from exports.excel_exporter import export_to_excel

    if df.empty:
        return

    # Drop internal cols for export
    export_df = df[[c for c in df.columns if not c.startswith("_") and c not in ("SNAP Test 1", "SNAP Test 2", "SNAP Test 3")]]

    st.markdown('<div class="export-bar">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2, 1, 1])

    with c1:
        st.markdown(
            f'<span class="export-label">Export {len(export_df):,} records</span>',
            unsafe_allow_html=True,
        )

    with c2:
        excel_bytes = export_to_excel(export_df, report_label, active_filters)
        safe_name = report_label.lower().replace(" ", "_").replace("/", "_")
        st.download_button(
            label="⬇ Download Excel",
            data=excel_bytes,
            file_name=f"ISH_{safe_name}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            key="dl_excel",
        )

    with c3:
        csv_bytes = export_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇ Download CSV",
            data=csv_bytes,
            file_name=f"ISH_{safe_name}.csv",
            mime="text/csv",
            use_container_width=True,
            key="dl_csv",
        )

    st.markdown("</div>", unsafe_allow_html=True)


# ── Landing / welcome screen ──────────────────────────────────────────────────

def render_welcome():
    st.markdown(
        """
        <div class="welcome-panel">
            <div class="welcome-logo">ISH</div>
            <div class="welcome-title">Admissions Report Centre</div>
            <div class="welcome-sub">
                Select a report from the sidebar to get started.<br>
                Apply filters, preview results, and export to Excel or CSV.
            </div>
            <div class="welcome-groups">
                <div class="welcome-group"><span class="wg-dot"></span>Funnel Reports</div>
                <div class="welcome-group"><span class="wg-dot"></span>Geography Reports</div>
                <div class="welcome-group"><span class="wg-dot"></span>Demographics</div>
                <div class="welcome-group"><span class="wg-dot"></span>Payments</div>
                <div class="welcome-group"><span class="wg-dot"></span>NRI / International</div>
                <div class="welcome-group"><span class="wg-dot"></span>Student Detail</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── Dividers ─────────────────────────────────────────────────────────────────

def section_divider():
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
