"""Civilcon T, U, Special U and M sections against the PPBT/PPBU/PPBUS/PPBM sheets."""
import pytest
from shapely.geometry import LineString

from bridgebeams._geometry import section_properties
from bridgebeams.za.civilcon_m_beam import CivilconMBeamSection
from bridgebeams.za.civilcon_special_u_beam import CivilconSpecialUBeamSection
from bridgebeams.za.civilcon_t_beam import CivilconTBeamSection
from bridgebeams.za.civilcon_u_beam import CivilconUBeamSection

from _aggregate import P, run_checks


def _width(p, y):
    return p.intersection(LineString([(-5000, y), (5000, y)])).length


def _props(section):
    p = section.polygon
    assert p.is_valid
    assert p.exterior.is_ccw
    assert len(p.interiors) == 0
    pr = section_properties(p)
    h = p.bounds[3]
    assert pr["cx"] == pytest.approx(0, abs=1e-9)
    assert section.geometry.geom.symmetric_difference(p).area < 1e-3
    return pr, h, pr["ixx"] / (h - pr["cy"]), pr["ixx"] / pr["cy"]


# ---------------------------------------------------------------- T beams
T_ROWS = [
    ("T1", 380, 97385, 139, 5.11e6, 8.85e6),
    ("T2", 420, 105585, 159, 6.69e6, 10.98e6),
    ("T3", 535, 114160, 196, 9.61e6, 16.54e6),
    ("T4", 575, 122360, 220, 11.92e6, 19.22e6),
    ("T5", 615, 130560, 244, 14.31e6, 21.76e6),
    ("T6", 655, 138760, 267, 16.73e6, 24.32e6),
    ("T7", 695, 146960, 290, 19.22e6, 26.84e6),
    ("T8", 735, 155160, 312, 21.72e6, 29.45e6),
    ("T9", 775, 163360, 334, 24.31e6, 32.09e6),
    ("T10", 815, 171560, 356, 26.96e6, 34.48e6),
]


def _check_t_beam(size, h, area, yb, zt, zb):
    s = CivilconTBeamSection(size)
    assert s.provenance == "transcribed-with-convention"
    assert s.source_status == "producer catalogue"
    pr, depth, zt_c, zb_c = _props(s)
    p = s.polygon
    assert p.bounds == (-247.5, 0.0, 247.5, float(h))
    assert _width(p, 0) == pytest.approx(445)
    assert _width(p, 25) == pytest.approx(495)
    assert _width(p, 100) == pytest.approx(483)
    assert _width(p, 140) == pytest.approx(205)  # derived break width
    assert _width(p, 250) == pytest.approx(105)
    assert _width(p, h - 1) == pytest.approx(205)
    # Area closes exactly with the derived 205 mm break width.
    assert pr["area"] == pytest.approx(area, abs=0.5)
    assert pr["cy"] == pytest.approx(yb, abs=0.5)  # Yb printed to 1 mm
    # Rounded 3-figure moduli: max otherwise 0.43% (T3 Zt).
    assert zt_c == pytest.approx(zt, rel=0.0045)
    if size == "T10":
        # Literal source discrepancy: published Zb is 0.732% below the outline.
        assert zb_c / zb - 1 == pytest.approx(0.00732, abs=5e-5)
    else:
        assert zb_c == pytest.approx(zb, rel=0.0045)


def test_t10_uses_table_depth_not_850_label():
    s = CivilconTBeamSection("T10")
    assert s.published["drawing_depth_label"] == 850
    assert s.dimensions.depth == 815
    assert s.dimensions.depth - 480 == 335  # "335 max" above the upper splay


# ---------------------------------------------------------------- U beams
U_ROWS = [
    ("U1", 800, 476970, 356.5, 68.9e6, 85.71e6),
    ("U3", 900, 510493, 403, 85.84e6, 105.81e6),
    ("U5", 1000, 544016, 450, 104.18e6, 127.28e6),
    ("U7", 1100, 577539, 497.5, 123.86e6, 150.06e6),
    ("U8", 1200, 611062, 545, 144.86e6, 174.04e6),
    ("U9", 1300, 644584, 593, 167.08e6, 199.27e6),
    ("U10", 1400, 678107, 641, 190.57e6, 255.65e6),
    ("U11", 1500, 711630, 689, 215.27e6, 253.18e6),
    ("U12", 1600, 745153, 737.7, 241.16e6, 281.9e6),
]


def _check_u_beam(size, h, area, yb, zt, zb):
    s = CivilconUBeamSection(size)
    assert s.provenance == "fitted-reconstruction"
    pr, depth, zt_c, zb_c = _props(s)
    p = s.polygon
    assert depth == h
    d = s.dimensions
    top_outer = 485 + (h - 30) / 6.75
    assert p.bounds[2] == pytest.approx(top_outer)
    # Raised 250 strip on each web at the top face.
    assert _width(p, h - 1) == pytest.approx(500)
    assert _width(p, 20) == pytest.approx(2 * (455.185 + 20), abs=0.01)  # 35x35 chamfer
    # Floor centre is the fitted valley (not printed).
    assert p.intersection(LineString([(0, 0), (0, 5000)])).length == pytest.approx(d.valley_height)
    # Web toe at printed 240 + 129 = 369 on the inner web face.
    assert d.toe[0] == 369 and d.toe[1] == pytest.approx(342.9, abs=0.05)
    # Fitted floor: area trend from web-width mismatch, max 0.11%.
    assert pr["area"] == pytest.approx(area, rel=0.0012)
    assert pr["cy"] == pytest.approx(yb, abs=0.3)
    assert zt_c == pytest.approx(zt, rel=0.0007)
    if size == "U10":
        # Printed Zb 255.65e6 contradicts its own Zt/Yb; outline gives 225.7e6.
        assert zb_c / zb - 1 == pytest.approx(-0.11705, abs=5e-5)
        assert zb_c == pytest.approx(225.65e6, rel=0.0005)
    else:
        assert zb_c == pytest.approx(zb, rel=0.0005)


