"""The original multilingual survey keeps its own strict evidence schema."""
import importlib.util
import json
from pathlib import Path

import pytest


@pytest.fixture
def checker(tmp_path):
    path = Path(__file__).resolve().parents[1] / "tools/check_discovery_sources.py"
    spec = importlib.util.spec_from_file_location("discovery_schema_check", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.DATA = tmp_path
    return module


def legacy_record():
    return {
        "id": "survey-no-psc", "country_code": "BB", "country": "Barbados",
        "language": "en", "source_type": "authority_survey",
        "title_original": "", "title_en": "Bridge evidence survey",
        "url": "https://example.org/bridges", "locator": "",
        "family_names": [], "status": "no PSC beam evidence found",
        "authority": "Recorded public works authority",
        "note": "No PSC girder evidence in the checked source",
        "survey_status": "NONE-FOUND",
    }


def write_document(checker, record, *, legacy=True):
    document = {"records": [record]}
    if legacy:
        document["topic"] = "round5-multilingual-sweep"
    (checker.DATA / "deep-search-fixture.json").write_text(json.dumps(document))


def test_original_none_found_survey_accepts_no_named_family(checker, capsys):
    write_document(checker, legacy_record())
    checker.main()
    summary = json.loads(capsys.readouterr().out)
    assert summary["records"] == 1
    assert summary["statuses"] == {"no PSC beam evidence found": 1}


@pytest.mark.parametrize("field,value,missing", [
    ("authority", None, True), ("note", "", False),
    ("survey_status", "UNRECOGNIZED", False), ("survey_status", [], False),
])
def test_legacy_survey_requires_its_own_fields_and_categories(checker, field, value, missing):
    record = legacy_record()
    if missing:
        del record[field]
    else:
        record[field] = value
    write_document(checker, record)
    with pytest.raises(ValueError, match=field):
        checker.main()


def test_survey_schema_is_not_enabled_without_explicit_topic(checker):
    write_document(checker, legacy_record(), legacy=False)
    with pytest.raises(ValueError, match="organisation.*missing_information"):
        checker.main()


def test_standard_complete_outline_still_requires_named_sections(checker):
    record = legacy_record()
    record.update({"organisation": "Recorded producer", "missing_information": "None; outline transcribed",
                   "status": "complete_outline", "title_original": "Producer beam drawing", "locator": "Drawing A"})
    write_document(checker, record, legacy=False)
    with pytest.raises(ValueError, match="lacks named sections"):
        checker.main()
