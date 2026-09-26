"""DNIT IPR-751 semipermanent-bridge precast I longarinas PCP-10/15/20.

Source: DNIT/IPR, *Publicação IPR-751 — Álbum de projetos-tipo de pontes
semipermanentes*, Volume 1 — Desenhos, 2ª edição (Brasília, 2023), sheets
"PCP-10/15/20 – Longarina pré-moldada L01 = L02", Corte D-D (folhas 46, 55,
66; PDF pp 56, 65, 76; identical in the 2022 1st edition). Section
properties of the precast beam alone ("1ª etapa") are published in Volume 2
— Memória de cálculo, 2ª edição 2023, Tabela 2-5 (folhas 140–142).

Federal standard (Brazil) one-lane semipermanent bridges of 10, 15 and
20 m modules. Drawing units are centimetres; this module returns
millimetres, origin mid-soffit, y up. All dimensions of the plain
polygonal I are printed; the midspan section is modelled (solid end blocks
excluded). Volume 2 Tabela 2-1 labels PCP-10/15 "concreto armado
pré-moldado" and PCP-20 "protendido", while Volume 1 includes an
"armadura ativa" sheet for every module; the class is agnostic.
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
        resources.files("bridgebeams.br")
        .joinpath("data/dnit_pcp_longarinas.json")
        .read_text(encoding="utf-8")
    )


@dataclass(frozen=True)
class DnitPcpLongarinaDimensions:
    """Printed Corte D-D dimensions, millimetres (equal top/bottom widths)."""

    depth: float
    flange_width: float
    web_width: float
    top_flange: float
    top_taper: float
    bottom_flange: float
    bottom_taper: float

    @property
    def web_height(self) -> float:
        return self.depth - (
            self.top_flange + self.top_taper + self.bottom_flange + self.bottom_taper
        )

    @property
    def outline(self) -> list[tuple[float, float]]:
        xf, xw, D = self.flange_width / 2, self.web_width / 2, self.depth
        right = [
            (xf, 0.0),
            (xf, self.bottom_flange),
            (xw, self.bottom_flange + self.bottom_taper),
            (xw, D - self.top_flange - self.top_taper),
            (xf, D - self.top_flange),
            (xf, D),
        ]
        return right + [(-x, y) for x, y in reversed(right)]


class DnitPcpLongarinaSection:
    """DNIT PCP-10, PCP-15 or PCP-20 precast I longarina (midspan).

    >>> DnitPcpLongarinaSection("PCP-20").polygon.bounds
    (-300.0, 0.0, 300.0, 1300.0)
    """

    SIZES = ("PCP-10", "PCP-15", "PCP-20")

    def __init__(self, size: str = "PCP-20"):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        row = data["types"][size]
        self.size = size
        self.published = row
        self.provenance = row["provenance"]
        self.source_status = data["source_status"]
        self.dimensions = DnitPcpLongarinaDimensions(
            **{k: 10.0 * float(v) for k, v in row["dimensions_cm"].items()}
        )

    @property
    def polygon(self) -> Polygon:
        return orient(Polygon(self.dimensions.outline), sign=1.0)

    @property
    def geometry(self):
        """A ``sectionproperties`` Geometry in millimetres."""
        return geometry_from_polygon(self.polygon)


__all__ = ["DnitPcpLongarinaDimensions", "DnitPcpLongarinaSection"]
