"""
Data pipeline for loading and processing public startup datasets.
Reads a CSV from data/raw/, cleans it, and saves to data/processed/startups.json.

Usage:
    python -m app.services.data_loader
    python app/services/data_loader.py
"""

import json
import csv
from pathlib import Path


RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
OUTPUT_FILE = PROCESSED_DIR / "startups.json"

# Maps standard field names to common Kaggle column name variations
COLUMN_ALIASES = {
    "company_name":    ["company_name", "name", "company", "organization_name", "startup_name"],
    "industry":        ["industry", "category_code", "category", "sector", "market", "vertical"],
    "description":     ["description", "short_description", "about", "overview", "summary"],
    "founded_year":    ["founded_year", "founded_at", "founded", "year_founded", "founding_year", "year"],
    "status":          ["status", "company_status", "outcome"],
    "funding_total":   ["funding_total_usd", "total_funding", "funding_total", "total_funding_usd"],
    "funding_rounds":  ["funding_rounds", "num_funding_rounds", "rounds"],
    "has_VC":          ["has_VC", "vc_funded", "has_vc"],
    "is_top500":       ["is_top500", "top500", "top_500"],
}


def _find_column(headers: list[str], aliases: list[str]) -> str | None:
    """Return the first matching header from aliases (case-insensitive)."""
    lower_headers = [h.strip().lower() for h in headers]
    for alias in aliases:
        if alias.lower() in lower_headers:
            return headers[lower_headers.index(alias.lower())]
    return None


def load_csv(csv_path: str) -> list[dict]:
    """Load a CSV from data/raw/, clean and filter it, return standardized records."""
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    records = []
    with open(path, encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []

        col_map = {
            field: _find_column(headers, aliases)
            for field, aliases in COLUMN_ALIASES.items()
        }

        for row in reader:
            record = {}
            for field, col in col_map.items():
                record[field] = row[col].strip() if col and row.get(col) else None

            # Filter out rows missing the two most important fields
            if not record.get("company_name") or not record.get("industry"):
                continue

            # Clean founded_year to be an integer year if possible
            if record.get("founded_year"):
                try:
                    val = str(record["founded_year"]).strip()
                    if "/" in val:
                        record["founded_year"] = int(val.split("/")[-1])
                    else:
                        record["founded_year"] = int(val[:4])
                except (ValueError, TypeError):
                    record["founded_year"] = None

            # Clean numeric fields
            for field in ("funding_total", "funding_rounds"):
                if record.get(field):
                    try:
                        record[field] = float(record[field])
                    except (ValueError, TypeError):
                        record[field] = None

            for field in ("has_VC", "is_top500"):
                if record.get(field) is not None:
                    record[field] = record[field] in ("1", "1.0", "True", "true")

            # Build a description from available fields if dataset doesn't have one
            if not record.get("description"):
                city = row.get("city", "").strip()
                state = row.get("state_code", "").strip()
                status = row.get("status", "").strip()
                industry = record.get("industry", "")
                location = f" based in {city}, {state}" if city and state else ""
                status_str = f" Status: {status}." if status else ""
                record["description"] = f"{industry.capitalize()} company{location}.{status_str}"

            records.append(record)

    return records


def save_json(records: list[dict]) -> Path:
    """Save cleaned records to data/processed/startups.json."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)
    return OUTPUT_FILE


def load_processed() -> list[dict]:
    """Load the processed JSON for use by the validation agent."""
    if not OUTPUT_FILE.exists():
        raise FileNotFoundError(
            "Processed data not found. Run data_loader.py first.\n"
            f"Expected: {OUTPUT_FILE}"
        )
    with open(OUTPUT_FILE, encoding="utf-8") as f:
        return json.load(f)


class StartupDataLoader:
    def __init__(self):
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    def run(self, csv_path: str = None) -> Path:
        """Load CSV from data/raw/, clean it, and save to data/processed/startups.json."""
        if csv_path:
            target = Path(csv_path)
        else:
            target = next(RAW_DIR.glob("*.csv"), None)
            if target is None:
                raise FileNotFoundError(
                    "No CSV file found in data/raw/. "
                    "Download a startup dataset from Kaggle and place it there."
                )

        print(f"Loading from: {target}")
        records = load_csv(str(target))
        output = save_json(records)
        print(f"Done! Saved {len(records)} companies to {output}")
        print(f"Sample record: {records[0]}")
        return output


if __name__ == "__main__":
    import sys
    csv_arg = sys.argv[1] if len(sys.argv) > 1 else None
    loader = StartupDataLoader()
    loader.run(csv_arg)
