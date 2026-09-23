"""ODOT BR400 slabs/boxes vs printed sheet properties; BR300 I-girders analytic."""

import math

import pytest
from shapely.affinity import scale

from bridgebeams.us.state_common import gross_properties
from bridgebeams.us.state_or_girders import OrBoxSection, OrIGirderSection, OrSlabSection

IN = 25.4
ALL = (OrSlabSection, OrBoxSection, OrIGirderSection)
# size: (Area in2, c.g. in, I in4) as printed on each BR sheet
SLAB_PUB = {"12": (568, 5.97, 6851), "15": (562, 7.45, 12769), "18": (621, 8.94, 21626),
            "21": (696, 10.43, 34152), "26": (851, 12.92, 63596), "30": (938, 14.91, 97278)}
BOX_PUB = {"33": (753, 16.33, 110540), "39": (813, 19.29, 168600),
           "42": (843, 20.78, 203050), "48": (903, 23.75, 283450)}


@pytest.mark.parametrize("cls", ALL)
def test_every_size_valid_symmetric(cls):
    for size in cls.SIZES:
        s = cls(size)
        p = s.polygon
        assert p.is_valid and p.exterior.is_ccw
        assert all(not r.is_ccw for r in p.interiors)
        assert p.bounds[1] == pytest.approx(0.0, abs=1e-9)
        assert p.symmetric_difference(scale(p, xfact=-1, origin=(0, 0))).area < 1e-2
        assert s.provenance in {"transcribed", "transcribed-with-convention"}
        assert s.source_status
        assert s.geometry is not None


@pytest.mark.parametrize("cls", ALL)
def test_invalid_size_raises(cls):
    with pytest.raises(ValueError):
        cls("VI0")


# Area printed to 1 in2 (a 96-gon void loses <0.1 in2), c.g. to 0.01 in,
# I to 4-5 significant figures; residuals are <=0.5 in2, 0.01 in, 0.06 %.
@pytest.mark.parametrize("size", OrSlabSection.SIZES)
def test_slab_published(size):
    s = OrSlabSection(size)
    g = gross_properties(s.polygon, IN)
    a, yb, ix = SLAB_PUB[size]
    assert g["area"] == pytest.approx(a, abs=0.5)
    assert g["yb"] == pytest.approx(yb, abs=0.01)
    assert g["ix"] == pytest.approx(ix, rel=0.0006)
    assert s.polygon.bounds[2] - s.polygon.bounds[0] == pytest.approx(48 * IN)


@pytest.mark.parametrize("size", OrBoxSection.SIZES)
def test_box_published(size):
    g = gross_properties(OrBoxSection(size).polygon, IN)
    a, yb, ix = BOX_PUB[size]
    assert g["area"] == pytest.approx(a, abs=0.5)
    assert g["yb"] == pytest.approx(yb, abs=0.015)
    assert g["ix"] == pytest.approx(ix, rel=0.0006)


@pytest.mark.parametrize("size,depth,top,bot,web,area", [
    ("II", 36, 12, 18, 6, 12 * 6 + 3 * 9 + 6 * 15 + 6 * 12 + 18 * 6 - 1),
    ("III", 45, 16, 22, 7, 16 * 7 + 4.5 * 11.5 + 7 * 19 + 7.5 * 14.5 + 22 * 7 - 1),
    ("IV", 54, 20, 26, 8, 20 * 8 + 6 * 14 + 8 * 23 + 9 * 17 + 26 * 8 - 1),
    ("V", 63, 20, 26, 8, 20 * 8 + 6 * 14 + 8 * 32 + 9 * 17 + 26 * 8 - 1),
])
def test_i_girder_analytic(size, depth, top, bot, web, area):
    """No ODOT printed properties: check dims and trapezoid-sum area (1 in chamfers)."""
    s = OrIGirderSection(size)
    x0, _, x1, y1 = s.polygon.bounds
    assert y1 == pytest.approx(depth * IN)
    assert x1 - x0 == pytest.approx(bot * IN)
    assert s.dimensions.top_width == pytest.approx(top * IN)
    assert s.dimensions.web_width == pytest.approx(web * IN)
    assert gross_properties(s.polygon, IN)["area"] == pytest.approx(area)
    assert not math.isnan(gross_properties(s.polygon, IN)["ix"])
