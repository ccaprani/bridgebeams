"""VÁHOSTAV-SK-PREFA VPH-PTMN outlines against the catalogue section constants."""
import pytest
from shapely.geometry import LineString

from bridgebeams._geometry import section_properties
from bridgebeams.sk import VphGirderSection, VphSlabBeamSection


def width_at(poly, y):
    return poly.intersection(LineString([(-2000, y), (2000, y)])).length


def section(size):
    cls = VphSlabBeamSection if size.startswith("2016-PM") else VphGirderSection
    return cls(size)


ALL = VphSlabBeamSection.SIZES + VphGirderSection.SIZES

# Individually pinned source contradictions (computed - published); see
# src/bridgebeams/sk/data/vph_ptmn.json geometry_notes. Not rounding.
PINNED_AREA_PCT = {"2016-PM13-M": 0.481}
PINNED_2100 = {"area_pct": -0.129, "yt_mm": -30.17, "Iy_pct": -4.804}


def test_counts():
    assert len(VphSlabBeamSection.SIZES) == 6
    assert len(VphGirderSection.SIZES) == 6
    assert sum(len(section(s).designations) for s in ALL) == 20


@pytest.mark.parametrize("size", ALL)
def test_polygon_valid_and_geometry(size):
    s = section(size)
    p = s.polygon
    assert p.is_valid and p.exterior.is_ccw and not p.interiors
    assert s.geometry.geom.symmetric_difference(p).area < 1e-6
    assert s.provenance in ("transcribed", "transcribed-with-convention")
    assert "producer catalogue" in s.source_status
    minx, miny, maxx, maxy = p.bounds
    assert miny == pytest.approx(0) and maxy == pytest.approx(s.dimensions.depth)
    assert maxx == pytest.approx(-minx)


@pytest.mark.parametrize("size", ALL)
def test_published_properties(size):
    s = section(size)
    props = section_properties(s.polygon)
    pub = s.published
    area_pct = (props["area"] / 1e6 / pub["area_m2"] - 1) * 100
    dy = props["cy"] - pub["yt_from_soffit_m"] * 1000
    di = (props["ixx"] / 1e12 / pub["Iy_m4"] - 1) * 100
    if size == "2010-R2-2.1":
        # The drawing is closed and self-consistent; the table is not.
        assert area_pct == pytest.approx(PINNED_2100["area_pct"], abs=0.005)
        assert dy == pytest.approx(PINNED_2100["yt_mm"], abs=0.05)
        assert di == pytest.approx(PINNED_2100["Iy_pct"], abs=0.005)
        return
    if size.startswith("2016-PM"):
        # Areas printed to 3 s.f. (0.0005 m2 = 500 mm2); yt to 1 mm; I to 4 s.f.
        if size in PINNED_AREA_PCT:
            assert area_pct == pytest.approx(PINNED_AREA_PCT[size], abs=0.005)
        else:
            assert abs(props["area"] - pub["area_m2"] * 1e6) <= 500 + 1e-6
        assert abs(dy) <= 1.0
        # Systematic +0.27..+0.40 % inertia excess on every PM unit (K and M)
        # is unresolved; pin its sign and band rather than widen further.
        assert 0.25 <= di <= 0.40
    else:
        # 4-5 s.f. areas; the 2016 designs are 395 mm2 short (unresolved).
        assert abs(area_pct) <= 0.12
        assert abs(dy) <= 0.8
        assert abs(di) <= 0.55
    assert s.row["residuals"] == {"area_pct": pytest.approx(area_pct, abs=0.001),
                                  "yt_mm": pytest.approx(dy, abs=0.01),
                                  "Iy_pct": pytest.approx(di, abs=0.001)}


@pytest.mark.parametrize("size,bottom,web,top,rebate,chamfer", [
    ("2016-T", 820, 220, None, None, 15),
    ("2010-I-1.2", 800, 200, 800, 30, 15),
    ("2016-I", 820, 220, 820, 40, 15),
    ("2010-I-1.4", 800, 200, 800, 30, 15),
    ("2010-R2-1.9", 800, 200, 800, 40, 15),
    ("2010-R2-2.1", 800, 200, 1100, 40, 15),
])
def test_girder_widths_and_tangent_extents(size, bottom, web, top, rebate, chamfer):
    s = section(size)
    p, h = s.polygon, s.dimensions.depth
    assert width_at(p, 0) == pytest.approx(bottom - 2 * chamfer)
    assert width_at(p, 100) == pytest.approx(bottom)
    assert width_at(p, 140) == pytest.approx(bottom)          # lower fillet tangent
    assert width_at(p, 360) == pytest.approx(web)             # upper splay tangent
    assert width_at(p, 140 + 44) == pytest.approx(bottom - 2 * 26, abs=1.5)
    assert width_at(p, 360 - 44) == pytest.approx(web + 2 * 26, abs=1.5)
    assert width_at(p, h / 2) == pytest.approx(web)
    if top is None:
        assert width_at(p, 990) == pytest.approx(140)         # raised strip
        assert width_at(p, 970) == pytest.approx(220)
        return
    assert width_at(p, h - 10) == pytest.approx(top - 2 * rebate)
    assert width_at(p, h - 25) == pytest.approx(top)
    tangent = s.dimensions.top_web_tangent_depth
    assert width_at(p, h - tangent - 1) == pytest.approx(web)
    if size != "2010-R2-2.1":
        # Printed 33 edge (34 on 1.9 m) and 42 horizontal fillet extent.
        edge = 34 if size == "2010-R2-1.9" else 33
        assert width_at(p, h - edge + 0.5) == pytest.approx(top)
        # Splay is 1:6, so the 0.5 mm rounding of printed heights moves the
        # tangent point up to 3 mm horizontally on each side.
        assert width_at(p, h - edge - 49) == pytest.approx(top - 2 * 42, abs=6)
        assert width_at(p, h - edge - 49 - 36) == pytest.approx(web + 2 * 42, abs=6)
    else:
        # Sharp flange edge 20 + 55 below top, straight splay to R50 at the web.
        assert width_at(p, h - 74) == pytest.approx(top)
        assert width_at(p, h - 76) < top


@pytest.mark.parametrize("size,depth", [("2016-PM11-M", 400), ("2016-PM13-M", 500),
                                        ("2016-PM15-M", 575)])
def test_m_units(size, depth):
    p = section(size).polygon
    assert width_at(p, 30) == pytest.approx(820)
    assert width_at(p, 55) == pytest.approx(820)
    assert width_at(p, 275) == pytest.approx(220)
    assert width_at(p, 55 + 44) == pytest.approx(820 - 2 * 26, abs=1.5)
    assert width_at(p, 275 - 44) == pytest.approx(220 + 2 * 26, abs=1.5)
    assert width_at(p, depth - 1) == pytest.approx(220)


@pytest.mark.parametrize("size,depth", [("2016-PM11-K", 400), ("2016-PM13-K", 500),
                                        ("2016-PM15-K", 575)])
def test_k_units(size, depth):
    s = section(size)
    p = s.polygon
    assert p.bounds == pytest.approx((-390, 0, 390, depth))
    assert width_at(p, 30) == pytest.approx(780)
    assert width_at(p, 275) == pytest.approx(480)
    assert width_at(p, depth - 1) == pytest.approx(480)
    assert section_properties(p)["cx"] < -50  # block on the left


def test_invalid_sizes():
    with pytest.raises(ValueError):
        VphGirderSection("2010-R2-2.3")
    with pytest.raises(ValueError):
        VphSlabBeamSection("2016-PM17-K")
