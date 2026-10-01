"""Civilcon U1–U12 open-top trough ("U beam"): fitted reconstruction.

PPBU page 1 is a single U12 (1600 mm) section plus an elevation showing
how the shallower marks are formed. Printed and used directly:

* 970 mm base, taken at the theoretical soffit intersection of the outer
  faces (the drawn faces pass through ±485 at y=0 when scaled); 35 × 35 mm
  bottom chamfers measured along the face;
* outer batter 6.75 : 1 (vertical : horizontal) and 165 mm web thickness
  measured normal to the parallel web faces (horizontal width 166.80 mm);
* top: 50 mm outer shoulder 30 mm below the top, 250 mm raised strip,
  40 mm inner shoulder 33 mm below the top, then a 15 mm vertical lip;
* inner thickening: the inner face runs from the lip to meet the web
  face 380 mm below the inner shoulder (the right-hand elevation shows the
  whole top block moving down the outer face for shallower marks);
* floor half-widths 240 (centre valley to break) + 129 (break to web toe).

Not printed: the floor valley and break heights. The web-toe height
follows from the printed 369 mm half-width on the inner web face
(342.9 mm). The valley (129.4 mm) and break (218.3 mm) heights are fitted by least
squares to all nine published areas, centroids and inertias. The drawing
scales to about 153/204 mm and puts the toe at about (371, 358). The printed
129 mm scales as about 131 mm. Treat the floor as a reconstruction, not
a production dimension.

Published area increments are exactly 33523 mm² per 100 mm of depth,
implying a 167.6 mm horizontal web width against 166.8 mm from the printed
165 mm/6.75:1. This outline keeps the printed values, so areas drift from
+0.10% (U1) to -0.11% (U12). The printed U10 Zb (255.65e6) is inconsistent
with its own Zt and Yb; the outline gives about 225.6e6, which suggests a
digit transposition. The raw value is preserved.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon
from shapely.geometry.polygon import orient

from bridgebeams._geometry import geometry_from_polygon


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.za.data").joinpath("civilcon_u_beams.json").read_text()
    )


@dataclass(frozen=True)
class CivilconUBeamDimensions:
    """Millimetres; origin at the soffit centre, y positive upwards.

    ``valley_height`` and ``break_height`` are fitted (not printed).
    """

    depth: float
    valley_height: float = 129.4
    break_height: float = 218.3
    base_width: float = 970.0
    chamfer: float = 35.0
    batter: float = 6.75
    web_normal_thickness: float = 165.0
    outer_shoulder: float = 50.0
    outer_step: float = 30.0
    strip_width: float = 250.0
    inner_shoulder: float = 40.0
    inner_step: float = 33.0
    inner_lip: float = 15.0
    thickening_height: float = 380.0
    floor_break_half_width: float = 240.0
    floor_toe_offset: float = 129.0

    @property
    def web_horizontal_width(self) -> float:
        return self.web_normal_thickness * math.sqrt(1 + 1 / self.batter**2)

    def outer_x(self, y: float) -> float:
        return self.base_width / 2 + y / self.batter

    def inner_x(self, y: float) -> float:
        return self.outer_x(y) - self.web_horizontal_width

    @property
    def toe(self) -> tuple[float, float]:
        """Derived web toe: printed half-width on the inner web face."""
        x = self.floor_break_half_width + self.floor_toe_offset
        return x, (x - self.inner_x(0.0)) * self.batter

    @property
    def outline(self) -> list[tuple[float, float]]:
        """Right side: soffit, outer face, top, inner face, floor to centre."""
        d = self.depth
        c = self.outer_x(self.chamfer)
        t = self.outer_x(d - self.outer_step)
        break_y = d - self.inner_step - self.thickening_height
        return [
            (c - self.chamfer, 0.0),
            (c, self.chamfer),
            (t, d - self.outer_step),
            (t - self.outer_shoulder, d - self.outer_step),
            (t - self.outer_shoulder, d),
            (t - self.outer_shoulder - self.strip_width, d),
            (t - self.outer_shoulder - self.strip_width, d - self.inner_step),
            (t - self.outer_shoulder - self.strip_width - self.inner_shoulder, d - self.inner_step),
            (t - self.outer_shoulder - self.strip_width - self.inner_shoulder,
             d - self.inner_step - self.inner_lip),
            (self.inner_x(break_y), break_y),
            self.toe,
            (self.floor_break_half_width, self.break_height),
            (0.0, self.valley_height),
        ]


class CivilconUBeamSection:
    """Civilcon U-beam gross concrete section (PPBU), fitted floor levels."""

    SIZES = ("U1", "U3", "U5", "U7", "U8", "U9", "U10", "U11", "U12")

    def __init__(self, size: str = "U8"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        row = next(r for r in data["sections"] if r["section"] == size)
        fit = data["fitted_parameters"]
        self.size = size
        self.published = row
        self.provenance = row["provenance"]
        self.source_status = data["source_status"]
        self.dimensions = CivilconUBeamDimensions(
            depth=row["depth"],
            valley_height=fit["valley_height"],
            break_height=fit["break_height"],
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


__all__ = ["CivilconUBeamDimensions", "CivilconUBeamSection"]
