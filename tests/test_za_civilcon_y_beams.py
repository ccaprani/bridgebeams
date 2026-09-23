"""Check producer properties and visually confirmed Civilcon Y boundaries."""
import pytest
from shapely.geometry import LineString

from bridgebeams._geometry import section_properties
from bridgebeams.za.civilcon_y_beam import CivilconYBeamSection

from _aggregate import P, run_checks


def _check_source_dimensions_and_properties(size,h,w,area,cy,zt,zb):
    section=CivilconYBeamSection(size)
    p=section.polygon
    assert p.is_valid
    assert p.bounds == (-375.0,0.0,375.0,float(h))
    assert p.intersection(LineString([(-1000,h),(1000,h)])).length == pytest.approx(w)
    # Raised central face is50deep; below the ledge the sloping web resumes.
    assert p.intersection(LineString([(-1000,h-25),(1000,h-25)])).length == pytest.approx(w)
    assert p.intersection(LineString([(-1000,h-50),(1000,h-50)])).length == pytest.approx(w+80)
    assert p.intersection(LineString([(-1000,0),(1000,0)])).length == pytest.approx(700)
    assert p.intersection(LineString([(-1000,202),(1000,202)])).length == pytest.approx(740)
    props=section_properties(p)
    assert props['cx'] == pytest.approx(0,abs=1e-10)
    # Published widths are rounded to1mm; source centroids rounded to1mm.
    assert props['area'] == pytest.approx(area,rel=0.0004)
    assert props['cy'] == pytest.approx(cy,abs=0.5)
    calculated_zt=props['ixx']/(h-props['cy'])
    calculated_zb=props['ixx']/props['cy']
    if size == 'Y1':
        # Literal source Y1 modulus discrepancy: retain and quantify it.
        assert calculated_zt/zt-1 == pytest.approx(0.0033978,abs=1e-6)
        assert calculated_zb/zb-1 == pytest.approx(0.0016862,abs=1e-6)
    else:
        assert calculated_zt == pytest.approx(zt,rel=0.001)
        assert calculated_zb == pytest.approx(zb,rel=0.001)
    # sectionproperties rounds coordinates when constructing its geometry.
    assert section.geometry.geom.symmetric_difference(p).area < 1e-6


def _check_invalid_size():
    with pytest.raises(ValueError):
        CivilconYBeamSection('Y9')


ROWS = [
    ('Y1',700,198,309245,255,24.78e6,43.24e6),
    ('Y2',800,227,339943,299,35.06e6,58.75e6),
    ('Y3',900,256,373525,347,47.90e6,76.33e6),
    ('Y4',1000,285,409990,400,63.59e6,95.38e6),
    ('Y5',1100,313,449339,456,82.13e6,116.00e6),
    ('Y6',1200,342,491572,515,103.69e6,137.92e6),
    ('Y7',1300,371,536689,576,128.28e6,161.24e6),
    ('Y8',1400,400,584688,639,156.07e6,185.86e6),
]


def test_za_civilcon_y_beams_catalogue_checks():
    run_checks(
        (_check_source_dimensions_and_properties, P('size,h,w,area,cy,zt,zb', ROWS)),
        _check_invalid_size,
    )


def test_civilcon_y1_published_moduli_discrepancy_pinned():
    run_checks((_check_source_dimensions_and_properties, P('size,h,w,area,cy,zt,zb', ROWS[:1])))
