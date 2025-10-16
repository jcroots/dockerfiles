.PHONY: all
all:
	$(MAKE) -j2 debian/forky devops

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

.PHONY: check
check:
	@shellcheck */*/*.sh
