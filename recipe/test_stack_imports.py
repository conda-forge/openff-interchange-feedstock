from openff.interchange.components.interchange import Interchange
from openff.toolkit.utils.toolkits import (
    GLOBAL_TOOLKIT_REGISTRY,
    AmberToolsToolkitWrapper,
    RDKitToolkitWrapper,
)

assert RDKitToolkitWrapper().is_available()
assert AmberToolsToolkitWrapper().is_available()


print(GLOBAL_TOOLKIT_REGISTRY.registered_toolkit_versions)
