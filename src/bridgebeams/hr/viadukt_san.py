"""Viadukt d.d. SAN 210/75, 210/115, 210/135 voided slab girders (Croatia).

Source: TVZ (Tehničko veleučilište u Zagrebu) teaching notes "2. Pločasti
gredni mostovi", Slika 2.5 "Tipski montažni nosači", which reproduces the
Viadukt type girders (see data/viadukt_san.json). Millimetres, origin at
mid-soffit, y upwards; voids are polygon interiors.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon
from shapely.geometry.polygon import orient

from bridgebeams._geometry import geometry_from_polygon


def _load_data() -> dict:
    return json.loads(resources.files("bridgebeams.hr").joinpath("data/viadukt_san.json").read_text(encoding="utf-8"))


@dataclass(frozen=True)
class ViaduktSanDimensions:
    """mm. Round voids when ``void_diameter`` is set, else one chamfered box void."""

    depth: float
    width: float = 2100.0
    top_slab: float = 150.0
    bottom_slab: float = 100.0
    webs: float = 150.0
    void_chamfer: float = 150.0
    void_diameter: float | None = None
    void_centres_x: tuple[float, ...] = ()
    void_centre_y: float = 0.0
    key_centre_below_top: float = 250.0
    key_height: float = 150.0
    key_depth: float = 30.0
    key_flank: float = 30.0

    @property
    def exterior(self) -> list[tuple[float, float]]:
        b, h = self.width / 2, self.depth
        yc, hk, d, f = h - self.key_centre_below_top, self.key_height / 2, self.key_depth, self.key_flank
        right = [(b, 0.0), (b, yc - hk), (b - d, yc - hk + f), (b - d, yc + hk - f), (b, yc + hk), (b, h)]
        return right + [(-x, y) for x, y in reversed(right)]

    @property
    def voids(self) -> list[list[tuple[float, float]]]:
        if self.void_diameter is not None:
            r, n = self.void_diameter / 2, 64
            return [[(cx + r * math.cos(2 * math.pi * k / n), self.void_centre_y + r * math.sin(2 * math.pi * k / n))
                     for k in range(n)] for cx in self.void_centres_x]
        w, c = self.width / 2 - self.webs, self.void_chamfer
        y0, y1 = self.bottom_slab, self.depth - self.top_slab
        return [[(w - c, y0), (w, y0 + c), (w, y1 - c), (w - c, y1),
                 (-(w - c), y1), (-w, y1 - c), (-w, y0 + c), (-(w - c), y0)]]


class ViaduktSanSection:
    """SAN girder ``SAN 210/75``, ``SAN 210/115`` or ``SAN 210/135``."""

    SIZES = ("SAN 210/75", "SAN 210/115", "SAN 210/135")

    def __init__(self, size: str = "SAN 210/115"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        pr = data["printed"][size]
        est = data["estimates_cm"][size]
        key = data["estimates_cm"]["all"]["shear_key"]
        self.size = size
        self.published = pr
        self.provenance = data["provenance"][size]
        self.source_status = data["source_status"]
        cm = 10.0
        kw = dict(depth=pr["H"] * cm, width=pr["width"] * cm,
                  key_centre_below_top=key["centre_below_top"] * cm, key_height=key["height"] * cm,
                  key_depth=key["depth"] * cm, key_flank=key["flank"] * cm)
        if "void_diameter" in est:
            kw.update(void_diameter=est["void_diameter"] * cm,
                      void_centres_x=tuple(x * cm for x in est["void_centres_x"]),
                      void_centre_y=est["void_centre_y"] * cm)
        else:
            kw.update(top_slab=pr["top_slab"] * cm, bottom_slab=pr["bottom_slab"] * cm, webs=pr["webs"] * cm,
                      void_chamfer=est["void_chamfer"] * cm)
        self.dimensions = ViaduktSanDimensions(**kw)

    @property
    def polygon(self) -> Polygon:
        d = self.dimensions
        return orient(Polygon(d.exterior, d.voids), 1.0)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


__all__ = ["ViaduktSanDimensions", "ViaduktSanSection"]
