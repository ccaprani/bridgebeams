"""Spanbeton SKK/PIQ/SJP/SJP-flex/SRP/ZIP/ZIPXL against the published tables.

Published values are the bare precast ("Grootheden prefabligger") columns.
Properties are computed here including box voids (polygon interiors) and,
for SJP/SJP-flex, the transverse openings smeared along the span (the
tables state "stijfheid t.p.v. de sparingen").

Tolerances per family (tables give A to 3 s.f., Zb to 1 mm):
* SKK: 2 % A, 4 % I, 5 mm Zb (void haunches/ledge measured from the vector
  drawing). Zb for SKK 700-1500 is pinned (published ~h/2, model 8-16 mm up).
* PIQ: 3.5 % I; A and Zb pinned family-wide (published Ab exceeds the hollow
  self-weight, which the model matches).
* SJP: 1.2 % A/I, 7 mm Zb (fillets omitted). SJP-300 I pinned.
* SJP-flex: 2.2 % A, 4 % I, 7 mm Zb. SJP-flex 300-400 I pinned.
* SRP: 0.6 % A, 1 mm Zb; I pinned family-wide (published 5-5.5 % higher).
* ZIP: 3 % A (published consistently 2-3 % high; self-weight matches 0.4 %),
  1.2 % I, 3 mm Zb. ZIP-700 Zb pinned (source typo).
* ZIPXL 1800-2400: 4.2 % A, 5 % I, 3 mm Zb (systematic, self-weight 0.2 %).
* ZIPXL 1000-1700: A, Zb, I pinned family-wide (property table inconsistent
  with the dimensioned outline and with its own self-weight column).
"""

import json
import math
from importlib import resources

import pytest
from shapely.geometry import LineString, Polygon, box
from shapely.geometry.polygon import orient

from bridgebeams.nl.r2_spanbeton import (
    SpanbetonPiqSection,
    SpanbetonSjpFlexSection,
    SpanbetonSjpSection,
    SpanbetonSkkSection,
    SpanbetonSrpSection,
    SpanbetonZipSection,
    SpanbetonZipxlSection,
)

from _aggregate import P, run_checks

CLASSES = {
    "skk": SpanbetonSkkSection,
    "piq": SpanbetonPiqSection,
    "sjp": SpanbetonSjpSection,
    "sjp_flex": SpanbetonSjpFlexSection,
    "srp": SpanbetonSrpSection,
    "zip": SpanbetonZipSection,
    "zipxl": SpanbetonZipxlSection,
}
ALL = [(k, s) for k, c in CLASSES.items() for s in c.SIZES]
SMEAR = {  # fraction removed, band y0, y1
    "sjp": (math.pi * 40**2 / (80 * 250), 132.0, 212.0),
    "sjp_flex": (145 / 250, 160.0, 260.0),
}
DATA = json.loads(resources.files("bridgebeams.nl").joinpath("data/r2_spanbeton.json").read_text(encoding="utf-8"))


def _ring(coords):
    c = list(coords)[:-1]
    a = s = i = 0.0
    for (x1, y1), (x2, y2) in zip(c, c[1:] + c[:1]):
        cr = x1 * y2 - x2 * y1
        a += cr / 2
        s += (y1 + y2) * cr / 6
        i += (y1 * y1 + y1 * y2 + y2 * y2) * cr / 12
    return a, s, i


def _props(poly):
    """Area, centroid height, Ixx including holes (signed ring terms)."""
    a, s, i = _ring(poly.exterior.coords)
    for r in poly.interiors:
        da, ds, di = _ring(r.coords)
        a, s, i = a + da, s + ds, i + di
    yb = s / a
    return a, yb, i - a * yb * yb


def _model(key, sec):
    poly = sec.polygon
    a, yb, i = _props(poly)
    if key in SMEAR:
        f, y0, y1 = SMEAR[key]
        band = orient(poly.intersection(box(-2000, y0, 2000, y1)), 1.0)
        ab, ybb, ib = _props(band)
        ah = f * ab
        an = a - ah
        ybn = (a * yb - ah * ybb) / an
        i = i + a * (yb - ybn) ** 2 - (f * ib + ah * (ybb - ybn) ** 2)
        a, yb = an, ybn
    return a, yb, i


