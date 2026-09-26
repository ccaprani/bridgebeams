"""Prethor (Grupo Puentes, Spain) precast bridge beams from the "Dossier Prethor 2020".

Families (PDF pages, 1-based): Vigas "doble T" VI 60-140, VI 145-245 serie I
and VI 150-250 serie II (p59); Vigas Artesa VA-100 ... VA-260 (p61); Vigas U
VUP / VUG 100-200 (p63, repeated p64); Vigas Cajon VCP 80/220, VCP 100/200
(p66), VCG 80/220, VCG 100/200 (p67); Vigas Asimetricas Adosadas VAA 180/260,
two variants (p70).

The dossier prints only the overall envelope (H, top width ``a``, bottom
width) and the theoretical self-weight P (t/m) per size. The silhouettes are
embedded raster images drawn to scale (checked: printed widths and the drawn
depth agree within about 1 %), so every thickness, chamfer and haunch was
scaled from them (``provenance = "estimate"``). Where the scaled outline gave
a systematic mass error, one family-wide bottom-slab thickness was fitted to
the P table (``"fitted-reconstruction"``). See ``data/r2_prethor.json``.

Millimetres, origin at mid-soffit, y upwards. For the asymmetric VAA beams the
x origin is the middle of the 3.00 m soffit; the vertical outer web is on the
left (x = -1500) and the 1:4 sloping outer web on the right. The "Cajon" and
"U" beams are open-topped troughs as drawn (the deck slab closes them), so
they have no interior ring.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from importlib import resources

from shapely.geometry import Polygon
from shapely.geometry.polygon import orient

from bridgebeams._geometry import geometry_from_polygon
from bridgebeams.hu._fillet import fillet_polyline


@lru_cache(maxsize=1)
def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.es").joinpath("data/r2_prethor.json").read_text(encoding="utf-8")
    )


def _outline_mm(family: dict, depth_cm: float) -> list[tuple[float, float]]:
    """Resolve anchored cm vertices of ``family`` at depth H and return mm points.

    Vertex anchors: ``"b"`` fixed from the soffit; ``"t"`` y measured from the
    top (y + H); ``"ts"`` as ``"t"`` and also shifted outwards by
    ``slope * H`` (points riding on a 1:4 sloping outer web).
    """
    slope = family["web_slope"]
    pts = []
    for v in family["outline_cm"]:
        x, y, anchor = v[0], v[1], v[2]
        radius = v[3] if len(v) > 3 else 0.0
        if anchor == "t":
            y = depth_cm + y
        elif anchor == "ts":
            x, y = x + slope * depth_cm, depth_cm + y
        pts.append((x * 10.0, y * 10.0, radius * 10.0))
    if any(p[2] for p in pts):
        line = fillet_polyline(pts)
    else:
        line = [(p[0], p[1]) for p in pts]
    if family["symmetric"]:
        # right half from (0, 0) round to the centreline; mirror to the left
        return line + [(-x, y) for x, y in reversed(line) if x != 0.0]
    return line


@dataclass(frozen=True)
class PrethorBeamDimensions:
    """Printed envelope (mm) plus the resolved outline (mm, mid-soffit origin)."""

    family: str
    depth: float
    top_width: float
    bottom_width: float
    outline: tuple[tuple[float, float], ...]


class _PrethorSection:
    FAMILIES: tuple[str, ...] = ()
    SIZES: tuple[str, ...] = ()
    source_status = "producer catalogue (Dossier Prethor 2020)"

    def __init__(self, size: str):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        row = data["sizes"][size]
        fam = data["families"][row["family"]]
        self.size = size
        self.family = row["family"]
        self.published = {"P_t_per_m": row["P_t_per_m"], "H_cm": row["H_cm"], "a_cm": row.get("a_cm")}
        self.provenance = row["provenance"]
        self.density_t_m3 = data["density_t_m3"]
        outline = tuple(_outline_mm(fam, row["H_cm"]))
        self.dimensions = PrethorBeamDimensions(
            family=row["family"],
            depth=row["H_cm"] * 10.0,
            top_width=row["top_width_cm"] * 10.0,
            bottom_width=fam["bottom_width_cm"] * 10.0,
            outline=outline,
        )

    @property
    def polygon(self) -> Polygon:
        return orient(Polygon(self.dimensions.outline), 1.0)

    @property
    def geometry(self):
        return geometry_from_polygon(self.polygon)


def _sizes(*families: str) -> tuple[str, ...]:
    data = _load_data()
    return tuple(s for s, r in data["sizes"].items() if r["family"] in families)


class PrethorViSection(_PrethorSection):
    """Vigas "doble T": VI 60-140 (66/66), VI 145-245 serie I (110/80), VI 150-250 serie II (170/80)."""

    FAMILIES = ("VI", "VI-I", "VI-II")
    SIZES = _sizes(*FAMILIES)

    def __init__(self, size: str = "VI-I-185"):
        super().__init__(size)


class PrethorVaSection(_PrethorSection):
    """Vigas Artesa VA-100 ... VA-260 (open trough with outward top flanges, 1.72 m soffit)."""

    FAMILIES = ("VA",)
    SIZES = _sizes(*FAMILIES)

    def __init__(self, size: str = "VA-180"):
        super().__init__(size)


class PrethorVuSection(_PrethorSection):
    """Vigas U: VUP (1.98 m soffit) and VUG (2.63 m soffit), H 100-200, open trough."""

    FAMILIES = ("VUP", "VUG")
    SIZES = _sizes(*FAMILIES)

    def __init__(self, size: str = "VUP-160"):
        super().__init__(size)


class PrethorVcSection(_PrethorSection):
    """Vigas Cajon VCP (3.30 m soffit) and VCG (3.96 m soffit), 80/220 (lipped) and 100/200 (thick-top) series."""

    FAMILIES = ("VCP80/220", "VCP100/200", "VCG80/220", "VCG100/200")
    SIZES = _sizes(*FAMILIES)

    def __init__(self, size: str = "VCP100/200-160"):
        super().__init__(size)


class PrethorVaaSection(_PrethorSection):
    """Vigas Asimetricas Adosadas VAA 180/260, variant A (lipped tops) and B (rounded haunches)."""

    FAMILIES = ("VAA-A", "VAA-B")
    SIZES = _sizes(*FAMILIES)

    def __init__(self, size: str = "VAA-A-220"):
        super().__init__(size)


__all__ = [
    "PrethorBeamDimensions",
    "PrethorViSection",
    "PrethorVaSection",
    "PrethorVuSection",
    "PrethorVcSection",
    "PrethorVaaSection",
]
