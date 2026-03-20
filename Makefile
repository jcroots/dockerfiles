.PHONY: all
all:
	$(MAKE) -j2 debian/forky debian/bookworm
	$(MAKE) -j2 devops/aws devops/gcloud
	$(MAKE) brew
	$(MAKE) claude
	$(MAKE) claude-devops

# devops

.PHONY: devops
devops:
	$(MAKE) -j2 devops/aws devops/gcloud

.PHONY: devops/gcloud
devops/gcloud:
	cd devops/gcloud && ./build.sh

.PHONY: devops/aws
devops/aws:
	cd devops/aws && ./build.sh

# debian

.PHONY: debian
debian:
	$(MAKE) -j2 debian/forky debian/bookworm

.PHONY: debian/bookworm
debian/bookworm:
	cd debian/bookworm && ./build.sh

.PHONY: debian/forky
debian/forky:
	cd debian/forky && ./build.sh

# brew

.PHONY: brew
brew:
	cd brew && ./build.sh

# claude

.PHONY: claude-all
claude-all:
	$(MAKE) claude
	$(MAKE) claude-devops

.PHONY: claude
claude:
	cd claude/claude && ./build.sh

.PHONY: claude-devops
claude-devops:
	cd claude/claude-devops && ./build.sh

# utils

.PHONY: prune
prune:
	docker system prune --force

.PHONY: check
check:
	@find . -type f -name '*.sh' | xargs shellcheck
	@shellcheck -s bash brew/bashrc.brew
	@python3 -m py_compile upgrade.py && rm -rf __pycache__
