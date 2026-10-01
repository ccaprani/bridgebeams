"""Shared outline builder for Bulgarian crossfall I-girders (private helper)."""

from __future__ import annotations


def crossfall_i_outline(*, top_width: float, web: float, fillet_h: float, bottom_width: float,
                        haunch_h: float, flange_side_top: float, chamfer: float, web_top: float,
                        left: tuple[float, float, float], right: tuple[float, float, float]
                        ) -> list[tuple[float, float]]:
    """CCW outline (origin mid-soffit, y up) of an I-girder with a sloping top flange.

    ``left``/``right`` are (fillet_v, underside taper, edge thickness) measured
    upwards from ``web_top`` at each side.
    """
    b, t, bf, c = top_width / 2, web / 2, bottom_width / 2, chamfer
    yh = flange_side_top + haunch_h

    def side(sign: float, chain: tuple[float, float, float]):
        fv, taper, te = chain
        yf = web_top + fv
        yu = yf + taper
        return [(sign * t, yh), (sign * t, web_top), (sign * (t + fillet_h), yf),
                (sign * b, yu), (sign * b, yu + te)]

    right_side = [(bf - c, 0.0), (bf, c), (bf, flange_side_top)] + side(1.0, right)
    left_side = side(-1.0, left)[::-1] + [(-bf, flange_side_top), (-bf, c), (-bf + c, 0.0)]
    return right_side + left_side
