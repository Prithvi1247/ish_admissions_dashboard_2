# ISH Information Systems — Admissions Report Centre

Internal enterprise report builder for the admissions management team.

## Setup

```bash
pip install -r requirements.txt
```

## Data


```
data/
  admission_nri.csv
  category_wise.csv
  city_wise_data.csv
  course_wise_data.csv
  course_wise_paid.csv
  course_wise_registration.csv
  education_type_data.csv
  experience_wise_data.csv
  gender_data.csv
  nri_data.csv
  paid_wise_data.csv
  PaidStudentswithTestWiseCityDetails.csv
  payment_mode_data.csv
  PaymentModeWiseReport.csv
  registration_by_date_data.csv
  state_wise_data.csv
  TestDateWiseCityReport.csv
```

## Run

```bash
streamlit run app.py
```

## Project Structure

```
ish_report_center/
├── app.py                      # Entry point — orchestrates all modules
├── requirements.txt
├── data/                       # CSV exports from admissions portal (gitignored)
├── config/
│   └── report_registry.py      # Single source of truth for all 17 report definitions
├── core/
│   ├── data_loader.py          # Cached CSV parsing with all portal-specific rules
│   └── filter_engine.py        # Dynamic sidebar filter widgets + application logic
├── exports/
│   └── excel_exporter.py       # Branded two-sheet Excel workbook generator
└── ui/
    ├── components.py           # Reusable Streamlit rendering blocks
    └── styles.py               # Global CSS — ISH brand, ERP layout
```

## Adding a New Report

1. Add the CSV file to `data/`
2. Add an entry to `config/report_registry.py` following the existing pattern
3. No other changes required — the app is fully config-driven

## Architecture Notes

- **Config-driven**: `report_registry.py` drives parsing, filtering, display, and export
- **`@st.cache_data`**: data is loaded once per session; reloaded only when the file changes
- **No report-specific code** in filter_engine or components — all behaviour is metadata-driven
- **Export**: Excel workbook has two sheets — filtered data (branded) + filter metadata
