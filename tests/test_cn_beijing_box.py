"""Beijing 20BGQL2 midspan box: printed dimensions and analytic checks.

No section properties are published, so the checks are analytic: printed
chains, void consistency, and closed-form area of the fillet-free outline.
"""
import pytest
from shapely.geometry import LineString

from bridgebeams.cn import Beijing20bgql2BoxSection
from bridgebeams.mx._arcs import ring_properties

from _aggregate import P, run_checks


def _props(p):
    return ring_properties([list(p.exterior.coords)] + [list(r.coords) for r in p.interiors])


def _width(p, y):
    return p.intersection(LineString([(-5000, y), (5000, y)])).length


def _check_sizes_construct_and_bounds(size, a):
    s = Beijing20bgql2BoxSection(size)
    p = s.polygon
    assert p.is_valid and len(p.interiors) == 1
    assert p.bounds == pytest.approx((-2600 - a, 0, 2600 + a, 1800))
    assert s.provenance == "transcribed-with-convention"
    # wing: 200 thick at the tip, flat over a
    assert _width(p, 1700) == pytest.approx(2 * (2600 + a))
    # soffit 2 x 950 less the R50 tangent runs; full chord just above the arc
    assert 1800 < _width(p, 0.001) < 1900
    # at mid-height: outer web on 250:1450 slope minus the void
    y = 800.0
    outer = 2 * (950 + 250 * y / 1450)
    void = 2 * (730 + (916 - 730) * (y - 370) / (1450 - 370))
    assert _width(p, y) == pytest.approx(outer - void, abs=1e-6)


def _check_void_consistent_with_280_web():
    import math
    slope = 250 / 1450
    horiz = 280 * math.sqrt(1 + slope**2)
    # printed 916 / 730 half-widths follow from the 280 normal web within 0.5 mm
    assert 950 + slope * 1450 - horiz == pytest.approx(916, abs=0.5)
    assert 950 + slope * 370 - horiz == pytest.approx(730, abs=0.5)


def _check_analytic_area(a):
    s = Beijing20bgql2BoxSection(a=a, drip_groove=False)
    # Fillet-free closed form (mm2): 2 568 520 at a=0, +2*200*a
    sharp = 2568520 + 400 * a
    area = _props(s.polygon)["area"]
    # R50 corners: convex soffit corner removes, re-entrant wing corner adds;
    # net effect is a few hundred mm2 (arc discretisation included).
    assert area == pytest.approx(sharp, abs=400)
    grooved = _props(Beijing20bgql2BoxSection(a=a).polygon)["area"]
    # Two R20 semicircular grooves; at a=150 the groove centre sits on the
    # wing-soffit kink (6° slope change) so the cut is ~3% more than 2 halves.
    assert area - grooved == pytest.approx(3.14159265 * 400, rel=0.01 if a != 150 else 0.04)


def _check_parameter_limits_and_invalid_size():
    with pytest.raises(ValueError):
        Beijing20bgql2BoxSection("a=150")
    with pytest.raises(ValueError):
        Beijing20bgql2BoxSection(a=301)
    assert Beijing20bgql2BoxSection(a=150).polygon.bounds[2] == pytest.approx(2750)


def _check_geometry_roundtrip():
    s = Beijing20bgql2BoxSection("a=0")
    assert s.geometry.geom.symmetric_difference(s.polygon).area < 1e-3


def test_cn_beijing_box_catalogue_checks():
    run_checks(
        (_check_sizes_construct_and_bounds, P("size,a", [("a=0", 0.0), ("a=300", 300.0)])),
        _check_void_consistent_with_280_web,
        (_check_analytic_area, P("a", [0.0, 150.0, 300.0])),
        _check_parameter_limits_and_invalid_size,
        _check_geometry_roundtrip,
    )
