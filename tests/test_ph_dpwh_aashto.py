"""Philippine Standard AASHTO I-girders (owner-supplied DPWH-practice slide)."""

import math

import pytest

from bridgebeams._geometry import section_properties
from bridgebeams.ph import PhDpwhAashtoSection
from bridgebeams.us import AashtoIBeamSection

from _aggregate import P, run_checks

# size -> (depth, top width, web, bottom width) as printed on the slide
PRINTED = {
    "I": (711, 305, 152, 406),
    "II": (914, 305, 152, 457),
    "III": (1143, 406, 178, 559),
    "IV": (1372, 508, 203, 660),
    "V-as-drawn": (1829, 1067, 203, 660),
}
US_EQUIVALENT = {"I": "I", "II": "II", "III": "III", "IV": "IV"}


def _max_vertex_diff(a, b):
    ua = {(round(x, 3), round(y, 3)) for x, y in a.exterior.coords if x > 0}
    ub = [(x, y) for x, y in b.exterior.coords if x > 0]
    return max(min(math.dist(p, q) for q in ub) for p in ua)


def _check_geometry(size):
    s = PhDpwhAashtoSection(size)
    p = s.polygon
    depth, top, web, bottom = PRINTED[size]
    assert p.is_valid and p.exterior.is_ccw
    assert p.bounds == (-max(top, bottom) / 2, 0, max(top, bottom) / 2, depth)
    xs_mid = sorted({abs(x) for x, y in p.exterior.coords if 0 < y < depth})
    assert web / 2 in xs_mid
    assert s.geometry is not None
    assert s.source_status.startswith("secondary presentation slide")


def _check_provenance(size):
    s = PhDpwhAashtoSection(size)
    closes = s.published["chain_sum"] == s.published["depth"]
    assert s.provenance == ("transcribed" if closes else "transcribed-with-convention")
    assert abs(s.published["chain_sum"] - s.published["depth"]) <= 1


def _check_matches_us_within_rounding(size):
    ph = PhDpwhAashtoSection(size).polygon
    us = AashtoIBeamSection(US_EQUIVALENT[size]).polygon
    # callouts rounded to <=0.5 mm each, plus the 1 mm chain residual absorbed by the web
    assert _max_vertex_diff(ph, us) <= 1.1
    assert ph.area == pytest.approx(us.area, rel=0.0025)
    assert section_properties(ph)["ixx"] == pytest.approx(section_properties(us)["ixx"], rel=0.0025)


def _check_invalid_size():
    with pytest.raises(ValueError):
        PhDpwhAashtoSection("V")
    with pytest.raises(ValueError):
        PhDpwhAashtoSection("VI")


def test_ph_dpwh_aashto_catalogue_checks():
    run_checks(
        (_check_geometry, P("size", PhDpwhAashtoSection.SIZES)),
        (_check_provenance, P("size", PhDpwhAashtoSection.SIZES)),
        (_check_matches_us_within_rounding, P("size", list(US_EQUIVALENT))),
        _check_invalid_size,
    )


def test_ph_type_v_as_drawn_is_aashto_type_vi_not_v():
    """Slide 'TYPE V' is 1829 mm deep = AASHTO Type VI (72 in), not Type V (63 in)."""
    ph = PhDpwhAashtoSection("V-as-drawn")
    assert ph.label_on_slide == "TYPE V"
    assert ph.polygon.bounds[3] == 1829
    vi = AashtoIBeamSection("VI").polygon
    v = AashtoIBeamSection("V").polygon
    assert vi.bounds[3] == pytest.approx(1828.8)
    assert v.bounds[3] == pytest.approx(1600.2)
    # every vertex above the bottom flange matches Type VI within soft-conversion rounding
    upper = [(x, y) for x, y in ph.polygon.exterior.coords if y > 203]
    vi_pts = list(vi.exterior.coords)
    assert max(min(math.dist(p, q) for q in vi_pts) for p in upper) <= 0.6  # soft-conversion rounding
    # ... and not Type V
    assert ph.polygon.hausdorff_distance(v) > 200


def test_ph_type_v_as_drawn_bottom_flange_pinned():
    """Pinned discrepancy: slide prints 660 mm bottom flange; PCI Type VI has 28 in = 711.2 mm."""
    ph = PhDpwhAashtoSection("V-as-drawn").polygon
    vi = AashtoIBeamSection("VI").polygon
    soffit_ph = max(x for x, y in ph.exterior.coords if y == 0) * 2
    soffit_vi = max(x for x, y in vi.exterior.coords if y == 0) * 2
    assert soffit_ph == 660
    assert soffit_vi == pytest.approx(711.2)
    assert ph.hausdorff_distance(vi) == pytest.approx(25.6, abs=0.05)
    assert ph.area / vi.area == pytest.approx(0.97545, abs=1e-4)


def test_ph_chain_conventions_pinned():
    """Types II–IV: printed chains miss the overall depth by 1 mm; web absorbs it."""
    expected = {"II": (913, 382), "III": (1144, 482), "IV": (1371, 585)}
    for size, (chain_sum, web_used) in expected.items():
        s = PhDpwhAashtoSection(size)
        assert sum(s.published["chain_as_drawn"].values()) == chain_sum
        assert s.dimensions.web_height == web_used
