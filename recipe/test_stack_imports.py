import random

import openmm
import openmm.unit
import pydantic
from openff.interchange import Interchange, __version__
from openff.toolkit import ForceField, Molecule, Quantity
from openff.toolkit.utils.toolkits import (
    GLOBAL_TOOLKIT_REGISTRY,
    BuiltInToolkitWrapper,
    NAGLToolkitWrapper,
    RDKitToolkitWrapper,
)

assert __version__ != "0.0.0", f"Version handling mangled! Found {__version__}"

for thing in [
    "Interchange",
    "ForceField",
    "Molecule",
    "Quantity",
    "RDKitToolkitWrapper",
    "NAGLToolkitWrapper",
    "BuiltInToolkitWrapper",
    "GLOBAL_TOOLKIT_REGISTRY",
]:
    assert thing in dir(), f"{thing} not in dir()"

assert RDKitToolkitWrapper().is_available()
assert NAGLToolkitWrapper().is_available()
assert BuiltInToolkitWrapper().is_available()

print(GLOBAL_TOOLKIT_REGISTRY.registered_toolkit_versions)

molecule = Molecule.from_smiles("CN1C=NC2=C1C(=O)N(C(=O)N2C)C")
molecule.generate_conformers(n_conformers=1)

topology = molecule.to_topology()
topology.box_vectors = Quantity([4, 4, 4], "nanometer")

for offxml in [
    "openff_no_water_unconstrained-3.0.0-alpha0.offxml",
    "openff-2.3.0.offxml",
]:
    force_field = ForceField(offxml)

    flag = random.random()
    force_field["Electrostatics"].scale14 = flag

    interchange = force_field.create_interchange(topology)

    interchange.to_openmm_simulation(
        integrator=openmm.LangevinMiddleIntegrator(
            293.15 * openmm.unit.kelvin,
            1.0 / openmm.unit.picosecond,
            2.0 * openmm.unit.femtosecond,
        )
    )
    interchange.to_gromacs("fOOO")
    interchange.to_lammps("bAAAR")
    interchange.to_amber("bAAAZ")

    class Model(pydantic.BaseModel):
        x: Interchange
        y: Quantity

    parsed_model = Model.model_validate_json(
        Model(x=interchange, y=Quantity("21 angstrom")).model_dump_json()
    )

    assert parsed_model.x is not None
    assert parsed_model.x["Electrostatics"].scale_14 == flag, (
        f"{parsed_model.x["Electrostatics"].scale_14=}"
    )
    assert parsed_model.y.m_as("nanometer") == 2.1, (
        f"{parsed_model.y.m_as("nanometer")=}"
    )

    print(f"Used Pydantic version {pydantic.__version__=}")
