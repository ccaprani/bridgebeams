"""PCI Bridge Design Manual (Nov 2011) Appendix B standard products.

Published values are rounded table entries (area to 0.5-1 in2, yb to 0.01 in,
Ixx to 1 in4). Tolerances per family reflect that rounding plus the stated
conventions (polygonised voids, squared keyway steps, DBT 48 in taper end).
Individual source contradictions are pinned, not absorbed by tolerances.
"""

import pytest

from bridgebeams.us.pci_common import INCH_MM, gross_properties_in
from bridgebeams.us.pci_standard_products import (
    PciBoxBeamSection, PciBulbTeeSection, PciDeckBulbTeeSection, PciDoubleTeeSection,
    PciSlabBeamSection,
)

from _aggregate import P, run_checks

CLASSES = [PciSlabBeamSection, PciBoxBeamSection, PciBulbTeeSection, PciDeckBulbTeeSection, PciDoubleTeeSection]
# max |residual| in percent for unpinned sizes
TOL = {
    PciSlabBeamSection: {"area": 0.15, "yb": 0.01, "ixx": 0.03},   # 128-chord voids vs rounded areas
    PciBoxBeamSection: {"area": 0.01, "yb": 0.06, "ixx": 0.10},
    PciBulbTeeSection: {"area": 0.01, "yb": 0.02, "ixx": 0.035},
    PciDeckBulbTeeSection: {"area": 0.08, "yb": 0.03, "ixx": 0.005},
    PciDoubleTeeSection: {"area": 0.07, "yb": 0.04, "ixx": 0.04},
}
# Pinned source discrepancies: (class, size, property) -> residual %
PINNED = {
    ("PciDoubleTeeSection", "L5-27", "yb"): -0.352,
    ("PciDoubleTeeSection", "L6-27", "yb"): -0.271,
    ("PciDoubleTeeSection", "L6-27", "ixx"): 0.140,
    ("PciDoubleTeeSection", "H6-35", "area"): -0.893, ("PciDoubleTeeSection", "H6-35", "yb"): -0.244,
    ("PciDoubleTeeSection", "H6-35", "ixx"): -0.328,
    ("PciDoubleTeeSection", "H7-35", "area"): -0.833, ("PciDoubleTeeSection", "H7-35", "yb"): -0.186,
    ("PciDoubleTeeSection", "H7-35", "ixx"): -0.252,
    ("PciDoubleTeeSection", "H8-35", "area"): -0.781, ("PciDoubleTeeSection", "H8-35", "yb"): -0.166,
    ("PciDoubleTeeSection", "H8-35", "ixx"): -0.195,
    ("PciDoubleTeeSection", "H6-27", "area"): -0.342, ("PciDoubleTeeSection", "H6-27", "yb"): -0.632,
    ("PciDoubleTeeSection", "H6-27", "ixx"): 1.529,
    ("PciDoubleTeeSection", "H7-27", "area"): -0.316, ("PciDoubleTeeSection", "H7-27", "yb"): -0.580,
    ("PciDoubleTeeSection", "H7-27", "ixx"): 1.625,
    ("PciDoubleTeeSection", "H8-27", "area"): -0.294, ("PciDoubleTeeSection", "H8-27", "yb"): -0.534,
    ("PciDoubleTeeSection", "H8-27", "ixx"): 1.700,
    ("PciDoubleTeeSection", "H6-21", "area"): -0.621, ("PciDoubleTeeSection", "H6-21", "yb"): -0.499,
    ("PciDoubleTeeSection", "H6-21", "ixx"): 1.533,
    ("PciDoubleTeeSection", "H7-21", "area"): -0.568, ("PciDoubleTeeSection", "H7-21", "yb"): -0.401,
    ("PciDoubleTeeSection", "H7-21", "ixx"): 1.597,
    ("PciDoubleTeeSection", "H8-21", "area"): -0.524, ("PciDoubleTeeSection", "H8-21", "yb"): -0.379,
    ("PciDoubleTeeSection", "H8-21", "ixx"): 1.640,
}
CASES = [(c, s) for c in CLASSES for s in c.SIZES]


