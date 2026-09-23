"""Ukrainian bridge I-beams (NIDI 2022 recommendations, 3 Бетони, Kovalska/Oberbeton)."""

import pytest
from shapely.geometry import LineString

from bridgebeams._geometry import section_properties
from bridgebeams.ua import ThreeBetBeamSection, UaB40BeamSection, UaBmBeamSection

ALL = [(C, s) for C in (UaB40BeamSection, ThreeBetBeamSection, UaBmBeamSection) for s in C.SIZES]


def width_at(poly, y):
    return poly.intersection(LineString([(-5000, y), (5000, y)])).length


@pytest.mark.parametrize("cls,size", ALL)
def test_valid_envelope_and_metadata(cls, size):
    sec = cls(size)
    p, d = sec.polygon, sec.dimensions
    assert p.is_valid and p.exterior.is_ccw
    assert p.bounds[1] == 0 and p.bounds[3] == pytest.approx(d.depth)
    assert p.bounds[2] - p.bounds[0] == pytest.approx(max(d.top_width, d.bottom_width))
    assert sec.provenance in ("transcribed", "transcribed-with-convention")
    assert sec.source_status
    assert sec.geometry is not None


# ---- Б L.H.40 -------------------------------------------------------------

B40_DEPTH = {"B1200.100.40": 1000, "B1500.100.40": 1000, "B1800.110.40": 1100,
             "B2100.110.40": 1100, "B2400.110.40": 1100, "B3300.120.40": 1200}


@pytest.mark.parametrize("size", UaB40BeamSection.SIZES)
def test_b40_printed_widths(size):
    sec = UaB40BeamSection(size)
    p, h = sec.polygon, sec.dimensions.depth
    assert h == B40_DEPTH[size]
    assert width_at(p, h - 50) == pytest.approx(400)
    assert width_at(p, h / 2) == pytest.approx(180)
    assert width_at(p, 40) == pytest.approx(500)
    assert width_at(p, 0.001) == pytest.approx(460, abs=0.1)  # 20 x 20 chamfers


@pytest.mark.parametrize("size", UaB40BeamSection.SIZES)
def test_b40_section_chain_tangent_points(size):
    """Fillet tangent points reproduce the printed chain 131/31/63/39/512/31/106/31/f/20."""
    sec = UaB40BeamSection(size)
    h = sec.dimensions.depth
    f = sec.published["bottom_flange_vertical"]
    chain = [131, 31, 63, 39, 512, 31, 106, 31, f, 20]
    assert sum(chain) == h
    levels, y = [], h
    for c in chain[:-1]:
        y -= c
        levels.append(y)
    # right-side outline points: x of the polygon at each chain level must be at a
    # tangent point, i.e. the straight-segment/arc boundaries. Check via widths:
    p = sec.polygon
    # flange/web straight parts at the chain boundaries have the straight-part widths
    assert width_at(p, levels[0] + 0.3) == pytest.approx(400, abs=0.5)     # top flange ends at 131
    assert width_at(p, levels[3] - 0.3) == pytest.approx(180, abs=0.5)     # web starts at 264
    assert width_at(p, levels[4] + 0.3) == pytest.approx(180, abs=0.5)     # web ends 512 lower
    assert width_at(p, levels[7] - 0.3) == pytest.approx(500, abs=0.5)     # bottom flange from here down
    # and just beyond them the outline has left the straight part
    assert width_at(p, levels[0] - 2) < 399.9
    assert width_at(p, levels[3] + 2) > 180.05
    assert width_at(p, levels[4] - 2) > 180.05
    assert width_at(p, levels[7] + 2) < 499.9


def test_b40_same_depth_same_section():
    a = section_properties(UaB40BeamSection("B1800.110.40").polygon)
    b = section_properties(UaB40BeamSection("B2400.110.40").polygon)
    assert a["area"] == pytest.approx(b["area"])


# ---- 3Bet-90 / 3Bet-120 -----------------------------------------------------

@pytest.mark.parametrize("size", ThreeBetBeamSection.SIZES)
def test_3bet_volume(size):
    """Area vs producer volume / nominal length (no end blocks: V/L is constant per type).

    3Bet-90 (fully chained drawing) agrees within 0.25 %. 3Bet-120 is pinned
    at +1.3..1.45 %: its web taper stations are scaled, not dimensioned
    (see data/ua_beams.json geometry_notes).
    """
    sec = ThreeBetBeamSection(size)
    area = section_properties(sec.polygon)["area"]
    vl = sec.published_volume / sec.length * 1e9
    resid = area / vl - 1
    if sec.type == "3Bet-90":
        assert abs(resid) < 0.0025
        assert sec.provenance == "transcribed"
    else:
        assert 0.0130 < resid < 0.0145
        assert sec.provenance == "transcribed-with-convention"


def test_3bet90_printed_widths():
    p = ThreeBetBeamSection("3Bet-90-18").polygon
    assert width_at(p, 900) == pytest.approx(420)
    assert width_at(p, 860) == pytest.approx(440)
    assert width_at(p, 845) == pytest.approx(560)
    assert width_at(p, 730) == pytest.approx(540)
    assert width_at(p, 640) == pytest.approx(200)
    assert width_at(p, 450) == pytest.approx(160)
    assert width_at(p, 260) == pytest.approx(200)
    assert width_at(p, 170) == pytest.approx(520)
    assert width_at(p, 10) == pytest.approx(500)
    assert width_at(p, 0) == pytest.approx(480)


def test_3bet120_printed_widths():
    p = ThreeBetBeamSection("3Bet-120-33").polygon
    assert width_at(p, 1200) == pytest.approx(610)
    assert width_at(p, 1179.9) == pytest.approx(680, abs=3)  # on the R10 arc near its tangent point
    assert width_at(p, 1165) == pytest.approx(700)
    assert width_at(p, 1150) == pytest.approx(700)
    assert width_at(p, 730) == pytest.approx(150)
    assert width_at(p, 450) == pytest.approx(180)
    assert width_at(p, 25) == pytest.approx(580)


# ---- БМ-24 / БМ-33 ----------------------------------------------------------

@pytest.mark.parametrize("size,h", [("BM-24", 1100), ("BM-33", 1500)])
def test_bm_printed(size, h):
    p = UaBmBeamSection(size).polygon
    assert p.bounds[3] == h
    assert width_at(p, h - 20) == pytest.approx(480)
    assert width_at(p, h - 50) == pytest.approx(600)
    assert width_at(p, h / 2) == pytest.approx(160)
    assert width_at(p, 100) == pytest.approx(480)
    assert width_at(p, 0) == pytest.approx(440)
    # 1:1 haunches: top 220 high over 220 wide, bottom 160 over 160
    assert width_at(p, h - 210) == pytest.approx(600 - 2 * 110)
    assert width_at(p, 233) == pytest.approx(480 - 2 * 80)


def test_bm_web_difference_is_400():
    a24 = section_properties(UaBmBeamSection("BM-24").polygon)["area"]
    a33 = section_properties(UaBmBeamSection("BM-33").polygon)["area"]
    assert a33 - a24 == pytest.approx(400 * 160)


@pytest.mark.parametrize("cls,bad", [(UaB40BeamSection, "B2700.110.40"),
                                     (ThreeBetBeamSection, "3Bet-90-33"),
                                     (UaBmBeamSection, "BM-18")])
def test_invalid(cls, bad):
    with pytest.raises(ValueError):
        cls(bad)
