#!/bin/sh
set -eu
exec docker run -it --rm -u admin \
    --name admin-aws \
    --hostname aws.local \
    -v "${PWD}:/home/admin/src" \
    --workdir /home/admin/src \
    jcroots/admin-aws
