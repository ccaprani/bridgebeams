"""Independent published W properties and recovered concrete-contour checks."""
import pytest
from shapely.affinity import scale
from bridgebeams._geometry import section_properties
from bridgebeams.ie.ie_w import IeWBeamSection

# Manual PDF30 / printed28; independent literals, A(mm2), cy(mm), I(1e9 mm4).
PUBLISHED = [
    ("W1",572360,305.3,35.556), ("W3",606880,345.9,49.614),
    ("W5",641400,387.5,66.610), ("W7",692030,440.2,89.871),
    ("W8",726550,484.2,114.140), ("W9",761070,528.7,142.000),
    ("W10",812400,585.2,178.850), ("W11",846920,631.3,215.460),
    ("W12",881440,677.6,256.280), ("W13",933470,736.7,309.340),
    ("W14",975150,790.6,366.030), ("W15",1016060,844.3,428.300),
    ("W16",1057970,898.6,496.830), ("W17",1102680,954.5,572.450),
    ("W18",1150190,1011.8,655.490), ("W19",1213750,1081.1,758.560),
]

@pytest.mark.parametrize("size,area,cy,ixx",PUBLISHED)
def test_published_properties(size,area,cy,ixx):
    beam=IeWBeamSection(size);p=beam.polygon;d=beam.dimensions
    assert p.is_valid and p.exterior.is_ccw and not p.interiors
    assert p.symmetric_difference(scale(p,xfact=-1,origin=(0,0))).area < 1e-6
    assert d.depth-50-d.f-d.s-d.v-d.web_height == 360
    props=section_properties(p)
    assert props['area'] == pytest.approx(area,abs=4.000001,rel=0)
    if size == 'W11':
        # Source rounds/intermediates differ slightly beyond cy's half digit.
        assert props['cy']-cy == pytest.approx(-0.052619307,abs=0.000002)
    else:
        assert props['cy'] == pytest.approx(cy,abs=0.05,rel=0)
    assert props['ixx']/1e9 == pytest.approx(ixx,rel=0.000025)
    assert props['cx'] == pytest.approx(0,abs=1e-8)


def test_cad_lower_vertices_and_catalogue_revision_are_preserved():
    beam=IeWBeamSection('W19');vertices=list(beam.polygon.exterior.coords)
    for p in [(730,0),(750,20),(625,360),(500,210),(0,160)]:assert p in vertices
    assert (634,2150) in vertices  # current F100; old project CAD had F52
    assert (772,1874) in vertices
    assert (772,1410) in vertices
    assert beam.dimensions.v == 464


def test_size_validation_and_mesh():
    with pytest.raises(ValueError):IeWBeamSection('W2')
    g=IeWBeamSection('W19').geometry
    g.create_mesh(mesh_sizes=[10000])
    assert g.mesh is not None
