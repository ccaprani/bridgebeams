"""TIEL A-A nominal model: independent strip integration and rounded checks."""

import pytest
from shapely.affinity import scale

from bridgebeams import TielModelISection as RootSection
from bridgebeams.fi import TielModelIDimensions, TielModelISection
from bridgebeams._geometry import as_polygon, section_properties
from _aggregate import run_checks


def _strip_properties(layers):
    # Integrate b(y), y*b(y), y²*b(y) over independently transcribed strips.
    # This is not the implementation's polygon/shoelace algorithm.
    moments = [0.0, 0.0, 0.0]
    for y0, y1, b0, b1 in layers:
        slope = (b1 - b0) / (y1 - y0)
        intercept = b0 - slope * y0
        for n in range(3):
            moments[n] += (intercept * (y1**(n+1) - y0**(n+1)) / (n+1)
                           + slope * (y1**(n+2) - y0**(n+2)) / (n+2))
    a, q, i0 = moments
    return {"area": a, "cy": q/a, "ixx": i0 - q*q/a}


def _check_outline():
    beam = TielModelISection()
    assert RootSection is TielModelISection
    assert isinstance(beam.dimensions, TielModelIDimensions)
    assert beam.SIZES == ("TIEL-model-AA-h1270",)
    assert beam.dimensions.outline == [
        (-300, 0), (300, 0), (300, 210), (90, 420), (90, 1020),
        (150, 1070), (150, 1270), (-150, 1270), (-150, 1070),
        (-90, 1020), (-90, 420), (-300, 210)]
    p = beam.polygon
    assert p.is_valid and p.exterior.is_ccw and not p.interiors
    assert p.bounds == (-300, 0, 300, 1270)
    assert p.equals(scale(p, xfact=-1, yfact=1, origin=(0, 0)))
    assert as_polygon(beam.geometry).equals(p)
    d = beam.dimensions
    assert d.bottom_thickness + d.bottom_haunch + d.web_height + d.top_haunch + d.top_thickness == d.depth


def _check_properties():
    beam = TielModelISection()
    expected = _strip_properties([
        (0, 210, 600, 600), (210, 420, 600, 180),
        (420, 1020, 180, 180), (1020, 1070, 180, 300),
        (1070, 1270, 300, 300)])
    got = section_properties(as_polygon(beam.geometry))
    assert got["cx"] == pytest.approx(0, abs=1e-10)
    for key, value in expected.items():
        assert got[key] == pytest.approx(value, rel=1e-10)
    assert got["area"] == 387900
    ideal = _strip_properties([(0, 315, 600, 600), (315, 1045, 180, 180),
                               (1045, 1270, 300, 300)])
    assert ideal["area"] == got["area"]
    assert abs(ideal["cy"] - got["cy"]) > 1
    assert abs(ideal["ixx"] - got["ixx"]) > 3e8
    # Both geometries corroborate the printed *rounded* values, not each other.
    for props in (got, ideal):
        assert round(props["area"] / 1e6, 2) == beam.published["area_m2"]
        assert round(props["cy"] / 1e3, 2) == beam.published["cy_m"]
        assert round(props["ixx"] / 1e12, 3) == beam.published["ixx_m4"]


def _check_source_and_scope():
    beam = TielModelISection()
    assert beam.source["pdf_page"] == 28
    assert beam.source["printed_sheet"] == "LIITE 1.4"
    assert beam.source["section"] == "A-A"
    assert beam.source["sha256"] == "8a9b178803a0dbcdd85e872a4f6d80fd690b41688e3b4754e7a105ff8381fa78"
    assert beam.published["pdf_page"] == 51
    assert "not a national SKU" in beam.source_status
    for invalid in ("I1270", "TIEL-model-AA-h1500", 1270):
        with pytest.raises(ValueError):
            TielModelISection(invalid)


def test_fi_tiel_model_catalogue_checks():
    run_checks(_check_outline, _check_properties, _check_source_and_scope)
