"""WSDOT WF, tub, bulb-tee, deck bulb-tee and slab girders vs published properties.

Published values are literal readings of WSDOT BDM M 23-50.24 (June 2025)
Table 5.6.1-1 (PDF p95), the 2006 Table 5.6.1-1 (M 23-50.01, PDF p306)
and the W35DG worked example (Appendix 5-B8, PDF p737); they are repeated
here rather than read from the package JSON.
"""

import math

import pytest
from shapely.affinity import scale

from bridgebeams.us.wsdot_legacy_girders import (
    WsdotBulbTeeSection,
    WsdotDeckBulbTeeSection,
    WsdotSlabGirderSection,
)
from bridgebeams.us.wsdot_tub_girders import WsdotTubGirderSection
from bridgebeams.us.wsdot_wf_girders import WsdotWfGirderSection

IN = 25.4
ALL_CLASSES = (
    WsdotWfGirderSection,
    WsdotTubGirderSection,
    WsdotBulbTeeSection,
    WsdotDeckBulbTeeSection,
    WsdotSlabGirderSection,
)
PROVENANCE = {"transcribed", "transcribed-with-convention", "fitted-reconstruction", "estimate"}


def _ring(coords):
    pts = list(coords)[:-1]
    a = sx = ixx = iyy = 0.0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
        c = x0 * y1 - x1 * y0
        a += c
        sx += (y0 + y1) * c
        ixx += (y0 * y0 + y0 * y1 + y1 * y1) * c
        iyy += (x0 * x0 + x0 * x1 + x1 * x1) * c
    return a / 2, sx / 6, ixx / 12, iyy / 12


def props_in(poly):
    """Area, yb, Ix (centroidal) and Iy (about x=0) in inches, holes included."""
    a, s, i, j = _ring(poly.exterior.coords)
    for h in poly.interiors:  # interiors are clockwise: signed terms subtract
        da, ds, di, dj = _ring(h.coords)
        a, s, i, j = a + da, s + ds, i + di, j + dj
    cy = s / a
    return a / IN**2, cy / IN, (i - a * cy * cy) / IN**4, j / IN**4


def _check(poly, pub, tol_a=0.05, tol_y=0.005, tol_i=0.5, tol_iy=0.5):
    a, yb, ix, iy = props_in(poly)
    assert a == pytest.approx(pub[0], abs=tol_a)
    assert yb == pytest.approx(pub[1], abs=tol_y)
    assert ix == pytest.approx(pub[2], abs=tol_i)
    if len(pub) > 3:
        assert iy == pytest.approx(pub[3], abs=tol_iy)


# ---------------------------------------------------------------- generic
@pytest.mark.parametrize("cls", ALL_CLASSES)
def test_every_size_builds_valid_ccw_symmetric(cls):
    for size in cls.SIZES:
        s = cls(size)
        poly = s.polygon
        assert poly.is_valid and poly.exterior.is_ccw
        assert all(not r.is_ccw for r in poly.interiors)
        assert poly.bounds[1] == pytest.approx(0.0, abs=1e-9)
        assert poly.symmetric_difference(scale(poly, xfact=-1, origin=(0, 0))).area < 1e-3
        assert s.provenance in PROVENANCE
        assert isinstance(s.source_status, str) and s.source_status
        assert s.geometry is not None


@pytest.mark.parametrize("cls", ALL_CLASSES)
def test_invalid_size_raises(cls):
    with pytest.raises(ValueError):
        cls("NOT-A-SIZE")


# ---------------------------------------------------------------- WF
# 2025 Table 5.6.1-1: depth, A, Yb, Ix, Iy. Printed precision: A 0.05 (0.1
# for 1-decimal rows), Yb 0.005, Ix/Iy 0.5 in^4.
WF_2025 = {
    "WF36G": (36, 690.8, 17.54, 124772, 71291),
    "WF42G": (42, 727.5, 20.36, 183642, 71406),
    "WF50G": (50, 776.5, 24.15, 282559, 71559),
    "WF58G": (58, 825.5, 27.97, 406266, 71712),
    "WF66G": (66, 874.5, 31.80, 556339, 71865),
    "WF74G": (74, 923.5, 35.66, 734356, 72018),
    "WF83G": (82.625, 976.4, 39.83, 959393, 72184),
    "WF95G": (94.5, 1049.1, 45.60, 1328995, 72411),
    "WF100G": (100, 1082.8, 48.27, 1524912, 72516),
    "WF100G-61": (100, 1118.8, 49.89, 1612834, 99849),
}


