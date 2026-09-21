"""Soyuzdorproekt 3.503.1-81 33 m I-beams: validation against the
producer volume-derived areas (exact) and the drawing-fit tolerance."""

import json
from importlib import resources

import pytest

from bridgebeams._geometry import as_polygon, section_properties
from bridgebeams.ru import Su3503I33Section

DATA = json.loads(
    resources.files("bridgebeams.ru.data").joinpath("su3503_i33.json").read_text()
)


@pytest.mark.parametrize("size", Su3503I33Section.SIZES)
def test_volume_derived_area(size):
    beam = Su3503I33Section(size)
    poly = as_polygon(beam.geometry)
    assert poly.is_valid, size
    props = section_properties(poly)
    # producer volume / length -> exact target; fit tolerance 0.5%
    assert props["area"] == pytest.approx(beam.target_area, rel=0.005), size


def test_stack_and_widths():
    for row in DATA["published_properties"]:
        beam = Su3503I33Section(row["section"])
        assert beam.dimensions.top_width == row["top_width"]
        assert beam.dimensions.height == row["height"]
        assert beam.dimensions.bottom_flange_width == 620.0


def test_symmetric_and_valid():
    for size in Su3503I33Section.SIZES:
        beam = Su3503I33Section(size)
        poly = as_polygon(beam.geometry)
        assert poly.is_valid, size
        xmin, xmax, _, _ = beam.geometry.calculate_extents()
        assert -xmin == pytest.approx(xmax), size


def test_invalid_size_raises():
    with pytest.raises(ValueError):
        Su3503I33Section("B3300.174.123")
