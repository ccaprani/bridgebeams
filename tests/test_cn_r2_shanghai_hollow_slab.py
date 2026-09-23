"""Shanghai DBJT08-101 draft hollow slabs (rigid and hinged families)."""

import math

import numpy as np
import pytest

from bridgebeams.cn.r2_shanghai_hollow_slab import (
    ShanghaiHingedHollowSlabSection,
    ShanghaiRigidHollowSlabSection,
)


def _ring(coords):
    xs = np.array([c[0] for c in coords[:-1]])
    ys = np.array([c[1] for c in coords[:-1]])
    x2, y2 = np.roll(xs, -1), np.roll(ys, -1)
    cr = xs * y2 - x2 * ys
    return cr.sum() / 2, ((ys + y2) * cr).sum() / 6, ((ys * ys + ys * y2 + y2 * y2) * cr).sum() / 12


def _props(poly):
    """Area, centroid height and centroidal Ixx including holes."""
    a, s, i = _ring(list(poly.exterior.coords))
    for hole in poly.interiors:
        ha, hs, hi = _ring(list(hole.coords))
        a, s, i = a + ha, s + hs, i + hi  # holes are clockwise: negative terms
    cy = s / a
    return a, cy, i - a * cy * cy


ALL = [(cls, s) for cls in (ShanghaiRigidHollowSlabSection, ShanghaiHingedHollowSlabSection)
       for s in cls.SIZES]


@pytest.mark.parametrize("cls,size", ALL)
def test_valid_ccw_two_voids(cls, size):
    sec = cls(size)
    p = sec.polygon
    assert p.is_valid
    assert p.exterior.is_ccw
    assert len(p.interiors) == 2
    assert all(not h.is_ccw for h in p.interiors)
    minx, miny, maxx, maxy = p.bounds
    assert miny == pytest.approx(0.0)
    assert sec.provenance in ("transcribed", "transcribed-with-convention")
    assert "draft" in sec.source_status
    assert sec.geometry is not None


@pytest.mark.parametrize("size", ShanghaiRigidHollowSlabSection.SIZES)
def test_rigid_printed_heights(size):
    sec = ShanghaiRigidHollowSlabSection(size)
    d = sec.dimensions
    yl, yr = d.ledge_heights
    # Printed ledge heights 357/383, 457/483, 657/683, 757/783.
    assert (yl, yr) == pytest.approx((d.depth - 193, d.depth - 167))
    minx, _, maxx, maxy = sec.polygon.bounds
    assert maxx == pytest.approx(650.0)
    if d.unit == "middle":
        assert minx == pytest.approx(-650.0)
    else:
        assert minx == pytest.approx(-850.0)  # 300 + 1150 + 50 = 1500 overall
        # printed root height 283/383/583/683 and tip 50 + 200 above it
        pts = sec.polygon.exterior.coords
        assert any(abs(x + 550) < 1e-6 and abs(y - (d.depth - 267)) < 1e-6 for x, y in pts)
    assert maxy == pytest.approx(d.top_y(600.0))  # right top corner, 2% crossfall


@pytest.mark.parametrize("size", ShanghaiRigidHollowSlabSection.SIZES)
def test_rigid_analytic_area(size):
    """Independent hand area (no published table for volume 1).

    Core 1100 x D (the 2 % top line averages to D about x = 0), plus the
    overhang band(s), the cantilever trapezoid (edge), R30 fillets
    (r^2 - pi r^2 / 4 each) and minus the voids.
    """
    sec = ShanghaiRigidHollowSlabSection(size, arc_points=2000)
    d = sec.dimensions
    D = d.depth
    yl, yr = d.ledge_heights
    fillet = 30 * 30 - math.pi * 30 * 30 / 4
    if d.void_height == d.void_width:
        voids = 2 * math.pi * 180 ** 2
    else:
        voids = 2 * (math.pi * 180 ** 2 + 360 * (d.void_height - 360))
    band_r = 50 * ((d.top_y(550) + d.top_y(600)) / 2 - yr) + 0.5 * 50 * (d.top_y(600) - yr)
    if d.unit == "middle":
        band_l = 50 * ((d.top_y(-550) + d.top_y(-600)) / 2 - yl) + 0.5 * 50 * (d.top_y(-600) - yl)
        expected = 1100 * D + band_r + band_l + 2 * fillet - voids
    else:
        # cantilever: thickness 200 at the tip, 256 at the web (printed 283/50/200)
        cant = 300 * (200 + 256) / 2
        expected = 1100 * D + band_r + cant + fillet - voids
    a, _, _ = _props(sec.polygon)
    assert a == pytest.approx(expected, rel=2e-5)


@pytest.mark.parametrize("size", ShanghaiHingedHollowSlabSection.SIZES)
def test_hinged_matches_published(size):
    """Table 1 (PDF p130) gives A/Yx/I to 5 decimals in m units.

    Tolerances: area and centroid 0.05 % (5-figure rounding plus 64-point
    arc discretisation, <0.01 %); inertia 0.1 % because 10 m values are
    printed to only 3 significant figures (0.00956 m^4 -> +/-0.05 %).
    """
    sec = ShanghaiHingedHollowSlabSection(size)
    pub = sec.published
    a, cy, i = _props(sec.polygon)
    assert a == pytest.approx(pub["A"] * 1e6, rel=5e-4)
    assert cy == pytest.approx(pub["Yx"] * 1e3, rel=5e-4)
    assert sec.dimensions.depth - cy == pytest.approx(pub["Ys"] * 1e3, rel=5e-4)
    assert i == pytest.approx(pub["I"] * 1e12, rel=1e-3)
    assert sec.dimensions.depth == pytest.approx(pub["h"] * 1e3)


@pytest.mark.parametrize("size", ShanghaiHingedHollowSlabSection.SIZES)
def test_hinged_chains_close(size):
    d = ShanghaiHingedHollowSlabSection(size).dimensions
    assert d.void_bottom + d.void_height + d.void_top == pytest.approx(d.depth)
    assert 2 * d.void_side_cover + 2 * d.void_width + d.void_gap == pytest.approx(d.width)
    _, _, maxx, _ = ShanghaiHingedHollowSlabSection(size).polygon.bounds
    assert maxx == pytest.approx(495.0 if d.unit == "middle" else 497.5 + 400)


def test_for_span():
    assert ShanghaiRigidHollowSlabSection.for_span(18).size == "16-18m-middle"
    assert ShanghaiHingedHollowSlabSection.for_span(22, "edge").size == "20-22m-edge"
    with pytest.raises(ValueError):
        ShanghaiRigidHollowSlabSection.for_span(25)


@pytest.mark.parametrize("cls", [ShanghaiRigidHollowSlabSection, ShanghaiHingedHollowSlabSection])
def test_invalid_size(cls):
    with pytest.raises(ValueError):
        cls("25m-middle")
    with pytest.raises(ValueError):
        cls("10m-middle", arc_points=4)
