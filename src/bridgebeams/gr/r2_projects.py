"""Greek project-specific precast girders (Dervenakia bridge G3; NTUA Strymonas study).

Neither is a national standard family: each is one dimensioned midspan section
from a public project document (see data/r2_projects.json). Millimetres,
origin at mid-soffit, y upwards.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon


def _load_data() -> dict:
    return json.loads(resources.files("bridgebeams.gr").joinpath("data/r2_projects.json").read_text(encoding="utf-8"))


@dataclass(frozen=True)
class GrProjectGirderDimensions:
    depth: float
    top_width: float
    bottom_width: float
    half_profile: tuple[tuple[float, float], ...]


class GrProjectGirderSection:
    """'Dervenakia-G3' (2.40 m, tender 2022) and 'Strymonas-study' (2.05 m, NTUA 2020)."""

    SIZES = ("Dervenakia-G3", "Strymonas-study")

    def __init__(self, size: str = "Dervenakia-G3"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        row = _load_data()["sections"][size]
        self.size = size
        self.published = row["printed_m"]
        self.provenance = row["provenance"]
        self.source_status = row["source_status"]
        half = tuple(tuple(float(v) for v in p) for p in row["half_profile_mm"])
        self.dimensions = GrProjectGirderDimensions(
            depth=row["printed_m"]["depth"] * 1000, top_width=row["printed_m"]["top_width"] * 1000,
            bottom_width=row["printed_m"]["bottom_width"] * 1000, half_profile=half)

    @property
    def polygon(self) -> Polygon:
        right = list(self.dimensions.half_profile)
        return Polygon(right + [(-x, y) for x, y in reversed(right)])

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = ["GrProjectGirderDimensions", "GrProjectGirderSection"]
