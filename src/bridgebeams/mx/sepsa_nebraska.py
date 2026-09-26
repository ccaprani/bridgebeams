"""SEPSA "Trabe Nebraska" I-girders (producer profiles, not the US NU girder).

Source: Grupo Constructor SEPSA, *Catálogo de piezas SEPSA V-05 27-21*,
PDF page 5. Seven types (135, 180, 200 alero especial, 210, 220, 240,
240 base especial), each with an 18 cm or 20 cm web (135: 18 cm only).
The 20 cm web widens every horizontal chord by 2 cm (bottom 100→102,
top 125→127 / 184→186, 45→47); the published area differences
(2 cm × depth for every type) confirm this. Drawings are in centimetres;
this module returns millimetres with origin at mid-soffit, y upwards.

Printed: depth, the vertical chain (10 + 22 + web + 27 + 15; alero
especial 2 + 8.5 + 2.5 + 20 top; base especial 25 bottom edge), widths
41/18/41 and 27.5/45/27.5, R20 web fillets and R5 bottom-flange corner.
Not printed and therefore **estimated** (provenance ``"estimate"``): the
top-flange soffit break point, the flange-tip radius (R10; alero
especial R8.5 below a 2 cm vertical edge) and the 2 × 2 cm soffit chamfer
of the base especial type, all taken from the catalogue's uniform-scale
vector drawing, and the convention that every fillet is tangent to both
adjoining straight edges. The 45 cm width is taken as the chord at the
lower R20 tangent points. Only areas (m², 4 d.p.) are published.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon
from shapely.geometry.polygon import orient

from bridgebeams._geometry import geometry_from_polygon

from ._arcs import arc, fillet, intersect, unit

ARC_SEGMENTS = 48


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.mx")
        .joinpath("data/sepsa_nebraska.json")
        .read_text(encoding="utf-8")
    )


def _tangent_from_point(p, centre, radius, pick):
    """Directions from p of the two tangents to a circle; ``pick`` chooses."""
    dx, dy = centre[0] - p[0], centre[1] - p[1]
    dist = math.hypot(dx, dy)
    base = math.atan2(dy, dx)
    off = math.asin(radius / dist)
    dirs = [(math.cos(base + s * off), math.sin(base + s * off)) for s in (1, -1)]
    return pick(dirs)


@dataclass(frozen=True)
class SepsaNebraskaDimensions:
    """Dimensions in centimetres (catalogue units) for the 18 cm web.

    ``widen`` (cm) is added to every half-width: 0 for the 18 cm web,
    1 for the 20 cm web.
    """

    type_name: str
    depth: float
    web_width: float
    top_width: float
    bottom_width: float
    bottom_edge: float
    bottom_web_start: float
    top_web_end_from_top: float
    tip_edge: float
    tip_radius: float
    fillet_radius: float = 20.0
    bottom_corner_radius: float = 5.0
    lower_tangent_chord: float = 45.0
    soffit_chamfer: float = 0.0
    widen: float = 0.0

    def right_half_cm(self) -> list[tuple[float, float]]:
        H = self.depth
        tw = self.web_width / 2
        xb = self.bottom_width / 2
        xt = self.top_width / 2
        R = self.fillet_radius
        # Lower web fillet and bottom-flange taper line.
        c_lo = (tw + R, self.bottom_web_start)
        tx = self.lower_tangent_chord / 2
        ty = c_lo[1] - math.sqrt(R * R - (c_lo[0] - tx) ** 2)
        t_dir = unit((c_lo[1] - ty, -(c_lo[0] - tx)))  # outward, downward
        corner = intersect((tx, ty), t_dir, (xb, 0.0), (0.0, 1.0))
        pts = []
        c = self.soffit_chamfer
        pts += [(xb - c, 0.0), (xb, c)] if c else [(xb, 0.0)]
        pts += fillet(corner, (0.0, -1.0), (-t_dir[0], -t_dir[1]), self.bottom_corner_radius, ARC_SEGMENTS)
        pts += arc(c_lo, R, (tx, ty), (tw, c_lo[1]), ARC_SEGMENTS)
        # Upper web fillet tangent to the web and to the flange soffit line
        # drawn from the end of the tip arc.
        c_up = (tw + R, H - self.top_web_end_from_top)
        tip_c = (xt - self.tip_radius, H - self.tip_edge)
        p_tip = (tip_c[0], tip_c[1] - self.tip_radius)
        d = _tangent_from_point(p_tip, c_up, R, lambda ds: min(ds, key=lambda v: abs(v[1])))
        foot = ((c_up[0] - p_tip[0]) * d[0] + (c_up[1] - p_tip[1]) * d[1])
        t_up = (p_tip[0] + d[0] * foot, p_tip[1] + d[1] * foot)
        pts += arc(c_up, R, (tw, c_up[1]), t_up, ARC_SEGMENTS)
        pts += arc(tip_c, self.tip_radius, p_tip, (xt, tip_c[1]), ARC_SEGMENTS)
        if self.tip_edge:
            pts.append((xt, H))
        return [(x + self.widen if x > 0 else x, y) for x, y in pts]


class SepsaNebraskaSection:
    """SEPSA Nebraska girder; size ``"<type>-W18"`` or ``"<type>-W20"``.

    >>> from bridgebeams.mx import SepsaNebraskaSection
    >>> SepsaNebraskaSection("180-W20").polygon.bounds
    (-635.0, 0.0, 635.0, 1800.0)
    """

    SIZES = (
        "135-W18",
        "180-W18",
        "180-W20",
        "200-ALERO-ESPECIAL-W18",
        "200-ALERO-ESPECIAL-W20",
        "210-W18",
        "210-W20",
        "220-W18",
        "220-W20",
        "240-W18",
        "240-W20",
        "240-BASE-ESPECIAL-W18",
        "240-BASE-ESPECIAL-W20",
    )

    def __init__(self, size: str = "180-W18"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        type_name, web = size.rsplit("-W", 1)
        row = next(t for t in data["types"] if t["type"] == type_name)
        self.size = size
        self.published = row
        self.published_area_m2 = row["area_m2"][f"web_{web}"]
        self.provenance = row["provenance"]
        self.source_status = data["source_status"]
        self.dimensions = SepsaNebraskaDimensions(
            type_name=type_name,
            depth=row["depth_cm"],
            web_width=18.0,
            top_width=row["top_width_web18_cm"],
            bottom_width=100.0,
            bottom_edge=row["bottom_edge_cm"],
            bottom_web_start=row["bottom_edge_cm"] + 27.0,
            top_web_end_from_top=row["top_web_end_from_top_cm"],
            tip_edge=row["tip_vertical_edge_cm"],
            tip_radius=row["tip_radius_cm"],
            soffit_chamfer=row.get("soffit_chamfer_cm", 0.0),
            widen=0.0 if web == "18" else 1.0,
        )

    @property
    def polygon(self) -> Polygon:
        right = [(10.0 * x, 10.0 * y) for x, y in self.dimensions.right_half_cm()]
        if right[0][0] > 0:
            right = [(0.0, 0.0)] + right
        right = right + [(0.0, 10.0 * self.dimensions.depth)]
        left = [(-x, y) for x, y in reversed(right[1:-1])]
        return orient(Polygon(right + left), sign=1.0)

    @property
    def geometry(self):
        """The gross section as a sectionproperties Geometry, in millimetres."""
        return geometry_from_polygon(self.polygon)


__all__ = ["SepsaNebraskaDimensions", "SepsaNebraskaSection"]
