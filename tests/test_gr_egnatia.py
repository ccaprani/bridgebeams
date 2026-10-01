"""Greek Egnatia extended-I family: depth law, web rule, widths from the
published proposal; flange thicknesses are user design parameters (nothing
assumed), so validation is structural, not against thickness-dependent
published values."""

import json
from importlib import resources

import pytest

from bridgebeams._geometry import section_properties, as_polygon
from bridgebeams.gr import GrExtendedISection, standard_depth, web_width

from _aggregate import P, run_checks

DATA = json.loads(
    resources.files("bridgebeams.gr.data").joinpath("egnatia_extended_i.json").read_text()
)


def _check_standard_depth_matches_published_table():
    for length, depths in DATA["table_depths_m"].items():
        L = float(length)
        for weff, d_pub in zip(DATA["weff_classes_m"], depths):
            assert standard_depth(L, weff) == pytest.approx(d_pub, abs=0.005), (length, weff)


def _check_safe_side_selection_between_standard_lengths():
    # spans between standard lengths select the next-longer standard depth
    assert standard_depth(23.0, 2.5) == pytest.approx(standard_depth(23.5, 2.5))


def _check_web_rule_matches_published():
    assert web_width(1.25) == 300.0
    assert web_width(1.70) == 320.0
    assert web_width(2.15) == 340.0


def _check_widths_constant():
    beam = GrExtendedISection(span_m=35.0, weff_m=2.5,
                              top_flange_thickness=200, bottom_flange_thickness=300)
    d = beam.dimensions
    assert d.top_flange_width == 1400.0
    assert d.bottom_flange_width == 750.0


def _check_all_45_depths_construct_and_valid():
    count = 0
    for length in DATA["lengths_m"]:
        for weff in DATA["weff_classes_m"]:
            beam = GrExtendedISection(span_m=length, weff_m=weff,
                                      top_flange_thickness=200,
                                      bottom_flange_thickness=300)
            poly = beam.polygon
            assert poly.is_valid
            assert poly.area > 0
            count += 1
    assert count == 45


def _check_thickness_validation():
    with pytest.raises(ValueError):
        GrExtendedISection(span_m=35.0, weff_m=2.5, top_flange_thickness=0,
                           bottom_flange_thickness=300)


def _check_invalid_span_raises():
    with pytest.raises(ValueError):
        GrExtendedISection(span_m=-1.0, weff_m=2.5,
                           top_flange_thickness=200, bottom_flange_thickness=300)


def test_gr_egnatia_catalogue_checks():
    run_checks(
        _check_standard_depth_matches_published_table,
        _check_safe_side_selection_between_standard_lengths,
        _check_web_rule_matches_published,
        _check_widths_constant,
        _check_all_45_depths_construct_and_valid,
        _check_thickness_validation,
        _check_invalid_span_raises,
    )
