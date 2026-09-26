"""VDOT PCBT bulb-tees, voided slabs and box beams vs VDOT Part 2 Chapter 12.

Published values are literal readings of File Nos. 12.03-5 (PCBT),
12.05-5 (voided slabs) and 12.06-6 (interior box beams), repeated here.
"""

import pytest
from shapely.affinity import scale

from bridgebeams.us.state_common import gross_properties
from bridgebeams.us.state_va_girders import VaBoxBeamSection, VaPcbtSection, VaVoidedSlabSection

from _aggregate import P, run_checks

IN = 25.4
PROVENANCE = {"transcribed", "transcribed-with-convention", "fitted-reconstruction", "estimate"}
CLASSES = (VaPcbtSection, VaVoidedSlabSection, VaBoxBeamSection)

# File 12.03-5: D: (A in^2, yb in, I x10^3 in^4)
PCBT = {29: (634.7, 14.66, 66.8), 37: (690.7, 18.43, 126.0), 45: (746.7, 22.23, 207.3),
        53: (802.7, 26.06, 312.4), 61: (858.7, 29.92, 443.1), 69: (914.7, 33.79, 601.3),
        77: (970.7, 37.67, 788.7), 85: (1026.7, 41.57, 1007.2), 93: (1082.7, 45.48, 1258.5)}
# File 12.05-5: size: (net A in^2, I in^4) -- shear keys NOT deducted
SLAB = {"36x15": (439, 9725), "36x18": (491, 16514), "36x21": (530, 25747),
        "48x15": (569, 12897), "48x18": (628, 21855), "48x21": (703, 34517)}
# File 12.06-6: size: (net A in^2, yb in, I in^4) -- PCI shear keys deducted
BOX = {"36x27": (580, 13.31, 51070), "36x33": (640, 16.25, 86820), "36x39": (700, 19.20, 134100),
       "36x42": (730, 20.68, 162400), "48x27": (724, 13.35, 67380), "48x33": (784, 16.30, 113500),
       "48x39": (844, 19.25, 173700), "48x42": (874, 20.73, 209500)}


def _check_every_size_valid(cls):
    for size in cls.SIZES:
        s = cls(size)
        poly = s.polygon
        assert poly.is_valid and poly.exterior.is_ccw
        assert all(not r.is_ccw for r in poly.interiors)
        assert poly.bounds[1] == pytest.approx(0.0, abs=1e-9)
        assert poly.symmetric_difference(scale(poly, xfact=-1, origin=(0, 0))).area < 1e-2
        assert s.provenance in PROVENANCE and s.source_status
        assert s.geometry is not None


def _check_invalid_size(cls):
    with pytest.raises(ValueError):
        cls("nope")


def _check_pcbt_properties(depth):
    a, yb, i = PCBT[depth]
    s = VaPcbtSection(f"PCBT-{depth}")
    p = gross_properties(s.polygon, IN)
    assert s.polygon.bounds[3] == pytest.approx(depth * IN)
    assert s.polygon.bounds[2] - s.polygon.bounds[0] == pytest.approx(47 * IN)
    # 3/4 in soffit chamfer is the only convention; table is to 0.1 in^2 / 0.01 in / 0.1e3 in^4
    assert p["area"] == pytest.approx(a, abs=0.05)
    assert p["yb"] == pytest.approx(yb, abs=0.005)
    assert p["ix"] / 1e3 == pytest.approx(i, abs=0.05)


def test_pcbt_without_chamfer_would_be_high():
    # Evidence for the chamfer convention: the drawn-but-undimensioned chamfer
    # removes 0.5625 in^2; the key-less sharp-corner outline is 0.55 in^2 over the table.
    p = gross_properties(VaPcbtSection("PCBT-53").polygon, IN)
    assert p["area"] + 2 * 0.75**2 / 2 == pytest.approx(802.7 + 0.55, abs=0.05)


def _check_voided_slab_published_convention_exact(size):
    a, i = SLAB[size]
    p = gross_properties(VaVoidedSlabSection(size, shear_keys=False).polygon, IN)
    assert p["area"] == pytest.approx(a, abs=0.6)  # table rounds to 1 in^2; 96-gon voids
    assert p["ix"] == pytest.approx(i, rel=5e-4)
    assert p["yb"] == pytest.approx(int(size.split("x")[1]) / 2, abs=1e-6)


def _check_voided_slab_with_vdot_key(size):
    # Default outline includes the File 12.05-10 key (8.3 in^2 deducted in total).
    a, _ = SLAB[size]
    keyed = gross_properties(VaVoidedSlabSection(size).polygon, IN)
    plain = gross_properties(VaVoidedSlabSection(size, shear_keys=False).polygon, IN)
    assert plain["area"] - keyed["area"] == pytest.approx(8.297, abs=0.01)
    assert keyed["area"] == pytest.approx(a - 8.3, abs=0.6)


def _check_box_keyless_is_published_plus_20(size):
    # Confirms 6 in slabs / 5 in webs / 3x3 chamfers: PCI key deduction is 20 in^2.
    a, _, _ = BOX[size]
    plain = gross_properties(VaBoxBeamSection(size, shear_keys=False).polygon, IN)
    assert plain["area"] == pytest.approx(a + 20, abs=1e-6)


def _check_box_with_vdot_key_pinned_residuals(size):
    # Pinned: VDOT-drawn key removes 12.8 in^2 rather than the 20 in^2 of the
    # PCI key used by the table, so area is +7.2 in^2, yb +0.03..0.07 in, I +1.0..1.4 %.
    a, yb, i = BOX[size]
    p = gross_properties(VaBoxBeamSection(size).polygon, IN)
    assert p["area"] == pytest.approx(a + 7.2, abs=0.01)
    assert 0.02 < p["yb"] - yb < 0.08
    assert 1.0 < (p["ix"] / i - 1) * 100 < 1.45


def test_box_with_vdot_key_pinned_residuals():
    run_checks((_check_box_with_vdot_key_pinned_residuals, P("size", sorted(BOX))))


def test_us_state_va_girders_catalogue_checks():
    run_checks(
        (_check_every_size_valid, P("cls", CLASSES)),
        (_check_invalid_size, P("cls", CLASSES)),
        (_check_pcbt_properties, P("depth", sorted(PCBT))),
        (_check_voided_slab_published_convention_exact, P("size", sorted(SLAB))),
        (_check_voided_slab_with_vdot_key, P("size", sorted(SLAB))),
        (_check_box_keyless_is_published_plus_20, P("size", sorted(BOX))),
    )
