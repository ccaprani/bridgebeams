"""Somaco girders scaled from catalogue schematics (estimates)."""

import pytest

from bridgebeams._geometry import section_properties
from bridgebeams.ro.r2_somaco import SomacoGirderSection

from _aggregate import P, run_checks

# size: (depth mm, catalogue volume/length m2, allowed relative residual, sign-pinned)
EXPECTED = {
    "GP 52E": (520, 0.178, 0.01),
    "GP 105E": (1050, 0.533, 0.01),
    "GP 93": (930, 0.316, 0.04),  # pinned -3.4 %
    "GP 95E": (950, 0.479, 0.10),  # pinned -8.9 %: GP105E icon reused at h = 95
}


def _check_valid(size):
    sec = SomacoGirderSection(size)
    p = sec.polygon
    assert p.is_valid and p.exterior.is_ccw
    assert p.bounds[1] == pytest.approx(0.0, abs=1e-6)
    assert sec.provenance == "estimate"
    assert sec.geometry is not None


def _check_area_vs_volume_per_length(size):
    depth, mean, tol = EXPECTED[size]
    p = SomacoGirderSection(size).polygon
    assert p.bounds[3] == pytest.approx(depth)
    area = section_properties(p)["area"] / 1e6
    assert abs(area / mean - 1) <= tol


def test_gp95e_and_gp93_pinned_low():
    a95 = section_properties(SomacoGirderSection("GP 95E").polygon)["area"] / 1e6
    a93 = section_properties(SomacoGirderSection("GP 93").polygon)["area"] / 1e6
    assert -0.10 < a95 / 0.479 - 1 < -0.08
    assert -0.045 < a93 / 0.316 - 1 < -0.025


def _check_gp220_printed_widths_and_end_zone():
    p = SomacoGirderSection("GP 220-40").polygon
    assert p.bounds == pytest.approx((-600, 0, 600, 2200), abs=1.0)
    assert p.bounds[2] - p.bounds[0] == pytest.approx(1200, abs=1)
    from shapely.geometry import LineString
    assert p.intersection(LineString([(-900, 1), (900, 1)])).length == pytest.approx(880, abs=5)
    # Midspan E-E is lighter than the 34.85 m3 / 40 m mean that includes D-D ends.
    area = section_properties(p)["area"] / 1e6
    assert 0.78 < area / 0.871 < 0.88


def _check_invalid():
    with pytest.raises(ValueError):
        SomacoGirderSection("GP 85E")


def test_ro_r2_somaco_catalogue_checks():
    run_checks(
        (_check_valid, P("size", SomacoGirderSection.SIZES)),
        (_check_area_vs_volume_per_length, P("size", list(EXPECTED))),
        _check_gp220_printed_widths_and_end_zone,
        _check_invalid,
    )
