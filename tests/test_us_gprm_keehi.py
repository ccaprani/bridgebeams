"""Undated GPRM four-sheet source: five profiles vs published properties.

The source table largely excludes the drawn soffit bevels and lower-web
radii. The as-drawn area deficit is 0.288-0.589 in2, yb is 0.017-0.026 in
high, and Ixx is 0.11-0.14 percent low. Tolerances cover those documented
corner conventions and table rounding; dimensions are not fitted to them.
"""

import pytest
from shapely.affinity import scale

import bridgebeams
import bridgebeams.us
from bridgebeams.us.gprm_keehi_girders import GprmKeehiGirderSection
from bridgebeams.us.state_common import gross_properties

from _aggregate import P, run_checks

# Literal page 1-4 table readings, independently retained from the drawing.
# size: area in2, yb in, Ix in4, top modulus in3, bottom modulus in3, depth in
PRINTED = {
    "K-VI W": (1028.3, 38.10, 731754, 21589, 19204, 72),
    "K-VI": (944, 35.27, 638894, 17394, 18114, 72),
    "K-IV W": (873.5, 31.61, 409337, 15514, 12948, 58),
    "K-IV": (687.75, 25.38, 282484, 8660, 11130, 58),
    "K-IV MOD": (783.8, 29.62, 383594, 11846, 12951, 62),
}


def _check_profile(size):
    s = GprmKeehiGirderSection(size)
    p = s.polygon
    a, yb, ix, zt, zb, depth = PRINTED[size]
    assert p.is_valid and p.exterior.is_ccw and not p.is_empty
    assert p.bounds[1] == 0 and p.bounds[3] == pytest.approx(depth * 25.4)
    assert p.symmetric_difference(scale(p, xfact=-1, origin=(0, 0))).area < 1e-6
    g = gross_properties(p, 25.4)
    assert g["area"] == pytest.approx(a, abs=0.60)
    assert g["yb"] == pytest.approx(yb, abs=0.03)
    assert g["ix"] == pytest.approx(ix, rel=0.0015)
    assert g["ix"] / (depth - g["yb"]) == pytest.approx(zt, rel=0.0018)
    assert g["ix"] / g["yb"] == pytest.approx(zb, rel=0.0022)
    # Both labelled bevels are preserved; direct source area is higher.
    c = 0.75 * 25.4
    xb = 13 * 25.4
    assert any(x == pytest.approx(xb - c) and y == 0 for x, y in p.exterior.coords)
    assert any(x == pytest.approx(-xb + c) and y == 0 for x, y in p.exterior.coords)
    assert g["area"] < a
    assert s.provenance == "transcribed-with-convention" and s.source_status
    assert s.geometry is not None


def test_gprm_keehi_published_properties_and_geometry():
    run_checks((_check_profile, P("size", list(PRINTED))))


def test_gprm_keehi_public_api_and_explicit_variants():
    assert bridgebeams.GprmKeehiGirderSection is GprmKeehiGirderSection
    assert bridgebeams.us.GprmKeehiGirderSection is GprmKeehiGirderSection
    assert GprmKeehiGirderSection.SIZES == tuple(PRINTED)
    assert GprmKeehiGirderSection("K-IV MOD").dimensions.depth == pytest.approx(62 * 25.4)
    assert GprmKeehiGirderSection("K-IV W").dimensions.top_width == pytest.approx(56.5 * 25.4)
    assert GprmKeehiGirderSection("K-VI W").dimensions.top_width == pytest.approx(57 * 25.4)
    with pytest.raises(ValueError):
        GprmKeehiGirderSection("K-IV W narrow")
