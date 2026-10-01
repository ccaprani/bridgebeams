"""NHAI NH 45-A Package II and Delhi-Vadodara midspan I girders.

No published section properties exist on these sheets, so the checks are
independent hand sums of rectangles and trapezoids from the printed chains.
"""

import pytest

from bridgebeams._geometry import section_properties
from bridgebeams.india import (
    DelhiVadodaraPscISection,
    Nh45aIGirderSection,
    Nh45aPscISection,
    NhaiIGirderDimensions,
)

from _aggregate import P, run_checks


def _hand_area(top, web, base, web_h):
    return (top * 150 + (top + web) / 2 * 100 + web * web_h
            + (web + base) / 2 * 150 + base * 250)


EXPECTED = {
    # size: (depth, top, web, base, clear web, construction, pages)
    "PSC-1500": (1500, 900, 300, 750, 850, "PSC", (61, 66, 68)),
    "PSC-2000": (2000, 900, 300, 750, 1350, "PSC", (52, 63)),
    "RCC-1300": (1300, 800, 300, 600, 650, "RCC", (63,)),
    "RCC-1400": (1400, 800, 300, 600, 750, "RCC", (22,)),
    "RCC-1500": (1500, 800, 300, 600, 850, "RCC", (28, 30, 47)),
    "RCC-2000": (2000, 900, 300, 750, 1350, "RCC", (26,)),
    "RCC-2250": (2250, 900, 300, 750, 1600, "RCC", (44,)),
}


def _check_nh45a_outline_bounds_area_and_labels(size):
    depth, top, web, base, web_h, kind, pages = EXPECTED[size]
    s = Nh45aIGirderSection(size)
    poly = s.polygon
    assert poly.is_valid and poly.exterior.is_ccw
    assert poly.bounds == (-max(top, base) / 2, 0.0, max(top, base) / 2, depth)
    assert s.dimensions.web_height == web_h
    assert poly.area == pytest.approx(_hand_area(top, web, base, web_h), abs=1e-6)
    assert s.geometry.geom.area == pytest.approx(poly.area)
    assert s.construction == kind and s.prestressed is (kind == "PSC")
    assert s.provenance == "transcribed"
    assert s.source_status == "Final Feasibility Report"
    assert s.pdf_pages == pages


def _check_nh45a_gross_areas_match_assessment_values():
    areas = {sz: Nh45aIGirderSection(sz).polygon.area for sz in Nh45aIGirderSection.SIZES}
    assert areas == {"PSC-1500": 716250, "PSC-2000": 866250, "RCC-1300": 587500,
                     "RCC-1400": 617500, "RCC-1500": 647500, "RCC-2000": 866250,
                     "RCC-2250": 941250}


def _check_nh45a_splay_widths_match_printed_callouts():
    d900 = Nh45aIGirderSection("PSC-1500").dimensions
    d800 = Nh45aIGirderSection("RCC-1300").dimensions
    assert (d900.upper_splay_width, d900.lower_splay_width) == (300, 225)
    assert (d800.upper_splay_width, d800.lower_splay_width) == (250, 150)


def _check_identical_outlines_are_recorded_and_really_identical():
    psc, rcc = Nh45aIGirderSection("PSC-2000"), Nh45aIGirderSection("RCC-2000")
    assert psc.dimensions.outline == rcc.dimensions.outline
    assert "RCC-2000" in psc.identical_to and "PSC-2000" in rcc.identical_to
    assert psc.construction != rcc.construction
    rcc2250 = Nh45aIGirderSection("RCC-2250")
    assert rcc2250.dimensions.outline == Nh45aPscISection().dimensions.outline
    assert any("Nh45aPscISection" in x for x in rcc2250.identical_to)
    # Same 1500 depth but different families: must NOT be identical.
    assert (Nh45aIGirderSection("PSC-1500").dimensions.outline
            != Nh45aIGirderSection("RCC-1500").dimensions.outline)


def _check_delhi_vadodara_estimate():
    s = DelhiVadodaraPscISection()
    assert s.provenance == "estimate"
    assert s.construction == "PSC" and s.pdf_pages == (41,)
    assert s.polygon.is_valid
    assert s.polygon.bounds == (-550.0, 0.0, 550.0, 2000.0)
    assert s.dimensions.web_width == 300  # scaled 288 +/- 26 mm, see JSON estimate block
    assert s.polygon.area == pytest.approx(_hand_area(1100, 300, 750, 1350)) == 906250
    props = section_properties(s.polygon)
    assert 0 < props["cy"] < 2000 and props["ixx"] > 0


def _check_invalid_sizes_and_open_chain_raise():
    with pytest.raises(ValueError, match="size must be one of"):
        Nh45aIGirderSection("PSC-2250")
    with pytest.raises(ValueError, match="size must be one of"):
        DelhiVadodaraPscISection("KM37+744-END")
    with pytest.raises(ValueError, match="does not close"):
        NhaiIGirderDimensions(1500, 900, 300, 750, 150, 100, 800, 150, 250)


def test_india_nhai_i_girders_catalogue_checks():
    run_checks(
        (_check_nh45a_outline_bounds_area_and_labels, P("size", Nh45aIGirderSection.SIZES)),
        _check_nh45a_gross_areas_match_assessment_values,
        _check_nh45a_splay_widths_match_printed_callouts,
        _check_identical_outlines_are_recorded_and_really_identical,
        _check_delhi_vadodara_estimate,
        _check_invalid_sizes_and_open_chain_raise,
    )
