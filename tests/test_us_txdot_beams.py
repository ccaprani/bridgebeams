"""TxDOT girders, boxes, X-beams, slab and decked slab beams vs printed properties.

Printed values are repeated literally from the sources (IGD rev. 2023,
WF-IGD 2024, BB 2006/2012, XB 2022, PSB 2017 and PSTRS14 v6.1 Feb 2016
Figures 1, 8, 11, 16) rather than read back from the package JSON.
Tolerances: exact-transcription families are held to print rounding.
Families with undimensioned detail carry explicit per-family bounds that
are the observed residual envelope, stated in the JSON geometry notes.
"""

import pytest
from shapely.affinity import scale

from bridgebeams.us.state_common import gross_properties
from bridgebeams.us.txdot_girders import (
    TxDotDoubleTSection,
    TxDotIGirderSection,
    TxDotLegacyIBeamSection,
    TxDotUBeamSection,
    TxDotWideFlangeGirderSection,
)
from bridgebeams.us.txdot_slabs_boxes import (
    TxDotBoxBeamSection,
    TxDotDeckedSlabBeamSection,
    TxDotSlabBeamSection,
    TxDotXBeamSection,
)

from _aggregate import P, run_checks

IN = 25.4
CLASSES = (
    TxDotIGirderSection, TxDotWideFlangeGirderSection, TxDotLegacyIBeamSection,
    TxDotUBeamSection, TxDotDoubleTSection, TxDotBoxBeamSection, TxDotXBeamSection,
    TxDotSlabBeamSection, TxDotDeckedSlabBeamSection,
)
PROVENANCE = {"transcribed", "transcribed-with-convention", "fitted-reconstruction", "estimate"}


def props(sec):
    return gross_properties(sec.polygon, unit=IN)


def _check_every_size_valid_symmetric(cls):
    for size in cls.SIZES:
        s = cls(size)
        p = s.polygon
        assert p.is_valid and p.exterior.is_ccw
        assert all(not r.is_ccw for r in p.interiors)
        assert p.bounds[1] == pytest.approx(0.0, abs=1e-9)
        assert p.symmetric_difference(scale(p, xfact=-1, origin=(0, 0))).area < 1e-3
        assert s.provenance in PROVENANCE
        assert isinstance(s.source_status, str) and s.source_status
        assert s.geometry is not None


def _check_invalid_size_raises(cls):
    with pytest.raises(ValueError):
        cls("nonsense")


# ------------------------------------------------------------ Tx girders
TX = {  # A, Yb, Ix, Iy  (IGD sheet 1, rev. 3-23)
    "Tx28": (585, 12.98, 52772, 40559), "Tx34": (627, 15.51, 88355, 40731),
    "Tx40": (669, 18.10, 134990, 40902), "Tx46": (761, 20.10, 198089, 46478),
    "Tx54": (817, 23.51, 299740, 46707), "Tx62": (910, 28.28, 463072, 57351),
    "Tx70": (966, 31.91, 628747, 57579),
}
WF = {  # WF-IGD sheet 2, Aug 2024
    "WF-Tx28": (847, 16.47, 77175, 177678), "WF-Tx34": (889, 19.86, 129931, 177849),
    "WF-Tx40": (931, 23.21, 198439, 178021), "WF-Tx46": (1023, 25.77, 295105, 183597),
    "WF-Tx54": (1079, 29.99, 443002, 183825), "WF-Tx62": (1246, 36.27, 660613, 286765),
    "WF-Tx70": (1302, 40.69, 918917, 286994),
}


def _check_tx_girder_published(size):
    g = props(TxDotIGirderSection(size))
    a, yb, ix, iy = TX[size]
    assert g["area"] == pytest.approx(a, abs=0.51)
    assert g["yb"] == pytest.approx(yb, abs=0.005)
    assert g["ix"] == pytest.approx(ix, abs=0.5)
    assert g["iy"] == pytest.approx(iy, abs=0.5)


