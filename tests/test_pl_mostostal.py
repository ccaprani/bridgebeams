"""Polish Mosty-Łódź T-girders (T12-T27): internal-consistency validation.

No published section-property tables exist in the captured sources, so
validation is against closed-form values for the trapezoidal-stem
section and the attested cross-sectional constants."""

import json
from importlib import resources

import pytest

from bridgebeams._geometry import section_properties, as_polygon
from bridgebeams.pl import MostostalTSection

from _aggregate import P, run_checks

DATA = json.loads(
    resources.files("bridgebeams.pl.data").joinpath("mostostal_t.json").read_text()
)


def _check_all_sizes_match_attested_table():
    for row in DATA["published_properties"]:
        beam = MostostalTSection(row["section"])
        assert beam.dimensions.depth == row["depth"], row["section"]
        assert beam.dimensions.web_bottom_width == row["web_bottom_width"], row["section"]
        assert beam.dimensions.length_m == row["length_m"], row["section"]


def _check_constant_widths_attested():
    for size in MostostalTSection.SIZES:
        d = MostostalTSection(size).dimensions
        assert d.top_flange_width == 890.0
        assert d.web_top_width == 200.0


def _check_t15_t18_share_cross_section():
    d15 = MostostalTSection("T15").dimensions
    d18 = MostostalTSection("T18").dimensions
    assert (d15.depth, d15.web_bottom_width) == (d18.depth, d18.web_bottom_width)


def _check_t22_does_not_exist():
    with pytest.raises(ValueError):
        MostostalTSection("T22")


def _check_polygon_valid_symmetric_closed():
    for size in MostostalTSection.SIZES:
        beam = MostostalTSection(size)
        poly = beam.polygon
        assert poly.is_valid, size
        assert poly.area > 0, size
        xmin, xmax, _, _ = beam.geometry.calculate_extents()
        assert -xmin == pytest.approx(xmax), size
        # depth
        _, _, ymin, ymax = beam.geometry.calculate_extents()
        assert (ymax - ymin) == pytest.approx(beam.dimensions.depth), size


def _check_area_matches_closed_form():
    for size in MostostalTSection.SIZES:
        beam = MostostalTSection(size)
        got = beam.polygon.area
        assert got == pytest.approx(beam.analytic_properties()["area"], rel=1e-9), size


def _check_ixx_matches_closed_form():
    for size in MostostalTSection.SIZES:
        beam = MostostalTSection(size)
        got = section_properties(as_polygon(beam.geometry))["ixx"]
        assert got == pytest.approx(beam.analytic_properties()["ixx"], rel=1e-9), size


def _check_web_widens_downward():
    for size in MostostalTSection.SIZES:
        d = MostostalTSection(size).dimensions
        assert d.web_bottom_width > d.web_top_width, size


def _check_t27_web_bottom_attested():
    # Gąćkowski 2018: T27 web 0.20 m -> 0.465 m
    assert MostostalTSection("T27").dimensions.web_bottom_width == 465.0


def test_pl_mostostal_catalogue_checks():
    run_checks(
        _check_all_sizes_match_attested_table,
        _check_constant_widths_attested,
        _check_t15_t18_share_cross_section,
        _check_t22_does_not_exist,
        _check_polygon_valid_symmetric_closed,
        _check_area_matches_closed_form,
        _check_ixx_matches_closed_form,
        _check_web_widens_downward,
        _check_t27_web_bottom_attested,
    )
