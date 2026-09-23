"""Japanese JIS A 5373 pretensioned PC slab girders (スラブ橋げた).

Types AS05-AS24 (A live load) and BS05-BS24 (B live load), standard
spans 5-24 m. Types 05-11 (BS11 included) are solid (充実断面); 12-24
are hollow (中空断面) with a pentagonal-bottomed void.

Sources (see ``data/r2_jis_slab_girders.json`` for URLs and hashes):

- MLIT Chubu Regional Bureau 道路設計要領 第5章 橋梁 v2014.03,
  表-5-III-9 and 図-5-III-40, PDF p28 / printed 5-25 (dimensions).
  The 2025 edition drops this table and cites the PCCEN JIS A 5373-2016
  handbook instead, so the guideline is superseded as a source.
- Nihon Koatsu Concrete 2024 slab-girder specification sheet, PDF pp3-4
  (published gross A, yu, yl, I, W): every row reproduced to rounding.
- Asahi Danke JIS A 5373-2010 catalogue (independent H/H1/H2/H3 table).

Outline (mm): soffit 700 wide, 70 mm vertical edge, 30 x 30 splay in to
the 640 mm upper body. Hollow void: 400 wide, 300 wide top with 50 x 50
chamfers, vertical sides H1, bottom V 110 high with its apex H3 above the
soffit, top slab H2; H = H2 + 50 + H1 + 110 + H3.

The Chubu table prints AS19 H2 = 106; the depth chain, the Asahi Danke
table and the published area all require 160, which is used.

Origin at mid-soffit, y upwards. Midspan gross concrete only.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon
from shapely.geometry.polygon import orient

from bridgebeams._geometry import geometry_from_polygon

_BOTTOM_WIDTH = 700.0
_BODY_WIDTH = 640.0
_EDGE_HEIGHT = 70.0
_SPLAY = 30.0
_VOID_HALF_WIDTH = 200.0
_VOID_TOP_HALF_WIDTH = 150.0
_VOID_CHAMFER = 50.0
_VOID_V_HEIGHT = 110.0


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.jp")
        .joinpath("data/r2_jis_slab_girders.json")
        .read_text(encoding="utf-8")
    )


@dataclass(frozen=True)
class JisSlabGirderDimensions:
    """Table dimensions in millimetres; H1/H2/H3 are zero for solid types."""

    depth: float
    h1: float = 0.0
    h2: float = 0.0
    h3: float = 0.0

    @property
    def hollow(self) -> bool:
        return self.h1 > 0.0

    def outline(self) -> list[tuple[float, float]]:
        xb, xu = _BOTTOM_WIDTH / 2.0, _BODY_WIDTH / 2.0
        right = [
            (xb, 0.0),
            (xb, _EDGE_HEIGHT),
            (xu, _EDGE_HEIGHT + _SPLAY),
            (xu, self.depth),
        ]
        return right + [(-x, y) for x, y in reversed(right)]

    def void(self) -> list[tuple[float, float]]:
        if not self.hollow:
            return []
        y_side_bottom = self.h3 + _VOID_V_HEIGHT
        y_side_top = y_side_bottom + self.h1
        y_top = self.depth - self.h2
        if abs(y_top - (y_side_top + _VOID_CHAMFER)) > 1e-9:
            raise ValueError("void depth chain does not close")
        xv, xt = _VOID_HALF_WIDTH, _VOID_TOP_HALF_WIDTH
        return [
            (0.0, self.h3),
            (xv, y_side_bottom),
            (xv, y_side_top),
            (xt, y_top),
            (-xt, y_top),
            (-xv, y_side_top),
            (-xv, y_side_bottom),
        ]


class JisSlabGirderSection:
    """JIS A 5373 slab girder AS05-AS24 / BS05-BS24 gross midspan section.

    Examples
    --------
    >>> from bridgebeams.jp.r2_jis_slab_girders import JisSlabGirderSection
    >>> JisSlabGirderSection("BS20").dimensions.depth
    800.0
    """

    SIZES = tuple(f"{p}S{n:02d}" for p in "AB" for n in range(5, 25))
    source_status = (
        "JIS A 5373 recommended-specification slab girders; MLIT Chubu 2014 "
        "guideline (superseded) and producer catalogues"
    )

    def __init__(self, size: str = "BS20"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        row = _load_data()["sections"][size]
        dims = row["dimensions_source_mm"]
        self.size = size
        self.published = row["published_gross_cm"]
        self.provenance = row["provenance"]
        self.dimensions = JisSlabGirderDimensions(
            depth=float(dims["H"]),
            h1=float(dims.get("H1", 0.0)),
            h2=float(dims.get("H2", 0.0)),
            h3=float(dims.get("H3", 0.0)),
        )

    @property
    def polygon(self) -> Polygon:
        d = self.dimensions
        holes = [d.void()] if d.hollow else []
        return orient(Polygon(d.outline(), holes), sign=1.0)

    @property
    def geometry(self):
        """A ``sectionproperties`` Geometry in millimetres."""
        return geometry_from_polygon(self.polygon)


__all__ = ["JisSlabGirderDimensions", "JisSlabGirderSection"]
