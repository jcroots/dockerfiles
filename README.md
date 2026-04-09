# Dockerfiles

Layered Docker images for development and DevOps environments. Each image
builds on a parent, mapping the host user's UID/GID into the container so
files created inside have correct ownership on the host.

## Images

| Image | Base | Purpose |
|-------|------|---------|
| [debian/forky](./debian/forky/Dockerfile) | `debian:forky-*-slim` | Minimal Debian base with sudo and user setup |
| [debian/bookworm](./debian/bookworm/Dockerfile) | `debian:bookworm-*-slim` | Bookworm variant of the Debian base |
| [brew](./brew/Dockerfile) | `jcroots/forky` | Adds Homebrew package manager |
| [claude](./claude/claude/Dockerfile) | `jcroots/brew` | Development environment (Python, Go, Claude Code, uv) |
| [claude-devops](./claude/claude-devops/Dockerfile) | `jcroots/claude` | DevOps tools (Terraform, AWS CLI, GCloud CLI, Typst) |
| [devops/aws](./devops/aws/Dockerfile) | `jcroots/devops-aws` | AWS admin container |
| [devops/gcloud](./devops/gcloud/Dockerfile) | `jcroots/devops-gcloud` | GCloud admin container |

## Build

```bash
make all            # full build in dependency order
make check          # shellcheck + py_compile
```

Individual images can be built with `cd <dir> && ./build.sh`. Claude and
devops images have `run.sh` scripts that launch containers with workspace
volume mounts.

## Version Upgrades

```bash
python3 upgrade.py                        # upgrade Terraform + Debian base tags
python3 upgrade-all.py                    # upgrade all repos (devops, devops-vm, dockerfiles)
```

## License

[BSD 3-Clause](./LICENSE)
