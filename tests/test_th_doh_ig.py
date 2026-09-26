"""Thai DOH 20 m I-girder: dimension-stack and geometry checks."""

import pytest

from bridgebeams.th import ThDOHIGirderSection

from _aggregate import P, run_checks


def _check_dimension_stack():
    beam = ThDOHIGirderSection()
    d = beam.dimensions
    assert (
        d.top_flange_thickness
        + d.haunch_height
        + d.web_clear_height
        + d.bottom_flange_edge_thickness
        == pytest.approx(d.depth)
    )


def _check_construct_and_valid():
    beam = ThDOHIGirderSection()
    poly = beam.polygon
    assert poly.is_valid
    assert poly.area > 0


def _check_symmetric():
    from bridgebeams._geometry import as_polygon

    beam = ThDOHIGirderSection()
    xmin, xmax, _, _ = beam.geometry.calculate_extents()
    assert -xmin == pytest.approx(xmax)


def _check_web_between_flanges():
    beam = ThDOHIGirderSection()
    assert beam.dimensions.web_width < beam.dimensions.top_flange_width
    assert beam.dimensions.web_width < beam.dimensions.bottom_flange_width


def test_th_doh_ig_catalogue_checks():
    run_checks(
        _check_dimension_stack,
        _check_construct_and_valid,
        _check_symmetric,
        _check_web_between_flanges,
    )
