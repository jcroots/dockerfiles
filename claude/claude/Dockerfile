FROM jcroots/brew

LABEL maintainer="Jeremías Casteglione <jeremias.rootstrap@gmail.com>"
LABEL version="260402"

ENV JCROOTS_UPGRADE=260402

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
		/var/cache/apt/*cache.bin \
		/tmp/apt.install

ARG USER_NAME=jcroots

ENV USER_NAME=${USER_NAME}

COPY --chmod=644 brew.install /tmp/brew.install
RUN chown ${USER_NAME}:${USER_NAME} /tmp/brew.install

USER ${USER_NAME}:${USER_NAME}
WORKDIR /home/${USER_NAME}

ENV USER=${USER_NAME}
ENV HOME=/home/${USER_NAME}

RUN brew update \
	&& cat /tmp/brew.install | xargs brew install \
	&& brew autoremove \
	&& brew cleanup --prune=all \
	&& rm -vf /tmp/brew.install

RUN git config --global alias.st status

ENTRYPOINT ["/usr/local/bin/user-login.sh"]
