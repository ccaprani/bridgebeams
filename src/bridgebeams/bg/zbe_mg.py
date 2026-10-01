"""ЗБЕ ЕООД (Bulgaria) bridge I-girder, mean height 75 cm (drawing MG1).

Source: zbe.bg "Мостови греди" page and drawing MG1.png (cm; see
data/zbe_mg.json). Only the drawn 75 cm girder is implemented; the 95 cm
variant is mentioned in the page text but not drawn. Millimetres, origin at
mid-soffit, y upwards; crossfall as drawn (left edge high).
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
    return json.loads(resources.files("bridgebeams.bg").joinpath("data/zbe_mg.json").read_text(encoding="utf-8"))


@dataclass(frozen=True)
class ZbeMgDimensions:
    """mm. ``left``/``right`` = (fillet_v, underside taper, edge thickness)."""

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
    height_mean: float

    @property
    def web_top(self) -> float:
        return self.flange_side_top + self.haunch_h + self.web_h


class ZbeMgSection:
    """ZBE bridge girder ``MG75`` (Hср = 75 cm)."""

    SIZES = ("MG75",)

    def __init__(self, size: str = "MG75"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        row = data["sizes"][size]
        self.size = size
        self.provenance = row["provenance"]
        self.source_status = data["source_status"]
        self.published = row
        cm = 10.0
        fv = row["fillet_v"]
        self.dimensions = ZbeMgDimensions(
            top_width=row["B"] * cm, web=row["web"] * cm, fillet_h=row["fillet_h"] * cm,
            bottom_width=row["bottom_width"] * cm, haunch_h=row["haunch_h"] * cm,
            flange_side_top=row["side_total"] * cm, chamfer=row["chamfer"] * cm, web_h=row["web_h"] * cm,
            left=(fv * cm, row["left"][0] * cm, row["left"][1] * cm),
            right=(fv * cm, row["right"][0] * cm, row["right"][1] * cm),
            height_left=row["left"][2] * cm, height_right=row["right"][2] * cm,
            height_mean=row["H_mean"] * cm,
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


__all__ = ["ZbeMgDimensions", "ZbeMgSection"]
