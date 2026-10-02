"""SCIB PDF6 nominal outlines against independently read published properties."""

import pytest
from shapely.affinity import scale

import bridgebeams
import bridgebeams.my
from bridgebeams._geometry import section_properties
from bridgebeams.my.scib_i_beam import ScibIBeamSection

from _aggregate import P, run_checks

# Literal page6 table, independently read from all three printed groups.
# size: depth, area, Yb, Ixx (x10^9), Zt (x10^6), Zb (x10^6)
PRINTED = {
    "I5": (965, 272625, 427, 28.15, 52.32, 65.80),
    "I6": (1040, 283875, 461, 34.46, 59.56, 74.76),
    "I7": (1120, 295875, 497, 42.09, 67.67, 84.68),
    "I8": (1220, 369375, 492, 58.75, 80.74, 119.3),
    "I12": (1420, 423050, 668, 93.64, 124.36, 140.19),
    "I13": (1475, 445600, 707, 106.61, 138.81, 150.79),
    "I14": (1550, 460600, 744, 122.07, 151.34, 164.07),
    "I15": (1600, 508600, 725, 145.2, 166.0, 200.3),
    "I16": (1675, 523600, 760, 164.4, 179.8, 216.2),
    "I17": (1725, 554100, 767, 182.2, 190.2, 237.5),
    "I18": (1830, 598475, 793, 221.9, 214.0, 279.8),
}


def _check_profile(size):
    s = ScibIBeamSection(size)
    p = s.polygon
    depth, area, yb, ix, zt, zb = PRINTED[size]
    assert p.is_valid and not p.is_empty and p.exterior.is_ccw
    assert p.bounds[1] == 0 and p.bounds[3] == depth
    assert p.symmetric_difference(scale(p, xfact=-1, origin=(0, 0))).area < 1e-6
    g = section_properties(p)
    assert g["area"] == pytest.approx(area, abs=1e-6)
    assert g["cy"] == pytest.approx(yb, abs=0.5)  # source rounds to integer mm
    assert g["cx"] == pytest.approx(0, abs=1e-10)
    assert g["ixx"] == pytest.approx(ix * 1e9, rel=0.0009)
    assert g["ixx"] / (depth - g["cy"]) == pytest.approx(zt * 1e6, rel=0.0003)
    assert g["ixx"] / g["cy"] == pytest.approx(zb * 1e6, rel=0.0003)
    assert s.dimensions.top_edge > 0
    assert s.dimensions.top_width / 2 - s.dimensions.web_width / 2 == 105
    assert s.provenance == "transcribed-with-convention" and s.source_status
    assert s.geometry is not None


def test_scib_i_published_properties_and_geometry():
    run_checks((_check_profile, P("size", list(PRINTED))))


def test_scib_public_api_and_source_specific_width():
    assert bridgebeams.ScibIBeamSection is ScibIBeamSection
    assert bridgebeams.my.ScibIBeamSection is ScibIBeamSection
    assert ScibIBeamSection.SIZES == tuple(PRINTED)
    assert ScibIBeamSection("I18").dimensions.bottom_width == 660
    assert ScibIBeamSection("I5").dimensions.top_edge == 145
    assert ScibIBeamSection("I12").dimensions.top_edge == 200
    with pytest.raises(ValueError):
        ScibIBeamSection("I9")
