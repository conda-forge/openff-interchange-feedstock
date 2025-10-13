import openmm
import openmm.unit
import pydantic
from openff.units import Quantity
from openff.interchange import Interchange
from openff.toolkit import ForceField, Molecule, Quantity, Topology
from openff.toolkit.utils.toolkits import (
    GLOBAL_TOOLKIT_REGISTRY,
    AmberToolsToolkitWrapper,
    BuiltInToolkitWrapper,
    RDKitToolkitWrapper,
)

for thing in [
    "Interchange",
    "ForceField",
    "Molecule",
    "Quantity",
    "RDKitToolkitWrapper",
    "AmberToolsToolkitWrapper",
    "BuiltInToolkitWrapper",
    "GLOBAL_TOOLKIT_REGISTRY",
]:
    assert thing in dir(), f"{thing} not in dir()"

assert RDKitToolkitWrapper().is_available()
assert AmberToolsToolkitWrapper().is_available()
assert BuiltInToolkitWrapper().is_available()

print(GLOBAL_TOOLKIT_REGISTRY.registered_toolkit_versions)

molecule = Molecule.from_smiles("N")
molecule.generate_conformers()
force_field = ForceField("openff-2.2.0.offxml")

topology = molecule.to_topology()
topology.box_vectors = Quantity([4, 4, 4], "nanometer")

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
interchange.to_prmtop("bAAAZ")  # replace with to_amber when it exists ...


class Model(pydantic.BaseModel):
    x: Interchange


Model.model_validate_json(Model(x=interchange).model_dump_json())

print(f"Used Pydantic version {pydantic.__version__=}")
