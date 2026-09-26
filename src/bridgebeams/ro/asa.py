"""ASA CONS România (Consolis) precast road-bridge girders ("Grindă pod").

Source: ASA CONS Consolis product catalogue, PDF pages 97 (Grindă pod 42,
52), 99 (72, 80) and 101 (95, 105). Drawing dimensions are centimetres
(superscripts are decimals: 8^2 = 8.2 cm) and are converted to mm here.
See ``data/asa_grinda_pod.json`` for the transcription and conventions.

Conventions (all recorded per size in the JSON):

* Fillets use the printed radius exactly, constructed tangent to the
  printed straight faces. The printed fillet-extent chains (e.g. 4 / 4.8
  cm on 72/80) are then met within about 2 mm (5 mm for the 95/105 top
  fillets, measured to the theoretical knee), because they were rounded on a sloping flange.
* 42: the 14 cm callout is the theoretical intersection of the tapered
  stem faces with the lower-flange slope; the R5 fillet is inscribed there.
* 52: the stem width is not printed; 14 cm is copied from 42 (the drawing
  scales about 12.6-13 cm) -> ``estimate``.
* 95/105: the first vertical label (10 / 12 cm) is the flange-edge
  thickness plus a further 2 cm taper; only this reading closes the chain
  to 95 / 105 cm (the drawings are drawn about 2 cm shallower).
* 105: the lower-flange slope is undimensioned; 45 degrees is assumed
  (drawing about 46 degrees) -> ``estimate``.

Millimetres, origin at mid-soffit, y upwards; no end blocks or ducts.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from functools import lru_cache
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon, polygon_from_half_profile

from ._arc import fillet


@lru_cache(maxsize=None)
def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.ro").joinpath("data/asa_grinda_pod.json").read_text(encoding="utf-8")
    )


def _line_y(p, q, x):
    return p[1] + (q[1] - p[1]) * (x - p[0]) / (q[0] - p[0])


def _tangent_from_point(p, centre, radius):
    """Tangent point on a circle from external point ``p`` (the lower-left one)."""
    dx, dy = centre[0] - p[0], centre[1] - p[1]
    d = math.hypot(dx, dy)
    ang = math.atan2(dy, dx) + math.asin(radius / d)
    length = math.sqrt(d * d - radius * radius)
    return (p[0] + length * math.cos(ang), p[1] + length * math.sin(ang))


def _arc(centre, radius, start, end, segments=24):
    a0 = math.atan2(start[1] - centre[1], start[0] - centre[0])
    a1 = math.atan2(end[1] - centre[1], end[0] - centre[0])
    sweep = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
    return [
        (centre[0] + radius * math.cos(a0 + sweep * i / segments),
         centre[1] + radius * math.sin(a0 + sweep * i / segments))
        for i in range(segments + 1)
    ]


@dataclass(frozen=True)
class AsaGrindaPodDimensions:
    """Transcribed dimensions (mm) of one ASA "Grindă pod" girder."""

    mark: str
    depth: float
    shape: str  # "inverted-T" (42/52), "I-sloped" (72/80), "I-bulb" (95/105)
    params: tuple  # sorted (name, value) pairs from the JSON

    def __getitem__(self, key):
        return dict(self.params)[key]

    @property
    def outline(self) -> list[tuple[float, float]]:
        p = dict(self.params)
        H = self.depth
        if self.shape == "inverted-T":
            corner = (p["throat_width"] / 2, p["throat_level"])
            edge = (p["bottom_width"] / 2, p["flange_edge_level"])
            taper_top = (p["top_width"] / 2, p["taper_top_level"])
            return [
                (p["soffit_width"] / 2, 0.0),
                (p["bottom_width"] / 2 - p["side_offset"], p["chamfer"]),
                edge,
                *fillet(corner, edge, taper_top, p["radius"]),
                taper_top,
                (p["top_width"] / 2, H),
            ]
        xw = p["web_width"] / 2
        if self.shape == "I-sloped":
            edge = (p["bottom_width"] / 2, p["flange_edge_level"])
            centre = (xw + p["radius"], p["web_lower_tangent"])
            t_low = _tangent_from_point(edge, centre, p["radius"])
            lower = [edge, *_arc(centre, p["radius"], t_low, (xw, centre[1]))]
            bottom = [(p["soffit_width"] / 2, 0.0),
                      (p["bottom_width"] / 2 - p["side_offset"], p["chamfer"])]
        else:  # I-bulb
            edge = (p["bottom_width_at_edge"] / 2, p["flange_edge_level"])
            run, rise = p["lower_slope_run"], p["lower_slope_rise"]
            s = (edge[0] - xw) / run
            corner = (xw, edge[1] + rise * s)
            lower = [edge, *fillet(corner, edge, (xw, H), p["lower_radius"])]
            bottom = [(p["soffit_width"] / 2, 0.0)]
        top_edge = (p["top_width"] / 2, H - p["top_edge"])
        knee = (xw + p["top_slope_run"], H - p["top_edge"] - p["top_slope_drop"])
        corner = (xw, _line_y(top_edge, knee, xw))
        upper = fillet(corner, (xw, 0.0), top_edge, p["upper_radius"])
        return bottom + lower + upper + [top_edge, (p["top_width"] / 2, H)]


class AsaGrindaPodSection:
    """ASA CONS "Grindă pod" 42, 52, 72, 80, 95 and 105 bridge girders."""

    SIZES = ("42", "52", "72", "80", "95", "105")
    source_status = "producer catalogue (ASA CONS Consolis, 2025)"

    def __init__(self, size: str = "72"):
        size = str(size)
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        row = next(r for r in _load_data()["sections"] if r["mark"] == size)
        self.size = size
        self.name = row["name_original"]
        self.record = row
        self.provenance = row["provenance"]
        params = tuple(sorted((k, float(v) * 10.0) for k, v in row["model_parameters_cm"].items()))
        self.dimensions = AsaGrindaPodDimensions(size, float(row["depth_cm"]) * 10.0, row["shape"], params)

    @property
    def polygon(self) -> Polygon:
        return polygon_from_half_profile(self.dimensions.outline)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = ["AsaGrindaPodDimensions", "AsaGrindaPodSection"]
