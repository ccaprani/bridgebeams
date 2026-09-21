"""Turkish KGM standard precast pretensioned I-girders (I90-I170).

The KGM-lineage family (documented in the technical literature via Ozturk
& Ozturk, IMO; lineage to Yapi Merkezi Prefabrikasyon 2007) comprises four
I-sections - I90, I120, I140, I170 by total depth (900/1200/1400/1700 mm)
- with identical flange and web dimensions across types: top flange
750 wide, bottom flange 750 wide, web 200 thick, flange thickness 150 mm.
Effective spans: I90 18-23 m, I120 24-29 m, I140 30-33 m, I170 34-35 m.
KGM adopts AASHTO / AASHTO LRFD for design; the section and tendon layout
are fixed in each bridge's approved application project.

No published section-property tables exist for the family, so the tests
validate against closed-form analytic values for a plain symmetric
I-girder. The 150 mm flange thickness is assumed constant from the
family's documented worked example - cross-check against KGM-approved
project drawings before fabrication use.

Geometry convention: origin at the middle of the soffit, y positive
upwards, millimetres. Square flange tips (no nibs documented).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon

_DATA_FILE = "kgm_i_sections.json"


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.tr.data").joinpath(_DATA_FILE).read_text()
    )


@dataclass(frozen=True)
class KGMIDimensions:
    """Dimensions of one KGM I-girder size, millimetres."""

    depth: float
    flange_width: float = 750.0
    web_width: float = 200.0
    flange_thickness: float = 150.0

    @property
    def web_height(self) -> float:
        """Clear web height between the flanges."""
        return self.depth - 2.0 * self.flange_thickness

    @property
    def outline(self) -> list[tuple[float, float]]:
        """Full outline, anti-clockwise from the bottom-left soffit corner."""
        fw = self.flange_width / 2.0
        ww = self.web_width / 2.0
        ft = self.flange_thickness
        d = self.depth
        return [
            (-fw, 0.0),
            (fw, 0.0),
            (fw, ft),
            (ww, ft),
            (ww, d - ft),
            (fw, d - ft),
            (fw, d),
            (-fw, d),
            (-fw, d - ft),
            (-ww, d - ft),
            (-ww, ft),
            (-fw, ft),
        ]


class KGMISection:
    """Turkish KGM standard precast I-girder (I90-I170) as a
    ``sectionproperties`` Geometry.

    Examples
    --------
    >>> from bridgebeams.tr import KGMISection
    >>> i140 = KGMISection("I140")
    >>> i140.dimensions.depth
    1400.0
    """

    SIZES = ("I90", "I120", "I140", "I170")

    def __init__(self, size: str = "I140"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        row = next(r for r in data["published_properties"] if r["section"] == size)
        self.size = size
        self.published = row
        self.dimensions = KGMIDimensions(depth=float(row["depth"]))

    @property
    def polygon(self) -> Polygon:
        return Polygon(self.dimensions.outline)

    @property
    def geometry(self):
        """``sectionproperties`` Geometry of the girder (millimetres)."""
        return geometry_from_polygon(self.polygon)

    def analytic_properties(self) -> dict[str, float]:
        """Closed-form geometric properties of the symmetric I-girder.

        Returns the area, centroid height ``cy`` above the soffit, and the
        second moment of area ``ixx`` about the horizontal centroidal axis.
        """
        dims = self.dimensions
        d = dims.depth
        bf = dims.flange_width
        ft = dims.flange_thickness
        ww = dims.web_width
        wh = dims.web_height

        area = 2.0 * bf * ft + ww * wh
        # symmetric about mid-depth
        cy = d / 2.0
        ixx = (
            2.0 * (bf * ft**3 / 12.0 + bf * ft * (d / 2.0 - ft / 2.0) ** 2)
            + ww * wh**3 / 12.0
        )
        return {"area": area, "cy": cy, "ixx": ixx}


__all__ = ["KGMIDimensions", "KGMISection"]
