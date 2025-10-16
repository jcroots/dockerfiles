#!/bin/sh
set -eu
mkdir -vp ${PWD}/docker/config/gcloud
exec docker run -it --rm -u admin \
    --name admin-gcloud \
    --hostname gcloud.local \
    -v "${PWD}/docker/config/gcloud:/home/admin/.config/gcloud" \
    -v "${PWD}:/home/admin/src" \
    --workdir /home/admin/src \
    jcroots/admin-gcloud
