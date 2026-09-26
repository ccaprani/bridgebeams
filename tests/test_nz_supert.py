"""Source geometry regressions for RR 364 S1.01/S1.11/S1.21.

No published area/inertia fixture exists: independent area decomposition
checks the implemented approximation, not manufacturing accuracy.
"""

import pytest
from shapely.affinity import scale
from shapely.geometry import LineString, Point

from bridgebeams._geometry import as_polygon, section_properties
from bridgebeams.nz import NzSuperTSection

from _aggregate import P, run_checks


def _check_source_dimensions_and_open_void(depth, base, low, rise, clear):
    beam = NzSuperTSection(depth)
    dims, poly = beam.dimensions, as_polygon(beam.geometry)
    assert poly.is_valid and poly.exterior.is_ccw
    assert poly.bounds == (-1245, 0, 1245, depth)
    assert dims.bottom_flange_width == base
    assert dims.bottom_flange_height == low
    assert dims.void_rise == rise
    assert dims.web_clear_bottom == clear
    assert poly.contains(Point(0, low - 1))
    assert not poly.covers(Point(0, low + 1))
    assert not poly.covers(Point(0, depth - 50))
    cut = poly.intersection(LineString([(-2000, depth / 2), (2000, depth / 2)]))
    assert cut.geom_type == "MultiLineString"
    assert len(cut.geoms) == 2
    assert all(95 < part.length < 110 for part in cut.geoms)
    assert poly.symmetric_difference(scale(poly, xfact=-1, origin=(0, 0))).area < 1e-8


def _check_independent_trapezoid_area(depth, top):
    beam = NzSuperTSection(depth, top_width=top)
    p = beam.dimensions
    # Outer widths in three vertical bands minus the open valley/void.
    y_h = depth - 175
    w_h = p.bottom_flange_width + 2 * y_h / 10.56
    outer = (p.bottom_flange_width + w_h) * y_h / 2
    outer += (w_h + w_h + 200) * 75 / 2
    outer += top * 100
    valley = p.web_clear_bottom * p.void_rise / 2
    void = (p.web_clear_bottom + 840) * (depth - p.bottom_flange_height - p.void_rise) / 2
    bottom_chamfers = 20 * 20
    tip_chamfers = 20 * 20
    area = outer - valley - void - bottom_chamfers - tip_chamfers
    props = section_properties(beam.polygon)
    assert props["area"] == pytest.approx(area, abs=1e-6)
    assert props["cx"] == pytest.approx(0, abs=1e-9)
    assert props["ixx"] > 0


def _check_30m_drawing_has_narrower_top():
    wide = NzSuperTSection(1225)
    narrow = NzSuperTSection(1225, top_width=1990)
    assert narrow.polygon.bounds == (-995, 0, 995, 1225)
    assert wide.polygon.area - narrow.polygon.area == pytest.approx(500 * 100)


def _check_invalid_source_size_raises(kwargs):
    with pytest.raises(ValueError):
        NzSuperTSection(**kwargs)


def test_nz_supert_catalogue_checks():
    run_checks(
        (_check_source_dimensions_and_open_void, P("depth,base,low,rise,clear", [
    (1025, 852, 240, 67, 709),
    (1225, 814, 260, 64, 674),
])),
        (_check_independent_trapezoid_area, P("depth,top", [(1025, 2490), (1225, 2490), (1225, 1990)])),
        _check_30m_drawing_has_narrower_top,
        (_check_invalid_source_size_raises, P("kwargs", [
    {"depth": 1100}, {"depth": 1025, "top_width": 1990},
    {"depth": 1225, "top_width": 2500}, {"depth": 1225, "top_width": float("nan")},
])),
    )
