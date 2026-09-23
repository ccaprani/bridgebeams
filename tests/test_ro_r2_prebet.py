"""Prebet Aiud viaduct girders: printed chains, fillet constructions, identities.

No area/mass/inertia is published, so validation is analytic: overall
depths, width chains and vertical chains close exactly; fillet tangent
residuals against the printed chain splits are pinned at their recorded
values; recorded areas are regression-checked.
"""

import json
from importlib import resources

import pytest
from shapely.geometry import LineString

from bridgebeams._geometry import section_properties
from bridgebeams.ro.asa import AsaGrindaPodSection
from bridgebeams.ro.r2_prebet import PrebetGirderSection

DATA = json.loads(resources.files("bridgebeams.ro").joinpath("data/r2_prebet.json").read_text(encoding="utf-8"))

# depth, top width, max lower width (mm)
EXPECTED = {
    "INVT42-EC": (420, 207.0, 620), "INVT52-EC": (520, 220, 620),
    "INVT42-TIP": (420, 220, 600), "INVT52-TIP": (520, 220, 600),
    "I72-TIP": (720, 1020, 900), "I80-TIP": (800, 1020, 900),
    "T93-TIP": (930, 1200, 470), "T95-EC": (950, 1200, 500),
    "T103-TIP": (1030, 1200, 520), "T105-EC": (1050, 1200, 500),
    "T140": (1400, 1200, 800), "T160": (1600, 1200, 800), "T180": (1800, 1200, 800), "T200": (2000, 1200, 800),
    "I130": (1300, 520, 840), "I150": (1500, 520, 840), "I160": (1600, 520, 840), "I180": (1800, 520, 840),
    "TS160-TIP": (1600, 1200, 550), "TS184-EC": (1840, 1240, 640), "TS210-EC": (2100, 1220, 720),
}


def width_at(poly, y):
    return poly.intersection(LineString([(-5000, y), (5000, y)])).length


def test_sizes_cover_json():
    assert set(PrebetGirderSection.SIZES) == set(DATA["sizes"]) == set(EXPECTED)
    assert len(PrebetGirderSection.SIZES) == 21


@pytest.mark.parametrize("size", PrebetGirderSection.SIZES)
def test_outline(size):
    sec = PrebetGirderSection(size)
    poly = sec.polygon
    assert poly.is_valid and poly.exterior.is_ccw
    depth, top, bottom = EXPECTED[size]
    minx, miny, maxx, maxy = poly.bounds
    assert (miny, maxy) == pytest.approx((0.0, depth))
    assert sec.dimensions.top_width == pytest.approx(top, abs=0.5)
    assert sec.dimensions.bottom_width == pytest.approx(bottom)
    assert section_properties(poly)["cx"] == pytest.approx(0.0, abs=1e-6)
    assert sec.provenance in ("transcribed", "transcribed-with-convention")
    assert sec.source_status.startswith("producer web page")
    assert sec.geometry is not None


@pytest.mark.parametrize("size", PrebetGirderSection.SIZES)
def test_recorded_area_and_image(size):
    row = DATA["sizes"][size]
    props = section_properties(PrebetGirderSection(size).polygon)
    assert props["area"] == pytest.approx(row["model_properties_mm"]["area_mm2"], abs=1)
    img = DATA["images"][row["image"]]
    assert row["image_url"] == img["url"].replace(" ", "")
    assert img["url"].startswith("https://www.prebet.ro/wp-content/uploads/2016/05/")
    assert len(img["sha256"]) == 64


@pytest.mark.parametrize("size", PrebetGirderSection.SIZES)
def test_width_chains_sum(size):
    pr = DATA["sizes"][size]["printed_cm"]
    if "top_chain" in pr and "top_overall" in pr:
        assert sum(pr["top_chain"]) == pytest.approx(pr["top_overall"])
    if "bottom_chain" in pr and "bottom_overall" in pr:
        assert sum(pr["bottom_chain"]) == pytest.approx(pr["bottom_overall"])


@pytest.mark.parametrize("size", [s for s in PrebetGirderSection.SIZES
                                  if DATA["sizes"][s]["kind"] == "polyline"])
def test_polyline_chain_closes_to_depth(size):
    row = DATA["sizes"][size]
    chain = row["printed_cm"]["vertical_chain_from_soffit"]
    chain = [float(str(c).replace("max ", "")) for c in chain]
    assert sum(chain) == pytest.approx(row["depth_cm"])
    assert row["residuals_model_vs_printed"]["web_straight_cm"]["model"] == pytest.approx(chain[3] if size.startswith("TS") else chain[2])
    # printed plan widths at soffit, web and top edge
    p = PrebetGirderSection(size).polygon
    par = row["model_parameters_cm"]
    assert width_at(p, 1.0) == pytest.approx(par["bottom_width"] * 10)
    assert width_at(p, row["depth_cm"] * 5) == pytest.approx(par["web_width"] * 10)
    assert width_at(p, row["depth_cm"] * 10 - 1) == pytest.approx(par["top_width"] * 10)
    assert row["provenance"] == "transcribed"


