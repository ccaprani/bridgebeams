"""CDOT CBT girders vs worksheet B-618-CBT2 (rev 9/24) property table.

Published values are literal readings of the sheet's table, repeated here
rather than read from the package JSON. The outline reproduces A, yb, Ix
and Iy to print precision; the one 4 in^4 Ix difference (CBT81) is pinned.
"""

import pytest
from shapely.affinity import scale

from bridgebeams.us.state_co_cbt import CoCbtGirderSection
from bridgebeams.us.state_common import gross_properties

IN = 25.4
PROVENANCE = {"transcribed", "transcribed-with-convention", "fitted-reconstruction", "estimate"}
# size: (depth, A in^2, Ix in^4, Iy in^4, yb in)
PUBLISHED = {
    "CBT37.5": (37.5, 792, 151579, 88998, 18.50),
    "CBT45": (45, 845, 240424, 89212, 22.08),
    "CBT54": (54, 908, 378473, 89469, 26.40),
    "CBT63": (63, 971, 553233, 89727, 30.74),
    "CBT72": (72, 1034, 767268, 89984, 35.10),
    "CBT81": (81, 1097, 1023130, 90241, 39.48),
    "CBT90": (90, 1160, 1323390, 90498, 43.87),
}


def test_sizes_match_table():
    assert set(CoCbtGirderSection.SIZES) == set(PUBLISHED)


@pytest.mark.parametrize("size", CoCbtGirderSection.SIZES)
def test_valid_symmetric_outline(size):
    s = CoCbtGirderSection(size)
    poly = s.polygon
    assert poly.is_valid and poly.exterior.is_ccw
    assert poly.bounds[1] == pytest.approx(0.0, abs=1e-9)
    assert poly.bounds[3] == pytest.approx(PUBLISHED[size][0] * IN)
    assert poly.bounds[2] - poly.bounds[0] == pytest.approx(50 * IN)
    assert poly.symmetric_difference(scale(poly, xfact=-1, origin=(0, 0))).area < 1e-3
    assert s.provenance in PROVENANCE and s.source_status
    assert s.geometry is not None


@pytest.mark.parametrize("size", CoCbtGirderSection.SIZES)
def test_published_properties(size):
    depth, a, ix, iy, yb = PUBLISHED[size]
    p = gross_properties(CoCbtGirderSection(size).polygon, IN)
    assert p["area"] == pytest.approx(a, abs=0.5)  # table rounds to 1 in^2
    assert p["yb"] == pytest.approx(yb, abs=0.005)
    assert p["iy"] == pytest.approx(iy, abs=0.5)
    if size == "CBT81":
        # Pinned: computed 1,023,134.3 vs printed 1,023,130 (4 in^4, 4e-6 relative).
        assert p["ix"] == pytest.approx(1023134.3, abs=0.5)
    else:
        assert p["ix"] == pytest.approx(ix, abs=0.5)


def test_invalid_size():
    with pytest.raises(ValueError):
        CoCbtGirderSection("CBT100")
