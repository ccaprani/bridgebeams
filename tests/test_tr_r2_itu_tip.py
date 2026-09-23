"""İTÜ thesis TİP I/II/III x A/B/C beams vs published Tablo 3.1-3.6."""

import pytest
from shapely.geometry import LineString, Polygon, box
from shapely.ops import unary_union

from bridgebeams._geometry import section_properties
from bridgebeams.tr.r2_itu_tip import ItuTipBeamSection


def width_at(poly, y):
    return poly.intersection(LineString([(-5000, y), (5000, y)])).length


@pytest.mark.parametrize("size", ItuTipBeamSection.SIZES)
def test_valid_and_envelope(size):
    sec = ItuTipBeamSection(size)
    p, d = sec.polygon, sec.dimensions
    assert p.is_valid and p.exterior.is_ccw
    assert p.bounds == pytest.approx((-max(d.top_width, d.bottom_width) / 2, 0, max(d.top_width, d.bottom_width) / 2, d.depth))
    assert width_at(p, 1) == pytest.approx(d.bottom_width)
    assert width_at(p, d.depth - 1) == pytest.approx(d.top_width)
    assert width_at(p, d.depth / 2) == pytest.approx(200.0)
    assert d.web_height == pytest.approx(d.depth - 450.0)  # printed "H-45" (cm)
    assert sec.geometry is not None


@pytest.mark.parametrize("size", ItuTipBeamSection.SIZES)
def test_precast_properties_match_thesis(size):
    """Exact to the printed rounding (TİP III with the 13.0 cm splay convention)."""
    sec = ItuTipBeamSection(size)
    sp = section_properties(sec.polygon)
    pub = sec.published["precast"]
    assert sp["area"] == pytest.approx(pub["F_cm2"] * 100, abs=2.0)
    assert sp["cy"] == pytest.approx(pub["yalt_cm"] * 10, abs=0.06)
    assert sec.dimensions.depth - sp["cy"] == pytest.approx(pub["yust_cm"] * 10, abs=0.06)
    assert sp["ixx"] == pytest.approx(pub["Ix_cm4"] * 1e4, rel=2e-6)


@pytest.mark.parametrize("size", ItuTipBeamSection.SIZES)
def test_composite_properties_match_thesis(size):
    """Precast + 250 mm slab of the published transformed width b."""
    sec = ItuTipBeamSection(size)
    h, b = sec.dimensions.depth, sec.composite_effective_width
    comp = unary_union([sec.polygon, box(-b / 2, h, b / 2, h + 250)])
    assert isinstance(comp, Polygon)
    sp = section_properties(comp)
    pub = sec.published["composite"]
    assert sp["area"] == pytest.approx(pub["Fc_cm2"] * 100, abs=50)  # Fc printed to 1 cm2
    assert sp["cy"] == pytest.approx(pub["ycalt_cm"] * 10, abs=0.1)
    # b is printed rounded (63.69 / 80.83 cm; exact 78*29440/36057 = 63.6862):
    # Icx then differs by <= 2.5e-5 relative
    assert sp["ixx"] == pytest.approx(pub["Icx_cm4"] * 1e4, rel=5e-5)
    assert h - sp["cy"] == pytest.approx(pub["ycust_cm"] * 10, abs=0.1)  # to precast top


def test_provenance():
    assert ItuTipBeamSection("TIP-I-B").provenance == "transcribed"
    assert ItuTipBeamSection("TIP-II-C").provenance == "transcribed"
    assert ItuTipBeamSection("TIP-III-A").provenance == "transcribed-with-convention"


def test_tip_iii_printed_splay_would_miss_published_area():
    """Pinned discrepancy: the printed 13.5 cm top splay gives +13.75 cm2."""
    sec = ItuTipBeamSection("TIP-III-A")
    a = section_properties(sec.polygon)["area"]
    assert a + 1375.0 == pytest.approx(3615.0 * 100)


def test_invalid():
    with pytest.raises(ValueError):
        ItuTipBeamSection("TIP-IV-A")
