"""Iowa DOT BDM 5.4.1 (January 2025) A-D and BTB-BTE beams vs print.

Published values are literal readings of Figures 5.4.1.1.1-1/-2.

A-D: the printed A/yb/I equal the drawn section WITHOUT the two 3/4 in
soffit bevels (2 x 0.28125 in2) to print precision. The polygon keeps the
bevels as drawn; this discrepancy is pinned by adding the bevel triangles
back before comparison, and separately by checking the as-drawn deficit.

BTB-BTE: printed values are not mutually consistent (area steps 60.1,
57.0, 58.6 in2 for identical 9 in web increments of 58.5 in2). Residuals
are pinned per size; BTB printed yb 17.14 in is pinned as a probable
source error (computed 16.62 in; the other sizes agree within 0.16 in).
"""

import pytest
from shapely.affinity import scale
from shapely.geometry import Polygon

from bridgebeams.us.state_ia_beams import IaBulbTeeSection, IaIBeamSection

IN = 25.4


def _ring(coords):
    pts = list(coords)[:-1]
    a = s = i = 0.0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
        c = x0 * y1 - x1 * y0
        a += c
        s += (y0 + y1) * c
        i += (y0 * y0 + y0 * y1 + y1 * y1) * c
    return a / 2, s / 6, i / 12


def props_in(polys):
    a = s = i = 0.0
    for p in polys:
        da, ds, di = _ring(p.exterior.coords)
        k = 1 if da > 0 else -1
        a, s, i = a + k * da, s + k * ds, i + k * di
    cy = s / a
    return a / IN**2, cy / IN, (i - a * cy * cy) / IN**4


AD = {"A": (311.5, 14.05, 34082, 32, 17), "B": (382.5, 17.06, 62000, 39, 17),
      "C": (564.5, 20.23, 116354, 45, 20), "D": (638.75, 24.37, 214974, 54, 22)}
BT = {"BTB": (631.7, 17.14, 99980, 36), "BTC": (691.8, 20.74, 178971, 45),
      "BTD": (748.8, 24.64, 285860, 54), "BTE": (807.4, 28.75, 422790, 63)}
# pinned residuals (computed - printed): area in2, yb in, I relative
BT_RESID = {"BTB": (-0.13, -0.515, -0.00097), "BTC": (-1.73, -0.153, -0.00161),
            "BTD": (-0.23, -0.007, -0.00268), "BTE": (-0.33, -0.005, -0.00291)}


@pytest.mark.parametrize("cls", (IaIBeamSection, IaBulbTeeSection))
def test_every_size_valid(cls):
    for size in cls.SIZES:
        s = cls(size)
        p = s.polygon
        assert p.is_valid and p.exterior.is_ccw
        assert p.bounds[1] == pytest.approx(0.0, abs=1e-9)
        assert p.symmetric_difference(scale(p, xfact=-1, origin=(0, 0))).area < 1e-3
        assert s.provenance in {"transcribed", "transcribed-with-convention"}
        assert s.source_status
        assert s.geometry is not None


@pytest.mark.parametrize("cls", (IaIBeamSection, IaBulbTeeSection))
def test_invalid_size(cls):
    with pytest.raises(ValueError):
        cls("BTA")


@pytest.mark.parametrize("size,pub", AD.items())
def test_ad_published_excludes_bevels(size, pub):
    s = IaIBeamSection(size)
    p = s.polygon
    b = pub[4] / 2 * IN
    c = 0.75 * IN
    bevels = [Polygon([(b, 0), (b, c), (b - c, 0)]), Polygon([(-b, 0), (-b + c, 0), (-b, c)])]
    a, yb, ix = props_in([p] + bevels)
    assert p.bounds[3] / IN == pytest.approx(pub[3])
    assert (p.bounds[2] - p.bounds[0]) / IN == pytest.approx(pub[4])
    assert a == pytest.approx(pub[0], abs=0.005)
    assert yb == pytest.approx(pub[1], abs=0.006)
    assert ix == pytest.approx(pub[2], rel=1e-4)
    # as drawn (with bevels) the section is 0.5625 in2 below the printed area
    assert props_in([p])[0] - pub[0] == pytest.approx(-0.5625, abs=0.005)


@pytest.mark.parametrize("size,pub", BT.items())
def test_bt_published_pinned(size, pub):
    s = IaBulbTeeSection(size)
    a, yb, ix = props_in([s.polygon])
    da, dy, di = BT_RESID[size]
    assert s.polygon.bounds[3] / IN == pytest.approx(pub[3])
    assert a - pub[0] == pytest.approx(da, abs=0.02)
    assert yb - pub[1] == pytest.approx(dy, abs=0.003)
    assert ix / pub[2] - 1 == pytest.approx(di, abs=2e-5)
    # family-level envelope, excluding the pinned BTB yb
    assert abs(a / pub[0] - 1) < 0.003
    assert abs(ix / pub[2] - 1) < 0.003
    if size != "BTB":
        assert abs(yb - pub[1]) < 0.16


def test_bt_widths():
    p = IaBulbTeeSection("BTD").polygon
    assert (p.bounds[2] - p.bounds[0]) / IN == pytest.approx(34)
