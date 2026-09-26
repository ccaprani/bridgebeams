"""Sri Lanka RDA T/B/505 PSC inverted-T beam."""

import pytest

from bridgebeams._geometry import section_properties
from bridgebeams.lk.rda_beams import RdaTB505BeamSection

from _aggregate import P, run_checks


def _check_outline():
    sec = RdaTB505BeamSection()
    poly = sec.polygon
    assert poly.is_valid and poly.exterior.is_ccw
    assert poly.bounds == (-250, 0, 250, 525)
    top = sorted(x for x, y in poly.exterior.coords if y == 525)
    bot = sorted(x for x, y in poly.exterior.coords if y == 0)
    assert top[-1] - top[0] == 200
    assert bot[-1] - bot[0] == 450  # 500 less two 25 mm chamfer legs
    # 45 degree top splay: 50 high from 100 web to 200 bulb
    assert (sec.dimensions.top_width - sec.dimensions.web_width) / 2 == sec.dimensions.top_splay


def _check_area_and_centroid():
    # parts from soffit: chamfered strip, rectangle, taper, web, splay, bulb
    parts = [
        (500 * 25 - 25 * 25, None),
        (500 * 75, 25 + 37.5),
        ((500 + 100) / 2 * 80, 100 + 80 * (500 + 200) / (3 * 600)),
        (100 * 100, 180 + 50),
        ((200 + 100) / 2 * 50, 280 + 50 * (100 + 400) / (3 * 300)),
        (200 * 195, 330 + 97.5),
    ]
    # chamfered strip centroid: rectangle 500x25 minus two 25x25/2 triangles at the bottom
    rect, tri = 500 * 25, 2 * 312.5
    parts[0] = (rect - tri, (rect * 12.5 - tri * 25 / 3) / (rect - tri))
    area = sum(a for a, _ in parts)
    yb = sum(a * y for a, y in parts) / area
    props = section_properties(RdaTB505BeamSection().polygon)
    assert props["area"] == pytest.approx(area, rel=1e-12)
    assert props["cy"] == pytest.approx(yb, rel=1e-12)


def _check_meta_and_invalid():
    sec = RdaTB505BeamSection("TB505")
    assert sec.provenance == "transcribed"
    assert "T/B/505" in sec.source_status
    assert sec.length_m == 13.5
    assert sec.geometry is not None
    with pytest.raises(ValueError):
        RdaTB505BeamSection("TB506")


def test_lk_rda_tb505_catalogue_checks():
    run_checks(
        _check_outline,
        _check_area_and_centroid,
        _check_meta_and_invalid,
    )
