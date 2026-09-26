"""Pekabex MG-T span sections (estimate from scaled catalogue drawing)."""

import pytest

from bridgebeams._geometry import section_properties
from bridgebeams.pl.r2_pekabex_mg_t import PekabexMgtSection

from _aggregate import P, run_checks

DEPTH = dict(zip(PekabexMgtSection.SIZES, (900, 1000, 1100, 1200, 1300, 1450, 1600, 1750, 1900, 2100)))


def _check_valid_bounds(size):
    sec = PekabexMgtSection(size)
    p = sec.polygon
    assert p.is_valid and p.exterior.is_ccw
    assert p.bounds == pytest.approx((-1195, 0, 1195, DEPTH[size]))
    assert sec.provenance == "estimate"
    assert sec.source_status.startswith("producer catalogue")
    assert sec.geometry is not None


def _check_mean_area_from_volume(size):
    # Catalogue V/Lc averages the 450-web support zones with the span section,
    # so only a loose bracket applies (observed 0.95-1.08).
    sec = PekabexMgtSection(size)
    mean = sec.published["volume_m3"] / sec.published["length_m"] * 1e6
    ratio = mean / section_properties(sec.polygon)["area"]
    assert 0.94 < ratio < 1.09


def _check_web_width_at_mid_depth():
    p = PekabexMgtSection("MG-T30").polygon
    from shapely.geometry import LineString
    cut = p.intersection(LineString([(-2000, 700), (2000, 700)]))
    assert cut.length == pytest.approx(220.0)


def _check_invalid_size():
    with pytest.raises(ValueError):
        PekabexMgtSection("MG-T50")


def test_pl_r2_pekabex_mg_t_catalogue_checks():
    run_checks(
        (_check_valid_bounds, P("size", PekabexMgtSection.SIZES)),
        (_check_mean_area_from_volume, P("size", PekabexMgtSection.SIZES)),
        _check_web_width_at_mid_depth,
        _check_invalid_size,
    )
