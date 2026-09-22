"""Japanese standard precast pretensioned T-girders (JIS A 5373 けた橋げた).

Types AG18-AG24 (A live load) and BG18-BG24 (B live load), spans 18-24 m
at 1 m pitch. Cross-section per the MLIT Chubu Regional Bureau design
guideline (図-5-III-41, citing the PCCEN handbook / JIS A 5373):

- top flange 800 wide x 160 thick, 20 mm side returns, 35 mm haunch
- web + bottom 300 wide, constant to the soffit
- depth 900-1300 mm per type

Geometry convention: origin at the middle of the soffit, y positive
upwards, millimetres. Symmetric about x = 0.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon

_DATA_FILE = "jis_t_girders.json"

_TOP_W = 800.0
_TOP_T = 160.0
_RETURN = 20.0
_HAUNCH = 35.0
_WEB_BOTTOM_W = 300.0


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.jp.data").joinpath(_DATA_FILE).read_text()
    )


@dataclass(frozen=True)
class JisTGirderDimensions:
    """Dimensions of one JIS T-girder size, millimetres."""

    depth: float
    top_flange_width: float = _TOP_W
    top_flange_thickness: float = _TOP_T
    side_return: float = _RETURN
    haunch: float = _HAUNCH
    web_bottom_width: float = _WEB_BOTTOM_W

    @property
    def outline(self) -> list[tuple[float, float]]:
        """Full outline, anti-clockwise from the bottom-left corner.

        Top flange: 800 wide overall with 20 mm side returns at the tips;
        160 thick; 35 haunch to the 300 web; web/bottom 300 wide
        constant to the soffit.
        """
        d = self.depth
        t = _TOP_W / 2.0
        rt = t - _RETURN               # 380: flange underside at tip
        w = _WEB_BOTTOM_W / 2.0        # 150
        y1 = d - _TOP_T                # 740 (900 type)
        y2 = y1 - _HAUNCH              # 705
        return [
            (-w, 0.0),
            (w, 0.0),
            (w, y2),
            (rt, y1),
            (t, y1),
            (t, d),
            (-t, d),
            (-t, y1),
            (-rt, y1),
            (-w, y2),
        ]


class JisTGirderSection:
    """Japanese standard JIS A 5373 T-girder as a ``sectionproperties``
    Geometry.

    Examples
    --------
    >>> from bridgebeams.jp import JisTGirderSection
    >>> g = JisTGirderSection("AG24")
    >>> g.dimensions.depth
    1200.0
    """

    SIZES = tuple(
        [f"AG{i}" for i in range(18, 25)] + [f"BG{i}" for i in range(18, 25)]
    )

    def __init__(self, size: str = "AG21"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        row = next(r for r in data["types"] if r["section"] == size)
        self.size = size
        self.published = row
        self.dimensions = JisTGirderDimensions(depth=float(row["depth"]))

    @property
    def polygon(self) -> Polygon:
        return Polygon(self.dimensions.outline)

    @property
    def geometry(self):
        """``sectionproperties`` Geometry of the girder (millimetres)."""
        return geometry_from_polygon(self.polygon)


__all__ = ["JisTGirderDimensions", "JisTGirderSection"]
