"""Haitsma HKO, HKO-XL, HRP and HIP girders against the published tables.

Tolerances: published areas/inertias have three significant figures
(+/-0.3% area), centroids are whole millimetres. The HKO outline uses an
estimated root fillet (limits 0.8% A, 1.5 mm v, 0.6% I); HRP/HIP keys
and rebates are scaled/fitted (0.3% A, 1.5 mm V, 0.4% I); HKO-XL is a
scaled-and-fitted estimate (0.7% A, 1.5 mm Z, 0.6% I). Source outliers
are pinned individually below, not absorbed by wider tolerances.
"""

import pytest

from bridgebeams._geometry import section_properties
from bridgebeams.nl import (
    HaitsmaHipSection,
    HaitsmaHkoSection,
    HaitsmaHkoXlSection,
    HaitsmaHrpSection,
)

PINNED_I = {"HKO650": 0.0154, "HIP1700-natte-knoop": 0.0174}
PINNED_A = {"HIP1200-natte-knoop": -0.0068}


def _published(sec):
    r = sec.published
    area = r.get("Ab_mm2") or r.get("A_mm2")
    cy = r.get("v_mm") or r.get("V_mm") or r.get("Z_mm")
    ixx = r.get("I_mm4") or r["I_1e6mm4"] * 1e6
    return area, cy, ixx


CASES = (
    [(HaitsmaHkoSection, s, 0.008, 1.5, 0.006) for s in HaitsmaHkoSection.SIZES]
    + [(HaitsmaHkoXlSection, s, 0.007, 1.5, 0.006) for s in HaitsmaHkoXlSection.SIZES]
    + [(HaitsmaHrpSection, s, 0.003, 1.5, 0.004) for s in HaitsmaHrpSection.SIZES]
    + [(HaitsmaHipSection, s, 0.004, 1.5, 0.004) for s in HaitsmaHipSection.SIZES]
)


@pytest.mark.parametrize("cls,size,tol_a,tol_v,tol_i", CASES)
def test_published_properties(cls, size, tol_a, tol_v, tol_i):
    sec = cls(size)
    poly = sec.polygon
    assert poly.is_valid and poly.exterior.is_ccw
    props = section_properties(poly)
    area, cy, ixx = _published(sec)
    ra = props["area"] / area - 1
    ri = props["ixx"] / ixx - 1
    if size in PINNED_A:
        assert ra == pytest.approx(PINNED_A[size], abs=0.001)
    else:
        assert abs(ra) < tol_a
    assert abs(props["cy"] - cy) < tol_v
    if size in PINNED_I:
        assert ri == pytest.approx(PINNED_I[size], abs=0.001)
    else:
        assert abs(ri) < tol_i
    assert abs(props["cx"]) < 1e-6
    assert sec.geometry is not None


def test_hko_bounds_and_inertia_multiplier():
    sec = HaitsmaHkoSection("HKO600")
    minx, miny, maxx, maxy = sec.polygon.bounds
    assert (maxx - minx, miny, maxy) == pytest.approx((990.0, 0.0, 600.0))
    top = [x for x, y in sec.polygon.exterior.coords if abs(y - 600) < 1e-9]
    assert max(top) - min(top) == pytest.approx(484.0)
    # printed "10,57" with header mm4: the multiplier is 1e9
    assert section_properties(sec.polygon)["ixx"] / 10.57 == pytest.approx(1e9, rel=0.01)


def test_hrp_and_hip_key_widths():
    hrp = HaitsmaHrpSection("HRP1000").polygon
    assert hrp.bounds == pytest.approx((-585.0, 0.0, 585.0, 1000.0))
    nk = HaitsmaHipSection("HIP1500-natte-knoop").polygon
    assert nk.bounds == pytest.approx((-740.0, 0.0, 740.0, 1500.0))
    top = [x for x, y in nk.exterior.coords if abs(y - 1500) < 1e-9]
    assert max(top) - min(top) == pytest.approx(880.0)
    dl = HaitsmaHipSection("HIP1500-druklaag").polygon
    wide = [x for x, y in dl.exterior.coords if abs(y - (1500 - 90)) < 1e-9]
    assert max(wide) - min(wide) == pytest.approx(1440.0)


def test_hko_xl_is_estimate_with_printed_width():
    sec = HaitsmaHkoXlSection("HKO-XL800")
    assert sec.provenance == "estimate"
    minx, _, maxx, maxy = sec.polygon.bounds
    assert maxx - minx == pytest.approx(1180.0)
    assert maxy == pytest.approx(800.0)


def test_provenance_and_status():
    for cls in (HaitsmaHkoSection, HaitsmaHkoXlSection, HaitsmaHrpSection, HaitsmaHipSection):
        assert cls.provenance in {"transcribed", "transcribed-with-convention", "fitted-reconstruction", "estimate"}
        assert cls.source_status


@pytest.mark.parametrize("cls,bad", [(HaitsmaHkoSection, "HKO750"), (HaitsmaHkoXlSection, "HKO-XL850"),
                                     (HaitsmaHrpSection, "HRP1700"), (HaitsmaHipSection, "HIP2400-druklaag")])
def test_invalid_size(cls, bad):
    with pytest.raises(ValueError):
        cls(bad)