def _residuals(key, sec):
    r = sec.published
    a, yb, i = _model(key, sec)
    ib = r["Ib_1e9_mm4"] * 1e9 if "Ib_1e9_mm4" in r else r["Ib_1e6_mm4"] * 1e6
    w = r.get("self_weight_hollow_kN_m") or r["self_weight_kN_m"]
    return {"dA_rel": a / (r["Ab_1e3_mm2"] * 1e3) - 1, "dZb_mm": yb - r["Zb_mm"], "dI_rel": i / ib - 1,
            "dSelfWeight_rel": a * 25e-6 / w - 1}


def _width_at(poly, y):
    return poly.intersection(LineString([(-5000, y), (5000, y)])).length


def _check_valid_ccw_and_metadata(key, size):
    sec = CLASSES[key](size)
    p = sec.polygon
    assert p.is_valid and p.exterior.is_ccw
    assert p.bounds[1] == pytest.approx(0.0)
    n_voids = 1 if key in ("skk", "piq") else 0
    assert len(p.interiors) == n_voids
    for ring in p.interiors:
        assert not ring.is_ccw
    assert sec.provenance == "transcribed-with-convention"
    assert "production ended 2020" in sec.source_status
    assert sec.geometry is not None
    if key != "srp":
        assert abs(sum(x for x, _ in p.exterior.coords[:-1])) < 1e-6  # symmetric


def _check_skk_printed_dimensions(size):
    sec = SpanbetonSkkSection(size)
    d, p = sec.dimensions, sec.polygon
    h = d.depth
    assert p.bounds[3] == pytest.approx(h)
    assert _width_at(p, 100) == pytest.approx(d.width)  # solid bottom slab
    assert _width_at(p, h - 50) == pytest.approx(d.width - 60)  # 30 mm rebate each side
    # two webs of 155 at mid-depth
    assert _width_at(p, (d.bottom_slab + 75 + h - d.top_slab - 220) / 2) == pytest.approx(310)
    void = p.interiors[0]
    assert min(y for _, y in void.coords) == pytest.approx(d.bottom_slab)
    assert max(y for _, y in void.coords) == pytest.approx(h - d.top_slab)
    assert d.width == (1480 if h <= 1600 else 1180)


def _check_piq_printed_dimensions(size):
    sec = SpanbetonPiqSection(size)
    p, h = sec.polygon, sec.dimensions.depth
    assert p.bounds[3] == pytest.approx(h)
    assert p.bounds[2] - p.bounds[0] == pytest.approx(2790)
    assert _width_at(p, h - 10) == pytest.approx(1820)
    outer = Polygon(p.exterior)
    assert _width_at(outer, h - 400) == pytest.approx(1900)  # shoulder
    assert _width_at(p, 100) == pytest.approx(2790)
    # webs 183 each just above the bottom void chamfer level (outer faces 1750 apart)
    assert _width_at(p, 237) == pytest.approx(2 * 183, abs=6)


def _check_sjp_printed_dimensions(size):
    sec = SpanbetonSjpSection(size)
    d, p = sec.dimensions, sec.polygon
    assert p.bounds[3] == pytest.approx(d.h1)
    assert _width_at(p, 40) == pytest.approx(990)
    assert _width_at(p, d.h1 - 0.01) == pytest.approx(d.top_width, abs=0.1)
    # stem taper implied by the table: 260 at y=105 to b at h1-h2, 0.225 per side
    slope = (d.top_width - 260) / 2 / (d.h1 - d.h2 - 105)
    assert slope == pytest.approx(0.225, abs=0.002)


def _check_sjp_flex_printed_dimensions(size):
    sec = SpanbetonSjpFlexSection(size)
    d, p = sec.dimensions, sec.polygon
    assert p.bounds[3] == pytest.approx(d.h1)
    assert p.bounds[2] - p.bounds[0] == pytest.approx(1180)
    assert _width_at(p, 200) == pytest.approx(350)
    assert _width_at(p, d.h1 - 0.01) == pytest.approx(d.top_width, abs=0.1)
    # printed b follows 350 + 0.88 * (h1 - h2 - 286.4) to rounding (the modelled
    # stem stays vertical to y = 286 and meets b at h1 - h2 exactly)
    assert d.top_width == pytest.approx(350 + 0.88 * (d.h1 - d.h2 - 286.36), abs=1.0)


