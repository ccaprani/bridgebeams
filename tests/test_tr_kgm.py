"""Turkish KGM I-girders: no published property tables exist, so validation
is against closed-form analytic values for a plain symmetric I-girder."""

import pytest

from bridgebeams.tr import KGMIDimensions, KGMISection

from _aggregate import P, run_checks


def _check_stack_sums_to_depth(size):
    beam = KGMISection(size)
    dims = beam.dimensions
    assert 2 * dims.flange_thickness + dims.web_height == pytest.approx(dims.depth)


def _check_area_matches_analytic():
    for size in KGMISection.SIZES:
        beam = KGMISection(size)
        got = beam.polygon.area
        assert got == pytest.approx(beam.analytic_properties()["area"], rel=1e-9)


def _check_ixx_matches_analytic():
    from bridgebeams._geometry import section_properties, as_polygon

    for size in KGMISection.SIZES:
        beam = KGMISection(size)
        got = section_properties(as_polygon(beam.geometry))["ixx"]
        assert got == pytest.approx(beam.analytic_properties()["ixx"], rel=1e-9)


def _check_symmetric():
    from bridgebeams.tr import KGMISection

    beam = KGMISection("I120")
    xmin, xmax, _, _ = beam.geometry.calculate_extents()
    assert -xmin == pytest.approx(xmax)


def _check_invalid_size_raises():
    with pytest.raises(ValueError):
        KGMISection("I200")


def test_tr_kgm_catalogue_checks():
    run_checks(
        (_check_stack_sums_to_depth, P("size", KGMISection.SIZES)),
        _check_area_matches_analytic,
        _check_ixx_matches_analytic,
        _check_symmetric,
        _check_invalid_size_raises,
    )
