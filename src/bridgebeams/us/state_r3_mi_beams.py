"""Michigan local-agency precast beams (MDOT research report OR15-182, App. K).

Source (SHA-256 and page locators in data/state_r3_mi_beams.json): MDOT
Final Report OR15-182 (2018), Appendix K "Recommended Bridge Design Guide"
for secondary-route bridges, plan sheets dated 05/09/18:

* ``MiSpreadBoxBeamSection``: SBB 003 spread box beams 17x36, 21x36,
  21x48, 27x48, 33x48, 39x48, 48x48 in (7 profiles, ``"SBB27x48"``).
* ``MiSideBySideBoxBeamSection``: SSBB 003/004 side-by-side box beams
  17x36, 21x48, 27x48, 33x48, 39x48 in, interior (keyed both sides) and
  fascia (keyed one side, 9 in top slab) (10 profiles, ``"SSBB27x48-INT"``,
  ``"SSBB27x48-FAS"``). Shear-key offsets are estimates from the drawing.
* ``MiBulbTeeSection``: BTB 002 bulb tees 36/42/48 in deep, 49 in top and
  40 in bottom flange, 8 in web (3 profiles, ``"BT36"``).

The report states these plans are recommendations, not MDOT standards.
Gross midspan concrete only; millimetres, origin at soffit centre, y up;
box voids are polygon interiors.
"""

from __future__ import annotations

from dataclasses import dataclass

from bridgebeams._geometry import geometry_from_polygon
from bridgebeams.us.state_common import INCH_TO_MM, ccw_polygon, dedupe, load_json, mirror_half, to_mm

DATA_FILE = "state_r3_mi_beams.json"


def _data() -> dict:
    return load_json(DATA_FILE)


def box_void_in(width, y0, y1, chamfer):
    """Clockwise chamfered rectangular void ring (inches), centred on x = 0."""
    w, c = width / 2, chamfer
    ccw = [(-w + c, y0), (w - c, y0), (w, y0 + c), (w, y1 - c),
           (w - c, y1), (-w + c, y1), (-w, y1 - c), (-w, y0 + c)]
    return list(reversed(ccw))


def keyed_side_in(w, depth, bevel, key):
    """Right-side path (inches) from the soffit bevel up to the top, with shear key."""
    y_key_top = depth - key["top_zone"]
    y_key_bot = y_key_top - key["key_height"]
    s, r = key["top_setback"], key["recess"]
    return [
        (w - bevel, 0.0), (w, bevel), (w, y_key_bot - key["lower_slope_rise"]),
        (w - r, y_key_bot), (w - r, y_key_top - (r - s)), (w - s, y_key_top), (w - s, depth),
    ]


def plain_side_in(w, depth, bevel):
    return [(w - bevel, 0.0), (w, bevel), (w, depth)]


def box_outline_in(width, depth, bevel, key, key_right: bool, key_left: bool):
    """CCW outline (inches) of a box beam with optional side keys."""
    w = width / 2
    right = keyed_side_in(w, depth, bevel, key) if key_right else plain_side_in(w, depth, bevel)
    left = keyed_side_in(w, depth, bevel, key) if key_left else plain_side_in(w, depth, bevel)
    left_mirrored = [(-x, y) for x, y in reversed(left)]
    return dedupe(right + left_mirrored)


def bulb_tee_half_in(depth, t):
    """Right half (inches) of the BTB 002 bulb tee from (0, 0) to (0, depth)."""
    bw, tw, wb = t["bottom_width"] / 2, t["top_width"] / 2, t["web"] / 2
    y1 = t["bottom_edge"]
    y2 = y1 + t["bottom_taper_rise"]
    y3 = y2 + t["bottom_fillet_rise"]
    yt1 = depth - t["top_edge"]
    yt2 = yt1 - t["top_taper_rise"]
    yt3 = yt2 - t["top_fillet_rise"]
    return [
        (0.0, 0.0), (bw - t["bottom_bevel"], 0.0), (bw, t["bottom_bevel"]), (bw, y1),
        (bw - t["bottom_taper_run"], y2), (wb, y3), (wb, yt3),
        (wb + t["top_fillet_run"], yt2), (tw, yt1), (tw, depth), (0.0, depth),
    ]


@dataclass(frozen=True)
class MiBoxBeamDimensions:
    """Michigan box beam dimensions in millimetres (``source_in`` in inches)."""

    size: str
    kind: str
    width: float
    depth: float
    top_slab: float
    bottom_slab: float
    web: float
    void_width: float
    void_height: float
    source_in: dict


