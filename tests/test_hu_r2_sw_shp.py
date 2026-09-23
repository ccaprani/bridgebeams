"""SW Umwelttechnik SHP-22/32/40 (solid; mass-per-metre check)."""

import pytest
from shapely.geometry import LineString

from bridgebeams.hu.r2_sw_shp import SwShpSection


def width_at(poly, y):
    return poly.intersection(LineString([(-5000, y), (5000, y)])).length


@pytest.mark.parametrize("size,h,soffit", [("SHP-22", 220, 520), ("SHP-32", 320, 480), ("SHP-40", 400, 440)])
def test_printed(size, h, soffit):
    sec = SwShpSection(size)
    p = sec.polygon
    assert p.is_valid and p.exterior.is_ccw and len(p.interiors) == 0
    assert p.bounds[1] == pytest.approx(0, abs=1e-9) and p.bounds[3] == pytest.approx(h)
    assert width_at(p, h - 0.01) == pytest.approx(510 + 2 * 5 * 0.01 / 20, abs=0.01)
    # theoretical corners: 600 at the ledge level, printed soffit at y = 0
    assert width_at(p, h / 2) == pytest.approx(soffit + (600 - soffit) * (h / 2) / (h - 20), abs=0.01)
    assert width_at(p, 0.0001) == pytest.approx(soffit - 30, abs=0.1)
    assert sec.provenance == "transcribed-with-convention"
    assert sec.geometry is not None


@pytest.mark.parametrize("size,tol", [("SHP-22", 0.012), ("SHP-32", 0.005), ("SHP-40", 0.005)])
def test_mass_per_metre_at_2p5(size, tol):
    # table slope (t per m of length) vs A x 2.5 t/m3; SHP-22 +1.0 % (table masses to 0.01 t)
    sec = SwShpSection(size)
    assert sec.polygon.area / 1e6 * 2.5 == pytest.approx(sec.mass_per_metre_t, rel=tol)


def test_invalid():
    with pytest.raises(ValueError):
        SwShpSection("SHP-50")
