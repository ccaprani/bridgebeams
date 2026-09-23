"""Ashghal TY / TYE beams (SD 5-1-111 / 5-1-112 Rev 1)."""
import pytest

from bridgebeams._geometry import section_properties
from bridgebeams.qa.r2_ty_beams import QaTyBeamSection, QaTyeBeamSection

ALL = [(QaTyBeamSection, s) for s in QaTyBeamSection.SIZES] + [
    (QaTyeBeamSection, s) for s in QaTyeBeamSection.SIZES
]


@pytest.mark.parametrize("cls,size", ALL)
def test_valid_ccw_and_depth(cls, size):
    s = cls(size)
    p = s.polygon
    assert p.is_valid and p.exterior.is_ccw
    minx, miny, maxx, maxy = p.bounds
    assert miny == 0 and maxy == pytest.approx(s.published["depth"])
    assert maxx - minx == pytest.approx(750.0)
    assert s.provenance == "transcribed"
    assert "current standard" in s.source_status
    s.geometry


@pytest.mark.parametrize("size", QaTyBeamSection.SIZES)
def test_ty_published(size):
    s = QaTyBeamSection(size)
    r = s.published
    p = section_properties(s.polygon)
    # rounded printed values; drawing gives exact CAD dimensions
    assert p["area"] == pytest.approx(r["area"], rel=0.0008)
    assert p["cy"] == pytest.approx(r["yb"], abs=0.5)
    assert p["ixx"] == pytest.approx(r["ixx"], rel=0.0006)
    assert abs(p["cx"]) < 1e-6
    top = s.dimensions.web_width_at(r["depth"])
    assert top == pytest.approx(r["printed_top_width"], abs=0.6)


@pytest.mark.parametrize("size", QaTyeBeamSection.SIZES)
def test_tye_published_pinned_offset(size):
    """TYE areas/inertias are consistently 0.13-0.16% below the table (pinned)."""
    s = QaTyeBeamSection(size)
    r = s.published
    p = section_properties(s.polygon)
    da = p["area"] / r["area"] - 1
    assert -0.0016 < da < -0.0012
    assert -0.0016 < p["ixx"] / r["ixx"] - 1 < -0.0012
    assert p["cy"] == pytest.approx(r["yb"], abs=0.6)
    assert p["cx"] + 375 == pytest.approx(r["xc_from_vertical_face"], abs=1.0)


def test_tye_top_width_and_edge_face():
    s = QaTyeBeamSection("TYE10")
    xs = [x for x, y in s.polygon.exterior.coords if y == 850]
    assert max(xs) - min(xs) == pytest.approx(575.0)
    assert min(xs) == -375.0


@pytest.mark.parametrize("cls,bad", [(QaTyBeamSection, "TY11"), (QaTyeBeamSection, "TY1")])
def test_invalid(cls, bad):
    with pytest.raises(ValueError):
        cls(bad)
