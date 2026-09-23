"""Indonesia round-2: WIKA voided slabs and Waskita PC-I / voided slabs."""

import numpy as np
import pytest

from bridgebeams.id.r2_waskita import WaskitaPcIGirderSection, WaskitaVoidedSlabSection
from bridgebeams.id.r2_wika_voided_slab import WikaVoidedSlabSection

PROVENANCE = {"transcribed", "transcribed-with-convention", "fitted-reconstruction", "estimate"}


def props(poly):
    """Area, centroid and Ixx including interiors (holes subtracted)."""
    A = S = I0 = 0.0
    for ring, sgn in [(poly.exterior, 1)] + [(r, -1) for r in poly.interiors]:
        pts = np.asarray(ring.coords)[:-1]
        x, y = pts[:, 0], pts[:, 1]
        x2, y2 = np.roll(x, -1), np.roll(y, -1)
        cr = x * y2 - x2 * y
        s = np.sign(cr.sum())
        A += sgn * s * cr.sum() / 2
        S += sgn * s * ((y + y2) * cr).sum() / 6
        I0 += sgn * s * ((y * y + y * y2 + y2 * y2) * cr).sum() / 12
    cy = S / A
    return A, cy, I0 - A * cy * cy


@pytest.mark.parametrize("cls", [WikaVoidedSlabSection, WaskitaPcIGirderSection, WaskitaVoidedSlabSection])
def test_valid_and_invalid(cls):
    for s in cls.SIZES:
        sec = cls(s)
        p = sec.polygon
        assert p.is_valid and p.exterior.is_ccw
        assert all(not r.is_ccw for r in p.interiors)
        assert p.bounds[1] == pytest.approx(0)
        assert p.bounds[0] == pytest.approx(-p.bounds[2])
        assert sec.provenance in PROVENANCE and sec.source_status
        assert sec.geometry is not None
    with pytest.raises(ValueError):
        cls("X1")


def test_wika_vs_published():
    # Circles/stadia approximated by 256 segments per semicircle.
    for s in WikaVoidedSlabSection.SIZES:
        sec = WikaVoidedSlabSection(s, segments=256)
        p = sec.published
        assert len(sec.polygon.interiors) == 2
        assert sec.polygon.bounds[3] == p["dimensions_mm"]["depth"]
        assert sec.polygon.bounds[2] == 485
        a, cy, i = props(sec.polygon)
        assert a == pytest.approx(p["area"], rel=5e-4)
        assert i == pytest.approx(p["ixx"], rel=1.5e-3)
    assert WikaVoidedSlabSection("VS74").provenance == "fitted-reconstruction"


def test_waskita_pci_chain():
    sec = WaskitaPcIGirderSection("H170")
    d = sec.dimensions
    assert d.web_height == 1700 - 70 - 130 - 120 - 250 - 250
    minx, miny, maxx, maxy = sec.polygon.bounds
    assert (maxx * 2, maxy) == (800, 1700)
    assert WaskitaPcIGirderSection("H90").polygon.bounds[2] == 325  # B = 650 wider than A = 550
    for s in WaskitaPcIGirderSection.SIZES:
        assert WaskitaPcIGirderSection(s).dimensions.web_height > 0


def test_waskita_vs():
    t1 = WaskitaVoidedSlabSection("H66")
    assert len(t1.polygon.interiors) == 2 and t1.polygon.bounds[2] == 485
    t2 = WaskitaVoidedSlabSection("H62.5")
    assert len(t2.polygon.interiors) == 3 and t2.polygon.bounds[2] == 600
    assert t2.provenance == "estimate"
    a, cy, _ = props(t2.polygon)
    assert cy == pytest.approx(312.5, abs=15)
