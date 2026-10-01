"""Civilcon Y1–Y8 gross sections using the 40 mm in-situ-slab ledge.

PPBY page 1 dimensions the bottom flange, R100 web junction and eight
rounded top widths. Colin Caprani's 2026-09-22 visual review confirms the
40 mm wide, 50 mm deep notch on each side of those top widths. The separate
70 mm topdeck detail is not this outline. Rounded drawing dimensions produce small property residuals; Y1 additionally
has an unresolved modulus discrepancy (Zt +0.34%, Zb +0.17%). This profile
is not fitted to the published properties.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon, polygon_from_half_profile


def _load_data() -> dict:
    return json.loads(resources.files("bridgebeams.za.data").joinpath("civilcon_y_beams.json").read_text())


@dataclass(frozen=True)
class CivilconYBeamDimensions:
    """Millimetres; origin at soffit centre and y positive upwards.

    ``top_width`` is the central raised face between the two notches.
    The maximum width at the ledges is ``top_width + 80``. The R100
    fillet is tangent to the two straight faces meeting theoretically at
    (100, 379) on the right side; 379 = 25 + 177 + 177.
    """

    depth: float
    top_width: float
    notch_width: float = 40.0
    notch_depth: float = 50.0
    junction_radius: float = 100.0

    @property
    def outline(self) -> list[tuple[float, float]]:
        """Right side from soffit to top, with a 64-segment circular fillet."""
        a = (370.0, 202.0)
        corner = (100.0, 379.0)
        b = (self.top_width / 2 + self.notch_width, self.depth - self.notch_depth)
        def unit(p):
            dx, dy = p[0] - corner[0], p[1] - corner[1]
            length = math.hypot(dx, dy)
            return dx / length, dy / length
        u, v = unit(a), unit(b)
        angle = math.acos(u[0] * v[0] + u[1] * v[1])
        bx, by = u[0] + v[0], u[1] + v[1]
        scale = self.junction_radius / math.sin(angle / 2) / math.hypot(bx, by)
        centre = (corner[0] + bx * scale, corner[1] + by * scale)
        tangent_distance = self.junction_radius / math.tan(angle / 2)
        p = (corner[0] + u[0] * tangent_distance, corner[1] + u[1] * tangent_distance)
        q = (corner[0] + v[0] * tangent_distance, corner[1] + v[1] * tangent_distance)
        start = math.atan2(p[1] - centre[1], p[0] - centre[0])
        end = math.atan2(q[1] - centre[1], q[0] - centre[0])
        sweep = (end - start + math.pi) % (2 * math.pi) - math.pi
        arc = [
            (centre[0] + self.junction_radius * math.cos(start + sweep * i / 64),
             centre[1] + self.junction_radius * math.sin(start + sweep * i / 64))
            for i in range(65)
        ]
        return [(350.0, 0.0), (375.0, 25.0), a, *arc, b,
                (self.top_width / 2, self.depth - self.notch_depth),
                (self.top_width / 2, self.depth)]


class CivilconYBeamSection:
    """Source-dimensioned Civilcon Y1–Y8, 40 mm ledge arrangement only."""

    SIZES = tuple(f"Y{i}" for i in range(1, 9))

    # 40 x 50 mm ledge confirmed by reviewer reading; R100 fillet polygonised.
    provenance = "transcribed-with-convention"
    source_status = "producer catalogue (Civilcon PPBY)"

    def __init__(self, size: str = "Y4"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        row = next(r for r in _load_data()["published_properties"] if r["section"] == size)
        self.size = size
        self.published = row
        self.dimensions = CivilconYBeamDimensions(row["depth"], row["top_width_between_notches"])

    @property
    def polygon(self) -> Polygon:
        return polygon_from_half_profile(self.dimensions.outline)

    @property
    def geometry(self):
        """Return the gross concrete ``sectionproperties`` geometry."""
        return geometry_from_polygon(self.polygon)


__all__ = ["CivilconYBeamDimensions", "CivilconYBeamSection"]
