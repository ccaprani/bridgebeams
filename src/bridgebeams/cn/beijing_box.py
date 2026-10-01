"""Beijing 20BGQL2 single-track urban-rail precast box girder, midspan I–I.

Source: 北京市工程建设标准设计文件 / 轨道交通通用图集 20BGQL2
《时速100公里及以下城市轨道交通后张法预应力混凝土单线预制箱梁》
(Beijing Municipal Commission of Planning and Natural Resources), PDF
page 23 = printed page 15 (预制箱梁构造图（二）, section I–I); PDF page 22
(printed 14) confirms the 200 + 150 + 1450 = 1800 mm depth chain.

All dimensions are printed in millimetres. Width 2 × (2600 + a) with the
deck-width parameter ``a`` = 0–300 mm (Note 1). One section serves the
25, 30 and 32 m spans. Origin at mid-soffit, y upwards; the single void
is an interior ring.

Conventions (stated, not fitted): the two R50 corners per side (web–soffit
and web–wing) are exact tangent arcs; the A-detail drip groove (滴水檐, R20,
centred 150 mm from the wing tip on the wing soffit) is cut as a full R20
circle centred on the soffit surface (``drip_groove=False`` omits it).
Vent holes, the ø600 access hole, drain holes and the end thickening
(sections II–II/III–III) are not part of the midspan gross section.
No section properties are published; checks are analytic only.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from shapely.geometry import Point, Polygon
from shapely.geometry.polygon import orient

from bridgebeams._geometry import geometry_from_polygon

ARC_SEGMENTS = 32


def _fillet(corner, d_in, d_out, radius, n=ARC_SEGMENTS):
    ux, uy = d_in
    lu = math.hypot(ux, uy)
    ux, uy = ux / lu, uy / lu
    vx, vy = d_out
    lv = math.hypot(vx, vy)
    vx, vy = vx / lv, vy / lv
    theta = math.acos(max(-1.0, min(1.0, ux * vx + uy * vy)))
    t = radius / math.tan(theta / 2)
    p = (corner[0] + ux * t, corner[1] + uy * t)
    q = (corner[0] + vx * t, corner[1] + vy * t)
    bx, by = ux + vx, uy + vy
    lb = math.hypot(bx, by)
    dist = radius / math.sin(theta / 2)
    c = (corner[0] + bx / lb * dist, corner[1] + by / lb * dist)
    a0 = math.atan2(p[1] - c[1], p[0] - c[0])
    a1 = math.atan2(q[1] - c[1], q[0] - c[0])
    sweep = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
    return [(c[0] + radius * math.cos(a0 + sweep * i / n), c[1] + radius * math.sin(a0 + sweep * i / n)) for i in range(n + 1)]


@dataclass(frozen=True)
class Beijing20bgql2BoxDimensions:
    """Printed section I–I dimensions (mm)."""

    a: float = 0.0
    depth: float = 1800.0
    wing_web_run: float = 1400.0
    web_run: float = 250.0
    web_height: float = 1450.0
    soffit_half_width: float = 950.0
    wing_tip_thickness: float = 200.0
    wing_root_thickness: float = 350.0
    bottom_slab: float = 220.0
    void_height: float = 1380.0
    void_half_width_top_haunch_end: float = 916.0
    void_half_width_bottom_haunch_end: float = 730.0
    top_haunch: tuple[float, float] = (450.0, 150.0)
    bottom_haunch: tuple[float, float] = (300.0, 150.0)
    web_normal_thickness: float = 280.0
    corner_radius: float = 50.0
    drip_radius: float = 20.0
    drip_offset: float = 150.0

    @property
    def half_width(self) -> float:
        return 2600.0 + self.a

    def outer_right(self) -> list[tuple[float, float]]:
        x0, h = self.soffit_half_width, self.web_height
        x1 = x0 + self.web_run  # 1200
        xw = x1 + self.wing_web_run  # 2600
        yw = self.depth - self.wing_tip_thickness  # 1600
        r = self.corner_radius
        pts = [(0.0, 0.0)]
        pts += _fillet((x0, 0.0), (-1.0, 0.0), (self.web_run, h), r)
        pts += _fillet((x1, h), (-self.web_run, -h), (xw - x1, yw - h), r)
        pts += [(xw, yw), (self.half_width, yw), (self.half_width, self.depth), (0.0, self.depth)]
        return pts

    def void_right(self) -> list[tuple[float, float]]:
        y0 = self.bottom_slab
        y1 = y0 + self.void_height
        xb, xt = self.void_half_width_bottom_haunch_end, self.void_half_width_top_haunch_end
        hb, ht = self.bottom_haunch, self.top_haunch
        return [(0.0, y0), (xb - hb[0], y0), (xb, y0 + hb[1]), (xt, y1 - ht[1]), (xt - ht[0], y1), (0.0, y1)]

    def wing_soffit_y(self, x: float) -> float:
        x1 = self.soffit_half_width + self.web_run
        xw = x1 + self.wing_web_run
        yw = self.depth - self.wing_tip_thickness
        if x >= xw:
            return yw
        return self.web_height + (yw - self.web_height) * (x - x1) / (xw - x1)


def _mirror(right):
    ring = list(right) + [(-x, y) for x, y in reversed(right)]
    out = []
    for p in ring:
        if not out or math.hypot(p[0] - out[-1][0], p[1] - out[-1][1]) > 1e-9:
            out.append(p)
    if math.hypot(out[0][0] - out[-1][0], out[0][1] - out[-1][1]) < 1e-9:
        out.pop()
    return out


class Beijing20bgql2BoxSection:
    """Midspan section I–I of the 20BGQL2 single-track box girder.

    ``SIZES`` holds the two ends of the printed deck-width range
    (``"a=0"``, ``"a=300"``); any ``a`` in 0–300 mm may be passed instead.

    >>> from bridgebeams.cn import Beijing20bgql2BoxSection
    >>> Beijing20bgql2BoxSection("a=300").polygon.bounds
    (-2900.0, 0.0, 2900.0, 1800.0)
    """

    SIZES = ("a=0", "a=300")
    provenance = "transcribed-with-convention"
    source_status = "Beijing urban-rail standard atlas 20BGQL2 (北京市工程建设标准设计文件)"

    def __init__(self, size: str = "a=0", a: float | None = None, drip_groove: bool = True):
        """``a`` (mm), when given, overrides ``size``."""
        if a is None:
            if size not in self.SIZES:
                raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
            a = float(size.split("=")[1])
        if not 0.0 <= float(a) <= 300.0:
            raise ValueError("a must be within 0–300 mm (20BGQL2 Note 1)")
        self.a = float(a)
        self.size = f"a={self.a:g}"
        self.drip_groove = drip_groove
        self.dimensions = Beijing20bgql2BoxDimensions(a=self.a)

    @property
    def polygon(self) -> Polygon:
        d = self.dimensions
        poly = Polygon(_mirror(d.outer_right()), [_mirror(d.void_right())])
        if self.drip_groove:
            x = d.half_width - d.drip_offset
            y = d.wing_soffit_y(x)
            for sx in (1, -1):
                poly = poly.difference(Point(sx * x, y).buffer(d.drip_radius, quad_segs=16))
        return orient(poly, sign=1.0)

    @property
    def geometry(self):
        """The gross section as a sectionproperties Geometry, in millimetres."""
        return geometry_from_polygon(self.polygon)


__all__ = ["Beijing20bgql2BoxDimensions", "Beijing20bgql2BoxSection"]
