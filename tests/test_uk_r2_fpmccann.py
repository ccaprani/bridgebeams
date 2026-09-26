"""FP McCann (UK) Precast Bridge Beams v1.0 (2025): TY, TYE, Y, YE, MY, MYE, SY, W, Box."""

import json
from importlib import resources

import numpy as np
import pytest
from shapely.affinity import scale
from shapely.geometry import LineString

import bridgebeams.ie as ie
from bridgebeams.uk.r2_fpmccann import (
    FpMcCannBoxBeamSection,
    FpMcCannMyBeamSection,
    FpMcCannMyeBeamSection,
    FpMcCannSyBeamSection,
    FpMcCannTyBeamSection,
    FpMcCannTyeBeamSection,
    FpMcCannWBeamSection,
    FpMcCannYBeamSection,
    FpMcCannYeBeamSection,
)

from _aggregate import P, run_checks

DATA = json.loads(resources.files("bridgebeams.uk").joinpath("data/r2_fpmccann.json").read_text(encoding="utf-8"))
FAM = DATA["families"]
CLASSES = [FpMcCannTyBeamSection, FpMcCannTyeBeamSection, FpMcCannYBeamSection, FpMcCannYeBeamSection,
           FpMcCannMyBeamSection, FpMcCannMyeBeamSection, FpMcCannSyBeamSection, FpMcCannWBeamSection,
           FpMcCannBoxBeamSection]
ALL = [(c, s) for c in CLASSES for s in c.SIZES]

# (area rel, Yb abs mm, I rel, Yc abs mm) per family; justified in JSON "tolerances".
TOL = {"ty_type1": (5e-4, 0.1, 1.5e-3, None), "ty_type2": (1e-4, 0.1, 1e-3, None), "tye": (3e-4, 0.1, 1e-3, 0.25),
       "y": (2e-3, 0.6, 3.5e-3, None), "ye": (1e-3, 0.5, 2e-3, 0.6), "my": (1e-4, 0.15, 1e-3, None),
       "mye": (1e-4, 0.1, 1e-3, None), "sy": (5e-4, 0.15, 5e-4, None), "w": (5e-4, 0.1, 1e-3, None),
       "box": (1e-5, 0.5, 4e-3, None)}
SW_TOL = 2.5e-3  # self-weight vs area at 25 kN/m3


def props(poly):
    def ring(coords):
        c = np.asarray(coords)[:-1]
        x, y = c[:, 0], c[:, 1]
        x2, y2 = np.roll(x, -1), np.roll(y, -1)
        cr = x * y2 - x2 * y
        return (cr.sum() / 2, ((y + y2) * cr).sum() / 6, ((y * y + y * y2 + y2 * y2) * cr).sum() / 12,
                ((x + x2) * cr).sum() / 6)
    a, s, i, sx = ring(poly.exterior.coords)
    for r in poly.interiors:
        da, ds, di, dsx = ring(r.coords)
        a, s, i, sx = a + da, s + ds, i + di, sx + dsx
    cy = s / a
    return a, cy, i - a * cy * cy, sx / a


def key_of(sec):
    return sec.size.split(" (Type")[0] if sec.family.startswith("ty_") else sec.size


def width_at(poly, y):
    return poly.intersection(LineString([(-2000, y), (2000, y)])).length


def _check_tolerances_match_data():
    for fam, (ta, ty, ti, tc) in TOL.items():
        t = FAM[fam]["tolerances"]
        assert (t["area_rel"], t["yb_abs_mm"], t["I_rel"], t["yc_abs_mm"]) == (ta, ty, ti, tc)
    assert DATA["source"]["sha256"] == "243c2d0f902f52842eeb161a6082d4d0cf1a0d0d90e096996075f116b3723644"


def _check_profile_count():
    assert sum(len(c.SIZES) for c in CLASSES) == 84


def _check_valid_outline(cls, size):
    sec = cls(size)
    p = sec.polygon
    assert p.is_valid and p.exterior.is_ccw and not p.interiors
    assert p.bounds[1] == pytest.approx(0.0) and p.bounds[3] == pytest.approx(sec.published["depth_mm"])
    assert sec.provenance in ("transcribed", "transcribed-with-convention", "fitted-reconstruction", "estimate")
    assert "FP McCann" in sec.source_status
    assert sec.geometry is not None


