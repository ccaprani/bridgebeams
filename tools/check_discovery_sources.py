#!/usr/bin/env python3
"""Validate the multilingual named-section discovery queue.

This checks record structure and duplicate identifiers. Source truth still
requires reviewing the linked primary documents and cited page locators.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "docs/research/data"
STATUSES = {"named_only", "partial_dimensions", "complete_outline", "blocked"}
REQUIRED = (
    "id", "country_code", "country", "language", "source_type",
    "organisation", "title_original", "title_en", "url", "locator",
    "family_names", "status", "missing_information",
)


def main() -> None:
    files = sorted(DATA.glob("deep-search-*-2026-09.json"))
    if not files:
        raise ValueError("No deep-search records found")
    identifiers: set[str] = set()
    by_country: dict[str, int] = {}
    by_status: dict[str, int] = {}
    for file in files:
        document = json.loads(file.read_text(encoding="utf-8"))
        records = document["records"]
        if not isinstance(records, list) or not records:
            raise ValueError(f"{file}: expected nonempty records list")
        for record in records:
            missing = [key for key in REQUIRED if key not in record]
            if missing:
                raise ValueError(f"{file}: {record.get('id', '<no id>')}: missing {missing}")
            identity = record["id"]
            if not isinstance(identity, str) or not identity.strip() or identity in identifiers:
                raise ValueError(f"{file}: empty or duplicate id {identity!r}")
            identifiers.add(identity)
            code = record["country_code"]
            if not isinstance(code, str) or not re.fullmatch(r"[A-Z]{2}", code):
                raise ValueError(f"{identity}: invalid country_code {code!r}")
            status = record["status"]
            if status not in STATUSES:
                raise ValueError(f"{identity}: invalid status {status!r}")
            parsed = urlparse(record["url"])
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                raise ValueError(f"{identity}: invalid source URL")
            for key in REQUIRED:
                if key in {"family_names", "status", "url"}:
                    continue
                if not isinstance(record[key], str) or not record[key].strip():
                    raise ValueError(f"{identity}: empty {key}")
            names = record["family_names"]
            if not isinstance(names, list) or any(not isinstance(n, str) or not n.strip() for n in names):
                raise ValueError(f"{identity}: invalid family_names")
            if status != "blocked" and not names:
                raise ValueError(f"{identity}: verified lead lacks named sections")
            by_country[code] = by_country.get(code, 0) + 1
            by_status[status] = by_status.get(status, 0) + 1
    print(json.dumps({"files": len(files), "records": len(identifiers),
                      "countries": by_country, "statuses": by_status}, indent=2))


if __name__ == "__main__":
    main()
