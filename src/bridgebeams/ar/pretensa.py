"""Estructuras Pretensa (Argentina) bridge I-beams VI-90…VI-160 and VPI-45.

Source: Estructuras Pretensa, *Puentes* brochure (2 pp.). Page 1 tabulates
six standard "Viga VI" types (depth 0.90–1.60 m, self-weight kg/m, maximum
spans) under an undimensioned deck schematic; page 2 gives the juxtaposed
VPI-45 (0.45 m, 296 kg/m) with its depth dimensioned on the schematic.

**Every profile here is an estimate** (``provenance == "estimate"``). The
outline shape is read from the brochure schematics; widths and flange
proportions were scaled from those drawings (VI: drawing assumed to show
the 1.60 m maximum depth; VPI-45: scaled from its printed 0.45 m). For VI
types the flange thicknesses and tapers are scaled in proportion to depth,
flange widths are held at the scaled 585 mm, and the web width is solved so
that the gross area equals the published self-weight at an assumed
2500 kg/m³. The resulting webs (95–145 mm) are fitted numbers, not
producer dimensions. Millimetres, origin at mid-soffit, y up.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon
from shapely.geometry.polygon import orient

from bridgebeams._geometry import geometry_from_polygon


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.ar")
        .joinpath("data/pretensa_vi.json")
        .read_text(encoding="utf-8")
    )


@dataclass(frozen=True)
class PretensaViDimensions:
    """Estimated plain polygonal I outline, millimetres."""

    depth: float
    flange_width: float
    web_width: float
    top_flange: float
    top_taper: float
    bottom_flange: float
    bottom_taper: float

    @property
    def web_height(self) -> float:
        return self.depth - (
            self.top_flange + self.top_taper + self.bottom_flange + self.bottom_taper
        )

    @property
    def outline(self) -> list[tuple[float, float]]:
        xf, xw, D = self.flange_width / 2, self.web_width / 2, self.depth
        right = [
            (xf, 0.0),
            (xf, self.bottom_flange),
            (xw, self.bottom_flange + self.bottom_taper),
            (xw, D - self.top_flange - self.top_taper),
            (xf, D - self.top_flange),
            (xf, D),
        ]
        return right + [(-x, y) for x, y in reversed(right)]


class PretensaViSection:
    """Pretensa VI-90…VI-160 or VPI-45 (estimated outline).

    >>> PretensaViSection("VI-120").dimensions.depth
    1200.0
    """

    SIZES = ("VI-90", "VI-100", "VI-120", "VI-130", "VI-154", "VI-160", "VPI-45")

    def __init__(self, size: str = "VI-120"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        row = data["types"][size]
        self.size = size
        self.published = row
        self.provenance = row["provenance"]
        self.source_status = data["source_status"]
        self.dimensions = PretensaViDimensions(
            **{k: float(v) for k, v in row["dimensions_mm"].items()}
        )

    @property
    def polygon(self) -> Polygon:
        return orient(Polygon(self.dimensions.outline), sign=1.0)

    @property
    def geometry(self):
        """A ``sectionproperties`` Geometry in millimetres."""
        return geometry_from_polygon(self.polygon)


__all__ = ["PretensaViDimensions", "PretensaViSection"]
