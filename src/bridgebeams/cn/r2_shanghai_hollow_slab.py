"""Shanghai pretensioned prestressed hollow slabs (DBJT08-101 revision draft).

Source: 上海市建筑标准设计《先张法预应力混凝土空心板（桥梁）》
（征求意见稿）DBJT08-101-20xx, 图集号 2021沪G1005 (consultation draft,
2021; the issued edition is DBJT 08-101-2024, not held). Vector CAD
drawings, dimensions in millimetres.

Two families, each with middle (中板) and edge (边板) units:

- :class:`ShanghaiRigidHollowSlabSection` — 第一分册 刚接空心板, midspan
  section B-B, PDF pp 37-80. Depths 550/650/850/950 serve spans
  10/13/16-18/20-22 m. Top follows the printed 2 % crossfall, so the
  drawn section is asymmetric. R30 reentrant fillets are exact arcs; the
  edge-slab drip groove is omitted. No property table: analytic checks.
- :class:`ShanghaiHingedHollowSlabSection` — 第二分册 铰接空心板, PDF pp
  140-149. Depths 520/620/820/900. All eight outlines reproduce the
  published gross A, centroid and I (PDF p130, 表1 空心板毛截面特性)
  to within 0.04 %.

Origin at the middle of the soffit, y upwards. Voids are polygon
interiors (``arc_points`` vertices per half circle).
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
        resources.files("bridgebeams.cn")
        .joinpath("data/r2_shanghai_hollow_slabs.json")
        .read_text(encoding="utf-8")
    )


def _void(cx: float, bottom: float, width: float, height: float, n: int) -> list[tuple[float, float]]:
    """Circle (height == width) or round-ended slot, anticlockwise."""
    r = width / 2.0
    lower_c = bottom + r
    upper_c = bottom + height - r
    pts = []
    for i in range(n + 1):  # lower semicircle, from left (pi) to right (2 pi)
        a = math.pi + math.pi * i / n
        pts.append((cx + r * math.cos(a), lower_c + r * math.sin(a)))
    for i in range(n + 1):  # upper semicircle, right (0) to left (pi)
        a = math.pi * i / n
        pts.append((cx + r * math.cos(a), upper_c + r * math.sin(a)))
    out = []
    for p in pts:
        if not out or math.hypot(p[0] - out[-1][0], p[1] - out[-1][1]) > 1e-9:
            out.append(p)
    if math.hypot(out[0][0] - out[-1][0], out[0][1] - out[-1][1]) < 1e-9:
        out.pop()
    return out


def _arc(centre, radius, a0, a1, n):
    return [
        (centre[0] + radius * math.cos(a0 + (a1 - a0) * i / n),
         centre[1] + radius * math.sin(a0 + (a1 - a0) * i / n))
        for i in range(n + 1)
    ]


@dataclass(frozen=True)
class ShanghaiRigidHollowSlabDimensions:
    """Midspan section B-B of a 刚接 (rigid-jointed) slab, mm."""

    depth: float
    unit: str  # "middle" or "edge"
    void_height: float  # 360 circle, 650 round-ended slot
    void_bottom: float
    void_width: float = 360.0
    bottom_width: float = 1100.0
    ledge_width: float = 1300.0  # 50 + 1200 + 50 at the ledge corners
    top_surface_width: float = 1200.0
    overhang_depth: float = 180.0
    fillet_radius: float = 30.0
    crossfall: float = 0.02
    void_centre_offset: float = 225.0
    cantilever: float = 300.0  # edge slab only
    cantilever_tip: float = 200.0
    cantilever_rise: float = 50.0

    def top_y(self, x: float) -> float:
        return self.depth + self.crossfall * x

    @property
    def ledge_heights(self) -> tuple[float, float]:
        """Left and right ledge heights (printed e.g. 357/383 for 550)."""
        xl = self.ledge_width / 2.0
        return (self.top_y(-xl) - self.overhang_depth, self.top_y(xl) - self.overhang_depth)

    def outline(self, n_arc: int = 8) -> list[tuple[float, float]]:
        b = self.bottom_width / 2.0
        xl = self.ledge_width / 2.0
        xt = self.top_surface_width / 2.0
        r = self.fillet_radius
        yl, yr = self.ledge_heights
        pts = [(-b, 0.0), (b, 0.0)]
        # right web up to the R30 fillet, then ledge and overhang face
        pts += _arc((b + r, yr - r), r, math.pi, math.pi / 2.0, n_arc)
        pts += [(xl, yr), (xt, self.top_y(xt))]
        if self.unit == "middle":
            pts += [(-xt, self.top_y(-xt)), (-xl, yl)]
            pts += _arc((-b - r, yl - r), r, math.pi / 2.0, 0.0, n_arc)
        else:
            xc = b + self.cantilever
            y_tip = self.top_y(-xc)
            pts += [(-xc, y_tip), (-xc, y_tip - self.cantilever_tip),
                    (-b, y_tip - self.cantilever_tip - self.cantilever_rise)]
        return pts

    def voids(self, n: int) -> list[list[tuple[float, float]]]:
        return [
            _void(sgn * self.void_centre_offset, self.void_bottom,
                  self.void_width, self.void_height, n)
            for sgn in (-1.0, 1.0)
        ]


@dataclass(frozen=True)
class ShanghaiHingedHollowSlabDimensions:
    """Section of a 铰接 (hinge-jointed) slab, mm. Flat top."""

    depth: float
    unit: str
    key_run: float  # vertical extent of each key slope (70 or 80)
    key_inset: float  # horizontal inset of the deepest key point (50/60)
    void_height: float
    void_bottom: float
    void_top: float
    key_top_inset: float = 30.0
    key_top_height: float = 20.0
    void_width: float = 360.0
    void_side_cover: float = 100.0
    cantilever: float = 400.0
    cantilever_tip: float = 200.0
    cantilever_rise: float = 50.0

    @property
    def width(self) -> float:
        return 995.0 if self.unit == "edge" else 990.0

    @property
    def void_gap(self) -> float:
        return 75.0 if self.unit == "edge" else 70.0

    def _key(self, x0: float, sign: float) -> list[tuple[float, float]]:
        """Key points from the top corner downwards; x0 is the outer face."""
        d = self.depth
        return [
            (x0 + sign * self.key_top_inset, d),
            (x0 + sign * self.key_top_inset, d - self.key_top_height),
            (x0 + sign * self.key_inset, d - self.key_top_height - self.key_run),
            (x0, d - self.key_top_height - 2.0 * self.key_run),
        ]

    def outline(self) -> list[tuple[float, float]]:
        w = self.width
        x0, x1 = -w / 2.0, w / 2.0
        d = self.depth
        pts = [(x0, 0.0), (x1, 0.0)]
        if self.unit == "middle":
            pts += list(reversed(self._key(x1, -1.0)))
        else:
            root = d - self.cantilever_tip - self.cantilever_rise
            pts += [(x1, root), (x1 + self.cantilever, d - self.cantilever_tip),
                    (x1 + self.cantilever, d)]
        pts += self._key(x0, 1.0)
        return pts

    def voids(self, n: int) -> list[list[tuple[float, float]]]:
        x0 = -self.width / 2.0
        c1 = x0 + self.void_side_cover + self.void_width / 2.0
        c2 = c1 + self.void_width + self.void_gap
        return [_void(c, self.void_bottom, self.void_width, self.void_height, n) for c in (c1, c2)]


class _ShanghaiSlab:
    _family = ""
    SIZES: tuple[str, ...] = ()

    def __init__(self, size: str, arc_points: int = 64):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        if isinstance(arc_points, bool) or not isinstance(arc_points, int) or arc_points < 8:
            raise ValueError("arc_points must be an integer >= 8")
        data = _load_data()
        fam = data[self._family]
        self.size = size
        self.arc_points = arc_points
        self.source = data["source"]
        self.provenance = fam["provenance"]
        self.source_status = fam["source_status"]
        row = dict(fam["sections"][size])
        self.spans_m = tuple(row.pop("spans_m"))
        self.published = (fam.get("published_properties_m") or {}).get(size)
        self.dimensions = self._make_dims(row)

    @classmethod
    def for_span(cls, span_m: int, unit: str = "middle"):
        """Construct from a standard span (10, 13, 16, 18, 20, 22 m)."""
        for size in cls.SIZES:
            lo, _, rest = size.partition("m-")
            spans = [int(s) for s in lo.split("-")]
            if rest == unit and (span_m in spans or (len(spans) == 2 and spans[0] <= span_m <= spans[1])):
                return cls(size)
        raise ValueError(f"no {unit} slab for span {span_m!r} m")

    @property
    def geometry(self):
        """A ``sectionproperties`` Geometry in millimetres (voids included)."""
        return geometry_from_polygon(self.polygon)


class ShanghaiRigidHollowSlabSection(_ShanghaiSlab):
    """刚接空心板 midspan section (consultation draft DBJT08-101).

    Examples
    --------
    >>> from bridgebeams.cn.r2_shanghai_hollow_slab import ShanghaiRigidHollowSlabSection
    >>> ShanghaiRigidHollowSlabSection("10m-middle").dimensions.depth
    550.0
    """

    _family = "rigid"
    SIZES = (
        "10m-middle", "10m-edge", "13m-middle", "13m-edge",
        "16-18m-middle", "16-18m-edge", "20-22m-middle", "20-22m-edge",
    )

    def _make_dims(self, row):
        return ShanghaiRigidHollowSlabDimensions(
            depth=float(row["depth"]), unit=row["unit"],
            void_height=float(row["void_height"]), void_bottom=float(row["void_bottom"]),
            void_width=float(row["void_width"]),
        )

    @property
    def polygon(self) -> Polygon:
        d = self.dimensions
        n_fillet = max(8, self.arc_points // 4)  # quarter arc, same density as voids
        return orient(Polygon(d.outline(n_fillet), d.voids(self.arc_points)), sign=1.0)


class ShanghaiHingedHollowSlabSection(_ShanghaiSlab):
    """铰接空心板 section (consultation draft DBJT08-101), property-checked.

    Examples
    --------
    >>> from bridgebeams.cn.r2_shanghai_hollow_slab import ShanghaiHingedHollowSlabSection
    >>> ShanghaiHingedHollowSlabSection("20-22m-edge").dimensions.width
    995.0
    """

    _family = "hinged"
    SIZES = ShanghaiRigidHollowSlabSection.SIZES

    def _make_dims(self, row):
        return ShanghaiHingedHollowSlabDimensions(
            depth=float(row["depth"]), unit=row["unit"],
            key_run=float(row["key_run"]), key_inset=float(row["key_inset"]),
            void_height=float(row["void_height"]), void_bottom=float(row["void_bottom"]),
            void_top=float(row["void_top"]),
        )

    @property
    def polygon(self) -> Polygon:
        d = self.dimensions
        return orient(Polygon(d.outline(), d.voids(self.arc_points)), sign=1.0)


__all__ = [
    "ShanghaiHingedHollowSlabDimensions",
    "ShanghaiHingedHollowSlabSection",
    "ShanghaiRigidHollowSlabDimensions",
    "ShanghaiRigidHollowSlabSection",
]
