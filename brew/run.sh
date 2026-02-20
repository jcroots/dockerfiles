#!/bin/sh
set -eu
user=$(id -u -n)
exec docker run -it --rm -u "${user}" \
    --name "brew-${user}" \
    --hostname brew.debian.local \
    -e "TERM=${TERM}" \
    -v "${PWD}:/home/${user}/workspace:ro" \
    jcroots/brew
