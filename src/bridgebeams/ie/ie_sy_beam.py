"""Irish standard SY beams (SY1-SY6) and SYE edge beams (SYE1-SYE6) -
the long-span development of the Y family.

SY: 750 bottom flange, splay to a tapered stem carrying a 240-wide top
nib; only the depth varies across the range. SYE: full-height vertical
face on one side (x = -375) with a wider top. Validated against the
published properties: SY rms 0.012%, SYE rms 0.008% (see
``data/ie_sy_beam.json``).

Geometry convention: origin at the middle of the soffit, y positive
upwards, millimetres. SYE published ``Xc`` is measured from the vertical
face at x = -375.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon

_DATA_FILE = "ie_sy_beam.json"

_HALF_BOT_FACE = 350.0
_HALF_FLANGE = 375.0
_CHAMFER = 25.0
_SPLAY_Y = 397.3
_STEM_BOT_Y = 486.8
_STEM_TOP_Y_REF = 1450.0
_NIB_STEP = 40.0
_NIB_H = 50.0
_FACE_OFFSET = -375.0

# fitted SY stem/splay half-widths (mm)
_SY_SPLAY_W = 142.4
_SY_STEM_BOT = 102.9
_SY_STEM_TOP = 160.1

# fitted SYE dims
_SYE_SPLAY_W = 80.0
_SYE_STEM_BOT = 147.76
_SYE_STEM_TOP = 120.0
_SYE_WF_INTERCEPT = 700.0
_SYE_WF_SLOPE = 0.11643


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.ie.data").joinpath(_DATA_FILE).read_text()
    )


def sye_wf(depth: float) -> float:
    """SYE top-width law (fitted linear, reproduces published properties)."""
    return _SYE_WF_INTERCEPT + _SYE_WF_SLOPE * depth


@dataclass(frozen=True)
class IeSYBeamDimensions:
    """Dimensions of one SY-beam size, millimetres."""

    depth: float

    @property
    def outline(self) -> list[tuple[float, float]]:
        d = self.depth
        r = [
            (_HALF_BOT_FACE, 0.0),
            (_HALF_FLANGE, _CHAMFER),
            (_HALF_FLANGE, 248.7),
            (_SY_SPLAY_W, _SPLAY_Y),
            (_SY_STEM_BOT, _STEM_BOT_Y),
            (_SY_STEM_TOP, _STEM_TOP_Y_REF),
            (_SY_STEM_TOP, d - _NIB_H),
            (_SY_STEM_TOP - _NIB_STEP, d - _NIB_H),
            (_SY_STEM_TOP - _NIB_STEP, d),
        ]
        l = [(-x, y) for x, y in reversed(r)]
        return l + r


@dataclass(frozen=True)
class IeSYEBeamDimensions:
    """Dimensions of one SYE edge-beam size, millimetres."""

    depth: float
    top_width: float

    @property
    def outline(self) -> list[tuple[float, float]]:
        d = self.depth
        xr = _FACE_OFFSET + self.top_width
        return [
            (_FACE_OFFSET, _CHAMFER),
            (-_HALF_BOT_FACE, 0.0),
            (_HALF_BOT_FACE, 0.0),
            (_HALF_FLANGE, _CHAMFER),
            (_HALF_FLANGE, 248.7),
            (_SYE_SPLAY_W, _SPLAY_Y),
            (_SYE_STEM_BOT, _STEM_BOT_Y),
            (_SYE_STEM_TOP, _STEM_TOP_Y_REF),
            (_SYE_STEM_TOP, d - _NIB_H),
            (xr, d),
            (_FACE_OFFSET, d),
        ]


class IeSYBeamSection:
    """Irish standard SY beam (SY1-SY6) as a ``sectionproperties`` Geometry.

    Examples
    --------
    >>> from bridgebeams.ie import IeSYBeamSection
    >>> sy4 = IeSYBeamSection("SY4")
    >>> sy4.dimensions.depth
    1800.0
    """

    SIZES = tuple(f"SY{i}" for i in range(1, 7))

    def __init__(self, size: str = "SY4"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        row = next(r for r in data["published_properties"]["sy"] if r["section"] == size)
        self.size = size
        self.published = row
        self.dimensions = IeSYBeamDimensions(depth=float(row["depth"]))

    @property
    def polygon(self) -> Polygon:
        return Polygon(self.dimensions.outline)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


class IeSYEBeamSection:
    """Irish standard SYE edge beam (SYE1-SYE6) as a ``sectionproperties``
    Geometry."""

    SIZES = tuple(f"SYE{i}" for i in range(1, 7))

    def __init__(self, size: str = "SYE4"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        row = next(r for r in data["published_properties"]["sye"] if r["section"] == size)
        self.size = size
        self.published = row
        self.dimensions = IeSYEBeamDimensions(
            depth=float(row["depth"]), top_width=sye_wf(float(row["depth"]))
        )

    @property
    def polygon(self) -> Polygon:
        return Polygon(self.dimensions.outline)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = [
    "IeSYBeamDimensions",
    "IeSYBeamSection",
    "IeSYEBeamDimensions",
    "IeSYEBeamSection",
    "sye_wf",
]
