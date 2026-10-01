"""MDOT OR15-182 App. K box beams and bulb tees: sheet dimensions and checks.

No section properties are printed. Boxes are checked by hand-summed areas
from the printed callouts; bulb tees against the BTB 002 'APPROX WEIGHT'
row (= area x T x 150 pcf). Brice et al. (2021) has no Michigan table.
"""

import pytest
from shapely.affinity import scale

from bridgebeams.us.state_common import gross_properties
from bridgebeams.us.state_r3_mi_beams import (
    MiBulbTeeSection,
    MiSideBySideBoxBeamSection,
    MiSpreadBoxBeamSection,
)

from _aggregate import P, run_checks

IN = 25.4
BOX = {  # depth, width, top, bottom, web, void chamfer (inches, as printed)
    "17x36": (17, 36, 5, 5, 5, 1.5),
    "21x36": (21, 36, 5, 5, 5, 1.5),
    "21x48": (21, 48, 6, 6, 4, 1.5),
    "27x48": (27, 48, 6, 6, 4, 3),
    "33x48": (33, 48, 6, 6, 4, 3),
    "39x48": (39, 48, 6, 6, 4, 3),
    "48x48": (48, 48, 6, 6, 4, 3),
}
BEVEL = 0.5
# Estimated key (3 in top zone and 4 in key height printed): net area removed per keyed side
KEY_AREA = 3 * 0.375 + 0.5 * (0.75 + 0.375) * 0.375 + 0.75 * (4 - 0.375) + 0.5 * 0.75 * 0.75


def _box_area(d, w, top, bot, web, ch):
    void = (w - 2 * web) * (d - top - bot) - 2 * ch * ch
    return w * d - 2 * 0.5 * BEVEL**2 - void


def _area(poly):
    return gross_properties(poly, IN)["area"]


def _check_valid(cls, size):
    s = cls(size)
    p = s.polygon
    assert p.is_valid and p.exterior.is_ccw
    assert all(not r.is_ccw for r in p.interiors)
    assert p.bounds[1] == pytest.approx(0.0, abs=1e-9)
    assert s.provenance in ("transcribed", "transcribed-with-convention")
    assert s.source_status
    assert s.geometry is not None


def _check_symmetric(cls, size):
    p = cls(size).polygon
    assert p.symmetric_difference(scale(p, xfact=-1, origin=(0, 0))).area < 1e-2


def _check_spread_area_and_bounds(size):
    d, w, top, bot, web, ch = BOX[size[3:]]
    s = MiSpreadBoxBeamSection(size)
    x0, _, x1, y1 = s.polygon.bounds
    assert (x1 - x0, y1) == (pytest.approx(w * IN), pytest.approx(d * IN))
    assert len(s.polygon.interiors) == 1
    assert _area(s.polygon) == pytest.approx(_box_area(d, w, top, bot, web, ch))


def _check_ssbb_area(size):
    fam, kind = size.split("-")
    d, w, top, bot, web, ch = BOX[fam[4:]]
    s = MiSideBySideBoxBeamSection(size)
    x0, _, x1, y1 = s.polygon.bounds
    assert (x1 - x0, y1) == (pytest.approx(w * IN), pytest.approx(d * IN))
    if kind == "INT":
        expected = _box_area(d, w, top, bot, web, ch) - 2 * KEY_AREA
    elif fam == "SSBB17x36":
        assert len(s.polygon.interiors) == 0  # drawn solid
        expected = w * d - BEVEL**2 - KEY_AREA
    else:
        expected = _box_area(d, w, 9, bot, web, ch) - KEY_AREA
    assert _area(s.polygon) == pytest.approx(expected)


def _check_fascia_key_side(size):
    p = MiSideBySideBoxBeamSection(size).polygon
    top_xs = [x / IN for x, y in p.exterior.coords if y == pytest.approx(p.bounds[3])]
    assert max(top_xs) == pytest.approx(24 if "x48" in size else 18)
    assert min(top_xs) == pytest.approx(-(24 if "x48" in size else 18) + 0.375)


def _check_bulb_tee_dims(size):
    s = MiBulbTeeSection(size)
    x0, _, x1, y1 = s.polygon.bounds
    assert y1 == pytest.approx(int(size[2:]) * IN)
    assert x1 - x0 == pytest.approx(49 * IN)
    assert s.dimensions.bottom_width == pytest.approx(40 * IN)
    assert s.dimensions.web == pytest.approx(8 * IN)


def _check_bulb_tee_hand_area(size):
    d = int(size[2:])
    area = (49 * 5 + 0.5 * (49 + 14) * 3 + 0.5 * (14 + 8) * 3 + 8 * (d - 11 - 14.5)
            + 0.5 * (8 + 12) * 2 + 0.5 * (12 + 40) * 7 + 40 * 5.5 - 0.75**2)
    assert _area(MiBulbTeeSection(size).polygon) == pytest.approx(area)


def _check_bulb_tee_weight(span, depth, tons):
    area = _area(MiBulbTeeSection(f"BT{depth}").polygon)
    assert area / 144 * span * 150 / 2000 == pytest.approx(tons, rel=0.002)  # print rounding


def _check_invalid_sizes():
    for cls, bad in ((MiSpreadBoxBeamSection, "SBB42x48"),
                     (MiSideBySideBoxBeamSection, "SSBB48x48-INT"),
                     (MiBulbTeeSection, "BT54")):
        with pytest.raises(ValueError):
            cls(bad)


def test_us_state_r3_mi_beams_catalogue_checks():
    assert len(MiSpreadBoxBeamSection.SIZES) == 7
    assert len(MiSideBySideBoxBeamSection.SIZES) == 10
    assert len(MiBulbTeeSection.SIZES) == 3
    all_sizes = [(c, s) for c in (MiSpreadBoxBeamSection, MiSideBySideBoxBeamSection, MiBulbTeeSection)
                 for s in c.SIZES]
    symmetric = [(c, s) for c, s in all_sizes if not s.endswith("-FAS")]
    run_checks(
        (_check_valid, P("cls,size", all_sizes, ids=[s for _, s in all_sizes])),
        (_check_symmetric, P("cls,size", symmetric, ids=[s for _, s in symmetric])),
        (_check_spread_area_and_bounds, P("size", MiSpreadBoxBeamSection.SIZES)),
        (_check_ssbb_area, P("size", MiSideBySideBoxBeamSection.SIZES)),
        (_check_fascia_key_side, P("size", [s for s in MiSideBySideBoxBeamSection.SIZES if s.endswith("FAS")])),
        (_check_bulb_tee_dims, P("size", MiBulbTeeSection.SIZES)),
        (_check_bulb_tee_hand_area, P("size", MiBulbTeeSection.SIZES)),
        (_check_bulb_tee_weight, P("span,depth,tons", [(70, 36, 32), (80, 36, 36.6), (90, 42, 43.4),
                                                        (100, 48, 50.8), (110, 48, 55.8)])),
        _check_invalid_sizes,
    )
