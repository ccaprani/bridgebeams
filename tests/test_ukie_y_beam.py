"""Validation of the reconstructed Irish Y-beam family against published
section properties (Banagher manual 3rd ed. p. 32 == Concast == the 2007
spreadsheet).

The geometry is a documented least-squares reconstruction (rms 2.63%, max
4.8%), so tolerances are set at A: 4%, yc: 2.5%, Ixx: 5% of published
values. If a future revision tightens the reconstruction, tighten these
tolerances.
"""

import json
from importlib import resources

import pytest

from bridgebeams.ie import IeYBeamSection, strand_locations
from bridgebeams._geometry import as_polygon, section_properties

DATA = json.loads(
    resources.files("bridgebeams.ie.data").joinpath("ie_y_beam.json").read_text()
)

TOL = {"area": 0.04, "yc": 0.025, "ixx": 0.05}


def test_all_sizes_against_published_properties():
    for row in DATA["published_properties"]:
        beam = IeYBeamSection(row["section"])
        props = section_properties(beam.polygon)
        assert props["area"] == pytest.approx(row["area"], rel=TOL["area"]), row["section"]
        assert props["cy"] == pytest.approx(row["yc"], rel=TOL["yc"]), row["section"]
        assert props["ixx"] == pytest.approx(
            row["ixx_e9"] * 1e9, rel=TOL["ixx"]
        ), row["section"]


def test_reconstruction_rms_matches_documented_value():
    """Guard: if geometry changes, the documented rms must be re-established."""
    errs = []
    for row in DATA["published_properties"]:
        beam = IeYBeamSection(row["section"])
        props = section_properties(beam.polygon)
        errs += [
            (props["area"] - row["area"]) / row["area"],
            (props["area"] * props["cy"] - row["area"] * row["yc"])
            / (row["area"] * row["yc"]),
            (props["ixx"] - row["ixx_e9"] * 1e9) / (row["ixx_e9"] * 1e9),
        ]
    rms = (sum(e * e for e in errs) / len(errs)) ** 0.5
    assert rms * 100 <= DATA["fit"]["rms_error_pct"] + 0.05


def test_top_width_matches_published_wf():
    for row in DATA["published_properties"]:
        beam = IeYBeamSection(row["section"])
        assert beam.dimensions.top_width == pytest.approx(row["wf"], rel=0.005)


def test_geometry_valid_and_symmetric():
    for size in IeYBeamSection.SIZES:
        poly = as_polygon(IeYBeamSection(size).geometry)
        assert poly.is_valid
        assert poly.area > 0
        minx, _, maxx, _ = poly.bounds
        assert minx == pytest.approx(-375.0, abs=1e-6)
        assert maxx == pytest.approx(375.0, abs=1e-6)


def test_invalid_size_raises():
    with pytest.raises(ValueError):
        IeYBeamSection("Y9")


def test_strand_locations_inside_section():
    for size in IeYBeamSection.SIZES:
        beam = IeYBeamSection(size)
        pts = strand_locations(size)
        assert len(pts) > 0
        for x, y in pts:
            assert -375 <= x <= 375
            assert 0 < y < beam.depth


def test_strand_row_counts():
    pts = strand_locations("Y8")
    heights = sorted({round(y) for x, y in pts})
    assert heights[0] == 60  # bottom row at 60 mm
    assert len([y for y in heights if y <= 210]) == 4  # four bottom-zone rows
    # 13 + 14 + 14 + 10 strands in the bottom zone
    bottom = sum(1 for x, y in pts if y <= 210)
    assert bottom == 13 + 14 + 14 + 10


def test_strand_locations_exclude_rows_near_top():
    pts = strand_locations("Y1", min_top_cover=60.0)
    assert max(y for x, y in pts) <= 700 - 60
