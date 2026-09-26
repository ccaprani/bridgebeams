"""ODOT BR360/BR365/BR375 deck bulb-tees: sheet dimensions and analytic checks.

The sheets print no section properties (and Brice et al. 2021 Table A.11
covers the non-deck BT/BI details), so checks are dimensional plus a
hand-summed trapezoid area.
"""

import pytest
from shapely.affinity import scale

from bridgebeams.us.state_common import gross_properties
from bridgebeams.us.state_r3_or_deck_bulb_tee import OrDeckBulbTeeSection

from _aggregate import P, run_checks

IN = 25.4
DEPTH = {"DKBT36": 36, "DKBT45": 45, "DKBT60": 60}


def _check_valid_symmetric(size):
    s = OrDeckBulbTeeSection(size)
    p = s.polygon
    assert p.is_valid and p.exterior.is_ccw
    assert p.bounds[1] == pytest.approx(0.0, abs=1e-9)
    assert p.symmetric_difference(scale(p, xfact=-1, origin=(0, 0))).area < 1e-2
    assert s.provenance == "transcribed-with-convention"
    assert s.source_status
    assert s.geometry is not None


def _check_dimensions(size):
    s = OrDeckBulbTeeSection(size)
    fam, w = size.split("-W")
    x0, _, x1, y1 = s.polygon.bounds
    assert y1 == pytest.approx(DEPTH[fam] * IN)
    assert x1 - x0 == pytest.approx(float(w) * IN)
    assert s.dimensions.bulb_width == pytest.approx(24 * IN)
    assert s.dimensions.web_width == pytest.approx(6 * IN)
    assert s.dimensions.flange_edge_thickness == pytest.approx(6 * IN)


def _check_area_hand_sum(size):
    fam, w = size.split("-W")
    w, d = float(w), DEPTH[fam]
    web = d - 6 - 3 - 2 - 4 - 6
    area = (24 * 6 - 1) + 15 * 3 + 6 * web + 9 * 2 + 30 * 4 + w * 6
    assert gross_properties(OrDeckBulbTeeSection(size).polygon, IN)["area"] == pytest.approx(area)


def _check_flange_width_override():
    s = OrDeckBulbTeeSection("DKBT45-W72", flange_width=66)
    assert s.polygon.bounds[2] - s.polygon.bounds[0] == pytest.approx(66 * IN)
    with pytest.raises(ValueError):
        OrDeckBulbTeeSection("DKBT45-W72", flange_width=58)
    with pytest.raises(ValueError):
        OrDeckBulbTeeSection("DKBT45-W72", flange_width=104)


def _check_invalid_size_raises():
    with pytest.raises(ValueError):
        OrDeckBulbTeeSection("DKBT51-W72")


def test_us_state_r3_or_deck_bulb_tee_catalogue_checks():
    sizes = P("size", OrDeckBulbTeeSection.SIZES)
    assert len(OrDeckBulbTeeSection.SIZES) == 12
    run_checks(
        (_check_valid_symmetric, sizes),
        (_check_dimensions, sizes),
        (_check_area_hand_sum, sizes),
        _check_flange_width_override,
        _check_invalid_size_raises,
    )
