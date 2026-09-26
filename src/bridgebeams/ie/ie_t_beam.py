"""Irish standard T beams (T1-T10, solid slab construction).

The manufacturer publishes the full vertical stack (chamfer 25, flange side
75, splay 40, tapers 50/50, web H = 85 or 240, top flange F per size) and
the horizontal widths (445 bottom face, 495 flange, 105 web, 205 shoulder
and top flange). With these dims the reconstruction reproduces the
published areas, centroids and inertias of all ten sizes to within 0.02%
- see ``data/ie_t_beam.json``.

Geometry convention: origin at the middle of the soffit, y positive
upwards, millimetres.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources
from typing import Optional

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon, polygon_from_half_profile

_DATA_FILE = "ie_t_beam.json"

# published stack (mm)
_CHAMFER_H = 25.0
_FLANGE_SIDE_H = 75.0
_SPLAY_H = 40.0
_TAPER_H = 50.0

# exact horizontal widths (mm) - see data file "geometry" block
_BOTTOM_FACE = 445.0
_FLANGE_W_AT_25 = 495.0
_FLANGE_W_AT_100 = 485.0
_SHOULDER_W = 205.0
_WEB_W = 105.0
_UPPER_W = 205.0


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.ie.data").joinpath(_DATA_FILE).read_text()
    )


@dataclass(frozen=True)
class IeTBeamDimensions:
    """Dimensions of one T-beam size, millimetres."""

    depth: float
    flange_depth: float  # "F" in the manufacturer table
    web_height: float  # "H" in the manufacturer table (85 or 240)
    bottom_face_width: float = _BOTTOM_FACE
    flange_width: float = _FLANGE_W_AT_25
    flange_width_at_100: float = _FLANGE_W_AT_100
    shoulder_width: float = _SHOULDER_W
    web_width: float = _WEB_W
    top_width: float = _UPPER_W

    @property
    def outline(self) -> list[tuple[float, float]]:
        """Right-half profile, bottom (soffit) to top."""
        r = [
            (self.bottom_face_width / 2, 0.0),
            (self.flange_width / 2, _CHAMFER_H),
            (self.flange_width_at_100 / 2, _CHAMFER_H + _FLANGE_SIDE_H),
            (self.shoulder_width / 2, _CHAMFER_H + _FLANGE_SIDE_H + _SPLAY_H),
            (self.web_width / 2, _CHAMFER_H + _FLANGE_SIDE_H + _SPLAY_H + _TAPER_H),
            (
                self.web_width / 2,
                _CHAMFER_H + _FLANGE_SIDE_H + _SPLAY_H + _TAPER_H + self.web_height,
            ),
            (
                self.top_width / 2,
                _CHAMFER_H
                + _FLANGE_SIDE_H
                + _SPLAY_H
                + _TAPER_H
                + self.web_height
                + _TAPER_H,
            ),
            (
                self.top_width / 2,
                _CHAMFER_H
                + _FLANGE_SIDE_H
                + _SPLAY_H
                + _TAPER_H
                + self.web_height
                + _TAPER_H
                + self.flange_depth,
            ),
        ]
        return r


class IeTBeamSection:
    """Irish standard T beam (T1-T10) as a ``sectionproperties`` Geometry.

    Examples
    --------
    >>> from bridgebeams.ie import IeTBeamSection
    >>> t10 = IeTBeamSection("T10")
    >>> t10.dimensions.depth
    815.0
    """

    SIZES = tuple(f"T{i}" for i in range(1, 11))

    provenance = "transcribed"
    source_status = "producer catalogue (Banagher Bridge Beam Manual 3rd ed.)"

    def __init__(self, size: str = "T5"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        row = next(r for r in data["published_properties"] if r["section"] == size)
        self.size = size
        self.published = row
        self.dimensions = IeTBeamDimensions(
            depth=float(row["depth"]),
            flange_depth=float(row["F"]),
            web_height=float(row["H"]),
        )

    @property
    def polygon(self) -> Polygon:
        return polygon_from_half_profile(self.dimensions.outline)

    @property
    def geometry(self):
        """``sectionproperties`` Geometry of the beam (millimetres)."""
        return geometry_from_polygon(self.polygon)


__all__ = ["IeTBeamDimensions", "IeTBeamSection"]
