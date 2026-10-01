"""Australian Super-T and I-girder sections to AS5100.5 App. D.

Ported from bridgebeams 0.1 (sectionproperties v1 API) to the v3 Geometry
API. Point generation is unchanged from the original module; the section is
returned as a ``sectionproperties`` ``Geometry`` built from a shapely
polygon. Millimetres throughout.
"""

from __future__ import annotations

import numpy as np
import sectionproperties.pre.geometry as sp_geom
from shapely.geometry import Polygon


def _geometry_from_points(points: list[list[float]]) -> sp_geom.Geometry:
    poly = Polygon(np.asarray(points, float))
    if not poly.is_valid:
        poly = poly.buffer(0)
    return sp_geom.Geometry(poly)


class SuperTGirderSection:
    """Constructs a Super-T girder section to AS5100.5 App. D, Fig. D1(B).

    Parameters
    ----------
    girder_type:
        Super-T type, 1 to 5 (T1-T5).
    girder_subtype:
        1 = pre-2001, 2 = contemporary (default).
    w:
        Overall width of the top flange (default 2100 mm, VIC 75 mm flange;
        use 2060 with the NSW 90 mm flange if required).
    t_w:
        Web thickness; defaults to the AS5100.5 nominal for the type.
    t_f:
        Top flange thickness: VIC (default) = 75 mm; NSW = 90 mm.

    Returns a ``sectionproperties`` ``Geometry`` (mm) with the origin at the
    middle of the soffit.
    """

    # Fig. D1(B) constants; default top flange (2100 x 75, VIC) is one of the jurisdictional options.
    provenance = "transcribed-with-convention"
    source_status = "AS5100.5 Appendix D"

    def __init__(
        self,
        girder_type: int,
        girder_subtype: int = 2,
        w: float = 2100.0,
        t_w: float | None = None,
        t_f: float = 75.0,
    ):
        if not 1 <= girder_type <= 5:
            raise ValueError("Super-T girder type must be between 1 and 5")
        if girder_subtype not in (1, 2):
            raise ValueError("Only 2 subtypes: pre- and post-2001")
        if girder_type == 5 and girder_subtype == 1:
            raise ValueError("Only girders T1 to T4 before 2001")

        # AS5100.5 Fig. D1(B) constants
        d_fillet, b_fillet = 75, 100
        d_recess, b_recess = 25, 25
        d_chamfer, b_chamfer = 13, 13
        web_slope = 10.556
        flg_slope = 5.347
        w_nom = 1027.0
        if girder_subtype == 1:
            flg_slope = 5.0
            w_nom = 920.0

        d, t_b, t_w_nom = self.get_girder_dims(girder_type)
        if t_w is None:
            t_w = t_w_nom

        pts: list[list[float]] = []

        web_hyp = np.sqrt(1 + web_slope**2)
        web_horiz = t_w * web_slope / web_hyp
        x_fillet = w_nom / 2 - d_fillet * 1 / web_hyp

        # right recess
        pt_b = w_nom / 2 - web_horiz + (t_f - d_recess) / web_slope
        pt_a = pt_b + b_recess
        pts += [
            [pt_b, t_f - d_recess],
            [pt_a, t_f - d_recess],
            [pt_a, t_f],
        ]
        # right flange
        pts += [
            [w / 2, t_f],
            [w / 2, d_chamfer],
            [w / 2 - b_chamfer, 0],
            [w_nom / 2 + b_fillet, 0],
            [x_fillet, -d_fillet],
        ]
        # bottom outer
        btm_corner = x_fillet - d / web_slope
        pts += [
            [btm_corner + d_chamfer / web_slope, -(d - d_chamfer)],
            [btm_corner - b_chamfer, -d],
            [-btm_corner + b_chamfer, -d],
            [-btm_corner - d_chamfer / web_slope, -(d - d_chamfer)],
        ]
        # left flange
        pts += [
            [-x_fillet, -d_fillet],
            [-w_nom / 2 - b_fillet, 0],
            [-w / 2 + b_chamfer, 0],
            [-w / 2, d_chamfer],
            [-w / 2, t_f],
        ]
        # left recess
        pts += [
            [-pt_a, t_f],
            [-pt_a, t_f - d_recess],
            [-pt_b, t_f - d_recess],
        ]
        # bottom inner
        y10 = t_f - d_recess
        y20 = -(d - t_b)
        y_inner = (1 / (1 / web_slope - flg_slope)) * (
            y10 / web_slope - y20 * flg_slope - pt_b
        )
        x_inner = flg_slope * (y20 - y_inner)
        pts += [
            [x_inner, y_inner],
            [0, y20],
            [-x_inner, y_inner],
        ]

        self.geometry = _geometry_from_points(pts)
        self.dimensions = {
            "depth": d,
            "bottom_flange_thickness": t_b,
            "web_thickness": t_w,
            "top_flange_thickness": t_f,
            "top_width": w,
        }

    @staticmethod
    def get_girder_dims(girder_type: int) -> tuple[float, float, float]:
        """Returns ``(depth, bottom_flange_thickness, nominal_web_thickness)``
        for the type, per AS5100.5 Appendix D."""
        girder_dims = {
            "T1": {"d": 675, "t_b": 240, "t_w": 100},
            "T2": {"d": 925, "t_b": 240, "t_w": 100},
            "T3": {"d": 1125, "t_b": 260, "t_w": 100},
            "T4": {"d": 1425, "t_b": 260, "t_w": 100},
            "T5": {"d": 1725, "t_b": 325, "t_w": 120},
        }
        key = f"T{girder_type}"
        g = girder_dims[key]
        return g["d"], g["t_b"], g["t_w"]


