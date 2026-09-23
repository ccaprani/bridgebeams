"""Tilsta TILTO SIJA girders (vector CAD, 1:50)."""

import pytest
from shapely.geometry import LineString, box

from bridgebeams.lt.tilsta import TilstaSijaSection


def width_at(poly, y):
    return poly.intersection(LineString([(-5000, y), (5000, y)])).length


@pytest.mark.parametrize("size", TilstaSijaSection.SIZES)
def test_printed_dimensions(size):
    sec = TilstaSijaSection(size)
    d = sec.dimensions
    p = sec.polygon
    assert p.is_valid and p.exterior.is_ccw
    assert p.bounds == pytest.approx((-d.top_width / 2, 0, d.top_width / 2, d.depth))
    assert width_at(p, d.depth - 1) == pytest.approx(d.top_width)
    assert width_at(p, d.depth - d.flange + 1) == pytest.approx(d.top_width)
    assert width_at(p, d.chamfer) == pytest.approx(d.bottom_width, abs=0.01)
    assert width_at(p, 0.001) == pytest.approx(d.bottom_width - 2 * d.chamfer, abs=0.01)
    assert sec.geometry is not None


def below_flange(size):
    sec = TilstaSijaSection(size)
    h = sec.dimensions.depth
    return sec.polygon.intersection(box(-1000, 0, 1000, h - sec.dimensions.flange)).area / 1e6


@pytest.mark.parametrize("size", ["S-850-700", "S-850-710"])
def test_volume_without_flange_s850(size):
    # "Standartinio gaminio be lentynos 1 m ilgio tūris ~ 0,29 m3" (printed to 2 d.p.)
    assert below_flange(size) == pytest.approx(0.29, abs=0.005)


def test_s1000_volume_note_pinned():
    # Sheet 06 repeats "~0,29 m3" but the fully consistent drawing gives 0.353 m2 below the
    # flange (0.450 m2 total): the note is taken as copied from the S-850 sheet. Pinned.
    assert below_flange("S-1000") == pytest.approx(0.3528, abs=0.001)
    assert TilstaSijaSection("S-1000").published["volume_without_flange_m3_per_m"] == 0.29


def test_provenance():
    assert TilstaSijaSection("S-1000").provenance == "transcribed"
    assert TilstaSijaSection("S-850-710").provenance == "transcribed-with-convention"


def test_invalid():
    with pytest.raises(ValueError):
        TilstaSijaSection("S-1200")
