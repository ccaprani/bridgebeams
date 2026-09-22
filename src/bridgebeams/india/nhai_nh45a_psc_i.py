"""NH 45-A Ch 50+473 midspan PSC I-girder, feasibility drawing R0.

Source: NHAI / Feedback Infra, *PKG II Modified Structural Drawings*,
General Arrangement Drawing for Major Bridge (9 x 35.0 m) at design
Ch 50+473, drawing FIPL-HD-TPT-117-V-N-45A-MJB-CH-50+473-GA-01,
sheet 03/03, November 2017, PDF page 50, "SECTION AT MID".
https://nhai.gov.in/nhai/sites/default/files/2020/PKG_II_Modified_Structural_drawings.pdf

The title block says FINAL FEASIBILITY REPORT. This is one project drawing,
not an Indian national standard or an issued-for-construction detail. The
gross midspan contour excludes strands, reinforcement, deck slab, end blocks
and local details. Dimensions are millimetres, with soffit at y=0.
"""

from dataclasses import dataclass

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon


@dataclass(frozen=True)
class Nh45aPscIDimensions:
    """Dimensioned midspan outline from NHAI drawing sheet 03/03."""

    depth: float = 2250.0
    top_width: float = 900.0
    web_width: float = 300.0
    bottom_width: float = 750.0
    top_vertical: float = 150.0
    upper_splay_height: float = 100.0
    web_height: float = 1600.0
    lower_splay_height: float = 150.0
    bottom_vertical: float = 250.0

    @property
    def outline(self) -> list[tuple[float, float]]:
        """Clockwise vertices of the gross concrete section."""
        if self.depth != (self.top_vertical + self.upper_splay_height
                          + self.web_height + self.lower_splay_height
                          + self.bottom_vertical):
            raise ValueError("vertical dimension chain does not close")
        b, w, t = self.bottom_width / 2, self.web_width / 2, self.top_width / 2
        y_lower = self.bottom_vertical + self.lower_splay_height
        y_upper = y_lower + self.web_height
        y_top_splay = y_upper + self.upper_splay_height
        return [(-b, 0), (b, 0), (b, self.bottom_vertical),
                (w, y_lower), (w, y_upper), (t, y_top_splay),
                (t, self.depth), (-t, self.depth), (-t, y_top_splay),
                (-w, y_upper), (-w, y_lower), (-b, self.bottom_vertical)]


class Nh45aPscISection:
    """One project-specific midspan outline: ``CH50+473-MID``."""

    SIZES = ("CH50+473-MID",)

    def __init__(self, size: str = "CH50+473-MID") -> None:
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        self.size = size
        self.dimensions = Nh45aPscIDimensions()

    @property
    def polygon(self) -> Polygon:
        return Polygon(self.dimensions.outline)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = ["Nh45aPscIDimensions", "Nh45aPscISection"]
