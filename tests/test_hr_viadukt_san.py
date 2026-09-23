"""Viadukt SAN voided slab girders (TVZ teaching-note reproduction)."""

import numpy as np
import pytest
from shapely.geometry import LineString

from bridgebeams.hr.viadukt_san import ViaduktSanSection


def props_with_holes(poly):
    def ring(coords):
        c = np.asarray(coords)[:-1]
        x, y = c[:, 0], c[:, 1]
        x2, y2 = np.roll(x, -1), np.roll(y, -1)
        cr = x * y2 - x2 * y
        return cr.sum() / 2, ((y + y2) * cr).sum() / 6
    a, s = ring(poly.exterior.coords)
    for r in poly.interiors:
        da, ds = ring(r.coords)
        a, s = a + da, s + ds
    return a, s / a


@pytest.mark.parametrize("size,h,nvoid", [("SAN 210/75", 750, 3), ("SAN 210/115", 1150, 1), ("SAN 210/135", 1350, 1)])
def test_outline(size, h, nvoid):
    sec = ViaduktSanSection(size)
    p = sec.polygon
    assert p.is_valid and p.exterior.is_ccw
    assert len(p.interiors) == nvoid and all(not r.is_ccw for r in p.interiors)
    assert p.bounds == pytest.approx((-1050, 0, 1050, h))
    a, cy = props_with_holes(p)
    assert a == pytest.approx(p.area)
    assert 0 < cy < h
    assert sec.geometry is not None
    assert "teaching notes" in sec.source_status and "Viadukt" in sec.source_status


@pytest.mark.parametrize("size,h", [("SAN 210/115", 1150), ("SAN 210/135", 1350)])
def test_printed_walls(size, h):
    p = ViaduktSanSection(size).polygon
    vert = p.intersection(LineString([(0, -1), (0, h + 1)]))
    assert vert.length == pytest.approx(250)  # 15 top + 10 bottom
    assert vert.geoms[0].length in (pytest.approx(100), pytest.approx(150))
    horiz = p.intersection(LineString([(-1100, h / 2 - 100), (1100, h / 2 - 100)]))
    assert horiz.length == pytest.approx(300)  # two 15 cm webs
    assert ViaduktSanSection(size).provenance == "transcribed-with-convention"


def test_san75_estimate():
    sec = ViaduktSanSection("SAN 210/75")
    assert sec.provenance == "estimate"
    p = sec.polygon
    # 10 cm webs between O50 voids at 60 cm centres, 15 top / 10 bottom cover
    assert p.intersection(LineString([(-1100, 350), (1100, 350)])).length == pytest.approx(2100 - 3 * 500, abs=1)
    assert p.intersection(LineString([(0, -1), (0, 751)])).length == pytest.approx(250, abs=0.5)


def test_invalid():
    with pytest.raises(ValueError):
        ViaduktSanSection("SAN 210/95")
