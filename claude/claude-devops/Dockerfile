FROM jcroots/claude

LABEL maintainer="Jeremías Casteglione <jeremias.rootstrap@gmail.com>"
LABEL version="260319"

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

COPY --chmod=755 terraform-install.sh /tmp/terraform-install.sh
RUN /tmp/terraform-install.sh

ARG USER_NAME=jcroots

ENV USER_NAME=${USER_NAME}

USER ${USER_NAME}:${USER_NAME}
WORKDIR /home/${USER_NAME}

ENV USER=${USER_NAME}
ENV HOME=/home/${USER_NAME}

COPY --chmod=644 brew.install /tmp/brew.install

RUN brew update \
	&& cat /tmp/brew.install | xargs brew install \
	&& brew autoremove \
	&& brew cleanup --prune=all

ENTRYPOINT ["/usr/local/bin/user-login.sh"]