def test_sjp_flex_550_printed_width_pinned():
    """Printed b=556 breaks the 0.88 mm/mm taper of all other rows; 582 used."""
    r = SpanbetonSjpFlexSection("SJP-flex-550").published
    assert r["b_mm_printed"] == 556 and r["b_mm"] == 582
    others = [SpanbetonSjpFlexSection(s).published for s in SpanbetonSjpFlexSection.SIZES if s != "SJP-flex-550"]
    assert all(o["b_mm"] == o["b_mm_printed"] for o in others)


def _check_srp_printed_dimensions(size):
    sec = SpanbetonSrpSection(size)
    d, p = sec.dimensions, sec.polygon
    assert p.bounds[3] == pytest.approx(d.h1)
    assert p.bounds[2] - p.bounds[0] == pytest.approx(490)
    assert _width_at(p, 1) == pytest.approx(300)
    assert _width_at(p, d.h1 - 1) == pytest.approx(275 + 50 / 190, abs=0.01)
    r = sec.published
    assert d.h2 == r["h2_mm"] and d.h3 == r["h3_mm"]


def _check_zip_printed_dimensions(cls, size):
    sec = cls(size)
    d, p = sec.dimensions, sec.polygon
    assert p.bounds[3] == pytest.approx(d.total_depth)
    assert p.bounds[2] - p.bounds[0] == pytest.approx(d.width)
    assert _width_at(p, d.haunch_top + 1) == pytest.approx(d.stem)
    if d.series == "ZIP":
        assert d.h - d.h1 == 275
        assert _width_at(p, d.h + 1) == pytest.approx(230)
    elif d.series == "ZIPXL-1":
        assert _width_at(p, d.h - 1) == pytest.approx(500)
        assert _width_at(p, d.h + 1) == pytest.approx(430)
    else:
        assert d.h - d.h1 == 670
        assert _width_at(p, d.h - 60) == pytest.approx(1440)
        assert _width_at(p, d.h - 1) == pytest.approx(1370)


def _check_residuals_recorded_in_json(key, size):
    sec = CLASSES[key](size)
    got = _residuals(key, sec)
    rec = sec.residuals
    assert rec is not None
    for k in ("dA_rel", "dI_rel", "dSelfWeight_rel"):
        assert got[k] == pytest.approx(rec[k], abs=2e-5)
    assert got["dZb_mm"] == pytest.approx(rec["dZb_mm"], abs=0.01)


def test_residuals_recorded_in_json():
    run_checks((_check_residuals_recorded_in_json, P("key,size", ALL)))


def _zipkey(key, size):
    if key == "zipxl":
        return "zipxl1" if int(size.split("-")[1]) < 1800 else "zipxl2"
    return key


TOL = {  # dA_rel, dZb_mm, dI_rel, dSelfWeight_rel
    "skk": (0.020, 5.0, 0.040, 0.045),
    "piq": (None, None, 0.035, 0.016),
    "sjp": (0.012, 7.0, 0.012, 0.011),
    "sjp_flex": (0.022, 7.0, 0.040, 0.025),
    "srp": (0.006, 1.0, None, 0.006),
    "zip": (0.030, 3.0, 0.012, 0.005),
    "zipxl2": (0.042, 3.0, 0.050, 0.003),
    "zipxl1": (None, None, None, 0.004),
}
# Individual source/model discrepancies (value, abs tolerance).
PINNED = {
    ("SJP-300", "dI_rel"): (0.0517, 0.001),
    ("SJP-flex-300", "dI_rel"): (0.0799, 0.001),
    ("SJP-flex-350", "dI_rel"): (0.0587, 0.001),
    ("SJP-flex-400", "dI_rel"): (0.0439, 0.001),
    ("ZIP-700", "dZb_mm"): (21.8, 0.3),  # printed Zb 225 vs I/Wb = 246
    **{(f"SKK-{h}", "dZb_mm"): (v, 0.3) for h, v in
       ((700, 8.2), (800, 10.4), (900, 12.4), (1000, 14.3), (1100, 10.9), (1200, 12.5),
        (1300, 13.9), (1400, 15.2), (1500, 16.4))},
}
# Family-wide systematic discrepancies: (lo, hi) bands.
PINNED_BANDS = {
    ("piq", "dA_rel"): (-0.041, -0.036),
    ("piq", "dZb_mm"): (31.0, 39.0),
    ("srp", "dI_rel"): (-0.056, -0.049),
    ("zipxl1", "dA_rel"): (-0.073, -0.047),
    ("zipxl1", "dZb_mm"): (-35.5, -28.0),
    ("zipxl1", "dI_rel"): (-0.20, -0.10),
}


