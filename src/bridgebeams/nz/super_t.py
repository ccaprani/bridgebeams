"""New Zealand standard Super-T beams (NZTA RR 364, 2008): 1025 and 1225.

Proprietary twin-web Super-T section as standardised by NZTA RR 364
(drawing S1.01/S1.25, read and confirmed by C. Caprani from the official
drawing sheet): overall 2490 wide; bottom flange 852 wide x 240 deep with
100 wide x 75 high bottom-edge chamfers; two 100 mm webs whose inner faces
are 709 mm apart at the bottom flange and 840 mm apart at the top, on a
1:10.56 slope; top slab 100 mm thick x 2490 wide with 100 mm tips; a
15 x 45 formwork lip recess at the top of the void (omitted from the
structural outline). The 1225 shares the cross-section with webs
extended 200 mm; flagged as inferred.

Geometry convention: origin at the middle of the soffit, y positive
upwards, millimetres. Symmetric about x = 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon

_BOTTOM_W = 852.0
_CHAMFER_W = 100.0
_CHAMFER_H = 75.0
_BOTTOM_H = 240.0
_WEB_T = 100.0
_CLEAR_TOP = 840.0
_CLEAR_BOT = 709.0
_SLAB_T = 100.0
_TOP_W = 2490.0


@dataclass(frozen=True)
class NzSuperTDimensions:
    """Dimensions of one NZ Super-T size, millimetres."""

    depth: float  # 1025 or 1225
    top_width: float = _TOP_W
    bottom_flange_width: float = _BOTTOM_W
    bottom_flange_height: float = _BOTTOM_H
    web_thickness: float = _WEB_T
    web_clear_top: float = _CLEAR_TOP
    web_clear_bottom: float = _CLEAR_BOT
    top_slab_thickness: float = _SLAB_T
    chamfer_width: float = _CHAMFER_W
    chamfer_height: float = _CHAMFER_H

    @property
    def outline(self) -> list[tuple[float, float]]:
        """Half-section per NZTA RR 364 S1.01 (C. Caprani reading):

        bottom face 652 (852 less 2x100 chamfers); chamfers 100 wide x 75
        high; flange sides vertical to 240; 67 step; webs 100 thick with
        inner faces 709 clear at the step rising to 840 clear at the slab
        soffit (slope 1:9.4 as drawn, Colin's 1:10.56 reading noted);
        top slab 2490 x 100 with 100 tips.
        """
        d = self.depth
        bf = self.bottom_flange_width / 2.0      # 426
        cw = self.chamfer_width                  # 100
        ch = self.chamfer_height                 # 75
        step = 67.0
        wt = self.web_thickness / 2.0            # 50
        in_bot = self.web_clear_bottom / 2.0     # 354.5
        in_top = self.web_clear_top / 2.0        # 420.0
        y_step = self.bottom_flange_height + step  # 307
        y_slab = d - self.top_slab_thickness       # 925 / 1125

        r = [
            (bf, 0.0) if False else (bf - cw, 0.0),
            (bf, ch),
            (bf, self.bottom_flange_height),
            # step out to the web base outer face
            (in_bot + wt, y_step),
            # web inner face: from the step the inner face rises
            (in_bot - wt, y_step),
            (in_top - wt, y_slab),
            # top slab
            (self.top_width / 2.0, y_slab),
            (self.top_width / 2.0, d),
        ]
        l = [(-x, y) for x, y in reversed(r)]
        return l + r


class NzSuperTSection:
    """NZ standard Super-T (RR 364) as a ``sectionproperties`` Geometry.

    Examples
    --------
    >>> from bridgebeams.nz import NzSuperTSection
    >>> st = NzSuperTSection(1025)
    >>> st.dimensions.depth
    1025.0
    """

    SIZES = (1025, 1225)

    def __init__(self, depth: int = 1025):
        if depth not in self.SIZES:
            raise ValueError(f"depth must be one of {self.SIZES}, got {depth!r}")
        self.depth = depth
        self.dimensions = NzSuperTDimensions(depth=float(depth))

    @property
    def polygon(self) -> Polygon:
        return Polygon(self.dimensions.outline)

    @property
    def geometry(self):
        """``sectionproperties`` Geometry of the beam (millimetres)."""
        return geometry_from_polygon(self.polygon)


__all__ = ["NzSuperTDimensions", "NzSuperTSection"]
