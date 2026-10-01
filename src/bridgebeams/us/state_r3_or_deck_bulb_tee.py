"""Oregon DOT deck bulb-tee girders DKBT36/45/60 (BR360, BR365, BR375).

Sources (URLs, SHA-256 and page locators in data/state_r3_or_deck_bulb_tee.json):
Oregon Standard Drawings 2024, BR300 series (effective 2026-06-01), sheets
BR360/BR365/BR375, with the owner-supplied 2021-edition BR360 and BR375
sheets as identical corroboration.

The top flange width "W" is set per project (60 to 102 in per the sheets'
deck-reinforcement table). ``SIZES`` encode W = 60, 72, 84 and 102 in as
distinct profiles, e.g. ``"DKBT45-W72"``; any W in [60, 102] may be given
with ``flange_width`` (inches). Gross concrete only; millimetres, origin
at soffit centre, y upwards.
"""

from __future__ import annotations

from dataclasses import dataclass

from bridgebeams._geometry import geometry_from_polygon
from bridgebeams.us.state_common import INCH_TO_MM, ccw_polygon, load_json, mirror_half, to_mm

DATA_FILE = "state_r3_or_deck_bulb_tee.json"


def _data() -> dict:
    return load_json(DATA_FILE)


def dkbt_right_half_in(depth: float, flange_width: float, c: dict):
    """Right half (inches) of an ODOT deck bulb-tee from (0, 0) to (0, depth)."""
    bb, tw = c["bulb_width"] / 2, c["web_width"] / 2
    ch = c["soffit_chamfer"]
    y_web0 = c["bulb_edge"] + c["bulb_taper_rise"]
    y_flat = depth - c["flange_edge"]
    y_fil = y_flat - c["flange_taper_rise"]
    y_web1 = y_fil - c["fillet_rise"]
    x_fil = tw + c["fillet_run"]
    x_flat = x_fil + c["flange_taper_run"]
    return [
        (0.0, 0.0), (bb - ch, 0.0), (bb, ch), (bb, c["bulb_edge"]),
        (tw, y_web0), (tw, y_web1), (x_fil, y_fil), (x_flat, y_flat),
        (flange_width / 2, y_flat), (flange_width / 2, depth), (0.0, depth),
    ]


@dataclass(frozen=True)
class OrDeckBulbTeeDimensions:
    """ODOT deck bulb-tee dimensions in millimetres."""

    size: str
    depth: float
    flange_width: float
    bulb_width: float
    web_width: float
    flange_edge_thickness: float
    soffit_chamfer: float
    right_half: tuple[tuple[float, float], ...]


class OrDeckBulbTeeSection:
    """ODOT DKBT36/45/60 deck bulb-tee (BR360/BR365/BR375) at a given flange width."""

    FAMILIES = ("DKBT36", "DKBT45", "DKBT60")
    WIDTHS = (60, 72, 84, 102)
    SIZES = (
        "DKBT36-W60", "DKBT36-W72", "DKBT36-W84", "DKBT36-W102",
        "DKBT45-W60", "DKBT45-W72", "DKBT45-W84", "DKBT45-W102",
        "DKBT60-W60", "DKBT60-W72", "DKBT60-W84", "DKBT60-W102",
    )

    def __init__(self, size: str = "DKBT45-W72", flange_width: float | None = None):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _data()
        fam, w = size.split("-W")
        w = float(w) if flange_width is None else float(flange_width)
        lo, hi = data["flange_width_range"]
        if not lo <= w <= hi:
            raise ValueError(f"flange_width must be in [{lo}, {hi}] in, got {w}")
        row = data["sections"][fam]
        c = data["common_in"]
        self.size = size
        self.family = fam
        self.flange_width_in = w
        self.row = row
        self.provenance = data["provenance"]
        self.source_status = data["source_status"]
        self.published = None
        half = dkbt_right_half_in(row["depth"], w, c)
        self._ring_in = mirror_half(half)
        self.dimensions = OrDeckBulbTeeDimensions(
            size=size, depth=row["depth"] * INCH_TO_MM, flange_width=w * INCH_TO_MM,
            bulb_width=c["bulb_width"] * INCH_TO_MM, web_width=c["web_width"] * INCH_TO_MM,
            flange_edge_thickness=c["flange_edge"] * INCH_TO_MM,
            soffit_chamfer=c["soffit_chamfer"] * INCH_TO_MM,
            right_half=tuple(to_mm(half)),
        )

    @property
    def polygon(self):
        return ccw_polygon(to_mm(self._ring_in))

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = ["OrDeckBulbTeeDimensions", "OrDeckBulbTeeSection", "dkbt_right_half_in"]
