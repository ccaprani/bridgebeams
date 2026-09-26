"""Mexican producer "trabes tipo AASHTO": Prefabricados Dragón and Tubeco.

Two independent Mexican producer documents (round-2 retrieval, 2026-09-23):

* Prefabricados Dragón, *Ficha técnica — Trabes tipo AASHTO* (single page):
  Tipo I–VI drawn in metres. Every vertical chain and the top, web and bottom
  widths are printed. Types V and VI show a two-stage top-flange taper
  (0.08 then 0.10 m) whose horizontal break point is not printed.
* Tubeco, *Elementos presforzados* brochure, PDF p7 (printed p6): Tipo III,
  IV, V and VI drawn in centimetres, including the V/VI break points
  (34 + 9.5 + 20 + 9.5 + 34) and a 2 cm soffit chamfer.

These are Mexican producer profiles in their own right. Their Roman type
names follow the AASHTO/PCI family, but the geometry is taken only from the
Mexican documents (e.g. Dragón's Tipo V/VI webs are drawn and dimensioned
0.26 m, Tubeco's 20 cm). They are not aliases of ``us.AashtoIBeamSection``.

Origin at mid-soffit, y up, millimetres. Neither document publishes
section properties, so tests are analytic self-checks only. Conventions and
source typos are listed in ``data/r2_producer_aashto.json``.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon
from shapely.geometry.polygon import orient

from bridgebeams._geometry import geometry_from_polygon


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.mx")
        .joinpath("data/r2_producer_aashto.json")
        .read_text(encoding="utf-8")
    )


@dataclass(frozen=True)
class R2AashtoIDimensions:
    """Plain polygonal I outline, millimetres.

    Heights are measured down from the top (top flange) or up from the
    soffit (bottom flange). ``top_knee_width`` is the width at the end of
    the outer top taper when a second (inner) taper of height
    ``top_inner_taper`` runs on to the web; with ``top_inner_taper == 0``
    the single top taper runs directly to the web.
    """

    depth: float
    top_width: float
    web_width: float
    bottom_width: float
    top_flange: float
    top_outer_taper: float
    bottom_flange: float
    bottom_taper: float
    top_inner_taper: float = 0.0
    top_knee_width: float = 0.0
    soffit_chamfer: float = 0.0

    @property
    def web_height(self) -> float:
        return self.depth - (
            self.top_flange
            + self.top_outer_taper
            + self.top_inner_taper
            + self.bottom_flange
            + self.bottom_taper
        )

    def right_half(self) -> list[tuple[float, float]]:
        D, c = self.depth, self.soffit_chamfer
        xb, xt, xw = self.bottom_width / 2, self.top_width / 2, self.web_width / 2
        pts = [(xb - c, 0.0), (xb, c)] if c else [(xb, 0.0)]
        pts += [
            (xb, self.bottom_flange),
            (xw, self.bottom_flange + self.bottom_taper),
            (xw, self.bottom_flange + self.bottom_taper + self.web_height),
        ]
        if self.top_inner_taper:
            pts.append((self.top_knee_width / 2, D - self.top_flange - self.top_outer_taper))
        pts += [(xt, D - self.top_flange), (xt, D)]
        return pts

    @property
    def outline(self) -> list[tuple[float, float]]:
        right = self.right_half()
        return right + [(-x, y) for x, y in reversed(right)]


class _ProducerAashtoBase:
    _producer: str = ""
    SIZES: tuple[str, ...] = ()

    def __init__(self, size: str):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()["producers"][self._producer]
        row = data["types"][size]
        scale = {"m": 1000.0, "cm": 10.0, "mm": 1.0}[data["units"]]
        self.size = size
        self.published = row
        self.provenance = row["provenance"]
        self.source_status = data["source_status"]
        self.dimensions = R2AashtoIDimensions(
            **{k: float(v) * scale for k, v in row["dimensions"].items()}
        )
        if self.dimensions.web_height <= 0:
            raise ValueError("non-positive web height")  # pragma: no cover

    @property
    def polygon(self) -> Polygon:
        return orient(Polygon(self.dimensions.outline), sign=1.0)

    @property
    def geometry(self):
        """A ``sectionproperties`` Geometry in millimetres."""
        return geometry_from_polygon(self.polygon)


class DragonAashtoSection(_ProducerAashtoBase):
    """Prefabricados Dragón (Mexico) trabe tipo AASHTO I–VI.

    >>> DragonAashtoSection("IV").dimensions.depth
    1350.0
    """

    _producer = "dragon"
    SIZES = ("I", "II", "III", "IV", "V", "VI")

    def __init__(self, size: str = "IV"):
        super().__init__(size)


class TubecoAashtoSection(_ProducerAashtoBase):
    """Tubeco (Mexico) trabe AASHTO tipo III–VI.

    >>> TubecoAashtoSection("VI").dimensions.top_width
    1070.0
    """

    _producer = "tubeco"
    SIZES = ("III", "IV", "V", "VI")

    def __init__(self, size: str = "IV"):
        super().__init__(size)


__all__ = ["DragonAashtoSection", "R2AashtoIDimensions", "TubecoAashtoSection"]
