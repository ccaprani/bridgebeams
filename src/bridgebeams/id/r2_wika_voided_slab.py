"""WIKA Beton PC voided slabs VS-57/62/66/74 x 970 (bare precast unit).

Source: WIKA Beton *Brosur WTON 2022*, PDF p19 ("GIRDER SHAPE & DIMENSION |
PC VOIDED SLAB"); the same shapes recur in WIKA's Dec-2017 bridge sheet.
Printed: width 97 cm, depth 57/62/66/74 cm, void diameter 25/30/30 cm
(VS-74: oval, 30 cm wide), void-centre height 28.5/31/33/39 cm, area and
inertia (cm², cm⁴, dots are thousands separators).

Not printed but taken from the brochure's **vector** drawing, which is at
a uniform scale (97 cm width and the four depths agree to <= 1.2 %):
void centres at x = ±229.5 mm; a side shear key 30 mm deep with its
sloping lower face from y = 301.3 to 340.5 mm (910 mm top width above);
15 mm x 10.6 mm soffit chamfers. With these, VS-57/62/66 reproduce the
published area within 0.02 % and inertia within 0.1 %.

VS-74's oval is drawn as a stadium (30 cm semicircles, 366 mm high); the
drawn size leaves the area 1.8 % high. The oval height is therefore fitted
to the published area: 300 x 380 mm (80 mm straight sides), centred at the
printed 390 mm, which also gives the inertia within 0.1 %.

The "+18" composite rows (180 mm topping) are not modelled. Origin at
mid-soffit, y up, mm; voids are polygon interiors (``segments`` per
semicircle).
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
        resources.files("bridgebeams.id").joinpath("data/r2_wika_voided_slabs.json").read_text(encoding="utf-8")
    )


def _stadium(xc: float, yc: float, width: float, height: float, n: int) -> list[tuple[float, float]]:
    """Closed stadium/circle ring (circle when height == width)."""
    r = width / 2.0
    s = (height - width) / 2.0
    pts = [(xc + r * cos(pi * i / n), yc + s + r * sin(pi * i / n)) for i in range(n + 1)]
    pts += [(xc + r * cos(pi + pi * i / n), yc - s + r * sin(pi + pi * i / n)) for i in range(n + 1)]
    if s == 0:  # drop duplicated join points of a full circle
        pts = pts[:n] + pts[n + 1 : 2 * n + 1]
    return pts


@dataclass(frozen=True)
class WikaVoidedSlabDimensions:
    depth: float
    void_width: float
    void_height: float
    void_centre_height: float
    width: float = 970.0
    top_width: float = 910.0
    key_bottom: float = 301.3
    key_top: float = 340.5
    chamfer_width: float = 15.0
    chamfer_height: float = 10.6
    void_offset: float = 229.5

    def outline(self) -> list[tuple[float, float]]:
        b, t = self.width / 2, self.top_width / 2
        right = [(b - self.chamfer_width, 0.0), (b, self.chamfer_height), (b, self.key_bottom), (t, self.key_top), (t, self.depth)]
        return right + [(-x, y) for x, y in reversed(right)]


class WikaVoidedSlabSection:
    """WIKA PC voided slab VS57, VS62, VS66 or VS74 (970 mm wide)."""

    SIZES = ("VS57", "VS62", "VS66", "VS74")
    source_status = "producer brochure (WIKA Beton, July 2022)"

    def __init__(self, size: str = "VS62", segments: int = 64):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        if isinstance(segments, bool) or not isinstance(segments, int) or segments < 8:
            raise ValueError("segments must be an integer >= 8")
        row = _load()["sections"][size]
        self.size, self.published, self.segments = size, row, segments
        self.provenance = row["provenance"]
        self.dimensions = WikaVoidedSlabDimensions(**{k: float(v) for k, v in row["dimensions_mm"].items()})

    @property
    def polygon(self) -> Polygon:
        d = self.dimensions
        holes = [
            _stadium(s * d.void_offset, d.void_centre_height, d.void_width, d.void_height, self.segments)
            for s in (-1, 1)
        ]
        return orient(Polygon(d.outline(), holes), sign=1)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = ["WikaVoidedSlabDimensions", "WikaVoidedSlabSection"]
