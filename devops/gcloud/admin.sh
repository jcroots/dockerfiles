#!/bin/sh
set -eu
reponame=$(basename "${PWD}")
workspace="${HOME}/Workspace/devops/${reponame}"
mkdir -vp "${workspace}/docker/config/gcloud"
exec docker run -it --rm -u admin \
    --name "admin-gcloud-${reponame}" \
    --hostname "${reponame}.admin-gcloud.local" \
    -e "TERM=${TERM}" \
    -v "${PWD}/docker/config/gcloud:/home/admin/.config/gcloud" \
    -v "${PWD}:/home/admin/src" \
    --workdir /home/admin/src \
    jcroots/admin-gcloud
