"""Illinois DOT (IDOT) precast prestressed concrete deck beams.

Source: IDOT Bridge Cell Library, 'Beams-Prestressed Deck Beams' (cells
PD-<depth><width>-0 dated 4/4/2025), SECTION B-B 'Showing dimensions' on
PDF pp4-37. Twelve sections: 11x48, 11x52, 17x36, 17x48, 21x36, 21x48,
27x36, 27x48, 33x36, 33x48, 42x36, 42x48 (depth x width, inches). All
dimensions are printed; see data/state_il_deck_beams.json.

Validation: IDOT Design Guide 3.5 (May 2019) example gives A = 569.9 in2,
I = 49,697 in4 and Cb = 13.30 in for a 27x36 beam; the transcribed polygon
reproduces all three. The full BM Table 3.5.4-1 was not retrievable.

Interior beam (key on both faces). Gross concrete only; millimetres, origin
at soffit centre, y upwards.
"""

from __future__ import annotations

from dataclasses import dataclass

from bridgebeams._geometry import geometry_from_polygon
from bridgebeams.us.state_common import INCH_TO_MM, ccw_polygon, load_json, mirror_half, to_mm

DATA_FILE = "state_il_deck_beams.json"


def il_deck_beam_rings_in(row: dict, t: dict):
    """(shell, void-or-None) rings in inches."""
    w, d = row["width"], row["depth"]
    top, key, _ = row["bands"]
    h = w / 2
    ch = t["soffit_chamfer"]
    y_key_bottom = d - top - key
    half = [
        (0.0, 0.0), (h - ch, 0.0), (h, ch), (h, y_key_bottom),
        (h - t["key_inset"], y_key_bottom + t["key_lower_transition"]),
        (h - t["key_inset"], d - top - t["key_upper_transition"]),
        (h - t["top_face_inset"], d - top),
        (h - t["top_face_inset"], d), (0.0, d),
    ]
    shell = mirror_half(half)
    if not row["void"]:
        return shell, None
    vw, vh = row["void"]
    x, c = vw / 2, t["void_chamfer"]
    y0 = t["slab"]
    y1 = y0 + vh
    void = [(x - c, y0), (x, y0 + c), (x, y1 - c), (x - c, y1),
            (-x + c, y1), (-x, y1 - c), (-x, y0 + c), (-x + c, y0)]
    return shell, void


@dataclass(frozen=True)
class IlDeckBeamDimensions:
    """IDOT deck beam dimensions in millimetres."""

    size: str
    depth: float
    width: float
    top_width: float
    web: float | None
    void_width: float | None
    void_height: float | None


class IlDeckBeamSection:
    """IDOT PPC deck beam by designation ``"<depth>x<width>"`` (inches)."""

    SIZES = ("11x48", "11x52", "17x36", "17x48", "21x36", "21x48",
             "27x36", "27x48", "33x36", "33x48", "42x36", "42x48")

    def __init__(self, size: str = "27x48"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = load_json(DATA_FILE)
        row = data["sections"][size]
        t = data["template_in"]
        self.size = size
        self.row = row
        self.provenance = row["provenance"]
        self.source_status = data["source_status"]
        self.published = row.get("published")
        self._shell_in, self._void_in = il_deck_beam_rings_in(row, t)
        void = row["void"]
        self.dimensions = IlDeckBeamDimensions(
            size=size,
            depth=row["depth"] * INCH_TO_MM,
            width=row["width"] * INCH_TO_MM,
            top_width=(row["width"] - 2 * t["top_face_inset"]) * INCH_TO_MM,
            web=row["web"] * INCH_TO_MM if row["web"] else None,
            void_width=void[0] * INCH_TO_MM if void else None,
            void_height=void[1] * INCH_TO_MM if void else None,
        )

    @property
    def polygon(self):
        holes = [to_mm(self._void_in)] if self._void_in else []
        return ccw_polygon(to_mm(self._shell_in), holes)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = ["IlDeckBeamDimensions", "IlDeckBeamSection", "il_deck_beam_rings_in"]
