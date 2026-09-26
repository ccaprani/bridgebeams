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
    # Shared Banagher aliases keep their Irish IDs; UK-only producer families
    # (e.g. FP McCann) live in bridgebeams.uk modules and are GB-only.
    uk_own = {pid for family in by_code["GB"]["families"]
              if family["module"].startswith("bridgebeams.uk.") for pid in family["profile_ids"]}
    assert uk - uk_own and (uk - uk_own) <= ireland
    assert not uk_own & ireland
    assert data["country_profile_assignments"] == sum(row["count"] for row in data["countries"])
    assert data["implemented_profiles"] == len({
        pid for row in data["countries"] for family in row["families"]
        for pid in family["profile_ids"]
    })
