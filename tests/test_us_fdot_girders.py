"""FDOT FY 2026-27 Florida-I, Florida-U and Florida slab beams.

FDOT's SPI tables print area to 0.01 in2 (FIB/FSB), perimeter, Ixx, Iyy
and yt/yb to 0.01 in; FIB-84/96 Ixx and FUB-54+ Iyy only to 4 significant
figures. FIB and FSB reproduce the tables essentially exactly; FUB within
0.14 %. The single FSB outlier (18 in x 5'-0" Iyy) is pinned.
"""

import pytest

from bridgebeams.us.fdot_girders import (
    FdotFloridaIBeamSection, FdotFloridaSlabBeamSection, FdotFloridaUBeamSection,
)
from bridgebeams.us.pci_common import INCH_MM, gross_properties_in

from _aggregate import P, run_checks

CLASSES = [FdotFloridaIBeamSection, FdotFloridaUBeamSection, FdotFloridaSlabBeamSection]
TOL = {
    FdotFloridaIBeamSection: {"area": 0.01, "perimeter": 0.001, "ixx": 0.006, "iyy": 0.005, "yt": 0.03, "yb": 0.02},
    FdotFloridaUBeamSection: {"area": 0.08, "ixx": 0.06, "iyy": 0.14, "yt": 0.08, "yb": 0.11},
    FdotFloridaSlabBeamSection: {"area": 0.002, "perimeter": 0.005, "ixx": 0.01,  # Ixx to 1 in4 of ~5800
                                 "iyy": 0.001, "yt": 0.1, "yb": 0.1},
}
PINNED = {("FSB18-60", "iyy"): 0.511}
CASES = [(c, s) for c in CLASSES for s in c.SIZES]


def _check_published_properties(cls, size):
    beam = cls(size)
    g = gross_properties_in(beam.polygon)
    calc = {"area": g["area"], "yb": g["cy"], "yt": beam.dimensions.depth - g["cy"], "ixx": g["ixx"],
            "iyy": g["iyy"], "perimeter": g["perimeter"]}
    for prop, value in beam.published.items():
        res = 100 * (calc[prop] - value) / value
        if (size, prop) in PINNED:
            assert res == pytest.approx(PINNED[(size, prop)], abs=0.01)
        else:
            assert abs(res) <= TOL[cls][prop], (size, prop, res)


def _check_valid_symmetric_polygon(cls, size):
    beam = cls(size)
    poly = beam.polygon
    assert poly.is_valid and poly.exterior.is_ccw and not poly.interiors
    minx, miny, maxx, maxy = poly.bounds
    assert miny == pytest.approx(0, abs=1e-9)
    assert minx == pytest.approx(-maxx, abs=1e-6)
    assert maxy == pytest.approx(beam.dimensions.depth * INCH_MM)
    assert beam.provenance == "transcribed-with-convention"
    assert "2026-27" in beam.source_status
    assert beam.geometry is not None


def _check_overall_widths():
    assert FdotFloridaIBeamSection("FIB-96").polygon.bounds[2] * 2 == pytest.approx(48 * INCH_MM)
    # Sheet top widths: 7'-10", 8'-1", 8'-10"
    for size, width in (("FUB-48", 94), ("FUB-54", 97), ("FUB-72", 106)):
        assert FdotFloridaUBeamSection(size).polygon.bounds[2] * 2 == pytest.approx(width * INCH_MM)
    # W is at the soffit working point; the 3/4 in chamfer and 1/2 in draft keep the
    # concrete just inside it.
    fsb = FdotFloridaSlabBeamSection("FSB15-53")
    assert 53 * INCH_MM - 0.2 * INCH_MM < fsb.polygon.bounds[2] * 2 < 53 * INCH_MM
    assert fsb.dimensions.width == 53


def _check_fib_web_height_is_depth_minus_23():
    # 1'-1" (FIB-36) and 6'-1" (FIB-96) straight-web labels
    for size, web in (("FIB-36", 13), ("FIB-96", 73)):
        d = FdotFloridaIBeamSection(size).dimensions
        top_web = d.depth - d.top_edge - d.top_taper_drop - d.top_chamfer
        assert top_web - (d.bottom_edge + d.bottom_taper_rise) == pytest.approx(web)


def _check_unknown_size_rejected(cls):
    with pytest.raises(ValueError):
        cls("FIB-102")


def test_us_fdot_girders_catalogue_checks():
    run_checks(
        (_check_published_properties, P("cls,size", CASES, ids=[f"{c.__name__}-{s}" for c, s in CASES])),
        (_check_valid_symmetric_polygon, P("cls,size", CASES, ids=[f"{c.__name__}-{s}" for c, s in CASES])),
        _check_overall_widths,
        _check_fib_web_height_is_depth_minus_23,
        (_check_unknown_size_rejected, P("cls", CLASSES)),
    )


def test_fdot_fsb18_60_iyy_outlier_pinned():
    run_checks((_check_published_properties, P("cls,size", [(FdotFloridaSlabBeamSection, "FSB18-60")])))
