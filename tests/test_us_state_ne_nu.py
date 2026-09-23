"""NDOR NU900-NU2000 (Design Aids of NU I-Girder Bridges, Table 1) vs print.

Published inch values (Table 1, p14) are repeated literally. The geometry
is a fitted reconstruction: the metric template reproduces Table 1, but the
20 mm soffit chamfer is not drawn on Figure 1 and was chosen to remove a
constant +527 mm2 (+0.08%) area excess. Tolerances: area 0.02%, yb 0.06 in
(print is 0.1 in), I 0.07%. The metric-column NU1350 inertia is pinned as
a source typo.
"""

import pytest
from shapely.affinity import scale

from bridgebeams.us.state_ne_nu import NeNuGirderSection

IN = 25.4
PUB = {  # depth_mm: (area in2, yb in, I in4)
    "NU900": (648.1, 16.1, 110262),
    "NU1100": (694.6, 19.6, 182279),
    "NU1350": (752.7, 24.0, 302334),
    "NU1600": (810.8, 28.4, 458482),
    "NU1800": (857.3, 32.0, 611328),
    "NU2000": (903.8, 35.7, 790592),
}


def props_mm(poly):
    pts = list(poly.exterior.coords)[:-1]
    a = s = i = 0.0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
        c = x0 * y1 - x1 * y0
        a += c
        s += (y0 + y1) * c
        i += (y0 * y0 + y0 * y1 + y1 * y1) * c
    a, s, i = a / 2, s / 6, i / 12
    cy = s / a
    return a, cy, i - a * cy * cy


def test_every_size_valid():
    for size in NeNuGirderSection.SIZES:
        s = NeNuGirderSection(size)
        p = s.polygon
        assert p.is_valid and p.exterior.is_ccw
        assert p.bounds[1] == pytest.approx(0.0, abs=1e-9)
        assert p.bounds[3] == pytest.approx(float(size[2:]))
        assert (p.bounds[2] - p.bounds[0]) == pytest.approx(1225)
        assert p.symmetric_difference(scale(p, xfact=-1, origin=(0, 0))).area < 1e-3
        assert s.provenance == "fitted-reconstruction"
        assert s.source_status
        assert s.geometry is not None


def test_invalid_size():
    with pytest.raises(ValueError):
        NeNuGirderSection("NU35")


@pytest.mark.parametrize("size,pub", PUB.items())
def test_published_properties(size, pub):
    a, yb, i = props_mm(NeNuGirderSection(size).polygon)
    assert a / IN**2 == pytest.approx(pub[0], rel=2e-4)
    assert yb / IN == pytest.approx(pub[1], abs=0.06)
    assert i / IN**4 == pytest.approx(pub[2], rel=7e-4)


def test_nu1350_metric_inertia_typo_pinned():
    # Table 1 prints 126,841 x10^6 mm4 but 302,334 in4 = 125,840 x10^6 mm4
    assert 302334 * IN**4 / 1e6 == pytest.approx(125840, abs=1)
    _, _, i = props_mm(NeNuGirderSection("NU1350").polygon)
    assert i / 1e6 == pytest.approx(125840, rel=7e-4)
    assert abs(i / 1e6 / 126841 - 1) > 0.005


def test_soffit_chamfer_estimate():
    p = NeNuGirderSection("NU900").polygon
    soffit = [x for x, y in p.exterior.coords if abs(y) < 1e-9]
    assert max(soffit) - min(soffit) == pytest.approx(975 - 40)
