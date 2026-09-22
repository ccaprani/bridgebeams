"""Compare MnDOT 2019 RB outlines with independently printed properties."""

import pytest

from bridgebeams._geometry import section_properties
from bridgebeams.us import MnRectangularBeamSection

# Figure 5.4.6.1, Section 5, February 2019; inch-based source literals.
# Rows are designation, depth, A (in2), yb (in), Ixx (in4), Sb (in3).
PUBLISHED = [
    ("14RB", 14, 364, 7.00, 5945, 849),
    ("18RB", 18, 468, 9.00, 12640, 1404),
    ("22RB", 22, 572, 11.00, 23070, 2097),
]


@pytest.mark.parametrize("kind,depth,area,yb,ixx,sb", PUBLISHED)
def test_mndot_published_gross_properties(kind, depth, area, yb, ixx, sb):
    beam = MnRectangularBeamSection(kind)
    poly = beam.polygon
    assert poly.is_valid and poly.exterior.is_ccw
    assert poly.bounds == pytest.approx((-13 * 25.4, 0, 13 * 25.4, depth * 25.4))
    p = section_properties(poly)
    inch = 25.4
    assert p["area"] / inch**2 == pytest.approx(area, abs=0.005)
    assert p["cy"] / inch == pytest.approx(yb, abs=0.005)
    # The manual prints Ixx as 12,640 and 23,070 for 18/22RB; exact
    # rectangles give 12,636 and 23,070.667, within its displayed rounding.
    assert p["ixx"] / inch**4 == pytest.approx(ixx, abs=5)
    assert p["ixx"] / p["cy"] / inch**3 == pytest.approx(sb, abs=0.5)
    assert p["cx"] == pytest.approx(0, abs=1e-10)
    assert beam.geometry is not None


@pytest.mark.parametrize("invalid", ["27M", "14rb", "", None])
def test_mndot_rejects_non_rb_and_unknown_names(invalid):
    with pytest.raises(ValueError):
        MnRectangularBeamSection(invalid)
