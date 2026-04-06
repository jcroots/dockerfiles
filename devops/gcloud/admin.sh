#!/usr/bin/env bash
set -eu

reponame=$(basename "$(dirname "${PWD}")")/$(basename "${PWD}")
reposlug=$(echo "${reponame}" | tr '/' '-')

claude="${HOME}/Docker/dockerfiles/claude"
install -v -d -m 0750 "${claude}"
install -v -d -m 0750 "${claude}/config"
if ! test -s "${claude}/claude.json"; then
	touch "${claude}/claude.json"
fi
echo "Claude: ${claude}"

workspace="${HOME}/Docker/devops/${reponame}"
echo "Workspace: ${workspace}"

mkdir -vp "${workspace}"
mkdir -vp "${workspace}/config/gcloud"

echo "Admin: gcloud ${reponame}"

exec docker run -it --rm -u admin \
    --name "admin-gcloud-${reposlug}" \
    --hostname "${reposlug}-gcloud.devops.local" \
    -e "TERM=${TERM}" \
	-v "${claude}/config:/home/admin/.claude" \
	-v "${claude}/claude.json:/home/admin/.claude.json" \
    -v "${workspace}/config/gcloud:/home/admin/.config/gcloud" \
    -v "${workspace}:/home/admin/workspace" \
    -v "${PWD}:/home/admin/src" \
    --workdir /home/admin/src \
    jcroots/admin-gcloud
