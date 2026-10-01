"""Thai DOH standard precast prestressed I-girder (IG-205, 20 m span).

From the Royal Thai Government Department of Highways *Standard Drawings,
2015 Edition* (IG-205 "Girder Dimension", sheet 224/354). AASHTO-derived
section, HL-93 loading, 28 × 12.7 mm 7-wire strand layout (IG-206).

Geometry convention: origin at the middle of the soffit, y positive
upwards, millimetres. Symmetric about x = 0. The web/bottom-splay split
of the dimension stack is modelled as a plain web of the full clear
height (the official scan does not resolve the splay separately; effect
on area is <= 1%).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon

_DATA_FILE = "doh_ig_girders.json"


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.th.data").joinpath(_DATA_FILE).read_text()
    )


@dataclass(frozen=True)
class ThDOHIGirderDimensions:
    """Dimensions of the DOH 20 m I-girder, millimetres."""

    depth: float = 1200.0
    top_flange_width: float = 450.0
    top_flange_thickness: float = 100.0
    haunch_height: float = 75.0
    web_width: float = 175.0
    web_clear_height: float = 825.0  # balance of the 1200 stack
    bottom_flange_width: float = 500.0
    bottom_flange_edge_thickness: float = 200.0

    @property
    def outline(self) -> list[tuple[float, float]]:
        d = self.depth
        hw_t = self.top_flange_width / 2.0
        hw_b = self.bottom_flange_width / 2.0
        w = self.web_width / 2.0
        y_web_bot = (
            self.bottom_flange_edge_thickness + self.web_clear_height
        )
        y_web_top = y_web_bot + self.haunch_height
        r = [
            (hw_b, 0.0),
            (hw_b, self.bottom_flange_edge_thickness),
            (w, y_web_bot),
            (w, y_web_top),
            (hw_t, y_web_top + self.top_flange_thickness),
            (hw_t, d),
        ]
        l = [(-x, y) for x, y in reversed(r)]
        return l + r


class ThDOHIGirderSection:
    """Thai DOH 20 m standard I-girder as a ``sectionproperties`` Geometry.

    Examples
    --------
    >>> from bridgebeams.th import ThDOHIGirderSection
    >>> g = ThDOHIGirderSection()
    >>> g.dimensions.depth
    1200.0
    """

    # Unresolved web/splay split modelled as plain web; not fitted, so estimate over fitted-reconstruction.
    provenance = "estimate"
    source_status = "DOH Standard Drawings 2015 Edition"

    def __init__(self):
        data = _load_data()
        self.published = data["published_properties"][0]
        self.dimensions = ThDOHIGirderDimensions(
            depth=float(self.published["depth"]),
            top_flange_width=float(self.published["top_flange_width"]),
            top_flange_thickness=float(self.published["top_flange_thickness"]),
            haunch_height=float(self.published["haunch_height"]),
            web_width=float(self.published["web_width"]),
            web_clear_height=float(self.published.get("web_clear_height", 825.0)),
            bottom_flange_width=float(self.published["bottom_flange_width"]),
            bottom_flange_edge_thickness=float(
                self.published["bottom_flange_edge_thickness"]
            ),
        )

    @property
    def polygon(self) -> Polygon:
        return Polygon(self.dimensions.outline)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = ["ThDOHIGirderDimensions", "ThDOHIGirderSection"]
