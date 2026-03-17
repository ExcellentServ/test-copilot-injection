import sys
from typing import Dict

DEFAULT_REGISTRY = "https://pypi.org/simple/"


def get_registry_config() -> Dict[str, str]:
    """Return registry configuration as {'registry': DEFAULT_REGISTRY}."""
    return {"registry": DEFAULT_REGISTRY}


def check_python_version() -> bool:
    """Verify Python version meets requirements."""
    return sys.version_info >= (3, 8)
