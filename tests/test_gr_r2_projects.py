"""Greek project girders: Dervenakia G3 (2022 tender) and NTUA Strymonas study."""

import pytest
from shapely.geometry import LineString

from bridgebeams.gr.r2_projects import GrProjectGirderSection


def width_at(p, y):
    return p.intersection(LineString([(-3000, y), (3000, y)])).length


@pytest.mark.parametrize("size,depth,top,bottom,web", [
    ("Dervenakia-G3", 2400, 1400, 900, 300), ("Strymonas-study", 2050, 1250, 900, 250)])
def test_printed_dimensions(size, depth, top, bottom, web):
    sec = GrProjectGirderSection(size)
    p = sec.polygon
    assert p.is_valid and p.exterior.is_ccw
    assert p.bounds == pytest.approx((-top / 2, 0, top / 2, depth))
    assert width_at(p, 1) == pytest.approx(bottom)
    assert width_at(p, depth / 2) == pytest.approx(web)
    assert sec.geometry is not None


def test_chains_close():
    d = GrProjectGirderSection("Dervenakia-G3").published
    assert sum(d["vertical_chain_top_down"]) == pytest.approx(2.40)
    s = GrProjectGirderSection("Strymonas-study").published
    assert sum(s["vertical_chain_top_down"]) == pytest.approx(2.05)
    assert sum(s["top_chain"]) == pytest.approx(1.25)


def test_invalid():
    with pytest.raises(ValueError):
        GrProjectGirderSection("Egnatia")
