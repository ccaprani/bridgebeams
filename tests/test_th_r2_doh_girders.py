"""Thai DOH 2015 plank girders, box beams and I-girders (round 2)."""

import math

import pytest

from bridgebeams.th.r2_doh_girders import (
    ThDohBoxBeamSection,
    ThDohIGirderR2Section,
    ThDohPlankGirderSection,
)


def _ring_area(coords):
    pts = list(coords)[:-1]
    return 0.5 * sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]))


def _net_area(poly):
    return _ring_area(poly.exterior.coords) + sum(_ring_area(r.coords) for r in poly.interiors)


ALL = [(C, s) for C in (ThDohPlankGirderSection, ThDohBoxBeamSection, ThDohIGirderR2Section) for s in C.SIZES]


@pytest.mark.parametrize("cls,size", ALL)
def test_valid_ccw_and_labelled(cls, size):
    sec = cls(size)
    p = sec.polygon
    assert p.is_valid and p.exterior.is_ccw
    assert all(not r.is_ccw for r in p.interiors)
    assert sec.provenance in {"transcribed", "transcribed-with-convention", "fitted-reconstruction", "estimate"}
    assert "DOH" in sec.source_status
    assert sec.geometry is not None


def _side_cut(h, y_face, y_key, key=70.0, top=45.0):
    return key / 2 * (y_key - y_face) + (key + top) / 2 * (h - y_key)


@pytest.mark.parametrize("span,h,h1,h2", [(5, 180, 50, 90), (6, 210, 50, 90), (7, 240, 50, 90),
                                          (8, 280, 50, 100), (9, 310, 80, 140), (10, 350, 80, 140),
                                          (12, 450, 80, 140)])
def test_plank_table_and_area(span, h, h1, h2):
    for unit, sides in (("INT", 2), ("EXT", 1)):
        sec = ThDohPlankGirderSection(f"PG{span}-{unit}", circle_points=256)
        d = sec.dimensions
        assert (d.h, d.h1, d.h2) == (h, h1, h2)
        area = 990 * h - sides * _side_cut(h, h1, h2) - 2 * 200
        if span == 12:
            area -= 3 * math.pi * 75**2
            assert len(sec.polygon.interiors) == 3
        # 256-gon voids underestimate hole area by ~0.01 %
        assert _net_area(sec.polygon) == pytest.approx(area, rel=2e-4)
        minx, miny, maxx, maxy = sec.polygon.bounds
        assert (minx, miny, maxx, maxy) == (-495, 0, 495, h)


def test_plank_exterior_void_positions():
    p = ThDohPlankGirderSection("PG12-EXT").polygon
    xs = sorted(round(r.centroid.x) for r in p.interiors)
    assert xs == [-255, 45, 315]


@pytest.mark.parametrize("size,h,h1,h3,h4,h5,h7,b3", [
    ("BB15-INT", 600, 180, 140, 90, 100, 350, 290), ("BB15-EXT", 600, 180, 140, 90, 100, 350, 360),
    ("BB20-INT", 700, 180, 160, 80, 200, 400, 290), ("BB20-EXT", 700, 180, 160, 80, 200, 400, 360)])
def test_box_closure_and_area(size, h, h1, h3, h4, h5, h7, b3):
    sec = ThDohBoxBeamSection(size)
    assert h3 + 2 * h4 + h5 + h1 == h
    sides = 1 if size.endswith("EXT") else 2
    assert 70 * sides + 2 * 180 + 2 * 100 + b3 == 990
    void = (b3 + 200) * (2 * h4 + h5) - 4 * 0.5 * 100 * h4
    area = 990 * h - sides * _side_cut(h, h7, h7 + 70) - void
    assert _net_area(sec.polygon) == pytest.approx(area, abs=1e-6)
    assert sec.polygon.interiors[0].bounds[1] == h3
    assert sec.polygon.interiors[0].bounds[3] == h - h1


def test_box_void_wall_on_exposed_side():
    p = ThDohBoxBeamSection("BB15-EXT").polygon
    assert 495 - p.interiors[0].bounds[2] == pytest.approx(180)


def test_igirder_areas():
    ig15 = ThDohIGirderR2Section("IG15")
    a15 = 450 * 100 + (450 + 150) / 2 * 75 + 150 * 225 + (150 + 500) / 2 * 150 + 500 * 200 - 2 * 200
    assert ig15.polygon.area == pytest.approx(a15)
    assert ig15.dimensions.web == 150
    ig20 = ThDohIGirderR2Section("IG20")
    a20 = 450 * 100 + (450 + 175) / 2 * 75 + 175 * 625 + (175 + 500) / 2 * 200 + 500 * 200 - 2 * 200
    assert ig20.polygon.area == pytest.approx(a20)
    assert ig20.polygon.bounds == (-250, 0, 250, 1200)


@pytest.mark.parametrize("cls", [ThDohPlankGirderSection, ThDohBoxBeamSection, ThDohIGirderR2Section])
def test_invalid_size(cls):
    with pytest.raises(ValueError):
        cls("PG11-INT")
