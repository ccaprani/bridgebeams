"""Caltrans standard girders vs Bridge Design Memo 5.3 (September 2023) tables.

Published values are literal readings of Tables 5.3.4.1-1 to -5, repeated
here. Tolerances per family:
* I: exact geometry; yb printed to 0.1 in, I to 3 significant figures.
* BT: dimensions converted from metric and R 7-7/8 in fillets -> A 0.15 %,
  yb 0.05 in, I 0.45 %. BT49 area misprint pinned.
* WF (pretensioned and PT): tangent r = 10 / 2.5 in fillets -> A 0.03 %,
  yb 0.03 in, I 0.35 %. Odd rows (78/90/102/114) pinned separately.
* TUB: metric conversion -> A 0.1 %, yb 0.035 in, I 0.3 %.
"""

import pytest
from shapely.affinity import scale

from bridgebeams.us.state_ca_girders import (
    CaBathTubSection,
    CaBulbTeeSection,
    CaIGirderSection,
    CaVoidedSlabSection,
    CaWideFlangeSection,
)
from bridgebeams.us.state_common import gross_properties

from _aggregate import P, run_checks

IN = 25.4
PROVENANCE = {"transcribed", "transcribed-with-convention", "fitted-reconstruction", "estimate"}
CLASSES = (CaIGirderSection, CaBulbTeeSection, CaWideFlangeSection, CaBathTubSection, CaVoidedSlabSection)

I_TAB = {"CA I36": (432, 63000, 17.1), "CA I42": (474, 95400, 20.0), "CA I48": (516, 136400, 22.8),
         "CA I54": (558, 186400, 25.7), "CA I60": (600, 246900, 28.6), "CA I66": (642, 318000, 31.6)}
BT_TAB = {"CA BT49": (856, 272373, 25.3), "CA BT55": (925, 373350, 28.4), "CA BT61": (971, 483385, 31.3),
          "CA BT67": (1018, 610718, 34.2), "CA BT73": (1063, 755589, 37.2), "CA BT79": (1110, 919200, 40.1),
          "CA BT85": (1157, 1102271, 43.1)}
WF_TAB = {
    "CA WF48": (882, 274880, 20.69), "CA WF54": (921, 369100, 23.23), "CA WF60": (960, 479620, 25.82),
    "CA WF66": (999, 607130, 28.44), "CA WF72": (1038, 752430, 31.08), "CA WF78": (1075, 913490, 33.77),
    "CA WF84": (1116, 1099400, 36.45), "CA WF90": (1153, 1297900, 39.19), "CA WF96": (1194, 1526600, 41.91),
    "CA WF102": (1231, 1764700, 44.68), "CA WF108": (1272, 2039200, 47.42), "CA WF114": (1309, 2319500, 50.23),
    "CA WF120": (1350, 2643200, 52.99),
    "CA WF48PT": (954, 289440, 20.94), "CA WF54PT": (1002, 389840, 23.54), "CA WF60PT": (1050, 508060, 26.18),
    "CA WF66PT": (1098, 644950, 28.85), "CA WF72PT": (1146, 801460, 31.55), "CA WF78PT": (1192, 975690, 34.29),
    "CA WF84PT": (1242, 1177000, 37.01), "CA WF90PT": (1288, 1393100, 39.80), "CA WF96PT": (1338, 1642000, 42.56),
    "CA WF102PT": (1384, 1902800, 45.38), "CA WF108PT": (1434, 2202900, 48.16), "CA WF114PT": (1480, 2511700, 51.01),
    "CA WF120PT": (1530, 2867100, 53.81)}
TUB_TAB = {"CA TUB55": (1339, 460081, 24.1), "CA TUB61": (1435, 604231, 26.9), "CA TUB67": (1531, 773128, 29.7),
           "CA TUB73": (1627, 968692, 32.6), "CA TUB79": (1723, 1192606, 35.4), "CA TUB85": (1819, 1446551, 38.3)}
WF_ODD = {f"CA WF{d}{v}" for d in (78, 90, 102, 114) for v in ("", "PT")}


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


