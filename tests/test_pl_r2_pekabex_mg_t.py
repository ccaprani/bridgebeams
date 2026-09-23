"""Pekabex MG-T span sections (estimate from scaled catalogue drawing)."""

import pytest

from bridgebeams._geometry import section_properties
from bridgebeams.pl.r2_pekabex_mg_t import PekabexMgtSection

DEPTH = dict(zip(PekabexMgtSection.SIZES, (900, 1000, 1100, 1200, 1300, 1450, 1600, 1750, 1900, 2100)))


@pytest.mark.parametrize("size", PekabexMgtSection.SIZES)
def test_valid_bounds(size):
    sec = PekabexMgtSection(size)
    p = sec.polygon
    assert p.is_valid and p.exterior.is_ccw
    assert p.bounds == pytest.approx((-1195, 0, 1195, DEPTH[size]))
    assert sec.provenance == "estimate"
    assert sec.source_status.startswith("producer catalogue")
    assert sec.geometry is not None


@pytest.mark.parametrize("size", PekabexMgtSection.SIZES)
def test_mean_area_from_volume(size):
    # Catalogue V/Lc averages the 450-web support zones with the span section,
    # so only a loose bracket applies (observed 0.95-1.08).
    sec = PekabexMgtSection(size)
    mean = sec.published["volume_m3"] / sec.published["length_m"] * 1e6
    ratio = mean / section_properties(sec.polygon)["area"]
    assert 0.94 < ratio < 1.09


def test_web_width_at_mid_depth():
    p = PekabexMgtSection("MG-T30").polygon
    from shapely.geometry import LineString
    cut = p.intersection(LineString([(-2000, 700), (2000, 700)]))
    assert cut.length == pytest.approx(220.0)


def test_invalid_size():
    with pytest.raises(ValueError):
        PekabexMgtSection("MG-T50")
