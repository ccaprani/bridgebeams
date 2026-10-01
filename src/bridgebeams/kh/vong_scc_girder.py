"""Cambodian short-span PC I-girder from a Kochi University of Technology thesis.

Source: VONG Seng (2006), *Design of Prestressed Concrete Bridge Girder
Using Self-Compacting Concrete for Cambodian Rehabilitation*, doctoral
dissertation, Kochi University of Technology, Fig. 3.3.2 (PDF p30, printed
p28): girder TB_12_f60, 850 mm deep, selected for a 12 t self-weight limit.
A real-scale girder was produced and monitored in Cambodia. This is a
research design, not a Ministry of Public Works and Transport standard.
Millimetres, origin at mid-soffit, y upwards.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon
from shapely.geometry.polygon import orient

from bridgebeams._geometry import geometry_from_polygon, polygon_from_half_profile


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.kh")
        .joinpath("data/vong_scc_girder.json")
        .read_text(encoding="utf-8")
    )


@dataclass(frozen=True)
class KhVongGirderDimensions:
    depth: float
    top_width: float
    top_edge: float
    top_flange_zone: float
    web: float
    web_height: float
    bottom_zone: float
    bottom_edge: float
    bottom_width: float

    @property
    def right_half(self) -> list[tuple[float, float]]:
        b, w, t = self.bottom_width / 2, self.web / 2, self.top_width / 2
        return [(b, 0.0), (b, self.bottom_edge), (w, self.bottom_zone),
                (w, self.bottom_zone + self.web_height),
                (t, self.depth - self.top_edge), (t, self.depth)]


class KhVongGirderSection:
    """Thesis girder ``"TB_12_f60"`` (850 mm, 580/150/350 mm).

    Examples
    --------
    >>> KhVongGirderSection().polygon.area
    236900.0
    """

    SIZES = ("TB_12_f60",)
    source_status = "doctoral-thesis study design (Kochi University of Technology, 2006)"

    def __init__(self, size: str = "TB_12_f60"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        row = _load_data()["sections"][size]
        self.size = size
        self.published = row
        self.provenance = row["provenance"]
        self.dimensions = KhVongGirderDimensions(**{k: float(v) for k, v in row["dimensions_mm"].items()})

    @property
    def polygon(self) -> Polygon:
        return orient(polygon_from_half_profile(self.dimensions.right_half), sign=1.0)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = ["KhVongGirderDimensions", "KhVongGirderSection"]
