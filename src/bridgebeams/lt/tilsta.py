"""UAB "Tilsta" (Lithuania) TILTO SIJA precast T-girders S-1150, S-850, S-1000.

Source: UAB "Tilsta" gelžbetonio gaminių katalogas 2025, sheets 04–07 (vector
CAD side views at 1:50; see data/tilsta.json). Solid T-sections with a tapered
web and a curved flange haunch. Millimetres, origin at mid-soffit, y upwards.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon


def _load_data() -> dict:
    return json.loads(resources.files("bridgebeams.lt").joinpath("data/tilsta.json").read_text(encoding="utf-8"))


@dataclass(frozen=True)
class TilstaSijaDimensions:
    """Printed dimensions (mm) plus the right-half outline."""

    depth: float
    top_width: float
    flange: float
    bottom_width: float
    chamfer: float
    half_profile: tuple[tuple[float, float], ...]


class TilstaSijaSection:
    """TILTO SIJA ``S-1150``, ``S-850-710``, ``S-850-700`` or ``S-1000``."""

    SIZES = ("S-1150", "S-850-710", "S-850-700", "S-1000")

    def __init__(self, size: str = "S-1000"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        pr = data["printed"][size]
        self.size = size
        self.published = pr
        self.provenance = data["provenance"][size]
        self.source_status = data["source_status"]
        self.dimensions = TilstaSijaDimensions(
            depth=float(pr["H"]), top_width=float(pr["top_width"]), flange=float(pr["flange"]),
            bottom_width=float(pr["bottom_width"]), chamfer=float(pr["chamfer"]),
            half_profile=tuple(tuple(float(v) for v in p) for p in data["half_profiles_mm"][size]),
        )

    @property
    def polygon(self) -> Polygon:
        right = list(self.dimensions.half_profile)
        return Polygon(right + [(-x, y) for x, y in reversed(right)])

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = ["TilstaSijaDimensions", "TilstaSijaSection"]