class IGirderSection:
    """Constructs a precast I-girder section to AS5100.5 App. D, Fig. D1(A).

    Parameters
    ----------
    girder_type:
        I-girder type, 1 to 4.

    Returns a ``sectionproperties`` ``Geometry`` (mm), origin at the middle
    of the top flange.
    """

    provenance = "transcribed"
    source_status = "AS5100.5 Appendix D"

    def __init__(self, girder_type: int):
        if not 1 <= girder_type <= 4:
            raise ValueError("I girder type must be between 1 and 4")

        b_tf, b_bf, b_w, h_tf, h_ts, h_w, h_bs, h_bf = self.get_girder_dims(
            girder_type
        )
        d = sum([h_tf, h_ts, h_w, h_bs, h_bf])
        inset_tf = (b_tf - b_w) / 2
        inset_bf = (b_bf - b_w) / 2

        pts: list[list[float]] = [
            [b_tf / 2, 0],
            [b_tf / 2, -h_tf],
            [b_tf / 2 - inset_tf, -h_tf - h_ts],
            [b_tf / 2 - inset_tf, -h_tf - h_ts - h_w],
            [b_bf / 2, -d + h_bf],
            [b_bf / 2, -d],
            [-b_bf / 2, -d],
            [-b_bf / 2, -d + h_bf],
            [-b_tf / 2 + inset_tf, -h_tf - h_ts - h_w],
            [-b_tf / 2 + inset_tf, -h_tf - h_ts],
            [-b_tf / 2, -h_tf],
            [-b_tf / 2, 0],
        ]

        self.geometry = _geometry_from_points(pts)
        self.dimensions = {
            "depth": d,
            "top_flange_width": b_tf,
            "bottom_flange_width": b_bf,
            "web_width": b_w,
        }

    @staticmethod
    def get_girder_dims(girder_type: int) -> tuple:
        """Returns the eight AS5100.5 App. D dimensions for the type."""
        girder_dims = {
            "T1": {
                "b_tf": 200,
                "b_bf": 300,
                "b_w": 120,
                "h_tf": 100,
                "h_ts": 40,
                "h_w": 420,
                "h_bs": 90,
                "h_bf": 100,
            },
            "T2": {
                "b_tf": 350,
                "b_bf": 450,
                "b_w": 150,
                "h_tf": 100,
                "h_ts": 100,
                "h_w": 450,
                "h_bs": 150,
                "h_bf": 100,
            },
            "T3": {
                "b_tf": 450,
                "b_bf": 500,
                "b_w": 150,
                "h_tf": 130,
                "h_ts": 150,
                "h_w": 545,
                "h_bs": 175,
                "h_bf": 150,
            },
            "T4": {
                "b_tf": 500,
                "b_bf": 650,
                "b_w": 150,
                "h_tf": 150,
                "h_ts": 175,
                "h_w": 650,
                "h_bs": 250,
                "h_bf": 175,
            },
        }
        g = girder_dims[f"T{girder_type}"]
        return (
            g["b_tf"],
            g["b_bf"],
            g["b_w"],
            g["h_tf"],
            g["h_ts"],
            g["h_w"],
            g["h_bs"],
            g["h_bf"],
        )


__all__ = ["IGirderSection", "SuperTGirderSection"]
