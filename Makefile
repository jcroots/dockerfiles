.PHONY: all
all:
	$(MAKE) -j3 debian devops
	$(MAKE) brew-all

.PHONY: prune
prune:
	docker system prune --all --force

.PHONY: debian
debian: debian/forky

.PHONY: debian/forky
debian/forky:
	cd debian/forky && ./build.sh

.PHONY: devops
devops:
	$(MAKE) -j2 devops/aws devops/gcloud

.PHONY: devops/gcloud
devops/gcloud:
	cd devops/gcloud && ./build.sh

.PHONY: devops/aws
devops/aws:
	cd devops/aws && ./build.sh

.PHONY: brew-all
brew-all: brew
	$(MAKE) claude

.PHONY: brew
brew: debian/forky
	cd brew && ./build.sh

.PHONY: claude
claude: brew
	cd claude && ./build.sh

.PHONY: check
check:
	@find . -type f -name '*.sh' | xargs shellcheck
