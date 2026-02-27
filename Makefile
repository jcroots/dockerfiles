.PHONY: all
all:
	$(MAKE) -j2 debian devops
	$(MAKE) brew-all

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
	$(MAKE) debian/forky

.PHONY: debian/forky
debian/forky:
	cd debian/forky && ./build.sh

# brew

.PHONY: brew-all
brew-all:
	$(MAKE) brew
	$(MAKE) claude

.PHONY: brew
brew:
	cd brew && ./build.sh

.PHONY: claude
claude:
	cd claude && ./build.sh

# utils

.PHONY: prune
prune:
	docker system prune --force

.PHONY: check
check:
	@find . -type f -name '*.sh' | xargs shellcheck
