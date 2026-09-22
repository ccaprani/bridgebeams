"""Checks against independently transcribed Banagher Solid Box properties."""

import pytest
from shapely.affinity import scale

from bridgebeams._geometry import as_polygon, section_properties
from bridgebeams.ie.ie_solid_box import IeSolidBoxBeamSection


# PDF p14 / printed p12: area mm2, centroid mm, top and bottom Z in 1e6 mm3.
PUBLISHED = {
    1: [
        (118630, 141.5, 5.85, 6.55), (155130, 190.6, 10.37, 11.39),
        (191630, 240.0, 16.11, 17.46), (228130, 289.6, 23.09, 24.75),
        (264630, 339.3, 31.28, 33.26), (301130, 389.1, 40.70, 42.98),
        (337630, 438.9, 51.34, 53.93), (374130, 488.8, 63.19, 66.09),
    ],
    2: [
        (195125, 144.9, 9.70, 10.39), (257125, 194.3, 17.19, 18.20),
        (319125, 244.0, 26.77, 28.09), (381125, 293.8, 38.42, 40.05),
        (443125, 343.6, 52.15, 54.09), (505125, 393.5, 67.94, 70.19),
        (567125, 443.4, 85.81, 88.36), (629125, 493.3, 105.74, 108.60),
    ],
    3: [
        (261125, 146.2, 13.01, 13.69), (345125, 195.8, 23.07, 24.07),
        (429125, 245.5, 35.95, 37.26), (513125, 295.4, 51.64, 53.25),
        (597125, 345.3, 70.13, 72.05), (681125, 395.2, 91.43, 93.66),
        (765125, 445.1, 115.52, 118.06), (849125, 495.1, 142.42, 145.26),
    ],
}


@pytest.mark.parametrize("width_class", [1, 2, 3])
@pytest.mark.parametrize("depth_index", range(8))
def test_matches_published_properties(width_class, depth_index):
    beam = IeSolidBoxBeamSection(f"SD{depth_index + 1} ({width_class})")
    poly = as_polygon(beam.geometry)
    expected_area, yc, zt, zb = PUBLISHED[width_class][depth_index]
    depth = 300 + 100 * depth_index
    width = {1: 495, 2: 750, 3: 970}[width_class]
    assert poly.is_valid and poly.exterior.is_ccw
    assert poly.bounds == (-width / 2, 0, width / 2, depth)
    assert poly.symmetric_difference(scale(poly, xfact=-1, origin=(0, 0))).area < 1e-8
    props = section_properties(poly)
    assert props["area"] == pytest.approx(expected_area, abs=5.000001, rel=0)
    assert props["cx"] == pytest.approx(0, abs=1e-9)
    assert props["cy"] == pytest.approx(yc, abs=0.05, rel=0)
    # Published 0.01-unit rounding plus a 0.0002 allowance for intermediate
    # source rounding; the measured maximum discrepancy is 0.005183.
    assert props["ixx"] / (depth - props["cy"]) / 1e6 == pytest.approx(
        zt, abs=0.0052, rel=0
    )
    assert props["ixx"] / props["cy"] / 1e6 == pytest.approx(
        zb, abs=0.0052, rel=0
    )


def test_area_from_independent_layer_calculation():
    # Upper-width rectangle plus two lower wings, less two corner triangles.
    expected = 620 * 300 + 2 * (65 * 60 + 65 * 30 / 2 - 25 * 25 / 2)
    assert IeSolidBoxBeamSection("SD1 (2)").polygon.area == expected == 195125


def test_unresolved_width_is_not_exposed():
    assert len(IeSolidBoxBeamSection.SIZES) == 24
    with pytest.raises(ValueError):
        IeSolidBoxBeamSection("SD1 (4)")


def test_sectionproperties_mesh_smoke():
    geometry = IeSolidBoxBeamSection("SD8 (3)").geometry
    geometry.create_mesh(mesh_sizes=[10000])
    assert geometry.mesh is not None
