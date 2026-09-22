"""Ontario MTO SS107-25 (June 2025) prestressed solid slabs.

Typical gross concrete section from drawing 107.0025: 1220 mm wide,
S300/S400/S500 deep, with the shown 20 x 20 mm bottom chamfers. The
section excludes reinforcement, strands, local holes and end details.
The source is an Ontario standard drawing and must not be attributed to
Canada as a whole. All coordinates are millimetres, y=0 at the soffit.
"""

from dataclasses import dataclass

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon


@dataclass(frozen=True)
class CaMtoSolidSlabDimensions:
    depth: float
    width: float = 1220.0
    bottom_chamfer: float = 20.0

    @property
    def outline(self) -> list[tuple[float, float]]:
        w, d, c = self.width / 2, self.depth, self.bottom_chamfer
        return [(-w + c, 0), (w - c, 0), (w, c), (w, d),
                (-w, d), (-w, c)]


class CaMtoSolidSlabSection:
    """Ontario prestressed slab S300, S400 or S500, as drawn in SS107-25."""

    SIZES = ("S300", "S400", "S500")

    def __init__(self, size: str = "S300"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        self.size = size
        self.dimensions = CaMtoSolidSlabDimensions(depth=float(size[1:]))

    @property
    def polygon(self) -> Polygon:
        return Polygon(self.dimensions.outline)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = ["CaMtoSolidSlabDimensions", "CaMtoSolidSlabSection"]
