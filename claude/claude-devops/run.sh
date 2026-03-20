#!/bin/bash
set -eu
user=$(id -u -n)
cfgdir="${HOME}/Workspace/docker/dockerfiles/claude"
install -v -d -m 0750 "${cfgdir}"
install -v -d -m 0750 "${cfgdir}/config"
if ! test -s "${cfgdir}/config/claude.json"; then
	touch "${cfgdir}/config/claude.json"
fi
slug="$(echo -n "$(basename "${PWD}")" | tr '[:space:]' '-')"
exec docker run -it --rm -u "${user}" \
	--name "claude-devops-${slug}" \
	--hostname "claude-devops-${slug}.debian.local" \
	-e "TERM=${TERM}" \
	-v "${cfgdir}/config:/home/${user}/.claude" \
	-v "${cfgdir}/claude.json:/home/${user}/.claude.json" \
	-v "${PWD}:/home/${user}/workspace" \
	--workdir "/home/${user}/workspace" \
	jcroots/claude-devops
