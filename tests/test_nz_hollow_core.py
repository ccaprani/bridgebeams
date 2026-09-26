"""RR364 p40 source dimensions, void topology, and analytic circle limits."""
import math
import pytest
from shapely.geometry import LineString, Point, Polygon
from bridgebeams.nz.hollow_core import NzHollowCoreSection

from _aggregate import P, run_checks

def _check_independent_area_and_voids(unit,nvoid,key_sides):
    p=NzHollowCoreSection(unit=unit).polygon
    # Rectangle minus upper key recess, main key recess, two bottom corners.
    # Outer unit adds its 15x15 upper exposed corner chamfer.
    key_area=26*157+(26+38)*12/2+38*(430-12-110)
    gross=1144*587-key_sides*key_area-15**2
    if unit=='outer': gross-=15**2/2
    analytic=gross-nvoid*math.pi*184**2
    assert p.is_valid and p.exterior.is_ccw
    assert len(p.interiors)==nvoid
    regular_void=256/2*184**2*math.sin(2*math.pi/256)
    assert p.area==pytest.approx(gross-nvoid*regular_void)
    assert 0 < p.area-analytic < nvoid*math.pi*184**2*(2*math.pi/256)**2/6
    assert p.bounds==(0,0,1144,587)
    assert not p.covers(Point(836,294))
    assert p.covers(Point(308,294)) == (unit=='outer')
    at200=p.intersection(LineString([(-10,200),(1200,200)]))
    assert at200.bounds[0]==(38 if unit=='inner' else 0)
    assert at200.bounds[2]==1106
    assert p.intersection(LineString([(-10,500),(1200,500)])).length==(1092 if unit=='inner' else 1118)
    fine=NzHollowCoreSection(unit=unit,circle_points=512).polygon
    assert abs(fine.area-analytic)<abs(p.area-analytic)/3.99
    assert len(NzHollowCoreSection(unit=unit).geometry.geom.interiors)==nvoid

def _check_invalid_requests(kwargs):
    with pytest.raises(ValueError): NzHollowCoreSection(**kwargs)


def _check_single_inner_dimension_chain(depth,bottom,void_height):
    p=NzHollowCoreSection(depth).polygon
    assert p.is_valid and len(p.interiors)==1
    assert p.bounds==(0,0,1138,depth)
    assert p.centroid.x==pytest.approx(569)
    # Independent outer strips, printed1:80 lower-face draft, and chamfers.
    dx=90/80
    lower=(1138-2*dx)*20-20**2
    lower+=(1138-dx)*90
    key_zone=1070*308+(1070+1094)/2*12
    upper=1094*(depth-430)
    void_area=830*void_height-2*100**2
    assert p.area==pytest.approx(lower+key_zone+upper-void_area)
    hole=Polygon(p.interiors[0])
    assert hole.bounds==(154,bottom,984,depth-140)
    assert p.intersection(LineString([(-1,500),(1140,500)])).bounds[0]==22
    assert p.intersection(LineString([(-1,50),(1140,50)])).bounds[0]==pytest.approx(60/80)


def test_nz_hollow_core_catalogue_checks():
    run_checks(
        (_check_independent_area_and_voids, P('unit,nvoid,key_sides',[('inner',2,2),('outer',1,1)])),
        (_check_invalid_requests, P('kwargs',[{'depth':651},{'depth':650,'unit':'outer'},{'unit':'edge'},{'circle_points':31},{'circle_points':33},{'circle_points':True}])),
        (_check_single_inner_dimension_chain, P('depth,bottom,void_height',[(650,130,380),(900,155,605)])),
    )