def _check_published_properties(cls, size):
    sec = cls(size)
    fam = sec.family
    pub = sec.published
    d = pub["depth_mm"]
    a, cy, i, cx = props(sec.polygon)
    res = {"area_rel": a / pub["area_mm2"] - 1, "yb_abs": cy - pub["yb_mm"],
           "I_zb_rel": i / (pub["zb_1e6mm3"] * pub["yb_mm"] * 1e6) - 1,
           "I_zt_rel": i / (pub["zt_1e6mm3"] * (d - pub["yb_mm"]) * 1e6) - 1,
           "sw_rel": pub["self_weight_kN_m"] / (pub["area_mm2"] * 25e-6) - 1}
    if "yc_from_face_mm" in pub:
        face = 375.0 if fam == "tye" else -375.0
        res["yc_abs"] = abs(face - cx) - pub["yc_from_face_mm"]
    ta, ty, ti, tc = TOL[fam]
    lim = {"area_rel": ta, "yb_abs": ty, "I_zb_rel": ti, "I_zt_rel": ti, "sw_rel": SW_TOL, "yc_abs": tc}
    pins = FAM[fam]["pinned"].get(key_of(sec), {})
    for q, v in res.items():
        if q in pins:
            # pinned source discrepancy: reproduce the recorded residual and confirm it is real
            assert v == pytest.approx(pins[q]["residual"], abs=1e-4 if q.endswith("_rel") else 0.01)
            assert abs(v) > lim[q]
        else:
            assert abs(v) <= lim[q], (q, v)


def test_pins_are_the_expected_ones():
    pinned = {fam: {k: sorted(v) for k, v in FAM[fam]["pinned"].items()} for fam in FAM}
    assert pinned["tye"] == {"TYE4": ["I_zt_rel"], "TYE6": ["I_zb_rel"]}
    assert pinned["sy"] == {"SY6": ["I_zb_rel", "I_zt_rel", "yb_abs"]}
    assert pinned["mye"]["MYE7"] == ["I_zt_rel", "sw_rel"] and len(pinned["mye"]) == 7
    assert all(v == ["I_zb_rel", "I_zt_rel", "area_rel", "yb_abs"] for v in pinned["w"].values())
    assert len(pinned["w"]) == 6
    assert pinned["ye"] == {"YE8": ["yc_abs"]} and pinned["box"] == {"SD6 (750)": ["yb_abs"]}
    for fam in ("ty_type1", "ty_type2", "y", "my"):
        assert pinned[fam] == {}


# ---- printed dimensions ----------------------------------------------------------------
def _check_ty_printed(size):
    sec = FpMcCannTyBeamSection(size)
    p, d = sec.polygon, sec.dimensions.depth
    assert width_at(p, 0) == pytest.approx(700) and width_at(p, 25) == pytest.approx(750)
    assert width_at(p, 320) == pytest.approx(185)
    tw = FAM["ty_type2"]["transcribed_dims_mm"]["top_width_printed"]
    if sec.dimensions.variant == "type2":
        assert width_at(p, d - 1e-6) == pytest.approx(tw[sec.designation], abs=0.5)
    else:
        assert width_at(p, d - 1) == pytest.approx(FAM["ty_type1"]["transcribed_dims_mm"]["cap_width"][sec.designation])
        ledge = (width_at(p, d - 50.5) - width_at(p, d - 49.5)) / 2
        assert 40.0 <= ledge <= 42.0


def _check_ty_web_line_construction_point():
    # printed 164 wide at y = 268 on the web-line extension, 400 at TY10 top (Type 2)
    p = FpMcCannTyBeamSection("TY10 (Type 2)").polygon
    assert width_at(p, 850 - 1e-6) == pytest.approx(400, abs=0.01)
    assert 185 + 2 * (268 - 320) * 107.5 / 530 == pytest.approx(164, abs=0.2)


def _check_tye_face(size):
    sec = FpMcCannTyeBeamSection(size)
    p, d = sec.polygon, sec.dimensions.depth
    assert p.bounds[2] == pytest.approx(375)
    assert (375, d) in list(p.exterior.coords) and (375, 25) in list(p.exterior.coords)
    cut = p.intersection(LineString([(-2000, d - 1), (2000, d - 1)]))
    assert cut.length == pytest.approx(FAM["tye"]["transcribed_dims_mm"]["face_to_cap_edge"][size])
    assert width_at(p, 320) == pytest.approx(467.5)


