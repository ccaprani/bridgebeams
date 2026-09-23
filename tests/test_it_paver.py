"""Paver bridge beams (estimates scaled from catalogue sketches)."""

import pytest
from shapely.geometry import LineString

from bridgebeams._geometry import section_properties
from bridgebeams.it import PaverBeamSection


def width_at(p, y):
    return p.intersection(LineString([(-5000, y), (5000, y)])).length


@pytest.mark.parametrize("size", PaverBeamSection.SIZES)
def test_valid_and_printed_envelope(size):
    sec = PaverBeamSection(size)
    p, d = sec.polygon, sec.dimensions
    assert p.is_valid and p.exterior.is_ccw
    assert p.bounds[1] == 0 and p.bounds[3] == pytest.approx(d.depth)
    assert int(size[-3:] if size[-3:].isdigit() else size[-2:]) * 10 == d.depth
    assert sec.provenance == "estimate"
    assert sec.geometry is not None


@pytest.mark.parametrize("size", [s for s in PaverBeamSection.SIZES if s[:3] in ("VHP", "UHP")])
def test_troughs(size):
    p = PaverBeamSection(size).polygon
    bottom = 974 if size.startswith("VHP") else 2500
    assert width_at(p, 1) == pytest.approx(bottom, abs=1)
    top_edge = p.intersection(LineString([(-5000, p.bounds[3]), (5000, p.bounds[3])]))
    top = 1144 if size == "UHP60" else 2500
    assert top_edge.bounds[2] - top_edge.bounds[0] == pytest.approx(top)
    # open top: centreline is void above the 214 mm bottom slab
    assert not p.contains(LineString([(0, 300), (0, 590)]).centroid)


@pytest.mark.parametrize("size,area", [("UHP170", 1.005e6), ("UHP80", 0.745e6), ("VHP80", 0.531e6),
                                       ("HP100", 0.480e6), ("IHP65", 0.236e6)])
def test_area_vs_traced_sketch(size, area):
    # parametric model vs the scaled raster trace of the drawn sketch
    assert section_properties(PaverBeamSection(size).polygon)["area"] == pytest.approx(area, rel=0.02)


def test_printed_widths_other_families():
    assert width_at(PaverBeamSection("HP100").polygon, 999) == pytest.approx(1250)
    assert width_at(PaverBeamSection("HTP50").polygon, 499) == pytest.approx(1500)
    assert width_at(PaverBeamSection("HTP50").polygon, 200) == pytest.approx(600)
    assert width_at(PaverBeamSection("THP45").polygon, 449) == pytest.approx(180)
    assert width_at(PaverBeamSection("IHP80").polygon, 1) == pytest.approx(600)


def test_invalid():
    with pytest.raises(ValueError):
        PaverBeamSection("IHP120")
