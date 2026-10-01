"""São Domingos bridge (ES-010) precast I longarina vs Atena 2023 chapter figures."""
import pytest

from bridgebeams._geometry import section_properties
from bridgebeams.br.r3_ifes_sao_domingos import SaoDomingosLongarinaSection

from _aggregate import run_checks


def _check_valid_and_bounds():
    s = SaoDomingosLongarinaSection()
    p = s.polygon
    d = s.dimensions
    assert p.is_valid and p.exterior.is_ccw
    assert p.bounds == pytest.approx((-300, 0, 300, 1300))
    assert (d.top_flange + d.top_taper + d.web_height + d.bottom_taper
            + d.bottom_flange) == pytest.approx(d.depth)
    assert s.provenance == "transcribed"
    assert "project-specific" in s.source_status


def _check_self_weight():
    s = SaoDomingosLongarinaSection()
    area_m2 = section_properties(s.polygon)["area"] / 1e6
    assert area_m2 == pytest.approx(0.374375)
    # Tabela 5 q3 = 9,4 kN/m (2 s.f.) at 25 kN/m3
    assert 25.0 * area_m2 == pytest.approx(s.published["q3_self_weight_kN_per_m"], abs=0.05)


def _check_composite_depth():
    s = SaoDomingosLongarinaSection()
    assert (s.dimensions.depth / 1e3 + s.published["slab_thickness_m"]
            == pytest.approx(s.published["h_viga_laje_m"]))


def _check_invalid_size():
    with pytest.raises(ValueError):
        SaoDomingosLongarinaSection("SD-150")


def test_br_r3_ifes_sao_domingos_catalogue_checks():
    run_checks(_check_valid_and_bounds, _check_self_weight, _check_composite_depth,
               _check_invalid_size)


def test_yGc_not_reproduced_pinned():
    # Tabela 8 yGc = 0,921 m is neither the girder centroid (0.651 m) nor the
    # gross composite centroid with b = 2.2 m, 18 cm slab (1.031 m); pinned.
    s = SaoDomingosLongarinaSection()
    props = section_properties(s.polygon)
    A, y = props["area"], props["cy"]
    As = 2200 * 180
    yc = (A * y + As * 1390) / (A + As) / 1e3
    assert y / 1e3 == pytest.approx(0.651, abs=0.001)
    assert yc == pytest.approx(1.031, abs=0.001)
    assert s.published["yGc_m"] == 0.921
