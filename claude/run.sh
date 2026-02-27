#!/bin/sh
set -eu
user=$(id -u -n)
cfgdir="${HOME}/Workspace/docker/dockerfiles/claude"
install -v -d -m 0750 "${cfgdir}"
install -v -d -m 0750 "${cfgdir}/config"
if ! test -s "${cfgdir}/config/claude.json"; then
    touch "${cfgdir}/config/claude.json"
fi
exec docker run -it --rm -u "${user}" \
    --name "claude-${user}" \
    --hostname claude.debian.local \
    -e "TERM=${TERM}" \
    -v "${cfgdir}/config:/home/${user}/.claude" \
    -v "${cfgdir}/claude.json:/home/${user}/.claude.json" \
    -v "${PWD}:/home/${user}/workspace" \
	--workdir "/home/${user}/workspace" \
    jcroots/claude
