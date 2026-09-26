"""ASA CONS "Grindă pod" girders: printed chains and fillet constructions.

No area/inertia table is published, so checks are analytic: printed
widths/depths exactly, and the tangent-construction residuals against the
printed fillet-extent chains pinned at their documented values (<= 2 mm
for 72/80, 95/105 lower fillets <= 3.1 mm, 95/105 top horizontal 5 mm).
"""

import pytest

from bridgebeams._geometry import section_properties
from bridgebeams.ro import AsaGrindaPodSection

from _aggregate import P, run_checks

EXPECTED = {  # depth, top width, max bottom width (mm)
    "42": (420, 220, 600), "52": (520, 220, 600), "72": (720, 1020, 920),
    "80": (800, 1020, 920), "95": (950, 1200, 470), "105": (1050, 1180, 500),
}


def _check_outline(size):
    sec = AsaGrindaPodSection(size)
    poly = sec.polygon
    assert poly.is_valid and poly.exterior.is_ccw
    depth, top, bottom = EXPECTED[size]
    minx, miny, maxx, maxy = poly.bounds
    assert (miny, maxy) == pytest.approx((0.0, depth))
    tops = [x for x, y in poly.exterior.coords if abs(y - depth) < 1e-9]
    assert max(tops) - min(tops) == pytest.approx(top)
    lower = [abs(x) for x, y in poly.exterior.coords if y < 200]
    assert 2 * max(lower) == pytest.approx(bottom)
    assert maxx - minx == pytest.approx(max(top, bottom))
    assert section_properties(poly)["cx"] == pytest.approx(0.0, abs=1e-6)
    assert sec.geometry is not None
    assert sec.name == f"Grindă pod {size}"


def _web_tangents(sec):
    xw = sec.dimensions["web_width"] / 2
    ys = [y for x, y in sec.dimensions.outline if abs(x - xw) < 1e-6]
    return min(ys), max(ys)


def _check_fillet_tangent_residuals(size, low, high):
    lo, hi = _web_tangents(AsaGrindaPodSection(size))
    assert lo == pytest.approx(low, abs=0.1)
    assert hi == pytest.approx(high, abs=0.1)


def test_fillet_tangent_residuals():
    run_checks((_check_fillet_tangent_residuals, P("size,low,high", [("72", 240.0, 509.0), ("80", 240.0, 589.0),
                                           ("95", 331.9, 729.9), ("105", 362.8, 809.9)])))


def _check_72_upper_fillet_extents_vs_printed_4_and_4_8_cm():
    sec = AsaGrindaPodSection("72")
    pts = sec.dimensions.outline
    xw = 135.0
    i = max(k for k, (x, y) in enumerate(pts) if abs(x - xw) < 1e-6)
    end = pts[i + 24]  # slope tangent point of the upper R50 fillet
    assert end[0] - xw == pytest.approx(38.1, abs=0.1)  # printed 40
    assert end[1] - pts[i][1] == pytest.approx(48.5, abs=0.1)  # printed 48


def test_42_throat_convention():
    pts = AsaGrindaPodSection("42").dimensions.outline
    # stem narrower than the 140 mm sharp intersection only inside the fillet
    stem = [x for x, y in pts if 150 < y < 370]
    assert min(stem) > 70.0


def _check_provenance():
    prov = {s: AsaGrindaPodSection(s).provenance for s in AsaGrindaPodSection.SIZES}
    assert prov == {"42": "transcribed-with-convention", "52": "estimate",
                    "72": "transcribed-with-convention", "80": "transcribed-with-convention",
                    "95": "transcribed-with-convention", "105": "estimate"}
    assert AsaGrindaPodSection.source_status


def _check_invalid_size():
    with pytest.raises(ValueError):
        AsaGrindaPodSection("62")


def test_ro_asa_catalogue_checks():
    run_checks(
        (_check_outline, P("size", AsaGrindaPodSection.SIZES)),
        _check_72_upper_fillet_extents_vs_printed_4_and_4_8_cm,
        _check_provenance,
        _check_invalid_size,
    )
