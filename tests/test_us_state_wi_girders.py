"""WisDOT I-girders and box girders vs published properties.

Published values are literal readings of the WisDOT Chapter 19 design-data
standards (19.02-19.20, PDF pp2-12) and Bridge Manual Table 19.3-3 (January
2023, PDF p46), repeated here rather than read from the package JSON.
"""

import pytest
from shapely.affinity import scale

from bridgebeams.us.state_common import gross_properties
from bridgebeams.us.state_wi_girders import WiBoxGirderSection, WiGirderSection

IN = 25.4
PROVENANCE = {"transcribed", "transcribed-with-convention", "fitted-reconstruction", "estimate"}

# size: (A in2, yb in, I in4)
I_PUB = {
    "28": (312, 13.42, 28687),
    "36W": (632, 16.63, 99980),
    "45W": (692, 20.74, 178971),
    "54W": (798, 26.30, 321049),
    "72W": (915, 34.87, 656426),
    "82W": (980, 39.68, 905453),
}
# size: (A in2, I in4, Sb in3)
BOX_PUB = {
    "36x12": (422, 5101, 852), "36x17": (452, 14047, 1657), "36x21": (492, 25240, 2410),
    "36x27": (565, 50141, 3722), "36x33": (625, 85010, 5162), "36x42": (715, 158749, 7573),
    "48x12": (566, 6829, 1140), "48x17": (584, 18744, 2210), "48x21": (624, 33501, 3197),
    "48x27": (697, 65728, 4877), "48x33": (757, 110299, 6696), "48x42": (847, 203046, 9683),
}


@pytest.mark.parametrize("cls", (WiGirderSection, WiBoxGirderSection))
def test_every_size_valid_symmetric(cls):
    for size in cls.SIZES:
        s = cls(size)
        p = s.polygon
        assert p.is_valid and p.exterior.is_ccw
        assert all(not r.is_ccw for r in p.interiors)
        assert p.bounds[1] == pytest.approx(0.0, abs=1e-9)
        assert p.symmetric_difference(scale(p, xfact=-1, origin=(0, 0))).area < 1e-3
        assert s.provenance in PROVENANCE
        assert isinstance(s.source_status, str) and s.source_status
        assert s.geometry is not None


@pytest.mark.parametrize("cls", (WiGirderSection, WiBoxGirderSection))
def test_invalid_size_raises(cls):
    with pytest.raises(ValueError):
        cls("99X")


@pytest.mark.parametrize("size", WiGirderSection.SIZES)
def test_girder_bounds(size):
    s = WiGirderSection(size)
    x0, y0, x1, y1 = s.polygon.bounds
    assert y1 == pytest.approx(s.dimensions.depth)
    assert x1 - x0 == pytest.approx(max(s.dimensions.top_width, s.dimensions.bottom_width))
    widths = {"28": (18, 18), "36W": (34, 30), "45W": (34, 30), "54W": (48, 30), "72W": (48, 30), "82W": (48, 30)}
    top, bot = widths[size]
    assert s.dimensions.top_width == pytest.approx(top * IN)
    assert s.dimensions.bottom_width == pytest.approx(bot * IN)


# Published A is rounded to 1 in2 and yb to 0.01 in. Tolerances: 1.1 in2
# (36W prints 632 while 45W prints 692 = 632 + 9 in x 6.5 in - 1.5, i.e. the
# two printed areas are mutually inconsistent by ~1.5 in2), 0.03 in, 0.4 % I.
@pytest.mark.parametrize("size", ("36W", "54W", "72W", "82W"))
def test_girder_published_properties(size):
    g = gross_properties(WiGirderSection(size).polygon, IN)
    a, yb, ix = I_PUB[size]
    assert g["area"] == pytest.approx(a, abs=1.1)
    assert g["yb"] == pytest.approx(yb, abs=0.03)
    assert g["ix"] == pytest.approx(ix, rel=0.004)


def test_45w_pinned_centroid_discrepancy():
    """45W: A and I agree but printed yB = 20.74 in is 0.12 in above the drawn outline."""
    g = gross_properties(WiGirderSection("45W").polygon, IN)
    a, yb, ix = I_PUB["45W"]
    assert g["area"] == pytest.approx(a, abs=1.1)
    assert g["ix"] == pytest.approx(ix, rel=0.004)
    assert g["yb"] - yb == pytest.approx(-0.121, abs=0.01)


def test_28in_pinned_inertia_discrepancy():
    """28 in: A and yB match (bevel-free A = 312 exactly) but printed I is 2.3 % high."""
    g = gross_properties(WiGirderSection("28").polygon, IN)
    a, yb, ix = I_PUB["28"]
    assert g["area"] == pytest.approx(a, abs=0.6)
    assert g["yb"] == pytest.approx(yb, abs=0.03)
    assert g["ix"] / ix - 1 == pytest.approx(-0.02255, abs=0.001)


@pytest.mark.parametrize("size", WiBoxGirderSection.SIZES)
def test_box_pinned_systematic_residual(size):
    """Key-recess estimate: one systematic offset against Table 19.3-3.

    Every row is 3.0-3.6 in2 (<=0.8 %) heavier and 0.5-1.1 % stiffer than
    printed; published yb (I/Sb) lies below mid-depth, the drawn key puts it
    slightly above. Bands pin this pattern rather than a loose tolerance.
    """
    s = WiBoxGirderSection(size)
    g = gross_properties(s.polygon, IN)
    a, ix, sb = BOX_PUB[size]
    assert 3.0 <= g["area"] - a <= 3.6
    assert 0.005 <= g["ix"] / ix - 1 <= 0.011
    assert 0.0 <= g["yb"] - ix / sb <= 0.1
    depth = float(size.split("x")[1])
    assert len(s.polygon.interiors) == (0 if depth == 12 else 1)
    x0, _, x1, y1 = s.polygon.bounds
    assert x1 - x0 == pytest.approx(float(size.split("x")[0]) * IN)
    assert y1 == pytest.approx(depth * IN)
