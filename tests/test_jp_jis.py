"""Japanese JIS A 5373 T-girders: structural validation. No published
A/Ixx tables are freely available; checks are stack/geometry/symmetry."""

import pytest

from bridgebeams.jp import JisTGirderSection
from bridgebeams._geometry import section_properties, as_polygon

from _aggregate import P, run_checks


def _check_symmetric():
    for size in JisTGirderSection.SIZES:
        beam = JisTGirderSection(size)
        xmin, xmax, _, _ = beam.geometry.calculate_extents()
        assert -xmin == pytest.approx(xmax), size


def _check_depths_match_jis():
    expected = {"AG18": 900, "AG19": 1000, "AG20": 1000, "AG21": 1100,
                "AG22": 1100, "AG23": 1200, "AG24": 1200,
                "BG18": 1000, "BG19": 1000, "BG20": 1100, "BG21": 1100,
                "BG22": 1200, "BG23": 1200, "BG24": 1300}
    for size, depth in expected.items():
        assert JisTGirderSection(size).dimensions.depth == depth


def _check_section_constants():
    beam = JisTGirderSection("AG18")
    d = beam.dimensions
    assert d.top_flange_width == 800
    assert d.top_flange_thickness == 160
    assert d.web_bottom_width == 300
    assert d.haunch == 35


def _check_area_positive_and_plausible():
    # web 300 x full depth dominates; rough bounds for a 900-1300 deep section
    for size in JisTGirderSection.SIZES:
        beam = JisTGirderSection(size)
        props = section_properties(as_polygon(beam.geometry))
        assert 0.3 < props["area"] / 1e6 < 0.8, size


def _check_invalid_size_raises():
    with pytest.raises(ValueError):
        JisTGirderSection("AG25")


def test_jp_jis_catalogue_checks():
    run_checks(
        _check_symmetric,
        _check_depths_match_jis,
        _check_section_constants,
        _check_area_positive_and_plausible,
        _check_invalid_size_raises,
    )
