"""Four nominal PSC inverted-T sections from RMTO Publication 102 sheets.

The 56-page mirror contains both ordinary RC and PSC. These four sheets
positively identify prestressing and dimension the bare girder beneath an
180 mm CIP slab. Exclude that slab, permanent formwork, reinforcement and
end blocks. No undocumented chamfers or fillets are invented.

Sheet 8-6 h620 is withheld: its web-width chain is absent. Other PSC slab,
spaced-girder and joist families remain untranscribed. Mirror provenance
and current applicability are not equivalent to an official current release.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon


def _load_data() -> dict:
    return json.loads(resources.files("bridgebeams.ir.data").joinpath(
        "rmto_102.json").read_text())


@dataclass(frozen=True)
class Rmto102InvertedTDimensions:
    """Nominal bare dimensions in mm, origin at mid-soffit."""

    depth: float
    bottom_width: float
    web_width: float
    bottom_thickness: float
    haunch_height: float

    @property
    def web_height(self) -> float:
        """Straight web above the lower haunch, excluding the CIP slab."""
        return self.depth - self.bottom_thickness - self.haunch_height

    @property
    def outline(self) -> list[tuple[float, float]]:
        """Eight vertices, anti-clockwise from the bottom-left corner."""
        b, w = self.bottom_width / 2, self.web_width / 2
        y1 = self.bottom_thickness
        y2 = y1 + self.haunch_height
        return [(-b, 0), (b, 0), (b, y1), (w, y2), (w, self.depth),
                (-w, self.depth), (-w, y2), (-b, y1)]


class Rmto102InvertedTSection:
    """Sheet-keyed nominal PSC girders; names are catalogue locators, not SKUs."""

    SIZES = ("RMTO102-8-4-h370", "RMTO102-8-5-h470",
             "RMTO102-8-7-h770", "RMTO102-8-8A-h1000")
    provenance = "transcribed-with-convention"
    source_status = "RMTO Publication 102 mirror; nominal bare PSC girder at underside of slab; official version/current applicability unverified"

    def __init__(self, size: str = "RMTO102-8-4-h370"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        self.size = size
        self.row = data["sections"][size]
        self.source = data["source"]
        self.published = {}  # No bare A/cy/I table identified; do not invent one.
        self.dimensions = Rmto102InvertedTDimensions(
            depth=self.row["depth_mm"], **data["common_dimensions_mm"])

    @property
    def polygon(self) -> Polygon:
        return Polygon(self.dimensions.outline)

    @property
    def geometry(self):
        """Bare girder as a ``sectionproperties`` Geometry, in mm."""
        return geometry_from_polygon(self.polygon)


__all__ = ["Rmto102InvertedTDimensions", "Rmto102InvertedTSection"]
