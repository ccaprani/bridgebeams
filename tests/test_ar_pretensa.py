"""Pretensa VI / VPI-45 estimated outlines: self-weight fit and sanity bounds."""
import pytest

from bridgebeams._geometry import section_properties
from bridgebeams.ar import PretensaViSection

from _aggregate import P, run_checks


def _check_valid_estimate_and_mass(size):
    s = PretensaViSection(size)
    p = s.polygon
    assert p.is_valid and p.exterior.is_ccw
    assert s.provenance == "estimate"
    d = s.dimensions
    assert d.depth == pytest.approx(1000 * s.published["published_depth_m"])
    assert p.bounds == pytest.approx((-d.flange_width / 2, 0, d.flange_width / 2, d.depth))
    # gross area reproduces published kg/m at the stated 2500 kg/m3 (fit target)
    area = section_properties(p)["area"]
    assert area * 1e-6 * 2500 == pytest.approx(s.published["published_self_weight_kg_m"], rel=2e-4)
    # fitted webs stay in a physically plausible band
    assert 80 < d.web_width < 160
    assert d.web_height > 0


def _check_invalid_size():
    with pytest.raises(ValueError):
        PretensaViSection("VI-200")


def test_ar_pretensa_catalogue_checks():
    run_checks(
        (_check_valid_estimate_and_mass, P("size", PretensaViSection.SIZES)),
        _check_invalid_size,
    )
