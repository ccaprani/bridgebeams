"""Prethor (Dossier Prethor 2020) beams: envelope transcription and P-table checks."""

import pytest
from shapely.geometry import LineString

from bridgebeams.es.r2_prethor import (
    PrethorVaaSection,
    PrethorVaSection,
    PrethorVcSection,
    PrethorViSection,
    PrethorVuSection,
    _load_data,
)

CLASSES = (PrethorViSection, PrethorVaSection, PrethorVuSection, PrethorVcSection, PrethorVaaSection)
ALL = [(cls, s) for cls in CLASSES for s in cls.SIZES]

# |area x 2.5 t/m3 / P - 1| tolerance (%). Scaled-only families reproduce the
# table within ~1.1 %; fitted families within 2 % (VCP 80/220-220 -1.9 %, VAA-B-180 +1.8 %).
TOL = {"VI": 1.0, "VI-I": 1.0, "VI-II": 1.0, "VA": 1.0, "VCG80/220": 1.5, "VCG100/200": 1.0,
       "VUP": 2.0, "VUG": 2.0, "VCP80/220": 2.0, "VCP100/200": 2.0, "VAA-B": 2.0}
# Pinned contradictions (see data/r2_prethor.json "pinned"): expected residual range (%).
PINNED = {"VUP-120": (4.5, 5.5), "VCP80/220-95": (-9.0, -8.0),
          **{f"VAA-A-{h}": (7.0, 9.1) for h in (180, 200, 220, 240, 260)}}


def width_at(poly, y):
    return poly.intersection(LineString([(-9000, y), (9000, y)])).length


def test_counts():
    assert [len(c.SIZES) for c in CLASSES] == [17, 9, 12, 29, 10]


@pytest.mark.parametrize("cls,size", ALL)
def test_valid_envelope(cls, size):
    sec = cls(size)
    p, d = sec.polygon, sec.dimensions
    assert p.is_valid and p.exterior.is_ccw and len(p.interiors) == 0
    assert p.bounds[1] == 0 and p.bounds[3] == pytest.approx(d.depth)
    # printed overall top width, a printed to 1 cm (b + H/2 = 377.5 -> "3.78");
    # VUG: 1:4 webs give 10 mm less than every printed a (pinned in the JSON notes)
    tol = 10.0 if sec.family == "VUG" else 5.0 + 1e-6
    assert p.bounds[2] - p.bounds[0] == pytest.approx(d.top_width, abs=tol)
    assert sec.provenance in ("estimate", "fitted-reconstruction")
    assert sec.source_status.startswith("producer catalogue")


@pytest.mark.parametrize("cls,size", ALL)
def test_bottom_width(cls, size):
    sec = cls(size)
    p, b = sec.polygon, sec.dimensions.bottom_width
    if cls is PrethorViSection:
        assert width_at(p, 1) == pytest.approx(b)
    elif cls is PrethorVaaSection:
        assert p.bounds[0] == -1500 and width_at(p, 1) == pytest.approx(b + 0.25, abs=0.01)
    else:
        # soffit (possibly chamfered) not wider than printed; outer 1:4 webs pass through b at y = 0
        assert width_at(p, 0.5) <= b + 0.5
        y = 100.0
        assert width_at(p, y) == pytest.approx(b + 2 * y / 4, abs=0.01)


@pytest.mark.parametrize("cls,size", ALL)
def test_mass_vs_published(cls, size):
    sec = cls(size)
    area_m2 = sec.polygon.area / 1e6
    res = 100 * (area_m2 * sec.density_t_m3 / sec.published["P_t_per_m"] - 1)
    assert res == pytest.approx(_load_data()["sizes"][size]["residual_pct_vs_P"], abs=0.01)
    if size in PINNED:
        lo, hi = PINNED[size]
        assert lo <= res <= hi
        assert "pinned" in _load_data()["sizes"][size]
    else:
        assert abs(res) <= TOL[sec.family], res


def test_flanges_fixed_web_grows():
    a = PrethorViSection("VI-60").polygon
    b = PrethorViSection("VI-140").polygon
    assert (b.area - a.area) == pytest.approx(160 * 800)  # 16 cm web x 80 cm extra depth
    assert width_at(b, 700) == pytest.approx(160)


def test_open_troughs_have_no_top_slab():
    for cls, size in ((PrethorVuSection, "VUG-160"), (PrethorVcSection, "VCG80/220-240"), (PrethorVaSection, "VA-260")):
        p = cls(size).polygon
        assert width_at(p, p.bounds[3] - 1) < 0.5 * (p.bounds[2] - p.bounds[0])


def test_vaa_asymmetric_and_fitted():
    a = PrethorVaaSection("VAA-A-240")
    b = PrethorVaaSection("VAA-B-240")
    assert a.polygon.bounds == pytest.approx((-1500, 0, 2100, 2400))
    assert b.provenance == "fitted-reconstruction" and a.provenance == "estimate"
    assert b.geometry is not None


def test_invalid():
    for cls, bad in ((PrethorViSection, "VI-160"), (PrethorVaSection, "VA-280"), (PrethorVuSection, "VUP-220"),
                     (PrethorVcSection, "VCP80/220-240"), (PrethorVaaSection, "VAA-180")):
        with pytest.raises(ValueError):
            cls(bad)