def _check_y_printed(size):
    sec = FpMcCannYBeamSection(size)
    p, d = sec.polygon, sec.dimensions.depth
    assert width_at(p, 25) == pytest.approx(750) and width_at(p, 202) == pytest.approx(740)
    assert width_at(p, d - 1) == pytest.approx(FAM["y"]["transcribed_dims_mm"]["cap_width"][size])
    assert width_at(p, d - 56) == pytest.approx(sec.dimensions.cap + 80, abs=0.5)
    # narrowest web (fillet tangent) close to printed 216 minimum
    webmin = min(width_at(p, y) for y in np.arange(400, 480, 1.0))
    assert 214 <= webmin <= 220


def _check_ye_printed(size):
    sec = FpMcCannYeBeamSection(size)
    p, d = sec.polygon, sec.dimensions.depth
    assert p.bounds[0] == pytest.approx(-375)
    top = p.intersection(LineString([(-2000, d - 1), (2000, d - 1)]))
    assert top.length == pytest.approx(FAM["ye"]["transcribed_dims_mm"]["rebate_to_cap_edge"][size])
    assert top.bounds[0] == pytest.approx(-335)
    y = FpMcCannYBeamSection(size[0] + size[2:]).polygon  # same right (web) side as the Y beam
    assert p.intersection(LineString([(0, 300), (2000, 300)])).length == pytest.approx(
        y.intersection(LineString([(0, 300), (2000, 300)])).length)


def _check_my_printed(size):
    sec = FpMcCannMyBeamSection(size)
    p, d = sec.polygon, sec.dimensions.depth
    assert width_at(p, 0) == pytest.approx(920) and width_at(p, 50) == pytest.approx(970)
    assert width_at(p, 150) == pytest.approx(300)
    expected_top = 440 if d >= 500 else 300 + 140 * (d - 150) / 350
    assert width_at(p, d - 1e-6) == pytest.approx(expected_top, abs=0.01)
    assert sec.provenance == "fitted-reconstruction"


def _check_mye_printed(size):
    sec = FpMcCannMyeBeamSection(size)
    p = sec.polygon
    assert p.bounds[2] == pytest.approx(485)
    assert p.intersection(LineString([(-2000, 150.0001), (2000, 150.0001)])).length == pytest.approx(635, abs=0.01)


def _check_sy_printed(size):
    sec = FpMcCannSyBeamSection(size)
    p, d = sec.polygon, sec.dimensions.depth
    assert width_at(p, 202) == pytest.approx(750 - 2 * 5 * 177 / 227, abs=0.01)
    assert width_at(p, d - 1) == pytest.approx(240)  # cap convention (label '50 x 50' conflicts)
    assert width_at(p, d - 50 - 1e-6) == pytest.approx(320, abs=0.01)


def _check_w_printed(size):
    sec = FpMcCannWBeamSection(size)
    p, dim = sec.polygon, sec.dimensions
    top = FAM["w"]["transcribed_dims_mm"]["top"][size]
    assert p.bounds[2] * 2 == pytest.approx(top["L1"])
    assert width_at(p, 25) == pytest.approx(1510) and width_at(p, 0) == pytest.approx(1460)
    assert p.intersection(LineString([(0, 1e-6), (0, 5000)])).length == pytest.approx(160)
    # two webs cut at mid-depth: cap = L2 each side at the very top
    assert width_at(p, dim.depth - 1) == pytest.approx(2 * top["L2"])
    if size == "W3":
        assert dim.l3 == pytest.approx(1086) and top["L3"] == 1058  # printed L3 misprint
    else:
        assert dim.l3 == pytest.approx(top["L3"])
    # outer face at 82 degrees
    assert np.degrees(np.arctan2(dim.depth - 50 - 25, top["L1"] / 2 - 755)) == pytest.approx(82, abs=0.4)


def _check_box_printed(size):
    sec = FpMcCannBoxBeamSection(size)
    p, dim = sec.polygon, sec.dimensions
    assert width_at(p, 30) == pytest.approx(dim.bottom_width)
    assert width_at(p, dim.depth - 1) == pytest.approx(dim.bottom_width - 130)
    assert dim.top_width in (365, 620, 840)


