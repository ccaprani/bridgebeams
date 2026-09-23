"""CRH Concrete OT 118 inverted-T bridge beam."""

import pytest
from shapely.geometry import LineString

from bridgebeams._geometry import section_properties
from bridgebeams.dk import CrhOtBeamSection


def width_at(p, y):
    return p.intersection(LineString([(-2000, y), (2000, y)])).length


@pytest.mark.parametrize("size", CrhOtBeamSection.SIZES)
def test_printed_outline(size):
    sec = CrhOtBeamSection(size)
    p = sec.polygon
    h = sec.dimensions.depth
    assert p.is_valid and p.exterior.is_ccw
    assert p.bounds == pytest.approx((-590, 0, 590, h))
    assert width_at(p, 70) == pytest.approx(1180)
    assert width_at(p, h - 1) == pytest.approx(300)
    assert width_at(p, 170) == pytest.approx(300 + 2 * 130 * (85 - 0) / 85, rel=1e-9)
    assert sec.provenance == "transcribed-with-convention"
    assert sec.geometry is not None


def test_area_formula():
    # flange: 1180*140 + trapezoid (1180+560)/2*30 + haunch (560+300)/2*85 ; web 300*(H-255)
    a = section_properties(CrhOtBeamSection("OT 118/1000").polygon)["area"]
    assert a == pytest.approx(1180 * 140 + 870 * 30 + 430 * 85 + 300 * 745)


def test_invalid():
    with pytest.raises(ValueError):
        CrhOtBeamSection("OT 118/1450")
