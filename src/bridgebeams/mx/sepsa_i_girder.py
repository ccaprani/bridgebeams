"""Mexican SEPSA producer I-girders, from its catalogue page 4.

SEPSA labels these sections AASHTO, but its metric dimensions and modified
types are producer-specific. They are not aliases for US standard sections.
All dimensions are millimetres, with origin at mid-soffit and y upwards.
The published area table validates the drawing transcription; the source
does not provide independent centroid or inertia values for these profiles.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.mx")
        .joinpath("data/sepsa_i_girders.json")
        .read_text(encoding="utf-8")
    )


@dataclass(frozen=True)
class SepsaIGirderDimensions:
    """Drawing dimensions and an exact polygonal profile in millimetres."""

    size: str
    depth: float
    top_flange_width: float
    bottom_flange_width: float
    web_width: float
    right_half: tuple[tuple[float, float], ...]

    @property
    def outline(self) -> list[tuple[float, float]]:
        """Closed by Polygon; both soffit corners are included."""
        return [(-x, y) for x, y in reversed(self.right_half)] + list(
            self.right_half
        )


class SepsaIGirderSection:
    """One of seven SEPSA metric I-girder profiles.

    ``I-MODIFIED`` and ``IV-MODIFIED`` preserve the catalogue's explicit
    modified designations. ``I`` is deliberately not an accepted alias.

    >>> from bridgebeams.mx import SepsaIGirderSection
    >>> SepsaIGirderSection("I-MODIFIED").dimensions.depth
    540.0
    """

    SIZES = ("I-MODIFIED", "II", "III", "IV", "IV-MODIFIED", "V", "VI")

    provenance = "transcribed"
    source_status = "producer catalogue V-05-27-21"

    def __init__(self, size: str = "IV"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        row = next(
            r for r in _load_data()["published_properties"] if r["section"] == size
        )
        self.size = size
        self.published = row
        self.dimensions = SepsaIGirderDimensions(
            size=size,
            depth=10.0 * row["depth_cm"],
            top_flange_width=10.0 * row["top_flange_width_cm"],
            bottom_flange_width=10.0 * row["bottom_flange_width_cm"],
            web_width=10.0 * row["web_width_cm"],
            right_half=tuple((10.0 * x, 10.0 * y) for x, y in row["right_half_cm"]),
        )

    @property
    def polygon(self) -> Polygon:
        return Polygon(self.dimensions.outline)

    @property
    def geometry(self):
        """The beam as a sectionproperties Geometry, in millimetres."""
        return geometry_from_polygon(self.polygon)


__all__ = ["SepsaIGirderDimensions", "SepsaIGirderSection"]
