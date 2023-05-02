from openff.interchange import *
from openff.toolkit import *
from openff.toolkit.utils.toolkits import *

for thing in [
    "Interchange",
    "ForceField",
    "Molecule",
    "Topology",
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

force_field.create_openmm_system(molecule.to_topology())
Interchange.from_smirnoff(force_field, [molecule])
