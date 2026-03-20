#!/usr/bin/env python3
"""
upgrade.py - Check and update hardcoded software versions in installation scripts.

Targets:
  - Terraform            -> claude/claude-devops/terraform-install.sh
  - Debian forky slim    -> debian/forky/Dockerfile
  - Debian bookworm slim -> debian/bookworm/Dockerfile

Usage:
  python3 upgrade.py            # check and update
  python3 upgrade.py --dry-run  # check only, no file changes
"""

import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

WORKSPACE = Path(__file__).parent

TERRAFORM_SCRIPT    = WORKSPACE / "claude/claude-devops/terraform-install.sh"
FORKY_DOCKERFILE    = WORKSPACE / "debian/forky/Dockerfile"
BOOKWORM_DOCKERFILE = WORKSPACE / "debian/bookworm/Dockerfile"


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def fetch_json(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code} fetching {url}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error fetching {url}: {e.reason}") from e


# ---------------------------------------------------------------------------
# Version fetchers
# ---------------------------------------------------------------------------

def get_latest_terraform():
    data = fetch_json("https://api.releases.hashicorp.com/v1/releases/terraform/latest")
    return data["version"]


def get_latest_debian_forky_slim():
    """Return the latest forky-YYYYMMDD-slim tag from Docker Hub."""
    url = (
        "https://hub.docker.com/v2/repositories/library/debian/tags"
        "?name=forky-&ordering=last_updated&page_size=100"
    )
    data = fetch_json(url)
    pattern = re.compile(r"^forky-(\d{8})-slim$")
    candidates = []
    for result in data.get("results", []):
        m = pattern.match(result["name"])
        if m:
            candidates.append((m.group(1), result["name"]))  # (date_str, full_tag)
    if not candidates:
        raise RuntimeError("No forky-YYYYMMDD-slim tags found on Docker Hub")
    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[0][1]  # e.g. "forky-20260223-slim"


def get_latest_debian_bookworm_slim():
    """Return the latest bookworm-YYYYMMDD-slim tag from Docker Hub."""
    url = (
        "https://hub.docker.com/v2/repositories/library/debian/tags"
        "?name=bookworm-&ordering=last_updated&page_size=100"
    )
    data = fetch_json(url)
    pattern = re.compile(r"^bookworm-(\d{8})-slim$")
    candidates = []
    for result in data.get("results", []):
        m = pattern.match(result["name"])
        if m:
            candidates.append((m.group(1), result["name"]))  # (date_str, full_tag)
    if not candidates:
        raise RuntimeError("No bookworm-YYYYMMDD-slim tags found on Docker Hub")
    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[0][1]  # e.g. "bookworm-20260316-slim"


# ---------------------------------------------------------------------------
# File helpers
# ---------------------------------------------------------------------------

def read_current(path, pattern):
    """Extract current value using a regex with one capture group."""
    content = path.read_text()
    m = re.search(pattern, content)
    if not m:
        raise RuntimeError(f"Pattern {pattern!r} not found in {path}")
    return m.group(1)


def update_file(path, pattern, replacement, dry_run=False):
    """Replace first regex match in file. Returns True if content would change."""
    content = path.read_text()
    new_content, count = re.subn(pattern, replacement, content, count=1)
    if count == 0:
        raise RuntimeError(f"Pattern {pattern!r} not found in {path}")
    if new_content == content:
        return False
    if not dry_run:
        path.write_text(new_content)
    return True


# ---------------------------------------------------------------------------
# Per-tool check + update logic
# ---------------------------------------------------------------------------

def check(name, current, latest, path, search_pattern, replacement, dry_run):
    if current == latest:
        print(f"  ok        {current}")
        return False
    print(f"  outdated  {current} -> {latest}")
    changed = update_file(path, search_pattern, replacement, dry_run)
    if changed and not dry_run:
        print(f"  updated   {path.relative_to(WORKSPACE)}")
    elif changed and dry_run:
        print(f"  would update {path.relative_to(WORKSPACE)}")
    return changed


def run_terraform(dry_run):
    print("[terraform]")
    current = read_current(TERRAFORM_SCRIPT, r"TF_VERSION='([^']+)'")
    latest  = get_latest_terraform()
    return check(
        "terraform", current, latest,
        TERRAFORM_SCRIPT,
        r"TF_VERSION='[^']+'",
        f"TF_VERSION='{latest}'",
        dry_run,
    )


def run_debian_forky(dry_run):
    print("[debian forky slim]")
    current = read_current(FORKY_DOCKERFILE, r"FROM debian:(\S+)")
    latest  = get_latest_debian_forky_slim()
    return check(
        "debian", current, latest,
        FORKY_DOCKERFILE,
        r"FROM debian:\S+",
        f"FROM debian:{latest}",
        dry_run,
    )


def run_debian_bookworm(dry_run):
    print("[debian bookworm slim]")
    current = read_current(BOOKWORM_DOCKERFILE, r"FROM debian:(\S+)")
    latest  = get_latest_debian_bookworm_slim()
    return check(
        "debian", current, latest,
        BOOKWORM_DOCKERFILE,
        r"FROM debian:\S+",
        f"FROM debian:{latest}",
        dry_run,
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

CHECKS = [
    run_terraform,
    run_debian_forky,
    run_debian_bookworm,
]


def main():
    dry_run = "--dry-run" in sys.argv
    if dry_run:
        print("=== DRY-run mode: no files will be modified ===\n")

    any_updated = False
    any_error   = False

    for fn in CHECKS:
        try:
            updated = fn(dry_run)
            any_updated = any_updated or updated
        except Exception as e:
            print(f"  ERROR: {e}")
            any_error = True
        print()

    if any_error:
        print("Finished with errors.")
        sys.exit(1)
    elif any_updated and dry_run:
        print("Updates available (dry-run, no files changed).")
    elif any_updated:
        print("All updates applied.")
    else:
        print("Everything is up to date.")


if __name__ == "__main__":
    main()
