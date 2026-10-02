#!/usr/bin/env python3
"""Publish aggregate country counts from a completed local manufacturer campaign.

Only counts, geography, dates and input hashes leave the research directory.
The checked-in summary lets documentation builds run without source dossiers.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CAMPAIGN = ROOT / "docs/research/manufacturers/2026-10-01"
DEFAULT_OUTPUT = ROOT / "docs/source/_static/coverage/manufacturer-summary.json"
ROLE_METRICS = {
    "verified_manufacturer": "manufacturers",
    "verified_supplier": "suppliers",
    "historical_manufacturer": "historical_manufacturers",
    "historical_supplier": "historical_suppliers",
    "lead_unverified": "unverified_leads",
    "contractor_only": "contractors",
    "excluded": "excluded",
}
COUNT_FIELDS = ("records", "queries", *ROLE_METRICS.values(), "historical")
CLOSED_STATUSES = {"protocol_saturated", "searched_no_qualifying_source"}


def json_rows(path):
    with path.open(encoding="utf-8") as stream:
        for number, line in enumerate(stream, 1):
            if line.strip():
                try:
                    yield json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"{path.name}:{number}: invalid JSON") from exc


def actual_country(record):
    """Explicit actual-country null is not a discovery-country fallback."""
    return record["actual_country_iso2"] if "actual_country_iso2" in record else record.get("country_iso2")


def build_summary(campaign):
    aggregate = campaign / "aggregate"
    validation = json.loads((aggregate / "validation.json").read_text(encoding="utf-8"))
    if (validation.get("errors") or validation.get("warnings")
            or not validation.get("completion_gate_requested")
            or not validation.get("exports_refreshed")):
        raise ValueError("Manufacturer index must pass its completion gate before publication")
    inputs = [aggregate / name for name in ("companies.jsonl", "coverage.jsonl", "queries.jsonl", "validation.json")]
    # Validate the audit receipt's original input hashes when the local ledgers
    # are present. No original record or path is copied into the public payload.
    for name, expected in validation.get("input_sha256", {}).items():
        path = ROOT / name
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError(f"Audit input has changed or is missing: {name}")
    countries = {}
    for row in json_rows(aggregate / "coverage.jsonl"):
        code = row["country_iso2"]
        if code in countries or row["status"] not in CLOSED_STATUSES:
            raise ValueError(f"Duplicate or unfinished coverage: {code}")
        countries[code] = {
            "code": code, "name": row["country"], "continent": row["continent"],
            "coverage_status": row["status"], **dict.fromkeys(COUNT_FIELDS, 0),
        }
    ids = set()
    roles = Counter()
    for record in json_rows(aggregate / "companies.jsonl"):
        record_id = record["record_id"]
        if record_id in ids:
            raise ValueError(f"Duplicate canonical record: {record_id}")
        ids.add(record_id)
        code = actual_country(record)
        if code not in countries:
            raise ValueError(f"Canonical record needs known actual country: {record_id}")
        role = record["verification_status"]
        if role not in ROLE_METRICS:
            raise ValueError(f"Unknown role: {role}")
        target = countries[code]
        target["records"] += 1
        target[ROLE_METRICS[role]] += 1
        target["historical"] += int(role.startswith("historical_"))
        roles[role] += 1
    query_ids = set()
    for query in json_rows(aggregate / "queries.jsonl"):
        query_id = query["query_id"]
        if query_id in query_ids or query["country_iso2"] not in countries:
            raise ValueError(f"Duplicate or unknown-country query: {query_id}")
        query_ids.add(query_id)
        countries[query["country_iso2"]]["queries"] += 1
    if (len(ids) != validation["company_records"] or len(query_ids) != validation["queries"]
            or dict(roles) != validation["verification_status"]
            or len(countries) != validation["planned_jurisdictions"]):
        raise ValueError("Aggregate counts disagree with the completed audit receipt")
    if any(row["queries"] < 2 for row in countries.values()):
        raise ValueError("A researched jurisdiction lacks the minimum two queries")
    totals = {key: sum(row[key] for row in countries.values()) for key in COUNT_FIELDS}
    totals.update({
        "jurisdictions": len(countries),
        "manufacturer_countries": sum(row["manufacturers"] > 0 for row in countries.values()),
        "supplier_countries": sum(row["suppliers"] > 0 for row in countries.values()),
        "current_role_countries": sum(row["manufacturers"] + row["suppliers"] > 0 for row in countries.values()),
    })
    continents = {}
    for row in countries.values():
        target = continents.setdefault(row["continent"], {"jurisdictions": 0, **dict.fromkeys(COUNT_FIELDS, 0)})
        target["jurisdictions"] += 1
        for key in COUNT_FIELDS:
            target[key] += row[key]
    return {
        "schema_version": 1, "campaign_date": campaign.name,
        "snapshot_created_at": validation["snapshot_created_at"],
        "count_basis": "Named company, branch, public organisation or factory operating-unit records; not a legal-entity deduplication or factory census.",
        "current_role_basis": "Opened sources support advertised PSC bridge-beam manufacture or supply. Current means a source-supported advertised role, not verified physical production at the snapshot date.",
        "records_basis": "All canonical discovery records, including unverified leads, contractors and exclusions. Current manufacturers and suppliers are separate statuses, not overlapping counts.",
        "geography_basis": "Company actual country for records and roles; searched jurisdiction for queries. Foreign-market leads are excluded from domestic company counts. A zero is a saved-observation count, not evidence of producer absence.",
        "coverage_basis": "250 planned countries and areas in the UN M49 campaign partition with Taiwan and Kosovo recorded separately. Protocol closure means the documented search frontier was closed, not that every web page or producer was found.",
        "input_sha256": {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in inputs},
        "totals": totals, "continents": dict(sorted(continents.items())),
        "countries": sorted(countries.values(), key=lambda row: row["code"]),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("campaign", type=Path, nargs="?", default=DEFAULT_CAMPAIGN)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    summary = build_summary(args.campaign)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary["totals"], sort_keys=True))
    print(f"Public aggregate: {args.output}")


if __name__ == "__main__":
    main()
