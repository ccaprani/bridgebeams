"""MoDOT EPG 751.21.1.3 box beams, voided slabs and solid slabs vs print.

Literal readings of the EPG figures (dated 2021). All dimensions printed;
tolerances are print precision (A 0.1 in2, yb 0.01 in, integer I) except
the circular voids, which are 128-gons: that under-states void area by
0.04% (<= 0.13 in2), so voided-slab areas use +-0.2 in2 and I 0.02%.
"""

import pytest
from shapely.affinity import scale

from bridgebeams.us.state_mo_slabs_boxes import (
    MoDotBoxBeamSection,
    MoDotSolidSlabSection,
    MoDotVoidedSlabSection,
)

from _aggregate import P, run_checks

IN = 25.4
CLASSES = (MoDotBoxBeamSection, MoDotVoidedSlabSection, MoDotSolidSlabSection)


def _ring(coords):
    pts = list(coords)[:-1]
    a = s = i = j = 0.0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
        c = x0 * y1 - x1 * y0
        a += c
        s += (y0 + y1) * c
        i += (y0 * y0 + y0 * y1 + y1 * y1) * c
        j += (x0 * x0 + x0 * x1 + x1 * x1) * c
    return a / 2, s / 6, i / 12, j / 12


def props_in(poly):
    a, s, i, j = _ring(poly.exterior.coords)
    for h in poly.interiors:  # clockwise: signed terms subtract
        da, ds, di, dj = _ring(h.coords)
        a, s, i, j = a + da, s + ds, i + di, j + dj
    cy = s / a
    return a / IN**2, cy / IN, (i - a * cy * cy) / IN**4, j / IN**4


BOX = {  # A, yb, Ixx, Iyy, void area
    "ADJ36-17": (464.4, 8.30, 13896, 54433, 124.0),
    "ADJ36-21": (510.4, 10.19, 25129, 63415, 212.0),
    "ADJ36-27": (547.4, 13.02, 49024, 72827, 376.0),
    "ADJ36-33": (604.4, 15.90, 82934, 84713, 520.0),
    "ADJ36-39": (661.4, 18.81, 127710, 96599, 664.0),
    "ADJ36-42": (689.9, 20.27, 154494, 102542, 736.0),
    "ADJ48-17": (608.4, 8.29, 18608, 129185, 184.0),
    "ADJ48-21": (662.4, 10.19, 33516, 149661, 312.0),
    "ADJ48-27": (679.4, 12.97, 64499, 162380, 568.0),
    "ADJ48-33": (736.4, 15.83, 108042, 186151, 784.0),
    "ADJ48-39": (793.4, 18.71, 164816, 209921, 1000.0),
    "ADJ48-42": (821.9, 20.16, 198487, 221806, 1108.0),
    "SPR48-17": (629.8, 8.38, 18922, 140928, 184.0),
    "SPR48-21": (693.8, 10.31, 34200, 166869, 312.0),
    "SPR48-27": (725.8, 13.15, 66264, 187786, 568.0),
    "SPR48-33": (797.8, 16.05, 111729, 219754, 784.0),
    "SPR48-39": (869.8, 18.97, 171541, 251722, 1000.0),
    "SPR48-42": (905.8, 20.44, 207233, 267706, 1108.0),
}
VOIDED = {
    "ADJ36-15": (407.9, 7.30, 9265, 44859, 113.5),
    "ADJ36-18": (414.2, 8.66, 15150, 47021, 207.7),
    "ADJ36-21": (477.0, 10.40, 24509, 53328, 245.4),
    "ADJ48-15": (531.2, 7.29, 12363, 104974, 170.2),
    "ADJ48-18": (526.3, 8.63, 20075, 108244, 311.6),
    "ADJ48-21": (642.4, 10.42, 33175, 123986, 332.0),
    "SPR48-15": (547.5, 7.37, 12569, 113984, 170.2),
    "SPR48-18": (550.1, 8.75, 20478, 121353, 311.6),
    "SPR48-21": (673.7, 10.53, 33824, 141194, 332.0),
}
SOLID = {"SOLID48": (513.2, 5.48, 5191, 93190), "SOLID52": (557.2, 5.48, 5635, 119252)}


def _check_every_size_valid(cls):
    for size in cls.SIZES:
        s = cls(size)
        p = s.polygon
        assert p.is_valid and p.exterior.is_ccw
        assert all(not r.is_ccw for r in p.interiors)
        assert p.bounds[1] == pytest.approx(0.0, abs=1e-9)
        assert p.symmetric_difference(scale(p, xfact=-1, origin=(0, 0))).area < 1e-3
        assert s.provenance == "transcribed"
        assert s.source_status
        assert s.geometry is not None


def _check_invalid_size(cls):
    with pytest.raises(ValueError):
        cls("ADJ48-99")


def _check_counts():
    assert len(MoDotBoxBeamSection.SIZES) == 18
    assert len(MoDotVoidedSlabSection.SIZES) == 9
    assert len(MoDotSolidSlabSection.SIZES) == 2


def _check_box_published(size, pub):
    s = MoDotBoxBeamSection(size)
    a, yb, ix, iy = props_in(s.polygon)
    void = s.polygon.interiors[0]
    assert abs(_ring(void.coords)[0]) / IN**2 == pytest.approx(pub[4], abs=1e-6)
    assert a == pytest.approx(pub[0], abs=0.06)
    assert yb == pytest.approx(pub[1], abs=0.006)
    assert ix == pytest.approx(pub[2], rel=1e-4)
    assert iy == pytest.approx(pub[3], rel=1e-4)


def _check_voided_published(size, pub):
    s = MoDotVoidedSlabSection(size)
    a, yb, ix, iy = props_in(s.polygon)
    voids = sum(abs(_ring(h.coords)[0]) for h in s.polygon.interiors) / IN**2
    assert voids == pytest.approx(pub[4], abs=0.2)
    assert a == pytest.approx(pub[0], abs=0.2)
    assert yb == pytest.approx(pub[1], abs=0.006)
    assert ix == pytest.approx(pub[2], rel=2e-4)
    assert iy == pytest.approx(pub[3], rel=2e-4)


def _check_solid_published(size, pub):
    a, yb, ix, iy = props_in(MoDotSolidSlabSection(size).polygon)
    assert a == pytest.approx(pub[0], abs=0.06)
    assert yb == pytest.approx(pub[1], abs=0.006)
    assert ix == pytest.approx(pub[2], rel=1e-4)
    assert iy == pytest.approx(pub[3], rel=1e-4)


def _check_adjacent_top_width_and_key():
    s = MoDotBoxBeamSection("ADJ48-27")
    top = [x for x, y in s.polygon.exterior.coords if abs(y - 27 * IN) < 1e-6]
    assert (max(top) - min(top)) / IN == pytest.approx(46.75)
    assert (s.polygon.bounds[2] - s.polygon.bounds[0]) / IN == pytest.approx(48)
    sp = MoDotBoxBeamSection("SPR48-27")
    top = [x for x, y in sp.polygon.exterior.coords if abs(y - 27 * IN) < 1e-6]
    assert (max(top) - min(top)) / IN == pytest.approx(48)


def test_us_state_mo_slabs_boxes_catalogue_checks():
    run_checks(
        (_check_every_size_valid, P("cls", CLASSES)),
        (_check_invalid_size, P("cls", CLASSES)),
        _check_counts,
        (_check_box_published, P("size,pub", BOX.items())),
        (_check_voided_published, P("size,pub", VOIDED.items())),
        (_check_solid_published, P("size,pub", SOLID.items())),
        _check_adjacent_top_width_and_key,
    )
