"""Source dimensions and independent rectangle-minus-chamfers checks."""

import pytest
from shapely.geometry import LineString

from bridgebeams._geometry import as_polygon, section_properties
from bridgebeams.ca import CaMtoSolidSlabSection


@pytest.mark.parametrize("size,depth", [("S300", 300), ("S400", 400), ("S500", 500)])
def test_mto_ss107_25(size, depth):
    beam = CaMtoSolidSlabSection(size)
    poly = as_polygon(beam.geometry)
    assert poly.is_valid
    assert poly.bounds == (-610, 0, 610, depth)
    p = section_properties(poly)
    assert p["area"] == pytest.approx(1220 * depth - 400)
    assert p["cx"] == pytest.approx(0, abs=1e-9)
    expected_y = (1220 * depth * depth / 2 - 400 * 20 / 3) / (1220 * depth - 400)
    assert p["cy"] == pytest.approx(expected_y, abs=1e-9)
    i_about_soffit = 1220 * depth**3 / 3 - 20**4 / 6
    assert p["ixx"] == pytest.approx(i_about_soffit - p["area"] * expected_y**2, rel=1e-12)
    for y, expected_width in [(0, 1180), (10, 1200), (20, 1220), (depth / 2, 1220)]:
        cut = poly.intersection(LineString([(-1000, y), (1000, y)]))
        assert cut.length == pytest.approx(expected_width)


def test_invalid_designation():
    with pytest.raises(ValueError):
        CaMtoSolidSlabSection("S600")
