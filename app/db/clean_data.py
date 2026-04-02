import pandas as pd
import os

# File paths
RAW_FILE = "data/raw/investments_VC.csv"
PROCESSED_FILE = "data/processed/cleaned_startup_investments.csv"

# Load dataset
df = pd.read_csv(RAW_FILE, encoding="latin1")

# Fix column names (remove extra spaces)
df.columns = df.columns.str.strip()

# Keep only useful columns
columns_to_keep = [
    "permalink",
    "name",
    "homepage_url",
    "category_list",
    "market",
    "funding_total_usd",
    "status",
    "country_code",
    "state_code",
    "region",
    "city",
    "funding_rounds",
    "founded_at",
    "founded_month",
    "founded_quarter",
    "founded_year",
    "first_funding_at",
    "last_funding_at",
    "seed",
    "venture",
    "equity_crowdfunding",
    "undisclosed",
    "convertible_note",
    "debt_financing",
    "angel",
    "grant",
    "private_equity",
    "post_ipo_equity",
    "post_ipo_debt",
    "secondary_market",
    "product_crowdfunding",
    "round_A",
    "round_B",
    "round_C",
    "round_D",
    "round_E",
    "round_F",
    "round_G",
    "round_H"
]

df = df[columns_to_keep]

# Remove rows where startup name is missing
df = df.dropna(subset=["name"])

# Remove duplicate startups based on permalink
df = df.drop_duplicates(subset=["permalink"])

# Clean funding_total_usd properly
df["funding_total_usd"] = (
    df["funding_total_usd"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .str.replace("$", "", regex=False)
    .str.replace("-", "", regex=False)
    .str.strip()
)

df["funding_total_usd"] = pd.to_numeric(
    df["funding_total_usd"], errors="coerce")

# Convert numeric columns
numeric_columns = [
    "funding_rounds",
    "founded_year",
    "seed",
    "venture",
    "equity_crowdfunding",
    "undisclosed",
    "convertible_note",
    "debt_financing",
    "angel",
    "grant",
    "private_equity",
    "post_ipo_equity",
    "post_ipo_debt",
    "secondary_market",
    "product_crowdfunding",
    "round_A",
    "round_B",
    "round_C",
    "round_D",
    "round_E",
    "round_F",
    "round_G",
    "round_H"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Convert date columns
date_columns = [
    "founded_at",
    "founded_month",
    "first_funding_at",
    "last_funding_at"
]

for col in date_columns:
    df[col] = pd.to_datetime(df[col], errors="coerce")

# Remove unrealistic founded years
df = df[(df["founded_year"].isna()) | (df["founded_year"] >= 1900)]

# Save cleaned dataset
os.makedirs("data/processed", exist_ok=True)
df.to_csv(PROCESSED_FILE, index=False)

print("Cleaned dataset saved to:", PROCESSED_FILE)
print("Total cleaned rows:", len(df))
print("Total cleaned columns:", len(df.columns))
print("Non-null funding_total_usd values:",
      df["funding_total_usd"].notna().sum())
