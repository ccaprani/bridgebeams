"""Tests for Taiwan DGH 1991 PCI Types I-VII."""

import pytest

from bridgebeams._geometry import section_properties
from bridgebeams.tw.r2_thb_pci_girders import ThbPciGirderSection

from _aggregate import P, run_checks


def _analytic_area(d):
    return (
        d.top_width * d.top_flange
        + d.bottom_width * d.bottom_flange
        + 0.5 * (d.top_width + d.web_width) * d.top_taper
        + 0.5 * (d.bottom_width + d.web_width) * d.bottom_taper
        + d.web_width * d.clear_web
    )


def _check_valid_bounds_area(size):
    s = ThbPciGirderSection(size)
    p, d = s.polygon, s.dimensions
    assert p.is_valid and p.exterior.is_ccw
    assert p.bounds == (-max(d.top_width, d.bottom_width) / 2, 0, max(d.top_width, d.bottom_width) / 2, d.depth)
    assert d.clear_web > 0
    assert section_properties(p)["area"] == pytest.approx(_analytic_area(d))
    assert s.provenance == "transcribed"
    s.geometry


def _check_table_values():
    d = ThbPciGirderSection("VII").dimensions
    assert (d.depth, d.top_width, d.bottom_width, d.web_width) == (2200, 1400, 700, 200)
    assert (d.top_flange, d.bottom_flange, d.top_taper, d.bottom_taper) == (200, 350, 150, 250)
    t1 = ThbPciGirderSection("I").dimensions
    assert t1.bottom_taper == 190  # Table 4; Figure 2 prints 18 cm (pinned conflict)
    for k in ThbPciGirderSection.SIZES:
        dd = ThbPciGirderSection(k).dimensions
        f2 = ThbPciGirderSection(k).published["dimensions_source_cm"]["F2"] * 10
        assert (dd.bottom_width - dd.web_width) / 2 == pytest.approx(f2)


def _check_invalid():
    with pytest.raises(ValueError):
        ThbPciGirderSection("VIII")


def test_tw_r2_thb_pci_catalogue_checks():
    run_checks(
        (_check_valid_bounds_area, P("size", ThbPciGirderSection.SIZES)),
        _check_table_values,
        _check_invalid,
    )


def test_thb_type_i_bottom_taper_table_vs_figure_pinned():
    run_checks(_check_table_values)
