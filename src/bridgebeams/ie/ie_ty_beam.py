"""Irish standard TY beams (TY, beam & slab and solid slab) and TYE edge
beams.

Profile recovered exactly from the Banagher manual's true-scale vector
drawings (printed pp. 20, 22); every size reproduces the published area,
centroid and second moment of area to <=0.02%. Per size the manufacturer
publishes the top flange width ``Wf``; beam-and-slab variants carry a
nibbed top (nib = Wf + 80 at d - 50, cap Wf to the top), solid-slab
variants a full top flange of width ``Wf``; TYE variants extend the top to
a full-height vertical face at x = -375 (published ``Xc`` measured from
that face).

Geometry convention: origin at the middle of the soffit, y positive
upwards, millimetres.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources
from typing import Optional

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon

_DATA_FILE = "ie_ty_beam.json"

# fixed profile dims (mm), from the vector drawings
_HALF_BOT_FACE = 350.0
_HALF_FLANGE = 375.0
_CHAMFER = 25.0
_HALF_SIDE_TOP = 370.0
_SIDE_H = 135.0
_HALF_SHOULDER = 142.5
_SHOULDER_Y = 240.0
_HALF_WEB = 92.5
_WEB_Y = 320.0
_BS_NIB_STEP = 40.0
_BS_NIB_H = 50.0
_FACE_OFFSET = -375.0


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.ie.data").joinpath(_DATA_FILE).read_text()
    )


@dataclass(frozen=True)
class IeTYBeamDimensions:
    """Dimensions of one TY/TYE beam size, millimetres.

    ``variant`` is ``"bs"`` (beam & slab, nibbed top) or ``"ss"`` (solid
    slab, full top flange). ``edge`` adds the full-height vertical face at
    x = -375 (TYE).
    """

    depth: float
    top_width: float  # published Wf
    variant: str  # "bs" or "ss"
    edge: bool = False

    @property
    def outline(self) -> list[tuple[float, float]]:
        d, wfh = self.depth, self.top_width / 2.0
        r = [
            (_HALF_BOT_FACE, 0.0),
            (_HALF_FLANGE, _CHAMFER),
            (_HALF_SIDE_TOP, _SIDE_H),
            (_HALF_SHOULDER, _SHOULDER_Y),
            (_HALF_WEB, _WEB_Y),
        ]
        if self.edge:
            # top measured from the vertical face at x = -375
            xr = _FACE_OFFSET + self.top_width
            if self.variant == "bs":
                r += [(xr + _BS_NIB_STEP, d - _BS_NIB_H), (xr, d - _BS_NIB_H)]
            r += [(xr, d)]
            return (
                [(_FACE_OFFSET, _CHAMFER), (-_HALF_BOT_FACE, 0.0)]
                + r
                + [(_FACE_OFFSET, d)]
            )
        if self.variant == "bs":
            r += [(wfh + _BS_NIB_STEP, d - _BS_NIB_H), (wfh, d - _BS_NIB_H), (wfh, d)]
        else:
            r += [(wfh, d)]
        l = [(-x, y) for x, y in reversed(r)]
        return l + r

class IeTYBeamSection:
    """Irish standard TY beam as a ``sectionproperties`` Geometry.

    Parameters
    ----------
    size:
        Beam designation, e.g. ``"TY7"`` (with ``variant`` selecting the
        beam & slab or solid slab table) or ``"TYE7"`` (edge beam; the
        variant is inferred from the size number's availability in each
        table, defaulting to beam & slab).
    variant:
        ``"bs"`` (beam & slab) or ``"ss"`` (solid slab). TYE sizes carry
        both variants.

    Examples
    --------
    >>> from bridgebeams.ie import IeTYBeamSection
    >>> ty8 = IeTYBeamSection("TY8", variant="bs")
    >>> ty8.dimensions.depth
    750.0
    """

    SIZES_BS = tuple(f"TY{i}" for i in range(3, 12))
    SIZES_SS = tuple(f"TY{i}" for i in range(1, 12))
    SIZES_EDGE_BS = tuple(f"TYE{i}" for i in range(3, 12))
    SIZES_EDGE_SS = tuple(f"TYE{i}" for i in range(1, 12))

    # Measured from true-scale vector drawings rather than printed dims (cf. Hungarian FPT precedent).
    provenance = "transcribed-with-convention"
    source_status = "producer catalogue (Banagher Bridge Beam Manual 3rd ed.)"

    def __init__(self, size: str, variant: str = "bs"):
        if variant not in ("bs", "ss"):
            raise ValueError("variant must be 'bs' or 'ss'")
        self.size = size
        self.variant = variant
        self.edge = size.startswith("TYE")
        data = _load_data()
        key = ("tye_" if self.edge else "ty_") + variant
        rows = data["published_properties"][key]
        row = next((r for r in rows if r["section"] == size), None)
        if row is None:
            table = (self.SIZES_EDGE_SS if variant == "ss" else self.SIZES_EDGE_BS) if self.edge else (
                self.SIZES_SS if variant == "ss" else self.SIZES_BS
            )
            raise ValueError(f"size must be one of {table}, got {size!r}")
        self.published = row
        self.dimensions = IeTYBeamDimensions(
            depth=float(row["depth"]),
            top_width=float(row["wf"]),
            variant=variant,
            edge=self.edge,
        )

    @property
    def polygon(self) -> Polygon:
        return Polygon(self.dimensions.outline)

    @property
    def geometry(self):
        """``sectionproperties`` Geometry of the beam (millimetres)."""
        return geometry_from_polygon(self.polygon)


__all__ = ["IeTYBeamDimensions", "IeTYBeamSection"]
