"""Tierra Armada brochure beams (estimates traced from sketches)."""

import pytest
from shapely.geometry import LineString

from bridgebeams._geometry import section_properties
from bridgebeams.es.r2_tierra import TierraBeamSection

from _aggregate import P, run_checks


def width_at(poly, y):
    return poly.intersection(LineString([(-5000, y), (5000, y)])).length


def _check_valid_and_printed_envelope(size):
    sec = TierraBeamSection(size)
    p = sec.polygon
    d = sec.dimensions
    assert p.is_valid and p.exterior.is_ccw
    assert p.bounds[1] == 0 and p.bounds[3] == pytest.approx(d.depth)
    # printed lower wing at the soffit (chamfers of 30-40 mm excluded)
    if d.bottom_width != 3200:
        assert width_at(p, 45) == pytest.approx(d.bottom_width, abs=1)
    if d.top_width is not None:
        assert width_at(p, d.depth - 1) == pytest.approx(d.top_width)
    assert sec.provenance == "estimate"
    assert sec.geometry is not None


def _check_wide_u_soffit_is_3_20(size):
    p = TierraBeamSection(size).polygon
    assert width_at(p, 0.5) == pytest.approx(3200, abs=5)
    # open-top trough: nothing on the centreline above the bottom slab
    assert width_at(p, p.bounds[3] - 1) < p.bounds[2] - p.bounds[0]


def _check_area_increases_with_depth_within_series():
    a = [section_properties(TierraBeamSection(s).polygon)["area"] for s in ("IP-120", "IP-160", "IP-190")]
    assert a[0] < a[1] < a[2]


def _check_invalid():
    with pytest.raises(ValueError):
        TierraBeamSection("TA90E")


def test_es_r2_tierra_catalogue_checks():
    run_checks(
        (_check_valid_and_printed_envelope, P("size", TierraBeamSection.SIZES)),
        (_check_wide_u_soffit_is_3_20, P("size", ["TA90A", "TA150A", "TA210A"])),
        _check_area_increases_with_depth_within_series,
        _check_invalid,
    )
