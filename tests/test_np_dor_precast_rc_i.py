"""Nepal DoR precast RC I beams 1300/1700 with the 12x12 chamfer convention."""

import math

import pytest

from bridgebeams._geometry import section_properties
from bridgebeams.np import DorPrecastRcIDimensions, DorPrecastRcISection


def _sharp_area(web_h):
    return 700 * 150 + (700 + 325) / 2 * 65 + 325 * web_h + (325 + 700) / 2 * 150 + 700 * 250


def _chamfer_loss():
    tri = lambda a, b: 0.5 * 144 * abs(a[0] * b[1] - a[1] * b[0]) / (math.hypot(*a) * math.hypot(*b))
    soffit = tri((-1, 0), (0, 1))
    shoulder = tri((0, -1), (-187.5, 150))
    top_under = tri((0, 1), (-187.5, -65))
    return 2 * (soffit + shoulder + top_under)


@pytest.mark.parametrize("size,depth,web_h,span", [("1300", 1300, 685, 20.0), ("1700", 1700, 1085, 25.0)])
def test_sharp_outline_matches_printed_chain(size, depth, web_h, span):
    s = DorPrecastRcISection(size, chamfer=False)
    poly = s.polygon
    assert poly.is_valid and poly.exterior.is_ccw
    assert poly.bounds == (-350.0, 0.0, 350.0, depth)
    assert poly.area == pytest.approx(_sharp_area(web_h))
    assert s.span_m == span and s.prestressed is False
    assert s.provenance == "transcribed"
    # Detail 'Y' prints 187.5 splay horizontal
    assert (s.dimensions.bottom_width - s.dimensions.web_width) / 2 == 187.5


@pytest.mark.parametrize("size,web_h", [("1300", 685), ("1700", 1085)])
def test_chamfer_convention_area_effect(size, web_h):
    s = DorPrecastRcISection(size)
    assert s.provenance == "transcribed-with-convention"
    assert s.source_status == "DoR standard drawing, July 2015"
    poly = s.polygon
    assert poly.is_valid and len(poly.exterior.coords) - 1 == 12 + 6
    loss = _sharp_area(web_h) - poly.area
    assert loss == pytest.approx(_chamfer_loss(), abs=1e-6)
    assert loss == pytest.approx(392.5, abs=0.1)
    assert loss < 600 and loss / poly.area < 1e-3
    assert poly.area == pytest.approx(s.record["gross_area_mm2"], abs=0.1)
    # Chamfer is 12 mm along the soffit
    assert min(x for x, y in poly.exterior.coords if y == 0) == pytest.approx(-338.0)
    assert s.geometry.geom.area == pytest.approx(poly.area)
    sharp = section_properties(DorPrecastRcISection(size, chamfer=False).polygon)
    cham = section_properties(poly)
    assert abs(cham["cy"] - sharp["cy"]) < 0.5 and abs(cham["ixx"] / sharp["ixx"] - 1) < 1e-3


def test_invalid_size_and_chain():
    with pytest.raises(ValueError, match="size must be one of"):
        DorPrecastRcISection("1500")
    with pytest.raises(ValueError, match="does not close"):
        DorPrecastRcIDimensions(depth=1300, web_height=700)
