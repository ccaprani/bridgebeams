"""PCI Appendix B-7 (November 2011) published gross-section properties."""

import pytest

from bridgebeams._geometry import section_properties
from bridgebeams.us import AashtoIBeamSection

from _aggregate import P, run_checks


# Type, area (in²), centroid from soffit (in), centroidal Ixx (in⁴).
PUBLISHED = [
    ("I", 276, 12.59, 22750),
    ("II", 369, 15.83, 50980),
    ("III", 560, 20.27, 125390),
    ("IV", 789, 24.73, 260730),
    ("V", 1013, 31.96, 521180),
    ("VI", 1085, 36.38, 733320),
]


def _check_pci_dimension_chain_reproduces_published_properties(size, area, y_bottom, ixx):
    beam = AashtoIBeamSection(size)
    polygon = beam.polygon
    assert polygon.is_valid and polygon.exterior.is_ccw
    d = beam.dimensions
    assert polygon.bounds == pytest.approx((-d.b1 / 2 if d.b1 >= d.b2 else -d.b2 / 2,
                                           0, max(d.b1, d.b2) / 2, d.d1))
    props = section_properties(polygon)
    assert props["area"] / 25.4**2 == pytest.approx(area, abs=0.5)
    assert props["cy"] / 25.4 == pytest.approx(y_bottom, abs=0.005)
    assert props["ixx"] / 25.4**4 == pytest.approx(ixx, abs=25)
    assert props["cx"] == pytest.approx(0, abs=1e-9)
    assert beam.geometry is not None


def _check_type_v_upper_flange_has_two_source_slopes():
    beam = AashtoIBeamSection("V")
    d = beam.dimensions
    points_in = [(round(x / 25.4, 3), round(y / 25.4, 3)) for x, y in d.outline]
    assert (8, 55) in points_in  # D3/B5 transition in the PCI sketch.
    assert (21, 58) in points_in


def _check_unknown_aashto_size_rejected():
    with pytest.raises(ValueError):
        AashtoIBeamSection("Type IV Pakistan")


def test_us_aashto_i_catalogue_checks():
    run_checks(
        (_check_pci_dimension_chain_reproduces_published_properties, P("size,area,y_bottom,ixx", PUBLISHED)),
        _check_type_v_upper_flange_has_two_source_slopes,
        _check_unknown_aashto_size_rejected,
    )