def _check_published_properties(key, size):
    fam = _zipkey(key, size)
    res = _residuals(key, CLASSES[key](size))
    for j, q in enumerate(("dA_rel", "dZb_mm", "dI_rel", "dSelfWeight_rel")):
        if (size, q) in PINNED:
            val, tol = PINNED[(size, q)]
            assert res[q] == pytest.approx(val, abs=tol)
            assert abs(res[q]) > TOL[fam][j]  # still a genuine outlier
        elif (fam, q) in PINNED_BANDS:
            lo, hi = PINNED_BANDS[(fam, q)]
            assert lo <= res[q] <= hi
        else:
            assert abs(res[q]) < TOL[fam][j], (size, q, res[q])


def _check_skk_1600_row_matches_outline():
    """The one SKK 1480 row whose Zb is not ~h/2 agrees with the drawn outline."""
    res = _residuals("skk", SpanbetonSkkSection("SKK-1600"))
    assert abs(res["dZb_mm"]) < 1.0 and abs(res["dA_rel"]) < 0.005


def test_zip700_printed_zb_is_inconsistent_with_its_wb():
    r = SpanbetonZipSection("ZIP-700").published
    assert r["Ib_1e6_mm4"] / r["Wb_1e6_mm3"] == pytest.approx(246, abs=1)
    assert r["Zb_mm"] == 225


def _check_json_provenance_block():
    for k in ("skk_piq", "sjp", "zip"):
        src = DATA["sources"][k]
        assert src["url"].startswith("https://web.archive.org/web/2016") and src["original_url"].startswith("http://www.spanbeton.nl/")
        assert len(src["sha256"]) == 64
        assert src["local_file"].startswith("sources/expansion/round2/nl/")


def _check_invalid_size(cls):
    with pytest.raises(ValueError):
        cls("SKK-650")


def test_nl_r2_spanbeton_catalogue_checks():
    run_checks(
        (_check_valid_ccw_and_metadata, P("key,size", ALL)),
        (_check_skk_printed_dimensions, P("size", SpanbetonSkkSection.SIZES)),
        (_check_piq_printed_dimensions, P("size", SpanbetonPiqSection.SIZES)),
        (_check_sjp_printed_dimensions, P("size", SpanbetonSjpSection.SIZES)),
        (_check_sjp_flex_printed_dimensions, P("size", SpanbetonSjpFlexSection.SIZES)),
        (_check_srp_printed_dimensions, P("size", SpanbetonSrpSection.SIZES)),
        (_check_zip_printed_dimensions, P("cls,size", [(SpanbetonZipSection, s) for s in SpanbetonZipSection.SIZES]
                         + [(SpanbetonZipxlSection, s) for s in SpanbetonZipxlSection.SIZES])),
        (_check_published_properties, P("key,size", ALL)),
        _check_skk_1600_row_matches_outline,
        _check_json_provenance_block,
        (_check_invalid_size, P("cls", list(CLASSES.values()))),
    )


def test_spanbeton_pinned_residuals_and_bands():
    """Individual PINNED outliers and family-wide PINNED_BANDS (PIQ, SRP, ZIPXL 1000-1700)."""
    qs = ("dA_rel", "dZb_mm", "dI_rel", "dSelfWeight_rel")
    cases = [(k, s) for k, s in ALL
             if any((s, q) in PINNED or (_zipkey(k, s), q) in PINNED_BANDS for q in qs)]
    run_checks((_check_published_properties, P("key,size", cases)))
