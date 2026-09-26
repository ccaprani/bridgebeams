"""Paver (Italy) precast bridge beams scaled from catalogue sketches (estimates).

Sources: Paver Via "Tipologie travi da ponte" (2021) and the separate UHP 250,
HTP and HP 125 sheets (paver.it, 2024 uploads). Only depth H and the overall
widths B/C are printed; outlines are scaled from the to-scale grey sketches, so
every size is ``provenance = "estimate"`` (see data/paver.json).
Families: VHP (V trough), UHP (U trough with bottom wings), HP100 (I),
HTP (T at C = 150 cm), IHP (adjacent I), THP (adjacent inverted T).
Millimetres, origin at mid-soffit, y upwards.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon

from bridgebeams._geometry import geometry_from_polygon


def _load_data() -> dict:
    return json.loads(resources.files("bridgebeams.it").joinpath("data/paver.json").read_text(encoding="utf-8"))




def _outer_web_x(y: float, y0: float) -> float:
    return 522.0 + 0.1532 * (y - y0)


def _inner_web_x(y: float) -> float:
    return 375.0 + 0.1488 * (y - 289.0)


def _flange(h: float, y0: float) -> list[tuple[float, float]]:
    yw = h - 202.0
    xw = _outer_web_x(yw, y0)
    # haunch y = yw + 0.515 (x - xw) meets underside y = h - 81 + 0.049 (x - 938)
    xh = ((h - 81.0 - 0.049 * 938.0) - (yw - 0.515 * xw)) / (0.515 - 0.049)
    yh = yw + 0.515 * (xh - xw)
    return [(xw, yw), (xh, yh), (1243.0, h - 66.0), (1250.0, h - 59.0), (1250.0, h)]


def _inner(h: float) -> list[tuple[float, float]]:
    return [(_inner_web_x(h), h), (375.0, 289.0), (320.0, 238.0), (0.0, 214.0)]


def _half_profile(family: str, h: float, c: float | None = None) -> list[tuple[float, float]]:
    if family == "VHP":
        return [(487.0, 0.0), (522.0, 271.0), *_flange(h, 271.0), *_inner(h)]
    if family == "UHP":
        bottom = [(1250.0, 0.0), (1250.0, 84.0), (599.0, 172.0), (544.0, 234.0), (522.0, 253.0)]
        if h <= 600.0:  # UHP60: no top flange, top width C = 1144
            return [*bottom, (c / 2, h), *_inner(h)]
        return [*bottom, *_flange(h, 253.0), *_inner(h)]
    if family == "HP":
        return [(595.0, 0.0), (625.0, 40.0), (625.0, 155.0), (185.0, 185.0), (75.0, 240.0),
                (75.0, h - 185.0), (180.0, h - 140.0), (625.0, h - 85.0), (625.0, h)]
    if family == "HTP":
        return [(285.0, 0.0), (300.0, 15.0), (300.0, h - 90.0), (c / 2, h - 78.0), (c / 2, h)]
    if family == "IHP":
        return [(300.0, 0.0), (300.0, 135.0), (135.0, 170.0), (100.0, 205.0),
                (100.0, h - 170.0), (135.0, h - 125.0), (300.0, h - 90.0), (300.0, h)]
    if family == "THP":
        return [(300.0, 0.0), (300.0, 205.0), (280.0, 217.0), (135.0, 242.0), (90.0, 275.0), (90.0, h)]
    raise ValueError(family)


@dataclass(frozen=True)
class PaverBeamDimensions:
    """Printed H, B and C (mm); the outline details are family conventions (estimates)."""

    family: str
    depth: float
    bottom_width: float
    top_width: float

    @property
    def half_profile(self) -> list[tuple[float, float]]:
        return _half_profile(self.family, self.depth, self.top_width)


_FAMILY = {"UHP": "UHP", "VHP": "VHP", "HP1": "HP", "HTP": "HTP", "IHP": "IHP", "THP": "THP"}


class PaverBeamSection:
    """Paver VHP, UHP, HP100, HTP (C = 150), IHP65-90 and THP40-60 gross sections."""

    SIZES = ("VHP170", "VHP160", "VHP140", "VHP120", "VHP100", "VHP80",
             "UHP170", "UHP160", "UHP140", "UHP120", "UHP100", "UHP80", "UHP60",
             "HP100", "HTP60", "HTP50", "HTP40",
             "IHP90", "IHP85", "IHP80", "IHP75", "IHP70", "IHP65",
             "THP60", "THP55", "THP50", "THP45", "THP40")
    source_status = "producer catalogue (2021/2024)"

    def __init__(self, size: str = "UHP120"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        family = _FAMILY[size[:3]]
        table = data["tables"][family]
        row = table[size]
        self.size = size
        self.family = family
        self.published = dict(zip(table["_columns"].split(" cm")[0].split(", "), row))
        self.provenance = data["provenance"]
        h, b = row[0] * 10.0, row[1] * 10.0
        if family == "VHP":
            b, c = 974.0, 2500.0
        elif family == "UHP":
            c = 1144.0 if size == "UHP60" else row[2] * 10.0
        elif family == "THP":
            c = row[2] * 10.0
        else:
            c = row[2] * 10.0
        self.dimensions = PaverBeamDimensions(family, h, b, c)

    @property
    def polygon(self) -> Polygon:
        right = [p for p in self.dimensions.half_profile if p[0] > 0]
        return Polygon(right + [(-x, y) for x, y in reversed(right)])

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = ["PaverBeamDimensions", "PaverBeamSection"]
