"""NYSDOT prestressed units: box beams, slab units and PCEF bulb tees.

Source: New York State DOT Bridge Detail Sheets BD-PC (US customary), 2026
set "BD-PC_01-26" (approved 13 January 2026, EB 26-004, effective for
lettings from 1 May 2026):

* BD-PC1 / BD-PC2 (PDF pp1-2): 3'-0" and 4'-0" slab units and box beams,
  shear-key recess detail, property tables.
* BD-PC14 (PDF p14): PCEF bulb tees PCEF-39 ... PCEF-79 and property table.
  (The AASHTO Type I-VI on the same sheet are not repeated here; see
  :class:`bridgebeams.us.AashtoIBeamSection`.)

The NEBT (BD-PC15) and NEXT D/F (BD-PC31/36) sheets of the same set are
not implemented here: they duplicate the PCI Northeast NEBT/NEXT profiles
in :mod:`bridgebeams.us.pci_regional_products` (outlines agree within
~0.2% area). Their NYSDOT transcriptions remain in the JSON data.
Gross concrete only (interior unit): no strands, deck, grinding allowance
or fascia drip grooves. Millimetres, origin at the soffit centre, y up.
"""

from __future__ import annotations

from dataclasses import dataclass

from bridgebeams._geometry import geometry_from_polygon
from bridgebeams.us.state_common import (
    INCH_TO_MM,
    ccw_polygon,
    circle,
    load_json,
    mirror_half,
    to_mm,
)

DATA_FILE = "state_ny_bd_pc.json"
CIRCLE_N = 128


def _data() -> dict:
    return load_json(DATA_FILE)


# ------------------------------------------------------------------ outlines
def keyed_unit_half_in(width: float, depth: float, k: dict) -> list[tuple[float, float]]:
    """Right half of a BD-PC1/2 slab unit or box (shear-key recess detail)."""
    h = width / 2
    c = k["soffit_chamfer_in"]
    lower, upper = k["lower_band_in"], k["upper_band_in"]
    r_low, r_up = k["recess_from_bottom_face_in"], k["top_band_inset_in"]
    return [
        (0.0, 0.0),
        (h - c, 0.0),
        (h, c),
        (h, lower),
        (h - r_low, lower + r_low),
        (h - r_low, depth - upper - (r_low - r_up)),
        (h - r_up, depth - upper),
        (h - r_up, depth),
        (0.0, depth),
    ]


def ny_box_void_in(width: float, depth: float, t: dict) -> list[tuple[float, float]]:
    x = width / 2 - t["recess_from_bottom_face_in"] - t["web_in"]
    y0, y1, f = t["bottom_slab_in"], depth - t["top_slab_in"], t["void_chamfer_in"]
    return [(-x + f, y0), (x - f, y0), (x, y0 + f), (x, y1 - f), (x - f, y1),
            (-x + f, y1), (-x, y1 - f), (-x, y0 + f)]


def pcef_half_in(depth: float, t: dict) -> list[tuple[float, float]]:
    w = t["web_in"] / 2
    yb1 = t["bottom_edge_in"]
    yb2 = yb1 + t["bottom_taper_rise_in"]
    yb3 = yb2 + t["bottom_chamfer_in"]
    yt1 = depth - t["top_tip_in"]
    yt2 = yt1 - t["top_taper_drop_in"]
    return [
        (0.0, 0.0),
        (t["bottom_width_in"] / 2, 0.0),
        (t["bottom_width_in"] / 2, yb1),
        (w + t["bottom_chamfer_in"], yb2),
        (w, yb3),
        (w, yt2 - t["top_chamfer_in"]),
        (w + t["top_chamfer_in"], yt2),
        (t["top_width_in"] / 2, yt1),
        (t["top_width_in"] / 2, depth),
        (0.0, depth),
    ]


@dataclass(frozen=True)
class NyUnitDimensions:
    """Principal dimensions in millimetres."""

    size: str
    width: float
    depth: float
    n_voids: int = 0


class _NyBase:
    FAMILY = ""
    SIZES: tuple[str, ...] = ()

    def _init_row(self, size):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        fam = _data()["families"][self.FAMILY]
        row = fam["sections"][size]
        self.size = size
        self.row = row
        self.published = row["published"]
        self.provenance = row.get("provenance", fam["provenance"])
        self.source_status = fam["source_status"]
        return fam, row

    @property
    def polygon(self):
        """Gross concrete outline (mm), anticlockwise; voids clockwise."""
        return ccw_polygon(to_mm(self._shell_in), [to_mm(h) for h in self._holes_in])

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


class NyBoxBeamSection(_NyBase):
    """NYSDOT BD-PC1/PC2 box beams B36"/B48" x 24"-54" (e.g. ``"B48x33"``)."""

    FAMILY = "ny_box_beam"
    SIZES = tuple(f"B{w}x{d}" for w in (36, 48) for d in range(24, 55, 3))

    def __init__(self, size: str = "B48x33"):
        fam, row = self._init_row(size)
        t = fam["template_in"]
        w, d = row["width_in"], row["depth_in"]
        self._shell_in = mirror_half(keyed_unit_half_in(w, d, t))
        self._holes_in = [ny_box_void_in(w, d, t)]
        self.dimensions = NyUnitDimensions(size, w * INCH_TO_MM, d * INCH_TO_MM, 1)


class NySlabUnitSection(_NyBase):
    """NYSDOT BD-PC1/PC2 slab units S36"/S48" x 12"-21" (e.g. ``"S48x18"``)."""

    FAMILY = "ny_slab_unit"
    SIZES = tuple(f"S{w}x{d}" for w in (36, 48) for d in (12, 15, 18, 21))

    def __init__(self, size: str = "S48x18"):
        fam, row = self._init_row(size)
        t = fam["template_in"]
        w, d = row["width_in"], row["depth_in"]
        self._shell_in = mirror_half(keyed_unit_half_in(w, d, t))
        self._holes_in = [circle(x, d / 2, dia / 2, CIRCLE_N) for x, dia in row["voids_in"]]
        self.dimensions = NyUnitDimensions(size, w * INCH_TO_MM, d * INCH_TO_MM, len(self._holes_in))


@dataclass(frozen=True)
class NyGirderDimensions:
    """Principal dimensions in millimetres."""

    size: str
    depth: float
    top_width: float
    bottom_width: float
    web_width: float


class NyPcefBulbTeeSection(_NyBase):
    """NYSDOT BD-PC14 PCEF bulb tees PCEF-39 ... PCEF-79."""

    FAMILY = "ny_pcef_bulb_tee"
    SIZES = tuple(f"PCEF-{d}" for d in (39, 47, 55, 63, 71, 79))

    def __init__(self, size: str = "PCEF-63"):
        fam, row = self._init_row(size)
        t = fam["template_in"]
        self._shell_in = mirror_half(pcef_half_in(row["depth_in"], t))
        self._holes_in = []
        self.dimensions = NyGirderDimensions(size, row["depth_in"] * INCH_TO_MM,
                                             t["top_width_in"] * INCH_TO_MM,
                                             t["bottom_width_in"] * INCH_TO_MM,
                                             t["web_in"] * INCH_TO_MM)


__all__ = [
    "NyUnitDimensions", "NyBoxBeamSection", "NySlabUnitSection",
    "NyGirderDimensions", "NyPcefBulbTeeSection",
]
