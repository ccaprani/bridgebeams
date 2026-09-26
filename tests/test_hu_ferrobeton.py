"""Ferrobeton (Hungary) FP, FPT, ITG and FI-150 sections."""

import pytest

from bridgebeams._geometry import section_properties
from bridgebeams.hu import (
    FerrobetonFi150Section,
    FerrobetonFpSection,
    FerrobetonFptSection,
    FerrobetonItgSection,
)

from _aggregate import P, run_checks

ALL = [
    (cls, size)
    for cls in (FerrobetonFpSection, FerrobetonFptSection, FerrobetonItgSection, FerrobetonFi150Section)
    for size in cls.SIZES
]
PROVENANCE = {"transcribed", "transcribed-with-convention", "fitted-reconstruction", "estimate"}


def _check_valid_polygon(cls, size):
    sec = cls(size)
    poly = sec.polygon
    assert poly.is_valid and poly.exterior.is_ccw
    assert poly.bounds[1] == pytest.approx(0.0)
    assert sec.provenance in PROVENANCE
    assert sec.source_status == "producer catalogue"
    assert sec.geometry is not None


# ---- FP: plain polygon, analytic area from printed chain (cm)
def _check_fp_area_and_widths(size, depth, body):
    sec = FerrobetonFpSection(size)
    area_cm2 = 50 * 6.0 - 2 * 0.5 * 1.5 * 1.5 + 0.5 * (50 + 43) / 2 + 43 * body
    assert section_properties(sec.polygon)["area"] == pytest.approx(area_cm2 * 100, rel=1e-12)
    assert sec.polygon.bounds == pytest.approx((-250, 0, 250, depth * 10))
    assert sec.provenance == "transcribed"


# ---- FPT: tabulated Súly at 2500 kg/m³
def _check_fpt_mass_matches_catalogue(size):
    sec = FerrobetonFptSection(size)
    mass = section_properties(sec.polygon)["area"] * 1e-6 * 2500
    # nothing fitted: CAD-measured outline reproduces Súly within 0.1%
    assert mass == pytest.approx(sec.mass_per_length, rel=1e-3)
    assert sec.polygon.bounds == pytest.approx((-350, 0, 350, int(size.split("-")[1]) * 10))


def test_fpt_45_mass_discrepancy_pinned():
    # Template extrapolated to 45 cm gives 492.3 kg/m vs tabulated 455 (+8.2%).
    sec = FerrobetonFptSection("FPT-45")
    mass = section_properties(sec.polygon)["area"] * 1e-6 * 2500
    assert sec.provenance == "estimate"
    assert mass / sec.mass_per_length - 1 == pytest.approx(0.0821, abs=0.001)


def test_fpt_70_50_outline_and_mass_discrepancy_pinned():
    sec = FerrobetonFptSection("FPT-70/50")
    area = section_properties(sec.polygon)["area"]
    assert area == pytest.approx((50 * 16.75 + 1.75 * 40 + 30 * 51.5) * 100)
    assert sec.polygon.bounds == pytest.approx((-250, 0, 250, 700))
    # 613.1 kg/m vs tabulated 620 kg/m (-1.1%), unresolved
    assert area * 1e-6 * 2500 / 620 - 1 == pytest.approx(-0.0111, abs=0.0005)


def _check_fpt_web_step_equals_mass_step():
    a70 = section_properties(FerrobetonFptSection("FPT-70").polygon)["area"]
    a80 = section_properties(FerrobetonFptSection("FPT-80").polygon)["area"]
    assert a80 - a70 == pytest.approx(300 * 100)


# ---- ITG
def _check_itg90_chain_and_area():
    sec = FerrobetonItgSection("ITG-90")
    d = sec.dimensions
    assert d.overall_width == pytest.approx(612)
    assert sec.polygon.bounds == pytest.approx((-306, 0, 306, 900))
    # sharp polygon area from the printed chain (cm²)
    area = (
        (35 + 36.4) / 2 * 18 + (36.4 + 16) / 2 * 8.6 + 16 * 35.2 + (16 + 36.4) / 2 * 11.1
        + (36.4 + 61.2) / 2 * 2.8 + (61.2 + 60) / 2 * 9.8 + (48.6 + 46.6) / 2 * 4.5
    )
    assert section_properties(sec.polygon)["area"] == pytest.approx(area * 100, rel=1e-9)
    assert sec.provenance == "transcribed"


def _check_itg_other_depths_are_estimates_and_differ_only_in_web():
    a90 = section_properties(FerrobetonItgSection("ITG-90").polygon)["area"]
    for size, dh in (("ITG-70", -200), ("ITG-110", 200)):
        sec = FerrobetonItgSection(size)
        assert sec.provenance == "estimate"
        assert section_properties(sec.polygon)["area"] - a90 == pytest.approx(160 * dh)
    assert "ITG-45" not in FerrobetonItgSection.SIZES


# ---- FI-150
def _check_fi150_bounds_and_fillets_reduce_little():
    sec = FerrobetonFi150Section()
    assert sec.polygon.bounds == pytest.approx((-400, 0, 400, 1500))
    sharp = (
        (57 + 60) / 2 * 4 + 60 * 12 + (60 + 14.6) / 2 * 23 + 14.6 * 93 + (14.6 + 80) / 2 * 8
        + 80 * 7.5 + (80 + 72) / 2 * 0.5 + (72 + 71) / 2 * 2
    ) * 100
    area = section_properties(sec.polygon)["area"]
    # web fillets (R7.5, R15) add concrete; tip radii remove a little
    assert area > sharp
    assert area / sharp - 1 < 0.02
    assert sec.provenance == "estimate"


def _check_invalid_size(cls):
    with pytest.raises(ValueError):
        cls("ITG-45" if cls is FerrobetonItgSection else "bogus")


def test_hu_ferrobeton_catalogue_checks():
    run_checks(
        (_check_valid_polygon, P("cls,size", ALL)),
        (_check_fp_area_and_widths, P("size,depth,body", [("FP-20A", 20, 13.5), ("FP-30A", 30, 23.5), ("FP-37A", 37, 30.5)])),
        (_check_fpt_mass_matches_catalogue, P("size", ["FPT-70", "FPT-80", "FPT-90", "FPT-100", "FPT-130"])),
        _check_fpt_web_step_equals_mass_step,
        _check_itg90_chain_and_area,
        _check_itg_other_depths_are_estimates_and_differ_only_in_web,
        _check_fi150_bounds_and_fillets_reduce_little,
        (_check_invalid_size, P("cls", [FerrobetonFpSection, FerrobetonFptSection, FerrobetonItgSection, FerrobetonFi150Section])),
    )
