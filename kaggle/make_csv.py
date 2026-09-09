"""Write the scalar columns of visas.json as visas.csv for the Kaggle bundle.

The JSON is canonical. This file exists because Kaggle's preview and most
notebooks want a flat table; nested arrays (requirements, steps, faqs) and the
long-form notes stay in the JSON. Never edit the CSV by hand — regenerate it.
Run by .github/workflows/sync-kaggle.yml; the CSV is not committed here.
"""
import csv
import json
import sys

COLUMNS = [
    "slug", "country", "country_slug", "region", "programme_name", "visa_name",
    "program_status", "min_income_usd", "income_original", "cost_usd", "max_stay_months",
    "processing_time", "renewable", "max_total_years", "pr_path", "pr_after_years",
    "citizenship_path", "citizenship_after_years", "tax_residency_days",
    "foreign_income_taxed", "special_tax_regime", "dependents_allowed",
    "spouse_income_add_usd", "child_income_add_usd", "apply_from_abroad", "apply_method",
    "official_url", "page_url", "verified_at",
]


def main(src: str, dst: str) -> None:
    with open(src) as f:
        records = json.load(f)["records"]
    missing = [c for c in COLUMNS if c not in records[0]]
    if missing:
        raise SystemExit(f"visas.json no longer carries {missing} — update COLUMNS")
    with open(dst, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        for r in records:
            w.writerow({c: ("" if r.get(c) is None else r.get(c)) for c in COLUMNS})
    print(f"wrote {len(records)} rows to {dst}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
