from openff.interchange import Interchange
from openff.toolkit import ForceField, Molecule, Topology, Quantity
from openff.toolkit.utils.toolkits import (
    RDKitToolkitWrapper,
    OpenEyeToolkitWrapper,
    AmberToolsToolkitWrapper,
    BuiltInToolkitWrapper,
    ToolkitWrapper,
    GLOBAL_TOOLKIT_REGISTRY,
)
import openmm
import openmm.unit


for thing in [
    "Interchange",
    "ForceField",
    "Molecule",
    "Topology",
    "Quantity",
    "RDKitToolkitWrapper",
    "OpenEyeToolkitWrapper",
    "AmberToolsToolkitWrapper",
    "BuiltInToolkitWrapper",
    "ToolkitWrapper",
    "GLOBAL_TOOLKIT_REGISTRY",
]:
    assert thing in dir(), f"{thing} not in dir()"

assert RDKitToolkitWrapper().is_available()
assert AmberToolsToolkitWrapper().is_available()

print(GLOBAL_TOOLKIT_REGISTRY.registered_toolkit_versions)

molecule = Molecule.from_smiles("C")
molecule.generate_conformers()
force_field = ForceField("openff-2.0.0.offxml")

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
