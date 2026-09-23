"""Korean KHC I-girders: validate against the source paper's published
35 m section properties (A = 7,896 cm2, Ix = 4.644e12 mm4) and the exact
dimension stack H1+H2+H3+H4+H5 = H."""

import json
from importlib import resources

import pytest

from bridgebeams._geometry import as_polygon, section_properties
from bridgebeams.kr import KhcISection

from _aggregate import P, run_checks

DATA = json.loads(
    resources.files("bridgebeams.kr.data").joinpath("khc_i_girders.json").read_text()
)


def _check_dimension_stack_exact():
    for row in DATA["published_properties"]:
        assert (
            row["h1"] + row["h2"] + row["h3"] + row["h4"] + row["h5"] == row["depth"]
        ), row["section"]


def _check_khc35_against_published_properties():
    beam = KhcISection("KHC-35")
    props = section_properties(as_polygon(beam.geometry))
    # Literature (Computers and Concrete 6(1)): A = 7,896 cm2,
    # Ix = 46,440,522 cm4 = 4.644e11 mm4. Deviations are ~+2% (A) and
    # ~+3% (I): the drawn haunch depths (H2/H4) are slightly heavier
    # than the as-built section - documented in the data file.
    assert props["area"] == pytest.approx(789_600.0, rel=0.03), props["area"]
    assert props["ixx"] == pytest.approx(4.644e11, rel=0.05), props["ixx"]


def _check_all_sizes_construct_and_symmetric():
    for size in KhcISection.SIZES:
        beam = KhcISection(size)
        poly = as_polygon(beam.geometry)
        assert poly.is_valid, size
        xmin, xmax, _, _ = beam.geometry.calculate_extents()
        assert -xmin == pytest.approx(xmax), size


def _check_widths_match_published():
    for row in DATA["published_properties"]:
        beam = KhcISection(row["section"])
        d = beam.dimensions
        assert d.top_flange_width == row["b1"]
        assert d.web_width == row["b2"]
        assert d.bottom_flange_width == row["b3"]


def _check_invalid_size_raises():
    with pytest.raises(ValueError):
        KhcISection("KHC-45")


def test_kr_khc_catalogue_checks():
    run_checks(
        _check_dimension_stack_exact,
        _check_khc35_against_published_properties,
        _check_all_sizes_construct_and_symmetric,
        _check_widths_match_published,
        _check_invalid_size_raises,
    )