def _check_wf_girder_published(size):
    g = props(TxDotWideFlangeGirderSection(size))
    a, yb, ix, iy = WF[size]
    assert g["area"] == pytest.approx(a, abs=0.51)
    assert g["yb"] == pytest.approx(yb, abs=0.005)
    assert g["iy"] == pytest.approx(iy, abs=0.5)
    if size == "WF-Tx62":
        # Pinned: printed 660,613 is exactly 20,000 below the outline value.
        assert g["ix"] == pytest.approx(680613, abs=0.5)
    else:
        assert g["ix"] == pytest.approx(ix, abs=0.5)


def _check_tx_key_dimensions():
    s = TxDotIGirderSection("Tx62")
    assert s.dimensions.depth == pytest.approx(62 * IN)
    assert s.dimensions.top_width == pytest.approx(42 * IN)
    assert s.dimensions.bottom_width == pytest.approx(32 * IN)
    assert TxDotWideFlangeGirderSection("WF-Tx40").dimensions.top_width == pytest.approx(72 * IN)


# ------------------------------------------------------------ legacy I
LEG = {"A": (275.4, 12.61, 22658), "B": (360.3, 14.93, 43177), "C": (494.9, 17.09, 82602),
       "54": (493.4, 25.53, 164022), "72": (863.4, 33.73, 532060)}


def _check_legacy_i_published(size):
    g = props(TxDotLegacyIBeamSection(size))
    a, yb, ix = LEG[size]
    assert g["area"] == pytest.approx(a, abs=0.05)
    assert g["yb"] == pytest.approx(yb, abs=0.005)
    assert g["ix"] == pytest.approx(ix, abs=1)


def test_legacy_54_uses_corrected_web():
    # Pinned: printed F = 30 in does not close D = 54; F = 32 is used.
    s = TxDotLegacyIBeamSection("54")
    assert s.row["F"] == 32 and s.row["printed_F"] == 30
    assert s.provenance == "fitted-reconstruction"


# ------------------------------------------------------------ U beams
def test_u_beams_residuals_pinned():
    pub = {"U40": (977.0, 16.35, 183050), "U54": (1121.1, 22.46, 403458)}
    for size, (a, yb, ix) in pub.items():
        s = TxDotUBeamSection(size)
        assert s.dimensions.top_width == pytest.approx({"U40": 89, "U54": 96}[size] * IN)
        assert s.dimensions.bottom_width == pytest.approx(55 * IN)
        g = props(s)
        # Undimensioned corner detail: observed +0.15..0.28% area, +0.23% I.
        assert 0 < g["area"] - a < 0.003 * a
        assert abs(g["yb"] - yb) < 0.025
        assert 0 < g["ix"] - ix < 0.0025 * ix


# ------------------------------------------------------------ double T
DT = {
    "6T22": (706, 14.74, 26395), "7T22": (778, 15.13, 27797), "8T22": (850, 15.46, 28998),
    "6T28": (795, 18.77, 51233), "7T28": (867, 19.29, 54010), "8T28": (939, 19.73, 56395),
    "6T36": (899, 24.15, 98984), "7T36": (971, 24.81, 104422), "8T36": (1043, 25.37, 109138),
    "6HT22": (834, 13.70, 34048), "7HT22": (906, 14.13, 36122), "8HT22": (978, 14.48, 37922),
    "6HT28": (971, 17.36, 67033), "7HT28": (1043, 17.89, 71159), "8HT28": (1115, 18.35, 74780),
    "6HT36": (1139, 22.22, 132841), "7HT36": (1211, 22.86, 140925), "8HT36": (1283, 23.43, 148125),
}


def _check_double_t_estimate_envelope(size):
    g = props(TxDotDoubleTSection(size))
    a, yb, ix = DT[size]
    # Omitted fillets/edge keys: +4.0..4.5 in^2, yb +0.03..0.06 in, I +0.5..0.95%.
    assert 3.9 < g["area"] - a < 4.6
    assert 0.02 < g["yb"] - yb < 0.06
    assert 0.004 < (g["ix"] - ix) / ix < 0.0096


