"""Validate the versioned regional source records and report country coverage.

Run from any directory. Add --verify-downloads to check the ignored local
files against their SHA-256 hashes and PDFs against their page counts. Add --write-index
to refresh the generated coverage table in docs/research/README.md.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import date
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
CATALOGUES = (
    ("europe-americas", "Europe / Americas"),
    ("asia-africa", "Asia / Africa"),
)
START = "<!-- country-index:start -->"
END = "<!-- country-index:end -->"


def validate(verify_downloads: bool = False) -> tuple[list[dict], set[Path]]:
    records, seen, checked_files = [], set(), set()
    for stem, region in CATALOGUES:
        path = ROOT / "docs" / "research" / "data" / f"{stem}-sources.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        date.fromisoformat(data["accessed"])
        if not isinstance(data["sources"], list) or not data["sources"]:
            raise ValueError(f"{path}: expected non-empty sources list")
        for source in data["sources"]:
            source_id = source["id"]
            if source_id in seen:
                raise ValueError(f"Duplicate source id: {source_id}")
            seen.add(source_id)
            for field in ("id", "country", "country_code", "title_original",
                          "title_en", "organisation", "status"):
                if not isinstance(source.get(field), str) or not source[field].strip():
                    raise ValueError(f"{source_id}: missing/non-string {field}")
            if not re.fullmatch(r"[A-Z]{2}", source["country_code"]):
                raise ValueError(f"{source_id}: invalid country code")
            if not isinstance(source.get("evidence"), dict):
                raise ValueError(f"{source_id}: expected evidence object")
            if source.get("url") is None:
                citation = source["evidence"].get("citation")
                if not isinstance(citation, str) or not citation.strip():
                    raise ValueError(f"{source_id}: missing URL and bibliographic citation")
            else:
                parsed = urlparse(source["url"])
                if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                    raise ValueError(f"{source_id}: invalid source URL")
            for field in ("families", "dimensions"):
                if not isinstance(source.get(field), list):
                    raise ValueError(f"{source_id}: expected {field} list")
            if source.get("local_file"):
                local = (ROOT / source["local_file"]).resolve()
                if not local.is_relative_to(ROOT / "sources"):
                    raise ValueError(f"{source_id}: download is outside sources/")
                if not re.fullmatch(r"[a-f0-9]{64}", source.get("sha256", "")):
                    raise ValueError(f"{source_id}: invalid/missing SHA-256")
                is_pdf = local.suffix.lower() == ".pdf"
                if is_pdf and (not isinstance(source.get("pages"), int) or source["pages"] < 1):
                    raise ValueError(f"{source_id}: invalid/missing PDF page count")
                if verify_downloads:
                    digest = hashlib.sha256()
                    with local.open("rb") as stream:
                        for block in iter(lambda: stream.read(1024 * 1024), b""):
                            digest.update(block)
                    if digest.hexdigest() != source["sha256"]:
                        raise ValueError(f"{source_id}: file hash mismatch")
                    if is_pdf:
                        info = subprocess.run(
                            ["pdfinfo", str(local)], check=True, capture_output=True,
                            text=True, timeout=30,
                        ).stdout
                        match = re.search(r"^Pages:\s+(\d+)", info, re.MULTILINE)
                        if not match or int(match[1]) != source["pages"]:
                            raise ValueError(f"{source_id}: PDF page count mismatch")
                    checked_files.add(local)
            records.append({**source, "region": region, "catalogue": stem})
    return records, checked_files


def country_index(records: list[dict]) -> str:
    countries = defaultdict(list)
    for source in records:
        countries[source["country_code"]].append(source)
    rows = [
        "## Country index", "",
        f"{len(records)} source records across {len(countries)} country/jurisdiction codes. "
        "Counts include access blockers and rejected leads; they are not counts of "
        "implemented or verified beam families. Dimension rows include partial "
        "dimension and property tables.", "",
        "| Country / jurisdiction | Source records | Dimension / property rows | Report |",
        "|---|---:|---:|---|",
    ]
    for code, sources in sorted(countries.items(), key=lambda item: item[1][0]["country"]):
        country = sources[0]["country"].replace("|", "\\|")
        reports = sorted({s["catalogue"] for s in sources})
        links = "; ".join(f"[{name}]({name}-2026-09.md)" for name in reports)
        count = sum(len(s["dimensions"]) for s in sources)
        rows.append(f"| {country} ({code}) | {len(sources)} | {count} | {links} |")
    rows.extend(["", "Qatar, New Zealand, Norway and Japan also have a separate "
                 "[PDF backlog audit](pdf-transcription-2026-09.md). Its drawing "
                 "transcriptions are additional to the regional counts above."])
    return "\n".join(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-downloads", action="store_true")
    parser.add_argument("--write-index", action="store_true")
    args = parser.parse_args()
    records, checked = validate(args.verify_downloads)
    if args.write_index:
        path = ROOT / "docs" / "research" / "README.md"
        content = path.read_text(encoding="utf-8")
        generated = f"{START}\n{country_index(records)}\n{END}"
        if START in content and END in content:
            before, rest = content.split(START, 1)
            _, after = rest.split(END, 1)
            content = before + generated + after
        else:
            content = content.rstrip() + "\n\n" + generated + "\n"
        path.write_text(content, encoding="utf-8")
    print(json.dumps({
        "source_records": len(records),
        "country_codes": len({s["country_code"] for s in records}),
        "dimension_or_property_rows": sum(len(s["dimensions"]) for s in records),
        "local_files_verified": len(checked),
        "local_pdfs_verified": sum(p.suffix.lower() == ".pdf" for p in checked),
    }, indent=2))


if __name__ == "__main__":
    main()
