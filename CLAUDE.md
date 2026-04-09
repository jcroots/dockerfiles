# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Layered Docker image build system producing development and DevOps container environments. Images are tagged as `jcroots/<name>` and map the host user's UID/GID into containers for seamless filesystem access.

## Image Hierarchy

```
debian:forky-*-slim  ->  jcroots/forky  ->  jcroots/brew  ->  jcroots/claude  ->  jcroots/claude-devops
debian:bookworm-*-slim  ->  jcroots/bookworm
ghcr.io/jcroots/devops/aws-*  ->  jcroots/admin-aws
ghcr.io/jcroots/devops/gcloud-*  ->  jcroots/admin-gcloud
```

Build order matters: each image depends on its parent. The `make all` target handles this correctly.

## Build Commands

```bash
make all            # Full build (debian -> devops -> brew -> claude -> claude-devops)
make debian         # Both debian variants (parallel)
make devops         # AWS + GCloud admin images (parallel)
make brew           # Homebrew layer
make claude         # Claude dev environment
make claude-devops  # Claude DevOps environment
make claude-all     # brew + claude + claude-devops in sequence
make check          # Shellcheck all .sh files + py_compile upgrade.py + upgrade-all.py
make prune          # docker system prune --force
```

Individual images: `cd <dir> && ./build.sh` (each build.sh captures current user UID/GID as build args).

## Version Upgrades

`upgrade.py` checks upstream versions (Terraform, Debian tags) and patches Dockerfiles in-place:

```bash
python3 upgrade.py                        # Auto-upgrade Terraform + Debian base tags
python3 upgrade.py --dry-run              # Check only, no file changes
```

Updates `FROM` tags, `LABEL version=`, and `ENV JCROOTS_UPGRADE=` fields in the debian and terraform targets. Version labels use `YYMMDD` format.

`upgrade-all.py` orchestrates upgrades across all personal project repos (`devops`, `devops-vm`, `dockerfiles`) in dependency order:

```bash
python3 upgrade-all.py            # upgrade all repos (or: make upgrade-all)
python3 upgrade-all.py --dry-run  # check only, no file changes or builds
```

Pre-flight checks verify all repos are clean and on `main` before proceeding. Runs `upgrade.py` + `make` (if modified) on each dependency repo first, then on `dockerfiles`.

## Conventions

- Each image directory contains: `Dockerfile`, `build.sh`, and package lists (`apt.install`, optionally `brew.install`)
- `apt.install` / `brew.install` are newline-separated package lists read via `cat ... | xargs`
- `run.sh` scripts create host directories and launch containers with volume mounts (workspace, github, temp)
- Container data persists at `~/Docker/dockerfiles/claude/` on the host
- All shell scripts use `set -eu`; scripts are checked with `shellcheck`
- The `user-login.sh` entrypoint is shared across debian-based images

## Documentation Maintenance

When making changes to this repository, update `CLAUDE.md` and/or `README.md` if the changes affect:
- The image hierarchy (new images, changed base images, removed images)
- Build commands or Makefile targets
- `upgrade.py` behavior or flags
- Conventions (new file patterns, entrypoint changes, volume mount changes)
- The images table in README.md (new/renamed/removed images)
