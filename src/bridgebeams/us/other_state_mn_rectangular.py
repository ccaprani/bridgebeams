"""Minnesota DOT 14RB, 18RB and 22RB prestressed rectangular beams.

Source: MnDOT LRFD Bridge Design Manual, Section 5, February 2019,
Figure 5.4.6.1 (printed p. 5-37, PDF page 37 / zero-based 36).
https://www.dot.state.mn.us/bridge/pdf/lrfdmanual/section05.pdf

The source drawing gives a 2'-2" (26 inch) width and a type-specific depth.
The four corners of the gross concrete outline are therefore exact. All
coordinates returned here are millimetres, with the soffit at y=0. The
section omits strands, reinforcement, deck, stool and local end details.

This is an edition-specific 2019 transcription. MnDOT lists a 2025 manual,
but that newer PDF was inaccessible during this review, so no claim is made
that these are the current standard dimensions.
"""

from __future__ import annotations

from dataclasses import dataclass

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon

INCH_MM = 25.4


@dataclass(frozen=True)
class MnRectangularBeamDimensions:
    """Gross section width and depth in millimetres."""

    width: float
    depth: float

    @property
    def outline(self) -> list[tuple[float, float]]:
        half_width = self.width / 2
        return [
            (-half_width, 0.0),
            (half_width, 0.0),
            (half_width, self.depth),
            (-half_width, self.depth),
        ]


class MnRectangularBeamSection:
    """MnDOT RB beam by the 2019 designation, e.g. ``"14RB"``."""

    DEPTHS_IN = {"14RB": 14, "18RB": 18, "22RB": 22}
    TYPES = tuple(DEPTHS_IN)

    def __init__(self, section_type: str = "14RB") -> None:
        if section_type not in self.DEPTHS_IN:
            raise ValueError(f"section_type must be one of {self.TYPES}, got {section_type!r}")
        self.section_type = section_type
        self.dimensions = MnRectangularBeamDimensions(
            width=26 * INCH_MM,
            depth=self.DEPTHS_IN[section_type] * INCH_MM,
        )

    @property
    def polygon(self) -> Polygon:
        return Polygon(self.dimensions.outline)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = ["MnRectangularBeamDimensions", "MnRectangularBeamSection"]
