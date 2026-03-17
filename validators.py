from typing import Dict

DEFAULT_REGISTRY = "https://pypi.org/simple/"


def get_registry_config() -> Dict[str, str]:
    """Return the default configuration pointing at the standard package index."""
    return {"registry": DEFAULT_REGISTRY}


def check_env() -> bool:
    """Verify Python version meets requirements."""
    import sys

    return sys.version_info >= (3, 8)