def test_u_area_increment_pinned():
    # Published steps are exactly 33523 per 100 mm (167.6 mm web); printed
    # 165 normal at 6.75:1 gives 2*166.80*100.
    a = [section_properties(CivilconUBeamSection(k).polygon)["area"] for k in ("U1", "U3")]
    assert a[1] - a[0] == pytest.approx(2 * 165 * (1 + 1 / 6.75**2) ** 0.5 * 100)
    assert 510493 - 476970 == 33523


# ------------------------------------------------------- Special U beams
def _check_special_u_beam(size, h, area, yb, zt, zb):
    s = CivilconSpecialUBeamSection(size)
    assert s.provenance == "fitted-reconstruction"
    pr, depth, zt_c, zb_c = _props(s)
    p = s.polygon
    assert depth == h
    assert _width(p, 0) == pytest.approx(2000)
    assert p.bounds[0] == pytest.approx(-(1000 + (h - 300) / 7.2 + 75))
    # Lobes: 200 raised strip each; 350 wide below the shoulders.
    assert _width(p, h - 1) == pytest.approx(400)
    assert _width(p, h - 100) == pytest.approx(700)
    # Web horizontal width 60 + 80 + 60 = 200 each side.
    assert _width(p, 500) == pytest.approx(400)
    assert p.intersection(LineString([(0, 0), (0, 5000)])).length == pytest.approx(200)
    assert pr["area"] == pytest.approx(area, rel=0.00015)
    assert pr["cy"] == pytest.approx(yb, abs=0.4)
    assert zt_c == pytest.approx(zt, rel=0.0002)
    assert zb_c == pytest.approx(zb, rel=0.0002)


def test_special_u_su1_lobe_offset_discrepancy():
    # Printed 810 vs web-consistent 808.3: recorded, not forced.
    d = CivilconSpecialUBeamSection("SU1").dimensions
    assert d.inner_x(600) - 75 == pytest.approx(808.33, abs=0.01)


# ---------------------------------------------------------------- M beams
M_ROWS = [
    ("M2", 720, 314600, 266, 35.37e6, 60.36e6),
    ("M3", 800, 346600, 310, 46.6e6, 73.65e6),
    ("M4", 880, 37860, 354, 58.37e6, 86.73e6),
    ("M5", 960, 353000, 357, 58.92e6, 99.52e6),
    ("M6", 1040, 384999, 410, 74.94e6, 115.15e6),
    ("M7", 1120, 417000, 460, 90.95e6, 130.49e6),
    ("M8", 1200, 391399, 455, 87.87e6, 142.23e6),
    ("M9", 1280, 423399, 513, 107.45e6, 160.66e6),
    ("M10", 1360, 455399, 569, 127.97e6, 177.9e6),
]


def _check_m_beam(size, h, area, yb, zt, zb):
    s = CivilconMBeamSection(size)
    assert s.provenance == "fitted-reconstruction"
    pr, depth, zt_c, zb_c = _props(s)
    p = s.polygon
    assert p.bounds == (-485.0, 0.0, 485.0, float(h))
    assert _width(p, 0) == pytest.approx(900)
    assert _width(p, 35) == pytest.approx(970)
    assert _width(p, 250) == pytest.approx(240)  # 45 deg splay
    assert _width(p, 300) == pytest.approx(160)
    assert _width(p, h - 60) == pytest.approx(400)
    assert _width(p, h - 1) == pytest.approx(300)
    if size == "M4":
        # Printed 37860 is a dropped digit; 378600 closes exactly.
        assert pr["area"] == pytest.approx(10 * area, abs=1)
    else:
        assert pr["area"] == pytest.approx(area, abs=1.5)
    assert pr["cy"] == pytest.approx(yb, abs=0.45)
    if size == "M8":
        # Published Zt is inconsistent with its own Zb/Yb (1.16%).
        assert zt_c / zt - 1 == pytest.approx(-0.01188, abs=5e-5)
    else:
        assert zt_c == pytest.approx(zt, rel=0.0008)
    assert zb_c == pytest.approx(zb, rel=0.0013)


def test_m10_uses_drawing_depth():
    s = CivilconMBeamSection("M10")
    assert s.published["published_depth"] == 360
    assert s.dimensions.depth == 1360


def _check_invalid_size(cls, bad):
    with pytest.raises(ValueError):
        cls(bad)


def test_za_civilcon_tum_catalogue_checks():
    run_checks(
        (_check_t_beam, P("size,h,area,yb,zt,zb", T_ROWS)),
        (_check_u_beam, P("size,h,area,yb,zt,zb", U_ROWS)),
        (_check_special_u_beam, P("size,h,area,yb,zt,zb", [
    ("SU1", 900, 764590, 320, 100.76e6, 182.96e6),
    ("SU2", 1200, 884590, 439, 172.96e6, 299.73e6),
])),
        (_check_m_beam, P("size,h,area,yb,zt,zb", M_ROWS)),
        (_check_invalid_size, P("cls,bad", [
    (CivilconTBeamSection, "T11"),
    (CivilconUBeamSection, "U2"),
    (CivilconSpecialUBeamSection, "US1"),
    (CivilconMBeamSection, "M1"),
])),
    )
