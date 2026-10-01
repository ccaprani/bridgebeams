"""Iowa DOT standard pretensioned beams A-D and bulb tees BTB-BTE.

Source: Iowa DOT Bridges and Structures Bureau, LRFD Bridge Design Manual
5.4.1 (January 2025), Figures 5.4.1.1.1-1 (A to D) and 5.4.1.1.1-2 (BTB
to BTE), PDF page 3 / printed 5.4.1: 3,
https://iowadot.gov/media/4637/download?inline (retrieved from the
2025-05-22 Wayback snapshot; the live host returned HTTP 403).

* ``IaIBeamSection``: A, B, C, D (32/39/45/54 in). Every dimension printed;
  3/4 in soffit bevels as drawn. The printed A/yb/I exclude the bevels.
* ``IaBulbTeeSection``: BTB, BTC, BTD, BTE (36/45/54/63 in). Printed
  dimensions with R=8 in web fillets and R=2 in shoulder radii; the
  "3/4 in FILLET" at the soffit corners is taken as a 3/4 in radius
  (provenance ``transcribed-with-convention``).

Gross concrete only. Millimetres, origin at soffit centre, y upward.
"""

from __future__ import annotations

from dataclasses import dataclass

from bridgebeams._geometry import geometry_from_polygon
from bridgebeams.us.state_common import (
    INCH_TO_MM,
    ccw_polygon,
    filleted_path,
    load_json,
    mirror_half,
    to_mm,
)
from bridgebeams.us.state_mo_girders import tapered_i_half_in

DATA_FILE = "state_ia_beams.json"
ARC_SEGMENTS = 64


def bulb_tee_half_in(web_height: float, t: dict, n: int = ARC_SEGMENTS):
    """Right half (inches) of an Iowa BT beam."""
    bw, w, tw = t["bottom_width"] / 2, t["web_width"] / 2, t["top_width"] / 2
    y1 = t["bottom_edge"]
    y2 = y1 + t["bottom_taper"]
    y3 = y2 + web_height
    y4 = y3 + t["top_taper"]
    depth = y4 + t["top_edge"]
    pts = [(0.0, 0.0), (bw, 0.0), (bw, y1), (w, y2), (w, y3), (tw, y4), (tw, depth), (0.0, depth)]
    radii = {1: t["soffit_fillet_radius"], 2: t["bottom_flange_corner_radius"],
             3: t["web_fillet_radius"], 4: t["web_fillet_radius"]}
    return filleted_path(pts, radii, n)


@dataclass(frozen=True)
class IaBeamDimensions:
    """Principal dimensions in millimetres (``source_in`` in inches)."""

    size: str
    depth: float
    top_width: float
    web_width: float
    bottom_width: float
    source_in: dict


class IaIBeamSection:
    """Iowa DOT A, B, C and D pretensioned I beams."""

    SIZES = ("A", "B", "C", "D")

    def __init__(self, size: str = "C"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        row = load_json(DATA_FILE)["i_beams"][size]
        d = row["dimensions_in"]
        self.size = size
        self.row = row
        self.provenance = row["provenance"]
        self.source_status = row["source_status"]
        self.published = row["published_in"]
        self._half_in = tapered_i_half_in(d)
        self.dimensions = IaBeamDimensions(
            size=size, depth=self._half_in[-1][1] * INCH_TO_MM,
            top_width=d["top_width"] * INCH_TO_MM, web_width=d["web_width"] * INCH_TO_MM,
            bottom_width=d["bottom_width"] * INCH_TO_MM, source_in=dict(d),
        )

    @property
    def polygon(self):
        return ccw_polygon(to_mm(mirror_half(self._half_in)))

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


class IaBulbTeeSection:
    """Iowa DOT BTB, BTC, BTD and BTE bulb-tee beams."""

    SIZES = ("BTB", "BTC", "BTD", "BTE")

    def __init__(self, size: str = "BTC"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = load_json(DATA_FILE)
        row = data["bulb_tees"][size]
        t = data["bulb_tee_template_in"]
        self.size = size
        self.row = row
        self.provenance = row["provenance"]
        self.source_status = row["source_status"]
        self.published = row["published_in"]
        self._half_in = bulb_tee_half_in(row["web_height_in"], t)
        self.dimensions = IaBeamDimensions(
            size=size, depth=self._half_in[-1][1] * INCH_TO_MM,
            top_width=t["top_width"] * INCH_TO_MM, web_width=t["web_width"] * INCH_TO_MM,
            bottom_width=t["bottom_width"] * INCH_TO_MM,
            source_in={**t, "web_height": row["web_height_in"]},
        )

    @property
    def polygon(self):
        return ccw_polygon(to_mm(mirror_half(self._half_in)))

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = ["IaBeamDimensions", "IaIBeamSection", "IaBulbTeeSection", "bulb_tee_half_in"]
