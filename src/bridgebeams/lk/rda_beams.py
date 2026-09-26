"""Sri Lanka Road Development Authority standard PSC bridge beam T/B/505.

The 13.5 m pre-tensioned inverted-T beam (525 mm deep) is drawn on RDA
tender drawing RDA/NWP/T/497-9 (June 2024), PDF p10, as "SECTION OF BEAM",
and is referenced there as Drg No T/B/505. A second RDA tender pack
(Pallanoya-Inginiyagala bridge 3/2 km, PDF p10) confirms the printed web
(100), chamfer (25) and overall depth (525).

Millimetres, origin at mid-soffit, y upwards. Gross precast concrete only.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon, polygon_from_half_profile


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.lk").joinpath("data/rda_tb505.json").read_text(encoding="utf-8")
    )


@dataclass(frozen=True)
class RdaTB505Dimensions:
    """Printed dimensions (mm); the vertical chain runs up from the soffit."""

    depth: float
    top_width: float
    web_width: float
    bottom_width: float
    top_block_height: float
    top_splay: float
    web_height: float
    bottom_splay: float
    bottom_edge: float
    soffit_chamfer: float

    def __post_init__(self) -> None:
        chain = (self.soffit_chamfer + self.bottom_edge + self.bottom_splay
                 + self.web_height + self.top_splay + self.top_block_height)
        if abs(chain - self.depth) > 1e-6:
            raise ValueError(f"vertical chain {chain} does not close to depth {self.depth}")

    @property
    def right_half(self) -> list[tuple[float, float]]:
        b, w, t, c = self.bottom_width / 2, self.web_width / 2, self.top_width / 2, self.soffit_chamfer
        y1 = c + self.bottom_edge
        y2 = y1 + self.bottom_splay
        y3 = y2 + self.web_height
        y4 = y3 + self.top_splay
        return [(b - c, 0.0), (b, c), (b, y1), (w, y2), (w, y3), (t, y4), (t, self.depth)]


class RdaTB505BeamSection:
    """RDA Sri Lanka T/B/505 13.5 m PSC inverted-T beam (``"TB505"``)."""

    SIZES = ("TB505",)

    def __init__(self, size: str = "TB505") -> None:
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        row = data["sizes"][size]
        self.size = size
        self.record = row
        self.length_m = row["length_m"]
        self.provenance = row["provenance"]
        self.source_status = data["source_status"]
        self.dimensions = RdaTB505Dimensions(**{k: float(v) for k, v in row["dimensions_mm"].items()})

    @property
    def polygon(self) -> Polygon:
        return polygon_from_half_profile(self.dimensions.right_half)

    @property
    def geometry(self):
        """Gross concrete ``sectionproperties`` geometry (mm)."""
        return geometry_from_polygon(self.polygon)


__all__ = ["RdaTB505Dimensions", "RdaTB505BeamSection"]
