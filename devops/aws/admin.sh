#!/bin/sh
set -eu

reponame=$(basename "${PWD}")
workspace="${HOME}/Workspace/devops/${reponame}"

devops_srcdir="${HOME}/Github/jcroots/devops/aws/opt/devops"

mkdir -vp "${workspace}/docker/config/aws"

exec docker run -it --rm -u admin \
    --name "admin-aws-${reponame}" \
    --hostname "${reponame}.admin-aws.local" \
    -v "${devops_srcdir}:/opt/devops" \
    -v "${workspace}/docker/config/aws:/home/admin/.config/aws" \
    -v "${PWD}:/home/admin/src" \
    --workdir /home/admin/src \
    jcroots/admin-aws