@pytest.mark.parametrize("size,chain", [
    ("INVT52-EC", [15, 6, 8, 13, 10]), ("INVT52-TIP", [10, 7, 20, 5, 10]),
    ("I72-TIP", [11, 8.2, 4.8, 27, 4.8, 8.2, 8]), ("I80-TIP", [11, 8.2, 4.8, 35, 4.8, 8.2, 8]),
    ("T93-TIP", [12, 6.1, 15.4, 39.5, 10, 2, 8]), ("T95-EC", [12, 6.1, 15.4, 39.5, 10, 2, 10]),
    ("T105-EC", [12, 6, 15.5, 49.5, 10, 2, 10]),
    # T103-TIP: labels as read sum to 102.4; web label taken as 47.9 (see JSON)
    ("T103-TIP", [12, 6.8, 16.3, 47.9, 10, 2, 8]),
])
def test_filleted_chains_close(size, chain):
    assert sum(chain) == pytest.approx(DATA["sizes"][size]["depth_cm"])


def test_t103_as_read_misclosure_is_pinned():
    read = [12, 6.8, 16.3, 47.3, 10, 2, 8]
    assert sum(read) == pytest.approx(102.4)


def test_t95_ec_bottom_width_discrepancy_pinned():
    pr = DATA["sizes"]["T95-EC"]["printed_cm"]
    assert sum(pr["web_chain"]) == 51 and sum(pr["bottom_chain"]) == 50
    assert DATA["sizes"]["T95-EC"]["model_parameters_cm"]["edge_width"] == 50


# fillet tangent residuals vs printed chain splits (cm): pinned
PINNED = {
    ("INVT52-EC", "slope_tangent_level_cm"): 0.05,
    ("I72-TIP", "lower_slope_tangent_level_cm"): 0.01,
    ("I80-TIP", "upper_slope_tangent_level_cm"): 0.07,
    ("T93-TIP", "lower_slope_tangent_level_cm"): 0.75,
    ("T95-EC", "lower_slope_tangent_level_cm"): 0.75,
    ("T105-EC", "lower_slope_tangent_level_cm"): 0.65,
    ("T103-TIP", "lower_slope_tangent_level_cm"): 0.02,
    ("T93-TIP", "upper_web_tangent_level_cm"): 0.02,
    ("T95-EC", "upper_horizontal_extent_cm"): 0.02,
    ("T93-TIP", "upper_horizontal_extent_cm"): 0.5,
}


@pytest.mark.parametrize("key,tol", PINNED.items())
def test_fillet_residuals(key, tol):
    size, name = key
    r = DATA["sizes"][size]["residuals_model_vs_printed"][name]
    assert abs(r["model"] - r["printed"]) <= tol


def test_invt_ec_42_is_52_cut_at_dashed_line():
    a, b = PrebetGirderSection("INVT42-EC").polygon, PrebetGirderSection("INVT52-EC").polygon
    for y in (5, 100, 200, 300, 410):
        assert width_at(a, y) == pytest.approx(width_at(b, y))
    assert width_at(a, 419.9) == pytest.approx(207.0, abs=0.5)


@pytest.mark.parametrize("size", ["42", "52"])
def test_invt_tip_identical_to_asa_above_chamfer(size):
    pre = PrebetGirderSection(f"INVT{size}-TIP").polygon
    asa = AsaGrindaPodSection(size).polygon
    for y in range(100, int(size) * 10, 10):  # identical above the flange edge
        assert width_at(pre, y) == pytest.approx(width_at(asa, y), abs=0.01)
    # below: ASA prints a 2.5 cm chamfer + 1 cm edge draft; Prebet draws a vertical 60 cm edge
    assert width_at(pre, 30) == pytest.approx(600) and width_at(asa, 30) < 590
    assert DATA["sizes"][f"INVT{size}-TIP"]["identity"]["size"] == size


@pytest.mark.parametrize("size", ["72", "80"])
def test_i_tip_matches_asa_above_lower_flange(size):
    pre = PrebetGirderSection(f"I{size}-TIP").polygon
    asa = AsaGrindaPodSection(size).polygon
    depth = int(size) * 10
    for y in range(240, depth, 10):
        # same printed plan; ASA builds its upper R5 fillet at its printed 4 cm knee,
        # Prebet (no knee printed) tangent at the chain level: widths differ <= 8.3 mm
        assert width_at(pre, y) == pytest.approx(width_at(asa, y), abs=8.5)
    assert width_at(pre, 50) == pytest.approx(900)
    assert width_at(asa, 109) == pytest.approx(920, abs=1)  # ASA section prints 92 at the flange edge


def test_t93_is_iptana_95_with_8cm_flange_edge():
    pre = PrebetGirderSection("T93-TIP")
    asa = AsaGrindaPodSection("95")
    assert pre.dimensions.depth == 930 and asa.dimensions.depth == 950
    for y in (5, 150, 500):
        assert width_at(pre.polygon, y) == pytest.approx(width_at(asa.polygon, y), abs=15)
    assert width_at(pre.polygon, 929) == width_at(asa.polygon, 949) == pytest.approx(1200)


def test_areas_increase_within_families():
    for fam in (("T140", "T160", "T180", "T200"), ("I130", "I150", "I160", "I180"),
                ("TS160-TIP", "TS184-EC", "TS210-EC"), ("I72-TIP", "I80-TIP")):
        a = [section_properties(PrebetGirderSection(s).polygon)["area"] for s in fam]
        assert a == sorted(a)


def test_invalid():
    with pytest.raises(ValueError):
        PrebetGirderSection("T180-EC")
