"""Independent source-table checks for SEPSA's seven published outlines."""

import pytest
from shapely.affinity import scale

from bridgebeams._geometry import as_polygon, section_properties
from bridgebeams.mx import SepsaIGirderSection


# Source p4: published areas (m2), independently transcribed from the table.
PUBLISHED = {
    "I-MODIFIED": (0.2106, 540),
    "II": (0.2321, 910),
    "III": (0.3625, 1150),
    "IV": (0.4970, 1350),
    "IV-MODIFIED": (0.5233, 1350),
    "V": (0.6451, 1600),
    "VI": (0.6911, 1830),
}


@pytest.mark.parametrize("size", PUBLISHED)
def test_geometry_matches_published_area_and_depth(size):
    expected_area, depth = PUBLISHED[size]
    poly = as_polygon(SepsaIGirderSection(size).geometry)
    assert poly.is_valid
    assert poly.exterior.is_ccw
    assert poly.area == pytest.approx(expected_area * 1e6, abs=50.000001, rel=0)
    assert poly.bounds[1] == 0
    assert poly.bounds[3] == depth
    assert poly.symmetric_difference(scale(poly, xfact=-1, origin=(0, 0))).area < 1e-8
    props = section_properties(poly)
    assert abs(props["cx"]) < 1e-9
    assert 0 < props["cy"] < depth
    assert props["ixx"] > 0


def test_modified_i_area_from_independent_layer_calculation():
    # Two 590x100 flanges, two 100-deep trapezoids and a 140x140 web.
    analytical = 2 * 590 * 100 + 2 * (590 + 140) / 2 * 100 + 140 * 140
    assert SepsaIGirderSection("I-MODIFIED").polygon.area == analytical == 210600


def test_modifications_are_distinct_and_explicit():
    normal = SepsaIGirderSection("IV")
    modified = SepsaIGirderSection("IV-MODIFIED")
    assert normal.dimensions.top_flange_width == 500
    assert modified.dimensions.top_flange_width == 1250
    assert modified.polygon.area - normal.polygon.area == 26250
    with pytest.raises(ValueError):
        SepsaIGirderSection("I")


def test_sectionproperties_mesh_smoke():
    geometry = SepsaIGirderSection("VI").geometry
    geometry.create_mesh(mesh_sizes=[10000])
    assert geometry.mesh is not None
