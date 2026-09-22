"""Taiwan Freeway Bureau Type IV-VIII gross midspan I sections.

Source: 橋梁及結構工程設計注意事項, May 2020, Figure 10 and Table 14,
printed page 30 (PDF page 34). The authority specifies precast
post-tensioned girders. These are Taiwanese sections; their Roman type
names do not imply the corresponding AASHTO geometry.

Drawing dimensions are centimetres, converted to millimetres here. The
origin is the soffit centre, y upwards. Gross concrete geometry excludes
tendon ducts, reinforcement and longitudinal end-block thickening.
Table 14 dimensions B and C describe end blocks, not transverse widths.
No published area/centroid/inertia table accompanies the drawing.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.tw")
        .joinpath("data/freeway_i_sections.json")
        .read_text(encoding="utf-8")
    )


@dataclass(frozen=True)
class TaiwanIDimensions:
    """Written dimensions of a gross midspan section, in millimetres.

    Top splay heights are measured downwards from the flange edge. The
    optional inner splay joins ``top_knee_width`` to ``web_width``.
    """

    depth: float
    top_width: float
    bottom_width: float
    web_width: float
    top_edge_height: float
    top_outer_splay_height: float
    bottom_edge_height: float
    bottom_splay_height: float
    top_inner_splay_height: float = 0.0
    top_knee_width: float = 200.0

    @property
    def clear_web_height(self) -> float:
        return self.depth - (
            self.top_edge_height
            + self.top_outer_splay_height
            + self.top_inner_splay_height
            + self.bottom_edge_height
            + self.bottom_splay_height
        )

    @property
    def outline(self) -> list[tuple[float, float]]:
        """Anticlockwise outline, including both bottom flange corners."""
        xw = self.web_width / 2.0
        y_top_edge = self.depth - self.top_edge_height
        y_top_knee = y_top_edge - self.top_outer_splay_height
        right = [
            (self.bottom_width / 2.0, 0.0),
            (self.bottom_width / 2.0, self.bottom_edge_height),
            (xw, self.bottom_edge_height + self.bottom_splay_height),
            (xw, y_top_knee - self.top_inner_splay_height),
        ]
        if self.top_inner_splay_height:
            right.append((self.top_knee_width / 2.0, y_top_knee))
        right.extend(
            [(self.top_width / 2.0, y_top_edge), (self.top_width / 2.0, self.depth)]
        )
        return right + [(-x, y) for x, y in reversed(right)]


class TaiwanISection:
    """Freeway Bureau Type IV, V, VI, VII or VIII gross concrete section.

    Examples
    --------
    >>> from bridgebeams.tw import TaiwanISection
    >>> TaiwanISection("VI").dimensions.depth
    1850.0
    """

    SIZES = ("IV", "V", "VI", "VII", "VIII")

    def __init__(self, size: str = "VI"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        row = data["sections"][size]
        self.size = size
        self.published = row
        self.dimensions = TaiwanIDimensions(
            **{key: float(value) for key, value in row["dimensions_mm"].items()}
        )

    @property
    def polygon(self) -> Polygon:
        return Polygon(self.dimensions.outline)

    @property
    def geometry(self):
        """A ``sectionproperties`` Geometry in millimetres."""
        return geometry_from_polygon(self.polygon)


__all__ = ["TaiwanIDimensions", "TaiwanISection"]
