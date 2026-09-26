"""SADET (Morocco) I40-I55 estimated outlines."""
import pytest

from bridgebeams._geometry import section_properties
from bridgebeams.ma import SadetIBeamSection

from _aggregate import P, run_checks


def _check_outline(size):
    s = SadetIBeamSection(size)
    p = s.polygon
    assert p.is_valid and p.exterior.is_ccw
    minx, miny, maxx, maxy = p.bounds
    assert maxx - minx == pytest.approx(s.published["base_width"])
    assert (miny, maxy) == (0.0, 1220.0)
    assert s.provenance == "estimate"
    assert "producer catalogue" in s.source_status
    webs = sorted({abs(x) for x, y in p.exterior.coords if 200 < y < 1000})
    assert webs == [s.published["web_width_callout"] / 2]
    s.geometry


def _check_mass_residual_pinned(size, lo, hi):
    """Estimate vs printed mass at an assumed 2500 kg/m3 (density not printed)."""
    s = SadetIBeamSection(size)
    m = section_properties(s.polygon)["area"] * 2.5e-3
    assert lo < m / s.published["mass_kg_per_m"] - 1 < hi


def test_mass_residual_pinned():
    run_checks((_check_mass_residual_pinned, P("size,lo,hi", [("I45", -0.11, -0.08), ("I50", -0.05, -0.03), ("I55", -0.05, -0.03)])))


def test_i40_mass_anomaly_preserved():
    s = SadetIBeamSection("I40")
    assert s.published["mass_kg_per_m"] == 282
    assert section_properties(s.polygon)["area"] * 2.5e-3 > 2 * 282


def _check_invalid():
    with pytest.raises(ValueError):
        SadetIBeamSection("I60")


def test_ma_sadet_i_beams_catalogue_checks():
    run_checks(
        (_check_outline, P("size", SadetIBeamSection.SIZES)),
        _check_invalid,
    )
