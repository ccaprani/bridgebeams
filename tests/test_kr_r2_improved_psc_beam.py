"""Korean 개량형 PSC BEAM (2008, MLTM Daejeon) midspan sections."""

import math

import pytest

from bridgebeams._geometry import section_properties
from bridgebeams.kr.r2_improved_psc_beam import ImprovedPscBeamDimensions, ImprovedPscBeamSection

from _aggregate import P, run_checks

WEB = {"H1400": (1400, 865), "H1700": (1700, 1165), "H2000": (2000, 1465)}


def _sharp_area(h, hw):
    t, w, b = 1200, 200, 1000
    return t * 150 + (t + w) / 2 * 60 + w * hw + (b + w) / 2 * 150 + b * 175


def _fillet_delta(v_prev, v, v_next, r):
    """Area between the sharp corner and its tangent arc."""
    u = (v_prev[0] - v[0], v_prev[1] - v[1])
    q = (v_next[0] - v[0], v_next[1] - v[1])
    th = math.acos((u[0] * q[0] + u[1] * q[1]) / (math.hypot(*u) * math.hypot(*q)))
    return r * r * (1 / math.tan(th / 2) - (math.pi - th) / 2)


def _check_chain_and_area(size):
    h, hw = WEB[size]
    sec = ImprovedPscBeamSection(size)
    d = sec.dimensions
    assert d.top_edge + d.top_splay + d.web_height + d.bottom_splay + d.bottom_edge == h
    poly = sec.polygon
    assert poly.is_valid and poly.exterior.is_ccw
    minx, miny, maxx, maxy = poly.bounds
    assert (minx, maxx, miny, maxy) == (-600, 600, 0, h)
    # bottom flange width 1000 at the soffit
    bot = sorted(x for x, y in poly.exterior.coords if y == 0)
    assert bot[-1] - bot[0] == 1000
    # analytic fillet corrections: convex corners remove, re-entrant add
    pts = [(p[0], p[1]) for p in d.sharp_right_half]
    convex = _fillet_delta(pts[1], pts[2], pts[3], 100) + _fillet_delta(pts[4], pts[5], pts[6], 50)
    concave = _fillet_delta(pts[2], pts[3], pts[4], 150) + _fillet_delta(pts[3], pts[4], pts[5], 150)
    expected = _sharp_area(h, hw) + 2 * (concave - convex)
    # 16-chord tessellation under-represents each arc segment; tolerance 0.02%
    assert section_properties(poly)["area"] == pytest.approx(expected, rel=2e-4)


def _check_provenance_and_status():
    assert ImprovedPscBeamSection("H2000").provenance == "transcribed"
    assert ImprovedPscBeamSection("H1400").provenance == "transcribed-with-convention"
    assert "2008" in ImprovedPscBeamSection("H1700").source_status
    assert ImprovedPscBeamSection("H2000").span_m == (25, 30, 35)


def test_printed_75_does_not_close():
    """The printed '75' bottom side on the H=1.4/1.7 sheets leaves the chain 100 short."""
    with pytest.raises(ValueError):
        ImprovedPscBeamDimensions(depth=1400, web_height=865, bottom_edge=75)


def _check_geometry_and_invalid():
    assert ImprovedPscBeamSection("H1400").geometry is not None
    with pytest.raises(ValueError):
        ImprovedPscBeamSection("H1500")


def test_kr_r2_improved_psc_beam_catalogue_checks():
    run_checks(
        (_check_chain_and_area, P("size", ImprovedPscBeamSection.SIZES)),
        _check_provenance_and_status,
        _check_geometry_and_invalid,
    )
