"""Somaco (Romania) precast bridge girders scaled from catalogue outlines (estimates).

Source: Somaco, "Elemente prefabricate din beton pentru infrastructura rutieră"
(2025), PDF p3 (grinzi de pod tip IPTANA) and p4 (tip Eurocod; autostradă).
The catalogue prints only depth h (plus 1.20/2.20/0.88 m for GP 220-40); each
outline is the drawn vector schematic scaled to h. The schematics are to
scale (IPTANA GP42/GP72 reproduce the dimensioned ASA IPTANA sections), but
every section here is ``provenance = "estimate"``. See data/r2_somaco.json.
Millimetres, origin at mid-soffit, y upwards.
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
        resources.files("bridgebeams.ro").joinpath("data/r2_somaco.json").read_text(encoding="utf-8")
    )


@dataclass(frozen=True)
class SomacoGirderDimensions:
    """Scale factors (mm per drawing point) applied to the digitised outline."""

    depth: float
    scale_x: float
    scale_y: float


class SomacoGirderSection:
    """Somaco GP 52E, 95E, 105E, 93 and 220-40 (midspan E-E) gross sections."""

    SIZES = ("GP 52E", "GP 95E", "GP 105E", "GP 93", "GP 220-40")
    source_status = "producer catalogue (2025)"

    def __init__(self, size: str = "GP 105E"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        row = data["sizes"][size]
        self.size = size
        self.published = row
        self.provenance = row.get("provenance", data["provenance"])
        pts = data["icons_pt"][row["icon"]]
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        depth = row["depth_cm"] * 10.0
        sy = depth / (max(ys) - min(ys))
        if "top_width_cm" in row:
            sx = row["top_width_cm"] * 10.0 / (max(xs) - min(xs))
        else:
            sx = sy
        self._pts = pts
        self.dimensions = SomacoGirderDimensions(depth=depth, scale_x=sx, scale_y=sy)

    @property
    def polygon(self) -> Polygon:
        d = self.dimensions
        return orient(Polygon([(x * d.scale_x, y * d.scale_y) for x, y in self._pts]), 1.0)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = ["SomacoGirderDimensions", "SomacoGirderSection"]
