"""Ontario MTO prestressed box girders B700-B1000, 1220 and 915 mm wide.

The 1220 mm units are transcribed from the June 2025 standard drawings
SS107-13 (B700, B800, B900) and SS107-14 (B1000). The source is PDF page 1
of each, "STRAND GRID ARRANGEMENT", section 2 (the midspan voided
section). Printed values: 1220 mm width; H = 700/800/900/1000 mm;
140 mm top and bottom slabs; 125 mm webs; 75 x 75 mm void chamfers;
20 mm outer corner chamfers. Note 15 makes the top chamfers optional,
but they are drawn and included here. The girders have plain vertical
sides with no shear key. SS107-15 connects adjacent boxes with welded
steel ties across a nominal 10 mm gap. Chamfers are taken at 45 degrees.
The void is expanded polystyrene (note 16), so it is modelled as a hole.

The 915 mm width is only listed in the August 2023 DRAFT MTO Prestressed
Concrete Girder Guidelines (PDF p15-16, Table 3: "915 / 1220"). No
held current drawing shows it. The 915 units are a best estimate: the
1220 template is used, with the same 140/125/75/20 mm details and a
narrower void (665 mm). Their provenance is ``"estimate"``.

Coordinates are in millimetres, with the origin at mid-soffit and y upwards.
End blocks, holes, strands and bearings are excluded.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon
from shapely.geometry.polygon import orient

from bridgebeams._geometry import geometry_from_polygon


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.ca").joinpath("data/mto_box_girders.json").read_text()
    )


def _chamfered_rectangle(x0, y0, x1, y1, c):
    return [(x0 + c, y0), (x1 - c, y0), (x1, y0 + c), (x1, y1 - c),
            (x1 - c, y1), (x0 + c, y1), (x0, y1 - c), (x0, y0 + c)]


@dataclass(frozen=True)
class CaMtoBoxGirderDimensions:
    depth: float
    width: float = 1220.0
    top_slab: float = 140.0
    bottom_slab: float = 140.0
    web: float = 125.0
    void_chamfer: float = 75.0
    corner_chamfer: float = 20.0

    @property
    def outline(self) -> list[tuple[float, float]]:
        w = self.width / 2
        return _chamfered_rectangle(-w, 0.0, w, self.depth, self.corner_chamfer)

    @property
    def void(self) -> list[tuple[float, float]]:
        v = self.width / 2 - self.web
        return _chamfered_rectangle(-v, self.bottom_slab, v,
                                    self.depth - self.top_slab, self.void_chamfer)

    @property
    def void_width(self) -> float:
        return self.width - 2 * self.web


class CaMtoBoxGirderSection:
    """Ontario box girder; size string ``B<depth>-<width>``, e.g. ``B800-1220``."""

    SIZES = tuple(f"B{d}-{w}" for w in (1220, 915) for d in (700, 800, 900, 1000))

    def __init__(self, size: str = "B800-1220"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        row = _load_data()["sizes"][size]
        self.size = size
        self.drawing = row["drawing"]
        self.provenance = row["provenance"]
        self.source_status = row["source_status"]
        self.dimensions = CaMtoBoxGirderDimensions(depth=float(row["depth_mm"]),
                                                   width=float(row["width_mm"]))

    @property
    def polygon(self) -> Polygon:
        d = self.dimensions
        return orient(Polygon(d.outline, [d.void]), sign=1)

    @property
    def geometry(self):
        """Return the gross concrete ``sectionproperties`` geometry (void as a hole)."""
        return geometry_from_polygon(self.polygon)


__all__ = ["CaMtoBoxGirderDimensions", "CaMtoBoxGirderSection"]