def _calc(beam):
    g = gross_properties_in(beam.polygon)
    return {"area": g["area"], "yb": g["cy"], "ixx": g["ixx"], "iyy": g["iyy"], "perimeter": g["perimeter"]}


def _check_published_properties(cls, size):
    beam = cls(size)
    calc = _calc(beam)
    for prop, value in beam.published.items():
        res = 100 * (calc[prop] - value) / value
        pin = PINNED.get((cls.__name__, size, prop))
        if pin is not None:
            assert res == pytest.approx(pin, abs=0.01), (size, prop, res)
        else:
            assert abs(res) <= TOL[cls][prop], (size, prop, res)


def _check_valid_symmetric_polygon(cls, size):
    beam = cls(size)
    poly = beam.polygon
    assert poly.is_valid and poly.exterior.is_ccw
    assert all(not ring.is_ccw for ring in poly.interiors)
    minx, miny, maxx, maxy = poly.bounds
    assert miny == pytest.approx(0, abs=1e-9)
    assert minx == pytest.approx(-maxx, abs=1e-6)
    assert maxy == pytest.approx(beam.dimensions.depth * INCH_MM)
    assert gross_properties_in(poly)["cx"] == pytest.approx(0, abs=1e-6)
    assert beam.provenance in {"transcribed", "transcribed-with-convention", "fitted-reconstruction", "estimate"}
    assert beam.source_status
    assert beam.geometry is not None


def _check_widths_and_voids():
    assert PciSlabBeamSection("SIV-48").polygon.bounds[2] * 2 == pytest.approx(48 * INCH_MM)
    assert len(PciSlabBeamSection("SIV-48").polygon.interiors) == 3
    assert len(PciSlabBeamSection("SIII-36").polygon.interiors) == 2
    assert len(PciSlabBeamSection("SI-36").polygon.interiors) == 0
    box = PciBoxBeamSection("BIV-36").polygon
    assert len(box.interiors) == 1
    assert box.bounds[2] * 2 == pytest.approx(36 * INCH_MM)
    # stepped keyway: 3/8 in inset over the top 6 in, 3/4 in over the next 6 in
    from shapely.geometry import LineString
    def half_width_at(y_in):
        cut = box.intersection(LineString([(-1e4, y_in * INCH_MM), (1e4, y_in * INCH_MM)]))
        return cut.bounds[2] / INCH_MM
    assert half_width_at(42 - 3) == pytest.approx(18 - 0.375)
    assert half_width_at(42 - 9) == pytest.approx(18 - 0.75)
    assert half_width_at(42 - 20) == pytest.approx(18)
    bt = PciBulbTeeSection("BT-72").polygon
    assert bt.bounds[2] * 2 == pytest.approx(42 * INCH_MM)
    assert PciDeckBulbTeeSection("DBT65-96").polygon.bounds[2] * 2 == pytest.approx(96 * INCH_MM)
    assert PciDoubleTeeSection("H8-35").polygon.bounds[2] * 2 == pytest.approx(96 * INCH_MM)


def test_deck_bulb_tee_48_convention():
    # 19.5 in taper run cannot fit a 24 in half width; taper ends at the edge.
    assert PciDeckBulbTeeSection("DBT35-48").provenance == "transcribed-with-convention"
    assert PciDeckBulbTeeSection("DBT35-72").provenance == "transcribed"


def _check_unknown_size_rejected(cls):
    with pytest.raises(ValueError):
        cls("Type IV")


def test_us_pci_standard_products_catalogue_checks():
    run_checks(
        (_check_published_properties, P("cls,size", CASES, ids=[f"{c.__name__}-{s}" for c, s in CASES])),
        (_check_valid_symmetric_polygon, P("cls,size", CASES, ids=[f"{c.__name__}-{s}" for c, s in CASES])),
        _check_widths_and_voids,
        (_check_unknown_size_rejected, P("cls", CLASSES)),
    )


def test_pci_double_tee_discrepancies_pinned():
    pinned = {(c, s) for c, s, _ in PINNED}
    run_checks((_check_published_properties, P("cls,size", [(c, s) for c, s in CASES
                                                             if (c.__name__, s) in pinned])))
