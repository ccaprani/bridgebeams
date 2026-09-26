"""SEPSA "Muro/Losa TT" double-tee units (ligera, pesada, americana).

Source: Grupo Constructor SEPSA, *Catálogo de piezas SEPSA V-05 27-21*,
PDF page 19. The catalogue lists bridge use first ("trabes para puentes
vehiculares y peatonales") but the product is multi-purpose (floors, walls,
reinforced-earth facing). Drawings are in centimetres; this module returns
millimetres with origin at mid-soffit and y upwards. The soffit between
the stems is open, so the section is a single ring.

Every dimension is printed: 5 cm flange, 45° haunches (7.5 × 7.5 cm for
ligera, 8 × 8 cm for pesada and americana), stem top width 16 / 24.4 / 25 cm,
stem axes 150 / 150 / 122 cm apart, and the stem bottom width ``b`` per
depth from the area tables. Flange width ``a`` is a table variable; the
flange is trimmed symmetrically (each 10 cm of ``a`` changes the tabulated
area by exactly 50 cm², i.e. the 5 cm flange). Areas for every h × a cell
validate the outline; there are no published inertia values.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon, box
from shapely.geometry.polygon import orient

from bridgebeams._geometry import geometry_from_polygon


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.mx")
        .joinpath("data/sepsa_double_tees.json")
        .read_text(encoding="utf-8")
    )


@dataclass(frozen=True)
class SepsaDoubleTeeDimensions:
    """Dimensions in millimetres."""

    variant: str
    depth: float
    flange_width: float
    flange_thickness: float
    stem_spacing: float
    stem_top_width: float
    stem_bottom_width: float
    haunch_width: float
    haunch_depth: float

    @property
    def right_half(self) -> list[tuple[float, float]]:
        """From the flange soffit centreline round the right stem to the top."""
        h, tf = self.depth, self.flange_thickness
        xs = self.stem_spacing / 2
        st, sb = self.stem_top_width / 2, self.stem_bottom_width / 2
        hx, hy = self.haunch_width, self.haunch_depth
        y_f = h - tf
        return [
            (0.0, y_f),
            (xs - st - hx, y_f),
            (xs - st, y_f - hy),
            (xs - sb, 0.0),
            (xs + sb, 0.0),
            (xs + st, y_f - hy),
            (xs + st + hx, y_f),
            (self.flange_width / 2, y_f),
            (self.flange_width / 2, h),
        ]


class SepsaDoubleTeeSection:
    """One SEPSA double tee; size is ``"<VARIANT>-<h in cm>"``.

    ``a`` (mm) is the flange width, default 3000 mm, restricted to the
    tabulated range of the variant.

    >>> from bridgebeams.mx import SepsaDoubleTeeSection
    >>> SepsaDoubleTeeSection("PESADA-85").dimensions.stem_bottom_width
    160.0
    """

    SIZES = tuple(
        [f"LIGERA-{h}" for h in (85, 80, 75, 70, 65, 60, 55, 50, 45)]
        + [f"PESADA-{h}" for h in (85, 80, 75, 70, 65, 60, 55, 50, 45)]
        + [f"AMERICANA-{h}" for h in (81, 75, 70, 65, 60, 55, 50, 45)]
    )

    def __init__(self, size: str = "PESADA-85", a: float = 3000.0):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        variant_name, h = size.rsplit("-", 1)
        var = next(v for v in data["variants"] if v["variant"] == variant_name)
        row = next(r for r in var["rows"] if r["h_cm"] == float(h))
        a_cm = float(a) / 10.0
        if not var["a_min_cm"] <= a_cm <= var["a_max_cm"]:
            raise ValueError(
                f"a must be within {10 * var['a_min_cm']:.0f}–{10 * var['a_max_cm']:.0f} mm"
            )
        self.size = size
        self.a = float(a)
        self.published = row
        self.provenance = var["provenance"]
        self.source_status = data["source_status"]
        self.dimensions = SepsaDoubleTeeDimensions(
            variant=variant_name,
            depth=10.0 * row["h_cm"],
            flange_width=float(a),
            flange_thickness=10.0 * var["flange_thickness_cm"],
            stem_spacing=10.0 * var["stem_spacing_cm"],
            stem_top_width=10.0 * var["stem_top_width_cm"],
            stem_bottom_width=10.0 * row["b_cm"],
            haunch_width=10.0 * var["haunch_width_cm"],
            haunch_depth=10.0 * var["haunch_depth_cm"],
        )

    @property
    def polygon(self) -> Polygon:
        d = self.dimensions
        r = d.right_half
        poly = Polygon(r[1:] + [(-x, y) for x, y in reversed(r[1:])])
        half = d.flange_width / 2
        if half < d.stem_spacing / 2 + d.stem_top_width / 2 + d.haunch_width:
            # Pesada at a=190 cm: haunch foot (95.2 cm) overhangs the 95 cm edge;
            # trim to the flange edge (2 mm sliver).
            poly = poly.intersection(box(-half, 0.0, half, d.depth))
        return orient(poly, sign=1.0)

    @property
    def geometry(self):
        """The gross section as a sectionproperties Geometry, in millimetres."""
        return geometry_from_polygon(self.polygon)


__all__ = ["SepsaDoubleTeeDimensions", "SepsaDoubleTeeSection"]
