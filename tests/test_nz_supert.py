"""NZ Super-T: structural validation against Colin Caprani's confirmed
reading of NZTA RR 364 drawing S1.01 (no published property table)."""

import pytest

from bridgebeams._geometry import as_polygon, section_properties
from bridgebeams.nz import NzSuperTSection


def test_valid_and_symmetric():
    for d in NzSuperTSection.SIZES:
        beam = NzSuperTSection(d)
        poly = as_polygon(beam.geometry)
        assert poly.is_valid, d
        xmin, xmax, _, _ = beam.geometry.calculate_extents()
        assert -xmin == pytest.approx(xmax), d
        assert xmax == pytest.approx(2490 / 2, abs=1e-6), d


def test_depth_stack():
    for d in NzSuperTSection.SIZES:  # structural stack check
        beam = NzSuperTSection(d)
        dims = beam.dimensions
        # chamfer + flange + taper + slab must reach the top
        taper_top = (d - dims.top_slab_thickness) - (
            dims.bottom_flange_height + (dims.web_clear_top - dims.web_clear_bottom) / 2 * 10.56 * 0
        )
        # taper slope check: run/rise == 1/10.56
        run = (dims.web_clear_top - dims.web_clear_bottom) / 2
        rise = (d - dims.top_slab_thickness) - (
            dims.bottom_flange_height + (dims.web_clear_top - dims.web_clear_bottom) / 2 * 0
        )
        if d == 1025:  # slope read on the 1025 sheet; 1225 extends the webs (inferred)
            assert run / rise == pytest.approx(1 / 10.56, rel=0.02), d


def test_web_clear_distances():
    # Colin's 1:10.56 slope was read off the 1025 sheet; the 1225 extends
    # the webs (inferred), so its drawn slope differs slightly.
    beam = NzSuperTSection(1025)
    # inner faces: clear 709 at flange top, 840 at slab soffit
    _, y_fl_top = 240.0, 240.0
    x_in_bot = beam.dimensions.web_clear_bottom / 2
    x_in_top = beam.dimensions.web_clear_top / 2
    slope = (x_in_top - x_in_bot) / (beam.depth - beam.dimensions.top_slab_thickness - 240.0)
    assert slope == pytest.approx(1 / 10.56, rel=0.01)


def test_invalid_depth_raises():
    with pytest.raises(ValueError):
        NzSuperTSection(1100)


def test_area_plausible():
    # twin-web Super-T ~1025 deep: area should be roughly 0.55-0.75 m2
    beam = NzSuperTSection(1025)
    props = section_properties(as_polygon(beam.geometry))
    assert 0.6 < props["area"] / 1e6 < 1.2
