"""Bangladesh PC-I girders from the JICA Western Bangladesh Bridges Improvement survey.

Source: Preparatory Survey on Western Bangladesh Bridges Improvement Project,
Final Report, Table 7.4.1 "Summary of Preliminary Design of PC-I", printed
p7-27 (PDF p27 of openjicareport 12231726_02). Spans are 25/30/35/40 m, for
the Roads and Highways Department (RHD).

The sketches print the depth, the full vertical chain, the top-width chain
(80 + 540/640 + 80) and the bottom width. The web width is not printed. It
is fitted to the published section area: 200 mm reproduces 30/35/40 m
exactly, and 180 mm is adopted for 25 m (exact fit 179.5). Preliminary
design only.

Millimetres, origin at mid-soffit, y upwards. Gross midspan concrete only.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon, polygon_from_half_profile


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.bd").joinpath("data/jica_wbbip_pc_i.json").read_text(encoding="utf-8")
    )


@dataclass(frozen=True)
class JicaPcIDimensions:
    """PC-I dimensions (mm). ``top_notch_depth`` is the 70 mm top edge rebate."""

    depth: float
    top_width: float
    top_surface_width: float
    top_notch_depth: float
    top_edge: float
    top_splay: float
    web_height: float
    bottom_splay: float
    bottom_edge: float
    bottom_width: float
    web_width: float

    def __post_init__(self) -> None:
        chain = (self.top_notch_depth + self.top_edge + self.top_splay + self.web_height
                 + self.bottom_splay + self.bottom_edge)
        if abs(chain - self.depth) > 1e-6:
            raise ValueError(f"vertical chain {chain} does not close to depth {self.depth}")

    @property
    def right_half(self) -> list[tuple[float, float]]:
        b, w = self.bottom_width / 2, self.web_width / 2
        t, ts = self.top_width / 2, self.top_surface_width / 2
        y1 = self.bottom_edge
        y2 = y1 + self.bottom_splay
        y3 = y2 + self.web_height
        y4 = y3 + self.top_splay
        y5 = y4 + self.top_edge
        return [(b, 0.0), (b, y1), (w, y2), (w, y3), (t, y4), (t, y5), (ts, y5), (ts, self.depth)]


class JicaPcIGirderSection:
    """Bangladesh (RHD/JICA) PC-I girder: ``"25m"``, ``"30m"``, ``"35m"`` or ``"40m"``."""

    SIZES = ("25m", "30m", "35m", "40m")

    def __init__(self, size: str = "30m") -> None:
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        row = data["sizes"][size]
        self.size = size
        self.record = row
        self.published_area_mm2 = row["published_area_m2"] * 1e6
        self.provenance = row["provenance"]
        self.source_status = data["source_status"]
        self.dimensions = JicaPcIDimensions(**{k: float(v) for k, v in row["dimensions_mm"].items()})

    @property
    def polygon(self) -> Polygon:
        return polygon_from_half_profile(self.dimensions.right_half)

    @property
    def geometry(self):
        """Gross concrete ``sectionproperties`` geometry (mm)."""
        return geometry_from_polygon(self.polygon)


__all__ = ["JicaPcIDimensions", "JicaPcIGirderSection"]
