"""Polish Mosty-Łódź precast prestressed T-girders (T12-T27).

Standard Polish precast pretensioned T-girders (Mosty-Łódź S.A. catalogue
editions 2002/2005/2010; produced by Mosty-Łódź, Betard, FABUD WKB and
SIBET). T-section with a continuously tapered stem: top flange 890 mm
wide, web 200 mm at the top widening linearly to ``B`` at the soffit
(315/360/405/435/465 mm per size). The type number is the nominal
catalogue span in metres; T15 and T18 share one cross-section.

No published section-property tables exist in the captured sources, so
validation is against closed-form values for the trapezoidal-stem
section. The ~210 mm top flange thickness (attested second-hand for T27,
Cieśla 2013) is a constructor parameter - confirm per the Mosty-Łódź
catalogue before structural use.

Geometry convention: origin at the middle of the soffit, y positive
upwards, millimetres. Symmetric about x = 0.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon

_DATA_FILE = "mostostal_t.json"


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.pl.data").joinpath(_DATA_FILE).read_text()
    )


@dataclass(frozen=True)
class MostostalTDimensions:
    """Dimensions of one Mosty-Łódź T-girder size, millimetres."""

    depth: float
    web_bottom_width: float  # stem width B at the soffit
    length_m: float
    length_with_extensions_m: float
    top_flange_width: float = 890.0
    web_top_width: float = 200.0
    top_flange_thickness: float = 210.0  # attested second-hand (T27)

    @property
    def outline(self) -> list[tuple[float, float]]:
        """Full outline, anti-clockwise from the bottom-left soffit corner."""
        h = self.depth
        b = self.web_bottom_width / 2.0
        w = self.web_top_width / 2.0
        f = self.top_flange_width / 2.0
        y1 = h - self.top_flange_thickness
        return [
            (-b, 0.0),
            (b, 0.0),
            (w, y1),
            (f, y1),
            (f, h),
            (-f, h),
            (-f, y1),
            (-w, y1),
        ]


class MostostalTSection:
    """Polish Mosty-Łódź T-girder as a ``sectionproperties`` Geometry.

    Examples
    --------
    >>> from bridgebeams.pl import MostostalTSection
    >>> t27 = MostostalTSection("T27")
    >>> t27.dimensions.depth
    1100.0
    """

    SIZES = ("T12", "T15", "T18", "T21", "T24", "T27")

    def __init__(self, size: str = "T27", *, top_flange_thickness: float = 210.0):
        """
        Parameters
        ----------
        size:
            One of ``T12, T15, T18, T21, T24, T27`` (T22 does not exist).
        top_flange_thickness:
            Attested second-hand (~210 mm, Cieśla 2013, T27); override with
            the catalogue value before structural use.
        """
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        row = next(r for r in data["published_properties"] if r["section"] == size)
        self.size = size
        self.published = row
        self.dimensions = MostostalTDimensions(
            depth=float(row["depth"]),
            web_bottom_width=float(row["web_bottom_width"]),
            length_m=float(row["length_m"]),
            length_with_extensions_m=float(row["length_with_extensions_m"]),
            top_flange_width=float(data["constants"]["top_flange_width"]),
            web_top_width=float(data["constants"]["web_top_width"]),
            top_flange_thickness=float(top_flange_thickness),
        )

    @property
    def polygon(self) -> Polygon:
        return Polygon(self.dimensions.outline)

    @property
    def geometry(self):
        """``sectionproperties`` Geometry of the girder (millimetres)."""
        return geometry_from_polygon(self.polygon)

    def analytic_properties(self) -> dict[str, float]:
        """Closed-form properties of the trapezoidal-stem T-section.

        Top flange rectangle (890 x tf) plus a trapezoidal stem from
        ``web_top_width`` at the flange underside to
        ``web_bottom_width`` at the soffit.
        """
        dims = self.dimensions
        h = dims.depth
        tf = dims.top_flange_thickness
        fw = dims.top_flange_width
        w_top = dims.web_top_width
        w_bot = dims.web_bottom_width
        wh = h - tf

        area_flange = fw * tf
        area_stem = (w_top + w_bot) / 2.0 * wh
        area = area_flange + area_stem

        # stem width varies linearly: w(y) = w_bot + (w_top - w_bot) * y / wh
        # (y measured from the soffit, stem wider at the soffit)
        dw = w_top - w_bot
        # I about the soffit:
        #   stem:  int (w_bot + dw*y/wh) y^2 dy over 0..wh
        #   flange: rectangle about its own centroid + parallel axis
        i_stem_soffit = w_bot * wh**3 / 3.0 + dw * wh**3 / 4.0
        i_flange_soffit = fw * tf**3 / 12.0 + fw * tf * (h - tf / 2.0) ** 2
        i_soffit = i_stem_soffit + i_flange_soffit

        # centroid of the stem trapezoid from the soffit
        # (wide side w_bot at the base): h (w_bot + 2 w_top) / (3 (w_bot + w_top))
        cy_stem = wh * (w_bot + 2.0 * w_top) / (3.0 * (w_bot + w_top))
        cy = (area_flange * (h - tf / 2.0) + area_stem * cy_stem) / area

        ixx = i_soffit - area * cy**2
        return {"area": area, "cy": cy, "ixx": ixx}


__all__ = ["MostostalTDimensions", "MostostalTSection"]
