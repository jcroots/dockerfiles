#!/bin/sh
set -eu
user=$(id -u -n)
workspace="${HOME}/Workspace"
mkdir -vp "${workspace}"
exec docker run -it --rm -u "${user}" \
    --name "debian-forky-${user}" \
    --hostname forky.debian.local \
    -e "TERM=${TERM}" \
    -v "${workspace}:/home/${user}/workspace" \
    jcroots/forky
