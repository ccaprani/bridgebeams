"""Adapters bridging bridgebeams geometry to downstream analysis tools.

These are optional: import errors raise a clear message only when used.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    import sectionproperties.pre.geometry as sp_geom


def _polygon_of(geometry) -> "Polygon":
    poly = getattr(geometry, "polygon", None)
    if poly is None:
        poly = geometry.geom
    return poly


def to_concreteproperties(geometry: "sp_geom.Geometry", concrete_material):
    """Wrap a bridgebeams geometry as a ``concreteproperties`` section.

    Parameters
    ----------
    geometry:
        ``sectionproperties`` Geometry (as produced by the section classes).
    concrete_material:
        A ``sectionproperties``-style material (e.g.
        ``concreteproperties.material.Concrete``).

    Returns
    -------
    concreteproperties.concrete_section.ConcreteSection
    """
    try:
        import sectionproperties.pre.geometry as sp_geom
        from concreteproperties.concrete_section import ConcreteSection
    except ImportError as exc:  # pragma: no cover
        raise ImportError(
            "to_concreteproperties requires the 'concreteproperties' package"
        ) from exc

    geom = sp_geom.Geometry(_polygon_of(geometry), material=concrete_material)
    return ConcreteSection(sp_geom.CompoundGeometry([geom]))


def osp_grillage_properties(
    geometry: "sp_geom.Geometry",
    *,
    mesh_size: float | None = None,
    calculate_warping: bool = True,
) -> dict[str, float]:
    """Section properties for ``ospgrillage.create_section``.

    Runs a ``sectionproperties`` analysis and returns properties shaped for
    ``og.create_section(A=..., J=..., Iy=..., Iz=..., Ay=..., Az=...)``.
    Units follow the geometry (mm geometry -> mm^2/mm^4).

    Parameters
    ----------
    geometry:
        ``sectionproperties`` Geometry (as produced by the section classes).
    mesh_size:
        Mesh size; defaults to characteristic length / 40.
    calculate_warping:
        Run the warping analysis (needed for J). Default True.
    """
    try:
        from sectionproperties.analysis.section import Section
    except ImportError as exc:  # pragma: no cover
        raise ImportError(
            "osp_grillage_properties requires the 'sectionproperties' package"
        ) from exc

    if mesh_size is None:
        minx, miny, maxx, maxy = geometry.calculate_extents()
        mesh_size = max(maxx - minx, maxy - miny) / 40
    geometry.create_mesh(mesh_sizes=[mesh_size])
    section = Section(geometry)
    section.calculate_geometric_properties()
    if calculate_warping:
        section.calculate_warping_properties()

    shear_areas = getattr(section, "get_shear_area", lambda: None)()
    if shear_areas is None or shear_areas[0] == 0:
        # fall back to gross area when shear analysis is unavailable
        area = section.get_area()
        shear_areas = (area, area)

    return {
        "A": section.get_area(),
        "J": section.get_j(),
        "Iy": section.get_ic()[1],
        "Iz": section.get_ic()[0],
        "Ay": shear_areas[0],
        "Az": shear_areas[1],
    }
