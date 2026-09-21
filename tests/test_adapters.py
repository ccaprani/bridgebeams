"""Adapter tests (concreteproperties parts skipped if absent)."""

import pytest

from bridgebeams.ukie import IeYBeamSection


def test_osp_grillage_properties():
    from bridgebeams.adapters import osp_grillage_properties

    beam = IeYBeamSection("Y4")
    props = osp_grillage_properties(beam.geometry)
    for key in ("A", "J", "Iy", "Iz", "Ay", "Az"):
        assert key in props
        assert props[key] > 0
    # cross-check A against the exact polygon area (within mesh tolerance)
    from bridgebeams._geometry import as_polygon, section_properties

    exact = section_properties(as_polygon(beam.geometry))["area"]
    assert props["A"] == pytest.approx(exact, rel=0.005)


def test_to_concreteproperties():
    pytest.importorskip("concreteproperties")
    from concreteproperties.concrete_section import ConcreteSection
    from concreteproperties.material import Concrete
    from concreteproperties.stress_strain_profile import (
        ConcreteLinear,
        ConcreteUltimateProfile,
    )

    from bridgebeams.adapters import to_concreteproperties

    concrete = Concrete(
        name="32 MPa",
        density=2.4e-6,
        stress_strain_profile=ConcreteLinear(elastic_modulus=30e3),
        ultimate_stress_strain_profile=ConcreteUltimateProfile(
            strains=[0.0, 0.003],
            stresses=[0.0, 32.0],
            compressive_strength=32,
        ),
        flexural_tensile_strength=3.4,
        colour="lightgrey",
    )
    beam = IeYBeamSection("Y4")
    cs = to_concreteproperties(beam.geometry, concrete)
    assert isinstance(cs, ConcreteSection)
    # gross area must match the exact polygon area
    from bridgebeams._geometry import as_polygon, section_properties

    exact = section_properties(as_polygon(beam.geometry))["area"]
    assert cs.gross_properties.concrete_area == pytest.approx(exact, rel=1e-6)
