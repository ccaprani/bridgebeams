"""SCIB (Sarawak, Malaysia) prestressed I-beams I5-I8 and I12-I18.

Source: SCIB Concrete Manufacturing *Prestressed Concrete Beams*,
undated six-page catalogue, PDF page 6. Eleven gross outlines and the
printed A/Yt/Yb/Ixx/Zt/Zb table are transcribed in millimetres. The
top-edge thickness follows from the printed depth, lower flange and
haunch, straight web and 105 mm upper-haunch dimension chain.

Nominal sharp intersections are retained: no small unlabelled radius or
chamfer is inferred. Strand-location callouts and web-hole details are
not gross-outline dimensions. The printed I18 bottom width is 660 mm.
All printed areas are reproduced exactly, centroids to integer-table
rounding and Ixx within 0.085 percent. Source-rounding discrepancies are
recorded rather than used to fit the outline. Origin mid-soffit, y up.
"""

from __future__ import annotations

from dataclasses import dataclass

from ._common import _SizedSection


@dataclass(frozen=True)
class ScibIBeamDimensions:
    """Nominal gross cross-section dimensions in millimetres."""

    depth: float
    top_width: float
    web_width: float
    bottom_width: float
    bottom_edge: float
    bottom_splay: float
    web_height: float
    top_splay: float = 105.0

    @property
    def top_edge(self):
        """Top-edge thickness derived from closure of the printed height chain."""
        return self.depth - self.bottom_edge - self.bottom_splay - self.web_height - self.top_splay

    def right_half(self):
        xb, xw, xt = self.bottom_width / 2, self.web_width / 2, self.top_width / 2
        y_web_bottom = self.bottom_edge + self.bottom_splay
        y_web_top = y_web_bottom + self.web_height
        return [
            (xb, 0.0), (xb, self.bottom_edge), (xw, y_web_bottom),
            (xw, y_web_top), (xt, y_web_top + self.top_splay),
            (xt, self.depth), (0.0, self.depth),
        ]


class ScibIBeamSection(_SizedSection):
    """Eleven SCIB nominal prestressed I-beams, 965-1830 mm deep."""

    SIZES = ("I5", "I6", "I7", "I8", "I12", "I13", "I14", "I15", "I16", "I17", "I18")
    _DATA = "scib_i_beams.json"

    def __init__(self, size: str = "I14"):
        super().__init__(size)
        self.dimensions = ScibIBeamDimensions(
            **{name: float(value) for name, value in self.published["dimensions_mm"].items()}
        )

    def right_half(self):
        return self.dimensions.right_half()


__all__ = ["ScibIBeamDimensions", "ScibIBeamSection"]
