"""Pakistan NHA standard Types A-H and Lahore-Sialkot Motorway project girders."""

import pytest

from bridgebeams._geometry import section_properties
from bridgebeams.pk.nha_i_girders import LsmPscIGirderSection, NhaStandardIGirderSection

from _aggregate import P, run_checks

# Table 1, Mustafa & Javed (2025), PDF p2: (H, B1, B2, B3, D1..D5)
NHA_TABLE = {
    "A": (1200, 550, 180, 550, 250, 90, 475, 185, 200),
    "B": (1400, 550, 180, 550, 250, 90, 675, 185, 200),
    "C": (1600, 600, 180, 600, 250, 100, 750, 210, 290),
    "D": (1800, 700, 180, 600, 230, 130, 940, 210, 290),
    "E": (2000, 700, 180, 600, 230, 130, 1140, 210, 290),
    "F": (2200, 900, 190, 620, 200, 175, 1310, 215, 300),
    "G": (2400, 1000, 190, 650, 185, 200, 1485, 230, 300),
    "H": (2600, 1100, 190, 750, 170, 225, 1625, 280, 300),
}

# LSM drawings: (H, top, web, bottom, top_edge, top_splay, web, bottom_splay, bottom_edge)
LSM = {
    "20m": (1600, 800, 200, 600, 150, 150, 860, 200, 240),
    "30m": (2000, 900, 200, 600, 170, 170, 1170, 200, 290),
    "45m": (2750, 1100, 210, 750, 220, 200, 1650, 280, 400),
}


def _analytic(h, t, w, b, e1, s1, hw, s2, e2):
    area = t * e1 + (t + w) / 2 * s1 + w * hw + (b + w) / 2 * s2 + b * e2
    # first moment about the soffit, trapezoid by trapezoid
    parts = [
        (b * e2, e2 / 2),
        ((b + w) / 2 * s2, e2 + s2 * (b + 2 * w) / (3 * (b + w))),
        (w * hw, e2 + s2 + hw / 2),
        ((t + w) / 2 * s1, e2 + s2 + hw + s1 * (w + 2 * t) / (3 * (t + w))),
        (t * e1, h - e1 / 2),
    ]
    return area, sum(a * y for a, y in parts) / area


def _check_nha_types(size):
    sec = NhaStandardIGirderSection(size)
    h, b1, b2, b3, d1, d2, d3, d4, d5 = NHA_TABLE[size]
    assert d1 + d2 + d3 + d4 + d5 == h
    poly = sec.polygon
    assert poly.is_valid and poly.exterior.is_ccw
    minx, miny, maxx, maxy = poly.bounds
    assert (miny, maxy) == (0.0, h)
    assert maxx - minx == pytest.approx(max(b1, b3))
    props = section_properties(poly)
    area, yb = _analytic(h, b1, b2, b3, d1, d2, d3, d4, d5)
    assert props["area"] == pytest.approx(area, rel=1e-12)
    assert props["cy"] == pytest.approx(yb, rel=1e-12)
    assert sec.provenance == "transcribed"
    assert "NHA" in sec.source_status


def _check_nha_physical_widths():
    sec = NhaStandardIGirderSection("H")
    pts = list(sec.polygon.exterior.coords)
    top = sorted(x for x, y in pts if y == 2600)
    bot = sorted(x for x, y in pts if y == 0)
    assert top[-1] - top[0] == 1100
    assert bot[-1] - bot[0] == 750
    assert sec.span_range_m == "32-40"
    assert NhaStandardIGirderSection("A").span_range_m == "12-20"


def _check_lsm_sizes(size):
    sec = LsmPscIGirderSection(size)
    h, t, w, b, *_ = LSM[size]
    poly = sec.polygon
    assert poly.is_valid and poly.exterior.is_ccw
    assert poly.bounds[3] == h
    props = section_properties(poly)
    area, yb = _analytic(*LSM[size])
    assert props["area"] == pytest.approx(area, rel=1e-12)
    assert props["cy"] == pytest.approx(yb, rel=1e-12)
    assert sec.provenance == "transcribed"
    assert sec.drawing.startswith("LSM-EBP-BR-ST-")


def _check_lsm_30m_known_area():
    # 900x170 + (900+200)/2*170 + 200*1170 + (600+200)/2*200 + 600*290
    assert section_properties(LsmPscIGirderSection("30m").polygon)["area"] == pytest.approx(
        153000 + 93500 + 234000 + 80000 + 174000
    )


def _check_lsm_differs_from_nha_type_e():
    lsm = LsmPscIGirderSection("30m").dimensions
    nha = NhaStandardIGirderSection("E").dimensions
    assert lsm.depth == nha.depth == 2000
    assert (lsm.top_width, lsm.web_width) != (nha.top_width, nha.web_width)


def _check_invalid_size(cls):
    with pytest.raises(ValueError):
        cls("Z")


def test_pk_nha_i_girders_catalogue_checks():
    run_checks(
        (_check_nha_types, P("size", NhaStandardIGirderSection.SIZES)),
        _check_nha_physical_widths,
        (_check_lsm_sizes, P("size", LsmPscIGirderSection.SIZES)),
        _check_lsm_30m_known_area,
        _check_lsm_differs_from_nha_type_e,
        (_check_invalid_size, P("cls", [NhaStandardIGirderSection, LsmPscIGirderSection])),
    )
