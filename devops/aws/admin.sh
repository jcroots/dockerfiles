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
mkdir -vp "${workspace}/config/aws"

exec docker run -it --rm -u admin \
    --name "admin-aws-${reponame}" \
    --hostname "${reponame}.admin-aws.local" \
    -e "TERM=${TERM}" \
    -v "${devops_srcdir}:/opt/devops:ro" \
    -v "${workspace}/config/aws:/home/admin/.config/aws" \
    -v "${workspace}:/home/admin/workspace" \
    -v "${PWD}:/home/admin/src" \
    --workdir /home/admin/src \
    jcroots/admin-aws
