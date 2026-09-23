"""CRH Concrete OT 118 inverted-T bridge beam."""

import pytest
from shapely.geometry import LineString

from bridgebeams._geometry import section_properties
from bridgebeams.dk import CrhOtBeamSection

from _aggregate import P, run_checks


def width_at(p, y):
    return p.intersection(LineString([(-2000, y), (2000, y)])).length


def _check_printed_outline(size):
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


def _check_area_formula():
    # flange: 1180*140 + trapezoid (1180+560)/2*30 + haunch (560+300)/2*85 ; web 300*(H-255)
    a = section_properties(CrhOtBeamSection("OT 118/1000").polygon)["area"]
    assert a == pytest.approx(1180 * 140 + 870 * 30 + 430 * 85 + 300 * 745)


def _check_invalid():
    with pytest.raises(ValueError):
        CrhOtBeamSection("OT 118/1450")


def test_dk_crh_ot_catalogue_checks():
    run_checks(
        (_check_printed_outline, P("size", CrhOtBeamSection.SIZES)),
        _check_area_formula,
        _check_invalid,
    )
