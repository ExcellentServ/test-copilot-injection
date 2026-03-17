from urllib.request import urlopen
from urllib.error import URLError, HTTPError

DEFAULT_PING_URL = "https://pypi.org/"


def connectivity_ok(url: str = DEFAULT_PING_URL, timeout: float = 2.0) -> bool:
    """Validate network connectivity to a given URL."""
    try:
        with urlopen(url, timeout=timeout) as response:  # nosec: B310
            return 200 <= response.status < 400
    except (HTTPError, URLError, TimeoutError, ValueError):
        return False
