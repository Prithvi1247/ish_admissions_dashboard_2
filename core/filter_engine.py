"""
Filter Engine — renders dynamic sidebar filter widgets and applies them to data.
All filter logic is driven by report_registry metadata; no report-specific code here.
"""

import pandas as pd
import streamlit as st
from datetime import datetime
from core.data_loader import get_filter_options


def render_filters(df: pd.DataFrame, meta: dict, report_key: str) -> tuple[pd.DataFrame, dict]:
    """
    Render all applicable filter widgets in the sidebar.
    Returns (filtered_df, active_filters_dict).
    """
    active_filters = {}
    filtered = df.copy()

    # ── Text search (for student-detail reports) ─────────────────────────
    text_search_cols = meta.get("text_search_cols", [])
    if text_search_cols:
        search_val = st.sidebar.text_input(
            "Search",
            placeholder=f"Search by {', '.join(text_search_cols)}…",
            key=f"{report_key}_search",
        )
        if search_val:
            mask = pd.Series([False] * len(filtered), index=filtered.index)
            for col in text_search_cols:
                if col in filtered.columns:
                    mask |= filtered[col].astype(str).str.contains(search_val, case=False, na=False)
            filtered = filtered[mask]
            active_filters["Search"] = search_val

    # ── Multiselect filters ───────────────────────────────────────────────
    for col in meta.get("multiselect_cols", []):
        if col not in filtered.columns:
            continue
        options = get_filter_options(df, col)  # always use unfiltered options
        if not options:
            continue
        label = _humanise(col)
        selected = st.sidebar.multiselect(
            label,
            options=options,
            default=[],
            key=f"{report_key}_{col}_ms",
        )
        if selected:
            filtered = filtered[filtered[col].astype(str).isin(selected)]
            active_filters[label] = selected

    # ── Extra filter columns (e.g. State extracted from City) ────────────
    for col in meta.get("extra_filter_cols", []):
        if col not in filtered.columns:
            continue
        options = get_filter_options(df, col)
        if not options:
            continue
        label = _humanise(col)
        selected = st.sidebar.multiselect(
            label,
            options=options,
            default=[],
            key=f"{report_key}_{col}_extra",
        )
        if selected:
            filtered = filtered[filtered[col].astype(str).isin(selected)]
            active_filters[label] = selected

    # ── Date range filters ────────────────────────────────────────────────
    for col in meta.get("date_cols", []):
        if col not in filtered.columns:
            continue
        valid_dates = filtered[col].dropna()
        if valid_dates.empty:
            continue
        min_d, max_d = valid_dates.min().date(), valid_dates.max().date()
        st.sidebar.markdown(f"**{_humanise(col)} Range**")
        col1, col2 = st.sidebar.columns(2)
        from_d = col1.date_input("From", value=min_d, min_value=min_d, max_value=max_d,
                                 key=f"{report_key}_{col}_from")
        to_d = col2.date_input("To", value=max_d, min_value=min_d, max_value=max_d,
                               key=f"{report_key}_{col}_to")
        if from_d != min_d or to_d != max_d:
            filtered = filtered[
                filtered[col].dt.date.between(from_d, to_d)
            ]
            active_filters[f"{_humanise(col)} Range"] = f"{from_d} → {to_d}"

    # ── Numeric range filters (registered / paid applicants) ─────────────
    numeric_filter_candidates = [
        c for c in meta.get("numeric_cols", [])
        if c in ("Registered Applicants", "Paid Applicants")
    ]
    for col in numeric_filter_candidates:
        if col not in filtered.columns:
            continue
        col_vals = df[col].dropna()
        if col_vals.empty:
            continue
        min_v, max_v = int(col_vals.min()), int(col_vals.max())
        if min_v == max_v:
            continue
        label = f"Min {col}"
        val = st.sidebar.number_input(
            label,
            min_value=min_v,
            max_value=max_v,
            value=min_v,
            step=1,
            key=f"{report_key}_{col}_min",
        )
        if val > min_v:
            filtered = filtered[filtered[col] >= val]
            active_filters[label] = val

    # ── SNAP Test slot filter (student detail only) ───────────────────────
    if "SNAP Test 1" in df.columns:
        st.sidebar.markdown("**SNAP Test Slots**")
        selected_slots = []
        for slot in ["SNAP Test 1", "SNAP Test 2", "SNAP Test 3"]:
            if st.sidebar.checkbox(slot, value=False, key=f"{report_key}_{slot}_chk"):
                selected_slots.append(slot)
        if selected_slots:
            mask = pd.Series([False] * len(filtered), index=filtered.index)
            for slot in selected_slots:
                if slot in filtered.columns:
                    mask |= filtered[slot]
            filtered = filtered[mask]
            active_filters["SNAP Test Slots"] = selected_slots

    return filtered, active_filters


def _humanise(col: str) -> str:
    """Convert raw column name to display-friendly label."""
    mapping = {
        "Institute": "Programme",
        "StateWise": "State",
        "CityWise": "City",
        "CategoryWise": "Reservation Category",
        "GenderWise": "Gender",
        "EducationTypeWise": "Education Stream",
        "ExperienceWise": "Work Experience",
        "Paymentmodewise": "Payment Mode",
        "Programs": "Programme",
        "NRI_candidate": "NRI Candidate",
        "Admission_under_NRI": "Admission Under NRI",
        "Test City 1": "Test City 1",
        "Test City 2": "Test City 2",
        "Test City 3": "Test City 3",
        "State": "State",
    }
    return mapping.get(col, col.replace("_", " ").title())
