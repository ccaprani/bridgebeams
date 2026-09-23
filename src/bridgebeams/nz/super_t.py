"""NZTA RR 364 Super-T gross sections, dimensions in millimetres.

Visually transcribed from S1.01 (PDF page 8), S1.11 (page 15), and
S1.21 (page 22). These are OPEN TOP twin-web sections. The 1225 section
has a narrower base and thicker bottom than the 1025, rather than just
longer webs. For the 30 m arrangement, use ``top_width=1990``.

This is an explicitly simplified gross profile: the 15 mm formwork ledge
(detail A, depth 45 MAX, not a prescribed depth) is omitted, and its
840 mm clear dimension is placed at the top surface. This adjusts the
inner web taper slightly. The dimensioned 1:10.56 outer slope, lower
valley dimensions, upper 100 x 75 haunches and 20 mm corner chamfers are
retained. No published section-property table validates this approximation.
The source transcription supersedes the earlier interpretation of the
user's S1.01 reading, which mistook the top haunch for bottom chamfers.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon


@dataclass(frozen=True)
class NzSuperTDimensions:
    """Source dimensions; ``bottom_flange_height`` is the valley level.

    ``web_thickness`` records the published nominal 100 mm dimension.
    It does not override the independently dimensioned inner/outer
    boundaries of this simplified profile.
    """

    depth: float
    top_width: float = 2490.0
    bottom_flange_width: float | None = None
    bottom_flange_height: float | None = None
    web_thickness: float = 100.0
    web_clear_top: float = 840.0
    web_clear_bottom: float | None = None
    top_slab_thickness: float = 100.0
    chamfer_width: float = 20.0
    chamfer_height: float = 20.0
    void_rise: float | None = None
    outer_slope: float = 10.56
    haunch_width: float = 100.0
    haunch_height: float = 75.0

    def __post_init__(self):
        if self.depth not in (1025, 1225):
            raise ValueError("depth must be 1025 or 1225 mm")
        if not math.isfinite(self.top_width) or self.top_width not in (1990, 2490):
            raise ValueError("top_width must be 1990 or 2490 mm")
        if self.depth == 1025 and self.top_width != 2490:
            raise ValueError("the 1025 mm drawing specifies top_width=2490")
        values = (852.0, 240.0, 709.0, 67.0) if self.depth == 1025 else (
            814.0, 260.0, 674.0, 64.0
        )
        for name, value in zip(
            ("bottom_flange_width", "bottom_flange_height", "web_clear_bottom", "void_rise"),
            values,
        ):
            if getattr(self, name) is None:
                object.__setattr__(self, name, value)

    @property
    def outline(self) -> list[tuple[float, float]]:
        """Anticlockwise open-top boundary, origin at mid-soffit."""
        d = self.depth
        bf = self.bottom_flange_width / 2.0
        tip = self.top_width / 2.0
        y_haunch = d - self.top_slab_thickness - self.haunch_height
        x_haunch = bf + y_haunch / self.outer_slope
        c, ch = self.chamfer_width, self.chamfer_height
        right = [
            (0.0, 0.0),
            (bf - c, 0.0),
            (bf + ch / self.outer_slope, ch),
            (x_haunch, y_haunch),
            (x_haunch + self.haunch_width, d - self.top_slab_thickness),
            (tip - c, d - self.top_slab_thickness),
            (tip, d - self.top_slab_thickness + ch),
            (tip, d),
            (self.web_clear_top / 2.0, d),
            (self.web_clear_bottom / 2.0, self.bottom_flange_height + self.void_rise),
            (0.0, self.bottom_flange_height),
        ]
        return right + [(-x, y) for x, y in reversed(right[1:-1])]


class NzSuperTSection:
    """Simplified precast Super-T without permanent formwork or deck.

    Default widths follow S1.01/S1.11 (2490 mm); the 1225 mm, 30 m-span
    arrangement S1.21 is selected with ``top_width=1990``. These geometry
    choices do not establish structural capacity for a selected span.
    """

    SIZES = (1025, 1225)

    # Formwork ledge omitted (documented simplification); no property table to validate.
    provenance = "transcribed-with-convention"
    source_status = "NZTA RR364 standard drawings"

    def __init__(self, depth: int = 1025, *, top_width: float = 2490.0):
        self.dimensions = NzSuperTDimensions(depth=float(depth), top_width=float(top_width))
        self.depth = depth

    @property
    def polygon(self) -> Polygon:
        return Polygon(self.dimensions.outline)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = ["NzSuperTDimensions", "NzSuperTSection"]
