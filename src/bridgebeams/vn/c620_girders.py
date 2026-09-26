"""Vietnamese precast prestressed girders of Bê tông 620 Châu Thới.

Producer drawings published on https://620chauthoi.com (product pages
"Dầm I" and "Dầm T"): I 33 m (1400 deep), I 24.54 m (1143), I 18.6 m (700),
T 18.6 m cải tiến (950 at midspan) and T ngược 20 m inverted-T (750). All
dimensions are printed in millimetres. Midspan gross concrete sections only;
end blocks, holes and reinforcement are excluded. Origin at mid-soffit,
y upwards. These are producer profiles, not Bộ GTVT standard drawings, and
no identity with similarly sized foreign sections is implied.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon
from shapely.geometry.polygon import orient

from bridgebeams._geometry import geometry_from_polygon, polygon_from_half_profile

ARC_SEGMENTS = 24


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.vn")
        .joinpath("data/c620_girders.json")
        .read_text(encoding="utf-8")
    )


def _fillet(corner, d_in, d_out, radius, n=ARC_SEGMENTS):
    """Tangent arc replacing ``corner`` between incoming/outgoing directions."""
    ux, uy = d_in
    lu = math.hypot(ux, uy)
    ux, uy = ux / lu, uy / lu
    vx, vy = d_out
    lv = math.hypot(vx, vy)
    vx, vy = vx / lv, vy / lv
    # directions pointing away from the corner along each leg
    ax, ay = -ux, -uy
    theta = math.acos(max(-1.0, min(1.0, ax * vx + ay * vy)))
    t = radius / math.tan(theta / 2)
    p = (corner[0] + ax * t, corner[1] + ay * t)
    q = (corner[0] + vx * t, corner[1] + vy * t)
    bx, by = ax + vx, ay + vy
    lb = math.hypot(bx, by)
    dist = radius / math.sin(theta / 2)
    c = (corner[0] + bx / lb * dist, corner[1] + by / lb * dist)
    a0 = math.atan2(p[1] - c[1], p[0] - c[0])
    a1 = math.atan2(q[1] - c[1], q[0] - c[0])
    sweep = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
    return [(c[0] + radius * math.cos(a0 + sweep * i / n), c[1] + radius * math.sin(a0 + sweep * i / n))
            for i in range(n + 1)]


@dataclass(frozen=True)
class Vn620GirderDimensions:
    """Printed midspan dimensions (mm); unused fields are zero."""

    depth: float
    top_width: float = 0.0
    top_edge: float = 0.0
    top_haunch: float = 0.0
    web: float = 0.0
    web_height: float = 0.0
    bottom_splay: float = 0.0
    bottom_edge: float = 0.0
    bottom_width: float = 0.0
    chamfer: float = 0.0
    flange_width: float = 0.0
    top_rebate: float = 0.0
    flange_edge: float = 0.0
    block_width: float = 0.0
    block_depth: float = 0.0
    soffit_width: float = 0.0
    web_taper_h_per_v: float = 0.0
    fillet_radius: float = 0.0
    flange_rise: float = 0.0
    fillet_zone: float = 0.0


def _i_right(d: Vn620GirderDimensions) -> list[tuple[float, float]]:
    b, w, c = d.bottom_width / 2, d.web / 2, d.chamfer
    y1 = d.bottom_edge
    y2 = y1 + d.bottom_splay
    y3 = y2 + d.web_height
    y4 = y3 + d.top_haunch
    if d.flange_width:  # I18.6: 430 flange with 20 x 50 top rebates to a 390 top
        f = d.flange_width / 2
        y1 = c + d.bottom_edge
        y2 = y1 + d.bottom_splay
        y3 = y2 + d.web_height
        y4 = y3 + d.top_haunch
        y5 = y4 + d.flange_edge
        return [(b - c, 0.0), (b, c), (b, y1), (w, y2), (w, y3), (f, y4), (f, y5),
                (d.top_width / 2, y5), (d.top_width / 2, d.depth)]
    return [(b - c, 0.0), (b, c), (b, y1), (w, y2), (w, y3),
            (d.top_width / 2, y4), (d.top_width / 2, d.depth)]


def _t186_right(d: Vn620GirderDimensions) -> list[tuple[float, float]]:
    """Tapered web (1:12 per face) with an R130 arc tangent to the web and
    ending at the upper block's bottom outer corner."""
    k = d.web_taper_h_per_v
    x0 = d.soffit_width / 2
    yb = d.depth - d.block_depth
    xb = d.block_width / 2
    r = d.fillet_radius
    nrm = (1.0 / math.hypot(1.0, k), -k / math.hypot(1.0, k))  # outward normal

    def centre(t):
        return (x0 + k * t + r * nrm[0], t + r * nrm[1])

    def f(t):
        cx, cy = centre(t)
        return math.hypot(cx - xb, cy - yb) - r

    lo, hi = 0.0, yb
    for _ in range(200):  # f(lo) > 0, f(hi) < 0
        mid = (lo + hi) / 2
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
    t = (lo + hi) / 2
    cx, cy = centre(t)
    tx, ty = x0 + k * t, t
    a0 = math.atan2(ty - cy, tx - cx)
    a1 = math.atan2(yb - cy, xb - cx)
    sweep = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
    arc = [(cx + r * math.cos(a0 + sweep * i / ARC_SEGMENTS), cy + r * math.sin(a0 + sweep * i / ARC_SEGMENTS))
           for i in range(ARC_SEGMENTS + 1)]
    arc[-1] = (xb, yb)
    yr = d.depth - d.top_rebate
    return [(x0, 0.0)] + arc + [(xb, yr), (d.top_width / 2, yr), (d.top_width / 2, d.depth)]


def _tn_right(d: Vn620GirderDimensions) -> list[tuple[float, float]]:
    b, w, c = d.bottom_width / 2, d.web / 2, d.chamfer
    ye = d.bottom_edge
    yc = ye + d.flange_rise  # theoretical web / flange-top intersection
    yw = yc + d.fillet_zone + d.web_height
    yh = yw + d.top_haunch
    yf = yh + d.flange_edge
    arc = _fillet((w, yc), (w - b, yc - ye), (0.0, 1.0), d.fillet_radius)
    return ([(b - c, 0.0), (b, c), (b, ye)] + arc +
            [(w, yw), (d.flange_width / 2, yh), (d.flange_width / 2, yf),
             (d.top_width / 2, yf), (d.top_width / 2, d.depth)])


class Vn620GirderSection:
    """620 Châu Thới girder: ``"I33"``, ``"I24.54"``, ``"I18.6"``,
    ``"T18.6"`` (T cải tiến, midspan) or ``"TN20"`` (T ngược 20 m).

    Examples
    --------
    >>> Vn620GirderSection("I33").dimensions.depth
    1400.0
    """

    SIZES = ("I33", "I24.54", "I18.6", "T18.6", "TN20")
    source_status = "producer drawing (620 Châu Thới website, 2019 uploads)"

    def __init__(self, size: str = "I33"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        row = _load_data()["sections"][size]
        self.size = size
        self.published = row
        self.provenance = row["provenance"]
        self.dimensions = Vn620GirderDimensions(
            **{k: float(v) for k, v in row["dimensions_mm"].items()}
        )

    @property
    def polygon(self) -> Polygon:
        if self.size == "T18.6":
            right = _t186_right(self.dimensions)
        elif self.size == "TN20":
            right = _tn_right(self.dimensions)
        else:
            right = _i_right(self.dimensions)
        return orient(polygon_from_half_profile(right), sign=1.0)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = ["Vn620GirderDimensions", "Vn620GirderSection"]
