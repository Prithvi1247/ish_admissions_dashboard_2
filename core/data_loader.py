"""
Data Loader — cached CSV ingestion with all portal-specific parsing rules.
Each file's quirks (header offsets, total rows, trailing cols, date formats)
are handled here, driven by report_registry metadata.
"""

import pandas as pd
import streamlit as st
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
DATE_FORMAT = "%b-%d-%Y"  # e.g. May-06-2026


@st.cache_data(show_spinner=False)
def load_report(report_key: str, meta: dict) -> pd.DataFrame:
    filepath = DATA_DIR / meta["file"]
    if not filepath.exists():
        return pd.DataFrame()

    # Read raw, skipping portal title + blank line
    df = pd.read_csv(
        filepath,
        header=meta["header_row"],
        dtype=str,
        skip_blank_lines=False,
    )

    # Drop trailing empty column (unnamed artifacts from portal export)
    df = _drop_trailing_empty(df, meta.get("trailing_empty_col", False))

    # Strip whitespace from all string cells
    df = df.apply(lambda col: col.str.strip() if col.dtype == object else col)

    # Drop Total footer rows (S.No blank / "Total" in dimension col)
    if meta.get("drop_total"):
        sno_col = df.columns[0]
        df = df[df[sno_col].notna() & (df[sno_col].astype(str).str.strip() != "")]
        # Also drop rows where the dimension column value is "Total"
        dim = meta.get("dimension_col")
        if dim and dim in df.columns:
            df = df[df[dim].str.lower() != "total"]

    # Coerce numeric columns
    for col in meta.get("numeric_cols", []):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Parse date columns (Mon-DD-YYYY → datetime)
    for col in meta.get("date_cols", []):
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], format=DATE_FORMAT, errors="coerce")

    # Post-parse hooks
    hook = meta.get("post_parse")
    if hook == "strip_state_asterisk":
        df = _strip_state_asterisk(df, meta["dimension_col"])
    elif hook == "extract_state_from_city":
        df = _extract_state_from_city(df, meta["dimension_col"])
    elif hook == "parse_snap_tests":
        df = _parse_snap_tests(df)

    # Compute derived columns (e.g. Conversion %)
    for col_name, (numerator, denominator) in meta.get("computed_cols", {}).items():
        if numerator in df.columns and denominator in df.columns:
            df[col_name] = df.apply(
                lambda r: round(r[numerator] / r[denominator] * 100, 2)
                if pd.notna(r[denominator]) and r[denominator] != 0
                else None,
                axis=1,
            )

    # Reset index cleanly
    df = df.reset_index(drop=True)

    return df


# ── Post-parse hooks ─────────────────────────────────────────────────────────

def _drop_trailing_empty(df: pd.DataFrame, should_drop: bool) -> pd.DataFrame:
    if not should_drop:
        return df
    # Drop columns that are entirely unnamed/empty
    cols_to_keep = [
        c for c in df.columns
        if not (str(c).startswith("Unnamed") and df[c].isna().all())
    ]
    return df[cols_to_keep]


def _strip_state_asterisk(df: pd.DataFrame, col: str) -> pd.DataFrame:
    if col in df.columns:
        df[col] = df[col].str.replace(r"\s*\*+\s*$", "", regex=True).str.strip()
    return df


def _extract_state_from_city(df: pd.DataFrame, city_col: str) -> pd.DataFrame:
    """
    TestDateWiseCityReport: 'City - State' → split into City and State.
    Keeps original City Name column intact for display, adds State filter column.
    """
    if city_col not in df.columns:
        return df
    split = df[city_col].str.rsplit(" - ", n=1, expand=True)
    df["_City"] = split[0].str.strip() if 0 in split.columns else df[city_col]
    df["State"] = split[1].str.strip() if 1 in split.columns else None
    return df


def _parse_snap_tests(df: pd.DataFrame) -> pd.DataFrame:
    """
    PaidStudentswithTestWiseCityDetails:
    'Test' column is pipe-delimited list of test names.
    Expand into boolean flags for filter use.
    """
    if "Test" not in df.columns:
        return df
    df["SNAP Test 1"] = df["Test"].str.contains("SNAP Test 1", na=False)
    df["SNAP Test 2"] = df["Test"].str.contains("SNAP Test 2", na=False)
    df["SNAP Test 3"] = df["Test"].str.contains("SNAP Test 3", na=False)
    return df


def get_filter_options(df: pd.DataFrame, col: str) -> list:
    """Return sorted unique non-null values for a filter column."""
    if col not in df.columns:
        return []
    return sorted(df[col].dropna().astype(str).unique().tolist())
