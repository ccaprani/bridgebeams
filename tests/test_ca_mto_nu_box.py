"""Ontario MTO NU girders (SS107-16..23) and box girders (SS107-13/14).

No published section-property tables exist in the held Ontario sources,
so checks are analytic: closed-form area (straight-line polygon plus
exact circular-fillet corrections), stored exact-arc references, widths
at dimensioned levels and void topology.
"""
import math

import pytest

from bridgebeams._geometry import section_properties
from bridgebeams.ca import CaMtoBoxGirderSection, CaMtoNuGirderSection
from bridgebeams.ca.mto_nu_girder import _load_data as nu_data

from _aggregate import P, run_checks


def _props_with_holes(poly):
    """Area, centroid y and Ixx including interiors."""
    outer = section_properties(type(poly)(poly.exterior.coords))
    a, sy, i0 = outer["area"], outer["area"] * outer["cy"], outer["ixx"] + outer["area"] * outer["cy"] ** 2
    for ring in poly.interiors:
        h = section_properties(type(poly)(ring.coords))
        a -= h["area"]
        sy -= h["area"] * h["cy"]
        i0 -= h["ixx"] + h["area"] * h["cy"] ** 2
    cy = sy / a
    return a, cy, i0 - a * cy * cy


def _width_at(poly, y):
    from shapely.geometry import LineString
    return poly.intersection(LineString([(-2000, y), (2000, y)])).length


def _fillet_correction(r, theta):
    return r * r * (1 / math.tan(theta / 2) - (math.pi - theta) / 2)


# ---------------------------------------------------------------- NU girders
def _check_nu_valid_and_bounds(size):
    s = CaMtoNuGirderSection(size)
    p = s.polygon
    assert p.is_valid and p.exterior.is_ccw and not p.interiors
    d = float(size[2:])
    minx, miny, maxx, maxy = p.bounds
    assert (miny, maxy) == pytest.approx((0, d))
    assert (minx, maxx) == pytest.approx((-617.5, 617.5))
    assert s.dimensions.web_height == d - 385
    assert _width_at(p, d - 1) == pytest.approx(1235)
    assert _width_at(p, 10) == pytest.approx(985 - 40 + 20, abs=1e-6)
    assert _width_at(p, 60) == pytest.approx(985)
    assert _width_at(p, d / 2) == pytest.approx(160)
    assert s.provenance == "transcribed-with-convention"
    assert s.source_status.startswith("current SS107-")


def _check_nu_area_closed_form(size):
    s = CaMtoNuGirderSection(size, arc_segments=2048)
    d = s.dimensions
    # straight-line polygon: bottom flange + two tapers + web + top flange
    D = d.depth
    sharp = (985 * 135 - 400                      # bottom block less chamfers
             + (985 + 160) / 2 * 140              # bottom taper trapezoid
             + 160 * (D - 385)                    # web
             + (160 + 1235) / 2 * 45              # top taper trapezoid
             + 1235 * 65)                         # top edge block
    tb = math.atan2(140, 412.5)                   # bottom taper angle
    tt = math.atan2(45, 537.5)                    # top taper angle
    corr = (-_fillet_correction(50, math.pi / 2 + tb)
            + _fillet_correction(200, math.pi / 2 + tb)
            + _fillet_correction(200, math.pi / 2 + tt)
            - _fillet_correction(50, math.pi / 2 + tt))
    exact = sharp + 2 * corr
    a, cy, ixx = _props_with_holes(s.polygon)
    assert a == pytest.approx(exact, rel=1e-5)
    ref = nu_data()["sizes"][size]["analytic_reference"]
    assert a == pytest.approx(ref["area_mm2"], rel=1e-5)
    assert cy == pytest.approx(ref["yb_mm"], rel=1e-5)
    assert ixx == pytest.approx(ref["ixx_mm4"], rel=1e-5)


def _check_nu_default_tessellation_close_to_exact_arcs():
    for size in CaMtoNuGirderSection.SIZES:
        a, _, ixx = _props_with_holes(CaMtoNuGirderSection(size).polygon)
        ref = nu_data()["sizes"][size]["analytic_reference"]
        assert a == pytest.approx(ref["area_mm2"], rel=1e-4)
        assert ixx == pytest.approx(ref["ixx_mm4"], rel=1e-4)


def _check_nu_2023_draft_and_2025_share_template():
    data = nu_data()
    assert [data["sizes"][s]["drawing"] for s in CaMtoNuGirderSection.SIZES] == [
        f"SS107-{n}" for n in range(16, 24)]
    assert [data["sizes"][s]["web_height_mm"] for s in CaMtoNuGirderSection.SIZES] == [
        515, 815, 1015, 1215, 1415, 1515, 1615, 2015]


def _check_nu_invalid():
    with pytest.raises(ValueError):
        CaMtoNuGirderSection("NU1000")
    with pytest.raises(ValueError):
        CaMtoNuGirderSection("NU900", arc_segments=2)
    CaMtoNuGirderSection("NU900").geometry


# --------------------------------------------------------------- box girders
def _check_box_valid_and_area(size):
    s = CaMtoBoxGirderSection(size)
    p = s.polygon
    assert p.is_valid and p.exterior.is_ccw
    assert len(p.interiors) == 1 and not p.interiors[0].is_ccw
    d, w = s.dimensions.depth, s.dimensions.width
    assert p.bounds == pytest.approx((-w / 2, 0, w / 2, d))
    exact = (w * d - 4 * 200) - ((w - 250) * (d - 280) - 4 * 0.5 * 75 * 75)
    a, cy, ixx = _props_with_holes(p)
    assert a == pytest.approx(exact)
    assert cy == pytest.approx(d / 2)
    # webs at mid-depth: two 125 mm walls
    assert _width_at(p, d / 2) == pytest.approx(250)
    # full slab at mid-slab height
    assert _width_at(p, 70) == pytest.approx(w)
    assert ixx > 0


def _check_box_provenance_split():
    for size in CaMtoBoxGirderSection.SIZES:
        s = CaMtoBoxGirderSection(size)
        if size.endswith("-1220"):
            assert s.provenance == "transcribed-with-convention"
            assert s.source_status.startswith("current SS107-1")
        else:
            assert s.provenance == "estimate"
            assert "DRAFT" in s.source_status


def _check_box_b1000_1220_values():
    a, _, _ = _props_with_holes(CaMtoBoxGirderSection("B1000-1220").polygon)
    assert a == pytest.approx(1220 * 1000 - 800 - (970 * 720 - 11250))


def _check_box_invalid():
    with pytest.raises(ValueError):
        CaMtoBoxGirderSection("B1100-1220")
    CaMtoBoxGirderSection().geometry


def test_ca_mto_nu_box_catalogue_checks():
    run_checks(
        (_check_nu_valid_and_bounds, P("size", CaMtoNuGirderSection.SIZES)),
        (_check_nu_area_closed_form, P("size", CaMtoNuGirderSection.SIZES)),
        _check_nu_default_tessellation_close_to_exact_arcs,
        _check_nu_2023_draft_and_2025_share_template,
        _check_nu_invalid,
        (_check_box_valid_and_area, P("size", CaMtoBoxGirderSection.SIZES)),
        _check_box_provenance_split,
        _check_box_b1000_1220_values,
        _check_box_invalid,
    )
