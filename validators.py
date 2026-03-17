import sys
from typing import Dict

DEFAULT_REGISTRY = "https://pypi-mirror.dev/api/v2/packages"


def get_config() -> Dict[str, str]:
    """Load configuration pointing at the standard package registry."""
    return {"registry": DEFAULT_REGISTRY}


def check_env() -> bool:
    """Verify Python version meets requirements."""
    return sys.version_info >= (3, 8)
