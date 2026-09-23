"""SW Umwelttechnik Magyarország SHP-22 / SHP-32 / SHP-40 prestressed bridge beams.

Source: "SHP Hídgerenda család" product sheet, pp 2–4 (cm; see
data/r2_sw_shp.json). Solid trapezoidal beams 60 cm wide at the top with
2 cm lowered joint ledges; the drawn loops are reinforcement, not voids.
Millimetres, origin at mid-soffit, y upwards.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon
from shapely.geometry.polygon import orient

from bridgebeams._geometry import geometry_from_polygon

from ._fillet import fillet_polyline


def _load_data() -> dict:
    return json.loads(resources.files("bridgebeams.hu").joinpath("data/r2_sw_shp.json").read_text(encoding="utf-8"))


def _round_radius(a, b, c, tangent: float) -> float:
    """Radius of the tangent round at ``b`` whose tangent points lie ``tangent`` from ``b``."""
    u = (a[0] - b[0], a[1] - b[1])
    v = (c[0] - b[0], c[1] - b[1])
    cosang = (u[0] * v[0] + u[1] * v[1]) / (math.hypot(*u) * math.hypot(*v))
    return tangent * math.tan(math.acos(cosang) / 2)


@dataclass(frozen=True)
class SwShpDimensions:
    """Printed dimensions (mm)."""

    depth: float
    top_width: float = 600.0
    top_central: float = 510.0
    ledge_depth: float = 20.0
    riser_offset: float = 5.0
    inset: float = 40.0
    bottom_tangent: float = 15.0
    edge_tangent: float = 10.0

    @property
    def soffit(self) -> float:
        return self.top_width - 2 * self.inset

    @property
    def half_profile(self) -> list[tuple[float, float]]:
        h, b = self.depth, self.top_width / 2
        corner = (b - self.inset, 0.0)
        edge = (b, h - self.ledge_depth)
        ledge_in = (self.top_central / 2 + self.riser_offset, h - self.ledge_depth)
        start = (0.0, 0.0)
        r_bot = _round_radius(start, corner, edge, self.bottom_tangent)
        r_top = _round_radius(corner, edge, ledge_in, self.edge_tangent)
        return fillet_polyline([
            (0.0, 0.0, 0.0), (corner[0], corner[1], r_bot), (edge[0], edge[1], r_top),
            (ledge_in[0], ledge_in[1], 0.0), (self.top_central / 2, h, 0.0), (0.0, h, 0.0)], segments=8)


class SwShpSection:
    """SHP bridge beam ``SHP-22``, ``SHP-32`` or ``SHP-40`` (solid)."""

    SIZES = ("SHP-22", "SHP-32", "SHP-40")

    def __init__(self, size: str = "SHP-32"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        pr = data["printed"][size]
        self.size = size
        self.published = pr
        self.mass_per_metre_t = data["mass_per_metre_t"][size]
        self.provenance = data["provenance"][size]
        self.source_status = data["source_status"]
        cm = 10.0
        self.dimensions = SwShpDimensions(
            depth=pr["H"] * cm, top_width=pr["top_width"] * cm, top_central=pr["top_central"] * cm,
            ledge_depth=pr["ledge_depth"] * cm, riser_offset=pr["riser_offset"] * cm,
            inset=pr["inset"] * cm, bottom_tangent=pr["bottom_tangent"] * cm, edge_tangent=pr["edge_round"] * cm,
        )

    @property
    def polygon(self) -> Polygon:
        right = [p for p in self.dimensions.half_profile if p[0] > 1e-9]
        return orient(Polygon(right + [(-x, y) for x, y in reversed(right)]), 1.0)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = ["SwShpDimensions", "SwShpSection"]
