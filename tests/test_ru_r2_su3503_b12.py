"""Soyuzdorproekt 3.503.1-81 Vypusk 5-1 12 m beams (midspan section)."""

import pytest
from shapely.geometry import LineString

from bridgebeams._geometry import section_properties
from bridgebeams.ru.r2_su3503_b12 import Su3503B12Section


def width_at(poly, y):
    return poly.intersection(LineString([(-5000, y), (5000, y)])).length


@pytest.mark.parametrize("size", Su3503B12Section.SIZES)
def test_valid_and_printed_dims(size):
    sec = Su3503B12Section(size)
    p, d = sec.polygon, sec.dimensions
    assert p.is_valid and p.exterior.is_ccw
    assert p.bounds == pytest.approx((-d.slab_left, 0, d.slab_right, 900))
    # marked width "по бетону" = 1040 + e (edge) or 2e (intermediate)
    assert d.slab_left + d.slab_right == pytest.approx(d.top_width)
    assert int(size.split(".")[1]) * 10 == d.top_width
    assert width_at(p, 0.01) == pytest.approx(600, abs=0.1)
    assert width_at(p, 100) == pytest.approx(620, abs=2)  # 1:1 splay lands on 620
    assert width_at(p, 430) == pytest.approx(160)  # straight web between fillets
    assert width_at(p, 800) == pytest.approx(d.top_width)
    assert sec.geometry is not None


@pytest.mark.parametrize("size", Su3503B12Section.SIZES)
def test_mass_is_2_5_t_per_m3(size):
    pub = Su3503B12Section(size).published
    assert pub["mass_t"] / pub["volume_m3"] == pytest.approx(2.5, abs=0.01)


@pytest.mark.parametrize("size", Su3503B12Section.SIZES)
def test_midspan_area_vs_published_volume(size):
    """Pinned: midspan area x 12 m is 3.0-3.5 % below the published volume,
    a constant ~0.20 m3 excess for all marks (thickened support webs and end
    details, not modelled)."""
    sec = Su3503B12Section(size)
    a = section_properties(sec.polygon)["area"]
    excess = sec.published["volume_m3"] - a * 12000 / 1e9
    assert excess == pytest.approx(0.2007, abs=0.002)
    assert 0.964 < a / sec.volume_area < 0.972


def test_volume_steps_equal_slab_width_steps():
    """Published volume differences = slab width difference x 150 x 12 m."""
    area = {s: section_properties(Su3503B12Section(s).polygon)["area"] for s in Su3503B12Section.SIZES}
    vol = {s: Su3503B12Section(s).published["volume_m3"] for s in Su3503B12Section.SIZES}
    for a, b in [("B1200.174.90", "B1200.194.90"), ("B1200.140.90", "B1200.180.90"), ("B1200.140.90", "B1200.174.90")]:
        assert (area[b] - area[a]) * 12000 / 1e9 == pytest.approx(vol[b] - vol[a], abs=0.005)


def test_edge_beam_is_asymmetric():
    d = Su3503B12Section("B1200.194.90").dimensions
    assert (d.slab_left, d.slab_right) == (1040.0, 900.0)
    assert Su3503B12Section("B1200.174.90").provenance == "transcribed-with-convention"
    assert Su3503B12Section("B1200.140.90").provenance == "transcribed"


def test_invalid():
    with pytest.raises(ValueError):
        Su3503B12Section("B1406.130.93")
