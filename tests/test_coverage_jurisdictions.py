"""Shared producer geometry has one identity across country assignments."""

import json
from pathlib import Path

from bridgebeams.ie import IeWBeamSection
from bridgebeams.uk import UkWBeamSection


def test_shared_banagher_geometry_and_catalogue_identity():
    assert UkWBeamSection is IeWBeamSection
    data = json.loads((Path(__file__).resolve().parents[1] /
                       "docs/source/_static/coverage/coverage-data.json").read_text())
    by_code = {row["code"]: row for row in data["countries"]}
    uk = {pid for family in by_code["GB"]["families"] for pid in family["profile_ids"]}
    ireland = {pid for family in by_code["IE"]["families"] for pid in family["profile_ids"]}
    assert uk and uk <= ireland
    assert data["country_profile_assignments"] == sum(row["count"] for row in data["countries"])
    assert data["implemented_profiles"] == len({
        pid for row in data["countries"] for family in row["families"]
        for pid in family["profile_ids"]
    })
