"""Irish standard M beams (M1-M10) and UMB edge beams (UMB1-UMB10).

M profile: 970 bottom flange, splay to a 160 mm web of published height H
(200 for M1-M4, 440 for M5-M7, 680 for M8-M10), splay to a 400-wide upper
block, nibbed 300 top. Validated to <=0.66% against the published
properties of all eleven sizes.

UMB profile: U-shaped - 970 bottom flange, 600 void between legs, 650 top
slab with 135-wide edge upstands. UMB10 matches the manual drawing exactly;
all sizes validate to <=0.58%.

Geometry convention: origin at the middle of the soffit, y positive
upwards, millimetres.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon

_DATA_FILE = "ie_m_beam.json"


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.ukie.data").joinpath(_DATA_FILE).read_text()
    )


# ---- M -----------------------------------------------------------------

_M_FIXED = dict(
    bottom_face_half=445.0,
    flange_half=485.0,
    chamfer=25.0,
    flange_side_half=472.5,
    flange_side_h=158.0,
    splay_h=52.0,
    web_start_y=290.6,
    splay2_h=59.0,
    block_half=199.6,
    nib_step=50.1,
    nib_h=45.0,
    top_half=149.5,
)


@dataclass(frozen=True)
class IeMBeamDimensions:
    """Dimensions of one M-beam size, millimetres."""

    depth: float
    web_height: float  # published H: 200 / 440 / 680
    web_width: float = 80.0  # half-width; 160 web

    @property
    def outline(self) -> list[tuple[float, float]]:
        f = _M_FIXED
        r = [
            (f["bottom_face_half"], 0.0),
            (f["flange_half"], f["chamfer"]),
            (f["flange_side_half"], f["flange_side_h"]),
            (158.9, 210.0),
            (self.web_width, f["web_start_y"]),
            (self.web_width, f["web_start_y"] + self.web_height),
            (f["block_half"], f["web_start_y"] + self.web_height + f["splay2_h"]),
            (f["block_half"], self.depth - f["nib_h"]),
            (f["top_half"], self.depth - f["nib_h"]),
            (f["top_half"], self.depth),
        ]
        l = [(-x, y) for x, y in reversed(r)]
        return l + r


class IeMBeamSection:
    """Irish standard M beam (M1-M10) as a ``sectionproperties`` Geometry.

    Examples
    --------
    >>> from bridgebeams.ukie import IeMBeamSection
    >>> m4 = IeMBeamSection("M4")
    >>> m4.dimensions.depth
    880.0
    """

    SIZES = ("M1", "M680", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10")

    def __init__(self, size: str = "M4"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        row = next(r for r in data["published_properties"]["m"] if r["section"] == size)
        self.size = size
        self.published = row
        self.dimensions = IeMBeamDimensions(
            depth=float(row["depth"]), web_height=float(row["H"])
        )

    @property
    def polygon(self) -> Polygon:
        return Polygon(self.dimensions.outline)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


# ---- UMB ---------------------------------------------------------------

_UMB_FIXED = dict(
    bottom_face_half=460.0,
    flange_half=485.0,
    chamfer=25.0,
    void_apex=160.0,
    haunch=(200.0, 180.0),
    leg_half=300.0,
    leg_start_y=280.0,
    top_slab=45.0,
    upstand_half=460.0,
    upstand_inner=325.0,
)


@dataclass(frozen=True)
class IeUMBBeamDimensions:
    """Dimensions of one UMB edge-beam size, millimetres."""

    depth: float

    @property
    def outline(self) -> list[tuple[float, float]]:
        f = _UMB_FIXED
        d = self.depth
        return [
            (-f["bottom_face_half"], 0.0),
            (f["bottom_face_half"], 0.0),
            (f["flange_half"], f["chamfer"]),
            (f["flange_half"], d - f["top_slab"]),
            (f["upstand_half"], d - f["top_slab"]),
            (f["upstand_half"], d),
            (f["upstand_inner"], d),
            (f["upstand_inner"], d - f["top_slab"]),
            (f["leg_half"], d - f["top_slab"]),
            (f["leg_half"], f["leg_start_y"]),
            (f["haunch"][0], f["haunch"][1]),
            (0.0, f["void_apex"]),
            (-f["haunch"][0], f["haunch"][1]),
            (-f["leg_half"], f["leg_start_y"]),
            (-f["leg_half"], d - f["top_slab"]),
            (-(f["upstand_inner"]), d - f["top_slab"]),
            (-(f["upstand_inner"]), d),
            (-(f["upstand_half"]), d),
            (-(f["upstand_half"]), d - f["top_slab"]),
            (-(f["flange_half"]), d - f["top_slab"]),
            (-(f["flange_half"]), f["chamfer"]),
        ]


class IeUMBBeamSection:
    """Irish standard UMB edge beam (UMB1-UMB10) as a ``sectionproperties``
    Geometry.

    Examples
    --------
    >>> from bridgebeams.ukie import IeUMBBeamSection
    >>> umb10 = IeUMBBeamSection("UMB10")
    >>> umb10.dimensions.depth
    1360.0
    """

    SIZES = (
        "UMB1", "UMB680", "UMB2", "UMB3", "UMB4", "UMB5",
        "UMB6", "UMB7", "UMB8", "UMB9", "UMB10",
    )

    def __init__(self, size: str = "UMB10"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        row = next(r for r in data["published_properties"]["umb"] if r["section"] == size)
        self.size = size
        self.published = row
        self.dimensions = IeUMBBeamDimensions(depth=float(row["depth"]))

    @property
    def polygon(self) -> Polygon:
        return Polygon(self.dimensions.outline)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = ["IeMBeamDimensions", "IeMBeamSection", "IeUMBBeamDimensions", "IeUMBBeamSection"]
