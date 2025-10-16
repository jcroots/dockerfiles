.PHONY: all
all: debian/forky devops/gcloud devops/aws

.PHONY: debian/forky
debian/forky:
	cd debian/forky && ./build.sh

.PHONY: devops/gcloud
devops/gcloud:
	cd devops/gcloud && ./build.sh

.PHONY: devops/aws
devops/aws:
	cd devops/aws && ./build.sh
