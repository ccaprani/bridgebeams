"""Civilcon Special U (SU1/SU2) wide trough: fitted reconstruction.

PPBUS page 1 draws SU2 (1200 mm) solid and SU1 (900 mm) as a dashed top
lobe 300 mm lower on the same webs. The catalogue index says "US"; the
sheet and table say SU1/SU2, which are used here.

Printed and used directly: 2000 mm base, flat soffit without chamfers;
top lobe 175 + 175 = 350 mm wide, inner edge 850 mm from the centreline;
lobe stack 50 (raised strip above the shoulders) + 150 (vertical) + 100
(splay); 75 mm outer and inner splay offsets (inner splay length 125 = 75/100
triangle); 75 mm shoulders each side of a 200 mm raised strip; and the web
horizontal width 60 + 80 + 60 = 200 mm.

Derived: neck at the bottom of the lobe splays spans x = 925…1125, so the web
faces are parallel with a 1 : 7.2 batter from x = 800/1000 at the soffit.

Not printed; scaled from the drawing and confirmed by the properties: floor top
200 mm above the soffit, with a 45° splay from x = 700 to the inner web face
(meeting it at y ≈ 348.4). With these values both
published areas agree within 0.010% and Yb within 0.4 mm; all four
section moduli agree within 0.02%. A 1 mm floor-thickness change gives
about 0.2% area error, so the floor thickness is well constrained. The
splay size is weakly constrained. The published area difference of exactly
120000 mm² between the two depths confirms the 200 mm horizontal web width.

Drawing inconsistency: the dashed SU1 lobe is dimensioned 810 mm from the
centreline. Sliding the lobe down the 1 : 7.2 web by 300 mm gives 808.3
mm. The implementation keeps the web-consistent 808.3 value.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon
from shapely.geometry.polygon import orient

from bridgebeams._geometry import geometry_from_polygon


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.za.data").joinpath("civilcon_special_u_beams.json").read_text()
    )


@dataclass(frozen=True)
class CivilconSpecialUBeamDimensions:
    """Millimetres; origin at the soffit centre, y positive upwards.

    ``floor_thickness`` and ``splay_start_half_width`` are scaled from the
    drawing and fitted, not printed. The floor splay is at 45°.
    """

    depth: float
    floor_thickness: float = 200.0
    splay_start_half_width: float = 700.0
    base_width: float = 2000.0
    web_horizontal_width: float = 200.0
    lobe_height: float = 300.0
    lobe_step: float = 50.0
    lobe_splay_height: float = 100.0
    lobe_splay_offset: float = 75.0
    shoulder_width: float = 75.0
    batter: float = 7.2

    def outer_x(self, y: float) -> float:
        return self.base_width / 2 + y / self.batter

    def inner_x(self, y: float) -> float:
        return self.outer_x(y) - self.web_horizontal_width

    @property
    def splay_top(self) -> tuple[float, float]:
        """45° floor splay meets the inner web face."""
        x0, y0 = self.splay_start_half_width, self.floor_thickness
        y = (self.inner_x(0.0) - x0 + y0) / (1 - 1 / self.batter)
        return self.inner_x(y), y

    @property
    def outline(self) -> list[tuple[float, float]]:
        """Right side: soffit corner, outer web, lobe, inner web, floor to centre."""
        d = self.depth
        hn = d - self.lobe_height
        ni, no = self.inner_x(hn), self.outer_x(hn)
        s, e = self.lobe_splay_offset, self.lobe_splay_height
        k = self.lobe_step
        return [
            (self.base_width / 2, 0.0),
            (no, hn),
            (no + s, hn + e),
            (no + s, d - k),
            (no + s - self.shoulder_width, d - k),
            (no + s - self.shoulder_width, d),
            (ni - s + self.shoulder_width, d),
            (ni - s + self.shoulder_width, d - k),
            (ni - s, d - k),
            (ni - s, hn + e),
            (ni, hn),
            self.splay_top,
            (self.splay_start_half_width, self.floor_thickness),
            (0.0, self.floor_thickness),
        ]


class CivilconSpecialUBeamSection:
    """Civilcon Special U (SU1/SU2) gross concrete section (PPBUS)."""

    SIZES = ("SU1", "SU2")

    def __init__(self, size: str = "SU2"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        row = next(r for r in data["sections"] if r["section"] == size)
        fit = data["fitted_parameters"]
        self.size = size
        self.published = row
        self.provenance = row["provenance"]
        self.source_status = data["source_status"]
        self.dimensions = CivilconSpecialUBeamDimensions(
            depth=row["depth"],
            floor_thickness=fit["floor_thickness"],
            splay_start_half_width=fit["splay_start_half_width"],
        )

    @property
    def polygon(self) -> Polygon:
        right = self.dimensions.outline
        left = [(-x, y) for x, y in reversed(right[:-1])]
        return orient(Polygon(right + left), sign=1.0)

    @property
    def geometry(self):
        """Return the gross concrete ``sectionproperties`` geometry."""
        return geometry_from_polygon(self.polygon)


__all__ = ["CivilconSpecialUBeamDimensions", "CivilconSpecialUBeamSection"]
