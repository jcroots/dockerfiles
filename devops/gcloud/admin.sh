#!/bin/sh
set -eu

reponame=$(basename "${PWD}")
workspace="${HOME}/Workspace/devops/${reponame}"

devops_srcdir="${HOME}/Github/jcroots/devops/aws/opt/devops"

test -d "${devops_srcdir}" || {
	echo "${devops_srcdir}: dir not found" >&2
	exit 9
}

mkdir -vp "${workspace}"
mkdir -vp "${workspace}/config/gcloud"

exec docker run -it --rm -u admin \
    --name "admin-gcloud-${reponame}" \
    --hostname "${reponame}.admin-gcloud.local" \
    -e "TERM=${TERM}" \
    -v "${devops_srcdir}:/opt/devops:ro" \
    -v "${workspace}/config/gcloud:/home/admin/.config/gcloud" \
    -v "${workspace}:/home/admin/workspace" \
    -v "${PWD}:/home/admin/src" \
    --workdir /home/admin/src \
    jcroots/admin-gcloud
