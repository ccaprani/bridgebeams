"""Independent source chains and nominal geometry for rechecked RR364 sheets."""

import pytest
from shapely.geometry import LineString, Point, Polygon

from bridgebeams._geometry import section_properties
from bridgebeams.nz import NzHollowCoreSection, NzIBeamSection
from bridgebeams.nz._sources import rr364_record


def test_i1500_independent_nominal_properties():
    # Independent strip integration of the labeled S4.01 stations, with
    # two 20 x 20 chamfers and sharp nominal web-haunch intersections.
    section = NzIBeamSection(1500)
    polygon = section.polygon
    properties = section_properties(polygon)
    assert polygon.is_valid and polygon.exterior.is_ccw
    assert polygon.bounds == (-237.5, 0, 237.5, 1500)
    assert properties["area"] == pytest.approx(363100, abs=1e-7)
    assert polygon.centroid.y == pytest.approx(676.0391994859084, abs=1e-9)
    assert properties["cy"] == pytest.approx(676.0391994859084, abs=1e-9)
    assert properties["ixx"] == pytest.approx(88784866625.39398, rel=1e-12)
    assert polygon.intersection(LineString([(-500, 0), (500, 0)])).length == 435
    assert "sharp nominal junctions" in " ".join(section.geometry_conventions)


@pytest.mark.parametrize("depth,bottom,void_height,rise,run", [
    (650, 130, 380, 80, 1),
    (900, 155, 605, 140, 1.5),
])
def test_single_core_source_chains_and_nominal_draft(depth, bottom, void_height, rise, run):
    section = NzHollowCoreSection(depth)
    polygon = section.polygon
    assert polygon.is_valid and polygon.exterior.is_ccw
    assert len(polygon.interiors) == 1
    assert not polygon.interiors[0].is_ccw
    assert polygon.bounds == (0, 0, 1138, depth)
    hole = Polygon(polygon.interiors[0])
    assert hole.bounds == (154, bottom, 984, depth-140)
    assert hole.area == 830*void_height-2*100**2
    assert not polygon.covers(Point(569, (bottom+depth-140)/2))
    exterior = Polygon(polygon.exterior)
    horizontal = lambda y: exterior.intersection(LineString([(-10, y), (1148, y)]))
    # Printed top/max-width labels and the expressly documented ledge datum.
    assert horizontal(depth).length == 1094
    assert horizontal(110).length == 1138
    assert horizontal(50).bounds[0] == pytest.approx(60*run/rise)
    assert horizontal(0).length == pytest.approx(1138-2*(20+90*run/rise))
    assert section.dimensions.lower_face_slope == run/rise
    labels = section.source_record["dimensions"]
    assert sum(labels["lower_horizontal_labels"]) == 1138
    void = labels["void"]
    assert sum(void[name] for name in (
        "top_cover", "upper_corner_vertical", "straight_side_height",
        "lower_corner_vertical", "bottom_cover",
    )) == depth
    assert "nominal interpretation" in " ".join(section.geometry_conventions)


def test_900_draft_does_not_reuse_650_slope():
    lower650 = NzHollowCoreSection(650).polygon.intersection(
        LineString([(-10, 50), (1148, 50)])
    ).bounds[0]
    lower900 = NzHollowCoreSection(900).polygon.intersection(
        LineString([(-10, 50), (1148, 50)])
    ).bounds[0]
    assert lower650 == pytest.approx(0.75)
    assert lower900 == pytest.approx(9/14)
    assert lower900 != lower650


@pytest.mark.parametrize("depth", [650.0, 900.0])
def test_integral_float_depth_preserves_existing_numeric_api(depth):
    floating = NzHollowCoreSection(depth)
    integer = NzHollowCoreSection(int(depth))
    assert type(floating.depth) is float
    assert floating.depth == depth
    assert floating.polygon.equals_exact(integer.polygon, tolerance=0)
    assert floating.source_record == integer.source_record


@pytest.mark.parametrize("depth,first_label,total,top_width", [
    (650, 324, 1078, 1122),
    (900, 334, 1088, 1123),
])
def test_partial_outer_records_are_retained_without_construction(depth, first_label, total, top_width):
    record = rr364_record(f"hollow_core_{depth}_outer")
    assert record["status"] == "partial_dimensions"
    assert record["implemented"] is False
    assert record["dimensions"]["top_width"] == top_width
    assert record["dimensions"]["lower_horizontal_labels"][0] == first_label
    assert sum(record["dimensions"]["lower_horizontal_labels"]) == total
    assert total != record["dimensions"]["lower_width"]
    assert "different datums" in " ".join(record["gaps"])
    with pytest.raises(ValueError, match="endpoints remain unresolved"):
        NzHollowCoreSection(depth, unit="outer")


def test_packaged_provenance_isolated_from_caller_mutation():
    record = rr364_record("i_1500")
    assert record["source"]["pdf_sha256"] == "ea199fa1dfa3272c8c31bbe8ee200c616536fae4a25418ae084d51841b01fd6d"
    assert record["locator"]["pdf_page_one_based"] == 45
    assert record["locator"]["drawing_number"] == "S4.01"
    record["dimensions"]["depth"] = 0
    record["source"]["pdf_sha256"] = "changed"
    assert rr364_record("i_1500")["dimensions"]["depth"] == 1500
    assert NzIBeamSection(1500).source_record["source"]["pdf_sha256"] != "changed"
    section = NzHollowCoreSection(900)
    polygon_before = section.polygon
    record = section.source_record
    record["dimensions"]["void"]["bottom_cover"] = 0
    assert section.polygon.equals_exact(polygon_before, tolerance=0)


def test_earlier_1600_and_587_geometry_is_preserved():
    beam = NzIBeamSection(1600)
    assert beam.source_record is None
    assert beam.polygon.area == 454925
    assert beam.polygon.centroid.y == pytest.approx(716.059148943965)
    for unit, area, cx, cy, holes in (
        ("inner", 426260.83478484023, 572, 290.67051513021073, 2),
        ("outer", 548669.4173924201, 504.59970551274387, 292.40088772549086, 1),
    ):
        section = NzHollowCoreSection(587, unit=unit)
        polygon = section.polygon
        assert section.source_record is None
        assert polygon.area == pytest.approx(area)
        assert (polygon.centroid.x, polygon.centroid.y) == pytest.approx((cx, cy))
        assert len(polygon.interiors) == holes
