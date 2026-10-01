"""Independent current MDOT source stations, not property-fitted outlines.

PC-1Q/2L/4J/5D (12-22-2025), PDF page 1. The straight-profile
references integrate the published horizontal width stations analytically.
The 1800 reference solves offset lines for the published tangent circles.
"""

import math

import pytest
from shapely.affinity import scale
from shapely.geometry import LineString

from bridgebeams.us.state_common import gross_properties
from bridgebeams.us.state_r4_mi_mdot_standard import (
    MiMdot1800Section,
    MiMdot70ISection,
    MiMdotBulbTeeSection,
    MiMdotISection,
)

INCH = 25.4

# These stations are transcribed directly from current PC-1Q and PC-2L,
# independent of the implementation JSON. Each pair is (height, full width).
I_STATIONS = {
    "I28": [(0, 14.5), (.75, 16), (5, 16), (10, 6), (21, 6), (24, 12), (28, 12)],
    "I36": [(0, 16.5), (.75, 18), (6, 18), (12, 6), (27, 6), (30, 12), (36, 12)],
    "I45": [(0, 20.5), (.75, 22), (7, 22), (14.5, 7), (33.5, 7), (38, 16), (45, 16)],
    "I54": [(0, 24.5), (.75, 26), (8, 26), (17, 8), (40, 8), (46, 20), (54, 20)],
}
I70_STATIONS = [(0, 24.5), (.75, 26), (7.5, 26), (11, 6),
                (60.5, 6), (62, 10), (64, 30), (70, 30)]


def _bt_stations(depth):
    return [(0, 38.5), (.75, 40), (5.5, 40), (12.5, 12), (14.5, 8),
            (depth - 11, 8), (depth - 8, 14), (depth - 5, 49), (depth, 49)]


STRAIGHT_PROFILES = (
    [(MiMdotISection, size, stations) for size, stations in I_STATIONS.items()]
    + [(MiMdot70ISection, "I70", I70_STATIONS)]
    + [(MiMdotBulbTeeSection, f"BT{depth}", _bt_stations(depth))
       for depth in range(36, 73, 6)]
)
ALL_PROFILES = [(cls, size) for cls, size, _ in STRAIGHT_PROFILES] + [(MiMdot1800Section, "1800")]


def _width_at(polygon, height_in):
    line = LineString([(-100 * INCH, height_in * INCH), (100 * INCH, height_in * INCH)])
    return polygon.intersection(line).length / INCH


def _slab_properties(stations):
    """Integrate linear width functions; no polygon/shoelace reference."""
    area = first = second = 0.0
    for (y0, width0), (y1, width1) in zip(stations, stations[1:]):
        slope = (width1 - width0) / (y1 - y0)
        intercept = width0 - slope * y0
        area += intercept * (y1 - y0) + slope * (y1**2 - y0**2) / 2
        first += intercept * (y1**2 - y0**2) / 2 + slope * (y1**3 - y0**3) / 3
        second += intercept * (y1**3 - y0**3) / 3 + slope * (y1**4 - y0**4) / 4
    return area, first / area, second - first**2 / area


@pytest.mark.parametrize("cls,size", ALL_PROFILES)
def test_all_thirteen_current_midspan_profiles(cls, size):
    section = cls(size)
    polygon = section.polygon
    assert polygon.is_valid and polygon.exterior.is_ccw
    assert polygon.bounds[1] == pytest.approx(0, abs=1e-9)
    assert polygon.bounds[3] == pytest.approx(section.row["depth"] * INCH)
    assert polygon.symmetric_difference(scale(polygon, xfact=-1, origin=(0, 0))).area < 1e-6
    assert section.dimensions.depth == pytest.approx(section.row["depth"] * INCH)
    # Every source specifies a straight 3/4 in soffit bevel, including 1800.
    half_bottom = section.dimensions.bottom_width / INCH / 2
    vertices = list(polygon.exterior.coords)
    for x, y in [(half_bottom - .75, 0), (half_bottom, .75)]:
        assert any(abs(px / INCH - x) < 1e-9 and abs(py / INCH - y) < 1e-9
                   for px, py in vertices)


