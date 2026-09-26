"""Banagher Solid Box beams, nominal drawing outlines for width classes (1) through (4).

The 3rd-edition Bridge Beam Manual, PDF page 14 / printed page 12,
defines eight depths for each of the 495, 750, 970 and 1500 mm overall widths.
The polygon follows the drawing dimensions directly. Width class (4),
1500 mm, retains the nominal drawing despite a recorded source-property
discrepancy; its properties are calculated from geometry, not fitted to the table.

Dimensions are millimetres, with origin at mid-soffit and y upwards.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.ie.data")
        .joinpath("ie_solid_box.json")
        .read_text(encoding="utf-8")
    )


@dataclass(frozen=True)
class IeSolidBoxBeamDimensions:
    """Explicit nominal drawing dimensions for one solid box beam."""

    depth: float
    base_width: float
    side_projection: float = 65.0
    shoulder_rise: float = 30.0
    outer_vertical_face: float = 35.0
    bottom_chamfer: float = 25.0

    @property
    def top_width(self) -> float:
        return self.base_width - 2 * self.side_projection

    @property
    def outline(self) -> list[tuple[float, float]]:
        outside_x = self.base_width / 2
        shoulder_bottom_y = self.bottom_chamfer + self.outer_vertical_face
        right = [
            (outside_x - self.bottom_chamfer, 0.0),
            (outside_x, self.bottom_chamfer),
            (outside_x, shoulder_bottom_y),
            (self.top_width / 2, shoulder_bottom_y + self.shoulder_rise),
            (self.top_width / 2, self.depth),
        ]
        return [(-x, y) for x, y in reversed(right)] + right


class IeSolidBoxBeamSection:
    """A Banagher Solid Box profile with its source width-class designation.

    ``SD1 (1)`` is 300 mm deep and 495 mm wide; ``SD8 (3)`` is
    1000 mm deep and 970 mm wide. Class (4) is 1500 mm wide and its source
    area exceeds nominal geometry by 225/275 mm²; see source metadata.

    >>> from bridgebeams.ie.ie_solid_box import IeSolidBoxBeamSection
    >>> IeSolidBoxBeamSection("SD4 (2)").dimensions.depth
    600.0
    """

    SIZES = tuple(f"SD{i} ({width})" for width in (1, 2, 3, 4) for i in range(1, 9))

    provenance = "transcribed"

    @property
    def source_status(self) -> str:
        base = "producer catalogue (Banagher Bridge Beam Manual 3rd ed.)"
        if self.size.endswith("(4)"):
            return base + "; nominal drawing, published area differs by 225/275 mm2"
        return base

    def __init__(self, size: str = "SD4 (2)"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        row = next(
            row for row in _load_data()["published_properties"]
            if row["designation"] == size
        )
        self.size = size
        self.published = row
        self.dimensions = IeSolidBoxBeamDimensions(
            depth=float(row["depth_mm"]),
            base_width=float(row["overall_base_width_mm"]),
        )

    @property
    def polygon(self) -> Polygon:
        return Polygon(self.dimensions.outline)

    @property
    def geometry(self):
        """Return a sectionproperties Geometry in millimetres."""
        return geometry_from_polygon(self.polygon)


__all__ = ["IeSolidBoxBeamDimensions", "IeSolidBoxBeamSection"]
