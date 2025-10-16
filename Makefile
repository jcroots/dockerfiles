.PHONY: all
all: debian/forky devops/gcloud

.PHONY: debian/forky
debian/forky:
	cd debian/forky && ./build.sh

.PHONY: devops/gcloud
devops/gcloud:
	cd devops/gcloud && ./build.sh
