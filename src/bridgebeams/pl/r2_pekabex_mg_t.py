"""Pekabex / Mosty Gdańsk MG-T pretensioned bridge beams, span section (estimate).

Source: "System strunobetonowych belek prefabrykowanych typu MG-T", Pekabex /
Mosty Gdańsk catalogue (2023), PDF p3 section C–C (przekrój przęsłowy) and
PDF p6 table (MG-T18 … MG-T46, H = 0.90–2.10 m).

Only the top width (2390), span web (220) and depth H are printed; the flanges
are scaled from the to-scale vector outline. ``provenance = "estimate"``.
Millimetres, origin at mid-soffit, y upwards.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon
from bridgebeams.hu._fillet import fillet_polyline


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.pl").joinpath("data/r2_pekabex_mg_t.json").read_text(encoding="utf-8")
    )


@dataclass(frozen=True)
class PekabexMgtDimensions:
    """Span-section dimensions (mm); only top_width, web_width and depth are printed."""

    depth: float
    top_width: float = 2390.0
    web_width: float = 220.0
    bottom_width: float = 720.0
    bottom_edge_height: float = 250.0
    bottom_splay_top: float = 360.0
    web_top_below_top: float = 260.0
    haunch_half_width: float = 230.0
    flange_root_thickness: float = 150.0
    flange_tip_thickness: float = 80.0

    @property
    def outline(self) -> list[tuple[float, float]]:
        """Right half, from (0, 0) to (0, depth), with fitted fillets."""
        h = self.depth
        verts = [
            (0.0, 0.0, 0.0),
            (self.bottom_width / 2, 0.0, 45.0),
            (self.bottom_width / 2, self.bottom_edge_height, 50.0),
            (self.web_width / 2, self.bottom_splay_top, 20.0),
            (self.web_width / 2, h - self.web_top_below_top, 5.0),
            (self.haunch_half_width, h - self.flange_root_thickness, 5.0),
            (self.top_width / 2, h - self.flange_tip_thickness, 45.0),
            (self.top_width / 2, h, 0.0),
            (0.0, h, 0.0),
        ]
        return fillet_polyline(verts)


class PekabexMgtSection:
    """MG-T span (przęsłowy) gross concrete section, sizes MG-T18 … MG-T46."""

    SIZES = ("MG-T18", "MG-T21", "MG-T24", "MG-T27", "MG-T30",
             "MG-T33", "MG-T36", "MG-T39", "MG-T42", "MG-T46")
    source_status = "producer catalogue (2023)"

    def __init__(self, size: str = "MG-T30"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        row = data["sizes"][size]
        self.size = size
        self.published = row
        self.provenance = row.get("provenance", data["provenance"])
        self.dimensions = PekabexMgtDimensions(depth=round(row["depth_m"] * 1000.0, 6))

    @property
    def polygon(self) -> Polygon:
        right = self.dimensions.outline
        ring = right[:-1] + [(-x, y) for x, y in reversed(right[1:-1])]
        return Polygon(ring)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = ["PekabexMgtDimensions", "PekabexMgtSection"]
