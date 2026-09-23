"""WIKA Beton channel girders (fitted) and PC-I/PC-U/bulb-tee (estimates)."""
import pytest
from shapely.geometry import LineString

from bridgebeams._geometry import section_properties
from bridgebeams.id import (
    WikaBulbTeeSection,
    WikaChannelGirderSection,
    WikaPcIGirderSection,
    WikaPcUGirderSection,
)

from _aggregate import P, run_checks


def _width(p, y):
    return p.intersection(LineString([(-5000, y), (5000, y)])).length


# published: area cm2, inertia cm4 (brochure uses '.'/',' as thousands separator)
CG = {"CG60": (600, 4329, 1293103), "CG70": (700, 4806, 2023171),
      "CG80": (800, 5274, 2968087), "CG100": (1000, 6334, 5717699)}


def _check_channel_printed_dims_and_fit(size):
    d, a, i = CG[size]
    s = WikaChannelGirderSection(size)
    p = s.polygon
    assert p.is_valid and s.provenance == "fitted-reconstruction"
    assert p.bounds == pytest.approx((-600, 0, 600, d))
    assert _width(p, d) == pytest.approx(1170)            # 15 + 1170 + 15
    assert _width(p, d - 100) == pytest.approx(1200 - 2 * 35)  # fitted key recess
    assert _width(p, d - 250 - 1) < 1200 - 580             # two legs only below the slab
    props = section_properties(p)
    # Fitted undimensioned key/haunch/chamfers: common values, <=0.05% A, <=0.11% I.
    assert props["area"] == pytest.approx(100 * a, rel=0.0005)
    assert props["ixx"] == pytest.approx(1e4 * i, rel=0.0011)


def test_cg100_chain_discrepancy_pinned():
    # Printed 230+40+50+580+50+40+230 = 1220 != 1200; drawn void top 560 used.
    p = WikaChannelGirderSection("CG100").polygon
    assert _width(p, 1000 - 200 - 0.01) == pytest.approx(1200 - 560, abs=0.5)


PCI = {"H90": (900, 350, 650, 170, 2572, 2266607), "H125": (1250, 350, 650, 170, 3167, 5496255),
       "H160": (1600, 550, 650, 180, 4773, 14611104), "H170": (1700, 800, 700, 200, 6695, 23641085),
       "H210": (2100, 800, 700, 200, 7495, 41087033)}


def _check_pc_i_estimate(size):
    h, bt, bb, tw, a, i = PCI[size]
    s = WikaPcIGirderSection(size)
    p = s.polygon
    assert p.is_valid and s.provenance == "estimate"
    assert p.bounds == pytest.approx((-max(bt, bb) / 2, 0, max(bt, bb) / 2, h))
    assert _width(p, h / 2) == pytest.approx(tw)
    props = section_properties(p)
    # Two flange-depth factors solved exactly; 0.1 mm coordinate rounding only.
    assert props["area"] == pytest.approx(100 * a, rel=1e-4)
    assert props["ixx"] == pytest.approx(1e4 * i, rel=1e-4)


def _check_bulb_tee_estimate():
    s = WikaBulbTeeSection("H220")
    p = s.polygon
    assert p.is_valid and p.bounds == pytest.approx((-1200, 0, 1200, 2200))
    assert _width(p, 1200) == pytest.approx(250)
    props = section_properties(p)
    assert props["area"] == pytest.approx(12925e2, rel=1e-4)
    assert props["ixx"] == pytest.approx(90106159e4, rel=1e-4)


PCU = {"H120": (1200, 1720, 9178, 12633291), "H140": (1400, 1720, 10366, 19634469),
       "H165": (1650, 1900, 11878, 31358776), "H185": (1850, 1900, 13066, 43340406),
       "H210": (2100, 1900, 14678, 62328088), "H230": (2300, 2080, 15936, 80742448)}


def _check_pc_u_estimate(size):
    h, top, a, i = PCU[size]
    s = WikaPcUGirderSection(size)
    p = s.polygon
    assert p.is_valid and s.provenance == "estimate"
    assert p.bounds == pytest.approx((-top / 2, 0, top / 2, h), abs=0.1)
    assert _width(p, 150) > 800  # solid 300 mm bottom slab
    props = section_properties(p)
    # One common two-parameter fit for all six sizes: residuals up to 1.3% A, 0.8% I.
    assert props["area"] == pytest.approx(100 * a, rel=0.013)
    assert props["ixx"] == pytest.approx(1e4 * i, rel=0.008)
    stored = s.published["residuals"]
    assert props["area"] / (100 * a) - 1 == pytest.approx(stored["area_rel"], abs=2e-6)


def _check_invalid_size(cls):
    with pytest.raises(ValueError):
        cls("H999")


def test_id_wika_catalogue_checks():
    run_checks(
        (_check_channel_printed_dims_and_fit, P("size", list(CG))),
        (_check_pc_i_estimate, P("size", list(PCI))),
        _check_bulb_tee_estimate,
        (_check_pc_u_estimate, P("size", list(PCU))),
        (_check_invalid_size, P("cls", [WikaChannelGirderSection, WikaPcIGirderSection,
                                 WikaPcUGirderSection, WikaBulbTeeSection])),
    )