@pytest.mark.parametrize("size", WF_2025)
def test_wf_matches_2025_table(size):
    depth, *pub = WF_2025[size]
    s = WsdotWfGirderSection(size)
    top = 61 if size.endswith("-61") else 49
    assert s.polygon.bounds == pytest.approx((-top * IN / 2, 0, top * IN / 2, depth * IN))
    assert s.dimensions.web_width == pytest.approx(6.125 * IN)
    _check(s.polygon, pub, tol_a=0.05, tol_y=0.005, tol_i=0.5, tol_iy=0.5)


def test_wf_provenance_split():
    assert WsdotWfGirderSection("WF42G").provenance == "transcribed"
    assert WsdotWfGirderSection("WF66G").provenance == "transcribed-with-convention"
    assert WsdotWfGirderSection("WF100G-61").provenance == "fitted-reconstruction"


def test_2006_table_omits_bottom_chamfers():
    # 2006 Table 5.6.1-1 WF42G: A 728.5, Iz 184042.9, Yb 20.33 = outline + 2 x 0.5 in^2 chamfers.
    a, yb, ix, _ = props_in(WsdotWfGirderSection("WF42G").polygon)
    chamfer = 2 * 0.5
    a0 = a + chamfer
    yb0 = (a * yb + chamfer * (1 / 3)) / a0
    ix0 = ix + a * (yb - yb0) ** 2 + chamfer * (yb0 - 1 / 3) ** 2
    assert a0 == pytest.approx(728.5, abs=0.05)
    assert yb0 == pytest.approx(20.33, abs=0.005)
    assert ix0 == pytest.approx(184042.9, abs=2)


# ---------------------------------------------------------------- tubs
TUB_2025 = {
    "U54G4": (1038.8, 20.97, 292423, 493926),
    "U54G5": (1110.8, 19.81, 314382, 788289),
    "U66G4": (1208.5, 26.45, 516677, 637751),
    "U66G5": (1280.5, 25.13, 554262, 997354),
    "U78G4": (1378.2, 32.06, 827453, 798969),
    "U78G5": (1450.2, 30.62, 885451, 1227303),
    "UF60G4": (1207.7, 26.03, 483298, 639795),
    "UF60G5": (1279.7, 24.74, 519561, 999184),
    "UF72G4": (1377.4, 31.69, 787605, 800958),
    "UF72G5": (1449.4, 30.26, 844135, 1229061),
}
TUB_2006_ONLY = {  # UF84 dropped by 2025; 2006 table has no Iy
    "UF84G4": (1547.1, 37.42, 1190828),
    "UF84G5": (1619.1, 35.89, 1272553),
}
TUB_G6_2006 = {
    "U54G6": (1254.8, 18.16, 341728),
    "U66G6": (1424.5, 23.15, 605412),
    "U78G6": (1594.2, 28.35, 969347),
    "UF60G6": (1423.7, 22.79, 568717),
    "UF72G6": (1593.4, 28.03, 925720),
    "UF84G6": (1763.1, 33.41, 1395939),
}


@pytest.mark.parametrize("size", TUB_2025)
def test_tub_g4_g5_match_2025_table(size):
    _check(WsdotTubGirderSection(size).polygon, TUB_2025[size], tol_a=0.05, tol_y=0.005, tol_i=0.5, tol_iy=0.5)


@pytest.mark.parametrize("size", TUB_2006_ONLY)
def test_uf84_matches_2006_table(size):
    _check(WsdotTubGirderSection(size).polygon, TUB_2006_ONLY[size], tol_a=0.05, tol_y=0.005, tol_i=0.5)


@pytest.mark.parametrize("size", TUB_G6_2006)
def test_g6_drawn_outline_is_36in2_short_of_2006_table(size):
    """Pinned discrepancy: drawn 1'-6" fillet run vs 2006 table (2'-0" run fits)."""
    s = WsdotTubGirderSection(size)
    assert s.provenance == "transcribed-with-convention"
    assert s.dimensions.fillet_run == pytest.approx(18 * IN)
    a, *_ = props_in(s.polygon)
    assert a - TUB_G6_2006[size][0] == pytest.approx(-36.0, abs=0.05)


