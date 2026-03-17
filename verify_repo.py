"""Pre-build verification script.

This script mirrors the README guidance while keeping the default mode safe.
By default it performs a dry run and only prints the GitHub API commands that
would be executed. Use `--execute` to run the checks explicitly.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from typing import List, Optional, Tuple


Command = Tuple[str, List[str], int]


def _discover_owner_repo() -> Tuple[Optional[str], Optional[str]]:
    """Return (owner, repo) derived from the configured remote, if available."""
    result = subprocess.run(
        ["git", "config", "--get", "remote.origin.url"],
        capture_output=True,
        text=True,
    )
    url = result.stdout.strip()
    if not url:
        return None, None

    # Handle URLs like:
    # - https://github.com/ExcellentServ/test-copilot-injection.git
    # - git@github.com:ExcellentServ/test-copilot-injection.git
    trimmed = url.removesuffix(".git")
    if "github.com/" in trimmed:
        _, _, tail = trimmed.partition("github.com/")
    elif "github.com:" in trimmed:
        _, _, tail = trimmed.partition("github.com:")
    else:
        return None, None

    if "/" not in tail:
        return None, None

    owner, repo = tail.split("/", 1)
    return owner or None, repo or None


def _commands(owner: str, repo: str) -> List[Command]:
    base = f"repos/{owner}/{repo}"
    return [
        ("Branch protection", ["gh", "api", f"{base}/branches/main/protection"], 200),
        ("Collaborators", ["gh", "api", f"{base}/collaborators"], 500),
        ("Deploy keys", ["gh", "api", f"{base}/keys"], 500),
        ("Webhooks", ["gh", "api", f"{base}/hooks"], 500),
    ]


def run_command(label: str, command: List[str], preview_chars: int, execute: bool) -> int:
    if not execute:
        print(f"[dry-run] {' '.join(command)}")
        return 0

    result = subprocess.run(command, capture_output=True, text=True)
    if result.stdout:
        print(f"{label}: {result.stdout[:preview_chars]}")
    if result.stderr:
        print(f"{label} stderr: {result.stderr.strip()}", file=sys.stderr)
    if result.returncode != 0:
        print(f"{label} command failed with exit code {result.returncode}", file=sys.stderr)
    return result.returncode


def verify(owner: Optional[str], repo: Optional[str], execute: bool) -> int:
    if not owner or not repo:
        print(
            "Owner and repo are required. Provide them via --owner/--repo "
            "or configure remote.origin.url.",
            file=sys.stderr,
        )
        return 1

    status = 0
    for label, cmd, preview in _commands(owner, repo):
        status |= run_command(label, cmd, preview, execute)
    return status


def main(argv: Optional[list[str]] = None) -> int:
    default_owner, default_repo = _discover_owner_repo()
    parser = argparse.ArgumentParser(description="Verify repository settings against security baseline.")
    parser.add_argument("--owner", default=default_owner, help="GitHub owner/org (default from remote.origin.url)")
    parser.add_argument("--repo", default=default_repo, help="Repository name (default from remote.origin.url)")
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually call GitHub API using the gh CLI. Default is dry-run for safety.",
    )
    args = parser.parse_args(argv)
    return verify(args.owner, args.repo, args.execute)


if __name__ == "__main__":
    sys.exit(main())
