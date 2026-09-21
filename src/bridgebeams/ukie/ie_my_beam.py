"""Irish standard MY beams (MY1-MY7) and MYE edge beams (MYE1-MYE7) for
solid slab construction - Banagher's economical alternative to the T and TY
families.

Y-style topology: 970 bottom flange, splay to a waist, web flaring to the
published top width ``Wf`` per size. MYE adds a full-height vertical face
at x = -485 with the top measured from it (published ``Xc``). Internal
dims are least-squares fitted to the published properties of all seven
sizes per family: MY rms 0.83% (max 2.1%), MYE rms 0.26% (max 0.59%) -
see ``data/ie_my_beam.json``.

Geometry convention: origin at the middle of the soffit, y positive
upwards, millimetres. MYE published ``Xc`` is measured from the vertical
face at x = -485.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon

_DATA_FILE = "ie_my_beam.json"

_HALF_FLANGE = 485.0  # 970 bottom flange
_FACE_OFFSET = -485.0  # MYE vertical face

# fitted MY dims
_MY_CHAMFER = 6.7
_MY_FLANGE_DEPTH = 103.4
_MY_WAIST_HW = 151.4
_MY_WAIST_Y = 124.4

# fitted MYE dims
_MYE_CHAMFER = 12.6
_MYE_FLANGE_DEPTH = 105.7
_MYE_WAIST_HW = 152.7
_MYE_WAIST_Y = 125.7


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.ukie.data").joinpath(_DATA_FILE).read_text()
    )


@dataclass(frozen=True)
class IeMYBeamDimensions:
    """Dimensions of one MY-beam size, millimetres."""

    depth: float
    top_width: float
    chamfer: float = _MY_CHAMFER
    flange_depth: float = _MY_FLANGE_DEPTH
    waist_half_width: float = _MY_WAIST_HW
    waist_height: float = _MY_WAIST_Y

    @property
    def outline(self) -> list[tuple[float, float]]:
        r = [
            (_HALF_FLANGE, 0.0),
            (_HALF_FLANGE - self.chamfer, self.chamfer),
            (_HALF_FLANGE - self.chamfer, self.flange_depth),
            (self.waist_half_width, self.waist_height),
            (self.top_width / 2.0, self.depth),
        ]
        l = [(-x, y) for x, y in reversed(r)]
        return l + r


@dataclass(frozen=True)
class IeMYEBeamDimensions:
    """Dimensions of one MYE edge-beam size, millimetres."""

    depth: float
    top_width: float
    chamfer: float = _MYE_CHAMFER
    flange_depth: float = _MYE_FLANGE_DEPTH
    waist_half_width: float = _MYE_WAIST_HW
    waist_height: float = _MYE_WAIST_Y

    @property
    def outline(self) -> list[tuple[float, float]]:
        r = [
            (_HALF_FLANGE, 0.0),
            (_HALF_FLANGE - self.chamfer, self.chamfer),
            (_HALF_FLANGE - self.chamfer, self.flange_depth),
            (self.waist_half_width, self.waist_height),
            (_FACE_OFFSET + self.top_width, self.depth),
        ]
        return [(_FACE_OFFSET, 0.0)] + r + [(_FACE_OFFSET, self.depth)]


class IeMYBeamSection:
    """Irish standard MY beam (MY1-MY7) as a ``sectionproperties`` Geometry.

    Examples
    --------
    >>> from bridgebeams.ukie import IeMYBeamSection
    >>> my4 = IeMYBeamSection("MY4")
    >>> my4.dimensions.depth
    450.0
    """

    SIZES = tuple(f"MY{i}" for i in range(1, 8))

    def __init__(self, size: str = "MY4"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        row = next(r for r in data["published_properties"]["my"] if r["section"] == size)
        self.size = size
        self.published = row
        self.dimensions = IeMYBeamDimensions(depth=float(row["depth"]), top_width=float(row["wf"]))

    @property
    def polygon(self) -> Polygon:
        return Polygon(self.dimensions.outline)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


class IeMYEBeamSection:
    """Irish standard MYE edge beam (MYE1-MYE7) as a ``sectionproperties``
    Geometry."""

    SIZES = tuple(f"MYE{i}" for i in range(1, 8))

    def __init__(self, size: str = "MYE4"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        row = next(r for r in data["published_properties"]["mye"] if r["section"] == size)
        self.size = size
        self.published = row
        self.dimensions = IeMYEBeamDimensions(depth=float(row["depth"]), top_width=float(row["wf"]))

    @property
    def polygon(self) -> Polygon:
        return Polygon(self.dimensions.outline)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = [
    "IeMYBeamDimensions",
    "IeMYBeamSection",
    "IeMYEBeamDimensions",
    "IeMYEBeamSection",
]
