"""Validation of the Irish T-beam and YE edge-beam families against
published properties (Banagher manual 3rd ed., pp. 16 and 32-33)."""

import json
from importlib import resources

import pytest

from bridgebeams._geometry import as_polygon, section_properties
from bridgebeams.ie import IeTBeamSection, IeYEBeamSection

from _aggregate import P, run_checks

T_DATA = json.loads(
    resources.files("bridgebeams.ie.data").joinpath("ie_t_beam.json").read_text()
)
YE_DATA = json.loads(
    resources.files("bridgebeams.ie.data").joinpath("ie_ye_beam.json").read_text()
)

T_TOL = {"area": 0.001, "yc": 0.001, "ixx": 0.001}  # exact dims: <0.02% deviation
YE_TOL = {"area": 0.02, "yc": 0.02, "xc": 0.02, "ixx": 0.02}


def _check_t_beam_all_sizes_against_published():
    for row in T_DATA["published_properties"]:
        beam = IeTBeamSection(row["section"])
        props = section_properties(as_polygon(beam.geometry))
        assert props["area"] == pytest.approx(row["area"], rel=T_TOL["area"]), row["section"]
        assert props["cy"] == pytest.approx(row["yc"], rel=T_TOL["yc"]), row["section"]
        assert props["ixx"] == pytest.approx(row["ixx_e9"] * 1e9, rel=T_TOL["ixx"]), row["section"]


def _check_t_beam_depths_reconcile_with_published_stack():
    """F + 50 + H + 50 + 40 + 75 + 25 must equal the published depth."""
    for row in T_DATA["published_properties"]:
        assert (
            row["F"] + 50 + row["H"] + 50 + 40 + 75 + 25 == row["depth"]
        ), row["section"]


def _check_t_beam_web_height_subgroups():
    assert IeTBeamSection("T1").dimensions.web_height == 85.0
    assert IeTBeamSection("T3").dimensions.web_height == 240.0


def _check_t_beam_invalid_size_raises():
    with pytest.raises(ValueError):
        IeTBeamSection("T11")


def _check_ye_beam_all_sizes_against_published():
    for row in YE_DATA["published_properties"]:
        beam = IeYEBeamSection(row["section"])
        props = section_properties(as_polygon(beam.geometry))
        assert props["area"] == pytest.approx(row["area"], rel=YE_TOL["area"]), row["section"]
        assert props["cy"] == pytest.approx(row["yc"], rel=YE_TOL["yc"]), row["section"]
        # Xc: centroid offset from the vertical face at x = -375
        xc = props["cx"] + 375.0
        assert xc == pytest.approx(row["xc"], rel=YE_TOL["xc"]), row["section"]
        assert props["ixx"] == pytest.approx(row["ixx_e9"] * 1e9, rel=YE_TOL["ixx"]), row["section"]


def _check_ye_beam_vertical_face_position():
    for size in IeYEBeamSection.SIZES:
        poly = as_polygon(IeYEBeamSection(size).geometry)
        minx, _, _, _ = poly.bounds
        assert minx == pytest.approx(-375.0, abs=1e-6)


def _check_ye_beam_top_width_matches_published_wf():
    from bridgebeams.ie import wf_of_depth

    for row in YE_DATA["published_properties"]:
        assert wf_of_depth(row["depth"]) == pytest.approx(row["wf"], abs=0.05), row["section"]


def _check_ye_beam_invalid_size_raises():
    with pytest.raises(ValueError):
        IeYEBeamSection("YE9")


def test_ukie_t_ye_catalogue_checks():
    run_checks(
        _check_t_beam_all_sizes_against_published,
        _check_t_beam_depths_reconcile_with_published_stack,
        _check_t_beam_web_height_subgroups,
        _check_t_beam_invalid_size_raises,
        _check_ye_beam_all_sizes_against_published,
        _check_ye_beam_vertical_face_position,
        _check_ye_beam_top_width_matches_published_wf,
        _check_ye_beam_invalid_size_raises,
    )
