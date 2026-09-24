"""MOP Manual de Carreteras Vol. 4 §4.604 viga postensada and losa nervada rib."""
import pytest

from bridgebeams._geometry import section_properties
from bridgebeams.cl.mop_mc_v4 import MopLosaNervadaVigaSection, MopVigaPostensadaSection

from _aggregate import P, run_checks

ALL_ROWS = MopVigaPostensadaSection.SIZES + tuple(MopVigaPostensadaSection.ALIASES)


def _check_postensada_valid_and_bounds(size):
    s = MopVigaPostensadaSection(size)
    p = s.polygon
    d = s.dimensions
    assert p.is_valid and p.exterior.is_ccw
    assert p.bounds == pytest.approx((-d.a2 / 2, 0, d.a2 / 2, 800.0))
    assert d.web_height > 0
    assert (d.a1 - d.e) / 2 - d.top_fillet > 0  # flat flange underside exists
    assert s.provenance == "transcribed-with-convention"
    assert "Manual de Carreteras" in s.source_status
    # widths: a1 at the top face, e at mid-web, a2 across the bulb
    xs_top = sorted({round(x, 6) for x, y in p.exterior.coords if y == pytest.approx(800.0)})
    assert xs_top == pytest.approx([-d.a1 / 2, d.a1 / 2])


def _check_postensada_area_closed_form(size):
    d = MopVigaPostensadaSection(size).dimensions
    area = (d.a1 * d.top_flange
            + d.e * d.top_fillet + d.top_fillet ** 2  # web strip + two 45deg fillets
            + d.e * d.web_height
            + (d.e + d.a2) / 2 * d.bottom_taper
            + d.a2 * d.h4 - d.chamfer ** 2)  # two 2,5 cm soffit chamfers
    assert section_properties(MopVigaPostensadaSection(size).polygon)["area"] == pytest.approx(area)


def _check_rib_volumes(L):
    s = MopLosaNervadaVigaSection()
    area_m2 = section_properties(s.polygon)["area"] / 1e6
    assert area_m2 == pytest.approx(0.1575)
    # Cubicación 1 viga printed to 0.01 m3; beam length = L
    assert area_m2 * int(L) / 100 == pytest.approx(s.published["cubicacion_H30_m3_per_viga"][L], abs=0.005 + 1e-9)


def _check_rib_valid():
    s = MopLosaNervadaVigaSection()
    assert s.polygon.is_valid and s.polygon.exterior.is_ccw
    assert s.polygon.bounds == pytest.approx((-125, 0, 125, 700))
    assert s.provenance == "transcribed"


def _check_invalid_sizes():
    with pytest.raises(ValueError):
        MopVigaPostensadaSection("C8-L16")
    with pytest.raises(ValueError):
        MopLosaNervadaVigaSection("V30x80")


def test_cl_mop_mc_v4_catalogue_checks():
    run_checks(
        (_check_postensada_valid_and_bounds, P("size", ALL_ROWS)),
        (_check_postensada_area_closed_form, P("size", MopVigaPostensadaSection.SIZES)),
        (_check_rib_volumes, P("L", ["1100", "1200", "1300", "1400", "1500"])),
        _check_rib_valid,
        _check_invalid_sizes,
    )


def test_postensada_duplicate_rows_are_aliases():
    # Geometría table: C10-L12 == C8-L11 and C10-L13 == C8-L12 (cables differ only)
    for alias, canon in MopVigaPostensadaSection.ALIASES.items():
        a, c = MopVigaPostensadaSection(alias), MopVigaPostensadaSection(canon)
        assert a.canonical_size == canon
        assert a.dimensions == c.dimensions
        assert alias not in MopVigaPostensadaSection.SIZES
