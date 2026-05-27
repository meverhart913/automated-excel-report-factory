import pandas as pd
from pathlib import Path

RAW_FILE = Path("data/raw/sample_inventory_data.csv")

PROCESSED_DIR = Path("data/processed")
REPORTS_DIR = Path("reports")

CLEAN_FILE = PROCESSED_DIR / "cleaned_inventory_data.csv"
EXCEPTION_FILE = PROCESSED_DIR / "exception_inventory_data.csv"
REPORT_FILE = REPORTS_DIR / "inventory_report.xlsx"

required_columns = [
    "serial_number",
    "part_number",
    "overall_length",
    "diameter",
    "cal_alpha",
    "cal_od",
    "status",
    "inspection_date",
]

df = pd.read_csv(RAW_FILE)

missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    raise ValueError(f"Missing required columns: {missing_columns}")

df["inspection_date"] = pd.to_datetime(df["inspection_date"], errors="coerce")

df["quality_issue"] = ""

df.loc[df["cal_alpha"].isna(), "quality_issue"] += "Missing CAL_ALPHA; "
df.loc[df["cal_od"].isna(), "quality_issue"] += "Missing CAL_OD; "

clean_df = df[df["quality_issue"] == ""]
exception_df = df[df["quality_issue"] != ""]

summary_df = pd.DataFrame({
    "Metric": [
        "Total Records",
        "Clean Records",
        "Exception Records",
        "Unique Part Numbers",
    ],
    "Value": [
        len(df),
        len(clean_df),
        len(exception_df),
        df["part_number"].nunique(),
    ],
})

part_summary_df = (
    df.groupby("part_number")
    .agg(
        record_count=("serial_number", "count"),
        avg_overall_length=("overall_length", "mean"),
        avg_diameter=("diameter", "mean"),
        avg_cal_alpha=("cal_alpha", "mean"),
        avg_cal_od=("cal_od", "mean"),
    )
    .reset_index()
)

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

clean_df.to_csv(CLEAN_FILE, index=False)
exception_df.to_csv(EXCEPTION_FILE, index=False)

with pd.ExcelWriter(REPORT_FILE, engine="openpyxl") as writer:
    summary_df.to_excel(writer, sheet_name="Summary", index=False)
    part_summary_df.to_excel(writer, sheet_name="Part Summary", index=False)
    clean_df.to_excel(writer, sheet_name="Clean Data", index=False)
    exception_df.to_excel(writer, sheet_name="Exceptions", index=False)

print("Clean data exported.")
print("Exception data exported.")
print("Excel report created.")