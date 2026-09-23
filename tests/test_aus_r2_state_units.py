"""Queensland TMR deck units and TfNSW CBS double-T modules (round 2)."""

import pytest
from shapely.geometry import LineString

from bridgebeams.aus.r2_tfnsw_cbs_modules import TfnswCbsModuleSection
from bridgebeams.aus.r2_tmr_deck_units import TmrDeckUnitSection

from _aggregate import P, run_checks

S = 17.6  # printed web batter


def _width(poly, y):
    return poly.intersection(LineString([(-5000, y), (5000, y)])).length


def _props_with_holes(poly):
    """Area and centroidal Ixx including interiors (shoelace)."""
    def ring(coords):
        a = sy = iy = 0.0
        pts = list(coords)
        for (x1, y1), (x2, y2) in zip(pts[:-1], pts[1:]):
            c = x1 * y2 - x2 * y1
            a += c / 2
            sy += (y1 + y2) * c / 6
            iy += (y1 * y1 + y1 * y2 + y2 * y2) * c / 12
        return a, sy, iy
    a, sy, iy = ring(poly.exterior.coords)
    for h in poly.interiors:
        ha, hsy, hiy = ring(h.coords)
        a += ha; sy += hsy; iy += hiy
    cy = sy / a
    return a, cy, iy - a * cy * cy


# --- TMR deck units ---------------------------------------------------

def _check_tmr_area_and_chain(size, depth, void_h):
    sec = TmrDeckUnitSection(size)
    p = sec.polygon
    assert p.is_valid and p.exterior.is_ccw
    assert p.bounds == (-298, 0, 298, depth)
    assert len(p.interiors) == (1 if void_h else 0)
    # Printed: 596 wide, 25x25 soffit chamfers, void 120 side cover,
    # 240 bottom slab, 190 top slab, 75x75 void chamfers.
    gross = 596 * depth - 25 ** 2
    void = (356 * void_h - 2 * 75 ** 2) if void_h else 0
    assert p.area == pytest.approx(gross - void)
    a, cy, _ = _props_with_holes(p)
    assert a == pytest.approx(p.area)
    if void_h:
        assert 240 + void_h + 190 == depth
        assert _width(p, 240 + void_h / 2) == pytest.approx(240)
        assert sec.dimensions.void_top_cover == 190
    assert _width(p, 12.5) == pytest.approx(596 - 25)
    assert sec.provenance == "transcribed"
    assert "TMR" in sec.source_status


def _check_tmr_shared_span_profiles():
    assert TmrDeckUnitSection("500").spans_m == (10, 11)
    assert TmrDeckUnitSection("540").spans_m == (12, 13)
    assert TmrDeckUnitSection(1100).spans_m == (25,)
    assert len(TmrDeckUnitSection("760").geometry.geom.interiors) == 1


def _check_tmr_invalid():
    with pytest.raises(ValueError):
        TmrDeckUnitSection("600")


# --- TfNSW CBS modules ------------------------------------------------

def _inner(y):
    return 405 - y / S


def _check_cbs_internal_independent_area():
    p = TfnswCbsModuleSection("T1-internal").polygon
    assert p.is_valid and p.exterior.is_ccw
    assert p.bounds == pytest.approx((-1235, 0, 1235, 600))
    top = 1650 * 160
    band = 2470 * 75 - 75 * 2 * (405 - (365 + 440) / 2 / S) - 4 * 15 ** 2 / 2 + 2 * 20 ** 2 / 2
    web = 320 * 365 + 365 ** 2 / S - 2 * 20 ** 2 / 2 + 40 ** 2 / 2
    assert p.area == pytest.approx(top + band + 2 * web)
    assert p.centroid.x == pytest.approx(0, abs=1e-6)


def _check_cbs_printed_chains():
    p = TfnswCbsModuleSection("T1-internal").polygon
    # 79 / 366 / 760 top chain and 100/320/810 soffit chain
    assert 725 + 365 / S == pytest.approx(825 - 79, abs=0.5)
    assert 2 * _inner(440) == pytest.approx(760, abs=0.3)
    assert (725 + 365 / S) - _inner(440) == pytest.approx(366, abs=0.5)
    assert _width(p, 500) == pytest.approx(1650)


def _check_cbs_external_widths():
    t1 = TfnswCbsModuleSection("T1-external").polygon
    assert t1.bounds == pytest.approx((-825, 0, 1235, 755))
    kerb_face = -525 + 25 * (755 - 700) / 155
    assert _width(t1, 700) == pytest.approx(825 + kerb_face)
    assert _width(t1, 400) == pytest.approx(2060 - 2 * _inner(400))
    t2 = TfnswCbsModuleSection("T2-external").polygon
    assert t2.bounds == pytest.approx((-1175, 0, 1235, 755))
    t3 = TfnswCbsModuleSection("T3-external").polygon
    assert t3.bounds == pytest.approx((-1350, 0, 1070, 755))
    assert _width(t3, 500) == pytest.approx(2420)
    void_half = (_inner(420) + (_inner(440) - 20)) / 2
    # 15x15 chamfers at the kerb bottom and deck tip each cut 5 mm at y=430
    assert _width(t3, 430) == pytest.approx(2420 - 2 * void_half - 2 * 5)
    for s in TfnswCbsModuleSection.SIZES:
        sec = TfnswCbsModuleSection(s)
        assert sec.polygon.is_valid and sec.polygon.exterior.is_ccw
        assert sec.provenance in ("transcribed", "transcribed-with-convention")
        assert sec.geometry is not None


def _check_cbs_mass_increment_consistency():
    # Type 1 internal: 13.1 / 16.4 / 19.7 t for 8/10/12 m sets, 2550 kg/m3.
    # Increment 3.3 t per 2 m -> 0.647 m2 (+/-3 % from 0.1 t rounding).
    implied = 3.3 / 2.0 / 2.55 * 1e6
    area = TfnswCbsModuleSection("T1-internal").polygon.area
    assert area == pytest.approx(implied, rel=0.03)
    assert area / implied - 1 == pytest.approx(-0.0087, abs=0.001)


def _check_cbs_invalid():
    with pytest.raises(ValueError):
        TfnswCbsModuleSection("T4-internal")


def test_aus_r2_state_units_catalogue_checks():
    run_checks(
        (_check_tmr_area_and_chain, P("size,depth,void_h", [
    ("500", 500, 0), ("540", 540, 0), ("650", 650, 220), ("760", 760, 330), ("1100", 1100, 670)])),
        _check_tmr_shared_span_profiles,
        _check_tmr_invalid,
        _check_cbs_internal_independent_area,
        _check_cbs_printed_chains,
        _check_cbs_external_widths,
        _check_cbs_mass_increment_consistency,
        _check_cbs_invalid,
    )
