"""Public map counts preserve role scope, geography and output isolation."""
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess

import pytest

ROOT = Path(__file__).resolve().parents[1]


def load_tool(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_campaign(path):
    aggregate = path / "aggregate"
    aggregate.mkdir(parents=True)
    records = [
        {"record_id": "manufacturer", "country_iso2": "IN", "actual_country_iso2": "CA", "verification_status": "verified_manufacturer", "private_notes": "must not be published"},
        {"record_id": "supplier", "country_iso2": "IN", "verification_status": "verified_supplier"},
        {"record_id": "past", "country_iso2": "CA", "verification_status": "historical_supplier"},
        {"record_id": "lead", "country_iso2": "IN", "verification_status": "lead_unverified"},
    ]
    coverage = [{"country_iso2": code, "country": name, "continent": continent, "status": "protocol_saturated"}
                for code, name, continent in [("CA", "Canada", "north_america"), ("IN", "India", "asia")]]
    queries = [{"query_id": f"{code}-{n}", "country_iso2": code, "query": "private raw query"}
               for code in ("CA", "IN") for n in range(2)]
    validation = {"completion_gate_requested": True, "exports_refreshed": True, "errors": [], "warnings": [],
                  "company_records": 4, "queries": 4, "planned_jurisdictions": 2,
                  "verification_status": {"verified_manufacturer": 1, "verified_supplier": 1, "historical_supplier": 1, "lead_unverified": 1},
                  "snapshot_created_at": "2026-10-02T06:00:00Z"}
    for name, rows in [("companies.jsonl", records), ("coverage.jsonl", coverage), ("queries.jsonl", queries)]:
        (aggregate / name).write_text("".join(json.dumps(row) + "\n" for row in rows))
    (aggregate / "validation.json").write_text(json.dumps(validation))
    return records, validation


def test_public_summary_uses_actual_country_and_preserves_role_categories(tmp_path):
    tool = load_tool("build_manufacturer_summary")
    campaign = tmp_path / "2026-10-01"
    write_campaign(campaign)
    summary = tool.build_summary(campaign)
    rows = {row["code"]: row for row in summary["countries"]}
    assert rows["CA"]["manufacturers"] == 1
    assert rows["IN"]["manufacturers"] == 0
    assert rows["IN"]["suppliers"] == 1
    assert rows["CA"]["historical"] == 1
    assert summary["totals"]["records"] == 4
    assert summary["totals"]["current_role_countries"] == 2
    assert "private" not in json.dumps(summary)
    assert "record_id" not in json.dumps(summary)
    assert tool.actual_country({"actual_country_iso2": None, "country_iso2": "IN"}) is None


def test_summary_rejects_unfinished_or_inconsistent_audit(tmp_path):
    tool = load_tool("build_manufacturer_summary")
    campaign = tmp_path / "2026-10-01"
    _, validation = write_campaign(campaign)
    validation["queries"] = 5
    receipt = campaign / "aggregate/validation.json"
    receipt.write_text(json.dumps(validation))
    with pytest.raises(ValueError, match="disagree"):
        tool.build_summary(campaign)
    validation["warnings"] = ["unfinished"]
    receipt.write_text(json.dumps(validation))
    with pytest.raises(ValueError, match="completion gate"):
        tool.build_summary(campaign)


def test_checked_in_snapshot_has_audited_totals_and_no_dossiers():
    summary = json.loads((ROOT / "docs/source/_static/coverage/manufacturer-summary.json").read_text())
    assert {key: summary["totals"][key] for key in ("records", "manufacturers", "suppliers", "historical", "queries", "jurisdictions")} == {
        "records": 1728, "manufacturers": 497, "suppliers": 31, "historical": 118, "queries": 4555, "jurisdictions": 250,
    }
    for key in ("records", "manufacturers", "suppliers", "historical", "queries"):
        assert sum(row[key] for row in summary["countries"]) == summary["totals"][key]
        assert sum(row[key] for row in summary["continents"].values()) == summary["totals"][key]
    assert all("sources" not in row and "company_name" not in row for row in summary["countries"])


def test_fresh_docs_output_drops_old_attachments_and_retains_source_backups(tmp_path):
    tool = load_tool("build_local_docs")
    source_backup = tmp_path / "source/_static/coverage/backups/template.html.bak-test"
    source_backup.parent.mkdir(parents=True)
    source_backup.write_text("original source backup")
    output = tmp_path / "html"
    stale = output / "_static/coverage/backups/template.html.bak-test"
    stale.parent.mkdir(parents=True)
    stale.write_text("stale copied backup")
    (output / "dims_review.html").write_text("private old attachment")
    (output / "sources").symlink_to(tmp_path / "source", target_is_directory=True)
    candidate = tmp_path / "fresh/html"
    candidate.mkdir(parents=True)
    (candidate / "index.html").write_text("fresh public page")
    tool.replace_generated_output(candidate, output)
    assert (output / "index.html").read_text() == "fresh public page"
    assert not list(output.rglob("backups"))
    assert not (output / "dims_review.html").exists()
    assert not (output / "sources").exists()
    assert source_backup.read_text() == "original source backup"


def test_selected_metric_is_not_duplicated_in_comparison_columns(tmp_path):
    node = shutil.which("node")
    if node is None:
        pytest.skip("Node is needed to execute the offline table interaction")
    assets = ROOT / "docs/source/_static/coverage"
    template = (assets / "coverage-template.html").read_text()
    data = json.loads((assets / "coverage-data.json").read_text())
    country_header = re.search(r"<thead><tr>(.*?)</tr></thead>", template).group(1)
    headers = []
    for index, (attributes, text) in enumerate(re.findall(r"<th([^>]*)>(.*?)</th>", country_header)):
        comparison = re.search(r'data-comparison="([^"]+)"', attributes)
        headers.append({"cellIndex": index, "textContent": text, "dataset": {
            "comparison": comparison.group(1) if comparison else None}, "hidden": False})
    assert len(headers) == 9
    script = template.split("const DATA=", 1)[1].split("function selectCountry", 1)[0]
    script = "const DATA=" + script.replace("/* DATA */", json.dumps(data), 1)
    # Execute the actual metric handler with table cells, headings and map
    # controls represented by small DOM substitutes; no network/browser needed.
    harness = """
const assert=require('node:assert/strict');
const headings=HEADERS;
const widgets=Object.fromEntries(['search','scope','details','metric','metric-description','metric-summary','metric-heading','legend'].map(name=>[name,{value:'',textContent:'',innerHTML:''}]));
widgets.metric.value='sections';widgets['metric-heading']=headings[2];
const rows=COUNTRIES.map(row=>({dataset:{code:row.code},cells:headings.map(()=>({hidden:false,textContent:''})),querySelector(){return this.cells[2];}}));
const svg={setAttribute(){}};
const document={querySelector(selector){return selector==='svg'?svg:widgets[selector.slice(1)];},querySelectorAll(selector){if(selector==='th[data-comparison]')return headings.filter(th=>th.dataset.comparison);if(selector==='#country-rows tr')return rows;if(selector==='path.country')return [];throw Error(selector);}};
function filter(){}
ACTUAL_SCRIPT
for(const key of Object.keys(METRICS)){
 metric.value=key;updateMetric();
 const hidden=headings.filter(th=>th.hidden),expected=headings.filter(th=>th.dataset.comparison===key);
 assert.deepEqual(hidden,expected);
 for(const row of rows){
   assert.equal(row.cells[2].hidden,false);
   for(const th of headings.filter(th=>th.dataset.comparison))assert.equal(row.cells[th.cellIndex].hidden,th.hidden);
 }
 const visible=headings.filter(th=>!th.hidden).map(th=>th.textContent);
 assert.equal(visible.filter(label=>label===METRICS[key].label).length,1);
 console.log(key+': '+visible.join(' | '));
}
""".replace("HEADERS", json.dumps(headers)).replace("COUNTRIES", json.dumps(data["countries"])).replace("ACTUAL_SCRIPT", script)
    target = tmp_path / "table-interaction.cjs"
    target.write_text(harness)
    result = subprocess.run([node, str(target)], capture_output=True, text=True, check=True)
    assert len(result.stdout.splitlines()) == 7
