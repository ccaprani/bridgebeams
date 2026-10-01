"""Ontario MTO prestressed NU girders NU900-NU2400 (SS107-16 to SS107-23).

All eight June 2025 Ontario standard drawings (SS107-16 to SS107-23; PDF
page 1 of each, "TYPICAL SECTION") show one common gross outline. Only the
web height changes. The printed callouts are: 1235 mm top width;
65 mm flange-tip edge; 45 mm taper to the web face; web height D - 385 mm;
160 mm web; 140 mm bottom taper from the web face; 135 mm bottom edge;
985 mm bottom width; R200 web fillets; R50 flange-tip fillets; and a 20 mm
soffit chamfer. The July 2023 DRAFT sheets in ``ca_mto_nu.pdf`` carry
identical callouts. Each fillet is reconstructed as the unique circular arc
tangent to the two dimensioned straight lines meeting at the printed
theoretical corner. The arc is tessellated with ``arc_segments`` chords
(default 32). The chamfer is taken as 20 x 20 mm at 45 degrees. The
top-flange upper corners are square, as drawn. Holes, strands,
reinforcement and end details are excluded. The shape is an Ontario
provincial standard, not the US Nebraska NU metric shape. No section
property table is published on these sheets, so the tests use analytic
checks only.

Coordinates are in millimetres, with the origin at mid-soffit and y upwards.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon
from shapely.geometry.polygon import orient

from bridgebeams._geometry import geometry_from_polygon, polygon_from_half_profile


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.ca").joinpath("data/mto_nu_girders.json").read_text()
    )


def fillet(prev_pt, corner, next_pt, radius, segments):
    """Tessellated arc tangent to lines corner->prev_pt and corner->next_pt.

    Returns the points from the tangent point on the incoming line to the
    tangent point on the outgoing line, inclusive.
    """
    def unit(p):
        dx, dy = p[0] - corner[0], p[1] - corner[1]
        n = math.hypot(dx, dy)
        return dx / n, dy / n

    u, v = unit(prev_pt), unit(next_pt)
    angle = math.acos(max(-1.0, min(1.0, u[0] * v[0] + u[1] * v[1])))
    t = radius / math.tan(angle / 2)
    bx, by = u[0] + v[0], u[1] + v[1]
    h = radius / math.sin(angle / 2)
    bn = math.hypot(bx, by)
    centre = (corner[0] + bx / bn * h, corner[1] + by / bn * h)
    p = (corner[0] + u[0] * t, corner[1] + u[1] * t)
    q = (corner[0] + v[0] * t, corner[1] + v[1] * t)
    a0 = math.atan2(p[1] - centre[1], p[0] - centre[0])
    a1 = math.atan2(q[1] - centre[1], q[0] - centre[0])
    sweep = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
    return [(centre[0] + radius * math.cos(a0 + sweep * i / segments),
             centre[1] + radius * math.sin(a0 + sweep * i / segments))
            for i in range(segments + 1)]


@dataclass(frozen=True)
class CaMtoNuGirderDimensions:
    """Source dimensions (mm). ``depth`` is the only size-dependent value."""

    depth: float
    top_width: float = 1235.0
    top_edge: float = 65.0
    top_taper: float = 45.0
    web_width: float = 160.0
    bottom_taper: float = 140.0
    bottom_edge: float = 135.0
    bottom_width: float = 985.0
    web_radius: float = 200.0
    tip_radius: float = 50.0
    soffit_chamfer: float = 20.0

    @property
    def web_height(self) -> float:
        return self.depth - self.top_edge - self.top_taper - self.bottom_taper - self.bottom_edge

    def corners(self) -> list[tuple[float, float]]:
        """Right-half theoretical (unfilleted) corner chain, soffit to top."""
        d, c = self.depth, self.soffit_chamfer
        bw, tw, w = self.bottom_width / 2, self.top_width / 2, self.web_width / 2
        yb = self.bottom_edge
        yw0 = yb + self.bottom_taper
        yw1 = d - self.top_edge - self.top_taper
        yt = d - self.top_edge
        return [(0.0, 0.0), (bw - c, 0.0), (bw, c), (bw, yb), (w, yw0),
                (w, yw1), (tw, yt), (tw, d), (0.0, d)]

    def outline(self, arc_segments: int = 32) -> list[tuple[float, float]]:
        """Right-half outline with tessellated R50/R200 fillets."""
        k = self.corners()
        radii = {3: self.tip_radius, 4: self.web_radius,
                 5: self.web_radius, 6: self.tip_radius}
        pts: list[tuple[float, float]] = []
        for i, p in enumerate(k):
            if i in radii:
                pts.extend(fillet(k[i - 1], p, k[i + 1], radii[i], arc_segments))
            else:
                pts.append(p)
        return pts


class CaMtoNuGirderSection:
    """Ontario MTO NU girder, as drawn on SS107-16 to SS107-23 (June 2025)."""

    SIZES = ("NU900", "NU1200", "NU1400", "NU1600", "NU1800", "NU1900",
             "NU2000", "NU2400")

    def __init__(self, size: str = "NU1200", arc_segments: int = 32):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        if isinstance(arc_segments, bool) or not isinstance(arc_segments, int) or arc_segments < 4:
            raise ValueError("arc_segments must be an integer >= 4")
        data = _load_data()
        row = data["sizes"][size]
        self.size = size
        self.arc_segments = arc_segments
        self.drawing = row["drawing"]
        self.provenance = row["provenance"]
        self.source_status = row["source_status"]
        self.dimensions = CaMtoNuGirderDimensions(depth=float(row["depth_mm"]))

    @property
    def polygon(self) -> Polygon:
        right = self.dimensions.outline(self.arc_segments)
        # drop the centreline points; polygon_from_half_profile mirrors them
        return orient(polygon_from_half_profile(right[1:-1]), sign=1)

    @property
    def geometry(self):
        """Return the gross concrete ``sectionproperties`` geometry."""
        return geometry_from_polygon(self.polygon)


__all__ = ["CaMtoNuGirderDimensions", "CaMtoNuGirderSection"]