def _check_table_coverage():
    assert set(CaIGirderSection.SIZES) == set(I_TAB)
    assert set(CaBulbTeeSection.SIZES) == set(BT_TAB)
    assert set(CaWideFlangeSection.SIZES) == set(WF_TAB)
    assert set(CaBathTubSection.SIZES) == set(TUB_TAB)


def _props(cls, size):
    return gross_properties(cls(size).polygon, IN)


def _check_i_girder(size):
    a, i, yb = I_TAB[size]
    p = _props(CaIGirderSection, size)
    assert p["area"] == pytest.approx(a, abs=1e-6)
    assert p["yb"] == pytest.approx(yb, abs=0.05 + 1e-9)  # half a printed unit (I60: 28.650)
    assert p["ix"] == pytest.approx(i, rel=1.5e-3)  # I54: 186,659 vs printed 186,400
    assert CaIGirderSection(size).polygon.bounds[2] * 2 == pytest.approx(19 * IN)


def _check_bulb_tee(size):
    a, i, yb = BT_TAB[size]
    p = _props(CaBulbTeeSection, size)
    assert p["yb"] == pytest.approx(yb, abs=0.05)
    if size == "CA BT49":
        # Pinned misprint: printed 856 in^2, outline 876.1 in^2 (+2.35 %), I +1.24 %.
        assert p["area"] == pytest.approx(876.14, abs=0.05)
        assert p["ix"] / i - 1 == pytest.approx(0.0124, abs=5e-4)
    else:
        assert p["area"] == pytest.approx(a, rel=1.5e-3)
        assert p["ix"] == pytest.approx(i, rel=4.5e-3)


def _check_wide_flange(size):
    a, i, yb = WF_TAB[size]
    p = _props(CaWideFlangeSection, size)
    if size in WF_ODD:
        # Pinned: odd rows are ~2.2 in^2 below the uniform per-6-in progression.
        assert p["area"] - a == pytest.approx(2.2, abs=0.05)
        assert p["yb"] - yb == pytest.approx(-0.04, abs=0.015)
        assert p["ix"] / i - 1 == pytest.approx(0.0012, abs=3e-4)
    else:
        assert p["area"] == pytest.approx(a, rel=3e-4)
        assert p["yb"] == pytest.approx(yb, abs=0.03)
        assert p["ix"] == pytest.approx(i, rel=3.5e-3)


def _check_bath_tub(size):
    a, i, yb = TUB_TAB[size]
    p = _props(CaBathTubSection, size)
    assert p["area"] == pytest.approx(a, rel=1e-3)
    assert p["yb"] == pytest.approx(yb, abs=0.035)
    assert p["ix"] == pytest.approx(i, rel=3e-3)
    s = CaBathTubSection(size)
    assert s.polygon.bounds[2] * 2 == pytest.approx(s.dimensions.top_width)
    assert s.dimensions.bottom_width == pytest.approx(59 * IN)


def _check_voided_slab_printed_dimensions():
    s = CaVoidedSlabSection("SIV-48")
    b = s.polygon.bounds
    assert b[2] - b[0] == pytest.approx(48 * IN)
    assert b[3] == pytest.approx(21 * IN)
    assert [round(v[2] / IN, 6) for v in s.dimensions.voids] == [12, 9, 12]
    assert len(CaVoidedSlabSection("SI-36").polygon.interiors) == 0
    assert all(CaVoidedSlabSection(k).provenance == "estimate" for k in CaVoidedSlabSection.SIZES)


def test_us_state_ca_girders_catalogue_checks():
    run_checks(
        (_check_every_size_valid, P("cls", CLASSES)),
        (_check_invalid_size, P("cls", CLASSES)),
        _check_table_coverage,
        (_check_i_girder, P("size", sorted(I_TAB))),
        (_check_bulb_tee, P("size", sorted(BT_TAB))),
        (_check_wide_flange, P("size", sorted(WF_TAB))),
        (_check_bath_tub, P("size", sorted(TUB_TAB))),
        _check_voided_slab_printed_dimensions,
    )


def test_ca_bt49_area_misprint_pinned():
    run_checks((_check_bulb_tee, P("size", ["CA BT49"])))


def test_ca_wf_odd_rows_pinned():
    run_checks((_check_wide_flange, P("size", sorted(WF_ODD))))
