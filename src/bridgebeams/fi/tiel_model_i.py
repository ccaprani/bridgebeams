"""TIEL 2160004-2000 LIITE 1.4 A–A model girder, not a national SKU.

The preliminary-design guide permits project/mould changes. Only its one
fully dimensioned h1270 model is catalogued; no size matrix is inferred.
The 12-vertex nominal bare concrete outline excludes CIP slab, reinforcement
and end blocks. LIITE 4's rounded properties use a rectangular idealization,
not the exact physical haunches implemented here.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon


def _load_data() -> dict:
    return json.loads(resources.files("bridgebeams.fi.data").joinpath(
        "tiel_model_i.json").read_text())


@dataclass(frozen=True)
class TielModelIDimensions:
    """Nominal model dimensions in mm, origin at mid-soffit."""

    depth: float
    bottom_width: float
    bottom_thickness: float
    bottom_haunch: float
    web_width: float
    web_height: float
    top_haunch: float
    top_thickness: float
    top_width: float

    @property
    def outline(self) -> list[tuple[float, float]]:
        """Twelve vertices, anti-clockwise from the bottom-left corner."""
        b, w, t = self.bottom_width / 2, self.web_width / 2, self.top_width / 2
        y1 = self.bottom_thickness
        y2 = y1 + self.bottom_haunch
        y3 = y2 + self.web_height
        y4 = y3 + self.top_haunch
        return [(-b, 0), (b, 0), (b, y1), (w, y2), (w, y3),
                (t, y4), (t, self.depth), (-t, self.depth), (-t, y4),
                (-w, y3), (-w, y2), (-b, y1)]


class TielModelISection:
    """One source model example: ``TIEL-model-AA-h1270`` (not a standard SKU)."""

    SIZES = ("TIEL-model-AA-h1270",)
    provenance = "transcribed"
    source_status = "TIEL 2160004-2000 preliminary-design model, LIITE 1.4 A-A; nominal outline, not a national SKU"

    def __init__(self, size: str = "TIEL-model-AA-h1270"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        self.size = size
        self.row = data["sections"][size]
        self.source = data["source"]
        self.published = data["rounded_corroboration"]
        self.dimensions = TielModelIDimensions(**self.row["dimensions_mm"])

    @property
    def polygon(self) -> Polygon:
        return Polygon(self.dimensions.outline)

    @property
    def geometry(self):
        """Bare girder as a ``sectionproperties`` Geometry, in mm."""
        return geometry_from_polygon(self.polygon)


__all__ = ["TielModelIDimensions", "TielModelISection"]
