"""Independent published properties and open-top topology for Qatar Q-beams."""

import pytest
from shapely.geometry import Point, LineString

from bridgebeams._geometry import as_polygon, section_properties
from bridgebeams.qa import QaQBeamSection

from _aggregate import P, run_checks

# Directly transcribed SD 5-1-101 property-table fixtures, not implementation data.
PUBLISHED = [
    ("T1", 800, 565861, 381, 4.043e10),
    ("T2", 1050, 611622, 496, 8.182e10),
    ("T3", 1250, 661823, 588, 12.761e10),
    ("T4", 1550, 716068, 740, 21.633e10),
    ("T5", 1900, 815801, 903, 36.251e10),
]


def _check_source_table_and_topology(kind, depth, area, cy, ixx):
    beam = QaQBeamSection(kind)
    poly = as_polygon(beam.geometry)
    assert poly.is_valid and poly.exterior.is_ccw
    assert poly.bounds == (-1075, 0, 1075, depth)
    p = section_properties(poly)
    assert p["area"] == pytest.approx(area, rel=0.01)
    assert p["cy"] == pytest.approx(cy, rel=0.01)
    assert p["ixx"] == pytest.approx(ixx, rel=0.015)
    assert p["cx"] == pytest.approx(0, abs=1e-8)
    assert not poly.covers(Point(0, depth - 10))
    assert poly.contains(Point(0, beam.dimensions.valley_height - 1))
    assert not poly.covers(Point(0, beam.dimensions.valley_height + 1))
    cut = poly.intersection(LineString([(-2000, depth / 2), (2000, depth / 2)]))
    assert cut.geom_type == "MultiLineString"
    assert len(cut.geoms) == 2


def _check_t1_independent_integrated_area():
    # Gross outer trapezoid + haunch zone + flange band minus opening.
    d, b, low, rise, slope = 800, 939, 290, 71, 10.55
    yh = d - 117 - 75
    wh = b + 2 * yh / slope
    outer = (b + wh) * yh / 2 + (wh + 1469) * 75 / 2 + 2150 * 117
    xi = 420 - (d - 25 - low - rise) / slope
    void = xi * rise + (2 * xi + 840) * (d - 25 - low - rise) / 2
    void += 890 * 25
    # Two bottom corners and four flange-tip corners.
    chamfers = 3 * 13**2
    assert QaQBeamSection("T1").polygon.area == pytest.approx(outer - void - chamfers)


def _check_invalid_type(invalid):
    with pytest.raises(ValueError):
        QaQBeamSection(invalid)


def test_qa_q_beams_catalogue_checks():
    run_checks(
        (_check_source_table_and_topology, P("kind,depth,area,cy,ixx", PUBLISHED)),
        _check_t1_independent_integrated_area,
        (_check_invalid_type, P("invalid", ["T0", "T6", 1, None])),
    )
