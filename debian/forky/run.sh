#!/bin/sh
set -eu
workspace="${HOME}/Workspace/debian"
mkdir -vp "${workspace}"
exec docker run -it --rm -u jrms \
    --name debian-forky \
    --hostname forky.debian.local \
    -v "${workspace}:/home/jrms/workspace" \
    jcroots/forky
