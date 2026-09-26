"""Irish standard Y-beam (Y1-Y8) section, reconstructing the Banagher range.

The manufacturers (Banagher, Concast, Shay Murtagh - common industry range)
publish the top flange width ``Wf`` per size, section properties (A, yc, Zt,
Zb, Ixx) and "all possible strand locations" layouts, but not the internal
dimensions of the profile. This module parameterises the profile and holds a
least-squares reconstruction fitted to the published properties of all eight
sizes (see ``data/ie_y_beam.json`` for the fitted values, residuals and
sources).

Geometry convention: origin at the middle of the soffit, y positive upwards,
millimetres. The web of the fitted profile runs straight from the waist to
the top flange edge; per-size implied web slopes vary slightly (-0.15 to
+0.03 run/rise) which is the price of a single fixed-waist parameterisation
and is documented rather than hidden.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources
from typing import Optional

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon, polygon_from_half_profile

_SOFFIT_WIDTH = 750.0
_WF_SLOPE = 0.28840  # dWf/dd, total
_WF_INTERCEPT = -3.75
# least-squares reconstruction (see data file "fit" block)
_CHAMFER = 0.0
_FLANGE_DEPTH = 203.98
_WAIST_HALF_WIDTH = 168.21
_WAIST_HEIGHT = 275.62

_DATA_FILE = "ie_y_beam.json"


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.ie.data").joinpath(_DATA_FILE).read_text()
    )


@dataclass(frozen=True)
class IeYBeamDimensions:
    """Computed dimensions of one Y-beam size, in millimetres.

    Attributes
    ----------
    depth:
        Overall section depth (700 to 1400 for Y1-Y8).
    top_width:
        Published top flange width ``Wf``.
    soffit_width:
        Bottom flange width (750).
    flange_depth:
        Depth of the bottom flange (reconstructed).
    waist_half_width, waist_height:
        Position of the narrowest point of the web (reconstructed).
    chamfer:
        Bottom corner chamfer (reconstructed; ~0 for the fitted family).
    """

    depth: float
    top_width: float
    soffit_width: float
    flange_depth: float
    waist_half_width: float
    waist_height: float
    chamfer: float

    @property
    def outline(self) -> list[tuple[float, float]]:
        """Right-half profile, soffit centre to top, anti-clockwise."""
        half = self.soffit_width / 2.0
        pts: list[tuple[float, float]] = [(half, 0.0)]
        if self.chamfer > 0:
            pts.append((half - self.chamfer, self.chamfer))
        pts += [
            (half - self.chamfer, self.flange_depth),
            (self.waist_half_width, self.waist_height),
            (self.top_width / 2.0, self.depth),
        ]
        return pts


class IeYBeamSection:
    """Irish standard Y beam (Y1-Y8) as a ``sectionproperties`` Geometry.

    Examples
    --------
    >>> from bridgebeams.ie import IeYBeamSection
    >>> y4 = IeYBeamSection("Y4")
    >>> y4.dimensions.depth
    1000.0
    >>> geom = y4.geometry  # sectionproperties Geometry, mm, soffit mid-origin
    """

    SIZES = ("Y1", "Y2", "Y3", "Y4", "Y5", "Y6", "Y7", "Y8")

    provenance = "fitted-reconstruction"
    source_status = "producer catalogue (Banagher Bridge Beam Manual 3rd ed.)"

    def __init__(self, size: str = "Y4", *, depth: Optional[float] = None):
        """
        Parameters
        ----------
        size:
            One of ``Y1`` ... ``Y8``.
        depth:
            Override the depth for a non-standard size; ``Wf`` and the
            reconstructed dimensions follow the family's linear laws. The
            published property comparison does not apply to such sizes.
        """
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        row = next(r for r in data["published_properties"] if r["section"] == size)
        self.size = size
        self.depth = float(depth) if depth is not None else float(row["depth"])
        self.published = row
        self.dimensions = IeYBeamDimensions(
            depth=self.depth,
            top_width=_WF_INTERCEPT + _WF_SLOPE * self.depth,
            soffit_width=_SOFFIT_WIDTH,
            flange_depth=_FLANGE_DEPTH,
            waist_half_width=_WAIST_HALF_WIDTH,
            waist_height=_WAIST_HEIGHT,
            chamfer=_CHAMFER,
        )

    @property
    def polygon(self) -> Polygon:
        return polygon_from_half_profile(self.dimensions.outline)

    @property
    def geometry(self):
        """``sectionproperties`` Geometry of the beam (millimetres)."""
        return geometry_from_polygon(self.polygon)


def strand_locations(
    size: str = "Y4",
    *,
    depth: Optional[float] = None,
    min_top_cover: float = 60.0,
) -> list[tuple[float, float]]:
    """All possible strand locations (mm) for one Y-beam size.

    Rows follow the manufacturer's "all possible strand locations" figure
    (heights above soffit; all beams superimposed). Rows at or above
    ``depth - min_top_cover`` are excluded, and rows must fit within the
    beam's top width.

    Returns
    -------
    list[(x, y)]
        Strand coordinates, x across the 750 mm soffit width centred on
        zero, y above the soffit.
    """
    section = IeYBeamSection(size, depth=depth)
    data = _load_data()
    top_limit = section.depth - min_top_cover
    pts: list[tuple[float, float]] = []
    for row in data["strand_rows"]:
        height = float(row["height"])
        if height > top_limit:
            continue
        spread = float(row["spread"])
        half = spread / 2.0
        # a row must fit inside the local section width
        if 2.0 * half > section.dimensions.top_width and height > section.dimensions.waist_height:
            half = section.dimensions.top_width / 2.0 - 30.0  # edge cover
        count = int(row["count"])
        if count == 1:
            pts.append((0.0, height))
        else:
            step = spread / (count - 1)
            pts.extend((-half + i * step, height) for i in range(count))
    return pts


__all__ = ["IeYBeamDimensions", "IeYBeamSection", "strand_locations", "STRAND_ROWS_IE_Y"]
STRAND_ROWS_IE_Y = _load_data()["strand_rows"]
