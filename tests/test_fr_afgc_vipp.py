"""AFGC F-04 as-surveyed VIPP beam (support and mid-span)."""

import pytest
from shapely.geometry import LineString

from bridgebeams._geometry import section_properties
from bridgebeams.fr import AfgcVippBeamSection

from _aggregate import P, run_checks


def width_at(p, y):
    return p.intersection(LineString([(-3000, y), (3000, y)])).length


def _check_dimensions(size, web, bottom, top, yl, yr):
    sec = AfgcVippBeamSection(size)
    p = sec.polygon
    assert p.is_valid and p.exterior.is_ccw
    assert width_at(p, 1) == pytest.approx(bottom)
    assert width_at(p, 800) == pytest.approx(web)
    assert p.bounds[2] - p.bounds[0] == pytest.approx(top)
    xs = [c for c in p.exterior.coords]
    assert max(y for x, y in xs if x < 0) == pytest.approx(yl)
    assert max(y for x, y in xs if x > 0) == pytest.approx(yr)
    assert sec.provenance == "transcribed"
    assert sec.geometry is not None


def test_printed_total_conflicts_pinned():
    # part chains vs printed totals differ by 10 mm (survey rounding)
    sup = AfgcVippBeamSection("support").published
    assert sum(sup["bottom_parts_m"]) == pytest.approx(0.92) and sup["bottom_total_m"] == 0.91
    mid = AfgcVippBeamSection("mid-span").published
    assert sum(mid["top_parts_m"]) == pytest.approx(1.28) and mid["top_total_m"] == 1.29


def _check_support_heavier_than_midspan():
    a = [section_properties(AfgcVippBeamSection(s).polygon)["area"] for s in AfgcVippBeamSection.SIZES]
    assert a[0] > a[1]


def _check_invalid():
    with pytest.raises(ValueError):
        AfgcVippBeamSection("end-block")


def test_fr_afgc_vipp_catalogue_checks():
    run_checks(
        (_check_dimensions, P("size,web,bottom,top,yl,yr", [
    ("support", 420, 920, 1310, 1390, 1470), ("mid-span", 220, 910, 1280, 1440, 1400)])),
        _check_support_heavier_than_midspan,
        _check_invalid,
    )
