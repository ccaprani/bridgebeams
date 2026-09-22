"""Source-literal checks independent of the Norwegian implementation table."""
import pytest
from shapely.geometry import LineString, Point

from bridgebeams.no import NoNtbKtbSection

# Fig3.3.2a-j: depth, bottom, stem, top, shoulder, top thickness/haunch.
NTB = [
 ('NTB800-400x1400',1400,800,220,400,197,125,75),
 ('NTB1000-300x1200',1200,1000,220,300,173,125,37),
 ('NTB1200-220x1000',1000,1200,220,220,150,0,0),
 ('NTB1200-220x800',800,1200,220,220,150,0,0),
 ('NTB1200-220x600',600,1200,220,220,150,0,0),
]

@pytest.mark.parametrize('name,h,b,w,t,s,f,a',NTB)
def test_ntb_independent_strip_integral(name,h,b,w,t,s,f,a):
    p=NoNtbKtbSection(name).polygon
    # Horizontal strips: full bottom, rebate, haunch, stem, head.
    expected=b*(s-40)+(b-35)*40+(b-30+w)/2*(265-s)
    expected+=w*(h-f-a-265)+(w+t)/2*a+t*f
    expected-=15**2+2*30**2
    assert p.is_valid and p.exterior.is_ccw
    assert p.area==pytest.approx(expected)
    assert p.centroid.x==pytest.approx(0,abs=1e-10)
    assert p.bounds==(-b/2,0,b/2,h)
    assert p.intersection(LineString([(-2000,h),(2000,h)])).length==t-60
    # Both rebates stay unfilled in gross precast concrete.
    assert not p.covers(Point(b/2-10,s-20))
    assert not p.covers(Point(t/2-15,h-15))

@pytest.mark.parametrize('name,h,b,t,s,f,a,offset',[
 ('KTB570-400x1400',1400,570,370,197,125,75,-30),
 ('KTB1200',1200,670,320,173,125,37,0),
 ('KTB1000',1000,770,280,150,0,0,0),
 ('KTB800',800,770,280,150,0,0,0),
 ('KTB600',600,770,280,150,0,0,0),
])
def test_ktb_independent_integral_and_exterior(name,h,b,t,s,f,a,offset):
    p=NoNtbKtbSection(name).polygon
    expected=b*(s-40)+(b-17.5)*40+(b-15+280)/2*(265-s)
    expected+=280*(h-f-a-265)+(280+t)/2*a+t*f
    expected-=15**2+30**2+offset*h/2
    assert p.is_valid and p.exterior.is_ccw
    assert p.area==pytest.approx(expected)
    assert p.bounds==(offset,0,b,h)
    cut=p.intersection(LineString([(-100,h/2),(1000,h/2)]))
    assert cut.bounds[0]==pytest.approx(offset/2)
    assert cut.bounds[2]==280


def test_unknown_type_rejected():
    with pytest.raises(ValueError): NoNtbKtbSection('KTB900')
