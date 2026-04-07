#!/usr/bin/env python3
"""
upgrade.py - Check and update hardcoded software versions in installation scripts.

Targets:
  - Terraform            -> claude/claude-devops/terraform-install.sh
  - Debian forky slim    -> debian/forky/Dockerfile
  - Debian bookworm slim -> debian/bookworm/Dockerfile
  - devops release       -> devops/aws/Dockerfile, devops/gcloud/Dockerfile

Usage:
  python3 upgrade.py                   # skip devops, upgrade everything else
  python3 upgrade.py --devops 260320.1 # also upgrade devops to the given version
"""

import json
import re
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

WORKSPACE = Path(__file__).parent

TERRAFORM_SCRIPT    = WORKSPACE / "claude/claude-devops/terraform-install.sh"
FORKY_DOCKERFILE    = WORKSPACE / "debian/forky/Dockerfile"
BOOKWORM_DOCKERFILE = WORKSPACE / "debian/bookworm/Dockerfile"
DEVOPS_AWS_DOCKERFILE    = WORKSPACE / "devops/aws/Dockerfile"
DEVOPS_GCLOUD_DOCKERFILE = WORKSPACE / "devops/gcloud/Dockerfile"


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


def update_file(path, pattern, replacement):
    """Replace first regex match in file. Returns True if content changed."""
    content = path.read_text()
    new_content, count = re.subn(pattern, replacement, content, count=1)
    if count == 0:
        raise RuntimeError(f"Pattern {pattern!r} not found in {path}")
    if new_content == content:
        return False
    path.write_text(new_content)
    return True


def today_yymmdd():
    """Return today's date as YYMMDD string."""
    return date.today().strftime("%y%m%d")


def update_version_label(path, version):
    """Update LABEL version in a Dockerfile."""
    return update_file(path, r'LABEL version="[^"]*"', f'LABEL version="{version}"')


def update_or_add_jcroots_upgrade(path, version):
    """Update ENV JCROOTS_UPGRADE in a Dockerfile, or add it after LABEL version."""
    content = path.read_text()
    if re.search(r"ENV JCROOTS_UPGRADE=\S+", content):
        return update_file(path, r"ENV JCROOTS_UPGRADE=\S+", f"ENV JCROOTS_UPGRADE={version}")
    new_content, count = re.subn(
        r'(LABEL version="[^"]*")',
        rf'\1\nENV JCROOTS_UPGRADE={version}',
        content,
        count=1,
    )
    if count == 0:
        raise RuntimeError(f"LABEL version not found in {path}")
    if new_content == content:
        return False
    path.write_text(new_content)
    return True


# ---------------------------------------------------------------------------
# Per-tool check + update logic
# ---------------------------------------------------------------------------

def check(name, current, latest, path, search_pattern, replacement):
    if current == latest:
        print(f"  ok        {current}")
        return False
    print(f"  outdated  {current} -> {latest}")
    changed = update_file(path, search_pattern, replacement)
    if changed:
        print(f"  updated   {path.relative_to(WORKSPACE)}")
    return changed


def run_terraform():
    print("[terraform]")
    current = read_current(TERRAFORM_SCRIPT, r"TF_VERSION='([^']+)'")
    latest  = get_latest_terraform()
    return check(
        "terraform", current, latest,
        TERRAFORM_SCRIPT,
        r"TF_VERSION='[^']+'",
        f"TF_VERSION='{latest}'",
    )


def run_debian_forky():
    print("[debian forky slim]")
    current = read_current(FORKY_DOCKERFILE, r"FROM debian:(\S+)")
    latest  = get_latest_debian_forky_slim()
    changed = check(
        "debian", current, latest,
        FORKY_DOCKERFILE,
        r"FROM debian:\S+",
        f"FROM debian:{latest}",
    )
    if changed:
        version = today_yymmdd()
        update_version_label(FORKY_DOCKERFILE, version)
        update_or_add_jcroots_upgrade(FORKY_DOCKERFILE, version)
    return changed


def run_debian_bookworm():
    print("[debian bookworm slim]")
    current = read_current(BOOKWORM_DOCKERFILE, r"FROM debian:(\S+)")
    latest  = get_latest_debian_bookworm_slim()
    changed = check(
        "debian", current, latest,
        BOOKWORM_DOCKERFILE,
        r"FROM debian:\S+",
        f"FROM debian:{latest}",
    )
    if changed:
        version = today_yymmdd()
        update_version_label(BOOKWORM_DOCKERFILE, version)
        update_or_add_jcroots_upgrade(BOOKWORM_DOCKERFILE, version)
    return changed


def run_devops(version):
    any_updated = False
    for path, image in [
        (DEVOPS_AWS_DOCKERFILE,    "aws"),
        (DEVOPS_GCLOUD_DOCKERFILE, "gcloud"),
    ]:
        print(f"[devops {image}]")
        current = read_current(path, rf"FROM ghcr\.io/jcroots/devops/{image}-(\S+):latest")
        changed_from = update_file(
            path,
            rf"FROM ghcr\.io/jcroots/devops/{image}-\S+:latest",
            f"FROM ghcr.io/jcroots/devops/{image}-{version}:latest",
        )
        changed_env = update_file(
            path,
            r"ENV JCROOTS_UPGRADE=\S+",
            f"ENV JCROOTS_UPGRADE={version}",
        )
        changed_label = update_version_label(path, today_yymmdd())
        changed = changed_from or changed_env or changed_label
        if current == version:
            print(f"  ok        {current}")
        else:
            print(f"  outdated  {current} -> {version}")
            if changed:
                print(f"  updated   {path.relative_to(WORKSPACE)}")
        any_updated = any_updated or changed
        print()
    return any_updated


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

CHECKS = [
    run_terraform,
    run_debian_forky,
    run_debian_bookworm,
]


def main():
    args = sys.argv[1:]

    devops_version = None
    if "--devops" in args:
        idx = args.index("--devops")
        if idx + 1 >= len(args) or args[idx + 1].startswith("--"):
            print("ERROR: --devops requires a version argument", file=sys.stderr)
            sys.exit(1)
        devops_version = args[idx + 1]

    any_updated = False
    any_error   = False

    if devops_version:
        try:
            updated = run_devops(devops_version)
            any_updated = any_updated or updated
        except Exception as e:
            print(f"  ERROR: {e}")
            any_error = True
    else:
        print("[devops] skipped (no --devops VERSION provided)\n")

    for fn in CHECKS:
        try:
            updated = fn()
            any_updated = any_updated or updated
        except Exception as e:
            print(f"  ERROR: {e}")
            any_error = True
        print()

    if any_error:
        print("Finished with errors.")
        sys.exit(1)
    elif any_updated:
        print("All updates applied.")
    else:
        print("Everything is up to date.")


if __name__ == "__main__":
    main()
