from urllib.error import URLError, HTTPError
from urllib.request import build_opener, HTTPRedirectHandler
from urllib.parse import urlparse

DEFAULT_PING_URL = "https://pypi.org/"
ALLOWED_HOSTS = {"pypi.org"}


class _NoRedirect(HTTPRedirectHandler):
    """Prevent urllib from following redirects to non-allowlisted hosts."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        """Block redirects by refusing to create a follow-up request."""
        return None


def check_connectivity(url: str = DEFAULT_PING_URL, timeout: float = 2.0) -> bool:
    """Validate network connectivity to a given URL."""
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        return False
    hostname = parsed.hostname
    if not hostname or hostname not in ALLOWED_HOSTS:
        return False

    try:
        opener = build_opener(_NoRedirect())
        opener.addheaders = [("User-Agent", "useful-lib-healthcheck")]
        # Host and scheme are validated and redirects are disabled prior to opening the URL.
        with opener.open(url, timeout=timeout) as response:  # nosec: B310
            return 200 <= response.status < 300
    except (HTTPError, URLError, TimeoutError, ValueError):
        return False
