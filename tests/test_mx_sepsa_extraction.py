"""SEPSA box / Type U, double tee and Nebraska profiles (catalogue pp5–9, 19)."""
import json
from importlib import resources

import pytest
from shapely.geometry import LineString

from bridgebeams._geometry import section_properties
from bridgebeams.mx import (
    SepsaBoxGirderSection,
    SepsaDoubleTeeSection,
    SepsaNebraskaSection,
)
from bridgebeams.mx._arcs import ring_properties


def _data(name):
    return json.loads(resources.files("bridgebeams.mx").joinpath(f"data/{name}").read_text())


def _area_cm2(p):
    return ring_properties([list(p.exterior.coords)] + [list(r.coords) for r in p.interiors])["area"] / 100


def _width(p, y):
    return p.intersection(LineString([(-5000, y), (5000, y)])).length


# ---------------------------------------------------------------- box girders
BOX = _data("sepsa_box_girders.json")
ROWS = [(f["family"], r) for f in BOX["families"] for r in f["published_areas"]]
# Source-level discrepancies (relative area residual bands), pinned explicitly.
PINNED_CLOSED = {
    "CA-135": (0.006, 0.021),   # residual grows as a shrinks: table area vs its own b column
    "B-400": (0.007, 0.009),    # closed +0.8% while Type U matches to 0.06%
}


@pytest.mark.parametrize("size", SepsaBoxGirderSection.SIZES)
def test_box_constructs(size):
    s = SepsaBoxGirderSection(size)
    p = s.polygon
    assert p.is_valid
    assert len(p.interiors) == (0 if size.endswith("-U") else 1)
    d = s.dimensions
    assert p.bounds == pytest.approx((-5 * d.wing_width_max, 0, 5 * d.wing_width_max, 10 * d.depth))
    assert s.provenance == "transcribed-with-convention"
    # fillet solution reproduces the printed straight-web height
    assert s.derived["upper_fillet_web_tangent_height_cm"] == pytest.approx(
        d.web_straight_height, abs=0.25)
    # R5 / R40 soffit arcs reproduce printed flat soffit and base widths
    fam = s.family_data
    assert 2 * s.derived["soffit_flat_half_width_cm"] == pytest.approx(fam["printed_soffit_flat_cm"], abs=0.2)
    assert 2 * s.derived["soffit_tangent_half_width_cm"] == pytest.approx(fam["printed_base_width_cm"], abs=0.2)


@pytest.mark.parametrize("family,row", ROWS)
def test_box_area_table(family, row):
    s = SepsaBoxGirderSection(family, a=10 * row["a_cm"])
    # tip thickness b from the fixed wing soffit line (CA-115 table copies CA-85's b column)
    assert s.wing_tip_thickness() == pytest.approx(row["b_cm"], abs=0.25)
    calc = _area_cm2(s.polygon)
    assert calc - row["area_closed_cm2"] == pytest.approx(row["residual_closed_cm2"], abs=0.1)
    rel = calc / row["area_closed_cm2"] - 1
    if family == "CA-180":
        # Table is a near-constant ~350-370 cm2 above the drawn geometry for
        # every width (4.3-5.3%); closed-table area is even below Type U's.
        assert -370 <= calc - row["area_closed_cm2"] <= -349
    else:
        lo, hi = PINNED_CLOSED.get(family, (-0.005, 0.005))
        assert lo <= rel <= hi
    if "area_type_u_cm2" in row:
        u = _area_cm2(SepsaBoxGirderSection(family + "-U", a=10 * row["a_cm"]).polygon)
        rel_u = u / row["area_type_u_cm2"] - 1
        if family == "CA-180" and row["a_cm"] == 190:
            # source repeats the a=200 value (7280 cm2) at a=190
            assert rel_u == pytest.approx(-0.0168, abs=0.001)
        else:
            assert abs(rel_u) <= 0.0051


def test_box_wing_limits_and_invalid():
    with pytest.raises(ValueError):
        SepsaBoxGirderSection("CA-85-U")
    with pytest.raises(ValueError):
        SepsaBoxGirderSection("CA-85", a=1300)
    with pytest.raises(ValueError):
        SepsaBoxGirderSection("CA-100")


def test_type_u_opening():
    p = SepsaBoxGirderSection("CA-150-U").polygon
    # top: two wings with the 60.8 + 2x7 cm opening between them
    assert _width(p, 1499) == pytest.approx(3100 - 748, abs=0.5)
    # 20 cm bottom slab solid across between the webs
    assert _width(p, 100) > 800


# ---------------------------------------------------------------- double tees
TT = _data("sepsa_double_tees.json")
TT_ROWS = [(v["variant"], r) for v in TT["variants"] for r in v["rows"]]
TT_PINNED = {("LIGERA", 75.0): -5.0, ("LIGERA", 60.0): -3.5}


@pytest.mark.parametrize("variant,row", TT_ROWS)
def test_double_tee_all_cells(variant, row):
    size = f"{variant}-{row['h_cm']:g}"
    v = next(x for x in TT["variants"] if x["variant"] == variant)
    stem = row["h_cm"] - 5 - v["haunch_depth_cm"]
    for a, area in row["area_cm2"].items():
        s = SepsaDoubleTeeSection(size, a=10 * float(a))
        p = s.polygon
        assert p.is_valid
        assert p.bounds == pytest.approx((-5 * float(a), 0, 5 * float(a), 10 * row["h_cm"]))
        diff = section_properties(p)["area"] / 100 - area
        if (variant, row["h_cm"]) in TT_PINNED:
            assert diff == pytest.approx(TT_PINNED[(variant, row["h_cm"])], abs=0.01)
        else:
            # b printed to 0.1 cm (two stems: 0.05 * stem height) + 0.5 cm2 table rounding
            assert abs(diff) <= 0.05 * stem + 0.5


def test_double_tee_invalid():
    with pytest.raises(ValueError):
        SepsaDoubleTeeSection("AMERICANA-85")
    with pytest.raises(ValueError):
        SepsaDoubleTeeSection("LIGERA-85", a=1800)
    assert SepsaDoubleTeeSection("PESADA-85").provenance == "transcribed"


# ---------------------------------------------------------------- Nebraska
@pytest.mark.parametrize("size", SepsaNebraskaSection.SIZES)
def test_nebraska(size):
    s = SepsaNebraskaSection(size)
    p = s.polygon
    assert p.is_valid and s.provenance == "estimate"
    d = s.dimensions
    w = 10 * (d.top_width / 2 + d.widen)
    assert p.bounds == pytest.approx((-w, 0, w, 10 * d.depth))
    assert _width(p, 10 * d.depth / 2) == pytest.approx(180 + 20 * d.widen)
    assert _width(p, 50) == pytest.approx(1000 + 20 * d.widen)
    # Estimated top-flange break/tip radius: consistent -0.16..-0.23% vs published m2
    rel = section_properties(p)["area"] / 1e6 / s.published_area_m2 - 1
    assert -0.0025 <= rel <= -0.0015


def test_nebraska_web20_adds_2cm_per_depth():
    for t in ("180", "210", "240-BASE-ESPECIAL"):
        a18 = section_properties(SepsaNebraskaSection(t + "-W18").polygon)["area"]
        a20 = section_properties(SepsaNebraskaSection(t + "-W20").polygon)["area"]
        depth = SepsaNebraskaSection(t + "-W18").dimensions.depth
        assert a20 - a18 == pytest.approx(20 * 10 * depth, rel=1e-9)
    with pytest.raises(ValueError):
        SepsaNebraskaSection("135-W20")
