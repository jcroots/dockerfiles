#!/bin/sh
set -eu

_UID=$(id -u)
_GID=$(id -g)

exec docker build --rm \
    --build-arg "JRMS_UID=${_UID}" \
    --build-arg "JRMS_GID=${_GID}" \
    -t jcroots/forky .
