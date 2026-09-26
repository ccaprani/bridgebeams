"""IDOT PPC deck beams (cell library PD-*, 2025) vs Design Guide 3.5 example."""

import pytest
from shapely.affinity import scale

from bridgebeams.us.state_common import gross_properties
from bridgebeams.us.state_il_deck_beams import IlDeckBeamSection

from _aggregate import P, run_checks

IN = 25.4


def _check_every_size_valid_symmetric():
    for size in IlDeckBeamSection.SIZES:
        s = IlDeckBeamSection(size)
        p = s.polygon
        assert p.is_valid and p.exterior.is_ccw
        assert all(not r.is_ccw for r in p.interiors)
        assert p.bounds[1] == pytest.approx(0.0, abs=1e-9)
        assert p.symmetric_difference(scale(p, xfact=-1, origin=(0, 0))).area < 1e-3
        assert s.provenance == "transcribed"
        assert s.source_status
        assert s.geometry is not None


def _check_invalid_size_raises():
    with pytest.raises(ValueError):
        IlDeckBeamSection("27x40")


def _check_widths_depth_voids(size):
    s = IlDeckBeamSection(size)
    depth, width = (float(v) for v in size.split("x"))
    x0, _, x1, y1 = s.polygon.bounds
    assert x1 - x0 == pytest.approx(width * IN)
    assert y1 == pytest.approx(depth * IN)
    assert s.dimensions.top_width == pytest.approx((width - 1.25) * IN)
    assert len(s.polygon.interiors) == (0 if depth == 11 else 1)


def _check_11x48_solid_area_analytic():
    # 48x11 minus two 1.5 in chamfers and two keys (the key removes
    # 3*0.625 + 0.375*(0.625+1.25)/2 + (4-1.125)*1.25 + 0.75*1.25/2 per side).
    per_side = 3 * 0.625 + 0.375 * (0.625 + 1.25) / 2 + (4 - 1.125) * 1.25 + 0.75 * 1.25 / 2
    expected = 48 * 11 - 2 * 1.125 - 2 * per_side
    assert gross_properties(IlDeckBeamSection("11x48").polygon, IN)["area"] == pytest.approx(expected)


def _check_27x36_matches_design_guide_example():
    """DG 3.5: A = 569.9 in2, I = 49,697 in4, Cb = 13.30 in, Ct = 13.71 in.

    Cb + Ct = 27.01 in, so the printed centroid carries ~0.01 in rounding
    (Ct implies yb = 13.29); the model gives 13.295.
    """
    g = gross_properties(IlDeckBeamSection("27x36").polygon, IN)
    assert g["area"] == pytest.approx(569.9, abs=0.05)
    assert g["ix"] == pytest.approx(49697, abs=1.0)
    assert g["yb"] == pytest.approx(13.30, abs=0.01)
    assert 27 - g["yb"] == pytest.approx(13.71, abs=0.01)


def test_us_state_il_deck_beams_catalogue_checks():
    run_checks(
        _check_every_size_valid_symmetric,
        _check_invalid_size_raises,
        (_check_widths_depth_voids, P("size", IlDeckBeamSection.SIZES)),
        _check_11x48_solid_area_analytic,
        _check_27x36_matches_design_guide_example,
    )
