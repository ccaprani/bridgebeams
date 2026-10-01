"""NHAI feasibility-drawing midspan contour, PDF page 50."""

import pytest

from bridgebeams.india import Nh45aPscISection

from _aggregate import P, run_checks


def _check_nh45a_midspan_dimension_chain_and_gross_area():
    section = Nh45aPscISection()
    polygon = section.polygon
    assert polygon.is_valid
    assert polygon.bounds == (-450.0, 0.0, 450.0, 2250.0)
    assert section.dimensions.outline == [
        (-375, 0), (375, 0), (375, 250), (150, 400),
        (150, 2000), (450, 2100), (450, 2250),
        (-450, 2250), (-450, 2100), (-150, 2000),
        (-150, 400), (-375, 250),
    ]
    # Independent sum of two rectangles and three height-by-average-width bands.
    expected = 750 * 250 + (750 + 300) / 2 * 150 + 300 * 1600
    expected += (300 + 900) / 2 * 100 + 900 * 150
    assert polygon.area == expected == 941250
    assert section.geometry.geom.area == expected


def _check_nh45a_has_only_the_dimensioned_midspan_variant():
    with pytest.raises(ValueError, match="CH50\\+473-MID"):
        Nh45aPscISection("CH50+473-END")


def test_india_nhai_catalogue_checks():
    run_checks(
        _check_nh45a_midspan_dimension_chain_and_gross_area,
        _check_nh45a_has_only_the_dimensioned_midspan_variant,
    )
