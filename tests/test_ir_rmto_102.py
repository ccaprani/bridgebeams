"""RMTO nominal PSC sections: independent rectangle/triangle mechanics.

No published bare properties were identified. Expected A/cy/I use a full-height
200 mm stem, two 150x80 flange overhangs and two 150x150 right triangles.
These checks do not compute expectations from the implementation's outline.
"""

import pytest
from shapely.affinity import scale

from bridgebeams import Rmto102InvertedTSection as RootSection
from bridgebeams.ir import Rmto102InvertedTDimensions, Rmto102InvertedTSection
from bridgebeams._geometry import as_polygon, section_properties
from _aggregate import P, run_checks

# Drawing rows independently transcribed, including the non-monotonic PDF order.
ROWS = [
    ("RMTO102-8-4-h370", 370, 52, "8-4"),
    ("RMTO102-8-5-h470", 470, 51, "8-5"),
    ("RMTO102-8-7-h770", 770, 54, "8-7"),
    ("RMTO102-8-8A-h1000", 1000, 56, "8-8, part A"),
]


def _check_section(row):
    name, h, page, sheet = row
    beam = Rmto102InvertedTSection(name)
    assert RootSection is Rmto102InvertedTSection
    assert isinstance(beam.dimensions, Rmto102InvertedTDimensions)
    assert beam.row["pdf_page"] == page
    assert beam.row["printed_sheet"] == sheet
    assert beam.dimensions.depth == h
    assert beam.dimensions.web_height == h - 230
    assert beam.dimensions.outline == [(-250, 0), (250, 0), (250, 80),
        (100, 230), (100, h), (-100, h), (-100, 230), (-250, 80)]
    p = beam.polygon
    assert p.is_valid and p.exterior.is_ccw and not p.interiors
    assert len(p.exterior.coords) == 9
    assert p.bounds == (-250, 0, 250, h)
    assert p.equals(scale(p, xfact=-1, yfact=1, origin=(0, 0)))
    assert as_polygon(beam.geometry).equals(p)
    # Component (area, centroid height, own centroidal Ixx).
    pieces = [(200*h, h/2, 200*h**3/12),
              (2*150*80, 40, 2*150*80**3/12),
              (2*150*150/2, 80 + 150/3, 2*150*150**3/36)]
    area = sum(a for a, _, _ in pieces)
    cy = sum(a*y for a, y, _ in pieces)/area
    ixx = sum(i + a*(y-cy)**2 for a, y, i in pieces)
    got = section_properties(as_polygon(beam.geometry))
    assert got["area"] == pytest.approx(area, rel=1e-12)
    assert got["cy"] == pytest.approx(cy, rel=1e-12)
    assert got["ixx"] == pytest.approx(ixx, rel=1e-12)
    assert got["cx"] == pytest.approx(0, abs=1e-10)
    assert beam.published == {}
    assert "mirror" in beam.source_status and "unverified" in beam.source_status
    assert beam.source["sha256"] == "981cc9d2461c67af694bd05130dcf4b29e22b726f464c20087730302ac848919"


def _check_no_inferred_sizes():
    assert Rmto102InvertedTSection.SIZES == tuple(row[0] for row in ROWS)
    for invalid in ("RMTO102-8-6-h620", "h620", "RMTO102-8-4-h550", 370):
        with pytest.raises(ValueError):
            Rmto102InvertedTSection(invalid)


def test_ir_rmto_102_catalogue_checks():
    run_checks((_check_section, P("row", ROWS)), _check_no_inferred_sizes)
