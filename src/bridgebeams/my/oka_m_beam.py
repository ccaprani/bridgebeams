"""OKA (Malaysia) pretensioned M-beams M2-M10.

Source: OKA Concrete Industries *T-Beams / M-Beams* brochure, PDF p2
("OKA PRESTRESSED (PRETENSIONED) M-BEAMS"): three dimensioned sections
(M2-M4, M5-M7, M8-M10) and a property table (D, A, Yt, Yb, Ixx, Zt, Zb).

Printed geometry (mm): soffit 970 with 20 x 20 chamfers; bottom flange
edge 160 high with a 10 mm inward lean (10 + 315 + 80 = 405 horizontal
chain from flange edge to web face); 50 mm taper to the splay; 80 x 80
splay to a 160 mm web; lower web 200/440/680 mm for the three groups;
upper splay 60 high x 120 wide to a 400 mm top flange; 50 x 50 top
shoulders leaving a 300 mm raised strip. Within a group the top flange
edge is 120/200/280 mm (dashed M2/M3 outlines), i.e. each step adds 80 mm.

All rows are ~500 mm² (0.12-0.16 %) below the printed area; the printed
M10 area is a further 300 mm² low (pinned in tests). Origin mid-soffit,
y up, mm.
"""

from __future__ import annotations

from dataclasses import dataclass

from ._common import _SizedSection


@dataclass(frozen=True)
class OkaMBeamDimensions:
    depth: float
    lower_web: float
    bottom_width: float = 970.0
    chamfer: float = 20.0
    flange_edge: float = 160.0
    edge_lean: float = 10.0
    taper_height: float = 50.0
    splay: float = 80.0
    web_width: float = 160.0
    top_splay_height: float = 60.0
    top_width: float = 400.0
    shoulder: float = 50.0

    def right_half(self) -> list[tuple[float, float]]:
        b = self.bottom_width / 2
        xw = self.web_width / 2
        y_taper = self.flange_edge + self.taper_height
        y_web = y_taper + self.splay
        y_web_top = y_web + self.lower_web
        y_flange = y_web_top + self.top_splay_height
        xt = self.top_width / 2
        return [
            (b - self.chamfer, 0.0),
            (b, self.chamfer),
            (b - self.edge_lean, self.flange_edge),
            (xw + self.splay, y_taper),
            (xw, y_web),
            (xw, y_web_top),
            (xt, y_flange),
            (xt, self.depth - self.shoulder),
            (xt - self.shoulder, self.depth - self.shoulder),
            (xt - self.shoulder, self.depth),
            (0.0, self.depth),
        ]


class OkaMBeamSection(_SizedSection):
    """OKA pretensioned M-beam, sizes M2-M10 (720-1360 mm)."""

    SIZES = tuple(f"M{i}" for i in range(2, 11))
    _DATA = "oka_m_beams.json"

    def __init__(self, size: str = "M6"):
        super().__init__(size)
        p = self.published
        self.dimensions = OkaMBeamDimensions(depth=float(p["depth"]), lower_web=float(p["lower_web"]))

    def right_half(self):
        return self.dimensions.right_half()


__all__ = ["OkaMBeamDimensions", "OkaMBeamSection"]
