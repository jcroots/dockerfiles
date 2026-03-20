#!/bin/bash
set -eu

user=$(id -u -n)

workspace="${HOME}/Workspace"
github="${HOME}/Github"
temp="${HOME}/Temp"

install -v -d -m 0750 "${workspace}"
install -v -d -m 0750 "${github}"
install -v -d -m 0750 "${temp}"

cfgdir="${HOME}/Workspace/docker/dockerfiles/claude"
install -v -d -m 0750 "${cfgdir}"
install -v -d -m 0750 "${cfgdir}/config"

if ! test -s "${cfgdir}/claude.json"; then
	touch "${cfgdir}/claude.json"
fi

exec docker run -it --rm -u "${user}" \
	--name "claude-devops-${user}" \
	--hostname "claude-devops.debian.local" \
	-e "TERM=${TERM}" \
	-v "${cfgdir}/config:/home/${user}/.claude" \
	-v "${cfgdir}/claude.json:/home/${user}/.claude.json" \
	-v "${workspace}:/home/${user}/workspace:ro" \
	-v "${github}:/home/${user}/github" \
	-v "${temp}:/home/${user}/temp" \
	--workdir "/home/${user}" \
	jcroots/claude-devops
