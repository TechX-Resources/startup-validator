"""
Data pipeline for loading and processing public startup datasets.
Reads a CSV from data/raw/, validates data quality, cleans it,
and saves to both SQLite (data/processed/startups.db) and JSON.

Usage:
    python -m app.services.data_loader
    python app/services/data_loader.py
"""

import json
import csv
from pathlib import Path
from app.services.startup_db import save_records, query_all


RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
OUTPUT_FILE = PROCESSED_DIR / "startups.json"

COLUMN_ALIASES = {
    "company_name":  ["company_name", "name", "company", "organization_name", "startup_name"],
    "industry":      ["industry", "category_code", "category", "sector", "market", "vertical"],
    "description":   ["description", "short_description", "about", "overview", "summary"],
    "founded_year":  ["founded_year", "founded_at", "founded", "year_founded", "founding_year", "year"],
    "status":        ["status", "company_status", "outcome"],
    "funding_total": ["funding_total_usd", "total_funding", "funding_total", "total_funding_usd"],
    "funding_rounds":["funding_rounds", "num_funding_rounds", "rounds"],
    "has_VC":        ["has_VC", "vc_funded", "has_vc"],
    "is_top500":     ["is_top500", "top500", "top_500"],
}

# Data quality: valid year range
YEAR_MIN, YEAR_MAX = 1900, 2025


def _find_column(headers: list[str], aliases: list[str]) -> str | None:
    lower_headers = [h.strip().lower() for h in headers]
    for alias in aliases:
        if alias.lower() in lower_headers:
            return headers[lower_headers.index(alias.lower())]
    return None


def _quality_check(record: dict, issues: list) -> bool:
    """
    Validate a record for data quality. Returns True if record passes.
    Logs issues to the issues list for the quality report.
    """
    name = record.get("company_name", "unknown")

    if not record.get("company_name"):
        issues.append("missing company_name")
        return False
    if not record.get("industry"):
        issues.append(f"{name}: missing industry")
        return False

    year = record.get("founded_year")
    if year is not None and not (YEAR_MIN <= year <= YEAR_MAX):
        issues.append(f"{name}: invalid founded_year {year} — set to None")
        record["founded_year"] = None

    funding = record.get("funding_total")
    if funding is not None and funding < 0:
        issues.append(f"{name}: negative funding_total — set to None")
        record["funding_total"] = None

    return True


def load_csv(csv_path: str) -> tuple[list[dict], dict]:
    """
    Load a CSV, run quality checks, clean and return records + quality report.
    """
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    records, issues = [], []
    skipped = 0

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

            # Clean founded_year
            if record.get("founded_year"):
                try:
                    val = str(record["founded_year"]).strip()
                    record["founded_year"] = int(val.split("/")[-1] if "/" in val else val[:4])
                except (ValueError, TypeError):
                    record["founded_year"] = None

            # Clean numeric fields
            for field in ("funding_total", "funding_rounds"):
                try:
                    record[field] = float(record[field]) if record.get(field) else None
                except (ValueError, TypeError):
                    record[field] = None

            # Clean boolean fields
            for field in ("has_VC", "is_top500"):
                record[field] = record.get(field) in ("1", "1.0", "True", "true")

            # Build description if missing
            if not record.get("description"):
                city = row.get("city", "").strip()
                state = row.get("state_code", "").strip()
                status = record.get("status", "") or ""
                industry = record.get("industry", "")
                location = f" based in {city}, {state}" if city and state else ""
                status_str = f" Status: {status}." if status else ""
                record["description"] = f"{industry.capitalize()} company{location}.{status_str}"

            # Quality check
            if not _quality_check(record, issues):
                skipped += 1
                continue

            records.append(record)

    quality_report = {
        "total_raw": len(records) + skipped,
        "passed":    len(records),
        "skipped":   skipped,
        "issues":    issues[:20],  # cap at 20 for readability
    }
    return records, quality_report


def save_json(records: list[dict]) -> Path:
    """Save cleaned records to data/processed/startups.json."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)
    return OUTPUT_FILE


def load_processed() -> list[dict]:
    """Load processed startups from SQLite (primary) or JSON (fallback)."""
    try:
        rows = query_all()
        if rows:
            return rows
    except Exception:
        pass
    # JSON fallback
    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, encoding="utf-8") as f:
            return json.load(f)
    raise FileNotFoundError("No processed data found. Run data_loader.py first.")


class StartupDataLoader:
    def __init__(self):
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    def run(self, csv_path: str = None) -> Path:
        """Load CSV, run quality checks, save to SQLite + JSON."""
        if csv_path:
            target = Path(csv_path)
        else:
            target = next(RAW_DIR.glob("*.csv"), None)
            if target is None:
                raise FileNotFoundError("No CSV found in data/raw/.")

        print(f"Loading from: {target}")
        records, report = load_csv(str(target))

        print(f"\n--- Data Quality Report ---")
        print(f"  Total rows:  {report['total_raw']}")
        print(f"  Passed:      {report['passed']}")
        print(f"  Skipped:     {report['skipped']}")
        if report["issues"]:
            print(f"  Issues:      {report['issues'][:5]}")

        # Save to SQLite
        save_records(records)
        print(f"\n  Saved {len(records)} companies to SQLite")

        # Save to JSON as backup
        output = save_json(records)
        print(f"  Saved {len(records)} companies to {output}")
        print(f"\nSample: {records[0]}")
        return output


if __name__ == "__main__":
    import sys
    csv_arg = sys.argv[1] if len(sys.argv) > 1 else None
    loader = StartupDataLoader()
    loader.run(csv_arg)
