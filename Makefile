.PHONY: all
all:
	$(MAKE) -j2 debian devops brew

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

.PHONY: brew
brew: debian/forky
	cd brew && ./build.sh

.PHONY: check
check:
	@find . -type f -name '*.sh' | xargs shellcheck
