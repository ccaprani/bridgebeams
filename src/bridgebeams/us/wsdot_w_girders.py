"""WSDOT W-series prestressed I-girder sections.

These are the four 2006 archived WSDOT standard outlines, independently
corroborated by the June 2025 Bridge Design Manual property table. They are
gross concrete sections, excluding prestressing, deck, recesses and end
details. Source dimensions are inches; API geometry is millimetres, with
origin at the soffit centre and y upward. The source dates matter: these
outlines do not assert approval for use on a current bridge project.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon

INCH_TO_MM = 25.4


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.us")
        .joinpath("data/wsdot_w_girders.json")
        .read_text(encoding="utf-8")
    )


@dataclass(frozen=True)
class WsdotWDimensions:
    """Published W-series designation and symmetric gross outline, in mm."""

    size: str
    depth: float
    top_flange_width: float
    bottom_flange_width: float
    web_width: float
    right_half: tuple[tuple[float, float], ...]

    @property
    def outline(self) -> list[tuple[float, float]]:
        """Counterclockwise polygon vertices; last point is closed by Polygon."""
        return [(-x, y) for x, y in reversed(self.right_half[1:])] + list(
            self.right_half
        )


class WsdotWSection:
    """One of W42G, W50G, W58G and W74G from WSDOT's archived drawing."""

    SIZES = ("W42G", "W50G", "W58G", "W74G")

    def __init__(self, size: str = "W42G"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        row = _load_data()["sections"][size]
        self.size = size
        self.published = row["published_properties_imperial"]
        self.dimensions = WsdotWDimensions(
            size=size,
            depth=row["depth_in"] * INCH_TO_MM,
            top_flange_width=row["top_flange_width_in"] * INCH_TO_MM,
            bottom_flange_width=row["bottom_flange_width_in"] * INCH_TO_MM,
            web_width=row["web_width_in"] * INCH_TO_MM,
            right_half=tuple(
                (x * INCH_TO_MM, y * INCH_TO_MM)
                for x, y in row["right_half_in"]
            ),
        )

    @property
    def polygon(self) -> Polygon:
        """Gross concrete outline, in square-millimetre coordinate space."""
        return Polygon(self.dimensions.outline)

    @property
    def geometry(self):
        """The outline as a sectionproperties Geometry, in mm."""
        return geometry_from_polygon(self.polygon)


__all__ = ["WsdotWDimensions", "WsdotWSection"]
