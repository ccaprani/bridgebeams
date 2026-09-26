"""Rila (Kyustendil, Bulgaria) ГТ 75 … ГТ 185 precast bridge I-girders.

Source: Строителна фирма Рила, "Елементи за пътно строителство" web page,
drawings capture17/18/19 (cm; see data/rila_gt.json). The top flange carries a
2.5 % crossfall exactly as drawn for each size, so outlines are asymmetric.
Millimetres, origin at mid-soffit, y upwards.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon
from shapely.geometry.polygon import orient

from bridgebeams._geometry import geometry_from_polygon

from ._ibeam import crossfall_i_outline


def _load_data() -> dict:
    return json.loads(resources.files("bridgebeams.bg").joinpath("data/rila_gt.json").read_text(encoding="utf-8"))


@dataclass(frozen=True)
class RilaGtDimensions:
    """Printed dimensions converted to mm. ``left``/``right`` = (fillet_v, taper, edge thickness)."""

    top_width: float
    web: float
    fillet_h: float
    bottom_width: float
    haunch_h: float
    flange_side_top: float
    chamfer: float
    web_h: float
    left: tuple[float, float, float]
    right: tuple[float, float, float]
    height_left: float
    height_right: float

    @property
    def web_top(self) -> float:
        return self.flange_side_top + self.haunch_h + self.web_h


class RilaGtSection:
    """ГТ-series I-girder (``GT75``, ``GT95``, ``GT115``, ``GT140``, ``GT185``)."""

    SIZES = ("GT75", "GT95", "GT115", "GT140", "GT185")

    def __init__(self, size: str = "GT115"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        row = data["sizes"][size]
        self.size = size
        self.name_original = row["name_original"]
        self.provenance = row["provenance"]
        self.source_status = data["source_status"]
        self.published = row
        cm = 10.0
        self.dimensions = RilaGtDimensions(
            top_width=row["B"] * cm, web=row["web"] * cm, fillet_h=row["fillet_h"] * cm,
            bottom_width=row["bottom_width"] * cm, haunch_h=row["haunch_h"] * cm,
            flange_side_top=(row["chamfer"] + row["side_h"]) * cm, chamfer=row["chamfer"] * cm,
            web_h=row["web_h"] * cm,
            left=tuple(round(v * cm, 6) for v in row["left"][:3]),
            right=tuple(round(v * cm, 6) for v in row["right"][:3]),
            height_left=row["left"][3] * cm, height_right=row["right"][3] * cm,
        )

    @property
    def polygon(self) -> Polygon:
        d = self.dimensions
        pts = crossfall_i_outline(top_width=d.top_width, web=d.web, fillet_h=d.fillet_h,
                                  bottom_width=d.bottom_width, haunch_h=d.haunch_h,
                                  flange_side_top=d.flange_side_top, chamfer=d.chamfer,
                                  web_top=d.web_top, left=d.left, right=d.right)
        return orient(Polygon(pts), 1.0)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = ["RilaGtDimensions", "RilaGtSection"]
