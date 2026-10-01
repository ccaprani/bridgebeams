"""Tierra Armada (Geoquest, Spain) precast bridge beams traced from brochure sketches.

Source: Tierra Armada S.A., "Precast & Prestressed Beam Bridges" (F_Beams,
May 2012): IL series (PDF p3), IP medium/maximum series (p4), TPP inverted-I
(p5) and wide U / mono-beam series (p11). Only overall widths and depths are
printed; the outlines are traced from the to-scale sketches, so every size is
``provenance = "estimate"``. Millimetres, origin at mid-soffit, y upwards.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.es").joinpath("data/r2_tierra.json").read_text(encoding="utf-8")
    )


@dataclass(frozen=True)
class TierraBeamDimensions:
    """Printed envelope (mm) plus the traced right-half outline (sharp corners)."""

    depth: float
    bottom_width: float
    top_width: float | None
    half_profile: tuple[tuple[float, float], ...]


class TierraBeamSection:
    """IL, IP, TPP and wide-U (TA..A) gross sections from the Tierra Armada brochure."""

    SIZES = ("IL-60", "IL-90", "IL-110", "IP-120", "IP-160", "IP-190", "IP-200",
             "IP-235", "IP-235-A", "IP-255-A", "TPP75", "TPP120", "TPP180",
             "TA90A", "TA150A", "TA210A")
    source_status = "producer brochure (May 2012)"

    def __init__(self, size: str = "IP-160"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        row = data["sizes"][size]
        self.size = size
        self.series = row["series"]
        self.published = row
        self.provenance = row.get("provenance", data["provenance"])
        top = row.get("top_m")
        self.dimensions = TierraBeamDimensions(
            depth=round(row["depth_m"] * 1000, 6),
            bottom_width=round(row["bottom_m"] * 1000, 6),
            top_width=None if top is None else round(top * 1000, 6),
            half_profile=tuple(tuple(p) for p in row["half_profile_mm"]),
        )

    @property
    def polygon(self) -> Polygon:
        right = [p for p in self.dimensions.half_profile if p[0] > 0]
        return Polygon(right + [(-x, y) for x, y in reversed(right)])

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = ["TierraBeamDimensions", "TierraBeamSection"]
