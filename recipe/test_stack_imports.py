from openff.interchange import *
from openff.toolkit import *
from openff.toolkit.utils.toolkits import *

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

interchange = force_field.create_interchange(molecule.to_topology())
interchange.to_openmm_simulation()
interchange.to_gromacs("fOOO")
interchange.to_lammps("bAAAR")
interchange.to_prmtop("bAAAZ")
