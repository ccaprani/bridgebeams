"""NZTA RR 364 I-beams, drawings S4.01 and S4.10 (PDF pp. 45, 51).

Visually transcribed external profiles, millimetres. The source allows
20 x 20 mm bottom-corner chamfers or 20 mm radii; this implementation
selects the chamfers. Local holes, reinforcement, ducts and the in-situ
slab are omitted. No published section-property table was located.
The 1500 mm dimensions were rechecked against S4.01; small drawn
web-haunch fillets have no labeled radii and use sharp nominal junctions.
Its source locator, hash, labels and conventions are packaged in
``data/nzta_rr364_verified_dimensions.json``. The 1600 mm profile is
retained from the earlier transcription and was not rechecked here.
"""

from dataclasses import dataclass

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon, polygon_from_half_profile
from ._sources import rr364_record


@dataclass(frozen=True)
class NzIBeamDimensions:
    depth: float
    top_width: float
    top_thickness: float
    top_haunch_height: float
    web_width: float
    bottom_width: float
    bottom_thickness: float
    bottom_haunch_height: float
    bottom_chamfer: float = 20.0

    @property
    def outline(self) -> list[tuple[float, float]]:
        b, w, t = self.bottom_width / 2, self.web_width / 2, self.top_width / 2
        c, d = self.bottom_chamfer, self.depth
        right = [
            (b - c, 0), (b, c), (b, self.bottom_thickness),
            (w, self.bottom_thickness + self.bottom_haunch_height),
            (w, d - self.top_thickness - self.top_haunch_height),
            (t, d - self.top_thickness), (t, d),
        ]
        return list(polygon_from_half_profile(right).exterior.coords)[:-1]


class NzIBeamSection:
    """Standard 1500 or 1600 mm precast I-section, soffit at y=0."""

    SIZES = (1500, 1600)

    # Source allows chamfers or radii; chamfers selected.
    provenance = "transcribed-with-convention"
    source_status = "NZTA RR364 standard drawings"

    def __init__(self, depth: int = 1500):
        if depth not in self.SIZES:
            raise ValueError(f"depth must be one of {self.SIZES}, got {depth!r}")
        self.depth = depth
        if depth == 1500:
            self.dimensions = NzIBeamDimensions(**self.source_record["dimensions"])
        else:
            values = (1600, 470, 110, 145, 180, 620, 150, 220)
            self.dimensions = NzIBeamDimensions(*map(float, values))

    @property
    def source_record(self) -> dict | None:
        """Independent source evidence; only the 1500 mm profile was rechecked."""
        return rr364_record("i_1500") if self.depth == 1500 else None

    @property
    def geometry_conventions(self) -> tuple[str, ...]:
        record = self.source_record
        if record is not None:
            return tuple(record["geometry_conventions"])
        return ("Earlier 1600 mm transcription retained without rechecking.",
                "20 mm bottom chamfers and sharp nominal haunch junctions.")

    @property
    def polygon(self) -> Polygon:
        return Polygon(self.dimensions.outline)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = ["NzIBeamDimensions", "NzIBeamSection"]
