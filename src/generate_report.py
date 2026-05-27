import pandas as pd
from pathlib import Path

RAW_FILE = Path("data/raw/sample_inventory_data.csv")

PROCESSED_DIR = Path("data/processed")

CLEAN_FILE = PROCESSED_DIR / "cleaned_inventory_data.csv"
EXCEPTION_FILE = PROCESSED_DIR / "exception_inventory_data.csv"

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

df["inspection_date"] = pd.to_datetime(
    df["inspection_date"],
    errors="coerce"
)

df["quality_issue"] = ""

df.loc[df["cal_alpha"].isna(), "quality_issue"] += "Missing CAL_ALPHA; "
df.loc[df["cal_od"].isna(), "quality_issue"] += "Missing CAL_OD; "

clean_df = df[df["quality_issue"] == ""]
exception_df = df[df["quality_issue"] != ""]

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

clean_df.to_csv(CLEAN_FILE, index=False)
exception_df.to_csv(EXCEPTION_FILE, index=False)

print("Clean data exported.")
print("Exception data exported.")