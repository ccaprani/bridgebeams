"""Classic AASHTO/PCI I-beam Types I–VI from PCI's 2011 Appendix B-7.

These are the gross concrete outlines in the dated PCI reference, not a claim
that every state, producer or other country uses an unmodified section today.
The source table gives D1–D6 and B1–B6 in inches; all API coordinates are mm,
centred horizontally with y=0 at the soffit. Strands, deck and end blocks are
excluded. PDF: https://ems-www.pci.org/PCI_Docs/Design_Resources/Transportation_Resources/AASHTO%20I%20Beams.pdf
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon

INCH_MM = 25.4


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.us")
        .joinpath("data/aashto_i_beams.json")
        .read_text(encoding="utf-8")
    )


@dataclass(frozen=True)
class AashtoIBeamDimensions:
    """PCI D1–D6 and B1–B6 dimensions, converted to millimetres."""

    d1: float
    d2: float
    d3: float
    d4: float
    d5: float
    d6: float
    b1: float
    b2: float
    b3: float
    b4: float
    b5: float
    b6: float

    @property
    def outline(self) -> list[tuple[float, float]]:
        """Counterclockwise vertices of the symmetric gross outline."""
        if abs(self.b1 - self.b3 - 2 * (self.b4 + self.b5)) > 1e-8:
            raise ValueError("upper width dimension chain does not close")
        if abs(self.b2 - self.b3 - 2 * self.b6) > 1e-8:
            raise ValueError("lower width dimension chain does not close")
        web_top = self.d1 - self.d2 - self.d3 - self.d4
        web_bottom = self.d6 + self.d5
        if web_top <= web_bottom:
            raise ValueError("vertical dimension chain leaves no web")
        right = [
            (self.b2 / 2, 0.0),
            (self.b2 / 2, self.d6),
            (self.b3 / 2, web_bottom),
            (self.b3 / 2, web_top),
        ]
        if self.d3 or self.b5:
            right.append((self.b3 / 2 + self.b4, self.d1 - self.d2 - self.d3))
        right.extend([(self.b1 / 2, self.d1 - self.d2), (self.b1 / 2, self.d1)])
        return [(-x, y) for x, y in reversed(right)] + right


class AashtoIBeamSection:
    """2011 PCI reference Type I, II, III, IV, V or VI."""

    SIZES = ("I", "II", "III", "IV", "V", "VI")

    provenance = "transcribed"
    source_status = "historic standard (PCI BDM App. B-7, Nov 2011)"

    def __init__(self, size: str = "I") -> None:
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        row = _load_data()["sections"][size]
        self.size = size
        self.published = row["published"]
        self.dimensions = AashtoIBeamDimensions(
            *(value * INCH_MM for value in row["dimensions"])
        )

    @property
    def polygon(self) -> Polygon:
        return Polygon(self.dimensions.outline)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = ["AashtoIBeamDimensions", "AashtoIBeamSection"]
