"""Waskita Beton Precast (Indonesia) PC-I girders and voided slabs, 2026.

Source: PT Waskita Beton Precast Tbk, *Product Catalogue* 2026
(waskita-katalog-produk-2026.pdf). PC-I girder: notation sketch PDF p14
(printed 13, "Middle Section Type 1/Type 2") and dimension table PDF p15
(printed 14). Voided slab: PDF p44 (printed 43) typical sections and
PDF p45 (printed 44) dimension table. No section properties are published.

PC-I (``transcribed-with-convention``), middle (midspan) section: top
width A with 80 mm wide x 70 mm deep top shoulders; h1 = vertical flange
edge below the shoulder level; h2 = taper from the flange edge to the web
Tw1; h3 = bottom splay from the web to the bottom flange edge; h4 =
bottom flange edge; base B. The web height closes the depth chain
H - 70 - h1 - h2 - h3 - h4. The reading of h1 as starting below the 70 mm
shoulder is taken from the notation sketch (its h1 dimension begins at the
shoulder level). Tw2, h5-h8 describe the thickened end (edge) section and
are not used. The Semi-T column has no depth in the table and is not
implemented. These are Waskita products; the same H-designations in the
WIKA brochure (``bridgebeams.id.wika_girders``) are a different producer.

Voided slab (``estimate``): width B, depth H, void diameter D centred at
h = H/2, side key b = 50 wide with h2 vertical below the top and a 25 mm
(h1) sloping return. Not printed: void lateral positions and soffit
chamfers. Estimates: Type 1 (970, two voids) at x = ±240 mm and Type 2
(1200, three voids) at 0 and ±320 mm (both scaled from the schematic
sketch), 25 x 25 mm soffit chamfers.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources
from math import cos, pi, sin

from shapely.geometry import Polygon
from shapely.geometry.polygon import orient

from bridgebeams._geometry import geometry_from_polygon


def _load() -> dict:
    return json.loads(
        resources.files("bridgebeams.id").joinpath("data/r2_waskita.json").read_text(encoding="utf-8")
    )


@dataclass(frozen=True)
class WaskitaPcIDimensions:
    """Catalogue notation (mm): H, A, B, Tw1, h1-h4; 80 x 70 shoulders."""

    H: float
    A: float
    B: float
    Tw1: float
    h1: float
    h2: float
    h3: float
    h4: float
    shoulder_width: float = 80.0
    shoulder_depth: float = 70.0

    @property
    def web_height(self) -> float:
        return self.H - self.shoulder_depth - self.h1 - self.h2 - self.h3 - self.h4

    def right_half(self) -> list[tuple[float, float]]:
        xb, xw, xa = self.B / 2, self.Tw1 / 2, self.A / 2
        y1 = self.h4
        y2 = y1 + self.h3
        y3 = y2 + self.web_height
        y4 = y3 + self.h2
        y5 = y4 + self.h1
        return [(xb, 0.0), (xb, y1), (xw, y2), (xw, y3), (xa, y4), (xa, y5),
                (xa - self.shoulder_width, y5), (xa - self.shoulder_width, self.H), (0.0, self.H)]


class WaskitaPcIGirderSection:
    """Waskita PC-I girder middle section, H90-H230 (``"H170"`` etc.)."""

    SIZES = ("H90", "H125", "H140", "H160", "H170", "H185", "H210", "H230")
    source_status = "producer catalogue (Waskita Beton Precast, 2026)"

    def __init__(self, size: str = "H170"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        row = _load()["pc_i"]["sections"][size]
        self.size, self.published = size, row
        self.provenance = row["provenance"]
        n = row["notation_mm"]
        self.dimensions = WaskitaPcIDimensions(**{k: float(n[k]) for k in ("H", "A", "B", "Tw1", "h1", "h2", "h3", "h4")})

    @property
    def polygon(self) -> Polygon:
        r = self.dimensions.right_half()
        return orient(Polygon(r + [(-x, y) for x, y in reversed(r[:-1])]), sign=1)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


@dataclass(frozen=True)
class WaskitaVoidedSlabDimensions:
    H: float
    B: float
    D: float
    h2: float
    void_x: tuple[float, ...]
    h1: float = 25.0
    b: float = 50.0
    chamfer: float = 25.0

    @property
    def h(self) -> float:
        return self.H / 2

    def outline(self) -> list[tuple[float, float]]:
        hb, c = self.B / 2, self.chamfer
        y_key = self.H - self.h2
        right = [(hb - c, 0.0), (hb, c), (hb, y_key - self.h1), (hb - self.b, y_key), (hb - self.b, self.H)]
        return right + [(-x, y) for x, y in reversed(right)]


class WaskitaVoidedSlabSection:
    """Waskita voided slab: Type 1 ``H57/H62/H66`` (970), Type 2 ``H52.5/H62.5`` (1200)."""

    SIZES = ("H57", "H62", "H66", "H52.5", "H62.5")
    source_status = "producer catalogue (Waskita Beton Precast, 2026)"

    def __init__(self, size: str = "H62", segments: int = 64):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        if isinstance(segments, bool) or not isinstance(segments, int) or segments < 8:
            raise ValueError("segments must be an integer >= 8")
        row = _load()["voided_slab"]["sections"][size]
        self.size, self.published, self.segments = size, row, segments
        self.provenance = row["provenance"]
        n = row["notation_mm"]
        self.dimensions = WaskitaVoidedSlabDimensions(
            H=float(n["H"]), B=float(n["B"]), D=float(n["D"]), h2=float(n["h2"]),
            void_x=tuple(float(x) for x in row["estimated_void_x_mm"]),
        )

    @property
    def polygon(self) -> Polygon:
        d = self.dimensions
        r, n = d.D / 2, self.segments
        holes = [[(x + r * cos(2 * pi * i / (2 * n)), d.h + r * sin(2 * pi * i / (2 * n))) for i in range(2 * n)]
                 for x in d.void_x]
        return orient(Polygon(d.outline(), holes), sign=1)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = [
    "WaskitaPcIDimensions",
    "WaskitaPcIGirderSection",
    "WaskitaVoidedSlabDimensions",
    "WaskitaVoidedSlabSection",
]
