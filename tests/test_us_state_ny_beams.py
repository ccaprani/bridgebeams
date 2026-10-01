"""NYSDOT BD-PC 2026 units vs the printed property tables.

Printed values used literally in spot checks come from BD-PC1/2 (PDF pp1-2),
BD-PC14 (p14), BD-PC15 (p15), BD-PC31 (p31) and BD-PC36 (p36). Known
source inconsistencies are pinned individually rather than hidden by a
family-wide tolerance.
"""

import numpy as np
import pytest
from shapely.affinity import scale

from bridgebeams.us.state_common import ccw_polygon, circle, gross_properties, mirror_half
from bridgebeams.us.state_ny_beams import (
    NyBoxBeamSection,
    NyPcefBulbTeeSection,
    NySlabUnitSection,
    keyed_unit_half_in,
)

from _aggregate import P, run_checks

IN = 25.4
CLASSES = (NyBoxBeamSection, NySlabUnitSection, NyPcefBulbTeeSection)
PROVENANCE = {"transcribed", "transcribed-with-convention", "fitted-reconstruction", "estimate"}


def props(sec):
    return gross_properties(sec.polygon, IN)


def _check_all_sizes_valid_symmetric(cls):
    for size in cls.SIZES:
        s = cls(size)
        poly = s.polygon
        assert poly.is_valid and poly.exterior.is_ccw, size
        assert all(not r.is_ccw for r in poly.interiors)
        assert poly.bounds[1] == pytest.approx(0.0, abs=1e-9)
        assert poly.symmetric_difference(scale(poly, xfact=-1, origin=(0, 0))).area < 1e-2
        assert s.provenance in PROVENANCE
        assert s.source_status
        assert s.geometry is not None


def _check_invalid_size_raises(cls):
    with pytest.raises(ValueError):
        cls("B99x99")


def _check_counts_and_widths():
    assert len(NyBoxBeamSection.SIZES) == 22
    assert len(NySlabUnitSection.SIZES) == 8
    assert len(NyPcefBulbTeeSection.SIZES) == 6
    b = NyBoxBeamSection("B48x33").polygon.bounds
    assert b[2] - b[0] == pytest.approx(48 * IN) and b[3] == pytest.approx(33 * IN)


# ----------------------------------------------------------- boxes / slabs
def _check_b36_box_areas_exact():
    for d in range(24, 55, 3):
        s = NyBoxBeamSection(f"B36x{d}")
        assert props(s)["area"] == pytest.approx(s.published["area_in2"], abs=0.1)
    # literal: B36"x24" = 536.6 in2
    assert props(NyBoxBeamSection("B36x24"))["area"] == pytest.approx(536.6, abs=0.1)


def test_pinned_tabulated_yb_is_half_depth():
    """NYSDOT prints yb = D/2; the keyed outline's true centroid is lower."""
    for cls in (NyBoxBeamSection, NySlabUnitSection):
        for size in cls.SIZES:
            s = cls(size)
            d = s.dimensions.depth / IN
            assert s.published["yb_in"] == pytest.approx(d / 2)
            assert -0.09 < props(s)["yb"] - d / 2 < -0.01, size


def test_pinned_box_inertia_column_not_smooth():
    for w in (36, 48):
        pub = [NyBoxBeamSection(f"B{w}x{d}").published["ix_in4"] for d in range(24, 55, 3)]
        mod = [props(NyBoxBeamSection(f"B{w}x{d}"))["ix"] for d in range(24, 55, 3)]
        # I is cubic in depth: model third differences are constant (135 in4),
        # the printed column's swing between -4400 and +2500 in4
        assert np.ptp(np.diff(mod, 3)) < 1.0 and np.ptp(np.diff(pub, 3)) > 3000
        for p, m in zip(pub, mod):
            assert m == pytest.approx(p, rel=0.0095)


def test_pinned_b48_box_areas_below_model():
    for d in range(24, 55, 3):
        s = NyBoxBeamSection(f"B48x{d}")
        r = props(s)["area"] / s.published["area_in2"] - 1
        assert 0.004 < r < 0.009, d


def _check_solid_and_18in_slabs_match():
    for size in ("S36x12", "S48x12", "S36x18", "S48x18"):
        s = NySlabUnitSection(size)
        p = props(s)
        assert p["area"] == pytest.approx(s.published["area_in2"], abs=0.12), size
        assert p["ix"] == pytest.approx(s.published["ix_in4"], rel=1e-4), size
    # literal: S36"x12" = 423.1 in2, 5107.4 in4
    p = props(NySlabUnitSection("S36x12"))
    assert p["area"] == pytest.approx(423.1, abs=0.1) and p["ix"] == pytest.approx(5107.4, abs=0.5)


def test_pinned_s36x21_area():
    s = NySlabUnitSection("S36x21")
    p = props(s)
    assert p["area"] - s.published["area_in2"] == pytest.approx(-1.4, abs=0.1)
    assert p["ix"] == pytest.approx(s.published["ix_in4"], rel=1e-4)


def test_pinned_15in_slab_voids():
    for size, gap in (("S36x15", -0.9), ("S48x15", -2.9)):
        s = NySlabUnitSection(size)
        assert props(s)["area"] - s.published["area_in2"] == pytest.approx(gap, abs=0.15)


def test_pinned_s48x21_table_uses_three_12in_voids():
    s = NySlabUnitSection("S48x21")
    assert [v[1] for v in s.row["voids_in"]] == [12.0, 10.0, 12.0]  # as drawn
    assert props(s)["area"] > s.published["area_in2"] + 30
    t = {"soffit_chamfer_in": 0.75, "lower_band_in": 4.0, "upper_band_in": 4.0,
         "recess_from_bottom_face_in": 0.75, "top_band_inset_in": 0.375}
    alt = ccw_polygon(mirror_half(keyed_unit_half_in(48, 21, t)),
                      [circle(x, 10.5, 6.0, 256) for x in (-14, 0, 14)])
    p = gross_properties(alt)
    assert p["area"] == pytest.approx(646.4, abs=0.1)
    assert p["ix"] == pytest.approx(33426.2, rel=2e-3)


# ----------------------------------------------------------------- girders
def _check_pcef_matches_table():
    for size in NyPcefBulbTeeSection.SIZES:
        s = NyPcefBulbTeeSection(size)
        p = props(s)
        assert p["area"] == pytest.approx(s.published["area_in2"], abs=0.3), size
        assert p["yb"] == pytest.approx(s.published["yb_in"], abs=0.006), size
        if size == "PCEF-63":
            # printed 500945 is a transposition of the computed 500495
            assert s.published["ix_in4"] == 500945
            assert p["ix"] == pytest.approx(500495, abs=1)
        else:
            assert p["ix"] == pytest.approx(s.published["ix_in4"], rel=1e-5), size


def test_us_state_ny_beams_catalogue_checks():
    run_checks(
        (_check_all_sizes_valid_symmetric, P("cls", CLASSES)),
        (_check_invalid_size_raises, P("cls", CLASSES)),
        _check_counts_and_widths,
        _check_b36_box_areas_exact,
        _check_solid_and_18in_slabs_match,
        _check_pcef_matches_table,
    )
