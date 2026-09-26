"""Caltrans California Standard precast girders (Bridge Design Memo 5.3, Sept 2023).

Source: Caltrans Bridge Design Memo 5.3 "Precast Prestressed Girders",
September 2023, Section 5.3.4.1, Figures/Tables 5.3.4.1-1 to -6 (PDF pages
3-8). See ``data/state_ca_girders.json`` for URL, SHA-256, locators and all
conventions and residuals.

* ``CaIGirderSection``: CA I36-I66 (exact, all dimensions printed).
* ``CaBulbTeeSection``: CA BT49-BT85 (metric-converted, R 7-7/8 in fillets).
* ``CaWideFlangeSection``: CA WF48-WF120 pretensioned and ``...PT``
  post-tensioned (r = 10 in and 2 1/2 in tangent fillets).
* ``CaBathTubSection``: CA TUB55-TUB85 open-top tub girders.
* ``CaVoidedSlabSection``: SI-SIV, 36/48 in wide; shear key undimensioned
  (provenance ``estimate``), no published properties.

Gross concrete only. Millimetres, origin at the soffit centre, y upward.
Caltrans' xs1-121-1 bulb-tee detail sheet leaves depth as a project
variable, so named depths come from the Memo only.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from bridgebeams._geometry import geometry_from_polygon
from bridgebeams.us.state_common import (
    INCH_TO_MM,
    ccw_polygon,
    circle,
    dedupe,
    filleted_path,
    load_json,
    mirror_half,
    to_mm,
)

DATA_FILE = "state_ca_girders.json"


def _family(name: str) -> dict:
    data = load_json(DATA_FILE)
    return data, data["families"][name]


@dataclass(frozen=True)
class CaGirderDimensions:
    """Principal dimensions in millimetres plus the right-half outline."""

    size: str
    depth: float
    top_width: float
    bottom_width: float
    web_width: float
    right_half: tuple[tuple[float, float], ...]


class _CaSymmetric:
    FAMILY = ""
    SIZES: tuple[str, ...] = ()

    def __init__(self, size: str):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data, fam = _family(self.FAMILY)
        row = fam["sections"][size]
        self.size = size
        self.row = row
        self.provenance = row["provenance"]
        self.source_status = data["source_status"]
        self.published = row["published"]
        half, top, bot, web = self._half_in(row, fam["template_in"])
        self._ring_in = mirror_half(half)
        self.dimensions = CaGirderDimensions(
            size=size,
            depth=row["depth_in"] * INCH_TO_MM,
            top_width=top * INCH_TO_MM,
            bottom_width=bot * INCH_TO_MM,
            web_width=web * INCH_TO_MM,
            right_half=tuple(to_mm(half)),
        )

    def _half_in(self, row, t):  # pragma: no cover - abstract
        raise NotImplementedError

    @property
    def polygon(self):
        """Gross concrete outline (mm), anticlockwise."""
        return ccw_polygon(to_mm(self._ring_in))

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


class CaIGirderSection(_CaSymmetric):
    """California Standard "I" girder, e.g. ``CaIGirderSection("CA I48")``."""

    FAMILY = "I"
    SIZES = ("CA I36", "CA I42", "CA I48", "CA I54", "CA I60", "CA I66")

    def __init__(self, size: str = "CA I48"):
        super().__init__(size)

    def _half_in(self, row, t):
        d = row["depth_in"]
        tw, tt, bb = t["web"] / 2, t["top_width"] / 2, t["bottom_width"] / 2
        half = [
            (0.0, 0.0), (bb, 0.0), (bb, t["bottom_edge"]),
            (tw, t["bottom_edge"] + t["bottom_taper"]),
            (tw, d - t["top_edge"] - t["top_taper"]),
            (tt, d - t["top_edge"]), (tt, d), (0.0, d),
        ]
        return half, t["top_width"], t["bottom_width"], t["web"]


class CaBulbTeeSection(_CaSymmetric):
    """California Standard "Bulb-Tee" girder, e.g. ``CaBulbTeeSection("CA BT67")``."""

    FAMILY = "BT"
    SIZES = ("CA BT49", "CA BT55", "CA BT61", "CA BT67", "CA BT73", "CA BT79", "CA BT85")

    def __init__(self, size: str = "CA BT67"):
        super().__init__(size)

    def _half_in(self, row, t):
        d = row["depth_in"]
        tw, tt, bb = t["web"] / 2, t["top_width"] / 2, t["bottom_width"] / 2
        r = t["fillet_radius"]
        pts = [
            (0.0, 0.0), (bb, 0.0), (bb, t["bottom_edge"]),
            (tw, t["bottom_edge"] + t["bottom_taper"]),
            (tw, d - t["top_edge"] - t["top_taper"]),
            (tt, d - t["top_edge"]), (tt, d), (0.0, d),
        ]
        return filleted_path(pts, {3: r, 4: r}), t["top_width"], t["bottom_width"], t["web"]


class CaWideFlangeSection(_CaSymmetric):
    """California Standard "Wide-Flange" girder.

    Pretensioned ``"CA WF48"`` ... ``"CA WF120"`` and post-tensioned
    ``"CA WF48PT"`` ... ``"CA WF120PT"`` (wider web and flanges).
    """

    FAMILY = "WF"
    SIZES = tuple(f"CA WF{d}" for d in range(48, 121, 6)) + tuple(
        f"CA WF{d}PT" for d in range(48, 121, 6))

    def __init__(self, size: str = "CA WF72"):
        super().__init__(size)

    def _half_in(self, row, t):
        v = t[row["variant"]]
        d = row["depth_in"]
        tw, tt, bb = v["web"] / 2, v["top_width"] / 2, v["bottom_width"] / 2
        c, rs, rw = t["soffit_chamfer"], t["flange_tip_radius"], t["web_fillet_radius"]
        pts = [
            (0.0, 0.0), (bb - c, 0.0), (bb, c), (bb, t["bottom_edge"]),
            (tw, t["bottom_edge"] + t["bottom_taper_rise"]),
            (tw, d - t["top_edge"] - t["top_taper_rise"]),
            (tt, d - t["top_edge"]), (tt, d), (0.0, d),
        ]
        half = filleted_path(pts, {3: rs, 4: rw, 5: rw, 6: rs})
        return half, v["top_width"], v["bottom_width"], v["web"]


@dataclass(frozen=True)
class CaBathTubDimensions:
    """Tub girder dimensions in millimetres."""

    size: str
    depth: float
    bottom_width: float
    top_width: float
    web_thickness: float
    bottom_slab: float


class CaBathTubSection:
    """California Standard "Bath-Tub" girder, e.g. ``CaBathTubSection("CA TUB67")``.

    Open-top U section: the polygon is a single (non-convex) ring.
    """

    SIZES = ("CA TUB55", "CA TUB61", "CA TUB67", "CA TUB73", "CA TUB79", "CA TUB85")

    def __init__(self, size: str = "CA TUB67"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data, fam = _family("TUB")
        row = fam["sections"][size]
        t = fam["template_in"]
        self.size = size
        self.row = row
        self.provenance = row["provenance"]
        self.source_status = data["source_status"]
        self.published = row["published"]
        d = row["depth_in"]
        b = t["bottom_width"] / 2
        s = t["web_slope_h_per_v"]
        off = t["web_normal_thickness"] * math.sqrt(1 + s * s)
        slab, f = t["bottom_slab"], t["bottom_fillet"]

        def xo(y):
            return b + s * y

        def xi(y):
            return b - off + s * y

        xt = xo(d)
        xin = xt - t["flange_width"]
        right = [
            (xo(0.0), 0.0), (xt, d),
            (xin + t["ledge_width"], d), (xin + t["ledge_width"], d - t["ledge_depth"]),
            (xin, d - t["ledge_depth"]), (xin, d - t["inner_vertical_to"]),
            (xi(d - t["incline_to"]), d - t["incline_to"]),
            (xi(slab + f), slab + f), (xi(slab) - f, slab),
        ]
        # Ring: right half from soffit to the inner floor, then mirrored back.
        ring = right + [(-x, y) for x, y in reversed(right)]
        self._ring_in = dedupe(ring)
        self.dimensions = CaBathTubDimensions(
            size=size,
            depth=d * INCH_TO_MM,
            bottom_width=t["bottom_width"] * INCH_TO_MM,
            top_width=2 * xt * INCH_TO_MM,
            web_thickness=t["web_normal_thickness"] * INCH_TO_MM,
            bottom_slab=slab * INCH_TO_MM,
        )

    @property
    def polygon(self):
        return ccw_polygon(to_mm(self._ring_in))

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


@dataclass(frozen=True)
class CaVoidedSlabDimensions:
    """Voided slab dimensions in millimetres."""

    size: str
    width: float
    depth: float
    voids: tuple[tuple[float, float, float], ...]  # (x centre, y centre, diameter)


class CaVoidedSlabSection:
    """California Standard "Voided" slab, e.g. ``CaVoidedSlabSection("SIII-48")``.

    Provenance ``estimate``: the shear-key recess is drawn but not dimensioned.
    """

    SIZES = ("SI-36", "SI-48", "SII-36", "SII-48", "SIII-36", "SIII-48", "SIV-36", "SIV-48")

    def __init__(self, size: str = "SIII-48"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data, fam = _family("VOIDED_SLAB")
        row = fam["sections"][size]
        k = fam["key_estimate_in"]
        self.size = size
        self.row = row
        self.provenance = row["provenance"]
        self.source_status = data["source_status"]
        self.published = row["published"]
        w, d = row["width_in"], row["depth_in"]
        b = w / 2
        y_lo, y_hi = d / 3, d - d / 3
        half = [
            (0.0, 0.0), (b, 0.0), (b, y_lo), (b - k["recess"], y_lo),
            (b - k["recess"], y_hi - k["chamfer_rise"]),
            (b - k["top_inset"], y_hi), (b - k["top_inset"], d), (0.0, d),
        ]
        self._ring_in = mirror_half(half)
        self.dimensions = CaVoidedSlabDimensions(
            size=size,
            width=w * INCH_TO_MM,
            depth=d * INCH_TO_MM,
            voids=tuple((x * INCH_TO_MM, d / 2 * INCH_TO_MM, dia * INCH_TO_MM)
                        for x, dia in row["voids_x_dia_in"]),
        )

    @property
    def polygon(self):
        holes = [circle(x, y, dia / 2, 96) for x, y, dia in self.dimensions.voids]
        return ccw_polygon(to_mm(self._ring_in), holes)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = [
    "CaGirderDimensions",
    "CaIGirderSection",
    "CaBulbTeeSection",
    "CaWideFlangeSection",
    "CaBathTubDimensions",
    "CaBathTubSection",
    "CaVoidedSlabDimensions",
    "CaVoidedSlabSection",
]
