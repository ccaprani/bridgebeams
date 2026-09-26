"""WIKA Beton (Indonesia) precast bridge girders from the July 2022 brochure.

Source: WIKA Beton *Brosur WTON 2022*, PDF pages 17 (PC-U), 18 (PC-I),
20 (bulb tee) and 22 (channel girders). Origin at mid-soffit, y upwards,
millimetres.

* :class:`WikaChannelGirderSection` – CG60/70/80/100 × 1200 pretensioned
  channel ("precast bridge floor") units. Width and depth chains are
  printed; the side shear key, inner haunch rise and corner chamfers are
  undimensioned and were fitted (common values for all four sizes) to the
  published area and inertia. Provenance ``"fitted-reconstruction"``.
* :class:`WikaPcIGirderSection`, :class:`WikaPcUGirderSection`,
  :class:`WikaBulbTeeSection` – the brochure prints only depth, widths and
  web thickness. Outlines are **best estimates**: the brochure's (non-
  uniformly scaled) vector drawing gives the proportions, and flange depths
  are scaled to reproduce the published A and I (PC-U: one common fit for
  all six sizes, residuals up to 1.3 %). Provenance ``"estimate"``; do not
  treat them as manufacturer drawings.

Per-size coordinates, fit factors and residuals live in
``data/wika_girders.json``.
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
        resources.files("bridgebeams.id")
        .joinpath("data/wika_girders.json")
        .read_text(encoding="utf-8")
    )


@dataclass(frozen=True)
class WikaGirderDimensions:
    """Printed overall dimensions (mm) plus the implemented right half."""

    size: str
    depth: float
    top_width: float
    right_half: tuple[tuple[float, float], ...]
    bottom_width: float | None = None
    web_width: float | None = None


class _WikaSection:
    _key: str = ""
    _open_ring = False  # True: right half is an open chain mirrored as one ring
    SIZES: tuple[str, ...] = ()

    def __init__(self, size: str):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        fam = data[self._key]
        row = next(s for s in fam["sections"] if s["size"] == size)
        self.size = size
        self.published = row
        self.provenance = row["provenance"]
        self.source_status = data["source_status"]
        self.dimensions = WikaGirderDimensions(
            size=size,
            depth=float(row["depth_mm"]),
            top_width=float(row["top_width_mm"]),
            bottom_width=row.get("bottom_width_mm"),
            web_width=row.get("web_width_mm"),
            right_half=tuple((float(x), float(y)) for x, y in row["right_half_mm"]),
        )

    @property
    def polygon(self) -> Polygon:
        r = list(self.dimensions.right_half)
        if self._open_ring:
            ring = r + [(-x, y) for x, y in reversed(r)]
        else:
            left = [(-x, y) for x, y in reversed(r)]
            ring = left + r
        return orient(Polygon(ring), sign=1.0)

    @property
    def geometry(self):
        """The gross section as a sectionproperties Geometry, in millimetres."""
        return geometry_from_polygon(self.polygon)


class WikaChannelGirderSection(_WikaSection):
    """WIKA CG channel girder, 1200 mm wide (fitted reconstruction).

    >>> from bridgebeams.id import WikaChannelGirderSection
    >>> WikaChannelGirderSection("CG80").polygon.bounds
    (-600.0, 0.0, 600.0, 800.0)
    """

    _key = "channel"
    _open_ring = True
    SIZES = ("CG60", "CG70", "CG80", "CG100")

    def __init__(self, size: str = "CG80"):
        super().__init__(size)


class WikaPcIGirderSection(_WikaSection):
    """WIKA post-tensioned PC-I girder (estimate fitted to published A, I)."""

    _key = "pc_i"
    SIZES = ("H90", "H125", "H160", "H170", "H210")

    def __init__(self, size: str = "H170"):
        super().__init__(size)


class WikaPcUGirderSection(_WikaSection):
    """WIKA post-tensioned PC-U girder (estimate, common fit to A, I)."""

    _key = "pc_u"
    _open_ring = True  # right half: soffit corner ... bottom-slab top edge
    SIZES = ("H120", "H140", "H165", "H185", "H210", "H230")

    def __init__(self, size: str = "H185"):
        super().__init__(size)


class WikaBulbTeeSection(_WikaSection):
    """WIKA PC bulb tee H-220 (estimate fitted to published A, I)."""

    _key = "bulb_tee"
    SIZES = ("H220",)

    def __init__(self, size: str = "H220"):
        super().__init__(size)


__all__ = [
    "WikaBulbTeeSection",
    "WikaChannelGirderSection",
    "WikaGirderDimensions",
    "WikaPcIGirderSection",
    "WikaPcUGirderSection",
]
