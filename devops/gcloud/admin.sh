#!/usr/bin/env bash
set -eu

reponame=$(basename "$(dirname "${PWD}")")/$(basename "${PWD}")
reposlug=$(echo "${reponame}" | tr '/' '-')
echo "Repo: ${reponame} (${reposlug})"

workspace="${HOME}/Workspace/docker/${reponame}"
echo "Workspace: ${workspace}"

devops_srcdir="${HOME}/Github/jcroots/devops/gcloud/opt/devops"
echo "Devops: ${devops_srcdir}"

test -d "${devops_srcdir}" || {
	echo "${devops_srcdir}: dir not found" >&2
	exit 9
}

mkdir -vp "${workspace}"
mkdir -vp "${workspace}/config/gcloud"

exec docker run -it --rm -u admin \
    --name "admin-gcloud-${reposlug}" \
    --hostname "${reposlug}-gcloud.devops.local" \
    -e "TERM=${TERM}" \
    -v "${devops_srcdir}:/opt/devops:ro" \
    -v "${workspace}/config/gcloud:/home/admin/.config/gcloud" \
    -v "${workspace}:/home/admin/workspace" \
    -v "${PWD}:/home/admin/src" \
    --workdir /home/admin/src \
    jcroots/admin-gcloud
