"""MoDOT EPG 751.22.1.2 I girders and NU girders vs printed properties.

Published values are literal readings of the EPG figures (dated 2022),
repeated here rather than read from the package JSON. All dimensions are
printed, so tolerances are print precision: A +-0.05 in2 (0.1 print),
yb +-0.006 in (0.01 print), Ixx/Iyy +-0.01% (integer print; NU arcs are
64-segment polygons, chord error <= 0.002%).
"""

import pytest
from shapely.affinity import scale

from bridgebeams.us.state_mo_girders import MoDotIGirderSection, MoDotNuGirderSection

IN = 25.4
PROVENANCE = {"transcribed", "transcribed-with-convention", "fitted-reconstruction", "estimate"}


def _ring(coords):
    pts = list(coords)[:-1]
    a = s = i = j = 0.0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
        c = x0 * y1 - x1 * y0
        a += c
        s += (y0 + y1) * c
        i += (y0 * y0 + y0 * y1 + y1 * y1) * c
        j += (x0 * x0 + x0 * x1 + x1 * x1) * c
    return a / 2, s / 6, i / 12, j / 12


def props_in(poly):
    a, s, i, j = _ring(poly.exterior.coords)
    for h in poly.interiors:
        da, ds, di, dj = _ring(h.coords)
        a, s, i, j = a + da, s + ds, i + di, j + dj
    cy = s / a
    return a / IN**2, cy / IN, (i - a * cy * cy) / IN**4, j / IN**4


# size: (A, yb, Ixx, Iyy, depth_in)
I_PUB = {
    "Type2": (310.9, 14.08, 33974, 4045, 32),
    "Type2-7": (342.9, 14.26, 36812, 5032, 32),
    "Type2-8": (374.9, 14.41, 39632, 6190, 32),
    "Type3": (381.9, 17.08, 61841, 5119, 39),
    "Type3-7": (420.9, 17.31, 66991, 6347, 39),
    "Type3-8": (459.9, 17.49, 72106, 7785, 39),
    "Type4": (428.9, 19.54, 92450, 5618, 45),
    "Type4-7": (473.9, 19.82, 100400, 6976, 45),
    "Type4-8": (518.9, 20.06, 108288, 8570, 45),
    "Type6": (643.6, 25.92, 235735, 17833, 54),
    "Type6-7.5": (697.6, 26.00, 248915, 20650, 54),
    "Type6-8.5": (751.6, 26.07, 262087, 23817, 54),
    "Type7": (787.4, 37.58, 571047, 40630, 72.5),
    "Type8": (733.4, 33.03, 411683, 40468, 63.5),
}
NU_PUB = {
    "NU35": (639.8, 15.96, 108498, 60086, 35 + 7 / 16),
    "NU43": (686.1, 19.36, 179343, 60219, 43 + 5 / 16),
    "NU53": (743.9, 23.71, 297512, 60385, 53 + 5 / 32),
    "NU63": (801.7, 28.14, 451306, 60551, 63),
    "NU70": (848.0, 31.74, 601931, 60684, 70 + 7 / 8),
    "NU78": (894.2, 35.37, 778670, 60817, 78.75),
}


@pytest.mark.parametrize("cls", (MoDotIGirderSection, MoDotNuGirderSection))
def test_every_size_valid_symmetric(cls):
    for size in cls.SIZES:
        s = cls(size)
        p = s.polygon
        assert p.is_valid and p.exterior.is_ccw
        assert p.bounds[1] == pytest.approx(0.0, abs=1e-9)
        assert p.symmetric_difference(scale(p, xfact=-1, origin=(0, 0))).area < 1e-3
        assert s.provenance in PROVENANCE
        assert s.source_status
        assert s.geometry is not None


@pytest.mark.parametrize("cls", (MoDotIGirderSection, MoDotNuGirderSection))
def test_invalid_size(cls):
    with pytest.raises(ValueError):
        cls("Type5")


@pytest.mark.parametrize("size,pub", list(I_PUB.items()) + list(NU_PUB.items()))
def test_published_properties(size, pub):
    cls = MoDotNuGirderSection if size.startswith("NU") else MoDotIGirderSection
    s = cls(size)
    a, yb, ix, iy = props_in(s.polygon)
    assert s.polygon.bounds[3] / IN == pytest.approx(pub[4], abs=1e-9)
    assert a == pytest.approx(pub[0], abs=0.07)
    assert yb == pytest.approx(pub[1], abs=0.006)
    assert ix == pytest.approx(pub[2], rel=1e-4)
    assert iy == pytest.approx(pub[3], rel=1e-4)


def test_key_widths():
    t6 = MoDotIGirderSection("Type6").polygon.bounds
    assert (t6[2] - t6[0]) / IN == pytest.approx(24)
    t7 = MoDotIGirderSection("Type7").polygon.bounds
    assert (t7[2] - t7[0]) / IN == pytest.approx(42)
    nu = MoDotNuGirderSection("NU63")
    assert nu.dimensions.top_width / IN == pytest.approx(48.25)
    assert nu.dimensions.bottom_width / IN == pytest.approx(38.375)
    # soffit width reduced by the two 3/4 in chamfers
    soffit = [x for x, y in nu.polygon.exterior.coords if abs(y) < 1e-9]
    assert (max(soffit) - min(soffit)) / IN == pytest.approx(38.375 - 1.5)