# ------------------------------------------------------------ boxes / X / slabs
BOX = {
    "4B20": (591.8, 9.81, 28086), "5B20": (717.8, 9.88, 35234),
    "4B28": (678.8, 13.62, 68745), "5B28": (804.8, 13.74, 85370),
    "4B34": (798.8, 16.08, 115655), "5B34": (924.8, 16.28, 142161),
    "4B40": (918.8, 18.69, 176607), "4B40-C": (943.8, 18.37, 180159),
    "5B40": (1044.8, 18.93, 215300), "5B40-C": (1069.8, 18.64, 219007),
}
XB = {
    "4XB20": (689, 9.53, 29124), "5XB20": (839, 9.53, 36621),
    "4XB28": (781, 13.14, 72798), "5XB28": (931, 13.13, 90793),
    "4XB34": (919, 15.59, 123757), "5XB34": (1069, 15.61, 152730),
    "4XB40": (1057, 18.18, 190840), "5XB40": (1207, 18.20, 233453),
}
SLAB = {"4SB12": (573.0, 6.00, 6876), "4SB15": (716.2, 7.50, 13429),
        "5SB12": (717.0, 6.00, 8604), "5SB15": (896.2, 7.50, 16805)}
DS = {"6DS20": (1087, 10.82, 43704), "7DS20": (1183, 11.24, 46580), "8DS20": (1231, 11.43, 47879),
      "6DS23": (1123, 12.54, 64997), "7DS23": (1219, 13.05, 69202), "8DS23": (1267, 13.27, 71095)}


# ti: I tolerance (in^4). Decked slab void/edge are a 4-parameter least-squares
# fit to 9 printed values per depth, leaving I residuals up to 2.1 in^4.
def _check_voided_and_slab_published(cls, table, ta, ti):
    for size, (a, yb, ix) in table.items():
        s = cls(size)
        g = props(s)
        assert g["area"] == pytest.approx(a, abs=ta), size
        assert g["yb"] == pytest.approx(yb, abs=0.006), size
        assert g["ix"] == pytest.approx(ix, abs=ti), size


def _check_box_voids_and_widths():
    s = TxDotBoxBeamSection("5B40-C")
    assert len(s.polygon.interiors) == 1
    assert s.dimensions.width == pytest.approx(59.75 * IN)
    assert TxDotXBeamSection("4XB20").dimensions.width == pytest.approx(47.75 * IN)
    assert TxDotDeckedSlabBeamSection("8DS23").dimensions.width == pytest.approx(95.75 * IN)
    assert TxDotDeckedSlabBeamSection("6DS20").provenance == "fitted-reconstruction"


def test_us_txdot_beams_catalogue_checks():
    run_checks(
        (_check_every_size_valid_symmetric, P("cls", CLASSES)),
        (_check_invalid_size_raises, P("cls", CLASSES)),
        (_check_tx_girder_published, P("size", TX)),
        (_check_wf_girder_published, P("size", WF)),
        _check_tx_key_dimensions,
        (_check_legacy_i_published, P("size", LEG)),
        (_check_double_t_estimate_envelope, P("size", DT)),
        (_check_voided_and_slab_published, P("cls,table,ta,ti", [
    (TxDotBoxBeamSection, BOX, 0.05, 1.0), (TxDotXBeamSection, XB, 0.5, 1.0),
    (TxDotSlabBeamSection, SLAB, 0.1, 1.0), (TxDotDeckedSlabBeamSection, DS, 0.5, 2.5)])),
        _check_box_voids_and_widths,
    )


def test_txdot_wf_tx62_inertia_pinned():
    run_checks((_check_wf_girder_published, P("size", ["WF-Tx62"])))
