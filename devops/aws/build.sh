#!/bin/sh
set -eu

_UID=$(id -u)
_GID=$(id -g)

exec docker build --rm --pull \
    --build-arg "ADMIN_UID=${_UID}" \
    --build-arg "ADMIN_GID=${_GID}" \
    -t jcroots/admin-aws .
