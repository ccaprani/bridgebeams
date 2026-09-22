"""Analytic independent checks for RR 364 S4.01/S4.10 external profiles."""
import pytest
from shapely.geometry import LineString

from bridgebeams._geometry import as_polygon, section_properties
from bridgebeams.nz.i_beams import NzIBeamSection


@pytest.mark.parametrize("depth,top,bottom,web,area", [
    (1500, 375, 475, 175, 375*100 + (375+175)*75/2 + 175*1005 + (175+475)*150/2 + 475*170 - 400),
    (1600, 470, 620, 180, 470*110 + (470+180)*145/2 + 180*975 + (180+620)*220/2 + 620*150 - 400),
])
def test_source_profile(depth, top, bottom, web, area):
    beam = NzIBeamSection(depth)
    poly = as_polygon(beam.geometry)
    assert poly.is_valid
    assert poly.bounds == (-bottom/2, 0, bottom/2, depth)
    props = section_properties(poly)
    assert props["area"] == pytest.approx(area, abs=1e-7)
    assert props["cx"] == pytest.approx(0, abs=1e-8)
    assert props["ixx"] > 0
    for y, width in [(depth/2, web), (depth-1, top), (30, bottom)]:
        cut = poly.intersection(LineString([(-1000, y), (1000, y)]))
        assert cut.length == pytest.approx(width)


def test_invalid_depth():
    with pytest.raises(ValueError):
        NzIBeamSection(1550)
