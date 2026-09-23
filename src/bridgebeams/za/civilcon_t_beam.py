"""Civilcon T1–T10 inverted-T ("T beam") gross sections.

PPBT page 1 dimensions a 495 mm base with 25 × 25 mm bottom chamfers, a
6 mm side inset over the 75 mm flange edge, a 40 mm flange-top taper, a
50 mm splay to the 105 mm web, a 50 mm splay to the 205 mm top bulb and
the depth chain (``335 max`` above the upper splay). T1/T2 are drawn dashed:
the web stops 90 mm above the lower splay and a 50 mm splay rises to the
205 mm bulb (the ``90 / 50 / 90`` chain and the ``50`` offset callout).

The width at the flange-taper/splay junction is not printed. A width of
205 mm (the same as the bulb) closes all ten published areas exactly and
matches the drawing; it is recorded as a derived dimension.

The T10 depth label on the drawing reads 850, but the table gives 815,
``335 max`` above the 480 mm splay top gives 815, the 40 mm label pitch gives
815 and the published area closes exactly at 815. This implementation uses
815 and keeps the 850 label as a recorded discrepancy. The published T10
bottom modulus is 0.72% below the value for the outline that reproduces its
area and centroid; that source discrepancy is preserved, not fitted away.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon, polygon_from_half_profile


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.za.data").joinpath("civilcon_t_beams.json").read_text()
    )


@dataclass(frozen=True)
class CivilconTBeamDimensions:
    """Millimetres; origin at the soffit centre, y positive upwards.

    ``web_top`` is the height at which the 105 mm web ends and the upper
    50 mm splay to the bulb begins: 430 for T3–T10, 280 for T1/T2.
    ``taper_width`` (205) is derived from area closure, not printed.
    """

    depth: float
    web_top: float = 430.0
    base_width: float = 495.0
    chamfer: float = 25.0
    side_inset: float = 6.0
    flange_edge_top: float = 100.0
    taper_top: float = 140.0
    taper_width: float = 205.0
    web_bottom: float = 190.0
    web_width: float = 105.0
    upper_splay: float = 50.0
    bulb_width: float = 205.0

    @property
    def outline(self) -> list[tuple[float, float]]:
        """Right half from the soffit centre up to the top centre."""
        b = self.base_width / 2
        return [
            (0.0, 0.0),
            (b - self.chamfer, 0.0),
            (b, self.chamfer),
            (b - self.side_inset, self.flange_edge_top),
            (self.taper_width / 2, self.taper_top),
            (self.web_width / 2, self.web_bottom),
            (self.web_width / 2, self.web_top),
            (self.bulb_width / 2, self.web_top + self.upper_splay),
            (self.bulb_width / 2, self.depth),
            (0.0, self.depth),
        ]


class CivilconTBeamSection:
    """Civilcon T1–T10 gross concrete section (producer catalogue PPBT)."""

    SIZES = tuple(f"T{i}" for i in range(1, 11))

    def __init__(self, size: str = "T5"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        row = next(r for r in data["sections"] if r["section"] == size)
        self.size = size
        self.published = row
        self.provenance = row["provenance"]
        self.source_status = data["source_status"]
        self.dimensions = CivilconTBeamDimensions(
            depth=row["depth_used"], web_top=row["web_top"]
        )

    @property
    def polygon(self) -> Polygon:
        return polygon_from_half_profile(self.dimensions.outline[1:-1])

    @property
    def geometry(self):
        """Return the gross concrete ``sectionproperties`` geometry."""
        return geometry_from_polygon(self.polygon)


__all__ = ["CivilconTBeamDimensions", "CivilconTBeamSection"]
