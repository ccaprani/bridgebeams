"""Irish standard YE edge beams (YE1-YE8, beam & slab construction).

Edge-beam companion to the Y family: a full-height vertical face on one
side (x = -375, the parapet side) and a Y-like lower body on the other.
Manufacturers publish the top width ``Wf``, the centroid offset ``Xc`` from
the vertical face, section properties and strand layouts; the internal
profile is a documented least-squares reconstruction fitted to the
published A, yc, Xc and Ixx of all eight sizes (rms 0.75%, max 1.49% - see
``data/ie_ye_beam.json``).

Geometry convention: origin at the middle of the soffit, y positive
upwards, millimetres. The vertical face sits at x = -375 and published
``Xc`` is measured from it.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources
from typing import Optional

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon

_DATA_FILE = "ie_ye_beam.json"

_SOFFIT_EDGE = 375.0
_FACE_OFFSET = -375.0

# fitted right-side dims (mm) - see data file "fit" block
_CHAMFER = 0.0
_FLANGE_DEPTH = 224.31
_WAIST_HALF_WIDTH = 154.91
_WAIST_HEIGHT = 291.56

# published Wf line (least squares over YE1-YE8): Wf = 373.15 + 0.14419 d
_WF_INTERCEPT = 373.15
_WF_SLOPE = 0.144190


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.ukie.data").joinpath(_DATA_FILE).read_text()
    )


def wf_of_depth(depth: float) -> float:
    """Published top-width law for YE beams (linear fit, R^2 ~ 1)."""
    return _WF_INTERCEPT + _WF_SLOPE * depth


@dataclass(frozen=True)
class IeYEBeamDimensions:
    """Dimensions of one YE-beam size, millimetres."""

    depth: float
    top_width: float
    flange_depth: float
    waist_half_width: float
    waist_height: float
    chamfer: float = _CHAMFER

    @property
    def outline(self) -> list[tuple[float, float]]:
        """Full outline, anti-clockwise from the bottom-left (vertical face)."""
        xl = _FACE_OFFSET
        xr = _SOFFIT_EDGE
        return [
            (xl, 0.0),
            (xr, 0.0),
            (xr - self.chamfer, self.chamfer),
            (xr - self.chamfer, self.flange_depth),
            (self.waist_half_width, self.waist_height),
            (xl + self.top_width, self.depth),
            (xl, self.depth),
        ]


class IeYEBeamSection:
    """Irish standard YE edge beam (YE1-YE8) as a ``sectionproperties``
    Geometry.

    Examples
    --------
    >>> from bridgebeams.ukie import IeYEBeamSection
    >>> ye4 = IeYEBeamSection("YE4")
    >>> ye4.dimensions.depth
    1000.0
    """

    SIZES = tuple(f"YE{i}" for i in range(1, 9))

    def __init__(self, size: str = "YE4", *, depth: Optional[float] = None):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        row = next(r for r in data["published_properties"] if r["section"] == size)
        self.size = size
        self.depth = float(depth) if depth is not None else float(row["depth"])
        self.published = row
        self.dimensions = IeYEBeamDimensions(
            depth=self.depth,
            top_width=wf_of_depth(self.depth),
            flange_depth=_FLANGE_DEPTH,
            waist_half_width=_WAIST_HALF_WIDTH,
            waist_height=_WAIST_HEIGHT,
        )

    @property
    def polygon(self) -> Polygon:
        return Polygon(self.dimensions.outline)

    @property
    def geometry(self):
        """``sectionproperties`` Geometry of the beam (millimetres)."""
        return geometry_from_polygon(self.polygon)


__all__ = ["IeYEBeamDimensions", "IeYEBeamSection", "wf_of_depth"]
