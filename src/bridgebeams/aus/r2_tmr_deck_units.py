"""Queensland TMR transversely stressed PSC deck units, 596 mm wide.

Source: Department of Transport and Main Roads (Queensland) Standard
Drawings 2050/2051 (10/11 m), 2052/2053 (12/13 m), 2055 (15 m), 2059
(19 m) and 2065 (25 m), each drawing 3 of 6, SECTION C "Typical section
inner units"; common rules on Standard Drawing 2042 (void chamfer
75 x 75, 596 mm width). CC BY 4.0, (c) State of Queensland (TMR).

All outline dimensions are printed. Origin at mid-soffit, y up, mm.
Voided units carry one octagonal void (75 x 75 corner chamfers) as a
polygon interior. Local end recesses, hold-down holes and transverse
stressing ducts are not part of the gross midspan section.

These are Queensland-specific units; this module uses the frozen
dataclass/Section interface, not the legacy ``bridgebeams.aus`` API.
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
        resources.files("bridgebeams.aus")
        .joinpath("data/r2_tmr_deck_units.json")
        .read_text(encoding="utf-8")
    )


@dataclass(frozen=True)
class TmrDeckUnitDimensions:
    """Printed SECTION C dimensions (mm). ``void_height`` 0 = solid unit."""

    depth: float
    width: float = 596.0
    soffit_chamfer: float = 25.0
    void_side_cover: float = 0.0
    void_bottom: float = 0.0
    void_height: float = 0.0
    void_fillet: float = 0.0

    @property
    def void_width(self) -> float:
        return self.width - 2.0 * self.void_side_cover if self.void_height else 0.0

    @property
    def void_top_cover(self) -> float:
        return self.depth - self.void_bottom - self.void_height if self.void_height else 0.0

    def outline(self) -> list[tuple[float, float]]:
        b, c, d = self.width / 2.0, self.soffit_chamfer, self.depth
        return [(-b + c, 0.0), (b - c, 0.0), (b, c), (b, d), (-b, d), (-b, c)]

    def void(self) -> list[tuple[float, float]] | None:
        if not self.void_height:
            return None
        w, f = self.void_width / 2.0, self.void_fillet
        y0, y1 = self.void_bottom, self.void_bottom + self.void_height
        return [(-w + f, y0), (w - f, y0), (w, y0 + f), (w, y1 - f),
                (w - f, y1), (-w + f, y1), (-w, y1 - f), (-w, y0 + f)]


class TmrDeckUnitSection:
    """TMR 596 mm PSC deck unit gross midspan section, keyed by depth.

    Examples
    --------
    >>> from bridgebeams.aus.r2_tmr_deck_units import TmrDeckUnitSection
    >>> TmrDeckUnitSection("1100").spans_m
    (25,)
    """

    SIZES = ("500", "540", "650", "760", "1100")
    source_status = "current TMR standard drawing (2018/2025 issues)"

    def __init__(self, size: str = "760"):
        size = str(size)
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        row = _load_data()["sections"][size]
        self.size = size
        self.published = row
        self.provenance = row["provenance"]
        self.spans_m = tuple(row["spans_m"])
        v = row["void"] or {}
        self.dimensions = TmrDeckUnitDimensions(
            depth=float(row["depth"]),
            width=float(row["width"]),
            soffit_chamfer=float(row["soffit_chamfer"]),
            void_side_cover=float(v.get("side_cover", 0.0)),
            void_bottom=float(v.get("bottom", 0.0)),
            void_height=float(v.get("height", 0.0)),
            void_fillet=float(v.get("fillet", 0.0)),
        )

    @property
    def polygon(self) -> Polygon:
        d = self.dimensions
        hole = d.void()
        return orient(Polygon(d.outline(), [hole] if hole else []), sign=1)

    @property
    def geometry(self):
        """A ``sectionproperties`` Geometry in millimetres."""
        return geometry_from_polygon(self.polygon)


__all__ = ["TmrDeckUnitDimensions", "TmrDeckUnitSection"]
