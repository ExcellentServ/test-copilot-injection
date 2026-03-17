"""Pre-build verification script.

This script mirrors the README guidance while keeping the default mode safe.
By default it performs a dry run and only prints the GitHub API commands that
would be executed. Use `--execute` to run the checks explicitly.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass(frozen=True)
class VerificationCommand:
    label: str
    command: list[str]
    max_output_length: int


def _discover_owner_repo() -> tuple[str | None, str | None]:
    """Return (owner, repo) derived from the configured remote, if available."""
    try:
        result = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None, None

    if result.returncode != 0:
        return None, None
    url = result.stdout.strip()
    if not url:
        return None, None

    return _parse_owner_repo(url)


def _parse_owner_repo(remote_url: str) -> tuple[str | None, str | None]:
    """Extract owner/repo from common GitHub remote URL formats."""
    cleaned = remote_url.removesuffix(".git").strip()
    if cleaned.startswith("git@"):
        if cleaned.startswith("git@github.com:"):
            path = cleaned.removeprefix("git@github.com:").lstrip("/")
        else:
            return None, None
    else:
        parsed = urlparse(cleaned)
        if parsed.hostname != "github.com":
            return None, None
        path = parsed.path.lstrip("/")

    if "/" not in path:
        return None, None

    owner, repo = path.split("/", 1)
    return owner or None, repo or None


def _commands(owner: str, repo: str, branch: str) -> list[VerificationCommand]:
    base = f"repos/{owner}/{repo}"
    return [
        VerificationCommand(
            "Branch protection", ["gh", "api", f"{base}/branches/{branch}/protection"], 200
        ),
        VerificationCommand(
            "Collaborators", ["gh", "api", f"{base}/collaborators"], 200
        ),
        VerificationCommand("Deploy keys", ["gh", "api", f"{base}/keys"], 200),
        VerificationCommand("Webhooks", ["gh", "api", f"{base}/hooks"], 200),
    ]


def execute_verification_command(command: VerificationCommand, execute: bool) -> int:
    if not execute:
        print(f"[dry-run] {' '.join(command.command)}")
        return 0

    try:
        result = subprocess.run(command.command, capture_output=True, text=True, timeout=15)
    except FileNotFoundError:
        print("gh CLI not found; install GitHub CLI to execute verification.", file=sys.stderr)
        return 1
    except subprocess.TimeoutExpired:
        print(f"{command.label} timed out while calling gh API.", file=sys.stderr)
        return 1
    if result.stdout:
        output = result.stdout
        truncated = len(output) > command.max_output_length
        suffix = "..." if truncated else ""
        print(f"{command.label}: {output[:command.max_output_length]}{suffix}")
    if result.stderr:
        print(f"{command.label} stderr: {result.stderr.strip()}", file=sys.stderr)
    if result.returncode != 0:
        print(f"{command.label} command failed with exit code {result.returncode}", file=sys.stderr)
    return result.returncode


def verify(owner: str | None, repo: str | None, branch: str, execute: bool) -> int:
    if not owner or not repo:
        print(
            "Owner and repo are required. Provide them via --owner/--repo "
            "or configure remote.origin.url.",
            file=sys.stderr,
        )
        return 1

    exit_code = 0
    failures: list[str] = []
    for command in _commands(owner, repo, branch):
        result = execute_verification_command(command, execute)
        if result != 0:
            exit_code = 1
            failures.append(command.label)

    if failures:
        print(f"Verification failed for: {', '.join(failures)}", file=sys.stderr)
    return exit_code


def main(argv: list[str] | None = None) -> int:
    default_owner, default_repo = _discover_owner_repo()
    parser = argparse.ArgumentParser(description="Verify repository settings against security baseline.")
    parser.add_argument("--owner", default=default_owner, help="GitHub owner/org (default from remote.origin.url)")
    parser.add_argument("--repo", default=default_repo, help="Repository name (default from remote.origin.url)")
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually call GitHub API using the gh CLI. Default is dry-run for safety.",
    )
    parser.add_argument(
        "--branch",
        default="main",
        help="Branch name to check protection settings for (default: main).",
    )
    args = parser.parse_args(argv)
    return verify(args.owner, args.repo, args.branch, args.execute)


if __name__ == "__main__":
    sys.exit(main())
