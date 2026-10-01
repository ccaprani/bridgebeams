"""Ohio DOT prestressed concrete I-beams (standard bridge drawing PSID-1-13).

ODOT Bridge Design Manual (2020 Edition, January 2026 update) section
308.2.3.4 limits prestressed I-beams to AASHTO Types II-IV, the modified
Type IV (60, 66 and 72 in) and WF36-49 to WF72-49, "as shown in the
standard bridge drawing PSID-1-13". The BDM prints no geometry; the
outlines here are the concrete-outline lines of the PSID-1-13 MicroStation
drawing (rev. 2018-07-20), read at 1250 UOR per inch and exact to 1/16 in.
They reproduce Brice et al. (2021) Table A.10 exactly (A, yb, Ix, Iy).

Source URLs, SHA-256, sheet locators and printed properties are in
``data/state_r3_oh_i_beams.json``. Gross concrete only; millimetres,
origin at soffit centre, y upwards.
"""

from __future__ import annotations

from dataclasses import dataclass

from bridgebeams._geometry import geometry_from_polygon
from bridgebeams.us.state_common import INCH_TO_MM, ccw_polygon, load_json, mirror_half, to_mm

DATA_FILE = "state_r3_oh_i_beams.json"


def _data() -> dict:
    return load_json(DATA_FILE)


@dataclass(frozen=True)
class OhIBeamDimensions:
    """ODOT PSID-1-13 I-beam dimensions in millimetres."""

    size: str
    depth: float
    top_width: float
    bottom_width: float
    web_width: float
    soffit_chamfer: float
    right_half: tuple[tuple[float, float], ...]


class _OhIBeamBase:
    SIZES: tuple[str, ...] = ()
    DEFAULT = ""

    def __init__(self, size: str | None = None):
        size = self.DEFAULT if size is None else size
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _data()
        row = data["sections"][size]
        self.size = size
        self.row = row
        self.provenance = data["provenance"]
        self.source_status = data["source_status"]
        self.published = row["published_odot"]
        self.published_brice2021 = row.get("published_brice2021")
        half = [tuple(p) for p in row["right_half"]]
        self._ring_in = mirror_half(half)
        xs = [x for x, _ in half]
        d = row["depth"]
        top = max(x for x, y in half if y == d)
        bottom = max(xs[:3])
        web = min(x for x, y in half if 0 < y < d and x > 0)
        chamfer = half[2][1] - half[1][1]
        self.dimensions = OhIBeamDimensions(
            size=size, depth=d * INCH_TO_MM,
            top_width=2 * top * INCH_TO_MM, bottom_width=2 * bottom * INCH_TO_MM,
            web_width=2 * web * INCH_TO_MM, soffit_chamfer=chamfer * INCH_TO_MM,
            right_half=tuple(to_mm(half)),
        )

    @property
    def polygon(self):
        return ccw_polygon(to_mm(self._ring_in))

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


class OhAashtoIBeamSection(_OhIBeamBase):
    """ODOT AASHTO Type II/III/IV and modified Type IV (60/66/72 in), PSID-1-13 sheet 1."""

    SIZES = ("II", "III", "IV", "MOD-IV-60", "MOD-IV-66", "MOD-IV-72")
    DEFAULT = "IV"


class OhWfBeamSection(_OhIBeamBase):
    """ODOT WF36-49 ... WF72-49 wide-flange I-beam (49 in top flange), PSID-1-13 sheets 2-3."""

    SIZES = ("WF36-49", "WF42-49", "WF48-49", "WF54-49", "WF60-49", "WF66-49", "WF72-49")
    DEFAULT = "WF54-49"


__all__ = ["OhIBeamDimensions", "OhAashtoIBeamSection", "OhWfBeamSection"]
