import pandas as pd
from pathlib import Path

RAW_FILE = Path("data/raw/sample_inventory_data.csv")
PROCESSED_FILE = Path("data/processed/cleaned_inventory_data.csv")

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

PROCESSED_FILE.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(PROCESSED_FILE, index=False)

print("Cleaned data exported successfully.")
