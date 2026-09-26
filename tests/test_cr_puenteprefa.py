"""PuentePrefa (Costa Rica) Viga California and Simple te."""
import pytest
from shapely.geometry import LineString

from bridgebeams._geometry import section_properties
from bridgebeams.cr import PuentePrefaBeamSection

from _aggregate import P, run_checks


def _width(p, y):
    return p.intersection(LineString([(-5000, y), (5000, y)])).length


def _check_valid(size):
    s = PuentePrefaBeamSection(size)
    p = s.polygon
    assert p.is_valid and p.exterior.is_ccw
    assert p.bounds[1] == 0 and p.bounds[3] == pytest.approx(10 * s.published["printed_cm"]["depth"])
    assert s.provenance in {"estimate", "transcribed-with-convention"}


def _check_california_printed(size):
    p = PuentePrefaBeamSection(size).polygon
    assert _width(p, 10) == pytest.approx(480)  # printed bottom 48
    assert _width(p, 700) == pytest.approx(180)  # web 18 = 48 - 2 x 15 overhang


def _check_simple_te():
    s = PuentePrefaBeamSection("SIMPLE-TE-97")
    p = s.polygon
    assert _width(p, 965) == pytest.approx(930)
    assert _width(p, 0.001) == pytest.approx(110, abs=0.01)
    assert _width(p, 869.999) == pytest.approx(200, abs=0.01)
    # 93x10 flange + trapezoidal 87 cm stem (20 -> 11)
    assert section_properties(p)["area"] == pytest.approx(930 * 100 + 0.5 * (200 + 110) * 870)


def _check_invalid_size():
    with pytest.raises(ValueError):
        PuentePrefaBeamSection("DOBLE-TE")


def test_cr_puenteprefa_catalogue_checks():
    run_checks(
        (_check_valid, P("size", PuentePrefaBeamSection.SIZES)),
        (_check_california_printed, P("size", ["CALIFORNIA-137", "CALIFORNIA-167"])),
        _check_simple_te,
        _check_invalid_size,
    )
