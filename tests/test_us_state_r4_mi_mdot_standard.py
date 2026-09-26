"""MDOT PC/BDG standard beams: sheet dimensions and printed-property checks.

I-beams (PC-1Q) are checked against the BDG 6.60.01 BEAM PROPERTIES table
(A, St, Sb, I printed for Types I-IV); the filleted 1800 beam (PC-4J)
against BDG 6.60.02 with a 1 % tolerance; the bulb tees (PC-5D) against
the BDG 6.60.03 table, where the template reproduces A, Ybot and Ixx to
0.1 %. The 70 in I-beam (PC-2L) has no printed properties and is checked
by its exact dimension-chain closure and outline geometry.
"""

import pytest
from shapely.affinity import scale

from bridgebeams.us.state_common import gross_properties
from bridgebeams.us.state_r4_mi_mdot_standard import (
    MiMdot1800Section,
    MiMdot70ISection,
    MiMdotBulbTeeSection,
    MiMdotISection,
)

from _aggregate import P, run_checks

IN = 25.4

# Printed BDG 6.60.01 properties: size -> (A, St, Sb, I)
I_PRINTED = {
    "I28": (276, 1475, 1805, 22800),
    "I36": (369, 2530, 3220, 51000),
    "I45": (560, 5070, 6190, 125000),
    "I54": (789, 8910, 10550, 261000),
}
# Printed BDG 6.60.03 properties (49 in flange): size -> (A, Ybot, Ixx)
BT_PRINTED = {
    "BT36": (878.3, 18.2, 145592),
    "BT48": (974.3, 24.0, 305994),
    "BT54": (1022.3, 27.0, 412056),
    "BT60": (1070.3, 29.9, 536513),
    "BT66": (1118.3, 32.9, 680229),
    "BT72": (1166.3, 35.8, 844069),
}
# Printed BDG 6.60.02 properties for the 1800 beam
B1800_PRINTED = {"area": 875, "st": 16600, "sb": 18800, "ix": 624700}


def _props(section):
    return gross_properties(section.polygon, IN)


def _check_valid(cls, size):
    s = cls(size)
    p = s.polygon
    assert p.is_valid and p.exterior.is_ccw
    assert p.bounds[1] == pytest.approx(0.0, abs=1e-9)
    assert p.bounds[3] == pytest.approx(s.row["depth"] * IN, abs=1e-6)
    assert s.provenance in ("transcribed", "transcribed-with-convention")
    assert s.source_status
    assert s.geometry is not None


def _check_symmetric(cls, size):
    p = cls(size).polygon
    assert p.symmetric_difference(scale(p, xfact=-1, origin=(0, 0))).area < 1e-2


def _check_i_printed(size):
    s = MiMdotISection(size)
    g = _props(s)
    depth = s.row["depth"]
    yb = g["yb"]
    st, sb = g["ix"] / (depth - yb), g["ix"] / yb
    a_p, st_p, sb_p, i_p = I_PRINTED[size]
    assert g["area"] == pytest.approx(a_p, rel=0.01), (g["area"], a_p)
    assert st == pytest.approx(st_p, rel=0.01)
    assert sb == pytest.approx(sb_p, rel=0.01)
    assert g["ix"] == pytest.approx(i_p, rel=0.01)


def _check_bt_printed(size):
    a_p, yb_p, i_p = BT_PRINTED[size]
    g = _props(MiMdotBulbTeeSection(size))
    assert g["area"] == pytest.approx(a_p, rel=0.005), (g["area"], a_p)
    assert g["yb"] == pytest.approx(yb_p, abs=0.15)
    assert g["ix"] == pytest.approx(i_p, rel=0.005)


def _check_1800_printed():
    g = _props(MiMdot1800Section("1800"))
    depth = MiMdot1800Section("1800").row["depth"]
    yb = g["yb"]
    assert g["area"] == pytest.approx(B1800_PRINTED["area"], rel=0.01)
    assert g["ix"] / (depth - yb) == pytest.approx(B1800_PRINTED["st"], rel=0.01)
    assert g["ix"] / yb == pytest.approx(B1800_PRINTED["sb"], rel=0.01)
    assert g["ix"] == pytest.approx(B1800_PRINTED["ix"], rel=0.01)


def _check_i70_geometry():
    s = MiMdot70ISection("I70")
    g = _props(s)
    # Chain closure: 6 + 2 + 1 1/2 + 49 1/2 + 3 1/2 + 7 1/2 = 70 in
    r = s.row
    assert r["tip"] + r["taper"] + r["step"] + r["web_height"] + r["splay"] + r["bulb"] == 70
    assert s.row["top_width"] == 30 and s.row["bottom_width"] == 26 and s.row["web"] == 6
    # Sanity: solid-rectangle bound on the area and near-middepth centroid
    assert 0.30 * 30 * 70 < g["area"] < 30 * 70
    assert 32 < g["yb"] < 38


def _check_bt_matches_r3():
    """The BDG 49 in bulb tee equals the OR15-182 BTB 002 outline."""
    from bridgebeams.us.state_r3_mi_beams import MiBulbTeeSection

    for size in ("BT36", "BT42", "BT48"):
        r3 = MiBulbTeeSection(size)
        r4 = MiMdotBulbTeeSection(size)
        assert r3.polygon.symmetric_difference(r4.polygon).area < 1e-6  # mm^2


def test_r4_mi_mdot_standard():
    all_sizes = ([(MiMdotISection, s) for s in MiMdotISection.SIZES]
                 + [(MiMdot70ISection, "I70"), (MiMdot1800Section, "1800")]
                 + [(MiMdotBulbTeeSection, s) for s in MiMdotBulbTeeSection.SIZES])
    ids = [f"{c.__name__}:{s}" for c, s in all_sizes]
    run_checks(
        (_check_valid, P("cls,size", all_sizes, ids=ids)),
        (_check_symmetric, P("cls,size", all_sizes, ids=ids)),
        (_check_i_printed, P("size", list(I_PRINTED))),
        (_check_bt_printed, P("size", list(BT_PRINTED))),
        _check_1800_printed,
        _check_i70_geometry,
        _check_bt_matches_r3,
    )
