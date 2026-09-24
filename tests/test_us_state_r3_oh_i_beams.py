"""ODOT PSID-1-13 I-beams vs Brice et al. (2021) Table A.10 and PSID-1-13 printed tables."""

import pytest
from shapely.affinity import scale
from shapely.geometry import Polygon

from bridgebeams.us.state_common import gross_properties, mirror_half
from bridgebeams.us.state_r3_oh_i_beams import OhAashtoIBeamSection, OhWfBeamSection

from _aggregate import P, run_checks

IN = 25.4
ALL = (OhAashtoIBeamSection, OhWfBeamSection)
CASES = [(c, s) for c in ALL for s in c.SIZES]


def _props(cls, size):
    return gross_properties(cls(size).polygon, IN)


def _sharp_props(cls, size):
    """Properties with the 3/4 in soffit chamfers squared off."""
    half = [tuple(p) for p in cls(size).row["right_half"]]
    half = [half[0], (half[2][0], 0.0)] + half[3:]
    return gross_properties(Polygon(mirror_half(half)), 1.0)


def _check_valid_symmetric(cls, size):
    s = cls(size)
    p = s.polygon
    assert p.is_valid and p.exterior.is_ccw
    assert p.bounds[1] == pytest.approx(0.0, abs=1e-9)
    assert p.symmetric_difference(scale(p, xfact=-1, origin=(0, 0))).area < 1e-2
    assert s.provenance == "transcribed" and s.source_status
    assert s.geometry is not None
    assert s.dimensions.soffit_chamfer == pytest.approx(0.75 * IN)


def _check_invalid_size_raises(cls):
    with pytest.raises(ValueError):
        cls("WF78-49")


def _check_wf_dimensions(size):
    d = OhWfBeamSection(size).dimensions
    assert d.depth == pytest.approx(int(size[2:4]) * IN)
    assert (d.top_width, d.bottom_width, d.web_width) == pytest.approx((49 * IN, 40 * IN, 8 * IN))


# Brice et al. 2021 Table A.10 is reproduced to every printed digit
# (A 0.1 in2, y 0.01 in, Ix/Iy 1 in4): exact-arithmetic outline.
def _check_brice(cls, size):
    b = cls(size).published_brice2021
    g = _props(cls, size)
    assert g["area"] == pytest.approx(b["area"], abs=0.05)
    assert g["yb"] == pytest.approx(b["yb"], abs=0.006)
    assert g["ix"] == pytest.approx(b["ix"], abs=1)
    assert g["iy"] == pytest.approx(b["iy"], abs=1)


# PSID-1-13 sheet 1 printed properties for II/III/IV/Mod IV 60/66 are those
# of the UNchamfered section (pinned discrepancy, see JSON "discrepancies").
def _check_odot_sheet1_unchamfered(size):
    o = OhAashtoIBeamSection(size).published
    g = _sharp_props(OhAashtoIBeamSection, size)
    assert g["area"] == pytest.approx(o["area"], abs=0.5)
    assert g["yb"] == pytest.approx(o["yb"], abs=0.006)
    assert g["ix"] == pytest.approx(o["ix"], rel=1.5e-4)


def _check_wf_odot_printed(size):
    o = OhWfBeamSection(size).published
    g = _props(OhWfBeamSection, size)
    assert g["yb"] == pytest.approx(o["yb"], abs=0.05)
    assert g["ix"] == pytest.approx(o["ix"], rel=6e-4)


def test_us_state_r3_oh_i_beams_catalogue_checks():
    run_checks(
        (_check_valid_symmetric, P("cls,size", CASES)),
        (_check_invalid_size_raises, P("cls", ALL)),
        (_check_wf_dimensions, P("size", OhWfBeamSection.SIZES)),
        (_check_brice, P("cls,size", [c for c in CASES if c[1] not in ("II", "III", "IV")])),
        (_check_odot_sheet1_unchamfered, P("size", ("II", "III", "IV", "MOD-IV-60", "MOD-IV-66"))),
        (_check_wf_odot_printed, P("size", OhWfBeamSection.SIZES)),
    )


def test_oh_mod_iv_72_printed_matches_chamfered_outline():
    """Unlike the other sheet-1 rows, Mod IV 72 is printed for the chamfered section."""
    o = OhAashtoIBeamSection("MOD-IV-72").published
    g = _props(OhAashtoIBeamSection, "MOD-IV-72")
    assert g["area"] == pytest.approx(o["area"], abs=0.5)
    assert g["yb"] == pytest.approx(o["yb"], abs=0.005)
    assert g["ix"] == pytest.approx(o["ix"], abs=1)


def test_oh_wf_printed_area_exceeds_outline():
    """PSID-1-13 prints every WF area 0.4 in2 above the CAD outline (Brice agrees with the outline)."""
    for size in OhWfBeamSection.SIZES:
        o = OhWfBeamSection(size).published
        assert o["area"] - _props(OhWfBeamSection, size)["area"] == pytest.approx(0.4, abs=0.05)
