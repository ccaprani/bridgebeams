"""PCI regional products: NEXT D/F, NEBT, NEDBT, Zone 6 spliced U-girders.

NEXT tables give area/I to 1 unit and yb to 0.01 in; the undimensioned edge
key (D) and edge rounding (F) were scaled from the drawings, not fitted, so
0.1-0.15 % is allowed. NEBT/NEDBT are metric-origin sections printed with
2-decimal or 1/16 in callouts. Zone 6 areas are implied by the tabulated
weights at the stated 150 pcf.
"""

import pytest

from bridgebeams.us.pci_common import INCH_MM, gross_properties_in
from bridgebeams.us.pci_regional_products import (
    PciNeBulbTeeSection, PciNeDeckBulbTeeSection, PciNextBeamSection, PciZone6UGirderSection,
)

CLASSES = [PciNextBeamSection, PciNeBulbTeeSection, PciNeDeckBulbTeeSection, PciZone6UGirderSection]
TOL = {
    PciNextBeamSection: {"area": 0.11, "ixx": 0.10, "yb": 0.15},
    PciNeBulbTeeSection: {"area": 0.08, "yb": 0.07, "ixx": 0.18},
    PciNeDeckBulbTeeSection: {"area": 0.13, "ixx": 0.05, "yb": 0.02},
    PciZone6UGirderSection: {"area": 0.16},
}
CASES = [(c, s) for c in CLASSES for s in c.SIZES]


@pytest.mark.parametrize("cls,size", CASES, ids=[f"{c.__name__}-{s}" for c, s in CASES])
def test_published_properties(cls, size):
    beam = cls(size)
    g = gross_properties_in(beam.polygon)
    calc = {"area": g["area"], "yb": g["cy"], "ixx": g["ixx"]}
    for prop, value in beam.published.items():
        res = 100 * (calc[prop] - value) / value
        assert abs(res) <= TOL[cls][prop], (size, prop, res)


@pytest.mark.parametrize("cls,size", CASES, ids=[f"{c.__name__}-{s}" for c, s in CASES])
def test_valid_symmetric_polygon(cls, size):
    beam = cls(size)
    poly = beam.polygon
    assert poly.is_valid and poly.exterior.is_ccw and not poly.interiors
    minx, miny, maxx, maxy = poly.bounds
    assert miny == pytest.approx(0, abs=1e-9)
    assert minx == pytest.approx(-maxx, abs=1e-6)
    assert maxy == pytest.approx(beam.dimensions.depth * INCH_MM)
    assert beam.provenance in {"transcribed", "transcribed-with-convention", "fitted-reconstruction", "estimate"}
    assert beam.source_status
    assert beam.geometry is not None


def test_key_widths():
    assert PciNextBeamSection("NEXT36D-120").polygon.bounds[2] * 2 == pytest.approx(120 * INCH_MM)
    assert PciNextBeamSection("NEXT24F-95.5").polygon.bounds[2] * 2 == pytest.approx(95.5 * INCH_MM)
    assert PciNeBulbTeeSection("NEBT87").polygon.bounds[2] * 2 == pytest.approx(47.24 * INCH_MM)
    assert PciNeDeckBulbTeeSection("NEDBT80").polygon.bounds[2] * 2 == pytest.approx(60 * INCH_MM)
    for size in PciZone6UGirderSection.SIZES:
        u = PciZone6UGirderSection(size)
        assert u.polygon.bounds[2] * 2 == pytest.approx(u.row["W"] * INCH_MM)
        # W = T + 2 tf in the source table
        assert u.row["W"] == u.row["T"] + 2 * u.row["tf"]


def test_next_stem_batter_closes():
    # 15 in stem top minus 0.375/12 batter per face over the stem height = base width C
    for size in PciNextBeamSection.SIZES:
        d = PciNextBeamSection(size).dimensions
        assert d.stem_top - 2 * 0.375 / 12 * (d.depth - d.flange) == pytest.approx(d.stem_base)


def test_zone6_is_open_top_u():
    u = PciZone6UGirderSection("U84-4").polygon
    # centre of the girder at mid-depth is void
    from shapely.geometry import Point
    assert not u.contains(Point(0, 42 * INCH_MM))
    assert u.contains(Point(0, 4 * INCH_MM))


@pytest.mark.parametrize("cls", CLASSES)
def test_unknown_size_rejected(cls):
    with pytest.raises(ValueError):
        cls("NEXT 40")
