"""Haitsma HKP (folder edition), HBM-450/550 and HGR-500."""

import numpy as np
import pytest
from shapely.geometry import LineString

from bridgebeams.nl.r2_haitsma import HaitsmaHbmSection, HaitsmaHgrSection, HaitsmaHkpSection

from _aggregate import P, run_checks


def props_with_holes(poly):
    def ring(coords):
        c = np.asarray(coords)[:-1]
        x, y = c[:, 0], c[:, 1]
        x2, y2 = np.roll(x, -1), np.roll(y, -1)
        cr = x * y2 - x2 * y
        return cr.sum() / 2, ((y + y2) * cr).sum() / 6, ((y * y + y * y2 + y2 * y2) * cr).sum() / 12
    a, s, i = ring(poly.exterior.coords)
    for r in poly.interiors:
        da, ds, di = ring(r.coords)
        a, s, i = a + da, s + ds, i + di
    cy = s / a
    return a, cy, i - a * cy * cy


def _check_hkp_matches_folder_table(size):
    sec = HaitsmaHkpSection(size)
    p = sec.polygon
    assert p.is_valid and p.exterior.is_ccw and len(p.interiors) == 1
    assert p.bounds == pytest.approx((-740, 0, 740, sec.dimensions.depth))
    a, cy, i = props_with_holes(p)
    pub = sec.published
    # table: A to 3 s.f. of 1e5 (±500 mm2 rounding) plus 0.1 % convention allowance
    assert a == pytest.approx(pub["A_1e5mm2"] * 1e5, rel=1e-3)
    assert cy == pytest.approx(pub["v_mm"], abs=1.0)
    assert i == pytest.approx(pub["I_1e9mm4"] * 1e9, rel=1.5e-3)
    assert sec.provenance == "transcribed-with-convention"
    assert sec.geometry is not None


def _check_hkp_web_thickness():
    p = HaitsmaHkpSection("HKP-1000").polygon
    cut = p.intersection(LineString([(-800, 500), (800, 500)]))
    assert cut.length == pytest.approx(280.0)


def _check_hbm_printed(size, depth, top, bottom):
    sec = HaitsmaHbmSection(size)
    p = sec.polygon
    assert p.is_valid and p.exterior.is_ccw
    assert p.bounds[3] == depth
    top_edge = p.intersection(LineString([(-900, depth), (900, depth)]))
    assert top_edge.length == pytest.approx(top)
    assert p.intersection(LineString([(-900, 0), (900, 0)])).length == pytest.approx(bottom)
    assert sec.provenance == "transcribed"


def test_hbm_folder_table_conflict_pinned():
    # Folder 'HUP' table Ab = 2.75e5 mm2 for 450 cannot be the drawn solid section.
    a = HaitsmaHbmSection("HBM-450").polygon.area
    assert a > 4.5e5 and HaitsmaHbmSection("HBM-450").published[1] == 2.75


def _check_hgr():
    sec = HaitsmaHgrSection()
    p = sec.polygon
    assert p.is_valid and p.exterior.is_ccw
    assert p.bounds[1] == 0 and p.bounds[3] == pytest.approx(765.5)
    assert p.intersection(LineString([(-900, 0), (900, 0)])).length == pytest.approx(485)
    assert sec.geometry is not None


def _check_invalid():
    for cls, bad in ((HaitsmaHkpSection, "HKP-1500"), (HaitsmaHbmSection, "HBM-350"), (HaitsmaHgrSection, "HGR-600")):
        with pytest.raises(ValueError):
            cls(bad)


def test_nl_r2_haitsma_catalogue_checks():
    run_checks(
        (_check_hkp_matches_folder_table, P("size", HaitsmaHkpSection.SIZES)),
        _check_hkp_web_thickness,
        (_check_hbm_printed, P("size,depth,top,bottom", [("HBM-450", 450, 1150, 400), ("HBM-550", 550, 1156, 400)])),
        _check_hgr,
        _check_invalid,
    )
