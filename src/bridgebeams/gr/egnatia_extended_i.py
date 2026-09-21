"""Greek standard extended-I precast bridge beams (Egnatia proposal).

Marinelli et al. (Frontiers in Built Environment 6:119, 2020, open access)
propose 45 standard extended-I sections for Greek highway bridges: 15
lengths (22.00-43.00 m in 1.5 m steps) x 3 effective deck-width classes,
with the depth given by the paper's law ``D = -0.303 + 0.047 L + 0.248
Weff`` (m), constant flange widths (top 1400, bottom 750) and a
depth-dependent web width (300/320/340 mm).

The paper publishes lengths, depths and flange **widths**; flange
**thicknesses** are design choices left open by the standardisation
proposal, so they are REQUIRED constructor arguments here (nothing is
assumed). Pass your design values, e.g. ``top_flange_thickness=200,
bottom_flange_thickness=300``.

Geometry convention: origin at the middle of the soffit, y positive
upwards, millimetres. Symmetric about x = 0.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon

_DATA_FILE = "egnatia_extended_i.json"

_TOP_FLANGE = 1400.0
_BOTTOM_FLANGE = 750.0


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.gr.data").joinpath(_DATA_FILE).read_text()
    )


def standard_depth(length_m: float, weff_m: float) -> float:
    """Published standard depth (m) for a span/deck-width class.

    Uses the paper's Table 6 exactly; spans between the 15 standard
    lengths select the next-longer standard length (the paper's
    "round to the safe side" rule).
    """
    data = _load_data()
    table = data["table_depths_m"]
    lengths = sorted(float(k) for k in table)
    weffs = data["weff_classes_m"]
    length_key = None
    for L in lengths:
        if length_m <= L:
            length_key = L
            break
    if length_key is None:
        raise ValueError(f"span {length_m} m exceeds the longest standard "
                         f"length {lengths[-1]} m")
    iw = weffs.index(min(weffs, key=lambda w: abs(w - weff_m)))
    return table[str(length_key)][iw]


def depth_law(length_m: float, weff_m: float) -> float:
    """Least-squares law reproducing Table 6 (max residual 4.2 cm):

    ``D = 0.0573 + 0.03135 L + 0.250 Weff`` (m).
    """
    return 0.0573 + 0.03135 * length_m + 0.250 * weff_m


def web_width(depth_m: float) -> float:
    """Greek Ministry minimum web width rule, by depth (mm)."""
    for limit, ww in _load_data()["web_rule"]:
        if depth_m <= limit:
            return ww
    raise ValueError(f"depth {depth_m} m outside the web-width rule")


@dataclass(frozen=True)
class EgnatiaIDimensions:
    """Dimensions of one extended-I size, millimetres."""

    length_m: float
    weff_m: float
    depth: float
    web_width: float
    top_flange_width: float
    bottom_flange_width: float
    top_flange_thickness: float
    bottom_flange_thickness: float

    @property
    def outline(self) -> list[tuple[float, float]]:
        d = self.depth
        t = self.top_flange_width / 2.0
        b = self.bottom_flange_width / 2.0
        w = self.web_width / 2.0
        y1 = d - self.top_flange_thickness
        y3 = self.bottom_flange_thickness
        return [
            (-b, 0.0),
            (b, 0.0),
            (b, y3),
            (w, y3),
            (w, y1),
            (t, y1),
            (t, d),
            (-t, d),
            (-t, y1),
            (-w, y1),
            (-w, y3),
            (-b, y3),
        ]


class GrExtendedISection:
    """Greek standard extended-I beam as a ``sectionproperties`` Geometry.

    Examples
    --------
    >>> from bridgebeams.gr import GrExtendedISection
    >>> g = GrExtendedISection(span_m=35.0, weff_m=2.5,
    ...                        top_flange_thickness=200,
    ...                        bottom_flange_thickness=300)
    >>> round(g.dimensions.depth, 3)
    1.94
    """

    LENGTHS_M = (22.0, 23.5, 25.0, 26.5, 28.0, 29.5, 31.0, 32.5, 34.0, 35.5,
                 37.0, 38.5, 40.0, 41.5, 43.0)
    WEFF_CLASSES_M = (2.0, 2.5, 3.0)

    def __init__(
        self,
        span_m: float = 35.0,
        weff_m: float = 2.5,
        *,
        top_flange_thickness: float,
        bottom_flange_thickness: float,
    ):
        """
        Parameters
        ----------
        span_m:
            Beam length in metres (22.0-43.0; the paper's 15 standard values
            are in ``LENGTHS_M``).
        weff_m:
            Effective deck width class (2.0 / 2.5 / 3.0).
        top_flange_thickness, bottom_flange_thickness:
            Design values (mm) - the source proposal leaves these to the
            designer, so they are required.
        """
        if span_m <= 0 or weff_m <= 0:
            raise ValueError("span_m and weff_m must be positive")
        if top_flange_thickness <= 0 or bottom_flange_thickness <= 0:
            raise ValueError("flange thicknesses must be positive")
        self.span_m = span_m
        self.weff_m = weff_m
        std_d = standard_depth(span_m, weff_m)
        self.dimensions = EgnatiaIDimensions(
            length_m=span_m,
            weff_m=weff_m,
            depth=std_d * 1000.0,
            web_width=web_width(std_d),
            top_flange_width=_TOP_FLANGE,
            bottom_flange_width=_BOTTOM_FLANGE,
            top_flange_thickness=float(top_flange_thickness),
            bottom_flange_thickness=float(bottom_flange_thickness),
        )

    @property
    def polygon(self) -> Polygon:
        return Polygon(self.dimensions.outline)

    @property
    def geometry(self):
        """``sectionproperties`` Geometry of the beam (millimetres)."""
        return geometry_from_polygon(self.polygon)


__all__ = [
    "EgnatiaIDimensions",
    "GrExtendedISection",
    "depth_law",
    "web_width",
]
