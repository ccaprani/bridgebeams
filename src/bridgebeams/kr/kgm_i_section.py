"""Korean KHC standard PSC I-girders (25/30/35 m spans; 20/40 m extrapolated).

Korea Expressway Corporation's standard prestressed concrete I-girder
sections. The source paper (Paik, Hwang & Shin, *Computers and Concrete*
6(1), Table 6) publishes the full dimension set per span: top flange
``B1 = H1`` wide × ``H1`` thick, top haunch ``H2`` high, web ``B2`` wide ×
``H3`` clear height, bottom haunch ``H4`` high tapering to the bottom
flange ``B3 = H3`` wide × ``H5`` thick, with ``H1 + H2 + H3 + H4 + H5 =
H`` verified exact for every span. The 35 m section's published
``A = 7,896 cm2`` and ``Ix = 4.644e12 mm4`` are used as validation
targets; the flange-thickness split (H4/H5) is as tabulated.

Geometry convention: origin at the middle of the soffit, y positive
upwards, millimetres. Symmetric about x = 0.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon

_DATA_FILE = "khc_i_girders.json"


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.kr.data").joinpath(_DATA_FILE).read_text()
    )


@dataclass(frozen=True)
class KhcIGirderDimensions:
    """Dimensions of one KHC I-girder size, millimetres."""

    depth: float
    top_flange_width: float  # B1
    web_width: float  # B2
    bottom_flange_width: float  # B3
    top_flange_thickness: float  # H1
    top_haunch_height: float  # H2
    web_clear_height: float  # H3
    bottom_haunch_height: float  # H4
    bottom_flange_thickness: float  # H5

    @property
    def outline(self) -> list[tuple[float, float]]:
        """Right half from the soffit, then mirrored (anti-clockwise).

        Bottom flange sofft = B3 wide for H5; bottom haunch flares to the
        web over H4; web H3 clear; top haunch H2; top flange B1 x H1.
        """
        hw_t = self.top_flange_width / 2.0
        hw_b = self.bottom_flange_width / 2.0
        w = self.web_width / 2.0
        y_web_bot = self.bottom_haunch_height + self.bottom_flange_thickness
        y_web_top = self.depth - self.top_flange_thickness - self.top_haunch_height
        r = [
            (hw_b, 0.0),
            (hw_b, self.bottom_flange_thickness),
            (w, y_web_bot),
            (w, y_web_top),
            (hw_t, y_web_top + self.top_haunch_height),
            (hw_t, self.depth),
        ]
        l = [(-x, y) for x, y in reversed(r)]
        return l + r


class KhcISection:
    """Korean KHC standard PSC I-girder as a ``sectionproperties`` Geometry.

    Examples
    --------
    >>> from bridgebeams.kr import KhcISection
    >>> g = KhcISection("KHC-35")
    >>> g.dimensions.depth
    2200.0
    """

    SIZES = ("KHC-20", "KHC-25", "KHC-30", "KHC-35", "KHC-40")
    STANDARD_SIZES = ("KHC-25", "KHC-30", "KHC-35")  # KHC-recommended; 20/40 extrapolated

    def __init__(self, size: str = "KHC-35"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        row = next(r for r in data["published_properties"] if r["section"] == size)
        self.size = size
        self.published = row
        self.dimensions = KhcIGirderDimensions(
            depth=float(row["depth"]),
            top_flange_width=float(row["b1"]),
            web_width=float(row["b2"]),
            bottom_flange_width=float(row["b3"]),
            top_flange_thickness=float(row["h1"]),
            top_haunch_height=float(row["h2"]),
            web_clear_height=float(row["h3"]),
            bottom_haunch_height=float(row["h4"]),
            bottom_flange_thickness=float(row["h5"]),
        )

    @property
    def polygon(self) -> Polygon:
        return Polygon(self.dimensions.outline)

    @property
    def geometry(self):
        """``sectionproperties`` Geometry of the girder (millimetres)."""
        return geometry_from_polygon(self.polygon)


__all__ = ["KhcIGirderDimensions", "KhcISection"]
