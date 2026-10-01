"""Chilean MOP standard single-span deck beams, Manual de Carreteras Vol. 4 §4.604.

Source: MOP – DGOP – Dirección de Vialidad, *Manual de Carreteras, Volumen
Nº 4 — Planos de Obras Tipo*, Edición 2018, Sección 4.604 "Tableros de un
Tramo, 11 m ≤ L ≤ 15 m":

* ``MopVigaPostensadaSection`` — "Tablero con Viga de Hormigón Postensado
  de un Tramo", lámina 4.604.203 "Geometría y Cables Viga Postensada"
  (Noviembre 2000; PDF p372), Corte C-C and the "Viga Postensada —
  Geometría (cm)" table (h4, e, a1, a2 per span L and calzada). Depth 80 cm.
  Lámina 4.604.201 (Marzo 2015) allows substitution by factory
  pretensioned beams.
* ``MopLosaNervadaVigaSection`` — "Tablero Losa Nervada de Hormigón Armado
  de un Tramo", lámina 4.604.001 (Marzo 2015; PDF p363) "Sección Viga":
  precast RC trapezoidal rib 25/20 x 70 cm; volumes on lámina 4.604.003.

Drawing units are centimetres; this module returns millimetres, origin
mid-soffit, y up. The deck crossfall p% on the post-tensioned beam's top
face is not modelled (top horizontal at the 80 cm axis depth).
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
        resources.files("bridgebeams.cl")
        .joinpath("data/mop_mc_v4_4604.json")
        .read_text(encoding="utf-8")
    )


@dataclass(frozen=True)
class MopVigaPostensadaDimensions:
    """Corte C-C dimensions in millimetres (symbols as on lámina 4.604.203)."""

    a1: float  # top flange width
    a2: float  # bottom bulb width
    e: float  # web width
    h4: float  # vertical side of the bottom bulb
    depth: float = 800.0
    top_flange: float = 150.0
    top_fillet: float = 50.0  # 5 x 5 cm 45 degree fillet flange-to-web
    bottom_taper: float = 100.0
    chamfer: float = 25.0  # "tip. 2,5" soffit chamfers

    @property
    def web_height(self) -> float:
        return self.depth - self.top_flange - self.top_fillet - self.bottom_taper - self.h4

    @property
    def outline(self) -> list[tuple[float, float]]:
        xa1, xa2, xe, D = self.a1 / 2, self.a2 / 2, self.e / 2, self.depth
        c = self.chamfer
        right = [
            (xa2 - c, 0.0),
            (xa2, c),
            (xa2, self.h4),
            (xe, self.h4 + self.bottom_taper),
            (xe, D - self.top_flange - self.top_fillet),
            (xe + self.top_fillet, D - self.top_flange),
            (xa1, D - self.top_flange),
            (xa1, D),
        ]
        return right + [(-x, y) for x, y in reversed(right)]


class MopVigaPostensadaSection:
    """MOP 4.604.203 viga postensada (midspan Corte C-C), 80 cm deep.

    Sizes are ``C8-L11`` ... ``C10-L15`` (calzada 8,0 m con pasillo / 10,0 m
    sin pasillo, span L in m). Only geometrically distinct outlines are in
    ``SIZES``; ``C10-L12`` and ``C10-L13`` are accepted as aliases of
    ``C8-L11`` and ``C8-L12``.

    >>> MopVigaPostensadaSection("C8-L15").polygon.bounds
    (-475.0, 0.0, 475.0, 800.0)
    """

    SIZES = ("C8-L11", "C8-L12", "C8-L13", "C8-L14", "C8-L15",
             "C10-L11", "C10-L14", "C10-L15")
    ALIASES = {"C10-L12": "C8-L11", "C10-L13": "C8-L12"}

    def __init__(self, size: str = "C8-L15"):
        if size not in self.SIZES and size not in self.ALIASES:
            raise ValueError(
                f"size must be one of {self.SIZES + tuple(self.ALIASES)}, got {size!r}"
            )
        data = _load_data()["viga_postensada"]
        row = data["table_rows"][size]
        self.size = size
        self.canonical_size = self.ALIASES.get(size, size)
        self.published = row
        self.provenance = data["provenance"]
        self.source_status = data["source_status"]
        self.dimensions = MopVigaPostensadaDimensions(
            **{k: 10.0 * float(row[k]) for k in ("a1", "a2", "e", "h4")}
        )

    @property
    def polygon(self) -> Polygon:
        return orient(Polygon(self.dimensions.outline), sign=1.0)

    @property
    def geometry(self):
        """A ``sectionproperties`` Geometry in millimetres."""
        return geometry_from_polygon(self.polygon)


@dataclass(frozen=True)
class MopLosaNervadaVigaDimensions:
    """Trapezoidal rib, millimetres."""

    depth: float
    top_width: float
    bottom_width: float

    @property
    def outline(self) -> list[tuple[float, float]]:
        b, t, D = self.bottom_width / 2, self.top_width / 2, self.depth
        return [(-b, 0.0), (b, 0.0), (t, D), (-t, D)]


class MopLosaNervadaVigaSection:
    """MOP 4.604.001 losa nervada precast RC rib ("Sección Viga"), 25/20 x 70 cm.

    >>> MopLosaNervadaVigaSection().polygon.bounds
    (-125.0, 0.0, 125.0, 700.0)
    """

    SIZES = ("V25/20x70",)

    def __init__(self, size: str = "V25/20x70"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()["losa_nervada"]
        self.size = size
        self.published = data["published"]
        self.provenance = data["provenance"]
        self.source_status = data["source_status"]
        self.dimensions = MopLosaNervadaVigaDimensions(
            **{k: 10.0 * float(v) for k, v in data["dimensions_cm"].items()}
        )

    @property
    def polygon(self) -> Polygon:
        return orient(Polygon(self.dimensions.outline), sign=1.0)

    @property
    def geometry(self):
        """A ``sectionproperties`` Geometry in millimetres."""
        return geometry_from_polygon(self.polygon)


__all__ = [
    "MopLosaNervadaVigaDimensions",
    "MopLosaNervadaVigaSection",
    "MopVigaPostensadaDimensions",
    "MopVigaPostensadaSection",
]
