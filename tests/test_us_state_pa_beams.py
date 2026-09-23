"""PennDOT BD-652M (2016) beams vs the printed section properties.

Published values are repeated literally from BD-652M sheets 1-3 (PDF pp1-3)
for spot checks; the full tables live in the package JSON. PennDOT prints
area to 1 in2, yb to 0.01 in and I to 1 in4; the tolerances below follow
that print precision except where a discrepancy is pinned explicitly.
"""

import pytest
from shapely.affinity import scale

from bridgebeams.us.state_common import gross_properties
from bridgebeams.us.state_pa_beams import (
    PaAashtoIBeamSection,
    PaBoxBeamSection,
    PaBulbTeeSection,
    PaIBeamSection,
    bc775_key_right_in,
)

from _aggregate import P, run_checks

IN = 25.4
CLASSES = (PaIBeamSection, PaAashtoIBeamSection, PaBulbTeeSection, PaBoxBeamSection)
PROVENANCE = {"transcribed", "transcribed-with-convention", "fitted-reconstruction", "estimate"}


def props(sec):
    return gross_properties(sec.polygon, IN)


def _check_all_sizes_valid_symmetric(cls):
    for size in cls.SIZES:
        s = cls(size)
        poly = s.polygon
        assert poly.is_valid and poly.exterior.is_ccw
        assert all(not r.is_ccw for r in poly.interiors)
        assert poly.bounds[1] == pytest.approx(0.0, abs=1e-9)
        assert poly.symmetric_difference(scale(poly, xfact=-1, origin=(0, 0))).area < 1e-3
        assert s.provenance in PROVENANCE
        assert s.source_status
        assert s.geometry is not None


def _check_invalid_size_raises(cls):
    with pytest.raises(ValueError):
        cls("nope")


def _check_counts():
    assert len(PaIBeamSection.SIZES) == 21
    assert len(PaAashtoIBeamSection.SIZES) == 7
    assert len(PaBulbTeeSection.SIZES) == 54
    assert len(PaBoxBeamSection.SIZES) == 58


def _check_girders_match_published_to_print_precision(cls):
    for size in cls.SIZES:
        s = cls(size)
        p, pub = props(s), s.published
        assert p["area"] == pytest.approx(pub["area_in2"], abs=0.51), size
        assert p["yb"] == pytest.approx(pub["yb_in"], abs=0.0101), size
        assert p["ix"] == pytest.approx(pub["ix_in4"], rel=1e-4), size


def _check_literal_spot_checks():
    # sheet 2: 24/48 -> 708 in2, 21.39 in, 172712 in4
    p = props(PaIBeamSection("24/48"))
    assert (round(p["area"]), round(p["yb"], 2), round(p["ix"])) == (708, 21.39, 172712)
    # sheet 2: AASHTO 28/96 -> 1277, 48.22, 1521775
    p = props(PaAashtoIBeamSection("28/96"))
    assert (round(p["area"]), round(p["yb"], 2)) == (1277, 48.22)
    assert p["ix"] == pytest.approx(1521775, abs=1.0)  # exact 1521775.5
    # sheet 3: 33/95.5 -> 1266, 46.02, 1521445
    p = props(PaBulbTeeSection("33/95.5"))
    assert (round(p["area"]), round(p["yb"], 2), round(p["ix"])) == (1266, 46.02, 1521445)
    s = PaBulbTeeSection("33/95.5")
    assert s.dimensions.top_width == pytest.approx(48 * IN)
    assert s.dimensions.depth == pytest.approx(95.5 * IN)


def test_24_63_uses_2016_corrected_row():
    # The 2008 sheet printed 872 in2 / 29.71 in for the same dimensions.
    p = props(PaIBeamSection("24/63"))
    assert round(p["area"]) == 920 and round(p["yb"], 2) == 30.90


def _check_spread_boxes_match_published():
    for size in PaBoxBeamSection.SIZES:
        if not size.startswith("spread"):
            continue
        s = PaBoxBeamSection(size)
        p, pub = props(s), s.published
        assert p["area"] == pytest.approx(pub["area_in2"], abs=0.51), size
        assert p["yb"] == pytest.approx(pub["yb_in"], abs=0.0101), size
        assert p["ix"] == pytest.approx(pub["ix_in4"], rel=1e-4), size
        assert len(s.polygon.interiors) == 1


def _check_adjacent_boxes_33_and_deeper_with_bc775_key():
    for size in PaBoxBeamSection.SIZES:
        if not size.startswith("adjacent"):
            continue
        depth = float(size.split("x")[1])
        if depth < 33:
            continue
        s = PaBoxBeamSection(size)
        p, pub = props(s), s.published
        assert p["area"] == pytest.approx(pub["area_in2"], abs=0.5), size
        assert p["yb"] == pytest.approx(pub["yb_in"], abs=0.025), size
        assert p["ix"] == pytest.approx(pub["ix_in4"], rel=1.1e-3), size


def test_pinned_adjacent_17_to_30_table_uses_plank_key():
    """BD-652M 17-30 in adjacent properties imply the 3 in/4 in key.

    BC-775M assigns the 3 in/4 in key only to 12 in planks, so the
    implementation keeps the 6 in/6 in key and this discrepancy is pinned.
    """
    for w in (48, 36):
        for d in (17, 21, 24, 27, 30):
            s = PaBoxBeamSection(f"adjacent-{w}x{d}")
            p, pub = props(s), s.published
            deficit = pub["area_in2"] - p["area"]
            assert 3.5 < deficit < 6.0, (w, d, deficit)
            # replacing the key by the planks' 3/4 key recovers the table area
            small = 2 * _key_area({"top_in": 3.0, "height_in": 4.0})
            large = 2 * _key_area({"top_in": 6.0, "height_in": 6.0})
            assert p["area"] + large - small == pytest.approx(pub["area_in2"], abs=1.0)


def _key_area(k):
    key = {"upper_recess_in": 0.375, "key_recess_in": 0.75,
           "upper_taper_rise_in": 0.375, "lower_taper_rise_in": 0.75, **k}
    pts = bc775_key_right_in(0.0, 0.0, key)  # face at x=0; recess is negative x
    area = 0.0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        area += -(x0 + x1) / 2 * (y1 - y0)
    return area


def _check_planks_match_published():
    for w in (48, 36):
        s = PaBoxBeamSection(f"plank-{w}x12")
        p, pub = props(s), s.published
        assert p["area"] == pytest.approx(pub["area_in2"], abs=0.5)
        assert p["yb"] == pytest.approx(pub["yb_in"], abs=0.006)
        assert p["ix"] == pytest.approx(pub["ix_in4"], rel=4e-4)
        assert not s.polygon.interiors


def test_us_state_pa_beams_catalogue_checks():
    run_checks(
        (_check_all_sizes_valid_symmetric, P("cls", CLASSES)),
        (_check_invalid_size_raises, P("cls", CLASSES)),
        _check_counts,
        (_check_girders_match_published_to_print_precision, P("cls", (PaIBeamSection, PaAashtoIBeamSection, PaBulbTeeSection))),
        _check_literal_spot_checks,
        _check_spread_boxes_match_published,
        _check_adjacent_boxes_33_and_deeper_with_bc775_key,
        _check_planks_match_published,
    )
