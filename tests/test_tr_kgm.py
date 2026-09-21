"""Turkish KGM I-girders: no published property tables exist, so validation
is against closed-form analytic values for a plain symmetric I-girder."""

import pytest

from bridgebeams.tr import KGMIDimensions, KGMISection


@pytest.mark.parametrize("size", KGMISection.SIZES)
def test_construct_and_valid(size):
    beam = KGMISection(size)
    poly = beam.polygon
    assert poly.is_valid
    assert poly.area > 0


@pytest.mark.parametrize("size", KGMISection.SIZES)
def test_stack_sums_to_depth(size):
    beam = KGMISection(size)
    dims = beam.dimensions
    assert 2 * dims.flange_thickness + dims.web_height == pytest.approx(dims.depth)


def test_area_matches_analytic():
    for size in KGMISection.SIZES:
        beam = KGMISection(size)
        got = beam.polygon.area
        assert got == pytest.approx(beam.analytic_properties()["area"], rel=1e-9)


def test_ixx_matches_analytic():
    from bridgebeams._geometry import section_properties, as_polygon

    for size in KGMISection.SIZES:
        beam = KGMISection(size)
        got = section_properties(as_polygon(beam.geometry))["ixx"]
        assert got == pytest.approx(beam.analytic_properties()["ixx"], rel=1e-9)


def test_symmetric():
    from bridgebeams.tr import KGMISection

    beam = KGMISection("I120")
    xmin, xmax, _, _ = beam.geometry.calculate_extents()
    assert -xmin == pytest.approx(xmax)


def test_invalid_size_raises():
    with pytest.raises(ValueError):
        KGMISection("I200")
