"""SEPSA Trabe Cajón box girders (CA-85…CA-180, B-400) and their Type U stage.

Source: Grupo Constructor SEPSA, *Catálogo de piezas SEPSA V-05 27-21*,
PDF pages 6–9. Drawings are in centimetres; this module returns
millimetres with origin at mid-soffit and y upwards.

Two concrete profiles are offered per family:

* ``"<family>"`` – the closed box (sección cerrada) with its trapezoidal
  chamfered void.
* ``"<family>-U"`` – the first-stage open "Sección tipo U" (CA-135, CA-150,
  CA-180 and B-400 only). The top slab between the two flange stubs is cast
  later with the deck ("Espacio colado en 2da etapa") and is not part of
  this profile.

The wing (aleta) width ``a`` is a catalogue variable. The flange soffit is a
single fixed line: shortening ``a`` moves the tip inward along that line
(the catalogue tables keep ``b + b1`` constant). ``a`` defaults to the
maximum drawn width and may be any value in the published range.

Geometry is built from the printed dimensions plus stated conventions; see
``data/sepsa_box_girders.json`` ``geometry_notes``. In brief: void chamfers
are 45°, web thickness is measured normal to the web, fillets (R22/R20 at
the web–wing junction, R5 at the soffit corners) are exact tangent arcs, and
the undimensioned B-400 soffit radius (R40), the Type U inner bottom radius
(R27) and the B-400 Type U top chamfer line were measured from the
catalogue's uniform-scale vector drawing. The fillet-to-wing junction is
solved so that the wing soffit reaches ``b1`` at the fillet tangent point.
Published areas (all 103 closed/Type U rows) validate the result; there
are no published centroid or inertia values.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from importlib import resources

from shapely.geometry import Polygon
from shapely.geometry.polygon import orient

from bridgebeams._geometry import geometry_from_polygon

from ._arcs import fillet, intersect, offset_line, unit

ARC_SEGMENTS = 48


def _load_data() -> dict:
    return json.loads(
        resources.files("bridgebeams.mx")
        .joinpath("data/sepsa_box_girders.json")
        .read_text(encoding="utf-8")
    )


def _dedupe(points):
    out = []
    for p in points:
        if not out or math.hypot(p[0] - out[-1][0], p[1] - out[-1][1]) > 1e-9:
            out.append(p)
    if len(out) > 1 and math.hypot(out[0][0] - out[-1][0], out[0][1] - out[-1][1]) < 1e-9:
        out.pop()
    return out


def _mirror_ring(right):
    """Right half from (0, y0) round to (0, y1) -> closed symmetric ring."""
    left = [(-x, y) for x, y in reversed(right)]
    return _dedupe(list(right) + left)


@dataclass(frozen=True)
class SepsaBoxDimensions:
    """Printed family dimensions in centimetres (catalogue units).

    ``web_straight_height`` is the printed height from the soffit to the
    start of the upper fillet; it is reported for comparison and is not
    used to build the outline (the fillet solution gives it).
    """

    family: str
    depth: float
    wing_width: float
    wing_width_max: float
    wing_width_min: float
    tip_thickness_at_max: float
    wing_taper_rise_at_max: float
    upper_fillet_radius: float
    soffit_radius: float
    bottom_slab: float
    void_height: float
    void_top_width: float
    void_bottom_width: float
    void_top_chamfer: float
    void_bottom_chamfer: float
    web_thickness: float
    web_straight_height: float
    u_gap: float | None = None
    u_stub: float | None = None
    u_web_thickness: float | None = None
    u_bottom_slab: float | None = None
    u_inner_radius: float | None = None
    u_top_chamfer_sum: float | None = None
    u_bottom_chamfer: float | None = None


class SepsaBoxGirderSection:
    """SEPSA closed box or first-stage Type U girder.

    >>> from bridgebeams.mx import SepsaBoxGirderSection
    >>> s = SepsaBoxGirderSection("CA-85")
    >>> round(s.polygon.bounds[3])
    850
    >>> round(SepsaBoxGirderSection("CA-150-U", a=2000).polygon.bounds[2])
    1000
    """

    SIZES = (
        "CA-85",
        "CA-115",
        "CA-135",
        "CA-150",
        "CA-180",
        "B-400",
        "CA-135-U",
        "CA-150-U",
        "CA-180-U",
        "B-400-U",
    )

    def __init__(self, size: str = "CA-135", a: float | None = None):
        if size not in self.SIZES:
            raise ValueError(f"size must be one of {self.SIZES}, got {size!r}")
        data = _load_data()
        self.size = size
        self.is_u = size.endswith("-U")
        family = size[:-2] if self.is_u else size
        fam = next(f for f in data["families"] if f["family"] == family)
        self.family_data = fam
        a_cm = fam["wing_width_max_cm"] if a is None else float(a) / 10.0
        if not fam["wing_width_min_cm"] - 1e-9 <= a_cm <= fam["wing_width_max_cm"] + 1e-9:
            raise ValueError(
                f"a must be within {10 * fam['wing_width_min_cm']:.0f}–"
                f"{10 * fam['wing_width_max_cm']:.0f} mm for {family}"
            )
        u = fam.get("type_u") or {}
        if self.is_u and not u:
            raise ValueError(f"{family} has no Type U stage")
        self.dimensions = SepsaBoxDimensions(
            family=family,
            depth=fam["depth_cm"],
            wing_width=a_cm,
            wing_width_max=fam["wing_width_max_cm"],
            wing_width_min=fam["wing_width_min_cm"],
            tip_thickness_at_max=fam["b_at_max_cm"],
            wing_taper_rise_at_max=fam["b1_at_max_cm"],
            upper_fillet_radius=fam["upper_fillet_radius_cm"],
            soffit_radius=fam["soffit_radius_cm"],
            bottom_slab=fam["bottom_slab_cm"],
            void_height=fam["void_height_cm"],
            void_top_width=fam["void_top_width_cm"],
            void_bottom_width=fam["void_bottom_width_cm"],
            void_top_chamfer=fam["void_top_chamfer_cm"],
            void_bottom_chamfer=fam["void_bottom_chamfer_cm"],
            web_thickness=fam["web_thickness_cm"],
            web_straight_height=fam["web_straight_height_cm"],
            u_gap=u.get("gap_cm"),
            u_stub=u.get("stub_cm"),
            u_web_thickness=u.get("web_thickness_cm"),
            u_bottom_slab=u.get("bottom_slab_cm"),
            u_inner_radius=u.get("inner_bottom_radius_cm"),
            u_top_chamfer_sum=u.get("top_chamfer_line_x_plus_y_cm"),
            u_bottom_chamfer=u.get("bottom_chamfer_cm"),
        )
        self.a = 10.0 * a_cm
        key = "provenance_u" if self.is_u else "provenance"
        self.provenance = fam[key]
        self.source_status = data["source_status"]
        self._solve()

    # -- construction (centimetres) ---------------------------------------
    def _solve(self) -> None:
        d = self.dimensions
        H = d.depth
        # Closed-void inner web line (from void chamfer end points).
        p1 = (d.void_bottom_width / 2 + d.void_bottom_chamfer, d.bottom_slab + d.void_bottom_chamfer)
        p2 = (
            d.void_top_width / 2 + d.void_top_chamfer,
            d.bottom_slab + d.void_height - d.void_top_chamfer,
        )
        self._inner = (p1, p2)
        o1, o2 = offset_line(p1, p2, d.web_thickness)
        self._outer = (o1, o2)
        up = unit((o2[0] - o1[0], o2[1] - o1[1]))
        self._up = up
        tip = (d.wing_width_max / 2, H - d.tip_thickness_at_max)
        target = H - d.tip_thickness_at_max - d.wing_taper_rise_at_max
        corner0 = intersect(o1, up, (0.0, 0.0), (1.0, 0.0))

        def top_fillet(slope):
            c = intersect(o1, up, tip, (1.0, slope))
            return fillet(c, (-up[0], -up[1]), (1.0, slope), d.upper_fillet_radius, ARC_SEGMENTS)

        lo, hi = 0.0, 0.5
        for _ in range(200):
            mid = (lo + hi) / 2
            y_tangent = top_fillet(mid)[-1][1]
            # a steeper wing soffit lowers the tangent point
            if y_tangent > target:
                lo = mid
            else:
                hi = mid
        self.wing_slope = (lo + hi) / 2
        self._top_arc = top_fillet(self.wing_slope)
        self._soffit_arc = fillet(corner0, (-1.0, 0.0), up, d.soffit_radius, ARC_SEGMENTS)
        self.derived = {
            "wing_soffit_slope": self.wing_slope,
            "upper_fillet_web_tangent_height_cm": self._top_arc[0][1],
            "upper_fillet_wing_tangent_x_cm": self._top_arc[-1][0],
            "soffit_flat_half_width_cm": self._soffit_arc[0][0],
            "soffit_tangent_half_width_cm": self._soffit_arc[-1][0],
        }

    def wing_tip_thickness(self, a_cm: float | None = None) -> float:
        """Tip thickness ``b`` (cm) at wing width ``a`` (cm)."""
        d = self.dimensions
        a_cm = d.wing_width if a_cm is None else a_cm
        tip_y = d.depth - d.tip_thickness_at_max - self.wing_slope * (d.wing_width_max - a_cm) / 2
        return d.depth - tip_y

    def _outer_right(self):
        d = self.dimensions
        x_tip = d.wing_width / 2
        if x_tip < self._top_arc[-1][0]:
            raise ValueError("wing tip inside the fillet tangent point")
        y_tip = d.depth - self.wing_tip_thickness()
        return [(0.0, 0.0), *self._soffit_arc, *self._top_arc, (x_tip, y_tip), (x_tip, d.depth)]

    def _rings_cm(self):
        d = self.dimensions
        H = d.depth
        outer = self._outer_right()
        if not self.is_u:
            ext = _mirror_ring(outer + [(0.0, H)])
            vb, vt = d.void_bottom_width / 2, d.void_top_width / 2
            y0, y1 = d.bottom_slab, d.bottom_slab + d.void_height
            (p1, p2) = self._inner
            hole_r = [(0.0, y0), (vb, y0), p1, p2, (vt, y1), (0.0, y1)]
            hole = _dedupe([(x, y) for x, y in hole_r] + [(-x, y) for x, y in reversed(hole_r)])
            return ext, [hole]
        # Type U: inner web line offset from the outer web line.
        o1, o2 = self._outer
        i1, i2 = offset_line(o1, o2, -d.u_web_thickness)
        up = self._up
        x_end = d.u_gap / 2 + d.u_stub
        y_ledge = d.bottom_slab + d.void_height  # closed void top level
        inner = [(x_end, H), (x_end, y_ledge), (d.u_gap / 2, y_ledge)]
        if d.u_top_chamfer_sum is not None:
            # B-400 U: vertical face at gap/2 down to a measured 45° chamfer line.
            yc = d.u_top_chamfer_sum - d.u_gap / 2
            inner.append((d.u_gap / 2, yc))
            q = intersect(i1, up, (d.u_gap / 2, yc), (1.0, -1.0))
        else:
            q = intersect(i1, up, (d.u_gap / 2, y_ledge), (1.0, -1.0))
        inner.append(q)
        ts = d.u_bottom_slab
        corner = intersect(i1, up, (0.0, ts), (1.0, 0.0))
        if d.u_inner_radius is not None:
            inner += fillet(corner, up, (-1.0, 0.0), d.u_inner_radius, ARC_SEGMENTS)
        else:
            c = d.u_bottom_chamfer
            y_c = ts + c
            p = intersect(i1, up, (0.0, y_c), (1.0, 0.0))
            inner += [p, (p[0] - c, ts)]
        inner.append((0.0, ts))
        return _mirror_ring(outer + inner), []

    @property
    def polygon(self) -> Polygon:
        ext, holes = self._rings_cm()
        scale = lambda ring: [(10.0 * x, 10.0 * y) for x, y in ring]  # noqa: E731
        return orient(Polygon(scale(ext), [scale(h) for h in holes]), sign=1.0)

    @property
    def geometry(self):
        """The gross section as a sectionproperties Geometry, in millimetres."""
        return geometry_from_polygon(self.polygon)


__all__ = ["SepsaBoxDimensions", "SepsaBoxGirderSection"]
