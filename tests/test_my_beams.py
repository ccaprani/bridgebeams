"""Malaysian JKR PRT, OKA M-beam and G-CAST beam sections."""

import numpy as np
import pytest

from bridgebeams.my.gcast_beams import (
    GcastIBeamSection,
    GcastTBeamSection,
    GcastTmBeamSection,
    GcastUBeamSection,
)
from bridgebeams.my.jkr_prt import JkrPrtBeamSection
from bridgebeams.my.oka_m_beam import OkaMBeamSection

from _aggregate import P, run_checks

CLASSES = [JkrPrtBeamSection, OkaMBeamSection, GcastUBeamSection, GcastTmBeamSection, GcastIBeamSection, GcastTBeamSection]
PROVENANCE = {"transcribed", "transcribed-with-convention", "fitted-reconstruction", "estimate"}


def props(poly):
    pts = np.asarray(poly.exterior.coords)[:-1]
    x, y = pts[:, 0], pts[:, 1]
    x2, y2 = np.roll(x, -1), np.roll(y, -1)
    cr = x * y2 - x2 * y
    a = cr.sum() / 2
    cy = ((y + y2) * cr).sum() / (6 * a)
    i0 = ((y * y + y * y2 + y2 * y2) * cr).sum() / 12
    return abs(a), cy, abs(i0) - abs(a) * cy * cy


def _check_all_sizes_valid(cls):
    for s in cls.SIZES:
        sec = cls(s)
        p = sec.polygon
        assert p.is_valid and p.exterior.is_ccw
        minx, miny, maxx, maxy = p.bounds
        assert miny == pytest.approx(0) and minx == pytest.approx(-maxx)
        assert maxy == pytest.approx(sec.published["depth"])
        assert sec.provenance in PROVENANCE and sec.source_status
        assert sec.geometry is not None


def _check_invalid_size(cls):
    with pytest.raises(ValueError):
        cls("nope")


def _check_prt_exact_areas_and_hw():
    for s in JkrPrtBeamSection.SIZES:
        sec = JkrPrtBeamSection(s)
        assert sec.dimensions.web_depth == sec.published["printed_hw"]
        pub = sec.published
        if pub.get("area"):
            a, cy, i = props(sec.polygon)
            assert a == pytest.approx(pub["area"], abs=1)
            assert cy == pytest.approx(pub["yb"], abs=0.5)  # table rounds to 1 mm
            assert i == pytest.approx(pub["ixx"], rel=1e-3)  # table gives 3 s.f.
    # PRT-M: printed area-range endpoints close exactly
    assert JkrPrtBeamSection("PRT-M1450").polygon.area == pytest.approx(518350)
    assert JkrPrtBeamSection("PRT-M1800").polygon.area == pytest.approx(623350)
    assert JkrPrtBeamSection("PRT1").polygon.bounds[2] == 400


def _check_oka_m_properties():
    # Systematic -500 mm2 (chamfer/lean likely ignored by the table): 0.2 % tol.
    for s in OkaMBeamSection.SIZES:
        sec = OkaMBeamSection(s)
        p = sec.published
        a, cy, i = props(sec.polygon)
        if s != "M10":
            assert a - p["area"] == pytest.approx(-500, abs=1)
        assert cy == pytest.approx(p["yb"], abs=1.5)
        assert i == pytest.approx(p["ixx"], rel=6e-3)
    # Pinned source discrepancy: printed M10 area is 300 mm2 below the
    # constant 32000 mm2 per 80 mm pattern (M9 + 32000 = 457450).
    a10 = OkaMBeamSection("M10").polygon.area
    assert a10 - 457150 == pytest.approx(-200, abs=1)
    assert OkaMBeamSection("M9").published["area"] + 32000 == 457450


def _check_gcast_u_fit():
    for s in GcastUBeamSection.SIZES:
        sec = GcastUBeamSection(s)
        p = sec.published
        a, cy, i = props(sec.polygon)
        assert a == pytest.approx(p["area"], rel=1.5e-3)
        assert cy == pytest.approx(p["yb"], abs=0.5)
        assert i == pytest.approx(p["ixx"], rel=3e-3)
    # printed chain: top block 325 wide, floor valley at 150 mm
    d = GcastUBeamSection("U12").dimensions
    assert d.outer_ledge + d.strip + d.inner_ledge == 325
    assert d.valley_height == 150 and d.toe_height == 355


def _check_gcast_tm_estimate():
    for s in GcastTmBeamSection.SIZES:
        sec = GcastTmBeamSection(s)
        p = sec.published
        a, cy, i = props(sec.polygon)
        assert sec.polygon.bounds[2] * 2 == pytest.approx(p["flange_width"])
        assert a == pytest.approx(p["area"], rel=2e-3)
        assert cy == pytest.approx(p["yb"], abs=2.0)
        assert i == pytest.approx(p["ixx"], rel=5e-3)


def _check_gcast_i_and_t():
    sec = GcastIBeamSection()
    a, cy, i = props(sec.polygon)
    assert a == pytest.approx(645144, rel=1e-3)
    assert cy == pytest.approx(803, abs=0.5)
    assert i == pytest.approx(211.9e9, rel=1e-3)
    t = GcastTBeamSection()
    a, cy, i = props(t.polygon)
    assert t.polygon.bounds[3] == 1800
    assert a == pytest.approx(757115, rel=1e-3)
    assert cy == pytest.approx(944, abs=1)
    assert i == pytest.approx(311.46e9, rel=2e-3)


def test_my_beams_catalogue_checks():
    run_checks(
        (_check_all_sizes_valid, P("cls", CLASSES)),
        (_check_invalid_size, P("cls", CLASSES)),
        _check_prt_exact_areas_and_hw,
        _check_oka_m_properties,
        _check_gcast_u_fit,
        _check_gcast_tm_estimate,
        _check_gcast_i_and_t,
    )


def test_oka_m10_area_discrepancy_pinned():
    """Printed M10 area breaks the 32000 mm2 per 80 mm pattern (inside the OKA M check)."""
    run_checks(_check_oka_m_properties)
