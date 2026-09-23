"""620 Châu Thới (Vietnam) producer girders."""

import pytest
from shapely.geometry import LineString

from bridgebeams._geometry import section_properties
from bridgebeams.vn.c620_girders import Vn620GirderSection


@pytest.mark.parametrize("size", Vn620GirderSection.SIZES)
def test_valid_and_labelled(size):
    sec = Vn620GirderSection(size)
    p = sec.polygon
    assert p.is_valid and p.exterior.is_ccw
    assert p.bounds[1] == 0 and p.bounds[3] == sec.dimensions.depth
    assert abs(p.bounds[0] + p.bounds[2]) < 1e-9
    assert sec.provenance in {"transcribed", "transcribed-with-convention"}
    assert "620" in sec.source_status
    assert sec.geometry is not None


def _i_area(top, tf, th, web, wh, bs, be, bot, ch):
    return (top * tf + (top + web) / 2 * th + web * wh + (web + bot) / 2 * bs + bot * be - ch * ch)


def test_i33_exact():
    s = Vn620GirderSection("I33")
    assert 160 + 120 + 770 + 170 + 180 == 1400
    assert s.polygon.area == pytest.approx(_i_area(500, 160, 120, 160, 770, 170, 180, 610, 25))
    assert s.polygon.bounds == (-305, 0, 305, 1400)


def test_i2454_exact():
    s = Vn620GirderSection("I24.54")
    assert 178 + 114 + 483 + 190 + 178 == 1143 and 116 * 2 + 178 == 410 and 190 * 2 + 178 == 558
    assert s.polygon.area == pytest.approx(_i_area(410, 178, 114, 178, 483, 190, 178, 558, 25))


def test_i186_exact():
    s = Vn620GirderSection("I18.6")
    assert 50 + 85 + 75 + 220 + 100 + 145 + 25 == 700
    expected = (390 * 50 + 430 * 85 + (430 + 160) / 2 * 75 + 160 * 220 + (160 + 560) / 2 * 100
                + 560 * 170 - 25 * 25)
    assert s.polygon.area == pytest.approx(expected)


def test_t186_taper_and_block():
    s = Vn620GirderSection("T18.6")
    p = s.polygon
    # soffit 200 wide, block 400 wide from 637 to 920, top 340
    assert p.bounds == pytest.approx((-200, 0, 200, 950))
    web_at_300 = p.intersection(LineString([(-300, 300), (300, 300)])).length
    assert web_at_300 == pytest.approx(200 + 2 * 300 / 12)  # 1:12 taper per face
    # the R130 fillet adds material beyond the straight taper: area bounds
    straight = (200 + 200 + 2 * 637 / 12) / 2 * 637 + 400 * 283 + 340 * 30
    assert straight < p.area < straight + 2 * 47 * 130


def test_inverted_t_bounds_and_area():
    s = Vn620GirderSection("TN20")
    p = s.polygon
    assert p.bounds == pytest.approx((-490, 0, 490, 750))
    # polygon without fillet: 980x100 - chamfers + sloped flange to web at 170 + web + haunch + flange + top
    base = 980 * 100 - 400 + (980 + 160) / 2 * 70 + 160 * (490 - 170) + (160 + 440) / 2 * 70 + 440 * 160 + 360 * 30
    assert base < p.area < base + 2 * 70 * 70 * (1 - 3.14159 / 4) * 1.3
    props = section_properties(p)
    assert 250 < props["cy"] < 375


def test_invalid_size():
    with pytest.raises(ValueError):
        Vn620GirderSection("I40")
