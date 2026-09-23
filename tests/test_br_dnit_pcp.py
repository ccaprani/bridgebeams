"""DNIT IPR-751 PCP-10/15/20 precast I longarinas vs Volume 2 Tabela 2-5."""
import pytest

from bridgebeams._geometry import section_properties
from bridgebeams.br import DnitPcpLongarinaSection

from _aggregate import P, run_checks


def _check_valid_and_bounds(size):
    s = DnitPcpLongarinaSection(size)
    p = s.polygon
    assert p.is_valid and p.exterior.is_ccw
    d = s.dimensions
    assert p.bounds == pytest.approx((-d.flange_width / 2, 0, d.flange_width / 2, d.depth))
    assert s.provenance == "transcribed"
    assert "IPR-751" in s.source_status


def _check_published_stage1_properties(size):
    s = DnitPcpLongarinaSection(size)
    pub = s.published["published_stage1"]
    props = section_properties(s.polygon)
    # A printed to 3 d.p. (m2), yi to mm, I to 3 significant figures
    assert props["area"] / 1e6 == pytest.approx(pub["A_m2"], abs=0.0005 + 1e-9)
    assert props["cy"] / 1e3 == pytest.approx(pub["yi_m"], abs=0.0005 + 1e-9)
    assert props["ixx"] / 1e12 == pytest.approx(pub["I_m4"], rel=0.012)


def test_pcp10_pinned_area_discrepancy():
    s = DnitPcpLongarinaSection("PCP-10")
    props = section_properties(s.polygon)
    pub = s.published["published_stage1"]
    # drawing gives exactly 0.2600 m2; Tabela 2-5 prints 0.267 (+2.7%), pinned
    assert props["area"] == pytest.approx(260000.0)
    assert pub["A_m2"] == 0.267
    assert props["cy"] / 1e3 == pytest.approx(pub["yi_m"])
    assert props["ixx"] / 1e12 == pytest.approx(pub["I_m4"], abs=0.0005)


def _check_invalid_size():
    with pytest.raises(ValueError):
        DnitPcpLongarinaSection("PCP-25")


def test_br_dnit_pcp_catalogue_checks():
    run_checks(
        (_check_valid_and_bounds, P("size", DnitPcpLongarinaSection.SIZES)),
        (_check_published_stage1_properties, P("size", ["PCP-15", "PCP-20"])),
        _check_invalid_size,
    )
