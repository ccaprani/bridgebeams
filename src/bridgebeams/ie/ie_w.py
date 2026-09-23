"""Banagher W beams from the third-edition manual and recovered producer CAD.

The current manual supplies all variable upper-web dimensions. A dimensioned
2006 W19 producer drawing supplies the common flat lower contour and 20 mm
bottom chamfers. Its older F/V dimensions are deliberately not substituted for
the current catalogue values. Dimensions are mm, origin at mid-soffit.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon


def _load_data() -> dict:
    return json.loads(resources.files("bridgebeams.ie.data").joinpath("ie_w.json").read_text(encoding="utf-8"))


@dataclass(frozen=True)
class IeWBeamDimensions:
    """Catalogue dimensions plus the CAD-verified common bottom contour."""

    depth: float
    overall_width: float
    inner_top_width: float
    web_height: float
    s: float
    f: float
    v: float = 0.0

    @property
    def outline(self) -> list[tuple[float, float]]:
        outer = self.overall_width / 2
        inner = self.inner_top_width / 2
        y_kink = self.depth - 50 - self.f - self.s
        right = [
            (0, 0), (730, 0), (750, 20),
            (outer, self.depth - 50), (outer - 40, self.depth - 50),
            (outer - 40, self.depth), (inner + 40, self.depth),
            (inner + 40, self.depth - 50), (inner, self.depth - 50),
            (inner, self.depth - 50 - self.f),
            (inner + self.s / 2, y_kink),
        ]
        if self.v:
            right.append((inner + self.s / 2, y_kink - self.v))
        right.extend([(625, 360), (500, 210), (0, 160)])
        return right + [(-x, y) for x, y in reversed(right[1:-1])]


class IeWBeamSection:
    """Gross open W section; sixteen published sizes W1 through W19.

    W2, W4 and W6 are not listed in the source. The concrete inner contour is
    entirely straight segments; reinforcement and local end details are omitted.
    """

    SIZES = ("W1", "W3", "W5", "W7", "W8", "W9", "W10", "W11",
             "W12", "W13", "W14", "W15", "W16", "W17", "W18", "W19")

    # Lower contour and chamfers taken from an older W19 project drawing.
    provenance = "transcribed-with-convention"
    source_status = "producer catalogue (Banagher 3rd ed.) with 2006 producer CAD lower contour"

    def __init__(self, size: str = "W10"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        self.size = size
        self.published = next(r for r in _load_data()["published_properties"] if r["designation"] == size)
        r = self.published
        self.dimensions = IeWBeamDimensions(
            depth=r["depth_mm"], overall_width=r["overall_width_W1_mm"],
            inner_top_width=r["W3_mm"], web_height=r["Web_mm"],
            s=r["S_mm"], f=r["F_mm"], v=r["V_mm"] or 0.0,
        )

    @property
    def polygon(self) -> Polygon:
        return Polygon(self.dimensions.outline)

    @property
    def geometry(self):
        """Return a sectionproperties Geometry in millimetres."""
        return geometry_from_polygon(self.polygon)


__all__ = ["IeWBeamDimensions", "IeWBeamSection"]
