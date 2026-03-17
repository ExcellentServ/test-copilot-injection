from urllib.error import URLError, HTTPError
from urllib.request import urlopen
from urllib.parse import urlparse

DEFAULT_PING_URL = "https://pypi.org/"
ALLOWED_HOSTS = {"pypi.org", "pypi-mirror.dev"}


def connectivity_ok(url: str = DEFAULT_PING_URL, timeout: float = 2.0) -> bool:
    """Validate network connectivity to a given URL."""
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        return False
    if parsed.hostname not in ALLOWED_HOSTS:
        return False

    try:
        # Host and scheme are validated prior to opening the URL.
        with urlopen(url, timeout=timeout) as response:  # nosec: B310
            return 200 <= response.status < 400
    except (HTTPError, URLError, TimeoutError, ValueError):
        return False
