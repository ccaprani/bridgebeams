"""CRH Concrete (Denmark) OT 118 inverted-T bridge beam ("omvendt T-bjælke").

CRH's OT-bjælker product page states the beam is used for its concrete
bridges (DS/EN 15050, C45/55) and gives a dimensioned 'OT 118' outline with a
depth range of 500-1400 mm. Sizes are enumerated at 100 mm steps (a stated
convention; see data/crh_ot.json). Millimetres, origin at mid-soffit, y up.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon


def _load_data() -> dict:
    return json.loads(resources.files("bridgebeams.dk").joinpath("data/crh_ot.json").read_text(encoding="utf-8"))


@dataclass(frozen=True)
class CrhOtDimensions:
    depth: float
    bottom_width: float = 1180.0
    web_width: float = 300.0
    edge_height: float = 140.0
    flange_rise: float = 30.0
    haunch_width: float = 130.0
    haunch_rise: float = 85.0

    @property
    def half_profile(self) -> list[tuple[float, float]]:
        b, w = self.bottom_width / 2, self.web_width / 2
        y1 = self.edge_height
        y2 = y1 + self.flange_rise
        y3 = y2 + self.haunch_rise
        return [(b, 0.0), (b, y1), (w + self.haunch_width, y2), (w, y3), (w, self.depth)]


class CrhOtBeamSection:
    """OT 118 inverted-T bridge beam, H = 500 … 1400 mm (100 mm steps, convention)."""

    SIZES = tuple(f"OT 118/{h}" for h in range(500, 1401, 100))
    source_status = "producer product page (2025)"

    def __init__(self, size: str = "OT 118/1000"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        self.size = size
        self.published = data["printed_mm"]
        self.provenance = data["provenance"]
        self.dimensions = CrhOtDimensions(depth=float(size.split("/")[1]))

    @property
    def polygon(self) -> Polygon:
        right = self.dimensions.half_profile
        return Polygon(right + [(-x, y) for x, y in reversed(right)])

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = ["CrhOtDimensions", "CrhOtBeamSection"]
