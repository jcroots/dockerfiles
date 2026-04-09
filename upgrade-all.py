#!/usr/bin/env python3
"""Upgrade all personal project repositories in dependency order."""

import subprocess
import sys
from pathlib import Path

PARENT_DIR = Path(__file__).resolve().parent.parent

DEPENDENCY_REPOS = [
    {"name": "devops", "make_target": "all"},
    {"name": "devops-vm", "make_target": "docker"},
]

SELF_REPO = {"name": "dockerfiles", "make_target": "all"}


def git(repo_path, *args):
    """Run a read-only git command and return stdout."""
    result = subprocess.run(
        ["git", *args],
        cwd=repo_path,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def check_repo(repo_path, name):
    """Verify repo exists, is on main branch, and has no local modifications."""
    if not repo_path.is_dir():
        raise RuntimeError(f"{name}: directory not found at {repo_path}")

    branch = git(repo_path, "rev-parse", "--abbrev-ref", "HEAD")
    if branch != "main":
        raise RuntimeError(f"{name}: checked out on '{branch}', expected 'main'")

    status = git(repo_path, "status", "--porcelain")
    if status:
        raise RuntimeError(f"{name}: has local modifications\n{status}")


def has_modifications(repo_path):
    """Check if repo has uncommitted changes after upgrade."""
    return bool(git(repo_path, "status", "--porcelain"))


def process_repo(repo_path, name, make_target, dry_run, force_build=False):
    """Run upgrade.py and optionally make if files changed. Returns True if built."""
    print(f"\n{'=' * 60}")
    print(f"  Upgrading {name}")
    print(f"{'=' * 60}\n")

    cmd = [sys.executable, "upgrade.py"]
    if dry_run:
        cmd.append("--dry-run")
    subprocess.run(cmd, cwd=repo_path, check=True)

    if dry_run:
        return False

    modified = has_modifications(repo_path)
    needs_build = modified or force_build

    if needs_build:
        reason = "files modified" if modified else "dependency rebuilt"
        print(f"\n  Building {name} (make {make_target}) [{reason}]...\n")
        subprocess.run(
            ["make", make_target],
            cwd=repo_path,
            check=True,
        )
        return True

    print(f"\n  No changes in {name}, skipping build.")
    return False


def main():
    dry_run = "--dry-run" in sys.argv
    all_repos = DEPENDENCY_REPOS + [SELF_REPO]

    if dry_run:
        print("=== DRY-RUN mode: no files will be modified, no builds will run ===\n")

    # Phase 1: pre-flight checks
    print("Checking all repositories...\n")
    for repo_config in all_repos:
        name = repo_config["name"]
        repo_path = PARENT_DIR / name
        check_repo(repo_path, name)
        print(f"  {name}: ok")

    # Phase 2: process all repos in dependency order, propagating builds
    modified = []
    any_built = False
    for repo_config in all_repos:
        name = repo_config["name"]
        repo_path = PARENT_DIR / name
        built = process_repo(
            repo_path, name, repo_config["make_target"], dry_run, any_built,
        )
        if built:
            modified.append(name)
            any_built = True

    print(f"\n{'=' * 60}")
    print("  All upgrades complete.")
    print(f"{'=' * 60}")

    if modified:
        print(f"\n  Repos with upgrades to commit, push, and release:")
        for name in modified:
            print(f"    - {name}")
    else:
        print(f"\n  No repos were modified.")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(f"\nERROR: command failed with exit code {e.returncode}: {e.cmd}")
        sys.exit(1)
    except RuntimeError as e:
        print(f"\nERROR: {e}")
        sys.exit(1)
