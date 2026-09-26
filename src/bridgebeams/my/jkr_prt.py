"""Malaysian JKR standard pretensioned T-beams PRT1-PRT3 and OKA PRT-M.

Sources (both producer reproductions of the JKR standard section):

* G-CAST (Cast Concrete Sdn Bhd) *Prestressed Concrete Beams* catalogue,
  June 2020 Rev.0, PDF p2 ("JKR PRESTRESSED PRT BEAMS"): dimensioned
  section plus D, A, Yt, Yb, Ixx, Zt, Zb for PRT1/2/3.
* OKA Concrete Industries *T-Beams / M-Beams* brochure (March 2018),
  PDF p1: the same section and A for PRT1/2/3, plus the OKA-modified
  PRT-M depths 1450-1800 mm with web depths hw = H - 195 mm and an area
  range 518 350-623 350 mm².

Section: 800 mm top flange with a 620 mm wide, 30 mm high raised strip
(90 mm shoulders each side), 130 mm flange edge, 35 mm taper over 250 mm
to a 300 mm web which runs to the soffit (no bottom flange, no chamfer
shown). PRT-M rows are not tabulated individually; they are built with the
same top and web, which reproduces both printed area-range endpoints
exactly and the printed hw list. Origin at mid-soffit, y up, mm.
"""

from __future__ import annotations

from dataclasses import dataclass

from ._common import _SizedSection


@dataclass(frozen=True)
class JkrPrtDimensions:
    depth: float
    top_width: float = 800.0
    strip_width: float = 620.0
    strip_height: float = 30.0
    flange_edge: float = 130.0
    taper_height: float = 35.0
    web_width: float = 300.0

    @property
    def web_depth(self) -> float:
        """Printed ``hw``: soffit to underside of the taper."""
        return self.depth - self.strip_height - self.flange_edge - self.taper_height

    def right_half(self) -> list[tuple[float, float]]:
        d, bw, bt, bs = self.depth, self.web_width / 2, self.top_width / 2, self.strip_width / 2
        return [
            (bw, 0.0),
            (bw, self.web_depth),
            (bt, self.web_depth + self.taper_height),
            (bt, d - self.strip_height),
            (bs, d - self.strip_height),
            (bs, d),
            (0.0, d),
        ]


class JkrPrtBeamSection(_SizedSection):
    """JKR PRT1/PRT2/PRT3 and OKA PRT-M (1450-1800) pretensioned T-beams.

    >>> JkrPrtBeamSection("PRT1").polygon.area
    458350.0
    """

    SIZES = ("PRT1", "PRT2", "PRT3") + tuple(
        f"PRT-M{d}" for d in (1450, 1500, 1550, 1600, 1650, 1700, 1800)
    )
    _DATA = "jkr_prt.json"

    def __init__(self, size: str = "PRT1"):
        super().__init__(size)
        self.dimensions = JkrPrtDimensions(depth=float(self.published["depth"]))

    def right_half(self):
        return self.dimensions.right_half()


__all__ = ["JkrPrtDimensions", "JkrPrtBeamSection"]
