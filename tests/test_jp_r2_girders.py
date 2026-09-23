"""Tests for round-2 Japanese sections: JIS A 5373 slab girders, Bi-pre girders."""

import numpy as np
import pytest

from bridgebeams.jp.r2_bipre_girders import BipreHollowGirderSection, BipreIGirderSection
from bridgebeams.jp.r2_jis_slab_girders import JisSlabGirderSection


def _props(poly):
    """Area, centroid height, centroidal Ixx including interior rings."""

    def ring(coords):
        c = np.asarray(coords)[:-1]
        x, y = c[:, 0], c[:, 1]
        x2, y2 = np.roll(x, -1), np.roll(y, -1)
        cr = x * y2 - x2 * y
        return cr.sum() / 2, ((y + y2) * cr).sum() / 6, ((y * y + y * y2 + y2 * y2) * cr).sum() / 12

    a, q, i = ring(poly.exterior.coords)
    for r in poly.interiors:
        a2, q2, i2 = ring(r.coords)
        a, q, i = a + a2, q + q2, i + i2
    cy = q / a
    return a, cy, i - a * cy * cy


@pytest.mark.parametrize("size", JisSlabGirderSection.SIZES)
def test_jis_slab_valid_and_bounds(size):
    s = JisSlabGirderSection(size)
    p = s.polygon
    assert p.is_valid and p.exterior.is_ccw
    assert all(not r.is_ccw for r in p.interiors)
    minx, miny, maxx, maxy = p.bounds
    assert (minx, maxx, miny) == (-350, 350, 0)
    assert maxy == s.dimensions.depth
    assert len(p.interiors) == (1 if s.dimensions.hollow else 0)
    assert s.provenance in ("transcribed", "transcribed-with-convention")
    s.geometry


@pytest.mark.parametrize("size", JisSlabGirderSection.SIZES)
def test_jis_slab_matches_published_gross_properties(size):
    # Nihon Koatsu 2024 table: A to 1 cm2, I to 4-5 sig figs, y to 0.1 cm. Exact
    # centroids often fall on x.x5 cm and the table rounds those ties either way
    # (AS13 yuc 25.3 vs identical BS12 25.4), hence 0.06 cm.
    s = JisSlabGirderSection(size)
    pub = s.published
    a, cy, ixx = _props(s.polygon)
    assert a / 100 == pytest.approx(pub["Ac_cm2"], abs=0.5)
    assert cy / 10 == pytest.approx(-pub["ylc_cm"], abs=0.06)
    assert (s.dimensions.depth - cy) / 10 == pytest.approx(pub["yuc_cm"], abs=0.06)
    assert ixx / 1e4 == pytest.approx(pub["Ic_cm4"], rel=1e-4)


def test_jis_slab_as19_misprint_resolved():
    s = JisSlabGirderSection("AS19")
    assert s.dimensions.h2 == 160.0  # Chubu 2014 prints 106
    assert s.provenance == "transcribed-with-convention"
    assert _props(s.polygon)[0] == pytest.approx(_props(JisSlabGirderSection("AS20").polygon)[0])


def test_jis_slab_invalid():
    with pytest.raises(ValueError):
        JisSlabGirderSection("AS25")


@pytest.mark.parametrize("size", BipreIGirderSection.SIZES)
def test_bipre_i(size):
    s = BipreIGirderSection(size)
    p = s.polygon
    d = s.dimensions
    assert p.is_valid and p.exterior.is_ccw
    assert p.bounds == (-d.top_width / 2, 0, d.top_width / 2, d.depth)
    assert d.clear_web > 0
    top = [x for x, y in p.exterior.coords if y == d.depth]
    assert max(top) - min(top) == pytest.approx(d.top_width - 60)
    a, cy, _ = _props(p)
    # symmetric apart from the 30 mm top set-back, which lowers the centroid slightly
    assert d.depth / 2 - 15 < cy < d.depth / 2
    s.geometry


def test_bipre_i_printed_chains():
    webs = {k: BipreIGirderSection(k).dimensions.clear_web for k in BipreIGirderSection.SIZES}
    assert webs == {"I25": 130, "I30": 190, "I35": 300, "I40": 330, "I45": 440, "I50": 590}
    assert BipreIGirderSection("I45").provenance == "estimate"


@pytest.mark.parametrize("size", BipreHollowGirderSection.SIZES)
def test_bipre_hollow(size):
    s = BipreHollowGirderSection(size)
    p = s.polygon
    d = s.dimensions
    assert p.is_valid and p.exterior.is_ccw and len(p.interiors) == 1
    assert p.bounds == (-425, 0, 425, d.depth)
    assert d.void_apex_height == 200
    a, _, _ = _props(p)
    solid = 850 * 100 + 0.5 * (850 + 750) * 50 + 750 * (d.depth - 150)
    void = 370 * d.void_side + 0.5 * 370 * 75
    assert a == pytest.approx(solid - void)


def test_bipre_invalid():
    with pytest.raises(ValueError):
        BipreIGirderSection("I55")
    with pytest.raises(ValueError):
        BipreHollowGirderSection("H40")
