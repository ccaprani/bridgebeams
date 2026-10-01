"""Basic geometry sanity for the ported Australian sections (v3 API)."""

import pytest

from bridgebeams.aus import IGirderSection, SuperTGirderSection
from bridgebeams._geometry import as_polygon, section_properties


def test_supert_depths_match_as5100():
    """Faithful port of bridgebeams 0.1: the profile spans t_f above the
    datum and d below, i.e. total drawn depth = d + t_f (origin at mid
    bottom flange after the original control-point convention)."""
    expected = {1: 675, 2: 925, 3: 1125, 4: 1425, 5: 1725}
    for gtype, depth in expected.items():
        st = SuperTGirderSection(girder_type=gtype)
        _, _, ymin, ymax = st.geometry.calculate_extents()
        assert (ymax - ymin) == pytest.approx(depth + 75.0, abs=1e-6)


def test_supert_symmetric_about_centreline():
    st = SuperTGirderSection(girder_type=3)
    poly = as_polygon(st.geometry)
    # mirror test: mirrored polygon coincides with original
    from shapely.geometry import Polygon

    mirrored = Polygon([(-x, y) for x, y in poly.exterior.coords])
    sym_diff = poly.symmetric_difference(mirrored).area
    assert sym_diff / poly.area < 1e-6


def test_igirder_areas_monotonic():
    areas = []
    for gtype in (1, 2, 3, 4):
        ig = IGirderSection(girder_type=gtype)
        areas.append(section_properties(as_polygon(ig.geometry))["area"])
    assert areas == sorted(areas)


def test_igirder_invalid_type_raises():
    with pytest.raises(ValueError):
        IGirderSection(girder_type=5)
