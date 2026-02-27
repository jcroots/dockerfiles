FROM jcroots/brew

LABEL maintainer="Jeremías Casteglione <jeremias.rootstrap@gmail.com>"
LABEL version="260227"

USER root:root
WORKDIR /root

ENV USER=root
ENV HOME=/root

ENV DEBIAN_FRONTEND=noninteractive

COPY apt.install /tmp/apt.install

RUN apt-get clean \
	&& apt-get update -yy \
	&& cat /tmp/apt.install | xargs apt-get install -yy --no-install-recommends \
	&& apt-get clean \
	&& apt-get autoremove -yy --purge \
	&& rm -rf /var/lib/apt/lists/* \
		/var/cache/apt/archives/*.deb \
		/var/cache/apt/*cache.bin

ARG USER_NAME=jcroots

ENV USER_NAME=${USER_NAME}

USER ${USER_NAME}:${USER_NAME}
WORKDIR /home/${USER_NAME}

ENV USER=${USER_NAME}
ENV HOME=/home/${USER_NAME}

RUN brew update \
	&& brew install claude-code \
	&& brew cleanup --prune=all

ENTRYPOINT ["/usr/local/bin/user-login.sh"]
