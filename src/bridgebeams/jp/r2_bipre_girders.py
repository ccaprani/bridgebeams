"""Bi-Prestressing (バイプレ方式) precast I and hollow girders, trial designs.

Source: バイプレストレッシング工法協会, プレキャスト桁の標準断面
(https://bipre.sakura.ne.jp/cross/index.html), section GIFs img3 (I
girders, spans 25-50 m) and img11 (hollow girders, spans 25-35 m). The
association calls these trial designs (試設計) for depth-limited road
bridges, B live load, not a national standard. See
``data/r2_bipre_girders.json`` for hashes and all conventions.

I girders: flange 30 mm set-back at the top surface and a 30 mm full-width
lip at the flange edge (horizontal-step convention), two-slope tapers
meeting at x = +/-200 mm. The 45 m type's vertical chain is scaled from
the drawing (estimate). Hollow girders: 750 mm body on an 850 mm bottom
ledge, single void with a V-shaped bottom.

Origin at mid-soffit, y upwards, millimetres. Gross concrete only;
compression bars and tendons are not deducted.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon
from shapely.geometry.polygon import orient

from bridgebeams._geometry import geometry_from_polygon

_LIP = 30.0


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.jp")
        .joinpath("data/r2_bipre_girders.json")
        .read_text(encoding="utf-8")
    )


@dataclass(frozen=True)
class BipreIGirderDimensions:
    """Symmetric I girder; flange = edge thickness of each flange."""

    depth: float
    top_width: float
    bottom_width: float
    web_width: float
    flange: float
    outer_taper: float
    inner_taper: float
    outer_run: float
    inner_run: float

    @property
    def clear_web(self) -> float:
        return self.depth - 2.0 * (self.flange + self.outer_taper + self.inner_taper)

    def outline(self) -> list[tuple[float, float]]:
        xw = self.web_width / 2.0
        xk = xw + self.inner_run
        xb, xt = self.bottom_width / 2.0, self.top_width / 2.0
        if abs(xk + self.outer_run - xt) > 1e-9 or abs(xk + self.outer_run - xb) > 1e-9:
            raise ValueError("flange width chain does not close")
        d, f = self.depth, self.flange
        y1 = f + self.outer_taper
        y2 = y1 + self.inner_taper
        right = [
            (xb, 0.0),
            (xb, f),
            (xk, y1),
            (xw, y2),
            (xw, d - y2),
            (xk, d - y1),
            (xt, d - f),
            (xt, d - f + _LIP),
            (xt - _LIP, d - f + _LIP),
            (xt - _LIP, d),
        ]
        return right + [(-x, y) for x, y in reversed(right)]


@dataclass(frozen=True)
class BipreHollowGirderDimensions:
    depth: float
    top_width: float
    bottom_width: float
    wall: float
    void_width: float
    top_slab: float
    void_side: float
    void_v: float
    ledge: float
    ledge_edge: float

    @property
    def void_apex_height(self) -> float:
        return self.depth - self.top_slab - self.void_side - self.void_v

    def outline(self) -> list[tuple[float, float]]:
        xb, xt = self.bottom_width / 2.0, self.top_width / 2.0
        right = [
            (xb, 0.0),
            (xb, self.ledge_edge),
            (xt, self.ledge_edge + self.ledge),
            (xt, self.depth),
        ]
        return right + [(-x, y) for x, y in reversed(right)]

    def void(self) -> list[tuple[float, float]]:
        xv = self.void_width / 2.0
        if abs(xv + self.wall - self.top_width / 2.0) > 1e-9:
            raise ValueError("wall/void width chain does not close")
        y0 = self.void_apex_height
        y1 = y0 + self.void_v
        y2 = y1 + self.void_side
        return [(0.0, y0), (xv, y1), (xv, y2), (-xv, y2), (-xv, y1)]


class _BipreBase:
    SIZES: tuple[str, ...] = ()
    source_status = "association trial design (試設計), Bi-Prestressing System Institution web page (c) 2009"
    _dims_cls: type = BipreIGirderDimensions

    def __init__(self, size: str):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        row = dict(_load_data()["sections"][size])
        self.size = size
        self.span_m = row.pop("span_m")
        self.provenance = row.pop("provenance")
        row.pop("clear_web", None)
        row.pop("void_apex_height", None)
        self.dimensions = self._dims_cls(**{k: float(v) for k, v in row.items()})

    @property
    def geometry(self):
        """A ``sectionproperties`` Geometry in millimetres."""
        return geometry_from_polygon(self.polygon)


class BipreIGirderSection(_BipreBase):
    """Bi-pre precast I girder for spans 25-50 m (I25 ... I50).

    >>> from bridgebeams.jp.r2_bipre_girders import BipreIGirderSection
    >>> BipreIGirderSection("I40").dimensions.depth
    1250.0
    """

    SIZES = ("I25", "I30", "I35", "I40", "I45", "I50")
    _dims_cls = BipreIGirderDimensions

    def __init__(self, size: str = "I40"):
        super().__init__(size)

    @property
    def polygon(self) -> Polygon:
        return orient(Polygon(self.dimensions.outline()), sign=1.0)


class BipreHollowGirderSection(_BipreBase):
    """Bi-pre precast hollow girder for spans 25-35 m (H25, H30, H35)."""

    SIZES = ("H25", "H30", "H35")
    _dims_cls = BipreHollowGirderDimensions

    def __init__(self, size: str = "H30"):
        super().__init__(size)

    @property
    def polygon(self) -> Polygon:
        d = self.dimensions
        return orient(Polygon(d.outline(), [d.void()]), sign=1.0)


__all__ = [
    "BipreHollowGirderDimensions",
    "BipreHollowGirderSection",
    "BipreIGirderDimensions",
    "BipreIGirderSection",
]