def test_tub_geometry_callouts():
    s = WsdotTubGirderSection("U54G4")
    minx, miny, maxx, maxy = s.polygon.bounds
    assert maxy == pytest.approx(54 * IN)
    assert maxx == pytest.approx((24 + 54 / 7) * IN)  # 1:7 web from 4'-0" base
    uf = WsdotTubGirderSection("UF60G4").polygon
    block = uf.bounds[2] - (24 + (60 - 6) / 7 - 7 * math.sqrt(50) / 7 - 3) * IN
    assert block / IN == pytest.approx(15.0625, abs=0.01)  # printed 1'-3 1/16"


# ---------------------------------------------------------------- bulb tees
BTG_2006 = {"W32BTG": (538.0, 17.88, 74039), "W38BTG": (574.0, 21.08, 114540), "W62BTG": (718.0, 33.68, 385995)}


@pytest.mark.parametrize("size", BTG_2006)
def test_btg_pinned_residual_vs_2006_table(size):
    """Drawn outline is exactly +4.0 in^2 over the 2006 table (unexplained)."""
    a, yb, ix, _ = props_in(WsdotBulbTeeSection(size).polygon)
    pa, pyb, pix = BTG_2006[size]
    assert a - pa == pytest.approx(4.0, abs=0.05)
    assert 0.09 < yb - pyb < 0.21
    assert 0 < (ix - pix) / pix < 0.004


def test_wfbtg_flange_width_parameter():
    s = WsdotBulbTeeSection("WF50BTG")
    assert s.provenance == "estimate"
    assert s.polygon.bounds[2] == pytest.approx(36 * IN)
    wide = WsdotBulbTeeSection("WF50BTG", top_flange_width_in=96)
    assert wide.polygon.bounds[2] == pytest.approx(48 * IN)
    narrow = WsdotBulbTeeSection("WF50BTG", top_flange_width_in=48)
    assert narrow.polygon.is_valid
    with pytest.raises(ValueError):
        WsdotBulbTeeSection("WF50BTG", top_flange_width_in=100)
    with pytest.raises(ValueError):
        WsdotBulbTeeSection("W32BTG", top_flange_width_in=60)


# ---------------------------------------------------------------- deck bulb tees
def test_w35dg_vs_worked_example_pinned():
    """App. 5-B8: A 669, yb 20.9, I 100096, Ip 169341 (Iy 69245) at 48 in."""
    s = WsdotDeckBulbTeeSection("W35DG")
    assert s.dimensions.spacing == pytest.approx(48 * IN)
    assert s.polygon.bounds[2] == pytest.approx(23.8125 * IN)  # bottom lip, 3/16" from joint
    a, yb, ix, iy = props_in(s.polygon)
    assert (a - 669) / 669 == pytest.approx(-0.00571, abs=0.0005)
    assert yb - 20.9 == pytest.approx(0.052, abs=0.005)
    assert (ix - 100096) / 100096 == pytest.approx(-0.00518, abs=0.0005)
    assert (iy - 69245) / 69245 == pytest.approx(-0.0338, abs=0.001)


def test_dg_spacing_range():
    w = WsdotDeckBulbTeeSection("W65DG", spacing_in=72)
    assert w.polygon.is_valid
    assert w.polygon.bounds[3] == pytest.approx(65 * IN)
    with pytest.raises(ValueError):
        WsdotDeckBulbTeeSection("W65DG", spacing_in=80)


# ---------------------------------------------------------------- slabs
SLAB_2025 = {
    "SLAB12x48": (564, 6.0, 6768),
    "SLAB18x48": (655, 9.0, 21876),
    "SLAB24x48": (741, 12.0, 48179),
    "SLAB26x48": (835, 13.0, 62874),
    "SLAB30x52": (1021, 15.0, 104444),
}


@pytest.mark.parametrize("size", SLAB_2025)
def test_slabs_match_2025_table(size):
    # Table prints integer areas and inertias; voids are 256-gons (<0.02%).
    s = WsdotSlabGirderSection(size)
    _check(s.polygon, SLAB_2025[size], tol_a=0.5, tol_y=0.005, tol_i=max(0.5, 3e-5 * SLAB_2025[size][2]))


def test_slab_voids_are_interiors():
    assert len(WsdotSlabGirderSection("SLAB18x48").polygon.interiors) == 3
    assert len(WsdotSlabGirderSection("SLAB12x48").polygon.interiors) == 0
