from openff.toolkit import *
from openff.interchange import *
from openff.toolkit.utils.toolkits import *


assert RDKitToolkitWrapper().is_available()
assert AmberToolsToolkitWrapper().is_available()

print(GLOBAL_TOOLKIT_REGISTRY.registered_toolkit_versions)

molecule = Molecule.from_smiles("CCO")
molecule.generate_conformers()
force_field = ForceField("openff-2.0.0.offxml")

force_field.create_openmm_system(molecule.to_topology())
