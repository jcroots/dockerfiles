#!/bin/sh
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

devops_srcdir="${HOME}/Github/jcroots/devops/opt/devops"
echo "Devops: ${devops_srcdir}"

test -d "${devops_srcdir}" || {
	echo "${devops_srcdir}: dir not found" >&2
	exit 9
}

mkdir -vp "${workspace}"
mkdir -vp "${workspace}/config/aws"

echo "Admin: aws ${reponame}"

exec docker run -it --rm -u admin \
    --name "admin-aws-${reposlug}" \
    --hostname "${reposlug}-aws.devops.local" \
    -e "TERM=${TERM}" \
	-v "${claude}/config:/home/admin/.claude" \
	-v "${claude}/claude.json:/home/admin/.claude.json" \
    -v "${devops_srcdir}:/opt/devops:ro" \
    -v "${workspace}/config/aws:/home/admin/.aws" \
    -v "${workspace}:/home/admin/workspace" \
    -v "${PWD}:/home/admin/src" \
    --workdir /home/admin/src \
    jcroots/admin-aws
