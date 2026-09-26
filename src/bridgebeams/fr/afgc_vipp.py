"""As-surveyed French VIPP post-tensioned I beam (AFGC technical sheet F-04, 2010).

Figure 3 (PDF p7) of Bessoule & Boy, "Ouvrages d'art de type VIPP :
détermination des hypothèses de recalcul à partir de reconnaissances physiques
in situ" dimensions one existing beam at the bearing ("support") and at
mid-span. Modelled asymmetrically as measured; see data/afgc_vipp.json.
Millimetres, x = 0 at the web centreline, y = 0 at the soffit.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon
from shapely.geometry.polygon import orient

from bridgebeams._geometry import geometry_from_polygon


def _load_data() -> dict:
    return json.loads(resources.files("bridgebeams.fr").joinpath("data/afgc_vipp.json").read_text(encoding="utf-8"))


@dataclass(frozen=True)
class AfgcVippDimensions:
    """Printed chains converted to mm (left and right halves as surveyed)."""

    top_parts: tuple[float, float, float]
    bottom_parts: tuple[float, float, float]
    left: dict
    right: dict

    def _side(self, s: dict, sign: float, overhang: float, bottom: float) -> list[tuple[float, float]]:
        w = self.top_parts[1] / 2
        y_web_top = s["bottom_edge"] + s["splay"] + s["web"]
        y_tip = s["tip_underside_to_soffit"]
        return [(sign * (w + bottom), 0.0), (sign * (w + bottom), s["bottom_edge"]),
                (sign * w, s["bottom_edge"] + s["splay"]), (sign * w, y_web_top),
                (sign * (w + overhang), y_tip), (sign * (w + overhang), y_tip + s["tip"])]

    @property
    def outline(self) -> list[tuple[float, float]]:
        right = self._side(self.right, 1.0, self.top_parts[2], self.bottom_parts[2])
        left = self._side(self.left, -1.0, self.top_parts[0], self.bottom_parts[0])
        return right + list(reversed(left))


class AfgcVippBeamSection:
    """AFGC F-04 surveyed VIPP beam: 'support' (bearing) and 'mid-span' sections."""

    SIZES = ("support", "mid-span")
    source_status = "as-surveyed existing VIPP beam (AFGC technical sheet, 2010)"

    def __init__(self, size: str = "mid-span"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        row = data["sections"][size]
        self.size = size
        self.published = row
        self.provenance = data["provenance"]
        mm = lambda d: {k: round(v * 1000.0, 6) for k, v in d.items()}
        self.dimensions = AfgcVippDimensions(
            top_parts=tuple(round(v * 1000, 6) for v in row["top_parts_m"]),
            bottom_parts=tuple(round(v * 1000, 6) for v in row["bottom_parts_m"]),
            left=mm(row["left_m"]), right=mm(row["right_m"]))

    @property
    def polygon(self) -> Polygon:
        return orient(Polygon(self.dimensions.outline), 1.0)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = ["AfgcVippDimensions", "AfgcVippBeamSection"]
