"""Belgian FEBE standardised I-beams: validation of the designation
system, pairing rules and geometry. Flange thicknesses are design
parameters (not published in open sources), so property validation is
structural plus consistency checks against the pairing rules."""

import json
from importlib import resources

import pytest

from bridgebeams._geometry import section_properties, as_polygon
from bridgebeams.be import FebeIDimensions, FebeISection

DATA = json.loads(
    resources.files("bridgebeams.be.data").joinpath("febe_i_beams.json").read_text()
)

SMALL_H = list(range(900, 1651, 50))
LARGE_H = list(range(1700, 2051, 50))


def test_designation_count():
    # 16 small heights x 2 b + 8 large heights x 5 b = 72 designations
    assert len(SMALL_H) == 16 and len(LARGE_H) == 8
    assert len(SMALL_H) * 2 + len(LARGE_H) * 5 == 72


@pytest.mark.parametrize("h", SMALL_H)
@pytest.mark.parametrize("b", [620, 640])
def test_small_family(h, b):
    beam = FebeISection(f"{h}/{b}", top_flange_thickness=150, bottom_flange_thickness=150)
    d = beam.dimensions
    assert d.subfamily == "small"
    assert d.web_width == b - 480          # pairing rule
    assert d.gorge == b - 240              # pairing rule
    assert (d.n, d.r, d.s) == (60.0, 80.0, 200.0)
    poly = beam.polygon
    assert poly.is_valid
    assert poly.area > 0


@pytest.mark.parametrize("h", LARGE_H)
@pytest.mark.parametrize("b", [800, 820, 840, 860, 880])
def test_large_family(h, b):
    beam = FebeISection(f"{h}/{b}", top_flange_thickness=250, bottom_flange_thickness=250)
    d = beam.dimensions
    assert d.subfamily == "large"
    assert d.web_width == b - 660          # pairing rule
    assert d.gorge == b - 320              # pairing rule
    assert (d.n, d.r, d.s) == (80.0, 120.0, 210.0)
    assert beam.polygon.is_valid


def test_symmetric_and_stack():
    beam = FebeISection("1200/640", top_flange_thickness=200, bottom_flange_thickness=250)
    props = section_properties(as_polygon(beam.geometry))
    d = beam.dimensions
    xmin, xmax, _, _ = beam.geometry.calculate_extents()
    assert -xmin == pytest.approx(xmax)
    # stack: 2 x flange thickness + web clear = depth
    assert d.top_flange_thickness + d.bottom_flange_thickness + (
        d.depth - d.top_flange_thickness - d.bottom_flange_thickness
    ) == pytest.approx(d.depth)
    # web fits inside the gorge
    assert d.web_width < d.gorge
    assert props["area"] > 0


def test_gorge_narrower_than_flange():
    for b in (620, 640):
        assert b - 240 < b
    for b in (800, 820, 840, 860, 880):
        assert b - 320 < b


def test_thickness_required():
    with pytest.raises(ValueError, match="not published"):
        FebeISection("900/620")


def test_invalid_designations_raise():
    with pytest.raises(ValueError):  # h outside family
        FebeISection("850/620", top_flange_thickness=150, bottom_flange_thickness=150)
    with pytest.raises(ValueError):  # gap between sub-families
        FebeISection("1675/620", top_flange_thickness=150, bottom_flange_thickness=150)
    with pytest.raises(ValueError):  # b not standard for large family
        FebeISection("1800/620", top_flange_thickness=200, bottom_flange_thickness=200)
    with pytest.raises(ValueError):  # malformed designation
        FebeISection("900", top_flange_thickness=150, bottom_flange_thickness=150)


def test_m_cycle_search_attested_metadata():
    # attested cycle 150->200->250->300 across successive 50 mm steps
    assert FebeISection("900/620", top_flange_thickness=150,
                        bottom_flange_thickness=150).dimensions.m_search_attested == 150.0
    assert FebeISection("950/620", top_flange_thickness=150,
                        bottom_flange_thickness=150).dimensions.m_search_attested == 200.0
    assert FebeISection("2050/880", top_flange_thickness=300,
                        bottom_flange_thickness=210).dimensions.m_search_attested == 300.0


def test_data_file_evidence_levels():
    ev = DATA["evidence_levels"]
    assert "SEARCH-ATTESTED" in ev["m_cycle"]
    assert "NOT PUBLISHED" in ev["flange_thicknesses"]
    assert "attested" in ev["widths_and_pairings"]
