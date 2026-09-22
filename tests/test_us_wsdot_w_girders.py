"""WSDOT W-series figures against published 2025 gross properties."""

import pytest
from shapely.affinity import scale

from bridgebeams._geometry import as_polygon, section_properties
from bridgebeams.us import WsdotWSection


# WSDOT Bridge Design Manual M 23-50.24, Table 5.6.1-1, printed p. 5-85.
# Values are literal source-table readings rather than copied from the JSON.
PUBLISHED = {
    "W42G": (42, 15, 20, 373.25, 18.94, 76092, 5408),
    "W50G": (50, 20, 25, 525.5, 22.81, 164958, 13363),
    "W58G": (58, 25, 25, 603.5, 28.00, 264609, 17065),
    "W74G": (73.5, 43, 25, 746.7, 38.08, 546110, 34759),
}


def _iy_about_centroid(poly):
    # Direct Green-theorem integration of x² about the symmetry axis.
    pts = list(poly.exterior.coords)
    return abs(
        sum(
            (x * x + x * u + u * u) * (x * v - u * y) / 12
            for (x, y), (u, v) in zip(pts, pts[1:])
        )
    )


@pytest.mark.parametrize("size", PUBLISHED)
def test_source_dimensions_and_gross_properties(size):
    depth, top, bottom, area, yb, ix, iy = PUBLISHED[size]
    section = WsdotWSection(size)
    d = section.dimensions
    assert d.depth == depth * 25.4
    assert d.top_flange_width == top * 25.4
    assert d.bottom_flange_width == bottom * 25.4
    assert d.web_width == 6 * 25.4

    poly = as_polygon(section.geometry)
    assert poly.is_valid
    assert poly.exterior.is_ccw
    half_width = max(top, bottom) * 12.7
    assert poly.bounds == pytest.approx((-half_width, 0, half_width, depth * 25.4))
    assert poly.symmetric_difference(scale(poly, xfact=-1, origin=(0, 0))).area < 1e-7

    props = section_properties(poly)
    assert props["area"] / 25.4**2 == pytest.approx(area, abs=0.05)
    assert props["cy"] / 25.4 == pytest.approx(yb, abs=0.005)
    assert abs(props["cx"]) < 1e-9
    assert props["ixx"] / 25.4**4 == pytest.approx(ix, abs=0.5)
    assert _iy_about_centroid(poly) / 25.4**4 == pytest.approx(iy, abs=0.5)


def test_drawing_features_are_not_smoothed_or_omitted():
    # June 2006 printed drawing 5.6-A1-1, PDF p. 440. Coordinates in inches.
    w42 = WsdotWSection("W42G").dimensions.right_half
    for actual, expected in zip(
        w42,
        [(0, 0), (9, 0), (10, 1), (10, 5), (3, 7), (3, 37), (7.5, 38.5), (7.5, 42)],
    ):
        assert (actual[0] / 25.4, actual[1] / 25.4) == pytest.approx(expected)
    w74 = WsdotWSection("W74G").dimensions.right_half
    for actual, expected in zip(
        w74[-4:], [(3, 66), (5, 68), (21.5, 70.625), (21.5, 73.5)]
    ):
        assert (actual[0] / 25.4, actual[1] / 25.4) == pytest.approx(expected)
    with pytest.raises(ValueError):
        WsdotWSection("WF42G")


def test_sectionproperties_mesh_smoke():
    geometry = WsdotWSection("W74G").geometry
    geometry.create_mesh(mesh_sizes=[20000])
    assert geometry.mesh is not None