# ---- comparison with the Banagher / ie implementation ------------------------------------------
def ie_polygon(cls, size):
    if cls is FpMcCannTyBeamSection:
        des, t = size.split(" (Type ")
        return ie.IeTYBeamSection(des, "bs" if t.startswith("1") else "ss").polygon
    if cls is FpMcCannTyeBeamSection:
        return scale(ie.IeTYBeamSection(size, "bs").polygon, -1, 1, origin=(0, 0))
    if cls is FpMcCannYBeamSection:
        return ie.IeYBeamSection(size).polygon
    if cls is FpMcCannYeBeamSection:
        return ie.IeYEBeamSection(size).polygon
    if cls is FpMcCannMyBeamSection:
        return ie.IeMYBeamSection(size).polygon
    if cls is FpMcCannMyeBeamSection:
        return scale(ie.IeMYEBeamSection(size).polygon, -1, 1, origin=(0, 0))
    if cls is FpMcCannSyBeamSection:
        return ie.IeSYBeamSection(size).polygon
    if cls is FpMcCannWBeamSection:
        return ie.IeWBeamSection(size).polygon
    k, w = size.split(" (")
    return ie.IeSolidBoxBeamSection(f"{k} ({ {'495': 1, '750': 2, '970': 3}[w.rstrip(')')] })").polygon


VERDICT_BOUNDS = {"identical": (0, 10), "near-identical": (10, 150), "different": (1000, 1e9)}


def _check_banagher_comparison(cls, size):
    sec = cls(size)
    comp = FAM[sec.family]["banagher_ie_comparison"]
    rec = comp["per_size"][key_of(sec)]
    sd = sec.polygon.symmetric_difference(ie_polygon(cls, size)).area
    assert sd == pytest.approx(rec["symmetric_difference_mm2"], abs=0.5)
    lo, hi = VERDICT_BOUNDS[comp["verdict"]]
    if comp["verdict"] == "identical":
        assert sd <= hi
    else:
        assert lo <= sd <= hi


def _check_banagher_verdicts():
    v = {fam: FAM[fam]["banagher_ie_comparison"]["verdict"] for fam in FAM}
    assert v == {"ty_type1": "near-identical", "ty_type2": "identical", "tye": "near-identical", "y": "different",
                 "ye": "different", "my": "different", "mye": "different", "sy": "different", "w": "different",
                 "box": "identical"}


def _check_invalid_sizes():
    for cls, bad in ((FpMcCannTyBeamSection, "TY3 (Type 1)"), (FpMcCannTyBeamSection, "TY11 (Type 2)"),
                     (FpMcCannTyeBeamSection, "TYE3"), (FpMcCannYBeamSection, "Y9"), (FpMcCannYeBeamSection, "YE9"),
                     (FpMcCannMyBeamSection, "MY8"), (FpMcCannMyeBeamSection, "MYE8"), (FpMcCannSyBeamSection, "SY7"),
                     (FpMcCannWBeamSection, "W2"), (FpMcCannBoxBeamSection, "SD7 (750)"),
                     (FpMcCannBoxBeamSection, "SD1 (1500)")):
        with pytest.raises(ValueError):
            cls(bad)


def test_uk_r2_fpmccann_catalogue_checks():
    run_checks(
        _check_tolerances_match_data,
        _check_profile_count,
        (_check_valid_outline, P("cls,size", ALL)),
        (_check_published_properties, P("cls,size", ALL)),
        (_check_ty_printed, P("size", FpMcCannTyBeamSection.SIZES)),
        _check_ty_web_line_construction_point,
        (_check_tye_face, P("size", FpMcCannTyeBeamSection.SIZES)),
        (_check_y_printed, P("size", FpMcCannYBeamSection.SIZES)),
        (_check_ye_printed, P("size", FpMcCannYeBeamSection.SIZES)),
        (_check_my_printed, P("size", FpMcCannMyBeamSection.SIZES)),
        (_check_mye_printed, P("size", FpMcCannMyeBeamSection.SIZES)),
        (_check_sy_printed, P("size", FpMcCannSyBeamSection.SIZES)),
        (_check_w_printed, P("size", FpMcCannWBeamSection.SIZES)),
        (_check_box_printed, P("size", FpMcCannBoxBeamSection.SIZES)),
        (_check_banagher_comparison, P("cls,size", ALL)),
        _check_banagher_verdicts,
        _check_invalid_sizes,
    )


def test_fpmccann_published_discrepancies_pinned():
    """TYE4/TYE6, SY6, MYE, W, YE8 and SD6 (750) residuals recorded under JSON "pinned"."""
    run_checks((_check_published_properties, P("cls,size", [(c, s) for c, s in ALL
                                                             if key_of(c(s)) in FAM[c(s).family]["pinned"]])))


def test_fpmccann_sy_cap_and_w_l3_misprint_pinned():
    run_checks((_check_sy_printed, P("size", FpMcCannSyBeamSection.SIZES)),
               (_check_w_printed, P("size", FpMcCannWBeamSection.SIZES)))
