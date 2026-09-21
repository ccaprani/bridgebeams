"""Irish standard U beams (U600-U12) and SU edge beams (SU11-SU12).

Profile recovered exactly from the Banagher manual's true-scale vector
drawing (printed p. 24); all thirteen sizes reproduce the published area,
centroid and second moment of area to <=0.3%. Per size the manufacturer
publishes the overall top width ``W1``, the void top width ``W2`` and the
leg top width ``W3``; ``W2`` is derived here as ``W1 - 2*(W3 + notch/step
allowance)`` which matches the drawing exactly.

Geometry convention: origin at the middle of the soffit, y positive
upwards, millimetres.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon

_DATA_FILE = "ie_u_beam.json"

_R_OUT = 485.0  # flange half-width at y=20 (970 total)
_R_IN = 465.0   # bottom face half-width (930 total)
_STEP = 40.0
_STEP_BELOW_TOP = 50.0


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.ukie.data").joinpath(_DATA_FILE).read_text()
    )


@dataclass(frozen=True)
class IeUBeamDimensions:
    """Dimensions of one U/SU beam size, millimetres."""

    depth: float
    w1: float  # overall top width (at the widest point, d - 50)
    w2: float  # void top width (derived from W1 - 2*(W3 + allowance))
    w3: float  # leg top face width
    subgroup: str  # "small" (U600-U1), "large" (U3-U12) or "SU"

    @property
    def outline(self) -> list[tuple[float, float]]:
        d, W1h, W2h = self.depth, self.w1 / 2.0, self.w2 / 2.0
        sg = self.subgroup
        pts: list[tuple[float, float]]
        if sg == "small":
            pts = [
                (0.0, 160.0), (W2h - 100.0, 180.0), (W2h, 280.0), (W2h, d - 25.0),
                (W2h + 25.0, d - 25.0), (W2h + 25.0, d), (W1h - _STEP, d),
                (W1h - _STEP, d - _STEP_BELOW_TOP), (W1h, d - _STEP_BELOW_TOP),
                (_R_OUT, 20.0), (_R_IN, 0.0),
                (-_R_IN, 0.0), (-_R_OUT, 20.0), (-W1h, d - _STEP_BELOW_TOP),
                (-(W1h - _STEP), d - _STEP_BELOW_TOP), (-(W1h - _STEP), d),
                (-(W2h + 25.0), d), (-(W2h + 25.0), d - 25.0),
                (-W2h, d - 25.0), (-W2h, 280.0), (-(W2h - 100.0), 180.0),
            ]
        elif sg == "large":
            pts = [
                (0.0, 160.0), (240.0, 210.0), (365.0, 360.0),
                (W1h - 218.7, d - 415.0), (W2h, d - 55.0), (W2h, d - 25.0),
                (W2h + 40.0, d - 25.0), (W2h + 40.0, d), (W1h - _STEP, d),
                (W1h - _STEP, d - _STEP_BELOW_TOP), (W1h, d - _STEP_BELOW_TOP),
                (_R_OUT, 20.0), (_R_IN, 0.0),
                (-_R_IN, 0.0), (-_R_OUT, 20.0), (-W1h, d - _STEP_BELOW_TOP),
                (-(W1h - _STEP), d - _STEP_BELOW_TOP), (-(W1h - _STEP), d),
                (-(W2h + 40.0), d), (-(W2h + 40.0), d - 25.0),
                (-W2h, d - 25.0), (-W2h, d - 55.0), (-(W1h - 218.7), d - 415.0),
                (-365.0, 360.0), (-240.0, 210.0),
            ]
        elif sg == "SU":
            pts = [
                (0.0, 210.0), (247.0, 260.0), (372.0, 410.0),
                (W1h - 229.2, d - 490.0), (W2h, d - 90.0), (W2h, d - 25.0),
                (W2h + 40.0, d - 25.0), (W2h + 40.0, d), (W1h - _STEP, d),
                (W1h - _STEP, d - _STEP_BELOW_TOP), (W1h, d - _STEP_BELOW_TOP),
                (_R_OUT, 20.0), (_R_IN, 0.0),
                (-_R_IN, 0.0), (-_R_OUT, 20.0), (-W1h, d - _STEP_BELOW_TOP),
                (-(W1h - _STEP), d - _STEP_BELOW_TOP), (-(W1h - _STEP), d),
                (-(W2h + 40.0), d), (-(W2h + 40.0), d - 25.0),
                (-W2h, d - 25.0), (-W2h, d - 90.0), (-(W1h - 229.2), d - 490.0),
                (-372.0, 410.0), (-247.0, 260.0),
            ]
        else:
            raise ValueError(f"unknown subgroup {sg!r}")
        return pts


class IeUBeamSection:
    """Irish standard U beam (U600-U12) or SU edge beam (SU11-SU12) as a
    ``sectionproperties`` Geometry.

    Examples
    --------
    >>> from bridgebeams.ukie import IeUBeamSection
    >>> u8 = IeUBeamSection("U8")
    >>> u8.dimensions.depth
    1200.0
    """

    SIZES = tuple(
        ["U600", "U700", "U1", "U3", "U5", "U7", "U8", "U9", "U10", "U11", "U12"]
        + ["SU11", "SU12"]
    )

    def __init__(self, size: str = "U8"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        row = next(r for r in data["published_properties"] if r["section"] == size)
        self.size = size
        self.published = row
        self.dimensions = IeUBeamDimensions(
            depth=float(row["depth"]),
            w1=float(row["w1"]),
            w2=float(row["w1"]) - 2.0 * (float(row["w3"]) + (65.0 if row["subgroup"] == "small" else 80.0)),
            w3=float(row["w3"]),
            subgroup=row["subgroup"],
        )

    @property
    def polygon(self) -> Polygon:
        return Polygon(self.dimensions.outline)

    @property
    def geometry(self):
        """``sectionproperties`` Geometry of the beam (millimetres)."""
        return geometry_from_polygon(self.polygon)


__all__ = ["IeUBeamDimensions", "IeUBeamSection"]
