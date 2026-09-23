"""Spanish HP-1 (1977) Types I–VI midspan sections."""

import math

import pytest

from bridgebeams._geometry import section_properties
from bridgebeams.es import Hp1BeamSection

# (depth, top, web, bottom) in mm and the published Mediciones per metre:
# hormigón m³/m (3 decimals) and molde m²/m (2 decimals).
EXPECTED = {
    "I": (1300, 800, 160, 560, 0.445, 3.74),
    "II": (1500, 800, 160, 600, 0.504, 4.21),
    "III": (1700, 900, 160, 700, 0.620, 4.82),
    "IV": (1900, 1000, 190, 750, 0.753, 5.33),
    "V": (2100, 1100, 190, 800, 0.842, 5.89),
    "VI": (2300, 1200, 190, 800, 0.934, 6.37),
}


@pytest.mark.parametrize("size", Hp1BeamSection.SIZES)
def test_valid_ccw_and_bounds(size):
    sec = Hp1BeamSection(size)
    poly = sec.polygon
    depth, top, web, bottom, _, _ = EXPECTED[size]
    assert poly.is_valid and poly.exterior.is_ccw
    assert poly.bounds == pytest.approx((-top / 2, 0, top / 2, depth))
    assert sec.dimensions.web_width == web
    assert sec.dimensions.bottom_width == bottom
    assert sec.source_status == "historic 1977 standard"
    assert sec.provenance == "transcribed"
    assert sec.geometry is not None


@pytest.mark.parametrize("size", Hp1BeamSection.SIZES)
def test_area_matches_published_concrete_volume(size):
    # Published m³/m is rounded to 0.001 m² → ±500 mm² half-unit.
    area = section_properties(Hp1BeamSection(size).polygon)["area"]
    assert abs(area - EXPECTED[size][4] * 1e6) <= 500.0 + 1e-6


@pytest.mark.parametrize("size", Hp1BeamSection.SIZES)
def test_formwork_matches_published_molde(size):
    # Molde m²/m = wetted perimeter excluding the top (deck-contact) face;
    # rounded to 0.01 m → ±5 mm.
    coords = list(Hp1BeamSection(size).polygon.exterior.coords)
    perim = sum(math.dist(a, b) for a, b in zip(coords, coords[1:]))
    top = EXPECTED[size][1]
    assert abs(perim - top - EXPECTED[size][5] * 1000) <= 5.0 + 1e-6


def test_centroid_below_mid_depth_type_i():
    props = section_properties(Hp1BeamSection("I").polygon)
    assert 0.40 * 1300 < props["cy"] < 0.55 * 1300


def test_invalid_size():
    with pytest.raises(ValueError):
        Hp1BeamSection("VII")
