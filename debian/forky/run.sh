#!/bin/sh
set -eu
exec docker run -it --rm -u jrms \
    --name debian-forky \
    --hostname forky.local \
    jcroots/forky
