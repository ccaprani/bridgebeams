"""Missouri DOT (MoDOT) prestressed box beams, voided slabs and solid slabs.

Source: MoDOT Engineering Policy Guide 751.21 "Prestressed Concrete Slab
and Box Beams", 751.21.1.3 Geometric Properties (figures dated 2021),
https://epg.modot.org/index.php/751.21_Prestressed_Concrete_Slab_and_Box_Beams

* ``MoDotBoxBeamSection``: adjacent 3 ft and 4 ft and spread 4 ft boxes,
  17/21/27/33/39/42 in deep (18 profiles).
* ``MoDotVoidedSlabSection``: adjacent 3 ft and 4 ft and spread 4 ft
  circular-voided slabs, 15/18/21 in deep (9 profiles).
* ``MoDotSolidSlabSection``: 48 and 52 in wide, 11 in deep (2 profiles).

Size keys: ``ADJ36-17`` = adjacent, 36 in wide, 17 in deep; ``SPR48-21`` =
spread, 48 in wide; ``SOLID48``.

Adjacent beams carry the 751.21.1.3 side shear key (5/8 in top setback,
1 1/4 in recess). Every dimension is printed; computed gross areas match
the printed A to print precision. Circular voids are 128-gons.
Millimetres, origin at soffit centre, y upward; voids are interiors.
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

DATA_FILE = "state_mo_slabs_boxes.json"
VOID_SEGMENTS = 128


def keyed_half_in(width, depth, bevel, key, bottom_zone, top_zone):
    """Right half (inches) of an adjacent beam with the MoDOT side key."""
    w = width / 2
    y_rec_top = depth - top_zone
    return [
        (0.0, 0.0), (w - bevel, 0.0), (w, bevel), (w, bottom_zone),
        (w - key["recess_depth"], bottom_zone + key["lower_slope_rise"]),
        (w - key["recess_depth"], y_rec_top - key["upper_chamfer_rise"]),
        (w - key["top_setback"], y_rec_top),
        (w - key["top_setback"], depth), (0.0, depth),
    ]


def plain_half_in(width, depth, bevel):
    w = width / 2
    return [(0.0, 0.0), (w - bevel, 0.0), (w, bevel), (w, depth), (0.0, depth)]


def box_void_in(width, y0, y1, chamfer):
    """Clockwise chamfered rectangular void ring (inches)."""
    w, c = width / 2, chamfer
    ccw = [(-w + c, y0), (w - c, y0), (w, y0 + c), (w, y1 - c),
           (w - c, y1), (-w + c, y1), (-w, y1 - c), (-w, y0 + c)]
    return list(reversed(ccw))


@dataclass(frozen=True)
class MoDotBoxDimensions:
    """Box beam dimensions in millimetres (``source_in`` holds inches)."""

    size: str
    kind: str
    width: float
    depth: float
    top_width: float
    void_width: float
    void_height: float
    source_in: dict


class MoDotBoxBeamSection:
    """MoDOT adjacent (keyed) and spread prestressed box beams."""

    SIZES = tuple(
        f"{k}-{d}" for k in ("ADJ36", "ADJ48", "SPR48") for d in (17, 21, 27, 33, 39, 42)
    )

    def __init__(self, size: str = "ADJ48-27"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = load_json(DATA_FILE)
        row = data["box_beams"][size]
        v = row["void_in"]
        w, d, bev = row["width_in"], row["depth_in"], row["soffit_bevel_in"]
        adjacent = row["kind"] == "adjacent"
        key = data["shear_key_in"]["box_and_voided"]
        self.size = size
        self.row = row
        self.provenance = row["provenance"]
        self.source_status = row["source_status"]
        self.published = row["published_in"]
        if adjacent:
            self._half_in = keyed_half_in(w, d, bev, key, key["bottom_zone"], key["top_zone"])
        else:
            self._half_in = plain_half_in(w, d, bev)
        self._void_in = box_void_in(v["width"], v["bottom_slab"], d - v["top_slab"], v["corner_chamfer"])
        top_w = w - 2 * key["top_setback"] if adjacent else w
        self.dimensions = MoDotBoxDimensions(
            size=size, kind=row["kind"], width=w * INCH_TO_MM, depth=d * INCH_TO_MM,
            top_width=top_w * INCH_TO_MM, void_width=v["width"] * INCH_TO_MM,
            void_height=(d - v["top_slab"] - v["bottom_slab"]) * INCH_TO_MM,
            source_in={"width": w, "depth": d, "void": dict(v), "soffit_bevel": bev},
        )

    @property
    def polygon(self):
        return ccw_polygon(to_mm(mirror_half(self._half_in)), [to_mm(self._void_in)])

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


@dataclass(frozen=True)
class MoDotVoidedSlabDimensions:
    """Voided slab dimensions in millimetres."""

    size: str
    kind: str
    width: float
    depth: float
    void_centre_height: float
    voids: tuple  # ((x_centre, diameter), ...) in mm


class MoDotVoidedSlabSection:
    """MoDOT adjacent (keyed) and spread circular-voided slab beams."""

    SIZES = tuple(f"{k}-{d}" for k in ("ADJ36", "ADJ48", "SPR48") for d in (15, 18, 21))

    def __init__(self, size: str = "ADJ48-18"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = load_json(DATA_FILE)
        row = data["voided_slabs"][size]
        w, d, bev = row["width_in"], row["depth_in"], row["soffit_bevel_in"]
        key = data["shear_key_in"]["box_and_voided"]
        self.size = size
        self.row = row
        self.provenance = row["provenance"]
        self.source_status = row["source_status"]
        self.published = row["published_in"]
        if row["kind"] == "adjacent":
            self._half_in = keyed_half_in(w, d, bev, key, key["bottom_zone"], key["top_zone"])
        else:
            self._half_in = plain_half_in(w, d, bev)
        cy = row["voids_in"]["centre_height"]
        self._voids_in = [(x, cy, dia) for x, dia in row["voids_in"]["x_and_diameter"]]
        self.dimensions = MoDotVoidedSlabDimensions(
            size=size, kind=row["kind"], width=w * INCH_TO_MM, depth=d * INCH_TO_MM,
            void_centre_height=cy * INCH_TO_MM,
            voids=tuple((x * INCH_TO_MM, dia * INCH_TO_MM) for x, _, dia in self._voids_in),
        )

    @property
    def polygon(self):
        holes = [to_mm(circle(x, cy, dia / 2, VOID_SEGMENTS)) for x, cy, dia in self._voids_in]
        return ccw_polygon(to_mm(mirror_half(self._half_in)), holes)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


@dataclass(frozen=True)
class MoDotSolidSlabDimensions:
    """Solid slab dimensions in millimetres."""

    size: str
    width: float
    depth: float
    top_width: float


class MoDotSolidSlabSection:
    """MoDOT 11 in solid slab beams, 48 or 52 in wide, with side keys."""

    SIZES = ("SOLID48", "SOLID52")

    def __init__(self, size: str = "SOLID48"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = load_json(DATA_FILE)
        row = data["solid_slabs"][size]
        key = data["shear_key_in"]["solid"]
        w, d, bev = row["width_in"], row["depth_in"], row["soffit_bevel_in"]
        self.size = size
        self.row = row
        self.provenance = row["provenance"]
        self.source_status = row["source_status"]
        self.published = row["published_in"]
        self._half_in = keyed_half_in(w, d, bev, key, key["bottom_zone"], key["top_zone"])
        self.dimensions = MoDotSolidSlabDimensions(
            size=size, width=w * INCH_TO_MM, depth=d * INCH_TO_MM,
            top_width=(w - 2 * key["top_setback"]) * INCH_TO_MM,
        )

    @property
    def polygon(self):
        return ccw_polygon(to_mm(mirror_half(self._half_in)))

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = [
    "MoDotBoxDimensions", "MoDotBoxBeamSection",
    "MoDotVoidedSlabDimensions", "MoDotVoidedSlabSection",
    "MoDotSolidSlabDimensions", "MoDotSolidSlabSection",
]
