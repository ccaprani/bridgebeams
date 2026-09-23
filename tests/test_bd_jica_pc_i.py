"""Bangladesh JICA/RHD PC-I girders fitted to published section areas."""

import pytest

from bridgebeams._geometry import section_properties
from bridgebeams.bd.jica_pc_i import JicaPcIGirderSection

from _aggregate import P, run_checks

PUBLISHED_M2 = {"25m": 0.5290, "30m": 0.6723, "35m": 0.6960, "40m": 0.7523}


def _check_area_with_200_web(size):
    sec = JicaPcIGirderSection(size)
    assert sec.dimensions.web_width == 200
    area = section_properties(sec.polygon)["area"]
    # published to 4 decimal places of m2, i.e. +/-50 mm2 rounding
    assert area == pytest.approx(PUBLISHED_M2[size] * 1e6, abs=50.0)


def test_35m_rounding_boundary():
    """35 m with a 200 web gives 696,050 mm2, exactly on the 0.6960/0.6961 rounding boundary."""
    assert section_properties(JicaPcIGirderSection("35m").polygon)["area"] == pytest.approx(696_050.0)


def test_25m_pinned_residual():
    """25 m: exact fit is a 179.5 mm web; the adopted 180 gives +550 mm2 (+0.10%)."""
    sec = JicaPcIGirderSection("25m")
    area = section_properties(sec.polygon)["area"]
    assert area == pytest.approx(529_550.0)
    assert area - PUBLISHED_M2["25m"] * 1e6 == pytest.approx(550.0)


def _check_outline(size):
    sec = JicaPcIGirderSection(size)
    d = sec.dimensions
    poly = sec.polygon
    assert poly.is_valid and poly.exterior.is_ccw
    assert poly.bounds[1] == 0 and poly.bounds[3] == d.depth
    assert poly.bounds[2] - poly.bounds[0] == max(d.top_width, d.bottom_width)
    top = sorted(x for x, y in poly.exterior.coords if y == d.depth)
    assert top[-1] - top[0] == d.top_width - 160  # 80 mm edge rebate each side
    assert sec.provenance == "fitted-reconstruction"
    assert "JICA" in sec.source_status


def _check_invalid():
    with pytest.raises(ValueError):
        JicaPcIGirderSection("45m")


def test_bd_jica_pc_i_catalogue_checks():
    run_checks(
        (_check_area_with_200_web, P("size", ["30m", "35m", "40m"])),
        (_check_outline, P("size", JicaPcIGirderSection.SIZES)),
        _check_invalid,
    )
