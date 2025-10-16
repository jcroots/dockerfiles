#!/usr/bin/env bash
set -eu
srcdir="$(dirname "$(dirname "$(realpath "$0")")")/aws"
admin="${srcdir}/admin.sh"
test -x "${admin}" || {
	echo "${admin}: not found or not executable" >&2
	exit 9
}
echo "Run: ${admin}"
exec "${admin}"