@pytest.mark.parametrize("cls,size,stations", STRAIGHT_PROFILES)
def test_dimensioned_stations_and_analytical_properties(cls, size, stations):
    polygon = cls(size).polygon
    for y, width in stations:
        assert _width_at(polygon, y) == pytest.approx(width, abs=1e-8)
    expected = _slab_properties(stations)
    actual = gross_properties(polygon, INCH)
    assert actual["area"] == pytest.approx(expected[0], rel=1e-11)
    assert actual["yb"] == pytest.approx(expected[1], rel=1e-11)
    assert actual["ix"] == pytest.approx(expected[2], rel=1e-11)


def test_i70_short_upper_haunch_and_current_i28_tip():
    polygon = MiMdot70ISection("I70").polygon
    assert _width_at(polygon, 62) == pytest.approx(10)
    assert _width_at(polygon, 63) == pytest.approx(20)
    assert _width_at(MiMdotISection("I28").polygon, 24) == pytest.approx(12)


def _circle_from_offset_lines(previous, corner, following, radius):
    """Intersect independently offset incoming/outgoing line equations."""
    incoming = (corner[0] - previous[0], corner[1] - previous[1])
    outgoing = (following[0] - corner[0], following[1] - corner[1])
    incoming = tuple(v / math.hypot(*incoming) for v in incoming)
    outgoing = tuple(v / math.hypot(*outgoing) for v in outgoing)
    normals = [(-incoming[1], incoming[0]), (-outgoing[1], outgoing[0])]
    turn = incoming[0] * outgoing[1] - incoming[1] * outgoing[0]
    rhs = math.copysign(radius, turn)
    (a, b), (c, d) = normals
    determinant = a * d - b * c
    offset = (rhs * (d - b) / determinant, rhs * (a - c) / determinant)
    centre = (corner[0] + offset[0], corner[1] + offset[1])
    tangencies = []
    for direction in (incoming, outgoing):
        projection = sum(v * w for v, w in zip(offset, direction))
        tangencies.append(tuple(corner[i] + projection * direction[i] for i in (0, 1)))
    return centre, tangencies


def test_1800_source_radii_and_tangent_stations():
    # Sharp intersections come only from the published width/vertical chains.
    stations = [(0, 0), (17, 0), (17.75, .75), (17.75, 5.875),
                (2.9375, 11.375), (2.9375, 65.875),
                (23.625, 67.875), (23.625, 70.875), (0, 70.875)]
    half = [(x / INCH, y / INCH) for x, y in MiMdot1800Section("1800").dimensions.right_half]
    for index, radius in [(3, 2), (4, 7.875), (5, 7.875), (6, 2)]:
        centre, tangencies = _circle_from_offset_lines(
            stations[index - 1], stations[index], stations[index + 1], radius
        )
        for tangent in tangencies:
            assert any(math.dist(point, tangent) < 1e-9 for point in half)
        on_circle = [point for point in half if abs(math.dist(point, centre) - radius) < 1e-9]
        assert len(on_circle) == 17  # 16 chords, source radii unchanged


def test_unresolved_variants_remain_explicit_partial_dimensions():
    from bridgebeams.us.state_r4_mi_mdot_standard import _data

    data = _data()
    for group, key in [("i70", "end_face"), ("bulb_tee", "61_in_flange")]:
        partial = data[group]["partial_sections"][key]
        assert partial["status"] == "partial_dimensions" and not partial["implemented"]
        assert partial["unresolved"]
    assert MiMdot70ISection.SIZES == ("I70",)
    assert MiMdotBulbTeeSection.SIZES == tuple(f"BT{depth}" for depth in range(36, 73, 6))