class _MiBoxBase:
    _GROUP = ""

    def _build(self, size, row, fam, kind, key_right, key_left, top_slab, solid=False):
        data = _data()
        grp = data[self._GROUP]
        d, w = row["depth"], row["width"]
        bev = grp["common_in"]["soffit_bevel"]
        key = grp.get("shear_key_in")
        self.size = size
        self.family = fam
        self.kind = kind
        self.row = row
        self.provenance = grp["provenance"]
        self.source_status = data["source_status"]
        self.published = None
        self._outline_in = box_outline_in(w, d, bev, key, key_right, key_left)
        vw = w - 2 * row["web"]
        y0, y1 = row["bottom_slab"], d - top_slab
        self._void_in = None if solid else box_void_in(vw, y0, y1, row["void_chamfer"])
        self.dimensions = MiBoxBeamDimensions(
            size=size, kind=kind, width=w * INCH_TO_MM, depth=d * INCH_TO_MM,
            top_slab=(d if solid else top_slab) * INCH_TO_MM,
            bottom_slab=row["bottom_slab"] * INCH_TO_MM, web=row["web"] * INCH_TO_MM,
            void_width=0.0 if solid else vw * INCH_TO_MM,
            void_height=0.0 if solid else (y1 - y0) * INCH_TO_MM,
            source_in=dict(row),
        )

    @property
    def polygon(self):
        holes = [] if self._void_in is None else [to_mm(self._void_in)]
        return ccw_polygon(to_mm(self._outline_in), holes)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


class MiSpreadBoxBeamSection(_MiBoxBase):
    """MDOT OR15-182 SBB 003 spread box beam (no shear keys)."""

    _GROUP = "spread_box"
    SIZES = ("SBB17x36", "SBB21x36", "SBB21x48", "SBB27x48", "SBB33x48", "SBB39x48", "SBB48x48")

    def __init__(self, size: str = "SBB27x48"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        row = _data()[self._GROUP]["sections"][size]
        self._build(size, row, size, "spread", False, False, row["top_slab"])


class MiSideBySideBoxBeamSection(_MiBoxBase):
    """MDOT OR15-182 SSBB 003/004 side-by-side box beam, interior or fascia.

    Interior beams are keyed both sides; fascia beams on the -x side only
    and have a 9 in top slab (17x36 fascia is solid, as drawn).
    """

    _GROUP = "side_by_side_box"
    FAMILIES = ("SSBB17x36", "SSBB21x48", "SSBB27x48", "SSBB33x48", "SSBB39x48")
    SIZES = tuple(f"{f}-{k}" for f in FAMILIES for k in ("INT", "FAS"))

    def __init__(self, size: str = "SSBB27x48-INT"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        fam, kind = size.split("-")
        row = _data()[self._GROUP]["sections"][fam]
        if kind == "INT":
            self._build(size, row, fam, "interior", True, True, row["top_slab"])
        else:
            solid = row["fascia_top_slab"] is None
            self._build(size, row, fam, "fascia", False, True,
                        row["top_slab"] if solid else row["fascia_top_slab"], solid=solid)


@dataclass(frozen=True)
class MiBulbTeeDimensions:
    """Michigan bulb tee dimensions in millimetres."""

    size: str
    depth: float
    top_width: float
    bottom_width: float
    web: float
    right_half: tuple[tuple[float, float], ...]


class MiBulbTeeSection:
    """MDOT OR15-182 BTB 002 bulb-tee girder, 36/42/48 in deep."""

    SIZES = ("BT36", "BT42", "BT48")

    def __init__(self, size: str = "BT36"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        grp = _data()["bulb_tee"]
        t = grp["template_in"]
        d = grp["sections"][size]["depth"]
        self.size = size
        self.provenance = grp["provenance"]
        self.source_status = _data()["source_status"]
        self.published = grp["published_weights"]
        half = bulb_tee_half_in(d, t)
        self._ring_in = mirror_half(half)
        self.dimensions = MiBulbTeeDimensions(
            size=size, depth=d * INCH_TO_MM, top_width=t["top_width"] * INCH_TO_MM,
            bottom_width=t["bottom_width"] * INCH_TO_MM, web=t["web"] * INCH_TO_MM,
            right_half=tuple(to_mm(half)),
        )

    @property
    def polygon(self):
        return ccw_polygon(to_mm(self._ring_in))

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = [
    "MiBoxBeamDimensions", "MiSpreadBoxBeamSection", "MiSideBySideBoxBeamSection",
    "MiBulbTeeDimensions", "MiBulbTeeSection",
]
