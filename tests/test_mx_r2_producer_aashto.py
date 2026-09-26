"""Mexican producer trabes AASHTO: Prefabricados Dragón (I–VI), Tubeco (III–VI)."""
import pytest
from shapely.geometry import LineString

from bridgebeams._geometry import section_properties
from bridgebeams.mx.r2_producer_aashto import DragonAashtoSection, TubecoAashtoSection

from _aggregate import P, run_checks

CASES = [(DragonAashtoSection, s) for s in DragonAashtoSection.SIZES] + [
    (TubecoAashtoSection, s) for s in TubecoAashtoSection.SIZES
]


def _width(p, y):
    return p.intersection(LineString([(-5000, y), (5000, y)])).length


def _check_valid_ccw_and_bounds(cls, size):
    s = cls(size)
    p = s.polygon
    assert p.is_valid and p.exterior.is_ccw
    d = s.dimensions
    half = max(d.top_width, d.bottom_width) / 2
    assert p.bounds == pytest.approx((-half, 0.0, half, d.depth))
    assert d.web_height > 0
    assert s.provenance in {"transcribed", "transcribed-with-convention"}
    assert s.source_status
    # widths at mid-web, just below the top and just above the soffit
    assert _width(p, d.depth - 1) == pytest.approx(d.top_width)
    assert _width(p, d.bottom_flange + d.bottom_taper + d.web_height / 2) == pytest.approx(d.web_width)
    assert _width(p, d.soffit_chamfer + 1) == pytest.approx(d.bottom_width, abs=1e-6)


def _check_printed_vertical_chain_closes(cls, size):
    s = cls(size)
    chain = s.published.get("printed_chain_m") or s.published["printed_chain_cm"]
    scale = 1000.0 if "printed_chain_m" in s.published else 10.0
    total = sum(chain) * scale
    if cls is TubecoAashtoSection and size == "IV":
        # pinned source typo: printed chain 129 cm vs printed depth 135 cm ('9' should be 15)
        assert total == pytest.approx(1290.0)
        assert s.dimensions.top_outer_taper == pytest.approx(150.0)
    else:
        assert total == pytest.approx(s.dimensions.depth)


def test_tubeco_iii_top_width_typo_pinned():
    s = TubecoAashtoSection("III")
    assert s.published["printed_top_width_cm"] == 30  # printed, contradicts 11 + 18 + 11
    assert s.dimensions.top_width == pytest.approx(400.0)


def _check_tubeco_knee_from_printed_chain():
    for size in ("V", "VI"):
        d = TubecoAashtoSection(size).dimensions
        assert d.top_knee_width == pytest.approx(200 + 2 * 95)
        assert (d.top_width - d.top_knee_width) / 2 == pytest.approx(340)


def _check_analytic_areas():
    # Hand-computed trapezoid sums (mm^2)
    assert section_properties(DragonAashtoSection("IV").polygon)["area"] == pytest.approx(497400.0)
    assert section_properties(DragonAashtoSection("I").polygon)["area"] == pytest.approx(168620.0)
    # Tubeco IV: Dragón IV outline less two 20x20 mm soffit chamfer triangles (same printed widths/chain)
    t4 = section_properties(TubecoAashtoSection("IV").polygon)["area"]
    assert t4 == pytest.approx(497400.0 - 2 * 0.5 * 20.0 * 20.0)


def _check_invalid_size():
    with pytest.raises(ValueError):
        DragonAashtoSection("VII")
    with pytest.raises(ValueError):
        TubecoAashtoSection("I")


def test_mx_r2_producer_aashto_catalogue_checks():
    run_checks(
        (_check_valid_ccw_and_bounds, P("cls,size", CASES)),
        (_check_printed_vertical_chain_closes, P("cls,size", CASES)),
        _check_tubeco_knee_from_printed_chain,
        _check_analytic_areas,
        _check_invalid_size,
    )
