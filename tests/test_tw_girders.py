"""Check Taiwan geometry against independent integration of drawing widths.

This is analytic geometric validation, not published-property validation:
Figure 10/Table 14 contain dimensions but no area or inertia table.
"""

import pytest
from shapely.geometry import LineString

from bridgebeams._geometry import as_polygon, section_properties
from bridgebeams.tw import TaiwanISection

from _aggregate import P, run_checks


# Independently transcribed Figure 10 / Table 14 depths in millimetres.
DEPTHS = {"IV": 1350, "V": 1600, "VI": 1850, "VII": 2000, "VIII": 2100}


def drawing_width_strips(size):
    """(bottom y, top y, bottom width, top width), direct drawing stacks."""
    height = DEPTHS[size]
    if size == "IV":
        return [
            (0, 200, 650, 650),
            (200, 425, 650, 200),
            (425, height - 350, 200, 200),
            (height - 350, height - 200, 200, 500),
            (height - 200, height, 500, 500),
        ]
    return [
        (0, 200, 700, 700),
        (200, 450, 700, 200),
        (450, height - 300, 200, 200),
        (height - 300, height - 200, 200, 400),
        (height - 200, height - 125, 400, 1050),
        (height - 125, height, 1050, 1050),
    ]


def strip_integrals(strips):
    """Integrate linear widths in local strip coordinates, without polygons."""
    area = first = second = 0.0
    for y0, y1, b0, b1 in strips:
        h = y1 - y0
        slope = (b1 - b0) / h
        a = b0 * h + slope * h**2 / 2
        q_local = b0 * h**2 / 2 + slope * h**3 / 3
        i_local = b0 * h**3 / 3 + slope * h**4 / 4
        area += a
        first += y0 * a + q_local
        second += y0**2 * a + 2 * y0 * q_local + i_local
    cy = first / area
    return area, cy, second - area * cy**2


def _check_shape_and_analytic_properties(size):
    beam = TaiwanISection(size)
    poly = beam.polygon
    assert poly.is_valid
    assert poly.exterior.is_ccw
    assert beam.dimensions.depth == DEPTHS[size]
    assert beam.dimensions.clear_web_height > 0
    expected_area, expected_cy, expected_ixx = strip_integrals(drawing_width_strips(size))
    props = section_properties(poly)
    assert poly.area == pytest.approx(expected_area, rel=1e-12)
    assert poly.centroid.y == pytest.approx(expected_cy, rel=1e-12)
    assert props["ixx"] == pytest.approx(expected_ixx, rel=1e-12)
    assert poly.centroid.x == pytest.approx(0, abs=1e-10)
    assert as_polygon(beam.geometry).equals(poly)


def _check_off_grid_slice_widths(size):
    # Samples inside every flange and splay catch shifted y references and
    # top-flange knees even if a coincidental overall area matches.
    poly = TaiwanISection(size).polygon
    for y0, y1, b0, b1 in drawing_width_strips(size):
        y = y0 + 0.37 * (y1 - y0)
        cut = poly.intersection(LineString([(-2000, y), (2000, y)]))
        assert cut.length == pytest.approx(b0 + 0.37 * (b1 - b0), abs=1e-9)


def _check_end_block_lengths_do_not_enter_midspan_profile():
    beam = TaiwanISection("VIII")
    assert beam.published["end_block_B_mm"] == 1600
    assert beam.published["end_block_C_mm"] == 500
    assert beam.polygon.bounds == (-525, 0, 525, 2100)
    # V and VIII differ only by 500 mm of 200 mm web.
    assert beam.polygon.area - TaiwanISection("V").polygon.area == pytest.approx(100000)


def _check_invalid_size(invalid):
    with pytest.raises(ValueError):
        TaiwanISection(invalid)


def test_tw_girders_catalogue_checks():
    run_checks(
        (_check_shape_and_analytic_properties, P("size", DEPTHS)),
        (_check_off_grid_slice_widths, P("size", DEPTHS)),
        _check_end_block_lengths_do_not_enter_midspan_profile,
        (_check_invalid_size, P("invalid", ["I", "IX", "Type IV", "iv", 4])),
    )
