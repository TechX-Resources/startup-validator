"""
Schema drift detection for the startup data pipeline.
On every pipeline run, compares incoming CSV columns against the expected schema.
Flags added, removed, or renamed columns before data is persisted.
"""

import json
from pathlib import Path
from datetime import datetime

SCHEMA_FILE = Path("data/processed/schema_snapshot.json")

# Expected columns based on the Kaggle startup dataset
EXPECTED_COLUMNS = {
    "name", "category_code", "founded_at", "status",
    "funding_total_usd", "funding_rounds", "has_VC", "is_top500",
    "city", "state_code",
}


def _load_snapshot() -> dict:
    if SCHEMA_FILE.exists():
        with open(SCHEMA_FILE) as f:
            return json.load(f)
    return {}


def _save_snapshot(columns: set):
    SCHEMA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SCHEMA_FILE, "w") as f:
        json.dump({
            "columns": sorted(columns),
            "last_checked": datetime.utcnow().isoformat(),
        }, f, indent=2)


def check_schema(incoming_columns: list[str]) -> dict:
    """
    Compare incoming CSV columns against last known snapshot.
    Returns a drift report with added/removed/missing columns.
    """
    incoming = set(incoming_columns)
    snapshot = _load_snapshot()
    previous = set(snapshot.get("columns", [])) if snapshot else None

    # Check against expected schema
    missing_expected  = EXPECTED_COLUMNS - incoming
    unexpected        = incoming - EXPECTED_COLUMNS

    # Check against last run snapshot
    added_since_last   = (incoming - previous) if previous else set()
    removed_since_last = (previous - incoming) if previous else set()

    drift_detected = bool(missing_expected or added_since_last or removed_since_last)

    report = {
        "drift_detected":      drift_detected,
        "missing_expected":    sorted(missing_expected),
        "unexpected_columns":  sorted(unexpected),
        "added_since_last":    sorted(added_since_last),
        "removed_since_last":  sorted(removed_since_last),
        "checked_at":          datetime.utcnow().isoformat(),
    }

    if drift_detected:
        print(f"\n⚠ Schema drift detected!")
        if missing_expected:
            print(f"  Missing expected columns: {sorted(missing_expected)}")
        if added_since_last:
            print(f"  New columns since last run: {sorted(added_since_last)}")
        if removed_since_last:
            print(f"  Removed since last run: {sorted(removed_since_last)}")
    else:
        print("\n  Schema OK — no drift detected")

    # Save current as new snapshot
    _save_snapshot(incoming)
    return report
