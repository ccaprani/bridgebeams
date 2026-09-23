"""Bulgarian girders: Rila ГТ 75…185 and ZBE MG75 (printed cm chains)."""

import pytest
from shapely.geometry import LineString

from bridgebeams.bg.rila_gt import RilaGtSection
from bridgebeams.bg.zbe_mg import ZbeMgSection


def width_at(poly, y):
    return poly.intersection(LineString([(-5000, y), (5000, y)])).length


def edge_height(poly, x):
    return poly.intersection(LineString([(x, -1), (x, 5000)])).bounds[3]


# size: top width, web, bottom width, left/right edge heights, centre height (mm)
RILA = {
    "GT75": (1120, 180, 700, 750, 750, 750),
    "GT95": (1120, 180, 700, 936, 964, 950),
    "GT115": (1120, 180, 700, 1164, 1136, 1150),
    "GT140": (1200, 180, 700, 1385, 1415, 1400),
    "GT185": (1800, 200, 700, 1835, 1875, 1850),
}


@pytest.mark.parametrize("size", RilaGtSection.SIZES)
def test_rila_printed(size):
    sec = RilaGtSection(size)
    p = sec.polygon
    top, web, bot, hl, hr, hc = RILA[size]
    assert p.is_valid and p.exterior.is_ccw
    b = p.bounds
    assert (b[0], b[2]) == pytest.approx((-top / 2, top / 2))
    assert b[1] == 0
    assert edge_height(p, -top / 2 + 1e-6) == pytest.approx(hl, abs=0.01)
    assert edge_height(p, top / 2 - 1e-6) == pytest.approx(hr, abs=0.01)
    assert width_at(p, sec.dimensions.web_top - 100) == pytest.approx(web)
    assert width_at(p, sec.dimensions.flange_side_top - 1) == pytest.approx(bot)
    # soffit = bottom width - 2 chamfers
    assert width_at(p, 0.001) == pytest.approx(bot - 2 * sec.dimensions.chamfer, abs=0.01)
    assert sec.provenance in ("transcribed", "transcribed-with-convention")
    assert sec.geometry is not None
    # printed centre height = mean of the edge heights, except GT185 (pinned below)
    if size not in ("GT75", "GT185"):
        assert hc == sec.published["centre"] * 10
        assert (hl + hr) / 2 == pytest.approx(hc, abs=0.01)


def test_rila_gt185_centre_pinned():
    # Printed nominal 185 at the axis, but the printed edge heights 183.5 / 187.5 average 185.5.
    sec = RilaGtSection("GT185")
    d = sec.dimensions
    assert sec.published["centre"] == 185
    assert (d.height_left + d.height_right) / 2 == pytest.approx(1855)


def test_rila_gt115_right_chain_pinned():
    # Right chain prints taper 2.8 (sum 113.7) but right total 113.6; total governs.
    sec = RilaGtSection("GT115")
    assert sec.published["right_taper_printed"] == 2.8
    assert sec.dimensions.right[1] == pytest.approx(27.0)
    assert sec.provenance == "transcribed-with-convention"


def test_zbe_mg75():
    sec = ZbeMgSection()
    p = sec.polygon
    assert p.is_valid and p.exterior.is_ccw
    assert (p.bounds[0], p.bounds[2]) == pytest.approx((-550, 550))
    assert edge_height(p, -549.999) == pytest.approx(765, abs=0.01)
    assert edge_height(p, 549.999) == pytest.approx(735, abs=0.01)
    assert (765 + 735) / 2 == sec.dimensions.height_mean
    assert width_at(p, 300) == pytest.approx(180)
    assert width_at(p, 139) == pytest.approx(700)
    assert sec.provenance == "transcribed-with-convention"
    assert sec.geometry is not None


def test_invalid():
    with pytest.raises(ValueError):
        RilaGtSection("GT100")
    with pytest.raises(ValueError):
        ZbeMgSection("MG95")
