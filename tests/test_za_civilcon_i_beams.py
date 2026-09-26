"""Validate PPBI source orientation and its published section properties.

B1 is the drawn soffit; Yb is measured up from it. Area and centroidal
inertia alone cannot distinguish the former vertically reflected geometry.
"""

import json
from importlib import resources

import pytest
from shapely.geometry import LineString

from bridgebeams._geometry import as_polygon, section_properties
from bridgebeams.za import CivilconIBeamSection

from _aggregate import P, run_checks

DATA = json.loads(
    resources.files("bridgebeams.za.data").joinpath("civilcon_i_beams.json").read_text()
)
ROWS = DATA["published_properties"]


def _check_published_properties_and_source_orientation(row):
    beam = CivilconIBeamSection(row["section"])
    poly = beam.polygon
    props = section_properties(poly)
    assert poly.is_valid
    assert poly.exterior.is_ccw
    assert as_polygon(beam.geometry).equals(poly)
    assert props["area"] == pytest.approx(row["area"], rel=1e-12)
    assert props["cy"] == pytest.approx(row["yb_from_b1_face"], abs=0.5)
    height = row["d1_depth"]
    assert poly.intersection(LineString([(-1000, 0), (1000, 0)])).length == row["b1_soffit_width"]
    assert poly.intersection(LineString([(-1000, height), (1000, height)])).length == row["b4_top_flange_width"]
    assert props["ixx"] / props["cy"] / 1e6 == pytest.approx(row["zb_e6"], rel=4e-6)
    top_modulus = props["ixx"] / (height - props["cy"]) / 1e6
    if row["section"] == "I18":
        # Sole published Zt inconsistency: preserve the source number and
        # pin the actual discrepancy instead of widening all tolerances.
        assert row["zt_e6"] == 213.0987
        assert top_modulus / row["zt_e6"] - 1 == pytest.approx(0.004169, abs=1e-6)
    else:
        assert top_modulus == pytest.approx(row["zt_e6"], rel=4e-6)


def test_i1_source_soffit_and_centroid_regression():
    """Direct source literals make the orientation contract independent of JSON."""
    poly = CivilconIBeamSection("I1").polygon
    assert poly.centroid.y == pytest.approx(318.221, abs=0.001)
    assert poly.intersection(LineString([(-1000, 0), (1000, 0)])).length == 410
    assert poly.intersection(LineString([(-1000, 710), (1000, 710)])).length == 360


def _check_depth_stack_and_symmetry():
    for size in CivilconIBeamSection.SIZES:
        beam = CivilconIBeamSection(size)
        d = beam.dimensions
        assert d.d2 + d.d3 + d.d4 + d.d5 + d.d6 == d.d1
        assert d.b3 < min(d.b1, d.b4)
        minx, _, maxx, _ = beam.polygon.bounds
        assert minx == -maxx
        assert (d.b4 - d.b3) / 2 == d.d5


def _check_invalid_size_raises():
    with pytest.raises(ValueError):
        CivilconIBeamSection("I21")


def _check_all_20_sizes_present():
    assert CivilconIBeamSection.SIZES == tuple(f"I{i}" for i in range(1, 21))


def test_za_civilcon_i_beams_catalogue_checks():
    run_checks(
        (_check_published_properties_and_source_orientation, P("row", ROWS, ids=lambda row: row["section"])),
        _check_depth_stack_and_symmetry,
        _check_invalid_size_raises,
        _check_all_20_sizes_present,
    )


def test_civilcon_i18_published_zt_pinned():
    run_checks((_check_published_properties_and_source_orientation,
                P("row", [r for r in ROWS if r["section"] == "I18"], ids=lambda row: row["section"])))
